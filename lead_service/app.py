"""Low-resource HTTP service for Monster CG project brief submissions."""

from __future__ import annotations

import html
import json
import os
import re
import smtplib
import sqlite3
import ssl
import threading
import time
from collections import defaultdict, deque
from datetime import UTC, datetime
from email.message import EmailMessage
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

SERVICE_OPTIONS = {"rendering", "cad", "both"}
FIELD_LIMITS = {
    "email": 254,
    "service": 20,
    "brief": 5000,
    "contact_name": 120,
    "company": 120,
    "whatsapp": 40,
    "target_date": 40,
    "file_url": 500,
    "company_website": 200,
}
EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
MAX_BODY_BYTES = 16 * 1024
RATE_LIMIT_COUNT = 5
RATE_LIMIT_WINDOW_SECONDS = 15 * 60


class ValidationError(ValueError):
    """Raised when a public lead submission is invalid."""


def validate_lead(payload: object) -> dict[str, str]:
    if not isinstance(payload, dict):
        raise ValidationError("Invalid submission.")
    cleaned: dict[str, str] = {}
    for field, limit in FIELD_LIMITS.items():
        value = payload.get(field, "")
        if not isinstance(value, str):
            raise ValidationError("Invalid submission.")
        value = value.strip()
        if len(value) > limit:
            raise ValidationError("One or more fields are too long.")
        cleaned[field] = value

    if cleaned["company_website"]:
        raise ValidationError("Invalid submission.")
    if not EMAIL_PATTERN.fullmatch(cleaned["email"]):
        raise ValidationError("Enter a valid work email.")
    if cleaned["service"] not in SERVICE_OPTIONS:
        raise ValidationError("Choose a service.")
    if not cleaned["brief"]:
        raise ValidationError("Tell us briefly about the project.")
    if cleaned["file_url"] and not cleaned["file_url"].startswith(("https://", "http://")):
        raise ValidationError("File link must start with https:// or http://.")
    return cleaned


class LeadStore:
    def __init__(self, database_path: str):
        self.database_path = database_path
        self._lock = threading.Lock()
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS leads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    email TEXT NOT NULL,
                    service TEXT NOT NULL,
                    brief TEXT NOT NULL,
                    contact_name TEXT NOT NULL DEFAULT '',
                    company TEXT NOT NULL DEFAULT '',
                    whatsapp TEXT NOT NULL DEFAULT '',
                    target_date TEXT NOT NULL DEFAULT '',
                    file_url TEXT NOT NULL DEFAULT '',
                    source_ip TEXT NOT NULL
                )
                """
            )

    def insert(self, lead: dict[str, str], source_ip: str) -> dict[str, object]:
        created_at = datetime.now(UTC).replace(microsecond=0).isoformat()
        fields = ("email", "service", "brief", "contact_name", "company", "whatsapp", "target_date", "file_url")
        values = [lead.get(field, "") for field in fields]
        with self._lock, self._connect() as connection:
            cursor = connection.execute(
                """INSERT INTO leads (created_at, email, service, brief, contact_name, company, whatsapp, target_date, file_url, source_ip)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                [created_at, *values, source_ip],
            )
            lead_id = cursor.lastrowid
        return {"id": lead_id, "created_at": created_at, **{field: lead.get(field, "") for field in fields}, "source_ip": source_ip}

    def list_leads(self, limit: int = 200) -> list[dict[str, object]]:
        with self._connect() as connection:
            rows = connection.execute(
                """SELECT id, created_at, email, service, brief, contact_name, company, whatsapp, target_date, file_url
                FROM leads ORDER BY id DESC LIMIT ?""",
                (max(1, min(limit, 500)),),
            ).fetchall()
        return [dict(row) for row in rows]


class RateLimiter:
    def __init__(self) -> None:
        self.requests: dict[str, deque[float]] = defaultdict(deque)
        self.lock = threading.Lock()

    def allow(self, source_ip: str) -> bool:
        now = time.monotonic()
        with self.lock:
            records = self.requests[source_ip]
            while records and now - records[0] >= RATE_LIMIT_WINDOW_SECONDS:
                records.popleft()
            if len(records) >= RATE_LIMIT_COUNT:
                return False
            records.append(now)
            return True


