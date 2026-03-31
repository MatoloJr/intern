import frappe
from frappe import _
from frappe.utils import today, now


# ─── Public: Internship Postings ──────────────────────────────────────────────

@frappe.whitelist(allow_guest=True)
def get_postings(status="Published", department=None,
                 location=None, duration=None, stipend_type=None,
                 search=None, limit=20, offset=0):
    filters = {"status": status}
    if department:
        filters["department"] = department
    if location:
        filters["location"] = location
    if duration:
        filters["duration"] = duration
    if stipend_type:
        filters["stipend_type"] = stipend_type

    postings = frappe.get_all(
        "Internship Posting",
        filters=filters,
        fields=["name", "title", "department", "location", "duration",
                "deadline", "stipend_type", "stipend_amount", "description",
                "positions", "applications_count", "featured",
                "status", "posted_date"],
        limit=int(limit),
        start=int(offset),
        order_by="featured desc, posted_date desc"
    )

    if search:
        search = search.lower()
        postings = [
            p for p in postings
            if search in (p.title or "").lower()
            or search in (p.department or "").lower()
            or search in (p.location or "").lower()
        ]

    return postings


@frappe.whitelist(allow_guest=True)
def get_posting(name):
    doc = frappe.get_doc("Internship Posting", name)
    if doc.status not in ("Published",):
        frappe.throw(_("Posting not found"), frappe.DoesNotExistError)

    data = doc.as_dict()
    # Parse newline-separated text fields into lists for Vue
    data["responsibilities_list"] = _split_lines(doc.responsibilities)
    data["requirements_list"] = _split_lines(doc.requirements)
    data["skills_list"] = _split_lines(doc.skills)

    # Fetch similar postings (same dept, excluding this one)
    data["similar"] = frappe.get_all(
        "Internship Posting",
        filters={
            "department": doc.department,
            "status": "Published",
            "name": ["!=", name]
        },
        fields=["name", "title", "department", "location",
                "duration", "deadline", "stipend_type",
                "stipend_amount", "positions", "applications_count"],
        limit=3
    )
    return data


@frappe.whitelist(allow_guest=True)
def get_departments():
    return frappe.get_all(
        "Departments",
        fields=["name", "department", "supervisor"]
    )


# ─── Public: Applications ──────────────────────────────────────────────────────

@frappe.whitelist(allow_guest=True)
def submit_application(posting, applicant_name, email, phone,
                        university, course, year_of_study,
                        cover_letter="", school_letter=""):
    # Duplicate check
    if frappe.db.exists("Intern Application", {"posting": posting, "email": email}):
        frappe.throw(_("You have already applied for this position."))

    # Validate posting exists and is open (allow WALK-IN as a special case)
    if posting != "WALK-IN":
        if not frappe.db.exists("Internship Posting", posting):
            frappe.throw(_("Posting not found."))
        p = frappe.get_doc("Internship Posting", posting)
        if p.status != "Published":
            frappe.throw(_("This posting is no longer accepting applications."))
        if p.deadline and p.deadline < today():
            frappe.throw(_("The application deadline for this posting has passed."))

    doc = frappe.new_doc("Intern Application")
    doc.posting = posting if posting != "WALK-IN" else None
    doc.applicant_name = applicant_name
    doc.email = email
    doc.phone = phone
    # university and course are Link fields — store the value as-is
    # (frontend sends the name of the linked doc or free text)
    doc.university = university
    doc.course = course
    doc.year_of_study = year_of_study
    doc.cover_letter = cover_letter
    doc.school_letter = school_letter
    doc.status = "Pending"
    doc.date_applied = today()

    # Seed the timeline — field name is 'actions' per Application Timeline doctype
    doc.append("timeline", {
        "date": today(),
        "actions": "Application submitted",
        "by": frappe.session.user
    })

    doc.insert(ignore_permissions=True)

    # Increment applications_count on the posting
    if posting != "WALK-IN":
        frappe.db.set_value(
            "Internship Posting", posting,
            "applications_count",
            (frappe.db.get_value("Internship Posting", posting, "applications_count") or 0) + 1
        )

    frappe.db.commit()

    return {
        "name": doc.name,
        "message": "Application submitted successfully",
        "reference": doc.name
    }


