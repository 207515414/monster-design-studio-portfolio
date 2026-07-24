# Monster CG Lead Form Design

## Goal

Capture qualified project briefs without compromising the editorial, portfolio-led tone of the Monster CG homepage.

## Chosen approach

Use a self-hosted, low-resource lead service on the existing VPS. Nginx continues to serve the static website and reverse-proxies only `/api/leads` and `/admin/leads` to a local lightweight application. The application uses SQLite for lead storage and sends new-lead notifications to `zhangzheng270@gmail.com` through Gmail SMTP with a Gmail app password.

## Visitor experience

- The homepage keeps its existing `Send a Project Brief` call to action.
- A compact, dismissible project-brief form opens only after a visitor requests it; there is no automatic popup.
- Required fields: work email, required service, project brief.
- Optional fields: contact name, company, target date, WhatsApp, and file link. The initial version does not accept direct file uploads.
- Successful submission shows a clear on-page confirmation and offers WhatsApp as an alternative contact channel.

## Data and privacy

- The Monster CG VPS receives the submitted data, saves it locally, and sends a notification to the owner Gmail address.
- The form includes this statement with a link to the existing privacy policy: “We use your details only to respond to your inquiry and manage your project. We do not sell your information. See our Privacy Policy.”
- No claim that data is never processed by a third-party provider will be made.

## Technical boundaries

- The application uses Python 3 standard-library HTTP, SMTP, and SQLite capabilities only; no Docker, database server, or large framework is introduced.
- It is run by `systemd` as a dedicated non-root service and listens only on `127.0.0.1`.
- `/admin/leads` is protected by an owner-set password hash, and API responses use `Cache-Control: no-store`.
- Add a honeypot, request-size cap, rate limit, and Cloudflare Turnstile before public release.
- Gmail SMTP credentials, the admin password hash, and the Turnstile secret are stored only in a VPS environment file outside the Git repository.
- A daily SQLite backup runs on the VPS and retains a bounded number of copies.
- Preserve a no-JavaScript fallback to email and WhatsApp.
- Track form-open and successful-submit events through the existing `data-track` convention; do not transmit analytics until an analytics property is configured.

## Verification

- Validate required fields and keyboard-close behavior for the dialog.
- Submit a test lead to verify both the private admin inbox and Gmail notification.
- Confirm the API rejects malformed, oversized, and rate-limited requests.
- Re-run static link and page tests before release.
