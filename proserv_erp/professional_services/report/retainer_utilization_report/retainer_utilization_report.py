import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters or {})
    return columns, data


def get_columns():
    return [
        {"label": _("Retainer Agreement"), "fieldname": "retainer_agreement", "fieldtype": "Link", "options": "Retainer Agreement", "width": 180},
        {"label": _("Month"), "fieldname": "month", "fieldtype": "Data", "width": 100},
        {"label": _("Included Hours"), "fieldname": "included_hours", "fieldtype": "Float", "width": 120},
        {"label": _("Hours Consumed"), "fieldname": "hours_consumed", "fieldtype": "Float", "width": 130},
        {"label": _("Closing Balance"), "fieldname": "closing_balance_hours", "fieldtype": "Float", "width": 130},
        {"label": _("Overage Hours"), "fieldname": "overage_hours", "fieldtype": "Float", "width": 120},
        {"label": _("Overage Billed"), "fieldname": "overage_billed_amount", "fieldtype": "Currency", "width": 130},
    ]


def get_data(filters):
    rows = frappe.db.sql("""
        SELECT
            rc.retainer_agreement,
            rc.month,
            ra.included_hours_per_month AS included_hours,
            rc.hours_consumed,
            rc.closing_balance_hours,
            rc.overage_hours,
            rc.overage_billed_amount
        FROM `tabRetainer Consumption` rc
        LEFT JOIN `tabRetainer Agreement` ra ON ra.name = rc.retainer_agreement
        WHERE rc.docstatus < 2
        ORDER BY rc.month DESC
    """, as_dict=True)

    return [
        {
            "retainer_agreement": r.retainer_agreement,
            "month": r.month,
            "included_hours": flt(r.included_hours),
            "hours_consumed": flt(r.hours_consumed),
            "closing_balance_hours": flt(r.closing_balance_hours),
            "overage_hours": flt(r.overage_hours),
            "overage_billed_amount": flt(r.overage_billed_amount),
        }
        for r in rows
    ]
