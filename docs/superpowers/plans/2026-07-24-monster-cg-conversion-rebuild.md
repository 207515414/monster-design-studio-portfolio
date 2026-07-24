# Monster CG Conversion Rebuild Implementation Plan

> For agentic workers: REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Build an original, image-led B2B conversion site for Monster CG, with English and UAE Arabic entry points, truthful SEO, and measurable inquiry actions.

**Architecture:** Keep the static HTML/CSS/vanilla-JS stack and Nginx deployment. Replace the homepage with a conversion page; retain standalone service, industry, and portfolio pages. Add a locale layer at /ar-ae/ with explicit alternate links instead of automatic language redirects.

**Tech Stack:** Static HTML, CSS, vanilla JavaScript, Python unittest, XML sitemap, JSON-LD, Nginx, Search Console; optional future GA4.

---

## File structure

| File | Responsibility |
| --- | --- |
| index.html | English conversion homepage: copy, metadata, navigation, schema, and CTA links. |
| styles.css | Conversion homepage visual system and responsive behavior. |
| script.js | Existing accessible UI plus passive data-track hooks. |
| assets/brand/home/ | Original, non-project support artwork. |
| ar-ae/index.html | UAE Arabic landing page with reciprocal locale metadata. |
| ar-ae/privacy-policy/index.html | Faithful Arabic privacy-policy translation. |
| site.css | Shared static-page language selector and RTL styles. |
| sitemap.xml, robots.txt | Crawlable English and Arabic entry points. |
| tests/test_site.py | Homepage conversion, trust-policy, CTA, and asset tests. |
| tests/test_seo_architecture.py | Locale, alternate-link, sitemap, and keyword-ownership tests. |
| README.md | Search Console baseline, future GA4, VPS deployment handoff. |

### Task 1: Define failing conversion and locale contracts

**Files:**
- Modify: tests/test_site.py
- Modify: tests/test_seo_architecture.py

- [ ] **Step 1: Add homepage conversion tests**

~~~
def test_homepage_uses_conversion_positioning_and_separate_portfolio_link(self):
    self.assertIn("Architectural Visualization &amp; 3D Rendering for Global Design Teams", INDEX)
    self.assertIn("architectural visualization services", INDEX.lower())
    self.assertIn("outsource CAD drafting services", INDEX.lower())
    self.assertIn('href="/portfolio/"', INDEX)
    self.assertIn('href="/privacy-policy/"', INDEX)

def test_homepage_does_not_invent_scale_or_client_proof(self):
    lower = INDEX.lower()
    for phrase in ("trusted by", "projects completed", "years of experience", "client logos", "founded in"):
        self.assertNotIn(phrase, lower)

def test_homepage_exposes_trackable_inquiry_actions(self):
    self.assertIn('data-track="project-brief"', INDEX)
    self.assertIn('data-track="whatsapp-inquiry"', INDEX)
~~~

- [ ] **Step 2: Add Arabic locale test**

~~~
def test_uae_arabic_homepage_has_reciprocal_alternates_and_privacy_link(self):
    english = (ROOT / "index.html").read_text(encoding="utf-8")
    arabic = (ROOT / "ar-ae/index.html").read_text(encoding="utf-8")
    self.assertIn('hreflang="ar-AE" href="https://monster-cg.com/ar-ae/"', english)
    self.assertIn('hreflang="en" href="https://monster-cg.com/"', arabic)
    self.assertIn('hreflang="x-default" href="https://monster-cg.com/"', english)
    self.assertIn('lang="ar" dir="rtl"', arabic)
    self.assertIn('href="/ar-ae/privacy-policy/"', arabic)
~~~

- [ ] **Step 3: Run tests to verify they fail**

~~~
py -3 -m unittest discover -s tests -p "test_*.py" -v
~~~

Expected: FAIL because the new conversion strings, tracking hooks, Arabic route, and alternate links do not exist.

- [ ] **Step 4: Commit**

~~~
git add tests/test_site.py tests/test_seo_architecture.py
git commit -m "test: define conversion and locale requirements"
~~~

### Task 2: Create original homepage support images

**Files:**
- Create: assets/brand/home/hero-production-atmosphere.webp
- Create: assets/brand/home/cad-production-detail.webp
- Create: assets/brand/home/review-workflow-atmosphere.webp
- Modify: README.md
- Modify: tests/test_site.py

- [ ] **Step 1: Add the failing asset test**

~~~
def test_homepage_support_images_are_local_and_labelled_non_project(self):
    for relative in (
        "assets/brand/home/hero-production-atmosphere.webp",
        "assets/brand/home/cad-production-detail.webp",
        "assets/brand/home/review-workflow-atmosphere.webp",
    ):
        self.assertTrue((ROOT / relative).is_file(), relative)
    self.assertIn("non-project support imagery", (ROOT / "README.md").read_text(encoding="utf-8").lower())
~~~

- [ ] **Step 2: Confirm it fails**

~~~
py -3 -m unittest discover -s tests -p "test_site.py" -v
~~~

Expected: FAIL because the image files and documentation statement do not exist.

