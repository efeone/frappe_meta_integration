import frappe
import requests
from frappe_meta_integration.whatsapp.utils import *

def customer_after_insert(doc, method):
    if frappe.db.get_single_value("WhatsApp Cloud API Settings", "send_message_on_customer_creation") and doc.whatsapp_number:
        parameters = { 'username': doc.customer_name, 'company': frappe.defaults.get_user_default("company") }
        send_welcome_message(doc.whatsapp_number, parameters)
        doc.is_welcome_message_sent = 1
        doc.save()
