import frappe
from frappe.utils import flt


def after_install():
    setup_erpnext_masters()


def setup_erpnext_masters():
    """Create required ERPNext Cost Centers, Income Accounts, and base Customer."""
    try:
        company = frappe.db.get_single_value("Global Defaults", "default_company")
        if not company:
            frappe.log_error("ProEdge: No default company set — skipping ERPNext master setup.")
            return

        abbr = frappe.db.get_value("Company", company, "abbr") or "XX"

        _create_cost_centers(company, abbr)
        _create_income_accounts(company, abbr)
        _create_walk_in_customer()
        _create_erpnext_items()
        frappe.db.commit()
        frappe.logger().info("ProEdge: ERPNext master setup complete.")
    except Exception as e:
        frappe.log_error(f"ProEdge install error: {e}")


def _create_cost_centers(company, abbr):
    parent_cc = frappe.db.get_value(
        "Cost Center",
        {"is_group": 1, "company": company},
        "name"
    )
    if not parent_cc:
        return

    centers = [
        "Professional Services Operations",
        "Client Delivery",
        "Business Development",
        "Administration",
    ]
    for cc_name in centers:
        full_name = f"{cc_name} - {abbr}"
        if not frappe.db.exists("Cost Center", full_name):
            frappe.get_doc({
                "doctype": "Cost Center",
                "cost_center_name": cc_name,
                "parent_cost_center": parent_cc,
                "company": company,
                "is_group": 0,
            }).insert(ignore_permissions=True)


def _create_income_accounts(company, abbr):
    parent_income = frappe.db.get_value(
        "Account",
        {"account_type": "Income Account", "is_group": 1, "company": company},
        "name"
    )
    if not parent_income:
        return

    accounts = [
        "Professional Fees",
        "Retainer Income",
        "Expense Reimbursements",
        "Advisory Income",
    ]
    for acc_name in accounts:
        if not frappe.db.exists("Account", {"account_name": acc_name, "company": company}):
            frappe.get_doc({
                "doctype": "Account",
                "account_name": acc_name,
                "parent_account": parent_income,
                "account_type": "Income Account",
                "company": company,
            }).insert(ignore_permissions=True)


def _create_walk_in_customer():
    if not frappe.db.exists("Customer", "Walk-in Client"):
        frappe.get_doc({
            "doctype": "Customer",
            "customer_name": "Walk-in Client",
            "customer_type": "Individual",
            "customer_group": "All Customer Groups",
            "territory": "All Territories",
        }).insert(ignore_permissions=True)


def _create_erpnext_items():
    items = [
        ("Professional Services Revenue", "Services"),
        ("Retainer Fee Revenue", "Services"),
        ("Expense Reimbursement", "Services"),
    ]
    for item_name, item_group in items:
        if not frappe.db.exists("Item", item_name):
            frappe.get_doc({
                "doctype": "Item",
                "item_code": item_name,
                "item_name": item_name,
                "item_group": item_group,
                "is_stock_item": 0,
                "is_sales_item": 1,
            }).insert(ignore_permissions=True)
