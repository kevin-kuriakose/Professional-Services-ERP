import frappe
from frappe.model.document import Document
from frappe.utils import flt


class ExpenseClaim(Document):

    def validate(self):
        self._calculate_total()

    def _calculate_total(self):
        self.total_amount = sum(flt(row.amount) for row in (self.expenses or []))
