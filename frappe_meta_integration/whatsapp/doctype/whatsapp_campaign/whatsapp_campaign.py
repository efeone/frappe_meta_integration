# Copyright (c) 2023, efeone Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class WhatsAppCampaign(Document):
	def validate(self):
		self.validate_recepients()

	def on_submit(self):
		self.validate_recepients()
		self.send_message()

	@frappe.whitelist()
	def validate_recepients(self):
		if self.recipients:
			for recepient in self.recipients:
				if not recepient.whatsapp_number:
					frappe.throw("Recepient is required in Row {} to send messages".format(recepient.idx))
		else:
			frappe.throw("Recepient is required to send messages".format(recepient.idx))

	@frappe.whitelist()
	def send_message(self):
		if self.recipients:
			created = 0
			for recepient in self.recipients:
				whatsapp_communication = frappe.new_doc('WhatsApp Communication')
				whatsapp_communication.to = recepient.whatsapp_number
				whatsapp_communication.message_type = self.message_type
				whatsapp_communication.message_body = self.message_body
				whatsapp_communication.media_filename = self.media_filename
				whatsapp_communication.media_caption = self.media_caption
				whatsapp_communication.media_file = self.media_file
				whatsapp_communication.media_image = self.media_image
				whatsapp_communication.whatsapp_message_template = self.whatsapp_message_template
				whatsapp_communication.parameters = self.parameters
				whatsapp_communication.reference_dt = self.doctype
				whatsapp_communication.reference_dn = self.name
				whatsapp_communication.save(ignore_permissions=True)
				whatsapp_communication.send_message()
				frappe.db.set_value('WhatsApp Campaign Recipient', recepient.name, 'whatsapp_communication', whatsapp_communication.name)
				frappe.db.set_value('WhatsApp Campaign Recipient', recepient.name, 'status', whatsapp_communication.status)
				created = 1
			if created:
				frappe.db.commit()
				frappe.msgprint("WhatsApp Communications created", alert=True, indicator="green")
				self.reload()
		else:
			frappe.throw("Recepient is required to send messages".format(recepient.idx))
