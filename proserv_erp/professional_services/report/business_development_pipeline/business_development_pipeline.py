import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters or {})
    return columns, data


def get_columns():
    return [
        {"label": _("Opportunity"), "fieldname": "opportunity_name", "fieldtype": "Data", "width": 180},
        {"label": _("Client"), "fieldname": "client", "fieldtype": "Link", "options": "Client", "width": 150},
        {"label": _("Stage"), "fieldname": "stage", "fieldtype": "Data", "width": 130},
        {"label": _("Estimated Value"), "fieldname": "estimated_value", "fieldtype": "Currency", "width": 140},
        {"label": _("Probability %"), "fieldname": "probability_percent", "fieldtype": "Percent", "width": 120},
        {"label": _("Assigned Partner"), "fieldname": "assigned_partner", "fieldtype": "Link", "options": "User", "width": 140},
    ]


def get_data(filters):
    rows = frappe.db.sql("""
        SELECT opportunity_name, client, stage,
               estimated_value, probability_percent, assigned_partner
        FROM `tabOpportunity`
        WHERE docstatus < 2 AND stage NOT IN ('Closed Won', 'Closed Lost')
        ORDER BY estimated_value DESC
    """, as_dict=True)

    return [
        {
            "opportunity_name": r.opportunity_name,
            "client": r.client,
            "stage": r.stage,
            "estimated_value": flt(r.estimated_value),
            "probability_percent": flt(r.probability_percent),
            "assigned_partner": r.assigned_partner,
        }
        for r in rows
    ]
