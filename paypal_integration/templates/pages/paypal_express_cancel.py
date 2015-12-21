# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# See license.txt

from __future__ import unicode_literals

import frappe

def get_context(context):
	token = frappe.local.form_dict.token

	if token:
		paypal_express_payment = frappe.get_doc("Paypal Express Payment", token)
		paypal_express_payment.status = "Cancelled"
		paypal_express_payment.save(ignore_permissions=True)
		
		if paypal_express_payment.reference_doctype and paypal_express_payment.reference_docname:
			frappe.get_doc(paypal_express_payment.reference_doctype, 
				paypal_express_payment.reference_docname).run_method("set_cancelled")
		
		frappe.db.commit()
