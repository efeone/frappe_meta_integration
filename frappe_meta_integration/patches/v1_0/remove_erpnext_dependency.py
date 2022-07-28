from __future__ import unicode_literals
import frappe

def execute():
    frappe.enqueue(remove_custom_fields, queue='long')

def remove_custom_fields():
    if frappe.db.exists("Custom Field", {"fieldname": "whatsapp_number"}):
        custom_field_list = frappe.db.get_list("Custom Field", filters={"fieldname": "whatsapp_number"})
        for custom_field in custom_field_list:
            custom_field_doc = frappe.get_doc("Custom Field", custom_field.name)
            custom_field_doc.dt in ['Patient', 'Customer', 'Lab Test']
            custom_field_doc.delete()
        frappe.db.commit()
