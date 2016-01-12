# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# See license.txt

from __future__ import unicode_literals
import frappe
from payment_integration.express_checkout import trigger_ref_doc

def get_context(context):
	token = frappe.local.form_dict.token

	if token:
		paypal_express_payment = frappe.get_doc("Paypal Express Payment", token)
		paypal_express_payment.status = "Cancelled"
		paypal_express_payment.save(ignore_permissions=True)
		trigger_ref_doc(paypal_express_payment, "set_as_cancelled")
		frappe.db.commit()
