# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "paypal_integration"
app_title = "Paypal Integration"
app_publisher = "Frappe"
app_description = "Paypal Payment Gateway Integration"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@frappe.io"
app_version = "0.0.1"
hide_in_installer = True

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/paypal_integration/css/paypal_integration.css"
# app_include_js = "/assets/paypal_integration/js/paypal_integration.js"

# include js, css files in header of web template
# web_include_css = "/assets/paypal_integration/css/paypal_integration.css"
# web_include_js = "/assets/paypal_integration/js/paypal_integration.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "paypal_integration.install.before_install"
# after_install = "paypal_integration.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "paypal_integration.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"paypal_integration.tasks.all"
# 	],
# 	"daily": [
# 		"paypal_integration.tasks.daily"
# 	],
# 	"hourly": [
# 		"paypal_integration.tasks.hourly"
# 	],
# 	"weekly": [
# 		"paypal_integration.tasks.weekly"
# 	]
# 	"monthly": [
# 		"paypal_integration.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "paypal_integration.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "paypal_integration.event.get_events"
# }

