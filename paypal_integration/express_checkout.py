# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# See license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import get_url
from urllib import urlencode
import urlparse, json
from frappe import _
from frappe.utils import get_request_session

"""
Paypal Express Checkout using classic API

For full workflow:

https://developer.paypal.com/docs/classic/express-checkout/ht_ec-singleItemPayment-curl-etc/
"""

@frappe.whitelist(allow_guest=True, xss_safe=True)
def set_express_checkout(amount, currency="USD", data=None):
	validate_transaction_currency(currency)

	if not isinstance(data, basestring):
		data = json.dumps(data or "{}")

	response = execute_set_express_checkout(amount, currency)

	if not response["success"]:
		paypal_log(response)
		frappe.db.commit()

		frappe.respond_as_web_page(_("Something went wrong"),
			_("Looks like something is wrong with this site's Paypal configuration. Don't worry! No payment has been made from your Paypal account."),
			success=False,
			http_status_code=frappe.ValidationError.http_status_code)

		return

	paypal_settings = get_paypal_settings()
	if paypal_settings.paypal_sandbox:
		return_url = "https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_express-checkout&token={0}"
	else:
		return_url = "https://www.paypal.com/cgi-bin/webscr?cmd=_express-checkout&token={0}"

	token = response.get("TOKEN")[0]
	paypal_express_payment = frappe.get_doc({
		"doctype": "Paypal Express Payment",
		"status": "Started",
		"amount": amount,
		"currency": currency,
		"token": token,
		"data": data,
		"correlation_id": response.get("CORRELATIONID")[0]
	})
	if data:
		if isinstance(data, basestring):
			data = json.loads(data)

		if data.get("doctype") and data.get("docname"):
			paypal_express_payment.reference_doctype = data.get("doctype")
			paypal_express_payment.reference_docname = data.get("docname")

	paypal_express_payment.insert(ignore_permissions = True)
	frappe.db.commit()

	frappe.local.response["type"] = "redirect"
	frappe.local.response["location"] = return_url.format(token)

def execute_set_express_checkout(amount, currency):
	params = get_paypal_params()
	params.update({
		"METHOD": "SetExpressCheckout",
		"PAYMENTREQUEST_0_PAYMENTACTION": "SALE",
		"PAYMENTREQUEST_0_AMT": amount,
		"PAYMENTREQUEST_0_CURRENCYCODE": currency
	})

	return_url = get_url("/api/method/paypal_integration.express_checkout.get_express_checkout_details")

	params = urlencode(params) + \
		"&returnUrl={0}&cancelUrl={1}".format(return_url, get_url("/paypal-express-cancel"))

	return get_api_response(params.encode("utf-8"))

@frappe.whitelist(allow_guest=True, xss_safe=True)
def get_express_checkout_details(token):
	params = get_paypal_params()
	params.update({
		"METHOD": "GetExpressCheckoutDetails",
		"TOKEN": token
	})

	response = get_api_response(params)

	if not response["success"]:
		paypal_log(response, params)
		frappe.db.commit()

		frappe.respond_as_web_page(_("Something went wrong"),
			_("Looks like something went wrong during the transaction. Since we haven't confirmed the payment, Paypal will automatically refund you this amount. If it doesn't, please send us an email and mention the Correlation ID: {0}.").format(response.get("CORRELATIONID", [None])[0]),
			success=False,
			http_status_code=frappe.ValidationError.http_status_code)

		return

	paypal_express_payment = frappe.get_doc("Paypal Express Payment", token)
	paypal_express_payment.payerid = response.get("PAYERID")[0]
	paypal_express_payment.payer_email = response.get("EMAIL")[0]
	paypal_express_payment.status = "Verified"
	paypal_express_payment.save(ignore_permissions=True)
	frappe.db.commit()

	frappe.local.response["type"] = "redirect"
	frappe.local.response["location"] = get_url( \
		"/api/method/paypal_integration.express_checkout.confirm_payment?token="+paypal_express_payment.token)