@frappe.whitelist(allow_guest=True)
def get_application_status(email):
    apps = frappe.get_all(
        "Intern Application",
        filters={"email": email},
        fields=["name", "posting", "applicant_name",
                "status", "date_applied", "modified"]
    )
    for app in apps:
        if app.get("posting"):
            posting_data = frappe.db.get_value(
                "Internship Posting",
                app["posting"],
                ["title", "department", "location"],
                as_dict=True
            )
            if posting_data:
                app.update(posting_data)

        # Attach timeline — field name is 'actions' per Application Timeline doctype
        app["timeline"] = frappe.get_all(
            "Application Timeline",
            filters={"parent": app["name"]},
            fields=["date", "actions", "by"],
            order_by="date asc"
        )
    return apps


# ─── Public: Messages ─────────────────────────────────────────────────────────

@frappe.whitelist(allow_guest=True)
def get_messages(email):
    filters = {}
    if email:
        filters["to_email"] = email

    messages = frappe.get_all(
        "Intern Message",
        filters=filters,
        fields=["name", "subject", "body", "from_user",
                "message_type", "read", "sent_date", "application"],
        order_by="sent_date desc"
    )
    return messages


@frappe.whitelist(allow_guest=True)
def mark_message_read(name):
    frappe.db.set_value("Intern Message", name, "read", 1)
    frappe.db.commit()
    return {"message": "Marked as read"}


# ─── Admin: Postings Management ───────────────────────────────────────────────

@frappe.whitelist()
def create_posting(title, department, location, duration, deadline,
                    positions, stipend_type, stipend_amount=0,
                    description="", responsibilities="",
                    requirements="", skills="", featured=0,
                    status="Draft"):
    _require_admin()
    doc = frappe.new_doc("Internship Posting")
    doc.update({
        "title": title,
        "department": department,
        "location": location,
        "duration": duration,
        "deadline": deadline,
        "positions": int(positions),
        "stipend_type": stipend_type,
        "stipend_amount": float(stipend_amount or 0),
        "description": description,
        "responsibilities": responsibilities,
        "requirements": requirements,
        "skills": skills,
        "featured": int(featured),
        "status": status,
        "posted_date": today(),
        "applications_count": 0
    })
    doc.insert()
    frappe.db.commit()
    return doc.as_dict()


@frappe.whitelist()
def update_posting(name, **kwargs):
    _require_admin()
    doc = frappe.get_doc("Internship Posting", name)
    allowed = ["title", "department", "location", "duration", "deadline",
               "positions", "stipend_type", "stipend_amount", "description",
               "responsibilities", "requirements", "skills",
               "featured", "status"]
    for key in allowed:
        if key in kwargs:
            setattr(doc, key, kwargs[key])
    doc.save()
    frappe.db.commit()
    return doc.as_dict()


@frappe.whitelist()
def delete_posting(name):
    _require_admin()
    frappe.delete_doc("Internship Posting", name)
    frappe.db.commit()
    return {"message": "Deleted"}


# ─── Admin: Applications Management ──────────────────────────────────────────

@frappe.whitelist()
def admin_get_applications(posting=None, status=None,
                             search=None, limit=50, offset=0):
    _require_admin()
    filters = {}
    if posting:
        filters["posting"] = posting
    if status:
        filters["status"] = status

    apps = frappe.get_all(
        "Intern Application",
        filters=filters,
        fields=["name", "posting", "applicant_name", "email",
                "phone", "university", "course", "year_of_study",
                "status", "date_applied", "cv"],
        limit=int(limit),
        start=int(offset),
        order_by="date_applied desc"
    )

    if search:
        s = search.lower()
        apps = [a for a in apps
                if s in (a.applicant_name or "").lower()
                or s in (a.email or "").lower()]

    for app in apps:
        if app.get("posting"):
            posting_data = frappe.db.get_value(
                "Internship Posting",
                app["posting"],
                ["title", "department"],
                as_dict=True
            )
            if posting_data:
                app.update(posting_data)

        app["timeline"] = frappe.get_all(
            "Application Timeline",
            filters={"parent": app["name"]},
            fields=["date", "actions", "by"],
            order_by="date asc"
        )
    return apps


