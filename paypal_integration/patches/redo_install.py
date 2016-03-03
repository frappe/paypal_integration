import frappe

def execute():
	from paypal_integration.after_install import create_gateway_account, create_payment_gateway
	create_payment_gateway()
	create_gateway_account()
