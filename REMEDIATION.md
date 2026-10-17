# Conversion remediation — 2026-10-17

## Source and audit

Source: https://github.com/207515414/monster-design-studio-portfolio (main tree 593abc365534a6a1ec36e6f8876108ad4172c1b7). Git transport failed; text was retrieved using GitHub API and assets from the source archive and published site, all checked against upstream Git blob hashes. This local Git baseline is a snapshot, not upstream commit history. Do not force-push this repository. Apply the final patch to a normal upstream checkout for release.

Static HTML/CSS/vanilla JavaScript; no package.json, build tool, type-check configuration or mail backend. README documents GitHub Pages; deploy/nginx documents a Cloudflare-fronted Nginx server. The owner confirmed a self-hosted server; GitHub is used for code preparation before transfer. Existing script.js only sets data-last-cta; no configured GA4 delivery was found. Existing domain, metadata, sitemap, robots, language pages, search verification and original assets must be preserved.

Confirmed contact references in index.html and contact/index.html: zhangzheng270@gmail.com and https://wa.me/8619035057372. assets/data.js marks commercial-hotel-visualization and shanghai-duplex as concept work. Other entries describe presentation/proposal work, not completed buildings. No verified linked production-stage sequence was found.

## File plan recorded before implementation

- index.html, styles.css: supplied heading/copy; actual project hero; selected work before services; interior/exterior focus; subordinate CAD link; five steps; direct inquiry channels.
- portfolio/index.html and portfolio/{commercial-hotel-visualization,shanghai-duplex,guangzhou-villa,riverfront-residence,bank-office}/index.html: visual portfolio cards, final-image galleries, factual concise descriptions, concept labels where supported, inquiry links; retain URLs.
- site.css: responsive galleries, forms, accessible states and focus visibility.
- contact/index.html, assets/quote.js: six requested fields, explicit pending/error/success states and availability checks.
- server/quote.py, server/.env.example, deploy/nginx/quote-api.conf: standard-library SMTP service suitable for an existing Nginx host; server validation, honeypot, bounded persistent rate limits, same-origin JSON requests; no paid service or deployment.
- assets/conversions.js, privacy-policy/index.html: opt-in analytics integration, sanitized source paths, no inquiry payloads in analytics. No analytics vendor is installed without configuration.
- process/index.html, services/index.html: consistent five-step flow and service priority.
- sitemap.xml: accurate lastmod updates for changed pages.
- tests: update superseded positioning expectations and add backend behavior tests; run existing suite and JavaScript syntax checks.

## Release gates

Confirm actual host; run private SMTP configuration outside the public document root; test real delivery and spam handling; install API proxy only after review. GitHub Pages alone cannot run the Python service. Verify live API status and browser failure/success flows before enabling the form. Confirm privacy text and consent integration; connect a real analytics property and verify event receipt before reporting conversions operational. No production push is authorized.

## Verification results

- Existing Python suite plus backend behavior tests: 45 tests passed.
- JavaScript syntax: script.js, assets/data.js, assets/quote.js, assets/conversions.js passed `node --check`.
- `git diff --check` passed. No configured lint, TypeScript or build commands exist; this is a directly served static site.
- Chrome desktop/mobile checks: 1440, 390 and 320 px; home, portfolio index, hotel detail, duplex detail, services index, interior service, exterior service and contact (24 route/viewport combinations). No horizontal overflow, broken images or page JavaScript errors. Mobile menu open/Escape tested.
- Browser screenshots visually reviewed for homepage, portfolio and contact. Fixed existing overlay stacking and inaccurate project image dimensions. Original WebP images remain unchanged; below-fold galleries are lazy loaded and the hero uses fetchpriority=high.
- All 136 original binary assets verified against GitHub blob hashes; no original artwork deleted or rewritten.
- Backend tests cover malformed JSON, origin/body size rejection, validation, injection, missing configuration, SMTP failure, recipient/TLS, successful SMTP acceptance and persistent rate limits.
- Browser simulation covers unavailable API, failed submission preserving fields, success-only conversion after consent, source page, exclusion of submitted email, duplicate-submit prevention and consent withdrawal. SMTP and gtag were mocked. No real email or analytics delivery is claimed.
- Existing route coverage, canonical/title/description requirements, sitemap and local link tests pass. Production HTTP responses, indexing, server configuration and inbox delivery remain release gates.

## Remaining owner inputs and release checks

1. Existing SMTP provider/host, port, login, secret and provider-approved sender, configured privately on the server. Confirm the published recipient remains the desired business inbox. No credentials should be committed or posted into a public issue.
2. Server OS, Nginx document root and process manager when installation is authorized. Review Cloudflare trusted real-IP settings so rate limiting uses visitor IPs.
3. If analytics is desired: actual property configuration, consent manager and approved privacy/retention details. No tracking vendor has been silently installed.
4. Optional: public production-stage sequences linked to the same projects and clean standalone rendering exports. Existing presentation boards are retained as evidence; no invented process visuals are used.
5. Before release: backup current site, validate Nginx configuration, test real form delivery and error paths, inspect mobile pages at the public domain, verify all old URLs/canonical/sitemap and Search Console, then verify analytics receipt after consent. No push or production deployment was performed.

## Actual changed and added files

- `.gitignore`
- `README.md`
- `REMEDIATION.md`
- `about/index.html`
- `assets/conversions.js`
- `assets/quote.js`
- `blog/architectural-rendering-cost-factors/index.html`
- `blog/architectural-visualization-brief/index.html`
- `blog/index.html`
- `blog/paid-rendering-test-project/index.html`
- `blog/what-files-are-needed-for-a-3d-rendering-project/index.html`
- `contact/index.html`
- `deploy/QUOTE-SERVICE.md`
- `deploy/nginx/quote-api.conf`
- `faq/index.html`
- `index.html`
- `industries/architects/index.html`
- `industries/fit-out-contractors/index.html`
- `industries/interior-designers/index.html`
- `industries/real-estate-developers/index.html`
- `portfolio/bank-office/index.html`
- `portfolio/commercial-hotel-visualization/index.html`
- `portfolio/guangzhou-villa/index.html`
- `portfolio/index.html`
- `portfolio/riverfront-residence/index.html`
- `portfolio/shanghai-duplex/index.html`
- `privacy-policy/index.html`
- `process/index.html`
- `server/.env.example`
- `server/quote.py`
- `services/3d-exterior-rendering-services/index.html`
- `services/3d-interior-rendering-services/index.html`
- `services/architectural-visualization-services/index.html`
- `services/cad-drafting-services/index.html`
- `services/commercial-hospitality-rendering/index.html`
- `services/index.html`
- `services/interior-elevation-shop-drawing-services/index.html`
- `site.css`
- `sitemap.xml`
- `styles.css`
- `tests/test_quote.py`
- `tests/test_seo_architecture.py`
- `tests/test_site.py`
