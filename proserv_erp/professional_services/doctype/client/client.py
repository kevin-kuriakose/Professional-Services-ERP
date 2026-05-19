import frappe
from frappe.model.document import Document


class Client(Document):

    def after_insert(self):
        self._create_erpnext_customer()

    def _create_erpnext_customer(self):
        if self.erpnext_customer:
            return
        customer_name = self.client_name
        if not frappe.db.exists("Customer", customer_name):
            frappe.get_doc({
                "doctype": "Customer",
                "customer_name": customer_name,
                "customer_type": "Company" if self.client_type == "Company" else "Individual",
                "customer_group": "All Customer Groups",
                "territory": "All Territories",
            }).insert(ignore_permissions=True)
            frappe.db.commit()
        self.db_set("erpnext_customer", customer_name)