@frappe.whitelist()
def update_application_status(name, status, note=""):
    _require_admin()
    doc = frappe.get_doc("Intern Application", name)
    old_status = doc.status
    doc.status = status

    action_text = f"Status changed to {status}"
    if note:
        action_text += f": {note}"

    doc.append("timeline", {
        "date": today(),
        "actions": action_text,
        "by": frappe.session.user
    })

    doc.save()

    # Send a message to the applicant
    _send_status_message(doc, old_status, status)

    frappe.db.commit()
    return {"message": "Status updated"}


@frappe.whitelist()
def admin_send_message(to_email, subject, body, application=None):
    _require_admin()
    doc = frappe.new_doc("Intern Message")
    doc.to_email = to_email
    doc.subject = subject
    doc.body = body
    doc.message_type = "Message"
    doc.from_user = frappe.session.user
    doc.sent_date = now()
    doc.read = 0
    if application:
        doc.application = application
    doc.insert()
    frappe.db.commit()
    return {"message": "Message sent"}


# ─── Admin: Reports ───────────────────────────────────────────────────────────

@frappe.whitelist()
def get_dashboard_stats():
    _require_admin()
    return {
        "active_postings": frappe.db.count(
            "Internship Posting", {"status": "Published"}),
        "total_applications": frappe.db.count("Intern Application"),
        "pending_review": frappe.db.count(
            "Intern Application",
            {"status": ["in", ["Pending", "Under Review"]]}),
        "shortlisted": frappe.db.count(
            "Intern Application",
            {"status": ["in", ["Shortlisted", "Accepted"]]}),
        "accepted": frappe.db.count(
            "Intern Application", {"status": "Accepted"}),
        "rejected": frappe.db.count(
            "Intern Application", {"status": "Rejected"}),
    }


@frappe.whitelist()
def get_applications_by_department():
    _require_admin()
    depts = frappe.db.sql("""
        SELECT ip.department, COUNT(ia.name) as count
        FROM `tabIntern Application` ia
        JOIN `tabInternship Posting` ip ON ia.posting = ip.name
        GROUP BY ip.department
        ORDER BY count DESC
    """, as_dict=True)
    return depts


@frappe.whitelist()
def get_applications_by_university():
    _require_admin()
    return frappe.db.sql("""
        SELECT university,
               COUNT(*) as total,
               SUM(CASE WHEN status = 'Accepted' THEN 1 ELSE 0 END) as accepted
        FROM `tabIntern Application`
        WHERE university IS NOT NULL AND university != ''
        GROUP BY university
        ORDER BY total DESC
    """, as_dict=True)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _require_admin():
    if not frappe.has_permission("Internship Posting", "write"):
        frappe.throw(_("Not permitted"), frappe.PermissionError)


def _split_lines(text):
    if not text:
        return []
    return [l.strip() for l in text.split("\n") if l.strip()]


def _send_status_message(app_doc, old_status, new_status):
    status_messages = {
        "Under Review": "Your application is now under review by our team.",
        "Shortlisted": "Congratulations! You have been shortlisted.",
        "Accepted": "Congratulations! Your application has been accepted.",
        "Rejected": "Thank you for applying. Unfortunately your application was not successful."
    }
    body = status_messages.get(new_status)
    if not body:
        return

    posting_title = "General Application"
    if app_doc.posting:
        posting_title = frappe.db.get_value(
            "Internship Posting", app_doc.posting, "title") or posting_title

    msg = frappe.new_doc("Intern Message")
    msg.to_email = app_doc.email
    msg.subject = f"Application Update: {posting_title}"
    msg.body = (
        f"Dear {app_doc.applicant_name},<br><br>"
        f"{body}<br><br>"
        f"Reference: {app_doc.name}"
    )
    msg.message_type = "Notification"
    msg.from_user = frappe.session.user
    msg.sent_date = now()
    msg.read = 0
    msg.application = app_doc.name
    msg.insert(ignore_permissions=True)