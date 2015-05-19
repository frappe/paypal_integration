# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# See license.txt

from __future__ import unicode_literals

import frappe, json

no_cache = True

def get_context(context):
	token = frappe.local.form_dict.token

	if token:
		paypal_express_payment = frappe.get_doc("Paypal Express Payment", token)
		paypal_express_payment.status = "Verified"
		paypal_express_payment.save(ignore_permissions=True)
		frappe.db.commit()

	context.token = token
	context.data = json.loads(paypal_express_payment.data or "{}")
