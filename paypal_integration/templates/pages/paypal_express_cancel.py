# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# See license.txt

from __future__ import unicode_literals
import frappe

def get_context(context):
	token = frappe.local.form_dict.token

	if token:
		paypal_express_payment = frappe.get_doc("Paypal Express Payment", token)
		paypal_express_payment.status = "Cancelled"
		paypal_express_payment.flags.status_changed_to = "Cancelled"
		paypal_express_payment.save(ignore_permissions=True)
		frappe.db.commit()
