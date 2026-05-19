import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters or {})
    return columns, data


def get_columns():
    return [
        {"label": _("Staff"), "fieldname": "staff", "fieldtype": "Link", "options": "Staff Profile", "width": 160},
        {"label": _("Submitted"), "fieldname": "submitted", "fieldtype": "Int", "width": 110},
        {"label": _("Approved"), "fieldname": "approved", "fieldtype": "Int", "width": 110},
        {"label": _("Rejected"), "fieldname": "rejected", "fieldtype": "Int", "width": 110},
        {"label": _("Total Hours"), "fieldname": "total_hours", "fieldtype": "Float", "width": 120},
    ]


def get_data(filters):
    rows = frappe.db.sql("""
        SELECT
            staff,
            SUM(CASE WHEN `status` = 'Submitted' THEN 1 ELSE 0 END) AS submitted,
            SUM(CASE WHEN `status` = 'Approved' THEN 1 ELSE 0 END) AS approved,
            SUM(CASE WHEN `status` = 'Rejected' THEN 1 ELSE 0 END) AS rejected,
            SUM(hours) AS total_hours
        FROM `tabTimesheet Entry`
        WHERE docstatus < 2
        GROUP BY staff
        ORDER BY staff
    """, as_dict=True)

    return [
        {
            "staff": r.staff,
            "submitted": r.submitted,
            "approved": r.approved,
            "rejected": r.rejected,
            "total_hours": flt(r.total_hours),
        }
        for r in rows
    ]
