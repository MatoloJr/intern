import frappe
from frappe.utils import today, get_first_day_of_week, add_days, nowdate

def compile_weekly_reports():
    """Runs every Friday. Creates draft Weekly Reports for all active placements."""
    from frappe.utils import getdate, get_weekday
    
    if get_weekday(getdate(today())) != "Friday":
        # Only run on Fridays (Frappe scheduler weekly runs on Sundays by default,
        # so we guard explicitly here)
        settings = frappe.get_single("IVIAMS Settings Singleton")
        compile_day = settings.weekly_report_compile_day or "Friday"
        if get_weekday(getdate(today())) != compile_day:
            return

    active_placements = frappe.get_all(
        "Placement",
        filters={"status": "Active"},
        fields=["name", "participant", "supervisor"],
    )

    week_end = today()
    week_start = add_days(week_end, -6)

    for p in active_placements:
        # Skip if report already exists for this week
        exists = frappe.db.exists("Weekly Report", {
            "placement": p.name,
            "week_start": week_start,
        })
        if exists:
            continue

        # Fetch daily logs for this week
        logs = frappe.get_all(
            "Daily Activity Log",
            filters={
                "placement": p.name,
                "date": ["between", [week_start, week_end]],
                "status": "Submitted",
            },
            fields=["name", "date", "total_hours", "tasks_completed",
                    "outcomes", "challenges", "is_late"],
        )

        total_hours = sum(l.total_hours or 0 for l in logs)
        gaps = 5 - len([l for l in logs if l.date])  # working days without a log
        late_count = sum(1 for l in logs if l.is_late)

        # Get cumulative hours (all previous approved weekly reports)
        prev_hours = frappe.db.sql("""
            SELECT COALESCE(SUM(total_hours), 0) as total
            FROM `tabWeekly Report`
            WHERE placement = %s AND status = 'Approved'
              AND week_end < %s
        """, (p.name, week_start), as_dict=True)[0].total

        report = frappe.new_doc("Weekly Report")
        report.placement = p.name
        report.participant = p.participant
        report.week_start = week_start
        report.week_end = week_end
        report.total_hours = total_hours
        report.cumulative_hours = (prev_hours or 0) + total_hours
        report.gaps_in_logging = max(gaps, 0)
        report.late_submissions_count = late_count
        report.status = "Participant Review"
        report.insert(ignore_permissions=True)

        # Notify participant
        participant_email = frappe.db.get_value(
            "User Profile", p.participant, "email"
        )
        if participant_email:
            frappe.sendmail(
                recipients=[participant_email],
                subject="Your Weekly Report is Ready for Review",
                message=f"""
                <p>Your draft Weekly Report for {week_start} to {week_end} is ready.</p>
                <p>Please log in to the portal, review the report, add your personal summary, 
                and submit it to your supervisor.</p>
                <p>Total hours this week: <strong>{total_hours}</strong></p>
                """,
            )

    frappe.db.commit()

def send_timesheet_reminders():
    """Daily task: remind participants of approaching/overdue timesheets."""
    from frappe.utils import getdate, add_days
    
    settings = frappe.get_single("IVIAMS Settings Singleton")
    deadline_day = settings.time_sheet_deadline_day or "Monday"
    overdue_hours = settings.timesheet_overdue_reminder_hours or 48
    
    today_weekday = getdate(today()).strftime("%A")
    
    active_placements = frappe.get_all("Placement", filters={"status": "Active"}, pluck="name")
    
    for placement in active_placements:
        p_doc = frappe.get_doc("Placement", placement)
        participant_email = frappe.db.get_value("User Profile", p_doc.participant, "email")
        if not participant_email:
            continue
        
        # Check if last week's timesheet exists and is submitted
        last_monday = add_days(today(), -7)
        last_sunday = add_days(today(), -1)
        
        ts = frappe.db.exists("IVIAMS Timesheet", {
            "placement": placement,
            "week_start": last_monday,
            "status": ["in", ["Submitted", "Approved"]],
        })
        
        if not ts and today_weekday == deadline_day:
            frappe.sendmail(
                recipients=[participant_email],
                subject="Timesheet Submission Reminder",
                message=f"<p>Your timesheet for week {last_monday} to {last_sunday} is due. "
                        f"Please submit it as soon as possible.</p>",
            )

def send_evaluation_reminders():
    settings = frappe.get_single("IVIAMS Settings Singleton")
    mid_days = settings.mid_programme_evaluation_reminder_days or 0
    end_days = settings.end_programme_evaluation_reminder_days or 7

    active = frappe.get_all(
        "Placement",
        filters={"status": "Active"},
        fields=["name", "supervisor", "start_date", "end_date"],
    )

    from frappe.utils import date_diff, getdate, today as _today

    for p in active:
        if not p.start_date or not p.end_date:
            continue
        
        total_days = date_diff(p.end_date, p.start_date)
        mid_date = add_days(p.start_date, total_days // 2)
        end_reminder_date = add_days(p.end_date, -end_days)

        supervisor_email = frappe.db.get_value("Supervisor", p.supervisor, "email")
        if not supervisor_email:
            continue

        t = getdate(_today())

        # Mid-programme reminder
        if getdate(mid_date) == t:
            has_mid = frappe.db.exists("Performance Evaluation", {
                "placement": p.name, "evaluation_type": "Mid Programme"
            })
            if not has_mid:
                frappe.sendmail(
                    recipients=[supervisor_email],
                    subject="Mid-Programme Evaluation Due",
                    message=f"<p>Please complete the mid-programme evaluation for placement "
                            f"<strong>{p.name}</strong>.</p>",
                )

        # End-of-programme reminder
        if getdate(end_reminder_date) == t:
            has_end = frappe.db.exists("Performance Evaluation", {
                "placement": p.name, "evaluation_type": "End of Programme"
            })
            if not has_end:
                frappe.sendmail(
                    recipients=[supervisor_email],
                    subject="End-of-Programme Evaluation Due",
                    message=f"<p>Please complete the end-of-programme evaluation for placement "
                            f"<strong>{p.name}</strong>.</p>",
                )