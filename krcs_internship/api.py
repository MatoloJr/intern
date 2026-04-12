import frappe
from frappe import _
from frappe.utils import today, now


# ─── Public: Programme Postings ──────────────────────────────────────────────

@frappe.whitelist(allow_guest=True)
def get_postings(status="Published", department=None,
				 location=None, duration=None, stipend_type=None,
				 search=None, limit=20, offset=0):
	filters = {}

	if status and status != "":
		filters["status"] = status

	if department:
		filters["department"] = department
	if location:
		filters["location"] = location
	if duration:
		filters["duration"] = duration
	if stipend_type:
		filters["stipend_type"] = stipend_type

	postings = frappe.get_all(
		"Programme Posting",
		filters=filters,
		fields=["name", "title", "department", "location", "duration",
				"deadline", "stipend_type", "stipend_amount", "description",
				"positions", "applications_count", "featured",
				"status", "posted_date"],
		limit=int(limit),
		start=int(offset),
		order_by="featured desc, posted_date desc",
		ignore_permissions=True   # ← Guest has no DocType read role; bypass permission check
	)

	if search:
		s = search.lower()
		postings = [
			p for p in postings
			if s in (p.title or "").lower()
			or s in (p.department or "").lower()
			or s in (p.location or "").lower()
		]

	return postings


@frappe.whitelist(allow_guest=True)
def get_posting(name):
	if not frappe.db.exists("Programme Posting", name):
		frappe.throw(_("Posting not found"), frappe.DoesNotExistError)

	doc = frappe.get_doc("Programme Posting", name)

	if frappe.session.user == "Guest" and doc.status != "Published":
		frappe.throw(_("Posting not found"), frappe.DoesNotExistError)

	data = doc.as_dict()
	data["responsibilities_list"] = _split_lines(doc.responsibilities)
	data["requirements_list"] = _split_lines(doc.requirements)
	data["skills_list"] = _split_lines(doc.skills)

	data["similar"] = frappe.get_all(
		"Programme Posting",
		filters={
			"department": doc.department,
			"status": "Published",
			"name": ["!=", name]
		},
		fields=["name", "title", "department", "location",
				"duration", "deadline", "stipend_type",
				"stipend_amount", "positions", "applications_count"],
		limit=3,
		ignore_permissions=True
	)
	return data


@frappe.whitelist(allow_guest=True)
def get_departments():
	return frappe.get_all(
		"Departments",
		fields=["name", "department", "supervisor"],
		ignore_permissions=True
	)


@frappe.whitelist(allow_guest=True)
def get_universities():
	return frappe.get_all(
		"Universities",
		fields=["name", "name1 as university_name", "location", "type"],
		ignore_permissions=True
	)


@frappe.whitelist(allow_guest=True)
def get_courses():
	return frappe.get_all(
		"Courses",
		fields=["name", "name_of_course", "abbreviation"],
		ignore_permissions=True
	)


# ─── Public: Applications ──────────────────────────────────────────────────────

