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
        {"label": _("Engagement"), "fieldname": "engagement", "fieldtype": "Link", "options": "Engagement", "width": 160},
        {"label": _("Allocated Hrs/Week"), "fieldname": "allocated_hours_per_week", "fieldtype": "Float", "width": 150},
        {"label": _("Allocation %"), "fieldname": "allocation_percent", "fieldtype": "Percent", "width": 120},
        {"label": _("Start Date"), "fieldname": "start_date", "fieldtype": "Date", "width": 110},
        {"label": _("End Date"), "fieldname": "end_date", "fieldtype": "Date", "width": 110},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
    ]


def get_data(filters):
    rows = frappe.db.sql("""
        SELECT staff, engagement, allocated_hours_per_week,
               allocation_percent, start_date, end_date, `status`
        FROM `tabResource Allocation`
        WHERE docstatus < 2
        ORDER BY start_date DESC
    """, as_dict=True)

    return [
        {
            "staff": r.staff,
            "engagement": r.engagement,
            "allocated_hours_per_week": flt(r.allocated_hours_per_week),
            "allocation_percent": flt(r.allocation_percent),
            "start_date": r.start_date,
            "end_date": r.end_date,
            "status": r.status,
        }
        for r in rows
    ]
