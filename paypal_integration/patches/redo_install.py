import frappe

def execute():
	# should create payment gateway and payment gateway account
	try:
		frappe.get_doc("PayPal Settings").save()
	except frappe.MandatoryError:
		pass