@frappe.whitelist(allow_guest=True)
def submit_application(posting, applicant_name, email, phone,
						university, course, year_of_study,
						cover_letter="", school_letter=""):
	if not applicant_name or not str(applicant_name).strip():
		frappe.throw(_("Applicant name is required."))
	if not email or not str(email).strip():
		frappe.throw(_("Email is required."))

	applicant_name = str(applicant_name).strip()
	email = str(email).strip()

	is_walk_in = not posting or str(posting).strip() in ("", "WALK-IN", "None", "null")
	actual_posting = None

	if not is_walk_in:
		if not frappe.db.exists("Programme Posting", posting):
			frappe.throw(_("Posting not found."))
		p = frappe.get_doc("Programme Posting", posting)
		if p.status != "Published":
			frappe.throw(_("This posting is no longer accepting applications."))
		if p.deadline and str(p.deadline) < today():
			frappe.throw(_("The application deadline for this posting has passed."))
		existing = frappe.get_all(
			"Intern Application",
			filters={"posting": posting, "email": email},
			ignore_permissions=True,
			limit=1
		)
		if existing:
			frappe.throw(_("You have already applied for this position."))
		actual_posting = posting
	else:
		existing_walkin = frappe.get_all(
			"Intern Application",
			filters={"posting": ["is", "not set"], "email": email, "date_applied": today()},
			ignore_permissions=True,
			limit=1
		)
		if existing_walkin:
			frappe.throw(_("You have already submitted a walk-in application today."))

	doc = frappe.new_doc("Intern Application")

	if actual_posting:
		doc.posting = actual_posting

	doc.applicant_name = applicant_name
	doc.email = email
	doc.phone = phone or ""
	doc.university = _resolve_link("Universities", university)
	doc.course = _resolve_link("Courses", course)
	doc.year_of_study = year_of_study or ""
	doc.cover_letter = cover_letter or ""
	doc.school_letter = school_letter or ""
	doc.status = "Pending"
	doc.date_applied = today()

	notes_parts = []
	if university and not doc.university:
		notes_parts.append(f"University: {university}")
	if course and not doc.course:
		notes_parts.append(f"Course: {course}")
	if notes_parts:
		doc.notes = "\n".join(notes_parts)

	doc.append("timeline", {
		"date": today(),
		"actions": "Application submitted",
		"by": frappe.session.user
	})

	doc.insert(ignore_permissions=True, ignore_mandatory=True)

	if actual_posting:
		current = frappe.db.get_value(
			"Programme Posting", actual_posting, "applications_count") or 0
		frappe.db.set_value(
			"Programme Posting", actual_posting,
			"applications_count", current + 1,
			update_modified=False
		)

	frappe.db.commit()

	return {
		"name": doc.name,
		"message": "Application submitted successfully",
		"reference": doc.name
	}


@frappe.whitelist(allow_guest=True)
def get_application_status(email):
	if not email:
		return []

	apps = frappe.get_all(
		"Intern Application",
		filters={"email": str(email).strip()},
		fields=["name", "posting", "applicant_name",
				"status", "date_applied", "modified", "notes"],
		ignore_permissions=True
	)
	for app in apps:
		if app.get("posting"):
			posting_data = frappe.db.get_value(
				"Programme Posting",
				app["posting"],
				["title", "department", "location"],
				as_dict=True
			)
			if posting_data:
				app.update(posting_data)
		else:
			app["title"] = "Walk-in Application"
			app["department"] = ""
			app["location"] = ""

		app["timeline"] = frappe.get_all(
			"Application Timeline",
			filters={"parent": app["name"]},
			fields=["date", "actions", "by"],
			order_by="date asc",
			ignore_permissions=True
		)
	return apps


# ─── Public: Messages ─────────────────────────────────────────────────────────

@frappe.whitelist(allow_guest=True)
def get_messages(email):
	if not frappe.db.table_exists("tabIntern Message"):
		return []

	filters = {}
	if email:
		filters["to_email"] = email

	return frappe.get_all(
		"Intern Message",
		filters=filters,
		fields=["name", "subject", "body", "from_user",
				"message_type", "read", "sent_date", "application"],
		order_by="sent_date desc",
		ignore_permissions=True
	)


@frappe.whitelist(allow_guest=True)
def mark_message_read(name):
	if not frappe.db.table_exists("tabIntern Message"):
		return {"message": "Table not found"}
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
	doc = frappe.new_doc("Programme Posting")
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
	doc = frappe.get_doc("Programme Posting", name)
	allowed = ["title", "department", "location", "duration", "deadline",
			   "positions", "stipend_type", "stipend_amount", "description",
			   "responsibilities", "requirements", "skills",
			   "featured", "status"]
	for key in allowed:
		if key in kwargs:
			val = kwargs[key]
			if key == "featured":
				val = int(val) if val is not None else 0
			elif key == "positions":
				val = int(val) if val else 0
			elif key == "stipend_amount":
				val = float(val) if val else 0.0
			setattr(doc, key, val)
	doc.save()
	frappe.db.commit()
	return doc.as_dict()


