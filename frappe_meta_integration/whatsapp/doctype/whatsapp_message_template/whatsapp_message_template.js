// Copyright (c) 2022, efeone Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('WhatsApp Message Template', {
	refresh: function(frm) {
		if(frm.doc.name == 'welcome_message'){
			make_feilds_readonly(frm);
		}
		if(frm.doc.docstatus==1){
			$(".btn-default").hide();
		}
	},
	add_variable: function(frm){
		add_variable_popup(frm);
	}
});

let make_feilds_readonly=function(frm){
	$(".btn-default").hide();
	frm.set_df_property('category', 'read_only', 1);
	frm.set_df_property('parameters', 'read_only', 1);
	frm.refresh_fields()
}

let add_variable_popup = function(frm){
	let add_variable_dialog = new frappe.ui.Dialog({
    title: 'Add variable',
    fields: [
        {
            label: 'Variable Name',
            fieldname: 'variable_name',
            fieldtype: 'Data',
						reqd: '1'
        }
    ],
    primary_action_label: 'Submit',
    primary_action(res) {
				frm.set_value('parameter_count', frm.doc.parameter_count + 1 )
				frm.set_value('template', frm.doc.template + ' {{'+ frm.doc.parameter_count +'}} ')
				let row =frm.add_child('parameters',{
					parameter: res.variable_name
				});
				frm.refresh_fields()
        add_variable_dialog.hide();
    }
	});
	add_variable_dialog.show();
}
