import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters or {})
    return columns, data


def get_columns():
    return [
        {"label": _("Engagement"), "fieldname": "engagement", "fieldtype": "Link", "options": "Engagement", "width": 180},
        {"label": _("Client"), "fieldname": "client", "fieldtype": "Link", "options": "Client", "width": 160},
        {"label": _("Staff"), "fieldname": "staff", "fieldtype": "Link", "options": "Staff Profile", "width": 150},
        {"label": _("Hours"), "fieldname": "hours", "fieldtype": "Float", "width": 100},
        {"label": _("WIP Amount"), "fieldname": "billable_amount", "fieldtype": "Currency", "width": 130},
    ]


def get_data(filters):
    rows = frappe.db.sql("""
        SELECT
            te.engagement,
            e.client,
            te.staff,
            SUM(te.hours) AS hours,
            SUM(te.billable_amount) AS billable_amount
        FROM `tabTimesheet Entry` te
        LEFT JOIN `tabEngagement` e ON e.name = te.engagement
        WHERE te.docstatus = 1
          AND te.`status` = 'Approved'
          AND te.billing_type = 'Billable'
        GROUP BY te.engagement, te.staff
        ORDER BY billable_amount DESC
    """, as_dict=True)

    return [
        {
            "engagement": r.engagement,
            "client": r.client,
            "staff": r.staff,
            "hours": flt(r.hours),
            "billable_amount": flt(r.billable_amount),
        }
        for r in rows
    ]