@frappe.whitelist()
def delete_posting(name):
	_require_admin()
	frappe.delete_doc("Programme Posting", name)
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
				"status", "date_applied", "cv", "notes"],
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
				"Programme Posting",
				app["posting"],
				["title", "department"],
				as_dict=True
			)
			if posting_data:
				app.update(posting_data)
		else:
			app["title"] = "Walk-in Application"
			app["department"] = "—"

		app["timeline"] = frappe.get_all(
			"Application Timeline",
			filters={"parent": app["name"]},
			fields=["date", "actions", "by"],
			order_by="date asc"
		)

		if app.get("university"):
			uni_name = frappe.db.get_value("Universities", app["university"], "name1")
			app["university"] = uni_name or app["university"]
		if app.get("course"):
			course_name = frappe.db.get_value("Courses", app["course"], "name_of_course")
			app["course"] = course_name or app["course"]

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
	_send_status_message(doc, old_status, status)
	frappe.db.commit()
	return {"message": "Status updated"}


@frappe.whitelist()
def admin_send_message(to_email, subject, body, application=None):
	_require_admin()
	if not frappe.db.table_exists("tabIntern Message"):
		frappe.throw(_("Intern Message DocType not found. Run bench migrate."))
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
			"Programme Posting", {"status": "Published"}),
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
	return frappe.db.sql("""
		SELECT
			COALESCE(ip.department, 'Walk-in') AS department,
			COUNT(ia.name) AS count
		FROM `tabIntern Application` ia
		LEFT JOIN `tabProgramme Posting` ip ON ia.posting = ip.name
		GROUP BY COALESCE(ip.department, 'Walk-in')
		ORDER BY count DESC
	""", as_dict=True)


@frappe.whitelist()
def get_applications_by_university():
	_require_admin()
	return frappe.db.sql("""
		SELECT
			COALESCE(u.name1, ia.university, 'Unknown') AS university,
			COUNT(*) AS total,
			SUM(CASE WHEN ia.status = 'Accepted' THEN 1 ELSE 0 END) AS accepted
		FROM `tabIntern Application` ia
		LEFT JOIN `tabUniversities` u ON ia.university = u.name
		GROUP BY COALESCE(u.name1, ia.university, 'Unknown')
		ORDER BY total DESC
		LIMIT 20
	""", as_dict=True)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _require_admin():
	if not frappe.has_permission("Programme Posting", "write"):
		frappe.throw(_("Not permitted"), frappe.PermissionError)


def _split_lines(text):
	if not text:
		return []
	return [line.strip() for line in text.split("\n") if line.strip()]


def _resolve_link(doctype, value):
	if not value or not str(value).strip():
		return None
	value = str(value).strip()
	if frappe.db.exists(doctype, value):
		return value
	if doctype == "Universities":
		match = frappe.db.get_value("Universities", {"name1": value}, "name")
		return match or None
	if doctype == "Courses":
		match = frappe.db.get_value("Courses", {"name_of_course": value}, "name")
		return match or None
	return None


def _send_status_message(app_doc, old_status, new_status):
	if not frappe.db.table_exists("tabIntern Message"):
		return

	status_messages = {
		"Under Review": "Your application is now under review by our team.",
		"Shortlisted": "Congratulations! You have been shortlisted for the next stage.",
		"Accepted": "Congratulations! Your application has been accepted. Our team will be in touch with next steps.",
		"Rejected": "Thank you for applying to KRCS. Unfortunately your application was not successful this time."
	}
	body = status_messages.get(new_status)
	if not body:
		return

	posting_title = "General Application"
	if app_doc.posting:
		posting_title = frappe.db.get_value(
			"Programme Posting", app_doc.posting, "title") or posting_title

	try:
		msg = frappe.new_doc("Intern Message")
		msg.to_email = app_doc.email
		msg.subject = f"Application Update: {posting_title}"
		msg.body = (
			f"Dear {app_doc.applicant_name},<br><br>"
			f"{body}<br><br>"
			f"Reference: <strong>{app_doc.name}</strong><br><br>"
			f"Best regards,<br>KRCS Internship Team"
		)
		msg.message_type = "Notification"
		msg.from_user = frappe.session.user
		msg.sent_date = now()
		msg.read = 0
		msg.application = app_doc.name
		msg.insert(ignore_permissions=True)
	except Exception as e:
		frappe.log_error(str(e), "Intern Message Insert Failed")