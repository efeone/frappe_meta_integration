from __future__ import unicode_literals

import frappe
from frappe import _
from frappe_meta_integration.whatsapp.utils import *

@frappe.whitelist()
def contact_validate(doc, method):
    '''
    Validate WhatsApp Number and Setting Primary Number.
    '''
    is_primary = [whatsapp_no.whatsapp_number for whatsapp_no in doc.whatsapp_numbers if whatsapp_no.is_primary]

    if len(is_primary) > 1:
        frappe.throw(
            _("Only one {0} can be set as primary.").format(frappe.bold("WhatsApp Number"))
        )

    primary_whatsapp_number_exists = False
    for whatsapp_no in doc.whatsapp_numbers:
        if whatsapp_no.whatsapp_number:
            validate_whatsapp_number(whatsapp_no.whatsapp_number)
        if whatsapp_no.is_primary == 1:
            primary_whatsapp_number_exists = True
            doc.whatsapp_number = whatsapp_no.whatsapp_number

    if not primary_whatsapp_number_exists:
        doc.whatsapp_number = ""

@frappe.whitelist()
def user_after_insert(doc, method):
    '''
        WhatsApp 2 Factor Authentication
    '''
    welcome_message_template = frappe.db.get_single_value("WhatsApp Cloud API Settings", "welcome_message_template")
    if doc.user_whatsapp_number and welcome_message_template:
        template_doc = frappe.get_doc('WhatsApp Message Template', welcome_message_template)
        whatsapp_communication_doc = frappe.new_doc("WhatsApp Communication")
        whatsapp_communication_doc.to = doc.user_whatsapp_number
        whatsapp_communication_doc.message_type = 'Template'
        whatsapp_communication_doc.whatsapp_message_template = welcome_message_template
        whatsapp_communication_doc.reference_dt = 'User'
        whatsapp_communication_doc.reference_dn = doc.name
        for template_parameter in template_doc.parameters:
            row = whatsapp_communication_doc.append('parameters')
            row.parameter = template_parameter.parameter
            if template_parameter.parameter == 'user':
                row.value = doc.full_name
        whatsapp_communication_doc.save()
        whatsapp_communication_doc.send_message()
        frappe.db.set_value('User', doc.name, 'whatsapp_2f_authenticated', 1)
        frappe.db.commit()
