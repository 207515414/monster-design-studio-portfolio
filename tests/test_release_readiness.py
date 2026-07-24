import re
import unittest
from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "https://monster-cg.com"
EXCLUDED = {"404.html", "google21cc5db03d0ba754.html", "privacy-policy.html"}


class ReleaseReadinessTests(unittest.TestCase):
    def test_every_indexable_page_has_core_metadata(self):
        pages = [path for path in ROOT.rglob("*.html") if path.relative_to(ROOT).as_posix() not in EXCLUDED]
        titles = []
        descriptions = []
        for path in pages:
            relative = path.relative_to(ROOT).as_posix()
            content = path.read_text(encoding="utf-8")
            title = re.search(r"<title>(.*?)</title>", content, re.I | re.S)
            description = re.search(r'<meta\b[^>]*\bname="description"[^>]*\bcontent="([^"]+)"', content, re.I | re.S)
            canonical = re.search(r'<link rel="canonical" href="([^"]+)"', content, re.I)
            h1 = re.findall(r"<h1\b[^>]*>", content, re.I)
            self.assertIsNotNone(title, relative)
            self.assertIsNotNone(description, relative)
            self.assertIsNotNone(canonical, relative)
            self.assertEqual(len(h1), 1, relative)
            self.assertTrue(canonical.group(1).startswith(DOMAIN), relative)
            titles.append(title.group(1).strip())
            descriptions.append(description.group(1).strip())
        self.assertEqual(len(titles), len(set(titles)))
        self.assertEqual(len(descriptions), len(set(descriptions)))

    def test_sitemap_covers_all_indexable_directory_pages(self):
        root = ET.parse(ROOT / "sitemap.xml").getroot()
        urls = {node.text for node in root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc")}
        expected = set()
        for page in ROOT.rglob("index.html"):
            relative = page.parent.relative_to(ROOT).as_posix()
            url = DOMAIN + ("/" if relative == "." else f"/{relative}/")
            expected.add(url)
        self.assertTrue(expected.issubset(urls), sorted(expected - urls))


if __name__ == "__main__":
    unittest.main()
