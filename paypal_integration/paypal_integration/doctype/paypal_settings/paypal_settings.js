frappe.ui.form.on("PayPal Settings", {
	refresh: function(frm) {
		frm.add_custom_button(__("PayPal Express Payment Logs"), function() {
			frappe.set_route("List", "Paypal Express Payment");
		});
	}
})
