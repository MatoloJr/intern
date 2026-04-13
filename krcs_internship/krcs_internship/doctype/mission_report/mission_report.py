from frappe.model.document import Document
import frappe
from frappe import _

class MissionReport(Document):
    def validate(self):
        if not self.placements:
            frappe.throw(_("At least one placement must be linked to a Mission Report."))

    def on_submit(self):
        self._record_digital_sig()

    def _record_digital_sig(self):
        from frappe.utils import now_datetime
        import frappe.utils
        self.supervisor_digital_signature = (
            f"{frappe.session.user} | {frappe.utils.get_fullname(frappe.session.user)} "
            f"| {frappe.local.request_ip if frappe.local.request_ip else 'unknown'} "
            f"| {now_datetime()}"
        )
        self.db_update()