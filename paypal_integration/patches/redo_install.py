import frappe

def execute():
	# should create payment gateway and payment gateway account
	frappe.get_doc("Paypal Settings").save()
