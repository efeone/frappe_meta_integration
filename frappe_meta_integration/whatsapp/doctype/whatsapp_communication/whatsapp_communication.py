# Copyright (c) 2022, efeone Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
import requests
import mimetypes

from frappe.model.document import Document

class WhatsAppCommunication(Document):
	def validate(self):
		self.validate_image_attachment()
		self.validate_mandatory()
		self.validate_template()

		if self.message_type == "Audio" and self.media_file:
			self.preview_html = f"""
				<audio controls>
					<source src="{self.media_file}" type="{self.media_mime_type}">
					Your browser does not support the audio element.
				</audio>
			"""

		if self.message_type == "Video" and self.media_file:
			self.preview_html = f"""
				<video controls>
					<source src="{self.media_file}" type="{self.media_mime_type}">
					Your browser does not support the video element.
				</video>
			"""

	def validate_image_attachment(self):
		if self.media_image:
			self.media_file = self.media_image
		if self.media_file and self.message_type == "Image":
			self.media_image = self.media_file

	def validate_mandatory(self):
		if self.message_type == "Text" and not self.message_body:
			frappe.throw("Message Body is required for type Text.")
		if self.message_type == "Template" and not self.whatsapp_message_template:
			frappe.throw("Message Template is required for type Template.")

	def validate_parameters(self):
		if self.message_type == "Template":
			for parameter in self.parameters:
				if not parameter.value:
					frappe.throw('Parameter Value is Missing for <b>{0}</b> at row : <b>{1}</b>.'.format(parameter.parameter, parameter.idx))

	def validate_template(self):
		if self.message_type == "Template":
			if self.parameter_count:
				if self.parameter_count != len(self.parameters):
					frappe.throw("Parameter count and given number of parameters doesn't match!")

	def get_access_token(self):
		return frappe.utils.password.get_decrypted_password(
			"WhatsApp Cloud API Settings", "WhatsApp Cloud API Settings", "access_token"
		)

	@frappe.whitelist()
	def send_message(self):
		if not self.to:
			frappe.throw("Recepient (`to`) is required to send message.")

		access_token = self.get_access_token()

		api_base_url = "https://graph.facebook.com/v13.0"
		phone_number_id = frappe.db.get_single_value("WhatsApp Cloud API Settings", "phone_number_id")

		endpoint = f"{api_base_url}/{phone_number_id}/messages"

		response_data = {
			"messaging_product": "whatsapp",
			"recipient_type": "individual",
			"to": self.to,
			"type": self.message_type.lower(),
		}

		if self.message_type == "Text":
			response_data["text"] = {"preview_url": False, "body": self.message_body}

		if self.message_type in ("Audio", "Image", "Video", "Document"):
			if not self.media_id:
				frappe.throw("Please attach and upload the media before sending this message.")

			response_data[self.message_type.lower()] = {
				"id": self.media_id,
			}

			if self.message_type == "Image":
				response_data[self.message_type.lower()]["caption"] = self.media_caption

			if self.message_type == "Document":
				response_data[self.message_type.lower()]["filename"] = self.media_filename
				response_data[self.message_type.lower()]["caption"] = self.media_caption

		if self.message_type == "Template":
			self.validate_parameters()
			parameters = []
			for parameter in self.parameters:
				parameters.append({
					 "type": "text",
					 "text": parameter.value
				})
			components_dict = [
	            {
	                "type": "body",
	                "parameters": parameters
	            }
	        ]
			response_data["template"] = {"name": self.whatsapp_message_template, "language": { "code": self.template_language }, "components":components_dict }

		response = requests.post(
			endpoint,
			json=response_data,
			headers={
				"Authorization": "Bearer " + access_token,
				"Content-Type": "application/json",
			},
		)

		if response.ok:
			self.message_id = response.json().get("messages")[0]["id"]
			self.status = "Sent"
			self.save(ignore_permissions=True)
			if self.is_welcome_message:
				frappe.msgprint(("Welcome Message sent to {0} ").format(self.to), alert=True)
			return response.json()
		else:
			frappe.throw(response.json().get("error").get("message"))

	@frappe.whitelist()
	def upload_media(self):
		if not self.media_file:
			frappe.throw("`media_file` is required to upload media.")

		media_file_path = frappe.get_doc("File", {"file_url": self.media_file}).get_full_path()
		access_token = self.get_access_token()
		api_base_url = "https://graph.facebook.com/v13.0"
		phone_number_id = frappe.db.get_single_value("WhatsApp Cloud API Settings", "phone_number_id")

		if not self.media_mime_type:
			self.media_mime_type = mimetypes.guess_type(self.media_file)[0]

		# Way to send multi-part form data
		# Ref: https://stackoverflow.com/a/35974071
		form_data = {
			"file": (
				"file",
				open(media_file_path, "rb"),
				self.media_mime_type,
			),
			"messaging_product": (None, "whatsapp"),
			"type": (None, self.media_mime_type),
		}
		response = requests.post(
			f"{api_base_url}/{phone_number_id}/media",
			files=form_data,
			headers={
				"Authorization": "Bearer " + access_token,
			},
		)

		if response.ok:
			self.media_id = response.json().get("id")
			self.media_uploaded = True
			self.save(ignore_permissions=True)
		else:
			frappe.throw(response.json().get("error").get("message"))
