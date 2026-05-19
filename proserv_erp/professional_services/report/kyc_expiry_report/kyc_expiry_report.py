import frappe
from frappe import _
from frappe.utils import date_diff, nowdate


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters or {})
    return columns, data


def get_columns():
    return [
        {"label": _("KYC Record"), "fieldname": "name", "fieldtype": "Link", "options": "KYC Record", "width": 140},
        {"label": _("Client"), "fieldname": "client", "fieldtype": "Link", "options": "Client", "width": 160},
        {"label": _("Document Type"), "fieldname": "identity_document_type", "fieldtype": "Data", "width": 150},
        {"label": _("Document Number"), "fieldname": "document_number", "fieldtype": "Data", "width": 140},
        {"label": _("Expiry Date"), "fieldname": "document_expiry", "fieldtype": "Date", "width": 110},
        {"label": _("Days to Expiry"), "fieldname": "days_to_expiry", "fieldtype": "Int", "width": 120},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
    ]


def get_data(filters):
    rows = frappe.db.sql("""
        SELECT name, client, identity_document_type, document_number,
               document_expiry, `status`
        FROM `tabKYC Record`
        WHERE document_expiry <= DATE_ADD(CURDATE(), INTERVAL 60 DAY)
          AND `status` != 'Rejected'
          AND docstatus < 2
        ORDER BY document_expiry ASC
    """, as_dict=True)

    today = nowdate()
    result = []
    for r in rows:
        days = date_diff(r.document_expiry, today) if r.document_expiry else 0
        result.append({
            "name": r.name,
            "client": r.client,
            "identity_document_type": r.identity_document_type,
            "document_number": r.document_number,
            "document_expiry": r.document_expiry,
            "days_to_expiry": days,
            "status": r.status,
        })
    return result