def send_notification(lead: dict[str, object]) -> None:
    host = os.environ.get("LEADS_SMTP_HOST", "").strip()
    user = os.environ.get("LEADS_SMTP_USER", "").strip()
    password = os.environ.get("LEADS_SMTP_PASSWORD", "")
    recipient = os.environ.get("LEADS_NOTIFY_TO", "").strip()
    if not all((host, user, password, recipient)):
        return
    message = EmailMessage()
    message["Subject"] = f"New Monster CG project brief #{lead['id']}"
    message["From"] = user
    message["To"] = recipient
    message.set_content(
        "\n".join(
            [
                f"Lead #{lead['id']} received {lead['created_at']}",
                f"Email: {lead['email']}",
                f"Service: {lead['service']}",
                f"Name: {lead['contact_name']}",
                f"Company: {lead['company']}",
                f"WhatsApp: {lead['whatsapp']}",
                f"Target date: {lead['target_date']}",
                f"File link: {lead['file_url']}",
                "",
                "Project brief:",
                str(lead["brief"]),
            ]
        )
    )
    port = int(os.environ.get("LEADS_SMTP_PORT", "465"))
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(host, port, context=context, timeout=15) as smtp:
        smtp.login(user, password)
        smtp.send_message(message)


def render_inbox(leads: list[dict[str, object]]) -> str:
    rows = []
    for lead in leads:
        cells = [lead["created_at"], lead["email"], lead["service"], lead["contact_name"], lead["company"], lead["whatsapp"], lead["target_date"], lead["file_url"], lead["brief"]]
        rows.append("<tr>" + "".join(f"<td>{html.escape(str(cell)).replace(chr(10), '<br>')}</td>" for cell in cells) + "</tr>")
    body = "".join(rows) or "<tr><td colspan='9'>No project briefs have been received yet.</td></tr>"
    return f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='robots' content='noindex, nofollow'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Monster CG Leads</title><style>body{{margin:0;background:#f3f1ec;color:#17191a;font:14px/1.5 Arial,sans-serif}}main{{max-width:1500px;margin:auto;padding:32px}}h1{{font:36px Georgia,serif}}table{{width:100%;border-collapse:collapse;background:#fff}}th,td{{padding:12px;vertical-align:top;text-align:left;border:1px solid #ddd;word-break:break-word}}th{{background:#17191a;color:#fff}}td:last-child{{min-width:260px}}</style></head><body><main><h1>Project briefs</h1><p>Newest submissions first. This page is private.</p><table><thead><tr><th>Received (UTC)</th><th>Email</th><th>Service</th><th>Name</th><th>Company</th><th>WhatsApp</th><th>Target</th><th>File link</th><th>Brief</th></tr></thead><tbody>{body}</tbody></table></main></body></html>"""


class LeadRequestHandler(BaseHTTPRequestHandler):
    store: LeadStore
    limiter: RateLimiter

    def _send_json(self, status: HTTPStatus, payload: dict[str, object]) -> None:
        encoded = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/health":
            self._send_json(HTTPStatus.OK, {"ok": True})
            return
        if path != "/admin/leads":
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "Not found."})
            return
        encoded = render_inbox(self.store.list_leads()).encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(encoded)

    def do_POST(self) -> None:  # noqa: N802
        if urlparse(self.path).path != "/api/leads":
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "Not found."})
            return
        if self.headers.get_content_type() != "application/json":
            self._send_json(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, {"error": "Use application/json."})
            return
        content_length = self.headers.get("Content-Length")
        if not content_length or not content_length.isdigit():
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Invalid request."})
            return
        if int(content_length) > MAX_BODY_BYTES:
            self._send_json(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, {"error": "Submission is too large."})
            return
        source_ip = self.client_address[0]
        if not self.limiter.allow(source_ip):
            self._send_json(HTTPStatus.TOO_MANY_REQUESTS, {"error": "Please wait before trying again."})
            return
        try:
            payload = json.loads(self.rfile.read(int(content_length)).decode("utf-8"))
            lead = self.store.insert(validate_lead(payload), source_ip)
        except (UnicodeDecodeError, json.JSONDecodeError, ValidationError) as error:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(error) or "Invalid submission."})
            return
        try:
            send_notification(lead)
        except Exception:
            self.log_error("Lead %s stored but email notification failed", lead["id"])
        self._send_json(HTTPStatus.CREATED, {"ok": True})

    def log_message(self, format: str, *args: object) -> None:
        return


def make_server(bind: str, port: int, database_path: str) -> ThreadingHTTPServer:
    LeadRequestHandler.store = LeadStore(database_path)
    LeadRequestHandler.limiter = RateLimiter()
    return ThreadingHTTPServer((bind, port), LeadRequestHandler)


def main() -> None:
    bind = os.environ.get("LEADS_BIND", "127.0.0.1")
    port = int(os.environ.get("LEADS_PORT", "8091"))
    database_path = os.environ.get("LEADS_DATABASE", str(Path("/var/lib/monster-cg/leads.sqlite3")))
    Path(database_path).parent.mkdir(parents=True, exist_ok=True)
    server = make_server(bind, port, database_path)
    server.serve_forever()


if __name__ == "__main__":
    main()
