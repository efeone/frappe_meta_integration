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
