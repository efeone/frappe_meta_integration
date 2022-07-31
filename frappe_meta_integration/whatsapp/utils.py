from __future__ import unicode_literals

import frappe
from frappe import _
import requests
import json
import string
from frappe_meta_integration.whatsapp.doctype.whatsapp_communication.whatsapp_communication import WhatsAppCommunication
from frappe.utils.print_format import download_pdf
from frappe_meta_integration.whatsapp.pdf_utils import *

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

@frappe.whitelist()
def validate_whatsapp_number(whatsapp_number):
	'''
		Validate Phone Number with Special Characters.
	'''
	special_chars = string.punctuation #To get all punctuations
	bools = list(map(lambda char: char in special_chars, whatsapp_number))
	if any(bools):
		frappe.throw(
	        _("Whatsapp Number {0} is Invalid, Special Characters are not allowed.").format(frappe.bold(whatsapp_number))
        )
	if ' ' in whatsapp_number:
		frappe.throw(
	        _("Whatsapp Number {0} is Invalid, Spaces are not allowed.").format(frappe.bold(whatsapp_number))
        )

@frappe.whitelist()
def get_contact_list(txt, page_length=20):
	"""Returns contacts (from autosuggest)"""

	out = frappe.db.sql(
		"""
		select
			whatsapp_number as value,
			concat(first_name, ifnull(concat(' ',last_name), '' )) as description
		from
			tabContact
		where
			whatsapp_number <>'' AND (
				name like %(txt)s or
				whatsapp_number like %(txt)s
			)
		limit
			%(page_length)s""",
		{"txt": "%" + txt + "%", "page_length": page_length},
		as_dict=True,
	)
	out = filter(None, out)
	return out

@frappe.whitelist()
def send_whatsapp_msg(doctype, docname, args):
	"""
	Generate mediaif exists and send message
	"""
	pdf_link = None
	file_name = None
	if args and isinstance(args, str):
		args = json.loads(args)
	#Setting argumnents is exist
	print_format = args['print_format'] if 'print_format' in args else "Standard"
	message = args['message'] if 'message' in args else "Please find the attachments."

	#Setting recipients list
	recipients = (args['recipients']).replace(" ", "")
	last_char = recipients[-1]
	if last_char == ',':
		receiver_list = recipients[0: -1].split(',')
	else:
		receiver_list = recipients

	if args['attach_document_print']: #If Attachment included
		doctype = doctype
		docname =  docname
		title =  docname
		print_format = print_format
		doctype_folder = create_folder(_(doctype), "Home")
		title_folder = create_folder(title, doctype_folder)
		pdf_data = get_pdf_data(doctype, docname, print_format)
		file_ref = save_and_attach(pdf_data, doctype, docname, title_folder)
		pdf_link = file_ref.file_url
		file_name = file_ref.file_name
	if not args['attach_document_print'] and not message:
		frappe.throw(
	        _("Either Message or Attachment is required.")
        )
	WhatsAppCommunication.send_whatsapp_message(
		receiver_list = receiver_list,
		message = message,
		doctype = doctype,
		docname = docname,
		media = pdf_link,
		file_name = file_name,
	)
