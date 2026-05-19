import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters or {})
    return columns, data


def get_columns():
    return [
        {"label": _("Prepared By"), "fieldname": "prepared_by", "fieldtype": "Link", "options": "User", "width": 160},
        {"label": _("Total Proposals"), "fieldname": "total", "fieldtype": "Int", "width": 130},
        {"label": _("Won"), "fieldname": "won", "fieldtype": "Int", "width": 90},
        {"label": _("Lost"), "fieldname": "lost", "fieldtype": "Int", "width": 90},
        {"label": _("Win Rate %"), "fieldname": "win_rate", "fieldtype": "Percent", "width": 110},
        {"label": _("Total Fee (Won)"), "fieldname": "won_fee", "fieldtype": "Currency", "width": 140},
    ]


def get_data(filters):
    rows = frappe.db.sql("""
        SELECT
            prepared_by,
            COUNT(*) AS total,
            SUM(CASE WHEN `status` = 'Won' THEN 1 ELSE 0 END) AS won,
            SUM(CASE WHEN `status` = 'Lost' THEN 1 ELSE 0 END) AS lost,
            SUM(CASE WHEN `status` = 'Won' THEN total_fee ELSE 0 END) AS won_fee
        FROM `tabProposal`
        WHERE docstatus < 2
        GROUP BY prepared_by
        ORDER BY won DESC
    """, as_dict=True)

    result = []
    for r in rows:
        total = r.total or 0
        won = r.won or 0
        win_rate = (won / total * 100) if total else 0
        result.append({
            "prepared_by": r.prepared_by,
            "total": total,
            "won": won,
            "lost": r.lost or 0,
            "win_rate": win_rate,
            "won_fee": flt(r.won_fee),
        })
    return result
