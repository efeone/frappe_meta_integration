# Copyright (c) 2022, efeone Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
import requests
import mimetypes
from typing import Dict
from six import string_types

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

	def validate_header_media(self):
		if self.message_type == "Template" and self.whatsapp_message_template:
			if self.header_has_media:
				if not self.header_media:
					frappe.throw("`header_media` is required in selected Template.")

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
			self.validate_header_media()
			body_parameters = []
			for parameter in self.parameters:
				body_parameters.append({
					 "type": "text",
					 "text": parameter.value
				})
			if self.header_has_media:
				if self.header_media:
					media_file_path = frappe.utils.get_url()
					media_file_path += self.header_media
					headers_parameters = []
					if self.media_type == 'image':
						headers_parameters.append({
							"type": "image",
							"image": {
								"link": media_file_path
							}
						})
					if self.media_type == 'document':
						headers_parameters.append({
							"type": "document",
							"document": {
								"link": media_file_path
							}
						})
					if self.media_type == 'video':
						headers_parameters.append({
							"type": "video",
							"video": {
								"link": media_file_path
							}
						})
				components_dict = [
					{
						"type": "header",
						"parameters": headers_parameters
					},
					{
						"type": "body",
						"parameters": body_parameters
					}
				]
			else:
				components_dict = [
					{
						"type": "body",
						"parameters": body_parameters
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
				frappe.msgprint(("Welcome Message sent to {0} ").format(self.to), alert=True, indicator="green")
			else:
				if self.message_type not in ("Audio", "Image", "Video", "Document"):
					frappe.msgprint(("WhatsApp Message sent to {0} ").format(self.to), alert=True, indicator="green")
				else:
					frappe.msgprint(("Attachment sent to {0} ").format(self.to), alert=True, indicator="green")
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

	@classmethod
	def send_whatsapp_message(self, receiver_list, message, doctype, docname, media=None, file_name=None):
		if isinstance(receiver_list, string_types):
			if not isinstance(receiver_list, list):
				receiver_list = [receiver_list]

		for rec in receiver_list:
			"""
			Iterate receiver_list and send message to each recepient
			"""
			self.create_whatsapp_message(rec, message, doctype, docname) #For Text Message or Caption for documents
			if media and file_name:
				self.create_whatsapp_message(rec, message, doctype, docname, media, file_name) #For Document

	def create_whatsapp_message(to, message, doctype=None, docname=None, media=None, file_name=None):
		"""
		Create WhatsApp Communication with given data.
		"""
		wa_msg = frappe.new_doc('WhatsApp Communication')
		wa_msg.to = to
		wa_msg.reference_dt = doctype
		wa_msg.reference_dn = docname
		if media:
			wa_msg.message_type = "Document"
			wa_msg.media_filename = file_name
			wa_msg.media_file = media
		else:
			wa_msg.message_type = "Text"
			wa_msg.message_body = message
		wa_msg.save(ignore_permissions=True)
		if media and file_name:
			wa_msg.upload_media() #Upload Attachment
		wa_msg.send_message() #Send Attachment/Text Message

	def get_media_url(self):
		if not self.media_id:
			frappe.throw("`media_id` is missing.")

		api_base = "https://graph.facebook.com/v13.0"
		access_token = self.get_access_token()
		response = requests.get(
			f"{api_base}/{self.media_id}",
			headers={
				"Authorization": "Bearer " + access_token,
			},
		)

		if not response.ok:
			frappe.throw("Error fetching media URL")

		return response.json().get("url")

	@frappe.whitelist()
	def download_media(self) -> Dict:
		url = self.get_media_url()
		access_token = self.get_access_token()
		response = requests.get(
			url,
			headers={
				"Authorization": "Bearer " + access_token,
			},
		)

		file_name = get_media_extention(self, response.headers.get("Content-Type"))
		file_doc = frappe.get_doc(
			{
				"doctype": "File",
				"file_name": file_name,
				"content": response.content,
				"attached_to_doctype": "WhatsApp Communication",
				"attached_to_name": self.name,
				"attached_to_field": "media_file",
			}
		).insert(ignore_permissions=True)
		frappe.db.commit()

		self.set("media_file", file_doc.file_url)

		# Will be used to display image preview
		if self.message_type == "Image":
			self.set("media_image", file_doc.file_url)

		self.save()

		return file_doc.as_dict()

@frappe.whitelist()
def update_message_status(status: Dict):
	''' Method to updtae status of Message '''
	message_id = status.get("id")
	status = status.get("status")

	if frappe.db.exists('WhatsApp Communication', {"message_id": message_id}):
		frappe.db.set_value(
			"WhatsApp Communication", {"message_id": message_id}, "status", status.title()
		)
		frappe.db.commit()

@frappe.whitelist()
def create_incoming_whatsapp_message(message: Dict):
	''' Method to create Incoming messages via webhook '''
	MEDIA_TYPES = ("image", "sticker", "document", "audio", "video")
	message_type = message.get("type")
	message_data = frappe._dict(
		{
			"doctype": "WhatsApp Communication",
			"type": "Incoming",
			"status": "Received",
			"from_no": message.get("from"),
			"message_id": message.get("id"),
			"message_type": message_type.title(),
		}
	)

	if message_type == "text":
		message_data["message_body"] = message.get("text").get("body")
	elif message_type in MEDIA_TYPES:
		message_data["media_id"] = message.get(message_type).get("id")
		message_data["media_mime_type"] = message.get(message_type).get("mime_type")
		message_data["media_hash"] = message.get(message_type).get("sha256")

	if message_type == "document":
		message_data["media_filename"] = message.get("document").get("filename")
		message_data["media_caption"] = message.get("document").get("caption")

	if message_type == "image" or message_type == "video":
		message_data["media_caption"] = message.get(message_type).get("caption")

	message_doc = frappe.get_doc(message_data).insert(ignore_permissions=True)
	frappe.db.commit()

def get_media_extention(message_doc, content_type):
	return message_doc.media_filename or (
		"attachment_." + content_type.split(";")[0].split("/")[1]
	)
