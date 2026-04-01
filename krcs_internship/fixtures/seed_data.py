"""
krcs_internship/fixtures/seed_data.py

Run once to seed baseline reference data and sample postings.

Usage:
    bench --site intern.localhost execute krcs_internship.fixtures.seed_data.run
"""

import frappe
from frappe.utils import add_days, today


def run():
    """Seed all baseline data. Safe to run multiple times (idempotent)."""
    frappe.set_user("Administrator")

    seed_departments()
    seed_universities()
    seed_courses()
    seed_postings()

    frappe.db.commit()
    print("✅  Seed data loaded successfully.")


# ─── Departments ──────────────────────────────────────────────────────────────

DEPARTMENTS = [
    {"department": "PROGRAM",        "supervisor": "Program Manager"},
    {"department": "HR",             "supervisor": "HR Manager"},
    {"department": "AUDIT & RISK",   "supervisor": "Internal Auditor"},
    {"department": "PROCUREMENT",    "supervisor": "Supply Chain Manager"},
    {"department": "FINANCE",        "supervisor": "Finance Manager"},
    {"department": "GLOBAL FUND",    "supervisor": "Global Fund Coordinator"},
    {"department": "ICHA",           "supervisor": "ICHA Coordinator"},
    {"department": "NSD",            "supervisor": "NSD Manager"},
    {"department": "IT",             "supervisor": "ICT Manager"},
    {"department": "PR",             "supervisor": "Communications Manager"},
    {"department": "LEGAL",          "supervisor": "Legal Counsel"},
    {"department": "TRAINING SCHOOL","supervisor": "Training Coordinator"},
    {"department": "SECURITY",       "supervisor": "Security Manager"},
    {"department": "COMPLIANCE",     "supervisor": "Compliance Officer"},
]


def seed_departments():
    for d in DEPARTMENTS:
        if not frappe.db.exists("Departments", d["department"]):
            doc = frappe.new_doc("Departments")
            doc.department = d["department"]
            doc.supervisor = d["supervisor"]
            doc.insert(ignore_permissions=True)
            print(f"  Created department: {d['department']}")


# ─── Universities ─────────────────────────────────────────────────────────────

UNIVERSITIES = [
    {"name": "University of Nairobi",           "type": "University", "location": "Nairobi"},
    {"name": "Kenyatta University",             "type": "University", "location": "Nairobi"},
    {"name": "Strathmore University",           "type": "University", "location": "Nairobi"},
    {"name": "JKUAT",                           "type": "University", "location": "Juja"},
    {"name": "Moi University",                  "type": "University", "location": "Eldoret"},
    {"name": "Maseno University",               "type": "University", "location": "Kisumu"},
    {"name": "Egerton University",              "type": "University", "location": "Nakuru"},
    {"name": "Technical University of Kenya",   "type": "University", "location": "Nairobi"},
    {"name": "Kenya Methodist University",      "type": "University", "location": "Meru"},
    {"name": "Daystar University",              "type": "University", "location": "Nairobi"},
    {"name": "United States International University", "type": "University", "location": "Nairobi"},
    {"name": "Mount Kenya University",          "type": "University", "location": "Thika"},
    {"name": "Kenya Coast National Polytechnic","type": "College",    "location": "Mombasa"},
    {"name": "Kenya Medical Training College",  "type": "College",    "location": "Nairobi"},
]


def seed_universities():
    for u in UNIVERSITIES:
        if not frappe.db.exists("Universities", u["name"]):
            doc = frappe.new_doc("Universities")
            doc.name = u["name"]       # autoname = prompt, so name is set directly
            doc.name1 = u["name"]
            doc.type = u["type"]
            doc.location = u["location"]
            doc.insert(ignore_permissions=True)
            print(f"  Created university: {u['name']}")


# ─── Courses ──────────────────────────────────────────────────────────────────

COURSES = [
    {"name_of_course": "Bachelor of Business Information Technology", "abbreviation": "BBIT"},
    {"name_of_course": "Bachelor of Science in Computer Science",     "abbreviation": "BSc CS"},
    {"name_of_course": "Bachelor of Science in Information Technology","abbreviation": "BSc IT"},
    {"name_of_course": "Bachelor of Commerce",                         "abbreviation": "BCom"},
    {"name_of_course": "Bachelor of Science in Nursing",              "abbreviation": "BSc Nursing"},
    {"name_of_course": "Bachelor of Public Health",                   "abbreviation": "BPH"},
    {"name_of_course": "Bachelor of Science in Civil Engineering",    "abbreviation": "BSc CE"},
    {"name_of_course": "Bachelor of Arts in Communications",         "abbreviation": "BA Comm"},
    {"name_of_course": "Bachelor of Laws",                           "abbreviation": "LLB"},
    {"name_of_course": "Bachelor of Science in Finance",             "abbreviation": "BSc Finance"},
    {"name_of_course": "Bachelor of Science in Accounting",         "abbreviation": "BSc Acct"},
    {"name_of_course": "Bachelor of Science in Procurement",        "abbreviation": "BSc Proc"},
    {"name_of_course": "Diploma in Information Technology",         "abbreviation": "DIT"},
    {"name_of_course": "Diploma in Business Administration",        "abbreviation": "DBA"},
    {"name_of_course": "Bachelor of Science in Cybersecurity",      "abbreviation": "BSc CySec"},
    {"name_of_course": "Bachelor of Science in Telecommunications", "abbreviation": "BSc Telecom"},
    {"name_of_course": "Bachelor of Science in Biomedical Science", "abbreviation": "BSc BioMed"},
    {"name_of_course": "Bachelor of Science in Statistics",         "abbreviation": "BSc Stats"},
    {"name_of_course": "Master of Business Administration",         "abbreviation": "MBA"},
    {"name_of_course": "Bachelor of Education",                     "abbreviation": "BEd"},
]


