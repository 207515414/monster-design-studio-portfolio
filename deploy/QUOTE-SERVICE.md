# Quote service handoff (self-hosted Nginx)

No production installation has been performed. The website remains static; only `/api/quote` and `/api/quote/status` are proxied to a loopback Python service. Python 3.10+ is sufficient; there are no pip dependencies or new paid services.

1. Keep the existing server configuration and a recoverable copy of the current site. Copy **only public website files** into the document root. Never publish `.git`, `.agents`, `server`, `tests`, `docs`, deployment files, environment files or rate databases.
2. Install `server/quote.py` outside the web root, for example `/opt/monster-quote/quote.py`. Use an unprivileged service account; create `/var/lib/monster-quote` writable by that account only.
3. Create `/etc/monster-quote.env` (mode 0600) from `server/.env.example`. Supply your existing SMTP host, user, password and provider-approved From address. Use TLS port 587 or implicit TLS port 465. Generate a random `QUOTE_RATE_SECRET`, for example with `python3 -c 'import secrets; print(secrets.token_hex(32))'`. The recipient is the address verified in the original website, `zhangzheng270@gmail.com`.
4. Run as a persistent service using the example below, with the environment file loaded by systemd. The script itself does not read .env files. Restrict direct access: it binds only to 127.0.0.1.
5. Review and include `deploy/nginx/quote-api.conf` inside the existing HTTPS server block. Preserve existing redirects and cache rules. With Cloudflare, configure Nginx real-IP handling using **only verified Cloudflare proxy ranges** before `$remote_addr` is trusted as the visitor IP. Do not trust arbitrary forwarded headers. Without real-IP configuration, shared proxy addresses can exhaust the 5/hour limit.
6. Run `nginx -t` and review before reloading. Do not deploy merely because local tests pass.
7. Check GET `/api/quote/status`: `available: true` confirms presence of configuration only, not SMTP authentication or delivery. Send one clearly marked real test request, confirm SMTP acceptance, then confirm receipt in the business inbox and check spam. Check Reply-To. Verify unavailable/failed SMTP responses do not produce success UI or success events.
8. Check rate limiting, Unicode company names, invalid email, date and quantity, blank honeypot, server logs and mobile submission. SMTP disconnects can create an ambiguous outcome; the error UI asks users to contact the studio before retrying. The endpoint does not provide exactly-once delivery.

```ini
[Unit]
Description=Monster CG inquiry API
After=network.target

[Service]
User=monster-quote
Group=monster-quote
WorkingDirectory=/opt/monster-quote
EnvironmentFile=/etc/monster-quote.env
ExecStart=/usr/bin/python3 /opt/monster-quote/quote.py
Restart=on-failure
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/lib/monster-quote

[Install]
WantedBy=multi-user.target
```

Use provider-supported SMTP credentials; never commit them. Ensure SPF/DKIM/DMARC for the provider-approved sender as applicable. Do not use the visitor address as From. The server has per-network and global hourly limits backed by SQLite, a honeypot, strict same-origin JSON handling and bounded fields/body. Origin checks supplement spam controls; they are not authentication. Tune caps after observing legitimate usage. The database retains only hashed identifiers/timestamps; expired rows are pruned on the next request. No form body is logged by the app.

## Analytics integration

No GA4 ID or existing consent manager was found. `assets/conversions.js` does not load a vendor or set cookies. The consent manager must set `window.monsterAnalyticsConsent = true` only after the visitor's valid analytics consent and restore it to false on withdrawal. The approved analytics installation must supply `gtag`. Events are `quote_click`, `quote_submit_success`, `email_click`, `whatsapp_click`, with `source_page` restricted to a path. Query strings, form fields and email addresses are excluded from these events. No retroactive event queue is kept. Review the separate GA installation's automatic pageviews/enhanced measurement too; this adapter alone cannot control those.

Test in GA DebugView/Realtime after integration. Mocked browser events only validate the adapter; they do not prove that GA receives data. Review the privacy notice and retention policy before enabling analytics.

## Rollback

Restore the previous static files, remove only the two quote proxy locations and stop the quote service. Preserve all original project assets and URLs. Email and WhatsApp remain usable throughout. GitHub Pages alone cannot run this backend; this handoff targets the self-hosted server confirmed by the owner.
