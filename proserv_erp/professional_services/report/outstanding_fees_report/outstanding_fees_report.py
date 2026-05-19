import frappe
from frappe import _
from frappe.utils import flt, date_diff, nowdate


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters or {})
    return columns, data


def get_columns():
    return [
        {"label": _("Fee Note"), "fieldname": "name", "fieldtype": "Link", "options": "Fee Note", "width": 140},
        {"label": _("Client"), "fieldname": "client", "fieldtype": "Link", "options": "Client", "width": 160},
        {"label": _("Total"), "fieldname": "total", "fieldtype": "Currency", "width": 120},
        {"label": _("Due Date"), "fieldname": "due_date", "fieldtype": "Date", "width": 110},
        {"label": _("Days Overdue"), "fieldname": "days_overdue", "fieldtype": "Int", "width": 120},
        {"label": _("Aging Bucket"), "fieldname": "aging_bucket", "fieldtype": "Data", "width": 120},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
    ]


def get_data(filters):
    rows = frappe.db.sql("""
        SELECT name, client, total, due_date, `status`
        FROM `tabFee Note`
        WHERE `status` NOT IN ('Paid') AND docstatus < 2
        ORDER BY due_date ASC
    """, as_dict=True)

    today = nowdate()
    result = []
    for r in rows:
        days = date_diff(today, r.due_date) if r.due_date else 0
        if days <= 0:
            bucket = "Not Yet Due"
        elif days <= 30:
            bucket = "0-30 Days"
        elif days <= 60:
            bucket = "31-60 Days"
        elif days <= 90:
            bucket = "61-90 Days"
        else:
            bucket = "90+ Days"
        result.append({
            "name": r.name,
            "client": r.client,
            "total": flt(r.total),
            "due_date": r.due_date,
            "days_overdue": max(days, 0),
            "aging_bucket": bucket,
            "status": r.status,
        })
    return result
