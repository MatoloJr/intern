# stipend_payment_entry.py
import frappe
from frappe import _
from frappe.model.document import Document

class StipendPaymentEntry(Document):
    def validate(self):
        self.prevent_modification_if_processed()

    def prevent_modification_if_processed(self):
        if self.is_new():
            return
        old_status = frappe.db.get_value("Stipend Payment Entry", self.name, "status")
        if old_status == "Processed" and self.status != "Processed":
            frappe.throw(_("A Processed payment entry cannot be modified."))

    def on_update(self):
        if self.has_value_changed("status"):
            self._notify_on_status_change()

    def _notify_on_status_change(self):
        stipend = frappe.get_doc("Stipend Record", self.stipend_record)
        placement = frappe.get_doc("Placement", stipend.placement)
        volunteer_email = frappe.db.get_value("User Profile", placement.participant, "email")
        
        settings = frappe.get_single("IVIAMS Settings Singleton")
        hov_email = frappe.db.get_value("User", settings.head_of_volunteers, "email") if settings.head_of_volunteers else None

        if self.status == "Processed" and volunteer_email:
            frappe.sendmail(
                recipients=[volunteer_email],
                subject="Stipend Payment Processed",
                message=f"<p>Your stipend payment of <strong>KES {self.amount:,.0f}</strong> "
                        f"for {self.payment_date} has been processed. "
                        f"Reference: {self.reference_number}</p>",
            )
        elif self.status == "Failed":
            recipients = []
            if volunteer_email:
                recipients.append(volunteer_email)
            if hov_email:
                recipients.append(hov_email)
            if recipients:
                frappe.sendmail(
                    recipients=recipients,
                    subject="Stipend Payment Failed",
                    message=f"<p>The stipend payment of KES {self.amount:,.0f} "
                            f"for {self.payment_date} has failed. "
                            f"Please follow up with Finance.</p>",
                )