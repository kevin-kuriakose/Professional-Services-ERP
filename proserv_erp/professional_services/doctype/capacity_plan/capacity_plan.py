import frappe
from frappe.model.document import Document
from frappe.utils import flt


class CapacityPlan(Document):

    def validate(self):
        for row in (self.staff or []):
            row.available_hours = flt(row.total_capacity_hours) - flt(row.allocated_hours)
            if flt(row.total_capacity_hours):
                row.utilization_percent = (flt(row.allocated_hours) / flt(row.total_capacity_hours)) * 100
            else:
                row.utilization_percent = 0
