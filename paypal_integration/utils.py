import frappe
from frappe import _
from .express_checkout import set_express_checkout, validate_transaction_currency

def get_payment_url(doc, method):
	if doc.docstatus == 1:
		if doc.payment_gateway == "PayPal":
			set_express_checkout(doc.grand_total, doc.currency, {"doctype": doc.doctype, "docname": doc.name})
	else:
		frappe.respond_as_web_page(_("Invalid Payment Request"),
			_("Payment Request has been canceled by vendor"), success=False,
			http_status_code=frappe.ValidationError.http_status_code)

def validate_price_list_currency(doc, method):
	'''Called from Shopping Cart Settings hook'''
	if doc.enabled and doc.enable_checkout:
		if not doc.payment_gateway_account:
			doc.enable_checkout = 0
			return

		payment_gateway_account = frappe.get_doc("Payment Gateway Account", doc.payment_gateway_account)

		if payment_gateway_account.payment_gateway=="PayPal":
			price_list_currency = frappe.db.get_value("Price List", doc.price_list, "currency")

			validate_transaction_currency(price_list_currency)

			if price_list_currency != payment_gateway_account.currency:
				frappe.throw(_("Currency '{0}' of Price List '{1}' should be same as the Currency '{2}' of Payment Gateway Account '{3}'").format(price_list_currency, doc.price_list, payment_gateway_account.currency, payment_gateway_account.name))
