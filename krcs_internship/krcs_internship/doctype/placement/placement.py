# krcs_internship/krcs_internship/doctype/placement/placement.py

import frappe
from frappe import _
from frappe.model.document import Document

class Placement(Document):
    def validate(self):
        self.validate_dates()
        if self.status == "Terminated":
            if not self.termination_reason:
                frappe.throw(_("Termination reason is required when terminating a placement."))
            if not self.termination_date:
                frappe.throw(_("Termination date is required."))

    def validate_dates(self):
        if self.start_date and self.end_date:
            if self.start_date >= self.end_date:
                frappe.throw(_("End date must be after start date."))

    def on_update(self):
        if self.status == "Terminated":
            self._halt_stipend_payments()

    def _halt_stipend_payments(self):
        """Mark all pending stipend payments as Failed on termination."""
        pending = frappe.get_all(
            "Stipend Payment Entry",
            filters={
                "stipend_record": ["in",
                    frappe.get_all("Stipend Record",
                        filters={"placement": self.name},
                        pluck="name")
                ],
                "status": "Pending",
            },
            pluck="name",
        )
        for name in pending:
            frappe.db.set_value("Stipend Payment Entry", name, "status", "Failed")