from unittest import TestCase

from . import express_checkout
import frappe

class TestExpressCheckout(TestCase):
	def test_set_express_checkout(self):
		express_checkout.set_express_checkout(100, "USD")
		self.assertEqual(frappe.local.response["type"], "redirect")
