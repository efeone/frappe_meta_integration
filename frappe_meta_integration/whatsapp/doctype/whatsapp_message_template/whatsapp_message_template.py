# Copyright (c) 2022, efeone Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class WhatsAppMessageTemplate(Document):
	def validate(self):
		if self.parameter_count:
			if self.parameter_count != len(self.parameters):
				frappe.throw("Parameter count and given number of parameters doesn't match!")


@frappe.whitelist()
def set_template_parameters(whatsapp_message_template):
	template_doc = frappe.get_doc('WhatsApp Message Template', whatsapp_message_template)
	return template_doc.parameters
