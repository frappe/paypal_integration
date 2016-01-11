from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Integrations"),
			"icon": "icon-star",
			"items": [
				{
					"type": "doctype",
					"name": "PayPal Settings",
					"description": _("Setup PayPal credentials"),
					"hide_count": True
				}
			]
		}
	]