@frappe.whitelist(allow_guest=True, xss_safe=True)
def confirm_payment(token):
	paypal_express_payment = frappe.get_doc("Paypal Express Payment", token)

	params = get_paypal_params()
	params.update({
		"METHOD": "DoExpressCheckoutPayment",
		"PAYERID": paypal_express_payment.payerid,
		"TOKEN": paypal_express_payment.token,
		"PAYMENTREQUEST_0_PAYMENTACTION": "SALE",
		"PAYMENTREQUEST_0_AMT": paypal_express_payment.amount,
		"PAYMENTREQUEST_0_CURRENCYCODE": paypal_express_payment.currency
	})

	response = get_api_response(params)

	if response["success"]:
		paypal_express_payment.status = "Completed"
		paypal_express_payment.transaction_id = response.get("PAYMENTINFO_0_TRANSACTIONID")[0]
		paypal_express_payment.correlation_id = response.get("CORRELATIONID")[0]
		paypal_express_payment.flags.redirect = True
		paypal_express_payment.flags.redirect_to = get_url("/paypal-express-success")
		paypal_express_payment.flags.status_changed_to = "Completed"
		paypal_express_payment.save(ignore_permissions=True)

	else:
		paypal_express_payment.status = "Failed"
		paypal_express_payment.flags.redirect = True
		paypal_express_payment.flags.redirect_to = get_url("/paypal-express-failed")
		paypal_express_payment.save(ignore_permissions=True)

		paypal_log(response, params)

	frappe.db.commit()

	# this is done so that functions called via hooks can update flags.redirect_to
	if paypal_express_payment.flags.redirect:
		frappe.local.response["type"] = "redirect"
		frappe.local.response["location"] = paypal_express_payment.flags.redirect_to

def get_paypal_params():
	paypal_settings = get_paypal_settings()
	if paypal_settings.api_username:
		return {
			"USER": paypal_settings.api_username,
			"PWD": paypal_settings.api_password,
			"SIGNATURE": paypal_settings.signature,
			"VERSION": "98"
		}

	else :
		return {
			"USER": frappe.conf.paypal_username,
			"PWD": frappe.conf.paypal_password,
			"SIGNATURE": frappe.conf.paypal_signature,
			"VERSION": "98"
		}

def get_api_url():
	paypal_settings = get_paypal_settings()
	if paypal_settings.paypal_sandbox:
		return "https://api-3t.sandbox.paypal.com/nvp"
	else:
		return "https://api-3t.paypal.com/nvp"

def get_api_response(params):
	s = get_request_session()
	response = s.post(get_api_url(), data=params)
	response = urlparse.parse_qs(response.text)
	response["success"] = response.get("ACK")[0]=="Success"
	return response

def get_paypal_settings():
	paypal_settings = frappe.get_doc("PayPal Settings")

	# update from site_config.json
	for key in ("paypal_sandbox", "paypal_username", "paypal_password", "paypal_signature"):
		if key in frappe.local.conf:
			paypal_settings.set(key, frappe.local.conf[key])

	return paypal_settings

def validate_transaction_currency(currency):
	if currency not in ["AUD", "BRL", "CAD", "CZK", "DKK", "EUR", "HKD", "HUF", "ILS", "JPY", "MYR", "MXN",
		"TWD", "NZD", "NOK", "PHP", "PLN", "GBP", "RUB", "SGD", "SEK", "CHF", "THB", "TRY", "USD"]:
		frappe.throw(_("Please select another payment method. PayPal does not support transactions in currency '{0}'").format(currency))

def paypal_log(response, params=None):
	frappe.get_doc({
		"doctype": "Paypal Log",
		"error": frappe.as_json(response),
		"params": frappe.as_json(params or "")
	}).insert(ignore_permissions=True)

def set_redirect(paypal_express_payment):
	"""ERPNext related redirects.
	   You need to set Paypal Express Payment.flags.redirect_to on status change.
	   Called via PaypalExpressPayment.on_update"""

	if "erpnext" not in frappe.get_installed_apps():
		return

	if not paypal_express_payment.flags.status_changed_to:
		return

	reference_doctype = paypal_express_payment.reference_doctype
	reference_docname = paypal_express_payment.reference_docname

	if not (reference_doctype and reference_docname):
		return

	reference_doc = frappe.get_doc(reference_doctype,  reference_docname)
	shopping_cart_settings = frappe.get_doc("Shopping Cart Settings")

	if paypal_express_payment.flags.status_changed_to == "Completed":
		reference_doc.run_method("set_as_paid")

		# if shopping cart enabled and in session
		if (shopping_cart_settings.enabled
			and hasattr(frappe.local, "session")
			and frappe.local.session.user != "Guest"):

			success_url = shopping_cart_settings.payment_success_url
			if success_url:
				paypal_express_payment.flags.redirect_to = ({
					"Orders": "orders",
					"Invoices": "invoices",
					"My Account": "me"
				}).get(success_url, "me")
			else:
				paypal_express_payment.flags.redirect_to = get_url("/orders/{0}".format(reference_doc.reference_name))

	elif paypal_express_payment.flags.status_changed_to == "Cancelled":
		reference_doc.run_method("set_as_cancelled")
