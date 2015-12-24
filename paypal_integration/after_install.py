# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# See license.txt

from __future__ import unicode_literals
import frappe
from erpnext.accounts.utils import add_ac

def create_payment_gateway():
	payment_gateway = frappe.get_doc({
		"doctype": "Payment Gateway",
		"gateway": "PayPal"
	}).insert(ignore_permissions=True)
	
	create_gateway_account()

def create_gateway_account():
	try:
		company_name = frappe.db.get_value("Global Defaults", None, "default_company")
		if company_name:
			company = frappe.get_doc("Company", company_name)
		
			if not frappe.db.get_value("Account", "PayPal - %s"%company.abbr, "name"):
				account_details = {
					'is_root': 'false', 
					'parent_account': 'Cash In Hand - %s'%company.abbr, 
					'root_type': '', 
					'account_currency': company.default_currency, 
					'company': company.name, 
					'account_name': "PayPal"
				}
			
				account = add_ac(account_details)
		
			if not frappe.db.get_value("Payment Gateway Account", {"gateway": "PayPal", 
				"currency": company.default_currency}, "name"):
			
				frappe.get_doc({
					"doctype": "Payment Gateway Account",
					"is_default": 1,
					"gateway": "PayPal",
					"payment_account": account,
					"currency": company.default_currency
				}).insert(ignore_permissions=True)
				
	except frappe.PermissionError as e:
		frappe.throw(_("Permission Error: {0}").format(frappe.get_traceback()), frappe.PermissionError)
		