import frappe
from frappe import _
from frappe.model.document import Document

class PerformanceEvaluation(Document):
    def validate(self):
        self.validate_scores()
        self.calculate_overall_score()
        self.check_threshold()

    def validate_scores(self):
        fields = [
            "punctuality_attendance", "quality_of_work", "communication",
            "initiative", "teamwork", "policy_compliance", "professional_conduct"
        ]
        for f in fields:
            val = getattr(self, f, None)
            if val is not None and not (1 <= val <= 5):
                frappe.throw(_(f"{f.replace('_', ' ').title()} must be between 1 and 5."))

    def calculate_overall_score(self):
        fields = [
            "punctuality_attendance", "quality_of_work", "communication",
            "initiative", "teamwork", "policy_compliance", "professional_conduct"
        ]
        scores = [getattr(self, f) for f in fields if getattr(self, f)]
        self.overall_score = round(sum(scores) / len(scores), 2) if scores else 0

    def check_threshold(self):
        settings = frappe.get_single("IVIAMS Settings Singleton")
        threshold = settings.performance_flag_threshold or 2.5
        self.below_threshold = 1 if self.overall_score < threshold else 0

    def on_update(self):
        if self.status == "Submitted":
            self._notify_coordinator()

    def _notify_coordinator(self):
        placement = frappe.get_doc("Placement", self.placement)
        # Get coordinator/admin to notify
        settings = frappe.get_single("IVIAMS Settings Singleton")
        # ... sendmail logic
        pass