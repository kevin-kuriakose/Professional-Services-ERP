import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters or {})
    return columns, data


def get_columns():
    return [
        {"label": _("Item"), "fieldname": "item_name", "fieldtype": "Data", "width": 200},
        {"label": _("Type"), "fieldname": "item_type", "fieldtype": "Data", "width": 140},
        {"label": _("Due Date"), "fieldname": "due_date", "fieldtype": "Date", "width": 110},
        {"label": _("Responsible"), "fieldname": "responsible", "fieldtype": "Data", "width": 150},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
    ]


def get_data(filters):
    result = []

    obligations = frappe.db.sql("""
        SELECT obligation_name, due_date, responsible_staff, `status`
        FROM `tabCompliance Obligation`
        WHERE `status` != 'Filed' AND docstatus < 2
        ORDER BY due_date ASC
    """, as_dict=True)
    for r in obligations:
        result.append({
            "item_name": r.obligation_name,
            "item_type": "Compliance Obligation",
            "due_date": r.due_date,
            "responsible": r.responsible_staff,
            "status": r.status,
        })

    certs = frappe.db.sql("""
        SELECT CONCAT(staff, ' - ', certificate_type) AS cert_name,
               expiry_date, staff, renewal_status
        FROM `tabPractice Certificate`
        WHERE renewal_status != 'Valid' OR expiry_date <= DATE_ADD(CURDATE(), INTERVAL 60 DAY)
        ORDER BY expiry_date ASC
    """, as_dict=True)
    for r in certs:
        result.append({
            "item_name": r.cert_name,
            "item_type": "Practice Certificate",
            "due_date": r.expiry_date,
            "responsible": r.staff,
            "status": r.renewal_status,
        })

    result.sort(key=lambda x: str(x.get("due_date") or "9999-99-99"))
    return result
