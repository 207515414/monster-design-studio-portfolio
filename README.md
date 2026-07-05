# Monster Design Studio Portfolio Site

Static portfolio website for Monster Design Studio: commercial interior design, visualization, FF&E direction, CAD drafting support, technical documentation, and anonymized construction drawing previews.

## Contact

- Brand: Monster Design Studio
- WhatsApp: +86 190 3505 7372
- Email: zhangzheng270@gmail.com
- Logo: original geometric mark in `assets/brand/logo-mark.svg`; horizontal version in `assets/brand/logo-horizontal.svg`
- Privacy Policy: `privacy-policy.html`
- SEO files: `robots.txt` and `sitemap.xml`

## Preview Locally

Open `index.html` directly in a browser, or run a local server:

```bash
python -m http.server 8080
```

Then open:

```text
http://localhost:8080
```

## Deploy to GitHub Pages

1. Create a new GitHub repository.
2. Upload everything inside this `portfolio-site` folder to the repository root.
3. Go to `Settings` -> `Pages`.
4. Under `Build and deployment`, choose:
   - Source: `Deploy from a branch`
   - Branch: `main`
   - Folder: `/root`
5. Save and wait for GitHub Pages to publish the URL.

## Notes

- Original PPT/PPTX files are not included.
- Original PDF/DWG drawing files are not included.
- The site uses cropped public preview images under `assets/public` and privacy-safe construction drawing previews.
- Keep generated exports, caches, temporary folders, and local editor files out of Git. Use the ignored `tmp/` or `exports/` folders if you need scratch space.
- Construction drawing title blocks, client names, and project identifiers are omitted from public preview images.
- The logo is an original geometric mark designed to avoid monster-claw, animal, and famous-brand visual references. Formal trademark use still requires a proper trademark search in the target countries.
- If a client project is confidential, remove its public preview folder under `assets/public/projects` and delete the matching project object in `assets/data.js`.
- If a construction drawing set is confidential, remove its folder under `assets/drawings` and delete the matching object in `window.CONSTRUCTION_SETS` in `assets/data.js`.
- For overseas B2B use, send clients the GitHub Pages URL together with a short message and ask them to send one plan, sketch, or reference image for quotation.
