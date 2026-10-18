# Optional GA4 activation

Status: owner supplied G-YXNXQPNM5P on 2026-10-18; configured for release. Server synchronization and actual GA4 receipt remain unverified.

1. Obtain the owner's web-stream measurement ID for monster-cg.com (G-...). Do not use a sample ID. Set only assets/analytics-config.json measurementId.
2. In GA4, disable Enhanced Measurement, Google Signals and user-provided data collection. Do not enable advertising integrations. Review retention settings and privacy notice with the owner.
3. Publish the script, consent CSS/config, updated English HTML script URLs and privacy notice together through the existing GitHub/server workflow. No npm build is required.
4. In a fresh browser, confirm no Google analytics/tag requests before accepting or after rejecting. Confirm the form still works regardless of choice. Privacy choices in the footer allows withdrawal and reloads to unload the tag. Choices expire after 180 days; GPC disables analytics.
5. After accepting, verify actual receipt of page_view, quote_click, email_click, whatsapp_click and quote_submit_success in GA4. Mark only quote_submit_success as a key event. Do not send real inquiries just to test without owner authorization.
6. Inspect requests: only sanitized source_page, page_location, blank page_referrer and static page_title are supplied. Never include email/company/message, query strings or URL fragments. Disable automatic events as above because they bypass this event allowlist.
7. Test desktop/mobile, rejection persistence, acceptance persistence and withdrawal. Treat local queue checks as implementation tests only, not proof of GA receipt.

Scope: English pages loading assets/conversions.js. Other language pages remain untracked. Blank/missing/invalid config keeps this integration disabled. Rollback by blanking measurementId; already-open pages may require reload.
