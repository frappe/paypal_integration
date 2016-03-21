import frappe

def execute():
	from paypal_integration.paypal_integration.doctype.paypal_settings import (create_gateway_account,
	create_payment_gateway)

	create_payment_gateway()
	create_gateway_account()
