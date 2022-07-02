import frappe
import requests
import json

def get_access_token():
	return frappe.utils.password.get_decrypted_password(
		"WhatsApp Cloud API Settings", "WhatsApp Cloud API Settings", "access_token"
	)

@frappe.whitelist()
def set_template_parameters(whatsapp_message_template):
	template_doc = frappe.get_doc('WhatsApp Message Template', whatsapp_message_template)
	return template_doc.parameters

@frappe.whitelist()
def send_welcome_message(phone_number, parameters = None):
	if parameters and isinstance(parameters, str):
		parameters = json.loads(parameters)
	access_token = get_access_token()
	phone_number_id = frappe.db.get_single_value("WhatsApp Cloud API Settings", "phone_number_id")
	welcome_message_template = frappe.db.get_single_value("WhatsApp Cloud API Settings", "welcome_message_template")
	template_parameters = set_template_parameters(welcome_message_template)
	whatsapp_communication_doc = frappe.new_doc("WhatsApp Communication")
	whatsapp_communication_doc.to = phone_number
	whatsapp_communication_doc.message_type = 'Template'
	whatsapp_communication_doc.whatsapp_message_template = welcome_message_template
	whatsapp_communication_doc.is_welcome_message = 1
	for template_parameter in template_parameters:
		row = whatsapp_communication_doc.append('parameters')
		row.parameter = template_parameter.parameter
		row.value = parameters[template_parameter.parameter]
	whatsapp_communication_doc.save()
	whatsapp_communication_doc.send_message()
