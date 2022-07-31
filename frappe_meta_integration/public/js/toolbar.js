frappe.provide('frappe.ui.form');
frappe.provide('frappe.model.docinfo');

$(document).ready(function (){
	frappe.ui.form.Controller = Class.extend({
		init: function(opts) {
			$.extend(this, opts);
			let ignored_doctype_list = ["DocType", "Customize Form"]
			frappe.ui.form.on(this.frm.doctype, {
				refresh(frm) {
					if(!ignored_doctype_list.includes(frm.doc.doctype)){
						frm.page.add_menu_item(__('Send via WhatsApp'), function() { send_sms(frm); });
					}
				}
			});
		}
	});
});

function send_sms(frm){
	if(frm.is_dirty()){
		frappe.throw(__('You have unsaved changes. Save before send.'))
	}
	else {
		create_recipients_dailog(frm);
	}
}

function create_recipients_dailog(frm){
	let d = new frappe.ui.Dialog({
    title: frm.doc.doctype + " : " + frm.doc.name,
    fields: [
			{
				label: __("To"),
				fieldtype: "MultiSelect",
				reqd: 1,
				fieldname: "recipients",
				default: frm.doc.whatsapp_number ? frm.doc.whatsapp_number : "",
			},
			{
				label: __("Message"),
				fieldtype: "Small Text",
				fieldname: "message",
				length: 700
			},
			{
				label: __("Attach Document Print"),
				fieldtype: "Check",
				fieldname: "attach_document_print"
			},
			{
				label: __("Select Print Format"),
				fieldtype: "Link",
				fieldname: "print_format",
				options: "Print Format",
				get_query: function () {
					return{
						filters: {
							'doc_type': frm.doc.doctype,
							'disabled': 0
						}
					}
				}
			}
		],
		primary_action_label: __("Send"),
		primary_action(values) {
			dialog_primary_action(frm, values)
			d.hide();
		},
		secondary_action_label: __("Discard"),
		secondary_action() {
			d.hide();
		},
		size: 'large',
		minimizable: true
	});
	d.show();
	get_whatsapp_number_list(d)
}

function get_whatsapp_number_list(d){
	d.fields_dict["recipients"].get_data = () => {
		const data = d.fields_dict["recipients"].get_value();
		const txt = data.match(/[^,\s*]*$/)[0] || '';
		frappe.call({
			method: "frappe_meta_integration.whatsapp.utils.get_contact_list",
			args: {txt},
			callback: (r) => {
				d.fields_dict["recipients"].set_data(r.message);
			}
		});
	};
}

function dialog_primary_action(frm, values){
	frappe.call({
		method: "frappe_meta_integration.whatsapp.utils.send_whatsapp_msg",
		args: {
      "doctype": frm.doc.doctype,
			"docname": frm.doc.name,
			"args": values
    },
		freeze: true,
    freeze_message: ('Sending WhatsApp Message.!!')
	});
}
