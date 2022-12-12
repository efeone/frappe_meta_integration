# Copyright (c) 2022, efeone Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
import requests
from frappe.model.document import Document
from frappe_meta_integration.whatsapp.utils import*

class WhatsAppMessageTemplate(Document):
	def set_template_name_and_codes(self):
		"""Set template code."""
		self.template_name = self.template_name.lower().replace(' ', '_')
		self.language_code = frappe.db.get_value(
			"Language", self.language
		).replace('-', '_')

	def autoname(self):
		self.set_template_name_and_codes()
		self.name = self.template_name

	def before_save(self):
		self.set_template_name_and_codes()

	def validate(self):
		self.set_template_name_and_codes()
		if self.parameter_count:
			if self.parameter_count != len(self.parameters):
				frappe.throw("Parameter count and given number of parameters doesn't match!")

	def on_submit(self):
		if not self.is_existing_template:
			self.set_template_name_and_codes()
			access_token = get_access_token()
			response_data = {
	            "name": self.template_name,
	            "language": self.language_code,
	            "category": self.category,
	            "components": [{
	                "type": "BODY",
	                "text": self.template
	            }]
	        }
			if self.header:
				response_data['components'].append({
					"type": "HEADER",
					"format": "TEXT",
					"text": self.header
				})
			if self.footer:
				response_data['components'].append({
					"type": "FOOTER",
					"text": self.footer
				})

			#Setting Action Button for quick replay
			if self.template_name and self.template_name=='welcome_message':
				response_data['components'].append({
					"type" : "BUTTONS",
					"buttons": [{
						"type": "QUICK_REPLY",
						"text": "Yes"
					}]
				})

			api_base_url = "https://graph.facebook.com/v13.0"
			business_account_id = frappe.db.get_single_value("WhatsApp Cloud API Settings", "business_account_id")
			endpoint = f"{api_base_url}/{business_account_id}/message_templates"
			response = requests.post(
				endpoint,
				json=response_data,
				headers={
					"Authorization": "Bearer " + access_token,
					"Content-Type": "application/json",
				},
			)
			if response.ok:
				frappe.db.set_value("WhatsApp Message Template", self.name, "id", response.json().get("id"))
				frappe.db.commit()
				self.reload()
			else:
				frappe.throw(response.json().get("error").get("message"))

	def on_trash(self):
		if self.template_name=='welcome_message':
			frappe.throw(msg="You're not authorised to Delete standard Templates", title="Not Permitted!")

@frappe.whitelist()
def set_template_parameters(whatsapp_message_template):
	template_doc = frappe.get_doc('WhatsApp Message Template', whatsapp_message_template)
	return template_doc.parameters
