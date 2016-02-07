# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# See license.txt

from __future__ import unicode_literals
import frappe
from erpnext.setup.setup_wizard.setup_wizard import create_bank_account

def create_payment_gateway():
	if frappe.db.exists("DocType", "Payment Gateway"):
		payment_gateway = frappe.get_doc({
			"doctype": "Payment Gateway",
			"gateway": "PayPal"
		})
		payment_gateway.insert(ignore_permissions=True)

		if frappe.db.exists("DocType", "Payment Gateway Account"):
			create_gateway_account()

def create_gateway_account():
	company_name = frappe.db.get_value("Global Defaults", None, "default_company")
	if company_name:
		company = frappe.get_doc("Company", company_name)
		
		bank = frappe.db.get_value("Account", {"account_name": "PayPal", "company": company_name}, 
			["name", "account_type"], as_dict=1)
		if not bank:
			bank_account = create_bank_account({"company_name": company_name, "bank_account": "PayPal"})
		elif bank.account_type == "Bank":
			bank_account = bank.name
		else:
			bank_account = None
			

		if bank_account and not frappe.db.get_value("Payment Gateway Account", 
			{"gateway": "PayPal", "currency": company.default_currency}, "name"):

			frappe.get_doc({
				"doctype": "Payment Gateway Account",
				"is_default": 1,
				"gateway": "PayPal",
				"payment_account": bank_account.name,
				"currency": company.default_currency
			}).insert(ignore_permissions=True)
