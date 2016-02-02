source_link = "https://github.com/frappe/paypal_integration"
docs_base_url = "https://frappe.github.io/paypal_integration"
headline = "PayPal Integration"
sub_heading = "Setup PayPal with ERPNext"
long_description = """ A payment gateway is an e-commerce application service provider service that authorizes 
credit card payments for e-businesses, online retailers, bricks and clicks, 
or traditional brick and mortar.

A payment gateway facilitates the transfer of information between a payment portal 
(such as a website, mobile phone or interactive voice response service) and 
the Front End Processor or acquiring bank."""

docs_version = "1.x.x"
splash_light_background = True

def get_context(context):
	context.app.splash_light_background = True
