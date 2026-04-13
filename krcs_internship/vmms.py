# krcs_internship/vmms.py

import frappe

def check_vmms_membership(email):
    """
    Returns True if the user has an active VMMS Membership.
    Returns True (permissive) if VMMS is not installed.
    """
    if not frappe.db.table_exists("tabVMMS Membership"):
        return True  # VMMS not installed — don't block
    
    return bool(frappe.db.count(
        "VMMS Membership",
        {"user": email, "status": "Active"}
    ))

def get_vmms_member_data(email):
    """Returns member data from VMMS if available."""
    if not frappe.db.table_exists("tabVMMS Member"):
        return None
    return frappe.db.get_value(
        "VMMS Member",
        {"email": email},
        ["name", "membership_type", "membership_expiry"],
        as_dict=True,
    )