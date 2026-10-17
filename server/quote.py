"""Loopback-only inquiry API. Python 3.10+, standard library only."""
import hashlib
import json
import os
import re
import smtplib
import sqlite3
import ssl
import time
from datetime import date
from email.message import EmailMessage
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

RECIPIENT = 'zhangzheng270@gmail.com'  # Verified in the original site.
SERVICES = {'Interior Rendering', 'Exterior Rendering', 'Interior & Exterior Rendering', 'CAD Support'}
MAX_BODY = 16384


def configured():
    return all(os.environ.get(k) for k in ('SMTP_HOST', 'SMTP_USER', 'SMTP_PASSWORD', 'SMTP_FROM', 'QUOTE_RATE_SECRET'))


def validate(data):
    if not isinstance(data, dict):
        raise ValueError('Please check the form fields.')
    limits = {'company': (1, 160), 'email': (3, 254), 'service': (1, 80),
              'quantity': (1, 4), 'deadline': (0, 10), 'message': (20, 5000), 'website': (0, 200)}
    clean = {}
    for key, (low, high) in limits.items():
        value = data.get(key, '')
        if not isinstance(value, str) or not low <= len(value.strip()) <= high or '\x00' in value:
            raise ValueError('Please check the form fields and project description length.')
        clean[key] = value.strip()
    if clean['website']:
        raise ValueError('This request could not be accepted. Please contact us by email.')
    if not re.fullmatch(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?\.[A-Za-z]{2,63}", clean['email']):
        raise ValueError('Enter a valid business email address.')
    if clean['service'] not in SERVICES:
        raise ValueError('Choose a service from the list.')
    if not re.fullmatch(r'[1-9][0-9]{0,3}', clean['quantity']) or int(clean['quantity']) > 1000:
        raise ValueError('Enter a quantity between 1 and 1000.')
    if clean['deadline']:
        try:
            if date.fromisoformat(clean['deadline']) < date.today():
                raise ValueError()
        except ValueError:
            raise ValueError('Choose today or a future target date, or leave the date blank.') from None
    source = data.get('source', '/contact/')
    clean['source'] = source if isinstance(source, str) and re.fullmatch(r'/[a-zA-Z0-9/_-]{0,200}', source) else '/contact/'
    return clean


def allow_request(ip, now=None):
    """Persistent per-IP (5/hour) and global (100/hour) caps; no raw IP storage."""
    now = time.time() if now is None else now
    path = os.environ.get('QUOTE_RATE_DB', '/var/lib/monster-quote/rate.sqlite3')
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    key = hashlib.sha256((os.environ['QUOTE_RATE_SECRET'] + ip).encode()).hexdigest()
    with sqlite3.connect(path, timeout=5) as db:
        db.execute('CREATE TABLE IF NOT EXISTS requests (client TEXT, stamp REAL)')
        db.execute('BEGIN IMMEDIATE')
        db.execute('DELETE FROM requests WHERE stamp < ?', (now - 3600,))
        total = db.execute('SELECT count(*) FROM requests').fetchone()[0]
        count = db.execute('SELECT count(*) FROM requests WHERE client = ?', (key,)).fetchone()[0]
        if count >= 5 or total >= 100:
            return False
        db.execute('INSERT INTO requests VALUES (?, ?)', (key, now))
    return True


def send_mail(data):
    mail = EmailMessage()
    mail['From'] = os.environ['SMTP_FROM']
    mail['To'] = RECIPIENT
    mail['Reply-To'] = data['email']
    mail['Subject'] = 'Monster CG website inquiry — ' + data['service']
    mail.set_content('\n\n'.join(f'{label}: {data[key] or "Not specified"}' for key, label in (
        ('company', 'Company'), ('email', 'Business email'), ('service', 'Service'),
        ('quantity', 'Estimated image / CAD drawing quantity'), ('deadline', 'Target date'),
        ('source', 'Source page'), ('message', 'Project description'))))
    port = int(os.environ.get('SMTP_PORT', '587'))
    context = ssl.create_default_context()
    if port == 465:
        client = smtplib.SMTP_SSL(os.environ['SMTP_HOST'], port, timeout=20, context=context)
    else:
        client = smtplib.SMTP(os.environ['SMTP_HOST'], port, timeout=20)
    with client:
        if port != 465:
            client.starttls(context=context)
        client.login(os.environ['SMTP_USER'], os.environ['SMTP_PASSWORD'])
        if client.send_message(mail):
            raise smtplib.SMTPException('Recipient not accepted')


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass  # Do not log personal data, raw requests or credentials.

    def respond(self, status, message, **extra):
        raw = json.dumps({'message': message, **extra}).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Content-Length', str(len(raw)))
        if status == 429:
            self.send_header('Retry-After', '3600')
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        if self.path != '/api/quote/status':
            return self.respond(404, 'Not found')
        return self.respond(200, 'Availability', available=configured())

    def do_POST(self):
        if self.path != '/api/quote':
            return self.respond(404, 'Not found')
        origins = os.environ.get('QUOTE_ORIGINS', 'https://monster-cg.com,https://www.monster-cg.com').split(',')
        if self.headers.get('Origin') not in origins:
            return self.respond(403, 'Please submit from the Monster CG website.')
        if self.headers.get('Content-Type', '').split(';')[0] != 'application/json':
            return self.respond(415, 'JSON required')
        try:
            size = int(self.headers.get('Content-Length', '0'))
        except ValueError:
            size = 0
        if not 0 < size <= MAX_BODY:
            return self.respond(413, 'Request is too large or empty.')
        if not configured():
            return self.respond(503, 'The form is temporarily unavailable. Please use email or WhatsApp.')
        try:
            # Only trust the single IP header overwritten by the loopback Nginx proxy.
            ip = self.headers.get('X-Real-IP', self.client_address[0])
            if not allow_request(ip):
                return self.respond(429, 'Too many attempts. Please try again in one hour or use email.')
            self.connection.settimeout(10)
            data = validate(json.loads(self.rfile.read(size)))
        except (ValueError, UnicodeError):
            return self.respond(400, 'Please check your email, quantity, date and project description (20–5000 characters).')
        except Exception:
            return self.respond(503, 'The form is temporarily unavailable. Please use email.')
        try:
            send_mail(data)
        except Exception:
            return self.respond(502, 'We could not confirm sending. Please contact us by email to avoid duplicate requests.')
        return self.respond(200, 'Your inquiry has been sent to Monster CG.', success=True)


if __name__ == '__main__':
    ThreadingHTTPServer(('127.0.0.1', int(os.environ.get('PORT', '8765'))), Handler).serve_forever()
