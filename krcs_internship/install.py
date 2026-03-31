import subprocess
import os


def build_portal():
    import frappe

    portal_dir = os.path.join(
        os.path.dirname(__file__),
        "public", "js", "portal"
    )
    if not os.path.exists(os.path.join(portal_dir, "package.json")):
        return
    try:
        subprocess.run(
            ["npm", "run", "build"],
            cwd=portal_dir,
            check=True
        )
        frappe.msgprint("Portal built successfully.")
    except subprocess.CalledProcessError as e:
        frappe.log_error(str(e), "Portal Build Failed")