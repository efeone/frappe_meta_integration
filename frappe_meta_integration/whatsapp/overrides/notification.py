import frappe
from frappe import _
from frappe.email.doctype.notification.notification import Notification, get_context, json
from frappe_meta_integration.whatsapp.doctype.whatsapp_communication.whatsapp_communication import WhatsAppCommunication
from frappe.utils.print_format import download_pdf
from frappe_meta_integration.whatsapp.pdf_utils import *

class SendNotification(Notification):
	def send(self, doc):
		"""
		Overrided current send method
		"""
		context = get_context(doc)
		context = {"doc": doc, "alert": self, "comments": None}
		if doc.get("_comments"):
			context["comments"] = json.loads(doc.get("_comments"))

		if self.is_standard:
			self.load_standard_properties(context)

		try:
			if self.channel == 'WhatsApp':
				self.send_whatsapp_msg(doc, context)
		except:
			frappe.log_error(title='Failed to send notification', message=frappe.get_traceback())

		super(SendNotification, self).send(doc)

	def send_whatsapp_msg(self, doc, context):
		"""
		Generate mediaif exists and send message
		"""
		pdf_link = None
		file_name = None
		attachments = self.get_attachment(doc)
		if attachments:
			doctype = attachments[0]['doctype']
			docname =  attachments[0]['name']
			title =  attachments[0]['name']
			print_format = attachments[0]['print_format']
			doctype_folder = create_folder(_(doctype), "Home")
			title_folder = create_folder(title, doctype_folder)
			pdf_data = get_pdf_data(doctype, docname, print_format)
			file_ref = save_and_attach(pdf_data, doctype, docname, title_folder)
			pdf_link = file_ref.file_url
			file_name = file_ref.file_name

		WhatsAppCommunication.send_whatsapp_message(
			receiver_list=self.get_receiver_list(doc, context),
			message=frappe.render_template(self.message, context),
			doctype = self.doctype,
			docname = self.name,
			media = pdf_link,
			file_name = file_name
		)
