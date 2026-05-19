import frappe
from frappe.model.document import Document
from frappe.utils import flt


class TimesheetEntry(Document):

    def validate(self):
        self._calculate_billable_amount()

    def _calculate_billable_amount(self):
        if self.billing_type == "Billable":
            self.billable_amount = flt(self.hours) * flt(self.billing_rate)
        else:
            self.billable_amount = 0.0

    def on_submit(self):
        self._update_engagement_actual_hours()

    def on_cancel(self):
        self._update_engagement_actual_hours(reverse=True)

    def _update_engagement_actual_hours(self, reverse=False):
        if not self.engagement:
            return
        current = flt(frappe.db.get_value("Engagement", self.engagement, "actual_hours"))
        delta = flt(self.hours)
        new_val = current - delta if reverse else current + delta
        frappe.db.set_value("Engagement", self.engagement, "actual_hours", new_val)
        frappe.db.commit()
