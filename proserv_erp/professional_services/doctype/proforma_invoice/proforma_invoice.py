import frappe
from frappe.model.document import Document
from frappe.utils import flt


class ProformaInvoice(Document):

    def validate(self):
        self._calculate_totals()

    def _calculate_totals(self):
        subtotal = sum(flt(row.amount) for row in (self.line_items or []))
        self.subtotal = subtotal
        gst_rate = 0.18
        self.gst = flt(subtotal - flt(self.discount)) * gst_rate
        self.total = flt(subtotal) - flt(self.discount) + flt(self.gst)
