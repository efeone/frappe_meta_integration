import frappe
import requests
from frappe_meta_integration.whatsapp.utils import *

def customer_on_update(doc, method):
    '''
        Send WhatsApp Message to Customer, if enabled in WhatsApp Cloud API Settings and haven't send yet.
    '''
    if frappe.db.get_single_value("WhatsApp Cloud API Settings", "send_message_on_customer_creation") and doc.whatsapp_number and doc.is_welcome_message_sent==0:
        parameters = { 'username': doc.customer_name, 'company': frappe.defaults.get_user_default("company") }
        send_welcome_message(doc.whatsapp_number, parameters)
        doc.is_welcome_message_sent = 1
        doc.save()

def patient_on_update(doc, method):
    '''
        Update WhatsApp Number in Customer while updating WhatsApp Number in Patient.
    '''
    if frappe.db.get_single_value("Healthcare Settings", "link_customer_to_patient"):
        if doc.customer and doc.whatsapp_number:
            customer = frappe.get_doc("Customer", doc.customer)
            customer.whatsapp_number = doc.whatsapp_number
            customer.ignore_mandatory = True
            customer.save(ignore_permissions=True)
