# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe

def execute():
	paypal_settings = frappe.get_doc("PayPal Settings")
	if not paypal_settings.api_username or not paypal_settings.api_password or not paypal_settings.signature:
		if frappe.conf.paypal_username and frappe.conf.paypal_password and frappe.conf.paypal_signature:
			frappe.get_doc({
				"doctype": "PayPal Settings",
				"api_username": frappe.conf.paypal_username,
				"api_password": frappe.conf.paypal_password,
				"signature": frappe.conf.paypal_signature
			}).insert(ignore_permissions=True)