// Copyright (c) 2022, efeone Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('WhatsApp Communication', {
  setup: function(frm){
    frm.get_field("parameters").grid.cannot_add_rows = true;
    frm.refresh_field("parameters");
    frm.set_query('whatsapp_message_template', () => {
        return {
            filters: {
                docstatus: 1
            }
        }
    })
    if(frm.doc.type == 'Incoming'){
		    frm.disable_form();
		}
  },
  refresh: function(frm) {
    if(!frm.is_new()){
      make_custom_buttons(frm);
    }
    if (frm.doc.preview_html) {
      let wrapper = frm.get_field("preview_html_rendered").$wrapper;
      wrapper.html(frm.doc.preview_html);
    }
    if(frm.doc.type == 'Incoming'){
		    frm.disable_form();
		}
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

function make_custom_buttons(frm){
  create_send_msg_button(frm);
  create_upload_media_button(frm);
  create_download_media_button(frm);
}

function create_send_msg_button(frm){
  if (!frm.doc.message_id && frm.doc.type =='Outgoing') {
    const btn = frm.add_custom_button("Send Message", () => {
      frm.call({
          doc: frm.doc,
          method: "send_message",
          btn,
      })
      .then((m) => frm.refresh());
    });
  }
}

function create_upload_media_button(frm){
  if (frm.doc.type === "Outgoing" && frm.doc.media_file && !frm.doc.media_uploaded) {
    const btn = frm.add_custom_button("Upload Attachment File", () => {
      frm.call({
        doc: frm.doc,
        method: "upload_media",
        btn,
      })
      .then(() => {
        frm.refresh();
        frappe.msgprint({
          title: "Attachment uploaded successfully.",
          message: "You can send this message now!",
          indicator: "green",
        });
      });
    });
  }
}

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

function create_download_media_button(frm){
  if (
    frm.doc.type === "Incoming" &&
    ["Image", "Video", "Audio", "Document"].includes(frm.doc.message_type) &&
    !frm.doc.media_file
  ) {
    const btn = frm.add_custom_button("Download Attachment File", () => {
      frm
        .call({
          doc: frm.doc,
          method: "download_media",
          btn,
        })
        .then((data) => {
          const file = data.message;
          frm.refresh();
          frappe.msgprint({
            title: "Attachment downloaded successfully.",
            message: `Attachment File: <a href="${file.file_url}" target="_blank">${file.file_name}</a>`,
            indicator: "green",
          });
        });
    });
  }
}
