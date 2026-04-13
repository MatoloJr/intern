import frappe
from frappe import _
from frappe.utils.pdf import get_pdf
import base64

LETTER_TEMPLATES = {
    "Industrial Attachment": "Industrial Attachment Placement Letter",
    "Internship": "Internship Offer Letter",
    "Volunteering": "Volunteering Engagement Letter",
}

def on_application_update(doc, method):
    if doc.status != "Accepted":
        return
    # Only trigger once — check if letter already sent
    if doc.get("__is_local"):
        return
    old_status = frappe.db.get_value("Intern Application", doc.name, "status",
                                      for_update=False)
    # The hook fires after save, so check the previous value via flags
    if not doc.flags.get("status_changed_to_accepted"):
        return
    _dispatch_programme_letter(doc)

def _dispatch_programme_letter(app_doc):
    programme_type = app_doc.programme_type
    if not programme_type:
        frappe.log_error(
            f"Intern Application {app_doc.name} has no programme_type — cannot dispatch letter.",
            "Letter Dispatch"
        )
        return

    template_name = LETTER_TEMPLATES.get(programme_type)
    if not template_name:
        return

    # Fetch active signatory
    signatory = frappe.db.get_value(
        "Signatory Profile",
        {"is_active": 1},
        ["full_name", "title", "signature_image"],
        as_dict=True,
    )

    # Render the print format to HTML, then convert to PDF
    try:
        html = frappe.get_print(
            "Intern Application",
            app_doc.name,
            print_format=template_name,
            as_pdf=False,
        )
        pdf_data = get_pdf(html)
    except Exception as e:
        frappe.log_error(str(e), "Letter PDF Generation Failed")
        return

    # Attach PDF to the application record
    file_name = f"{programme_type.replace(' ', '_')}_Letter_{app_doc.name}.pdf"
    file_doc = frappe.get_doc({
        "doctype": "File",
        "file_name": file_name,
        "attached_to_doctype": "Intern Application",
        "attached_to_name": app_doc.name,
        "content": base64.b64encode(pdf_data).decode(),
        "decode": True,
        "is_private": 0,
    })
    file_doc.insert(ignore_permissions=True)

    # Send email with PDF attached
    frappe.sendmail(
        recipients=[app_doc.email],
        subject=f"Your KRCS {programme_type} Application — Approved",
        message=f"""
        <p>Dear {app_doc.applicant_name},</p>
        <p>Congratulations! Your application for the <strong>{programme_type}</strong> 
        programme has been approved.</p>
        <p>Please find your formal programme letter attached to this email.</p>
        <p>Reference: <strong>{app_doc.name}</strong></p>
        <br><p>Best regards,<br>Kenya Red Cross Society</p>
        """,
        attachments=[{
            "fname": file_name,
            "fcontent": pdf_data,
        }],
    )
    frappe.db.commit()

@frappe.whitelist()
def digital_sign(doctype, docname, role):
    """
    Records an immutable digital acknowledgement.
    role: 'participant' or 'supervisor'
    """
    import frappe.utils
    from frappe.utils import now_datetime

    doc = frappe.get_doc(doctype, docname)
    
    sig_string = (
        f"{frappe.session.user} | "
        f"{frappe.utils.get_fullname(frappe.session.user)} | "
        f"{getattr(frappe.local, 'request_ip', 'unknown')} | "
        f"{now_datetime()}"
    )

    field_map = {
        "participant": "challenges",       # participant digital signature field in weekly report
        "supervisor": "supervisor_digital_signature",
    }
    field = field_map.get(role)
    if not field:
        frappe.throw(_("Invalid role for signing."))

    # Immutability check
    existing = frappe.db.get_value(doctype, docname, field)
    if existing:
        frappe.throw(_("This document has already been signed and cannot be re-signed."))

    frappe.db.set_value(doctype, docname, field, sig_string, update_modified=False)
    frappe.db.commit()
    return sig_string