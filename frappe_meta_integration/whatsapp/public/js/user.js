frappe.ui.form.on('User', {
	refresh(frm) {
		if(!frm.doc.whatsapp_2f_authenticated && frm.doc.user_whatsapp_number){
      frm.add_custom_button('Whatsapp 2FA', () => {
        set_primary_action(frm);
			});
		}
	}
});

function set_primary_action(frm){
  var feild_dicts = [];
  frappe.db.get_single_value("WhatsApp Cloud API Settings", "welcome_message_template").then( whatsapp_message_template => {
    frappe.call({
      method: 'frappe_meta_integration.whatsapp.doctype.whatsapp_message_template.whatsapp_message_template.set_template_parameters',
      args: {
        "whatsapp_message_template": whatsapp_message_template
      },
      callback: function(r) {
        for(var i=0; i< r.message.length; i++){
          const parameter = r.message[i].parameter
          var feild_dict = {
              label: parameter.charAt(0).toUpperCase() + parameter.slice(1),
              fieldname: parameter,
              fieldtype: 'Data',
              reqd: 1,
              description: 'Parameter required for Template',
          }
          feild_dicts.push(feild_dict)
        }
        frappe.prompt(feild_dicts,(values) => {
          send_welcome_message(frm, values);
        })
      }
    });
  });
}

function send_welcome_message(frm, values){
  frappe.call({
    method: 'frappe_meta_integration.whatsapp.utils.send_welcome_message',
    args: {
      "phone_number": frm.doc.user_whatsapp_number,
      "parameters": values
    },
    callback: function(r) {
      frm.set_value('whatsapp_2f_authenticated', 1);
      frm.save()
      frm.refresh_fields();
    }
  });
}
