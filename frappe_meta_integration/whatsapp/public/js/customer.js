frappe.ui.form.on('Customer', {
  refresh: function(frm) {
    if(frm.doc.whatsapp_number && !frm.doc.is_welcome_message_sent){
      frm.add_custom_button('Send Welcome Message', () => {
        set_primary_action(frm);
      }).addClass("btn-primary");
    }
    if(frm.doc.is_welcome_message_sent){
      frm.set_df_property('whatsapp_number', 'read_only', 1);
      frm.refresh_fields()
    }
  }
})

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
      "phone_number": frm.doc.whatsapp_number,
      "parameters": values
    },
    callback: function(r) {
      frm.set_value('is_welcome_message_sent', 1);
      frm.save()
      frm.refresh_fields();
    }
  });
}
