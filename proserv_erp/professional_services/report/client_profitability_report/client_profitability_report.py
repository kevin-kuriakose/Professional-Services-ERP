import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters or {})
    return columns, data


def get_columns():
    return [
        {"label": _("Client"), "fieldname": "client", "fieldtype": "Link", "options": "Client", "width": 180},
        {"label": _("Total Billed"), "fieldname": "total_billed", "fieldtype": "Currency", "width": 130},
        {"label": _("Outstanding"), "fieldname": "outstanding", "fieldtype": "Currency", "width": 130},
        {"label": _("Engagement Count"), "fieldname": "engagement_count", "fieldtype": "Int", "width": 140},
    ]


def get_data(filters):
    rows = frappe.db.sql("""
        SELECT
            fn.client,
            SUM(fn.total) AS total_billed,
            SUM(CASE WHEN fn.`status` NOT IN ('Paid') THEN fn.total ELSE 0 END) AS outstanding,
            COUNT(DISTINCT fn.engagement) AS engagement_count
        FROM `tabFee Note` fn
        WHERE fn.docstatus < 2
        GROUP BY fn.client
        ORDER BY total_billed DESC
    """, as_dict=True)

    return [
        {
            "client": r.client,
            "total_billed": flt(r.total_billed),
            "outstanding": flt(r.outstanding),
            "engagement_count": r.engagement_count,
        }
        for r in rows
    ]
