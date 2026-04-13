import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import get_datetime, time_diff_in_hours

class DailyActivityLog(Document):
    def validate(self):
        self.validate_one_per_day()
        self.calculate_total_hours()
        self.flag_if_late()

    def validate_one_per_day(self):
        if not self.is_new():
            return
        existing = frappe.db.count(
            "Daily Activity Log",
            {
                "placement": self.placement,
                "date": self.date,
                "name": ["!=", self.name],
                "status": ["!=", "Draft"],  # allow multiple drafts, only one submitted
            },
        )
        if existing:
            frappe.throw(
                _("A Daily Activity Log for {0} on {1} has already been submitted.").format(
                    self.placement, self.date
                )
            )

    def calculate_total_hours(self):
        if self.time_in and self.time_out:
            try:
                hours = time_diff_in_hours(
                    f"2000-01-01 {self.time_out}",
                    f"2000-01-01 {self.time_in}"
                )
                self.total_hours = round(max(hours, 0), 2)
            except Exception:
                pass

    def flag_if_late(self):
        if self.status != "Submitted":
            return
        settings = frappe.get_single("IVIAMS Settings Singleton")
        cutoff = settings.daily_log_cutoff_time
        if not cutoff:
            return
        from frappe.utils import now_datetime, get_time
        now = now_datetime()
        cutoff_today = get_datetime(f"{self.date} {cutoff}")
        self.is_late = 1 if now > cutoff_today else 0