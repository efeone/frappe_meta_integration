import frappe
from werkzeug.wrappers import Response
from frappe_meta_integration.whatsapp.doctype.whatsapp_communication.whatsapp_communication import (
	create_incoming_whatsapp_message,
    update_message_status
)

@frappe.whitelist(allow_guest=True)
def handle():
    if frappe.request.method == "GET":
        return verify_token_and_fulfill_challenge()

    try:
        form_dict = frappe.local.form_dict
        messages = form_dict["entry"][0]["changes"][0]["value"].get("messages", [])
        statuses = form_dict["entry"][0]["changes"][0]["value"].get("statuses", [])

        for status in statuses:
            update_message_status(status)
            
        for message in messages:
            create_incoming_whatsapp_message(message)

        frappe.get_doc(
            {"doctype": "WhatsApp Webhook Log", "payload": frappe.as_json(form_dict)}
        ).insert(ignore_permissions=True)
        frappe.db.commit()
    except Exception:
        frappe.log_error("WhatsApp Webhook Log Error", frappe.get_traceback())

def verify_token_and_fulfill_challenge():
	meta_challenge = frappe.form_dict.get("hub.challenge")
	expected_token = frappe.db.get_single_value("WhatsApp Cloud API Settings", "webhook_verify_token")

	if frappe.form_dict.get("hub.verify_token") != expected_token:
		frappe.throw("Verify token does not match")

	return Response(meta_challenge, status=200)
