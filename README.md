# KRCS Internship Platform

Full-stack internship management platform built on Frappe Framework with ERPNext and a custom Vue portal.

This document is an end-to-end runbook for getting the platform running in development and production.

## 1. Platform Overview

### Stack

- Backend: Frappe Framework (v17 dev), Python 3.10+
- Business app: ERPNext (develop branch)
- Custom app: krcs_internship
- Database: MariaDB
- Queue + cache: Redis
- Realtime: Socket.IO + Redis
- Frontend portal: Vue 3 + Vite (bundled into Frappe assets)

### Workspace Snapshot

- Bench root: `internship/`
- Active apps in this bench: `frappe`, `erpnext`, `krcs_internship`
- Site: `intern.localhost`
- Current dev web port in this bench: `8006`
- Portal URL: `/portal`

### Important App Behaviors

- The app exposes public and admin APIs in `apps/krcs_internship/api.py`
- Vue portal is built from:
	- `apps/krcs_internship/krcs_internship/public/js/portal`
- Portal production assets are served from:
	- `/assets/krcs_internship/js/portal/dist/`
- After every migrate, hook `after_migrate = ["krcs_internship.install.build_portal"]` runs `npm run build` for the portal.

## 2. Prerequisites

Install these on your server/workstation:

- Python 3.10 or newer
- Node.js 18+ (LTS recommended)
- npm 9+
- Redis server
- MariaDB server/client
- wkhtmltopdf (for PDF printing in Frappe/ERPNext)
- git

For Ubuntu/Debian, also ensure build essentials and headers are available:

- `build-essential`
- `python3-dev`
- `libmariadb-dev`
- `redis-tools`

## 3. Development Setup

Choose one of the two paths below.

### A) Use Existing Bench (this repository layout)

From bench root:

```bash
cd /home/matolo/frappe/internship
source env/bin/activate
```

Install/update Python + Node dependencies:

```bash
pip install -U pip
bench setup requirements
cd apps/krcs_internship/krcs_internship/public/js/portal && npm ci
cd /home/matolo/frappe/internship
```

Run migrations (this also builds the Vue portal via hook):

```bash
bench --site intern.localhost migrate
```

Start development services:

```bash
bench start
```

Open:

- Desk: `http://intern.localhost:8006/app`
- Portal: `http://intern.localhost:8006/portal`

### B) Fresh Bench Bootstrap

If building from scratch on a clean machine:

```bash
# Install bench first if needed
pip install frappe-bench

# Create bench
bench init internship --frappe-branch develop
cd internship

# Get apps
bench get-app erpnext --branch develop
bench get-app https://<your-git-host>/<org>/krcs_internship.git --branch main

# Create site
bench new-site intern.localhost

# Install apps
bench --site intern.localhost install-app erpnext
bench --site intern.localhost install-app krcs_internship

# Optional for local debugging
bench --site intern.localhost set-config developer_mode 1

# Migrate + build assets
bench --site intern.localhost migrate
bench build
bench start
```

## 4. Developer Workflow

### Daily Commands

```bash
source env/bin/activate
bench start
```

When schema/model changes are made:

```bash
bench --site intern.localhost migrate
```

When JS/CSS changes are made:

```bash
bench build --app krcs_internship
```

### Portal Frontend (Vue + Vite)

Run standalone frontend dev server for faster UI iteration:

```bash
cd apps/krcs_internship/krcs_internship/public/js/portal
npm ci
npm run dev
```

Notes:

- Vite proxy targets `http://intern.localhost:8006` for `/api`, `/assets`, and `/files`.
- For production-like output test:
	- `npm run build`
	- Verify generated files under `dist/`.

### Linting and Formatting

Enable pre-commit hooks:

```bash
cd apps/krcs_internship
pre-commit install
pre-commit run -a
```

### Tests

Run app tests:

```bash
cd /home/matolo/frappe/internship
bench --site intern.localhost run-tests --app krcs_internship
```

## 5. API Surface (Custom App)

Base format:

- `POST /api/method/krcs_internship.api.<method_name>`

Public methods (guest allowed in code):

- `get_postings`
- `get_posting`
- `get_departments`
- `submit_application`
- `get_application_status`
- `get_messages`
- `mark_message_read`