def seed_courses():
    for c in COURSES:
        if not frappe.db.exists("Courses", c["name_of_course"]):
            doc = frappe.new_doc("Courses")
            doc.name_of_course = c["name_of_course"]
            doc.abbreviation = c["abbreviation"]
            doc.insert(ignore_permissions=True)
            print(f"  Created course: {c['name_of_course']}")


# ─── Internship Postings ──────────────────────────────────────────────────────

POSTINGS = [
    {
        "title": "IT Systems Support Intern",
        "department": "IT",
        "location": "Nairobi",
        "duration": "3 months",
        "stipend_type": "Paid",
        "stipend_amount": 15000,
        "positions": 2,
        "featured": 1,
        "status": "Published",
        "description": "<p>Join the KRCS ICT team and gain hands-on experience supporting internal systems, helpdesk operations, and digital infrastructure across our national operations.</p>",
        "responsibilities": "Provide first-line IT helpdesk support to staff\nAssist with network troubleshooting and maintenance\nSupport server room operations and monitoring\nDocument IT processes and update knowledge base\nAssist in deploying software updates across branches",
        "requirements": "Currently enrolled in BSc Computer Science, IT, or related field\nMinimum Second Class Upper Division\nKnowledge of Windows Server and Active Directory\nStrong problem-solving skills",
        "skills": "Windows Server\nNetworking\nActive Directory\nHelpdesk Support\nDocumentation",
    },
    {
        "title": "Finance & Accounting Intern",
        "department": "FINANCE",
        "location": "Nairobi",
        "duration": "3 months",
        "stipend_type": "Paid",
        "stipend_amount": 12000,
        "positions": 3,
        "featured": 1,
        "status": "Published",
        "description": "<p>Support the Finance department in day-to-day accounting operations, financial reporting, and budget monitoring across KRCS programs.</p>",
        "responsibilities": "Assist with processing payments and reconciliations\nSupport preparation of financial statements and donor reports\nVerify invoices and procurement documentation\nMaintain accurate financial records and filing\nAssist during annual audit preparations",
        "requirements": "Pursuing BCom, BSc Finance, BSc Accounting, or CPA\nProficiency in MS Excel and accounting software\nStrong attention to detail\nKnowledge of IPSAS or IFRS a plus",
        "skills": "Excel\nQuickBooks\nFinancial Reporting\nReconciliation\nDonor Reporting",
    },
    {
        "title": "Communications & PR Intern",
        "department": "PR",
        "location": "Nairobi",
        "duration": "3 months",
        "stipend_type": "Paid",
        "stipend_amount": 10000,
        "positions": 2,
        "featured": 1,
        "status": "Published",
        "description": "<p>Support the Communications team in producing content, managing social media, and documenting humanitarian stories across KRCS programs.</p>",
        "responsibilities": "Write press releases, blog posts, and social media content\nPhotograph and document field activities\nAssist with media monitoring and reporting\nSupport event coordination and documentation\nUpdate website content and newsletters",
        "requirements": "Pursuing BA Communications, Journalism, Media Studies, or related\nStrong writing skills in English and Swahili\nBasic photography and video editing skills\nSocial media management experience",
        "skills": "Content Writing\nSocial Media\nPhotography\nWordPress\nCanva",
    },
    {
        "title": "Human Resources Intern",
        "department": "HR",
        "location": "Nairobi",
        "duration": "3 months",
        "stipend_type": "Unpaid",
        "stipend_amount": 0,
        "positions": 2,
        "featured": 0,
        "status": "Published",
        "description": "<p>Support the HR department in recruitment, staff welfare, and HR administration for one of Kenya's largest humanitarian organizations.</p>",
        "responsibilities": "Assist with recruitment coordination and shortlisting\nMaintain employee records and HR databases\nSupport onboarding processes for new staff and interns\nAssist in organising staff training and welfare activities\nPrepare HR reports and correspondence",
        "requirements": "Pursuing Bachelor's in Human Resource Management or Business\nKnowledge of Kenyan labour laws\nExcellent communication and interpersonal skills\nConfidentiality and professionalism",
        "skills": "Recruitment\nHR Information Systems\nEmployment Law\nMS Office\nReport Writing",
    },
    {
        "title": "Public Health Intern — Mombasa Branch",
        "department": "PROGRAM",
        "location": "Mombasa",
        "duration": "6 months",
        "stipend_type": "Paid",
        "stipend_amount": 18000,
        "positions": 4,
        "featured": 1,
        "status": "Published",
        "description": "<p>Support public health programs at the KRCS Mombasa branch, including community health education, WASH activities, and disease surveillance.</p>",
        "responsibilities": "Conduct community health education sessions\nAssist in WASH (Water, Sanitation and Hygiene) activities\nCollect and compile health surveillance data\nSupport health camps and blood donation drives\nWrite field reports and document beneficiary data",
        "requirements": "Pursuing BSc Public Health, Nursing, Community Health, or related\nFluent in Swahili and English\nWilling to work in coastal region communities\nValid NHIF cover",
        "skills": "Public Health\nCommunity Mobilisation\nData Collection\nReport Writing\nFirst Aid",
    },
    {
        "title": "Legal & Compliance Intern",
        "department": "LEGAL",
        "location": "Nairobi",
        "duration": "3 months",
        "stipend_type": "Unpaid",
        "stipend_amount": 0,
        "positions": 1,
        "featured": 0,
        "status": "Published",
        "description": "<p>Support the Legal and Compliance team in contract review, regulatory compliance, and organizational governance matters.</p>",
        "responsibilities": "Review and draft contracts and MOUs\nConduct legal research and prepare briefing notes\nAssist in maintaining compliance registers\nSupport data protection and governance reviews\nAttend and minute legal meetings",
        "requirements": "Pursuing LLB or equivalent law degree\nStrong legal research and writing skills\nFamiliarity with NGO governance and Kenyan law\nHigh degree of confidentiality",
        "skills": "Legal Research\nContract Review\nCompliance\nReport Writing\nMS Word",
    },
    {
        "title": "Procurement & Supply Chain Intern",
        "department": "PROCUREMENT",
        "location": "Nairobi",
        "duration": "3 months",
        "stipend_type": "Paid",
        "stipend_amount": 10000,
        "positions": 2,
        "featured": 0,
        "status": "Published",
        "description": "<p>Gain practical experience in humanitarian procurement, logistics, and asset management supporting KRCS national operations.</p>",
        "responsibilities": "Process purchase requisitions and purchase orders\nConduct market surveys and vendor assessments\nMaintain procurement and asset registers\nSupport warehousing and distribution activities\nAssist in preparation of procurement reports",
        "requirements": "Pursuing BSc Procurement, Supply Chain, Business Administration, or related\nKnowledge of public procurement regulations\nNumerical and analytical skills",
        "skills": "Procurement\nInventory Management\nMS Excel\nLogistics\nVendor Management",
    },
    {
        "title": "Monitoring, Evaluation & Learning Intern",
        "department": "PROGRAM",
        "location": "Nairobi",
        "duration": "6 months",
        "stipend_type": "Paid",
        "stipend_amount": 15000,
        "positions": 2,
        "featured": 0,
        "status": "Draft",
        "description": "<p>Support the MEL team in designing data collection tools, conducting field surveys, and producing analytical reports for KRCS programs.</p>",
        "responsibilities": "Design and test data collection tools (ODK, KoboToolbox)\nConduct field data collection visits\nClean, analyse, and visualise program data\nPrepare monthly MEL progress reports\nSupport program evaluations and learning activities",
        "requirements": "Pursuing BSc Statistics, Social Sciences, IT, or related\nProficiency in Excel, SPSS, or R\nExperience with ODK or KoboToolbox a plus",
        "skills": "Data Analysis\nKoboToolbox\nODK\nExcel\nReport Writing\nSPSS",
    },
]


def seed_postings():
    for p in POSTINGS:
        # Check if a posting with this title already exists
        existing = frappe.db.get_value(
            "Internship Posting", {"title": p["title"]}, "name")
        if existing:
            print(f"  Skipped existing posting: {p['title']}")
            continue

        from frappe.utils import add_days, today as _today
        doc = frappe.new_doc("Internship Posting")
        doc.title = p["title"]
        doc.department = p["department"]
        doc.location = p["location"]
        doc.duration = p["duration"]
        doc.stipend_type = p["stipend_type"]
        doc.stipend_amount = p.get("stipend_amount", 0)
        doc.positions = p.get("positions", 1)
        doc.featured = p.get("featured", 0)
        doc.status = p.get("status", "Draft")
        doc.description = p.get("description", "")
        doc.responsibilities = p.get("responsibilities", "")
        doc.requirements = p.get("requirements", "")
        doc.skills = p.get("skills", "")
        doc.posted_date = _today()
        doc.deadline = add_days(_today(), 60)
        doc.applications_count = 0
        doc.insert(ignore_permissions=True)
        print(f"  Created posting: {p['title']} [{p['status']}]")


if __name__ == "__main__":
    run()