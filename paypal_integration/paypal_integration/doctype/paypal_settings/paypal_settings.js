frappe.ui.form.on("PayPal Settings", {
	refresh: function(frm) {
		frm.add_custom_button(__("Payment Logs"), function() {
			frappe.set_route("List", "Paypal Express Payment");
		});
		frm.add_custom_button(__("Payment Gateway Accounts"), function() {
			frappe.route_options = {"payment_gateway": "PayPal"};
			frappe.set_route("List", "Payment Gateway Account");
		});
	}
})