Admin/auth-required methods:

- `create_posting`
- `update_posting`
- `delete_posting`
- `admin_get_applications`
- `update_application_status`
- `admin_send_message`
- `get_dashboard_stats`
- `get_applications_by_department`
- `get_applications_by_university`

## 6. Data Model Highlights

Primary DocTypes used by the internship domain:

- Internship Posting
- Intern Application
- Application Timeline
- Intern Message
- Departments
- Universities
- Courses
- Intern
- Intern Activities
- Intern Project
- Supervisor
- Project
- Asset Inventory / Asset Tracker / Assets Access / Virtual Systems

If this is a new environment, create baseline records first (Departments, Universities, Courses) before accepting applications.

## 7. Production Deployment

This section assumes Linux and a single bench host running Frappe, workers, Redis, and Nginx.

### 7.1 Pre-Production Checklist

- Domain DNS points to server
- Firewall allows 80/443
- MariaDB and Redis are healthy
- `developer_mode` is disabled in production site config
- Strong site/database credentials are in place
- Backups are configured and tested

### 7.2 Production Configuration

Set production-safe values:

```bash
cd /home/<user>/<bench>
source env/bin/activate

bench --site <site-name> set-config developer_mode 0
bench --site <site-name> set-maintenance-mode off
```

Tune bench-level workers/ports in `sites/common_site_config.json` as needed:

- `gunicorn_workers`
- `background_workers`
- `webserver_port`
- `socketio_port`

### 7.3 Build and Migrate for Release

```bash
bench --site <site-name> migrate
bench build --app krcs_internship --app frappe --app erpnext
```

### 7.4 Configure Process Supervision + Nginx

Use Bench-managed production setup:

```bash
sudo bench setup production <linux-user>
```

Or manually (if your org has custom provisioning):

```bash
bench setup supervisor
bench setup nginx
sudo supervisorctl reread
sudo supervisorctl update
sudo systemctl reload nginx
```

### 7.5 SSL

```bash
sudo bench setup lets-encrypt <site-name>
```

### 7.6 Restart and Validate

```bash
bench restart
bench --site <site-name> clear-cache
```

Validate:

- Desk login works
- `/portal` loads CSS/JS from assets
- API calls from portal succeed
- Worker queues process jobs
- Scheduler is active

## 8. Release/Update Procedure

For each deployment:

```bash
cd /home/<user>/<bench>
source env/bin/activate

git pull
bench update --requirements
bench --site <site-name> migrate
bench build --app krcs_internship --app frappe --app erpnext
bench restart
```

If you update app repos independently, ensure the app branches are aligned (for example, Frappe/ERPNext develop with compatible custom-app code).

## 9. Backup and Recovery

Create on-demand backup:

```bash
bench --site <site-name> backup --with-files
```

Recommended:

- Daily database + files backup
- Off-host backup copy (object storage or secondary server)
- Periodic restore drill on a staging environment

## 10. Troubleshooting

### Portal page loads but assets are missing

- Rebuild portal:
	- `cd apps/krcs_internship/krcs_internship/public/js/portal && npm ci && npm run build`
- Rebuild bench assets:
	- `bench build --app krcs_internship`
- Clear cache:
	- `bench --site <site-name> clear-cache`

### Migrate fails on portal build hook

- Ensure Node/npm are installed and available to the bench runtime user.
- Ensure `package.json` exists in portal directory.

### Background jobs not processing

- Check worker processes (Supervisor/systemd)
- Verify `redis_queue` in `sites/common_site_config.json`
- Inspect logs in `logs/`

### Realtime/socket issues

- Verify `socketio` process is up
- Check `redis_socketio` and `socketio_port`

## 11. Security and Secrets

- Do not commit real secrets from `site_config.json` or environment files.
- Keep production credentials outside git-tracked files.
- Restrict DB/Redis to localhost or private networks.
- Rotate credentials periodically.

## 12. Contributing

```bash
cd apps/krcs_internship
pre-commit install
pre-commit run -a
```

Before opening a PR:

1. Run tests for `krcs_internship`.
2. Run lint/format hooks.
3. Verify `/portal` and key API flows.

## License

MIT
