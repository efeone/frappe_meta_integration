// Copyright (c) 2022, efeone Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('WhatsApp Communication', {
  refresh: function(frm) {
    if(!frm.is_new()){
      make_custom_buttons(frm);
    }
    if (frm.doc.preview_html) {
      let wrapper = frm.get_field("preview_html_rendered").$wrapper;
      wrapper.html(frm.doc.preview_html);
    }
	}
});

function make_custom_buttons(frm){
  create_send_msg_button(frm);
  create_upload_media_button(frm);
}

function create_send_msg_button(frm){
  if (!frm.doc.message_id) {
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
