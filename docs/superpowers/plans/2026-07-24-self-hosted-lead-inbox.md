# Self-Hosted Lead Inbox Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a low-memory, self-hosted project-brief form, private lead inbox, and Gmail notifications to Monster CG.

**Architecture:** Nginx continues serving the static site and proxies only two paths to a Python 3 standard-library application on `127.0.0.1`. The application validates and stores submissions in a single SQLite database, sends a Gmail SMTP notification, and renders the private inbox. Nginx protects the inbox with `auth_basic`; secrets stay outside the repository.

**Tech Stack:** Static HTML/CSS/JavaScript, Python 3 standard library (`http.server`, `sqlite3`, `smtplib`), SQLite, systemd, Nginx, Cloudflare Turnstile.

---

### Task 1: Define submission validation in tests

**Files:**
- Create: `lead_service/test_app.py`
- Create: `lead_service/app.py`

- [ ] **Step 1: Write the failing tests**

```python
class LeadValidationTests(unittest.TestCase):
    def test_valid_lead_is_normalized(self):
        lead = validate_lead({"email": "  studio@example.com ", "service": "rendering", "brief": "Need two interior images."})
        self.assertEqual(lead["email"], "studio@example.com")

    def test_missing_required_fields_are_rejected(self):
        with self.assertRaises(ValidationError):
            validate_lead({"email": "", "service": "", "brief": ""})

    def test_honeypot_and_oversized_brief_are_rejected(self):
        with self.assertRaises(ValidationError):
            validate_lead({"email": "a@b.com", "service": "rendering", "brief": "x", "company_website": "bot"})
```

- [ ] **Step 2: Run the tests to verify failure**

Run: `py -3 -m unittest lead_service.test_app -v`

Expected: import failure because `lead_service.app` does not exist.

- [ ] **Step 3: Implement validation**

Create `lead_service/app.py` with `ValidationError`, `SERVICE_OPTIONS = {"rendering", "cad", "both"}`, and `validate_lead(payload)`. Reject non-object JSON, invalid email syntax, service values outside the set, missing brief, a non-empty `company_website` honeypot, and any field over its explicit limit (email 254, name/company 120, WhatsApp 40, target date 40, file URL 500, brief 5000). Return a trimmed dictionary containing only approved keys.

- [ ] **Step 4: Run the tests to verify success**

Run: `py -3 -m unittest lead_service.test_app -v`

Expected: all validation tests pass.

- [ ] **Step 5: Commit**

```bash
git add lead_service/app.py lead_service/test_app.py
git commit -m "feat: validate project brief submissions"
```

### Task 2: Persist leads and render the protected inbox

**Files:**
- Modify: `lead_service/app.py`
- Modify: `lead_service/test_app.py`

- [ ] **Step 1: Write the failing storage tests**

```python
class LeadStoreTests(unittest.TestCase):
    def test_store_assigns_identifier_and_lists_newest_first(self):
        store = LeadStore(":memory:")
        first = store.insert(valid_payload("first@example.com"))
        second = store.insert(valid_payload("second@example.com"))
        self.assertLess(first["id"], second["id"])
        self.assertEqual(store.list_leads()[0]["email"], "second@example.com")
```

- [ ] **Step 2: Run the storage test to verify failure**

Run: `py -3 -m unittest lead_service.test_app.LeadStoreTests -v`

Expected: failure because `LeadStore` is undefined.

- [ ] **Step 3: Implement SQLite storage and inbox HTML**

Add `LeadStore` using `sqlite3` with a `leads` table containing id, created_at, email, service, brief, contact_name, company, whatsapp, target_date, file_url, and source_ip. Use parameterized SQL only. Add `GET /admin/leads` to the HTTP handler; it renders escaped table cells, newest submissions first, and `Cache-Control: no-store`. Nginx, not the application, supplies the password protection.

- [ ] **Step 4: Run the storage test to verify success**

