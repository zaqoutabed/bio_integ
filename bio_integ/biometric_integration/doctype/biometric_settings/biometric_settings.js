// Copyright (c) 2023, Riane and contributors
// For license information, please see license.txt

frappe.ui.form.on('Biometric Settings', {
	fetch_checkin: function(frm) {
		cur_frm.call({
			method: 'bio_integ.api.execute',
			args: {},
			freeze: true,
			callback: function(r) {
				if (r.message){
					frappe.msgprint("Employee Checkin Fetched successefully")
				}
			}
		});
	},
	update_key: function(frm) {
		cur_frm.call({
			method: 'bio_integ.api.update_key',
			args: {},
			freeze: true,
			callback: function(r) {
				if (r.message){
					frappe.msgprint("Key updated successefully")
				}
			}
		});
	}
});
