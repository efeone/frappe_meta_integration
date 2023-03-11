// Copyright (c) 2023, efeone Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('WhatsApp Campaign', {
  setup: function(frm){
    frm.get_field("parameters").grid.cannot_add_rows = true;
    frm.refresh_field("parameters");
    frm.set_query('whatsapp_message_template', () => {
        return {
            filters: {
                docstatus: 1
            }
        }
    });
  },
  whatsapp_message_template: function(frm){
    set_template_parameters(frm);
  }
});

frappe.ui.form.on('WhatsApp Message Template Item', {
  parameters_remove: function(frm, cdt, cdn){
    frappe.show_alert({
      message:__('You are not allowed to add/remove parameter Manually!. Changes will be reverted.'),
      indicator:'red'
    }, 5);
    set_template_parameters(frm);
  },
  parameters_add: function(frm, cdt, cdn){
    frappe.show_alert({
      message:__('You are not allowed to add/remove parameter Manually!. Changes will be reverted.'),
      indicator:'red'
    }, 5);
    set_template_parameters(frm);
  }
});

function set_template_parameters(frm){
  if(frm.doc.whatsapp_message_template){
    frappe.call({
      method: 'frappe_meta_integration.whatsapp.doctype.whatsapp_message_template.whatsapp_message_template.set_template_parameters',
      args: {
        "whatsapp_message_template": frm.doc.whatsapp_message_template
      },
      callback: function(r) {
        frm.clear_table('parameters');
        for(var i=0; i< r.message.length; i++){
          let row =frm.add_child('parameters',{
            parameter: r.message[i].parameter
          });
        }
        frm.save()
      }
    });
  }
}