Run: `py -3 -m unittest lead_service.test_app.LeadStoreTests -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add lead_service/app.py lead_service/test_app.py
git commit -m "feat: store and display project leads"
```

### Task 3: Add the bounded public API and Gmail notification

**Files:**
- Modify: `lead_service/app.py`
- Modify: `lead_service/test_app.py`
- Create: `deploy/monster-cg-leads.env.example`

- [ ] **Step 1: Write failing HTTP and rate-limit tests**

```python
class LeadApiTests(unittest.TestCase):
    def test_post_lead_returns_201_and_stores_submission(self):
        status, body = post_json(self.server, "/api/leads", valid_payload())
        self.assertEqual(status, 201)
        self.assertEqual(body["ok"], True)

    def test_sixth_submission_from_same_ip_returns_429(self):
        for _ in range(5): post_json(self.server, "/api/leads", valid_payload())
        status, _ = post_json(self.server, "/api/leads", valid_payload())
        self.assertEqual(status, 429)
```

- [ ] **Step 2: Run the API tests to verify failure**

Run: `py -3 -m unittest lead_service.test_app.LeadApiTests -v`

Expected: failure because no handler accepts `/api/leads`.

- [ ] **Step 3: Implement the HTTP boundary**

Implement `POST /api/leads` with `Content-Type: application/json`, a 16 KiB request-size limit, JSON parsing, validation, SQLite insertion, and JSON responses. Keep at most five requests per source IP in a rolling 15-minute in-memory window. Return `201 {"ok": true}` for success, `400` for invalid input, `413` for a large body, `415` for an invalid content type, `429` when rate-limited, and `404` for other paths. Set `Cache-Control: no-store` and `X-Content-Type-Options: nosniff` on every API response.

Read Gmail SMTP values from environment variables `LEADS_SMTP_HOST`, `LEADS_SMTP_PORT`, `LEADS_SMTP_USER`, `LEADS_SMTP_PASSWORD`, and `LEADS_NOTIFY_TO`. Send a plain-text notification after insertion. If SMTP fails, retain the submission, log the failure without printing secrets, and return success to the visitor.

Create the environment example with variable names only and no real values.

- [ ] **Step 4: Run API tests to verify success**

Run: `py -3 -m unittest lead_service.test_app -v`

Expected: PASS, including 429 behavior.

- [ ] **Step 5: Commit**

```bash
git add lead_service/app.py lead_service/test_app.py deploy/monster-cg-leads.env.example
git commit -m "feat: add bounded lead API and email notifications"
```

### Task 4: Build the visitor-facing project brief form

**Files:**
- Modify: `index.html`
- Modify: `contact/index.html`
- Modify: `styles.css`
- Modify: `site.css`
- Modify: `script.js`
- Modify: `tests/test_site.py`

- [ ] **Step 1: Write failing static-page tests**

```python
def test_project_brief_form_has_privacy_and_no_javascript_fallback(self):
    self.assertIn('id="projectBriefForm"', INDEX)
    self.assertIn('We do not sell your information.', INDEX)
    self.assertIn('href="/privacy-policy/"', INDEX)
    self.assertIn('mailto:zhangzheng270@gmail.com', INDEX)
```

- [ ] **Step 2: Run the targeted test to verify failure**

Run: `py -3 -m unittest tests.test_site.SitePositioningTests.test_project_brief_form_has_privacy_and_no_javascript_fallback -v`

Expected: FAIL because the form does not exist.

- [ ] **Step 3: Implement the form and dialog behavior**

Add a non-automatic `<dialog>` project-brief form to the homepage and a full form to `/contact/`. Use required `email`, `service`, and `brief` fields plus optional name, company, WhatsApp, target date, and file URL fields. Include a visually hidden `company_website` honeypot, the exact approved privacy sentence, and a link to `/privacy-policy/`. Add a `<noscript>` email/WhatsApp fallback.

