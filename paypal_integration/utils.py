import frappe
from .express_checkout import set_express_checkout

def get_payment_url(doc, method):
	if doc.docstatus not in [0, 2]:
		if doc.payment_gateway == "PayPal":
			set_express_checkout(doc.amount, doc.currency, {"doctype": doc.doctype, "docname": doc.name})
	else:
		frappe.respond_as_web_page(_("Invalid Payment Request"), 
			_("Payment Request has been canceled by vendor"), success=False, 
			http_status_code=frappe.ValidationError.http_status_code)
	