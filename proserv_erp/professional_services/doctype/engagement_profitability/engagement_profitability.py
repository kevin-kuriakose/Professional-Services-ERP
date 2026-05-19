import frappe
from frappe.model.document import Document
from frappe.utils import flt


class EngagementProfitability(Document):

    def validate(self):
        self.gross_margin = flt(self.total_billed) - flt(self.total_cost)
        if flt(self.total_billed):
            self.margin_percent = (flt(self.gross_margin) / flt(self.total_billed)) * 100
        else:
            self.margin_percent = 0