- [ ] **Step 3: Generate the images with ImageGen**

Create three original, non-client images with these prompts:

~~~
Original wide editorial architectural-visualization studio atmosphere, a premium contemporary building interior at blue hour, warm practical lighting, subtle film grain, deep graphite shadows, warm ivory highlights, no people, no words, no logos, no identifiable real project, 16:9.
~~~

~~~
Original close-up still life for a premium architectural production studio: layered unbranded floor-plan sheets, a minimal scale ruler, translucent tracing paper, soft raking sunlight, charcoal and warm ivory palette, no text, no logos, no people, not a real client drawing, 3:2.
~~~

~~~
Original editorial architectural review scene: abstract pinned material samples and a softly out-of-focus neutral model silhouette, sophisticated graphic composition, warm grey and copper accent, no legible text, no logos, no people, not a client project, 3:2.
~~~

- [ ] **Step 4: Document image usage**

Append this sentence to README.md:

~~~
The files in assets/brand/home/ are original non-project support imagery for brand atmosphere and workflow sections; portfolio evidence continues to use the existing project assets only.
~~~

- [ ] **Step 5: Verify and commit**

~~~
py -3 -m unittest discover -s tests -p "test_site.py" -v
git add assets/brand/home README.md tests/test_site.py
git commit -m "feat: add original homepage support imagery"
~~~

Expected: PASS.

### Task 3: Rebuild the English conversion homepage

**Files:**
- Modify: index.html
- Modify: styles.css
- Modify: script.js
- Modify: tests/test_site.py

- [ ] **Step 1: Run the failing conversion tests**

~~~
py -3 -m unittest discover -s tests -p "test_site.py" -v
~~~

- [ ] **Step 2: Replace homepage metadata and locale links**

~~~
<title>Architectural Visualization &amp; CAD Production Support | Monster CG</title>
<meta name="description" content="Architectural visualization services, 3D rendering and CAD production support for architects, developers and fit-out teams worldwide." />
<link rel="canonical" href="https://monster-cg.com/" />
<link rel="alternate" hreflang="en" href="https://monster-cg.com/" />
<link rel="alternate" hreflang="ar-AE" href="https://monster-cg.com/ar-ae/" />
<link rel="alternate" hreflang="x-default" href="https://monster-cg.com/" />
~~~

- [ ] **Step 3: Implement semantic sections**

~~~
<main id="top">
  <section class="conversion-hero" aria-labelledby="hero-title">Hero value proposition, primary CTA, secondary CTA, and original studio-atmosphere image.</section>
  <section class="audience-pathways" aria-labelledby="audience-title">Audience pathways for architects, interior designers, developers, and fit-out teams.</section>
  <section class="capability-split" aria-labelledby="capabilities-title">Visualization and CAD-production capability groups with truthful service links.</section>
  <section class="production-method" aria-labelledby="method-title">Brief, production, review, and delivery workflow with original support imagery.</section>
  <section class="selected-work" aria-labelledby="work-title">Four to six cards that link only to existing Monster CG portfolio projects.</section>
  <section class="project-brief" aria-labelledby="brief-title">Project-input checklist and email, WhatsApp, and contact-page inquiry routes.</section>
</main>
~~~

The hero contains one H1, the exact phrase architectural visualization services once in supporting copy, and:

~~~
<a class="button primary" data-track="project-brief" href="/contact/">Send a Project Brief</a>
<a class="button secondary" href="/services/">Explore Capabilities</a>
~~~

The CAD section uses outsource CAD drafting services naturally once and links to /services/cad-drafting-services/. The selected-work section includes four to six existing portfolio links only.

- [ ] **Step 4: Add visual and interaction rules**

Add focused rules for conversion-hero, audience-pathways, capability-split, production-method, selected-work, project-brief, and language-switcher. Use local images with object-fit cover, buttons at least 44px high, responsive grids, and prefers-reduced-motion behavior.

Append this passive hook to script.js. It must not load analytics or transmit data:

~~~
document.querySelectorAll("[data-track]").forEach((link) => {
  link.addEventListener("click", () => {
    document.documentElement.dataset.lastCta = link.dataset.track;
  });
});
~~~

- [ ] **Step 5: Verify and commit**

~~~
py -3 -m unittest discover -s tests -p "test_site.py" -v
node --check script.js
git diff --check
git add index.html styles.css script.js tests/test_site.py
git commit -m "feat: rebuild Monster CG conversion homepage"
~~~

Expected: tests PASS, Node exits 0, and no whitespace errors.

### Task 4: Add UAE Arabic landing and privacy pages

**Files:**
- Create: ar-ae/index.html
- Create: ar-ae/privacy-policy/index.html
- Modify: site.css
- Modify: privacy-policy/index.html
- Modify: tests/test_seo_architecture.py

- [ ] **Step 1: Run the failing Arabic test**

~~~
py -3 -m unittest discover -s tests -p "test_seo_architecture.py" -v
~~~

- [ ] **Step 2: Create Arabic route and reciprocal metadata**

