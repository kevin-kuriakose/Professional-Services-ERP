import frappe


def execute():
    if frappe.db.exists("Workspace", "ProEdge"):
        return
    frappe.logger().info("ProEdge: workspace patch — workspace already handled by migrate.")
