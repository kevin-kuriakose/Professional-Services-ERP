import frappe
from frappe.model.document import Document
from frappe.utils import flt, nowdate


class FeeNote(Document):

    def validate(self):
        self._calculate_totals()

    def _calculate_totals(self):
        milestone_total = sum(flt(r.billing_amount) for r in (self.milestones_covered or []))
        timesheet_total = sum(flt(r.billable_amount) for r in (self.timesheets_covered or []))
        expense_total = sum(flt(r.amount) for r in (self.expenses_covered or []))
        subtotal = milestone_total + timesheet_total + expense_total
        self.subtotal = subtotal
        net = flt(subtotal) - flt(self.discount)
        self.gst_amount = net * 0.18
        self.total = net + flt(self.gst_amount)

    def on_submit(self):
        self._create_sales_invoice()

    def on_cancel(self):
        self._cancel_sales_invoice()

    def _create_sales_invoice(self):
        if self.erpnext_sales_invoice:
            return

        company = frappe.db.get_single_value("Global Defaults", "default_company")
        if not company:
            frappe.log_error("FeeNote: No default company set — skipping Sales Invoice creation.")
            return

        abbr = frappe.db.get_value("Company", company, "abbr") or "XX"
        customer = self._get_customer(company)
        income_account = self.income_account or f"Professional Fees - {abbr}"
        cost_center = self.cost_center

        items = [{
            "item_code": self._get_or_create_item(),
            "qty": 1,
            "rate": flt(self.total),
            "income_account": income_account,
            "cost_center": cost_center,
            "description": f"Fee Note {self.name} — Engagement: {self.engagement or 'N/A'}",
        }]

        si = frappe.get_doc({
            "doctype": "Sales Invoice",
            "customer": customer,
            "company": company,
            "posting_date": nowdate(),
            "due_date": self.due_date or nowdate(),
            "items": items,
            "custom_source_doctype": "Fee Note",
            "custom_source_name": self.name,
        })
        si.insert(ignore_permissions=True)
        si.submit()
        self.db_set("erpnext_sales_invoice", si.name)
        frappe.db.commit()

    def _get_customer(self, company):
        if self.client:
            customer = frappe.db.get_value("Client", self.client, "erpnext_customer")
            if customer and frappe.db.exists("Customer", customer):
                return customer
        if not frappe.db.exists("Customer", "Walk-in Client"):
            frappe.get_doc({
                "doctype": "Customer",
                "customer_name": "Walk-in Client",
                "customer_type": "Individual",
                "customer_group": "All Customer Groups",
                "territory": "All Territories",
            }).insert(ignore_permissions=True)
            frappe.db.commit()
        return "Walk-in Client"

    def _get_or_create_item(self):
        item_name = "Professional Services Revenue"
        if not frappe.db.exists("Item", item_name):
            frappe.get_doc({
                "doctype": "Item",
                "item_code": item_name,
                "item_name": item_name,
                "item_group": "Services",
                "is_stock_item": 0,
                "is_sales_item": 1,
            }).insert(ignore_permissions=True)
            frappe.db.commit()
        return item_name

    def _cancel_sales_invoice(self):
        if not self.erpnext_sales_invoice:
            return
        try:
            si = frappe.get_doc("Sales Invoice", self.erpnext_sales_invoice)
            if si.docstatus == 1:
                si.cancel()
            self.db_set("erpnext_sales_invoice", None)
            frappe.db.commit()
        except Exception as e:
            frappe.log_error(f"FeeNote cancel SI error: {e}")
