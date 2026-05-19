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
        {"label": _("Client"), "fieldname": "client", "fieldtype": "Link", "options": "Client", "width": 150},
        {"label": _("Budget"), "fieldname": "budget_amount", "fieldtype": "Currency", "width": 120},
        {"label": _("Estimated Hrs"), "fieldname": "estimated_hours", "fieldtype": "Float", "width": 120},
        {"label": _("Actual Hrs"), "fieldname": "actual_hours", "fieldtype": "Float", "width": 110},
        {"label": _("Total Billed"), "fieldname": "billed_amount", "fieldtype": "Currency", "width": 120},
        {"label": _("Margin %"), "fieldname": "margin_pct", "fieldtype": "Percent", "width": 110},
    ]


def get_data(filters):
    rows = frappe.db.sql("""
        SELECT
            e.name AS engagement,
            e.client,
            e.budget_amount,
            e.estimated_hours,
            e.actual_hours,
            e.billed_amount
        FROM `tabEngagement` e
        WHERE e.docstatus < 2
        ORDER BY e.billed_amount DESC
    """, as_dict=True)

    result = []
    for r in rows:
        billed = flt(r.billed_amount)
        budget = flt(r.budget_amount)
        margin_pct = ((billed - budget) / budget * 100) if budget else 0
        result.append({
            "engagement": r.engagement,
            "client": r.client,
            "budget_amount": budget,
            "estimated_hours": flt(r.estimated_hours),
            "actual_hours": flt(r.actual_hours),
            "billed_amount": billed,
            "margin_pct": margin_pct,
        })
    return result