In `script.js`, open the dialog only from `data-open-project-brief`, submit JSON to `/api/leads`, disable the submit button while pending, show a success state after HTTP 201, show a failure message with email/WhatsApp links for other failures, and close on Escape. Add `data-track="lead-form-open"` and `data-track="lead-form-submit"` without loading an analytics library.

- [ ] **Step 4: Run static tests and JavaScript syntax validation**

Run: `py -3 -m unittest discover -s tests -p "test_*.py" -v` and `node --check script.js`

Expected: all tests pass and Node exits 0.

- [ ] **Step 5: Commit**

```bash
git add index.html contact/index.html styles.css site.css script.js tests/test_site.py
git commit -m "feat: add project brief form interface"
```

### Task 5: Add low-resource VPS deployment controls

**Files:**
- Create: `deploy/monster-cg-leads.service`
- Create: `deploy/monster-cg-leads.nginx.conf`
- Create: `deploy/backup-leads.sh`
- Create: `deploy/monster-cg-leads-backup.service`
- Create: `deploy/monster-cg-leads-backup.timer`
- Modify: `README.md`

- [ ] **Step 1: Write deployment artifact tests**

```python
def test_lead_service_deployment_binds_only_to_localhost(self):
    unit = (ROOT / "deploy/monster-cg-leads.service").read_text()
    self.assertIn("MemoryMax=160M", unit)
    self.assertIn("LEADS_BIND=127.0.0.1", unit)
```

- [ ] **Step 2: Run the test to verify failure**

Run: `py -3 -m unittest tests.test_release_readiness -v`

Expected: FAIL because the deployment artifacts do not exist.

- [ ] **Step 3: Create deployment artifacts**

Create a systemd unit that runs the application as `www-data`, reads `/etc/monster-cg/leads.env`, restarts on failure, uses `MemoryMax=160M`, `CPUQuota=20%`, `NoNewPrivileges=true`, and binds only to `127.0.0.1:8091`. Create an Nginx include that proxies `/api/leads` and `/admin/leads` to that address, applies `client_max_body_size 16k`, disables proxy buffering, and uses `auth_basic` plus `/etc/monster-cg/admin.htpasswd` for `/admin/leads`.

Create a daily backup script that copies the SQLite database to `/var/backups/monster-cg-leads/` with a UTC timestamp and removes backups older than 14 days. Create a systemd timer that runs it daily. Document exact VPS setup commands, Gmail app-password setup, Turnstile key placement, service restart, health check, backup restore, and rollback in README.

- [ ] **Step 4: Run deployment artifact and full test suite**

Run: `py -3 -m unittest discover -s tests -p "test_*.py" -v` and `git diff --check`

Expected: all tests pass and no whitespace errors are reported.

- [ ] **Step 5: Commit**

```bash
git add deploy README.md tests/test_release_readiness.py
git commit -m "ops: deploy low-resource lead inbox service"
```

### Task 6: Deploy and verify with the owner

**Files:**
- No repository changes required.

- [ ] **Step 1: Create secrets on the VPS**

Create `/etc/monster-cg/leads.env` with the Gmail app password and Cloudflare Turnstile secret, then set owner `root:root` and mode `600`. Create `/etc/monster-cg/admin.htpasswd` using `htpasswd` and set mode `640` with group `www-data`.

- [ ] **Step 2: Install and start the service**

Copy the service, Nginx include, and backup timer to their `/etc` locations; run `systemctl daemon-reload`, enable the lead service and backup timer, test Nginx, and reload it.

- [ ] **Step 3: Perform a real submission test**

Use a test work email and submit the live form once. Verify that `/admin/leads` shows the lead and that the owner Gmail inbox receives the notification.

- [ ] **Step 4: Verify operational safety**

Run `systemctl status monster-cg-leads`, `journalctl -u monster-cg-leads -n 50`, `systemctl list-timers monster-cg-leads-backup.timer`, and inspect the backup directory. Confirm the process memory is below 160 MiB and the service listens only on `127.0.0.1:8091`.
