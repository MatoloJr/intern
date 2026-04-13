# Copyright (c) 2026, Ash_Ok and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

ELIGIBILITY = {
    "Industrial Attachment": ["Undergraduate"],
    "Internship": ["Undergraduate", "Postgraduate"],
    "Volunteering": ["Postgraduate", "Graduate"],
}

class InternApplication(Document):
    def validate(self):
        self.validate_academic_eligibility()
        self.validate_single_active_placement()

    def validate_academic_eligibility(self):
        if not self.programme_type or not self.academic_level:
            return
        allowed = ELIGIBILITY.get(self.programme_type, [])
        if self.academic_level not in allowed:
            frappe.throw(
                _(
                    "Your academic level ({0}) is not eligible for {1}. "
                    "Eligible levels: {2}."
                ).format(
                    self.academic_level,
                    self.programme_type,
                    ", ".join(allowed)
                )
            )

    def validate_single_active_placement(self):
        # Prevent duplicate active applications for same posting
        if not self.programme_posting or self.is_new():
            return
        existing = frappe.db.count(
            "Intern Application",
            {
                "programme_posting": self.programme_posting,
                "applicant_name": self.applicant_name,
                "status": ["not in", ["Rejected"]],
                "name": ["!=", self.name],
            },
        )
        if existing:
            frappe.throw(_("You already have an active application for this posting."))