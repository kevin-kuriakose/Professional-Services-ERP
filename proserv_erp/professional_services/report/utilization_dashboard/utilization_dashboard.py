import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters or {})
    return columns, data


def get_columns():
    return [
        {"label": _("Staff"), "fieldname": "staff_name", "fieldtype": "Data", "width": 160},
        {"label": _("Practice Area"), "fieldname": "practice_area", "fieldtype": "Data", "width": 140},
        {"label": _("Billable Hours"), "fieldname": "billable_hours", "fieldtype": "Float", "width": 120},
        {"label": _("Non-Billable Hours"), "fieldname": "non_billable_hours", "fieldtype": "Float", "width": 140},
        {"label": _("Total Hours"), "fieldname": "total_hours", "fieldtype": "Float", "width": 110},
        {"label": _("Utilization %"), "fieldname": "utilization_pct", "fieldtype": "Percent", "width": 120},
    ]


def get_data(filters):
    rows = frappe.db.sql("""
        SELECT
            sp.staff_name,
            sp.practice_area,
            SUM(CASE WHEN te.billing_type = 'Billable' THEN te.hours ELSE 0 END) AS billable_hours,
            SUM(CASE WHEN te.billing_type != 'Billable' THEN te.hours ELSE 0 END) AS non_billable_hours,
            SUM(te.hours) AS total_hours
        FROM `tabTimesheet Entry` te
        LEFT JOIN `tabStaff Profile` sp ON sp.name = te.staff
        WHERE te.docstatus < 2
        GROUP BY te.staff
        ORDER BY total_hours DESC
    """, as_dict=True)

    result = []
    for row in rows:
        total = flt(row.total_hours)
        billable = flt(row.billable_hours)
        utilization_pct = (billable / total * 100) if total else 0
        result.append({
            "staff_name": row.staff_name,
            "practice_area": row.practice_area,
            "billable_hours": billable,
            "non_billable_hours": flt(row.non_billable_hours),
            "total_hours": total,
            "utilization_pct": utilization_pct,
        })
    return result
