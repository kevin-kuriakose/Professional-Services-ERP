import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters or {})
    return columns, data


def get_columns():
    return [
        {"label": _("Expense Claim"), "fieldname": "name", "fieldtype": "Link", "options": "Expense Claim", "width": 150},
        {"label": _("Staff"), "fieldname": "staff", "fieldtype": "Link", "options": "Staff Profile", "width": 150},
        {"label": _("Claim Date"), "fieldname": "claim_date", "fieldtype": "Date", "width": 110},
        {"label": _("Total Amount"), "fieldname": "total_amount", "fieldtype": "Currency", "width": 130},
        {"label": _("Reimbursement Status"), "fieldname": "reimbursement_status", "fieldtype": "Data", "width": 160},
    ]


def get_data(filters):
    rows = frappe.db.sql("""
        SELECT name, staff, claim_date, total_amount, reimbursement_status
        FROM `tabExpense Claim`
        WHERE docstatus < 2 AND reimbursement_status != 'Paid'
        ORDER BY claim_date ASC
    """, as_dict=True)

    return [
        {
            "name": r.name,
            "staff": r.staff,
            "claim_date": r.claim_date,
            "total_amount": flt(r.total_amount),
            "reimbursement_status": r.reimbursement_status,
        }
        for r in rows
    ]
