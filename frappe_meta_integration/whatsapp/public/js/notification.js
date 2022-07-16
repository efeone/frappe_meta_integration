frappe.ui.form.on('Notification', {
	refresh: function(frm) {
		frm.events.setup_whatsapp_template(frm);
	},
	channel: function(frm) {
		frm.events.setup_whatsapp_template(frm);
	},
	setup_whatsapp_template: function(frm) {
		let template = '';
		if (frm.doc.channel === 'WhatsApp') {
			template = `
<h5 style='display: inline-block'>Message Example</h5>

<pre>
Your appointment is coming up on {{ doc.date }} at {{ doc.time }}
</pre>`;
		}
		if (template) {
			frm.set_df_property('message_examples', 'options', template);
		}
	}
});
