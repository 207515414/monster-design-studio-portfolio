# Monster CG Website

Static, multi-page marketing site for Monster CG. It uses only HTML, CSS and vanilla JavaScript, so GitHub Pages can publish it without a build server.

## Production configuration

- Canonical domain: `https://monster-cg.com`
- Custom-domain file: `CNAME` containing `monster-cg.com`
- GitHub Pages marker: `.nojekyll`
- Search verification file: `google21cc5db03d0ba754.html`
- Crawl controls: `robots.txt` and `sitemap.xml`

## Publish to GitHub Pages

1. Commit and push this repository's `main` branch.
2. In GitHub, open **Settings → Pages** and select **Deploy from a branch**, then choose `main` and `/ (root)`.
3. Confirm the custom domain is `monster-cg.com` and enable **Enforce HTTPS** after the certificate is available.
4. Do not delete `CNAME`, `.nojekyll`, the Google verification file, portfolio assets or contact links when publishing.
5. Wait for the Pages deployment to finish, then verify these production URLs return the expected page:
   - `https://monster-cg.com/`
   - `https://monster-cg.com/services/`
   - `https://monster-cg.com/portfolio/`
   - `https://monster-cg.com/robots.txt`
   - `https://monster-cg.com/sitemap.xml`
   - `https://monster-cg.com/404.html`

## Search Console handoff

1. Verify the `monster-cg.com` domain property.
2. Submit `https://monster-cg.com/sitemap.xml`.
3. Use URL Inspection for the home page, `/services/`, the six service pages and selected portfolio pages.
4. Request indexing only after checking that production canonical URLs match the sitemap.
5. Review Page Indexing, Core Web Vitals, HTTPS and Mobile Usability reports after Google has crawled the deployment.

## Local verification

Run these before publishing:

```text
py -3 -m unittest discover -s tests -p "test_*.py" -v
node --check script.js
node --check assets/data.js
git diff --check
```

The site intentionally uses Email and WhatsApp rather than a form that falsely claims to submit data. Monster CG provides remote visualization, drafting and technical-documentation production support; it does not provide local approvals, professional stamping or engineering certification.

The files in `assets/brand/home/` are original non-project support imagery for brand atmosphere and workflow sections; portfolio evidence continues to use the existing project assets only.

## Measurement baseline

1. In Search Console, export the previous 28 days of clicks, impressions, average position, top queries, top pages, index coverage, and Core Web Vitals before launch.
2. Submit the updated sitemap and request indexing for `/`, `/services/`, `/services/cad-drafting-services/`, and `/ar-ae/` after production verification.
3. Add GA4 only with a consent-aware implementation. Track `project-brief`, `whatsapp-inquiry`, `email-inquiry`, `language-switch`, `contact-form-start`, and `contact-form-submit` when GA4 is configured.
4. Compare the same Search Console window monthly; do not claim a ranking or lead guarantee.
