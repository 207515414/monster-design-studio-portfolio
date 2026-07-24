import re
import json
import unittest
from pathlib import Path
from urllib.parse import urlparse
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "https://monster-cg.com"

CORE_PAGES = (
    "index.html",
    "services/index.html",
    "portfolio/index.html",
    "process/index.html",
    "about/index.html",
    "faq/index.html",
    "blog/index.html",
    "contact/index.html",
    "privacy-policy/index.html",
)
SERVICE_PAGES = (
    "services/architectural-visualization-services/index.html",
    "services/3d-interior-rendering-services/index.html",
    "services/3d-exterior-rendering-services/index.html",
    "services/commercial-hospitality-rendering/index.html",
    "services/cad-drafting-services/index.html",
    "services/interior-elevation-shop-drawing-services/index.html",
)
INDUSTRY_PAGES = (
    "industries/architects/index.html",
    "industries/interior-designers/index.html",
    "industries/real-estate-developers/index.html",
    "industries/fit-out-contractors/index.html",
)


class SeoArchitectureTests(unittest.TestCase):
    def test_required_static_pages_exist(self):
        for relative in (*CORE_PAGES, *SERVICE_PAGES, *INDUSTRY_PAGES):
            with self.subTest(relative=relative):
                self.assertTrue((ROOT / relative).is_file(), relative)

    def test_public_pages_have_unique_titles_and_self_canonicals(self):
        titles = []
        for relative in (*CORE_PAGES, *SERVICE_PAGES, *INDUSTRY_PAGES):
            page = (ROOT / relative).read_text(encoding="utf-8")
            title = re.search(r"<title>(.*?)</title>", page, re.I | re.S)
            canonical = re.search(r'<link rel="canonical" href="([^"]+)"', page, re.I)
            h1 = re.findall(r"<h1\b[^>]*>", page, re.I)
            self.assertIsNotNone(title, relative)
            self.assertIsNotNone(canonical, relative)
            self.assertEqual(len(h1), 1, relative)
            self.assertTrue(canonical.group(1).startswith(DOMAIN), relative)
            titles.append(title.group(1).strip())
        self.assertEqual(len(titles), len(set(titles)))

    def test_robots_and_sitemap_use_the_production_domain(self):
        robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
        self.assertIn(f"Sitemap: {DOMAIN}/sitemap.xml", robots)
        self.assertNotIn("github.io", robots)
        root = ET.parse(ROOT / "sitemap.xml").getroot()
        locations = [node.text for node in root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
        self.assertGreaterEqual(len(locations), len(CORE_PAGES) + len(SERVICE_PAGES) + len(INDUSTRY_PAGES))
        self.assertTrue(all(url.startswith(DOMAIN) for url in locations))

    def test_github_pages_domain_and_not_found_page_are_present(self):
        self.assertEqual((ROOT / "CNAME").read_text(encoding="utf-8").strip(), "monster-cg.com")
        not_found = (ROOT / "404.html").read_text(encoding="utf-8")
        self.assertIn('content="noindex, follow"', not_found)
        self.assertIn('href="/"', not_found)

    def test_faq_and_published_articles_have_matching_json_ld(self):
        for relative, schema_type in (
            ("faq/index.html", "FAQPage"),
            ("blog/what-files-are-needed-for-a-3d-rendering-project/index.html", "Article"),
            ("blog/architectural-visualization-brief/index.html", "Article"),
            ("blog/paid-rendering-test-project/index.html", "Article"),
        ):
            page = (ROOT / relative).read_text(encoding="utf-8")
            match = re.search(r'<script type="application/ld\+json">(.*?)</script>', page, re.S)
            self.assertIsNotNone(match, relative)
            self.assertEqual(json.loads(match.group(1))["@type"], schema_type, relative)

    def test_internal_html_links_resolve_to_static_files(self):
        for path in ROOT.rglob("*.html"):
            page = path.read_text(encoding="utf-8")
            for href in re.findall(r'''href=["']([^"']+)["']''', page, re.I):
                if href.startswith(("http", "mailto:", "tel:", "#")):
                    continue
                target = href.split("#", 1)[0].split("?", 1)[0]
                if not target:
                    continue
                resolved = (ROOT / target.lstrip("/")).resolve() if target.startswith("/") else (path.parent / target).resolve()
                self.assertTrue(resolved.exists(), f"{path.relative_to(ROOT)} -> {href}")

    def test_no_unsupported_regulated_service_claims(self):
        combined = "\n".join(path.read_text(encoding="utf-8") for path in ROOT.rglob("*.html")).lower()
        for forbidden in ("licensed architectural services", "permit approval"):
            self.assertNotIn(forbidden, combined)

    def test_uae_arabic_homepage_has_reciprocal_alternates_and_privacy_link(self):
        english = (ROOT / "index.html").read_text(encoding="utf-8")
        arabic_path = ROOT / "ar-ae/index.html"
        self.assertTrue(arabic_path.is_file(), arabic_path)
        if not arabic_path.is_file():
            return
        arabic = arabic_path.read_text(encoding="utf-8")
        self.assertIn('hreflang="ar-AE" href="https://monster-cg.com/ar-ae/"', english)
        self.assertIn('hreflang="en" href="https://monster-cg.com/"', arabic)
        self.assertIn('hreflang="x-default" href="https://monster-cg.com/"', english)
        self.assertIn('lang="ar" dir="rtl"', arabic)
        self.assertIn('href="/ar-ae/privacy-policy/"', arabic)
        self.assertIn('href="../styles.css?v=', arabic)
        self.assertIn('src="../assets/brand/logo-mark.svg"', arabic)

    def test_sitemap_includes_english_and_uae_arabic_entry_points(self):
        root = ET.parse(ROOT / "sitemap.xml").getroot()
        locations = {
            node.text
            for node in root.findall(
                "{http://www.sitemaps.org/schemas/sitemap/0.9}url/"
                "{http://www.sitemaps.org/schemas/sitemap/0.9}loc"
            )
        }
        self.assertIn("https://monster-cg.com/", locations)
        self.assertIn("https://monster-cg.com/ar-ae/", locations)
        self.assertIn("https://monster-cg.com/ar-ae/privacy-policy/", locations)


if __name__ == "__main__":
    unittest.main()
