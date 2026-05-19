import frappe
from frappe.model.document import Document
from frappe.utils import flt


class Engagement(Document):

    def validate(self):
        self._check_budget_overrun()

    def _check_budget_overrun(self):
        if flt(self.estimated_hours) and flt(self.actual_hours) > flt(self.estimated_hours):
            frappe.msgprint(
                f"Actual hours ({flt(self.actual_hours)}) exceed estimated hours ({flt(self.estimated_hours)}).",
                indicator="orange",
                alert=True
            )

    def on_submit(self):
        pass

    def on_cancel(self):
        pass
