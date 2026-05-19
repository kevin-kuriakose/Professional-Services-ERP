import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters or {})
    return columns, data


def get_columns():
    return [
        {"label": _("Client"), "fieldname": "client", "fieldtype": "Link", "options": "Client", "width": 160},
        {"label": _("Engagement"), "fieldname": "engagement", "fieldtype": "Link", "options": "Engagement", "width": 160},
        {"label": _("Billing Method"), "fieldname": "billing_method", "fieldtype": "Data", "width": 130},
        {"label": _("Practice Area"), "fieldname": "practice_area", "fieldtype": "Data", "width": 140},
        {"label": _("Total Billed"), "fieldname": "total", "fieldtype": "Currency", "width": 130},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
    ]


def get_data(filters):
    rows = frappe.db.sql("""
        SELECT
            fn.client,
            fn.engagement,
            e.billing_method,
            e.practice_area,
            SUM(fn.total) AS total,
            fn.`status`
        FROM `tabFee Note` fn
        LEFT JOIN `tabEngagement` e ON e.name = fn.engagement
        WHERE fn.docstatus < 2
        GROUP BY fn.client, fn.engagement
        ORDER BY total DESC
    """, as_dict=True)

    return [
        {
            "client": r.client,
            "engagement": r.engagement,
            "billing_method": r.billing_method,
            "practice_area": r.practice_area,
            "total": flt(r.total),
            "status": r.status,
        }
        for r in rows
    ]
