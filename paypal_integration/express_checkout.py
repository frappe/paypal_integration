# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# See license.txt

from __future__ import unicode_literals
import requests
import frappe
from frappe.utils import get_url
from urllib import urlencode
import urlparse, json

"""
Paypal Express Checkout using classic API

For full workflow:

https://developer.paypal.com/docs/classic/express-checkout/ht_ec-singleItemPayment-curl-etc/
"""

class PaypalException(Exception): pass

@frappe.whitelist(allow_guest=True, xss_safe=True)
def set_express_checkout(amount, currency="USD", data=None):
	if not isinstance(data, basestring):
		data = json.dumps(data or "{}")

	response = execute_set_express_checkout(amount, currency)

	if frappe.conf.paypal_sandbox:
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
		"data": data
	})
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

	paypal_express_payment = frappe.get_doc("Paypal Express Payment", token)
	paypal_express_payment.payerid = response.get("PAYERID")[0]
	paypal_express_payment.status = "Verified"
	paypal_express_payment.save(ignore_permissions=True)
	frappe.db.commit()

	frappe.local.response["type"] = "redirect"
	frappe.local.response["location"] = get_url("/paypal-express-confirm?token=" \
		+ paypal_express_payment.token)

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

	try:
		get_api_response(params)

		paypal_express_payment = frappe.get_doc("Paypal Express Payment", token)
		paypal_express_payment.status = "Completed"
		paypal_express_payment.save(ignore_permissions=True)
		frappe.db.commit()

		frappe.local.response["type"] = "redirect"
		frappe.local.response["location"] = get_url("/paypal-express-success")
	except PaypalException:
		frappe.local.response["type"] = "redirect"
		frappe.local.response["location"] = get_url("/paypal-express-cancel")


def get_paypal_params():
	return {
		"USER": frappe.conf.paypal_username,
		"PWD": frappe.conf.paypal_password,
		"SIGNATURE": frappe.conf.paypal_signature,
		"VERSION": "98"
	}

def get_api_url():
	if frappe.conf.paypal_sandbox:
		return "https://api-3t.sandbox.paypal.com/nvp"
	else:
		return "https://api-3t.paypal.com/nvp"

def get_api_response(params):
	response = requests.post(get_api_url(), data=params)
	response = urlparse.parse_qs(response.text)
	if response.get("ACK")[0]=="Success":
		return response
	else:
		print response
		raise PaypalException
