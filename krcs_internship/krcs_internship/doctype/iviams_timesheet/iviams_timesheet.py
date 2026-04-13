import frappe
from frappe import _
from frappe.model.document import Document

class IVIAMSTimesheet(Document):
    def validate(self):
        self.pull_hours_from_daily_logs()

    def pull_hours_from_daily_logs(self):
        if not self.placement or not self.week_start or not self.week_end:
            return
        result = frappe.db.sql("""
            SELECT COALESCE(SUM(total_hours), 0) as total
            FROM `tabDaily Activity Log`
            WHERE placement = %s
              AND date BETWEEN %s AND %s
              AND status = 'Submitted'
        """, (self.placement, self.week_start, self.week_end), as_dict=True)
        self.total_hours = result[0].total if result else 0

    def on_update(self):
        if self.status == "Rejected" and not self.supervisor_comment:
            frappe.throw(_("A rejection comment is required."))