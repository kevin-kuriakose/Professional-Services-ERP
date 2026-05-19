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
        {"label": _("Billable Amount"), "fieldname": "billable_amount", "fieldtype": "Currency", "width": 140},
        {"label": _("Standard Rate Value"), "fieldname": "standard_value", "fieldtype": "Currency", "width": 150},
        {"label": _("Realization Rate %"), "fieldname": "realization_pct", "fieldtype": "Percent", "width": 140},
        {"label": _("Hours"), "fieldname": "hours", "fieldtype": "Float", "width": 100},
    ]


def get_data(filters):
    rows = frappe.db.sql("""
        SELECT
            te.staff,
            SUM(te.billable_amount) AS billable_amount,
            SUM(te.hours * sp.standard_billing_rate) AS standard_value,
            SUM(te.hours) AS hours
        FROM `tabTimesheet Entry` te
        LEFT JOIN `tabStaff Profile` sp ON sp.name = te.staff
        WHERE te.docstatus < 2 AND te.billing_type = 'Billable'
        GROUP BY te.staff
        ORDER BY billable_amount DESC
    """, as_dict=True)

    result = []
    for r in rows:
        billable = flt(r.billable_amount)
        standard = flt(r.standard_value)
        realization_pct = (billable / standard * 100) if standard else 0
        result.append({
            "staff": r.staff,
            "billable_amount": billable,
            "standard_value": standard,
            "realization_pct": realization_pct,
            "hours": flt(r.hours),
        })
    return result