~~~
<html lang="ar" dir="rtl">
<title>خدمات التصور المعماري والدعم الإنتاجي للرسومات | Monster CG</title>
<link rel="canonical" href="https://monster-cg.com/ar-ae/" />
<link rel="alternate" hreflang="en" href="https://monster-cg.com/" />
<link rel="alternate" hreflang="ar-AE" href="https://monster-cg.com/ar-ae/" />
<link rel="alternate" hreflang="x-default" href="https://monster-cg.com/" />
~~~

Translate only the approved service scope, production steps, project-input checklist, contact methods, and privacy link. Do not add UAE address, local-office claim, certification, or unsupported service.

- [ ] **Step 3: Create faithful Arabic privacy page**

Translate visible commitments from privacy-policy/index.html, preserving the same email, WhatsApp path, and policy meaning. Include a link back to /.

- [ ] **Step 4: Add RTL CSS**

~~~
[dir="rtl"] {
  font-family: Tahoma, Arial, sans-serif;
  text-align: right;
}

[dir="rtl"] .bar,
[dir="rtl"] nav,
[dir="rtl"] .locale-actions {
  direction: rtl;
}
~~~

- [ ] **Step 5: Verify and commit**

~~~
py -3 -m unittest discover -s tests -p "test_*.py" -v
git add ar-ae site.css privacy-policy/index.html tests/test_seo_architecture.py
git commit -m "feat: add UAE Arabic landing and privacy pages"
~~~

Expected: PASS.

### Task 5: Finalize sitemap, keyword ownership, and measurement handoff

**Files:**
- Modify: sitemap.xml
- Modify: README.md
- Modify: KEYWORD-MAP.md
- Modify: CONTENT-PLAN.md
- Modify: tests/test_seo_architecture.py

- [ ] **Step 1: Add a failing sitemap test**

~~~
def test_sitemap_includes_english_and_uae_arabic_entry_points(self):
    root = ET.parse(ROOT / "sitemap.xml").getroot()
    locations = {node.text for node in root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc")}
    self.assertIn("https://monster-cg.com/", locations)
    self.assertIn("https://monster-cg.com/ar-ae/", locations)
    self.assertIn("https://monster-cg.com/ar-ae/privacy-policy/", locations)
~~~

- [ ] **Step 2: Confirm it fails, then update sitemap and docs**

~~~
py -3 -m unittest discover -s tests -p "test_seo_architecture.py" -v
~~~

Add Arabic URLs to sitemap.xml. Update KEYWORD-MAP.md and CONTENT-PLAN.md with only supported English-first topics and Arabic UAE adaptations that never claim local presence.

- [ ] **Step 3: Add Search Console and future GA4 handoff to README**

~~~
## Measurement baseline

1. In Search Console, export the previous 28 days of clicks, impressions, average position, top queries, top pages, index coverage, and Core Web Vitals before launch.
2. Submit the updated sitemap and request indexing for /, /services/, /services/cad-drafting-services/, and /ar-ae/ after production verification.
3. Add GA4 only with a consent-aware implementation. Track project-brief, whatsapp-inquiry, email-inquiry, language-switch, contact-form-start, and contact-form-submit when GA4 is configured.
4. Compare the same Search Console window monthly; do not claim a ranking or lead guarantee.
~~~

- [ ] **Step 4: Verify and commit**

~~~
py -3 -m unittest discover -s tests -p "test_*.py" -v
node --check script.js
node --check assets/data.js
git diff --check
git add sitemap.xml README.md KEYWORD-MAP.md CONTENT-PLAN.md tests/test_seo_architecture.py
git commit -m "docs: add Monster CG SEO measurement handoff"
~~~

Expected: every test PASS and all syntax/diff checks exit 0.

### Task 6: Visual QA and VPS release

**Files:**
- Modify only if verification exposes a concrete issue: index.html, styles.css, site.css, script.js, or affected tests.

- [ ] **Step 1: Preview locally**

~~~
py -3 -m http.server 8080
~~~

Inspect /, /portfolio/, /contact/, /privacy-policy/, /ar-ae/, and /ar-ae/privacy-policy/ at desktop and 390px mobile width. Confirm the hero is visible without JavaScript, images load, language links work, privacy links work, and no page scrolls horizontally.

- [ ] **Step 2: Re-run release checks**

~~~
py -3 -m unittest discover -s tests -p "test_*.py" -v
node --check script.js
node --check assets/data.js
git diff --check
~~~

- [ ] **Step 3: Push reviewed commits**

~~~
git push origin main
~~~

Expected: main advances without overwriting remote commits.

- [ ] **Step 4: Update the VPS**

~~~
sudo git -C /var/www/monster-cg.com pull --ff-only origin main
sudo chown -R www-data:www-data /var/www/monster-cg.com
sudo nginx -t && sudo systemctl reload nginx
~~~

Expected: Git fast-forwards and Nginx reports syntax is ok and test is successful.

- [ ] **Step 5: Verify production**

~~~
curl -I https://monster-cg.com/
curl -I https://monster-cg.com/ar-ae/
curl -I https://monster-cg.com/sitemap.xml
~~~

Expected: each URL returns HTTP/1.1 200 OK.
