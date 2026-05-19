import frappe
from frappe.model.document import Document
from frappe.utils import flt


class Proposal(Document):

    def validate(self):
        self.total_fee = sum(flt(r.fee) for r in (self.services_included or []))
