# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from paypal_integration.after_install import create_gateway_account

class PayPalSettings(Document):
	def on_update(self):
		if frappe.db.get_value("Payment Gateway", {"gateway": "PayPal"}):
			create_gateway_account()		