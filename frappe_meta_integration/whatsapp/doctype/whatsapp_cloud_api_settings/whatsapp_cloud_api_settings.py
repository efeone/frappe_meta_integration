# Copyright (c) 2022, efeone Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
import requests
from frappe.model.document import Document

class WhatsAppCloudAPISettings(Document):
	pass

def get_access_token():
	return frappe.utils.password.get_decrypted_password(
		"WhatsApp Cloud API Settings", "WhatsApp Cloud API Settings", "access_token"
	)

@frappe.whitelist()
def send_test_message(phone_number):
	access_token = get_access_token()
	api_base_url = "https://graph.facebook.com/v13.0"
	phone_number_id = frappe.db.get_single_value("WhatsApp Cloud API Settings", "phone_number_id")

	endpoint = f"{api_base_url}/{phone_number_id}/messages"

	response_data = {
		"messaging_product": "whatsapp",
		"recipient_type": "individual",
		"to": phone_number,
		"type": 'template',
	}
	response_data["template"] = {"name": 'hello_world', "language": { "code": "en_US" } }
	response = requests.post(
		endpoint,
		json=response_data,
		headers={
			"Authorization": "Bearer " + access_token,
			"Content-Type": "application/json",
		},
	)

	if response.ok:
		return response.json().get("messages")[0]["id"]
	else:
		frappe.throw(response.json().get("error").get("message"))
