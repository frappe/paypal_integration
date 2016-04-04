# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from paypal_integration.express_checkout import set_redirect

class PaypalExpressPayment(Document):
	def on_update(self):
		set_redirect(self)
