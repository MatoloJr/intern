import subprocess
import os
import frappe


def build_portal():
	portal_dir = os.path.join(
		os.path.dirname(__file__),
		"public", "js", "portal"
	)

	pkg_json = os.path.join(portal_dir, "package.json")
	vite_config = os.path.join(portal_dir, "vite.config.js")

	if not os.path.exists(pkg_json):
		frappe.log_error("portal package.json not found — skipping portal build", "Portal Build")
		return

	if not os.path.exists(vite_config):
		frappe.log_error("portal vite.config.js not found — skipping portal build", "Portal Build")
		return

	try:
		# Install dependencies first in case node_modules is missing
		subprocess.run(
			["npm", "ci", "--prefer-offline"],
			cwd=portal_dir,
			check=True,
			capture_output=True,
			text=True
		)
	except subprocess.CalledProcessError as e:
		frappe.log_error(
			f"npm ci failed:\n{e.stdout}\n{e.stderr}",
			"Portal Build - npm ci"
		)
		# Continue anyway — node_modules may already exist

	try:
		result = subprocess.run(
			["npm", "run", "build"],
			cwd=portal_dir,
			check=True,
			capture_output=True,
			text=True
		)
		print(result.stdout)

		# Verify the output does not contain bare ES module exports
		portal_js = os.path.join(portal_dir, "dist", "portal.js")
		if os.path.exists(portal_js):
			with open(portal_js, "r") as f:
				# Read just the last 2KB to check for export statements
				f.seek(0, 2)
				size = f.tell()
				f.seek(max(0, size - 2048))
				tail = f.read()
			if "\nexport " in tail or tail.strip().endswith("export{"):
				frappe.log_error(
					"portal.js contains ES module exports — IIFE build may have failed. "
					"Check vite.config.js output.format is 'iife' and inlineDynamicImports is true.",
					"Portal Build Warning"
				)
		else:
			frappe.log_error("portal.js not found after build", "Portal Build Warning")

	except subprocess.CalledProcessError as e:
		frappe.log_error(
			f"npm run build failed:\n{e.stdout}\n{e.stderr}",
			"Portal Build Failed"
		)