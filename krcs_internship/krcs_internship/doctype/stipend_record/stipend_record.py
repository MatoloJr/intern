# stipend_record.py
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import add_months, add_days, getdate

class StipendRecord(Document):
    def validate(self):
        self.validate_volunteer_only()

    def validate_volunteer_only(self):
        programme_type = frappe.db.get_value("Placement", self.placement, "programme_type")
        # programme_type on Placement links to Programme Posting — need to get the actual type
        if programme_type:
            actual_type = frappe.db.get_value("Programme Posting", programme_type, "programme_type")
            if actual_type != "Volunteering":
                frappe.throw(_("Stipend Records can only be created for Volunteering placements."))

    def after_insert(self):
        self.generate_payment_schedule()

    def generate_payment_schedule(self):
        placement = frappe.get_doc("Placement", self.placement)
        if not placement.start_date or not placement.end_date:
            return

        dates = []
        current = getdate(placement.start_date)
        end = getdate(placement.end_date)

        while current <= end:
            dates.append(str(current))
            if self.frequency == "Weekly":
                current = add_days(current, 7)
            elif self.frequency == "Bi-Weekly":
                current = add_days(current, 14)
            else:  # Monthly
                current = add_months(current, 1)

        for payment_date in dates:
            entry = frappe.new_doc("Stipend Payment Entry")
            entry.stipend_record = self.name
            entry.payment_date = payment_date
            entry.amount = self.amount
            entry.status = "Pending"
            entry.insert(ignore_permissions=True)

        frappe.db.commit()