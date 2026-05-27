import frappe
from frappe.model.document import Document
from frappe.utils import flt, nowdate


class RetainerConsumption(Document):

    def validate(self):
        self._calculate_closing_balance()

    def _calculate_closing_balance(self):
        closing = flt(self.opening_balance_hours) + flt(self.hours_added) - flt(self.hours_consumed)
        self.closing_balance_hours = closing
        self.overage_hours = abs(closing) if closing < 0 else 0

    def on_submit(self):
        if flt(self.overage_billed_amount) > 0:
            self._create_overage_invoice()

    def on_cancel(self):
        self._cancel_sales_invoice()

    def _create_overage_invoice(self):
        if self.erpnext_sales_invoice:
            return
        company = frappe.db.get_single_value("Global Defaults", "default_company")
        if not company:
            return
        abbr = frappe.db.get_value("Company", company, "abbr") or "XX"

        client = frappe.db.get_value("Retainer Agreement", self.retainer_agreement, "client")
        customer = "Walk-in Client"
        if client:
            customer = frappe.db.get_value("Client", client, "erpnext_customer") or "Walk-in Client"

        item_name = "Retainer Fee Revenue"
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

        si = frappe.get_doc({
            "doctype": "BA Sales Invoice",
            "customer": customer,
            "company": company,
            "posting_date": nowdate(),
            "due_date": nowdate(),
            "items": [{
                "item_code": item_name,
                "qty": 1,
                "rate": flt(self.overage_billed_amount),
                "income_account": f"Retainer Income - {abbr}",
                "description": f"Retainer overage — {self.retainer_agreement} {self.month}",
            }],
        })
        si.insert(ignore_permissions=True)
        si.submit()
        self.db_set("erpnext_sales_invoice", si.name)
        frappe.db.commit()

    def _cancel_sales_invoice(self):
        if not self.erpnext_sales_invoice:
            return
        try:
            si = frappe.get_doc("BA Sales Invoice", self.erpnext_sales_invoice)
            if si.docstatus == 1:
                si.cancel()
            self.db_set("erpnext_sales_invoice", None)
            frappe.db.commit()
        except Exception as e:
            frappe.log_error(f"RetainerConsumption cancel SI error: {e}")
