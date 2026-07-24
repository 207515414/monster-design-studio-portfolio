import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = (ROOT / "index.html").read_text(encoding="utf-8")
DATA = (ROOT / "assets/data.js").read_text(encoding="utf-8")
SCRIPT = (ROOT / "script.js").read_text(encoding="utf-8")
STYLES = (ROOT / "styles.css").read_text(encoding="utf-8")


class SitePositioningTests(unittest.TestCase):
    def test_hero_states_b2b_remote_production_positioning(self):
        self.assertIn(
            "Architectural Visualization &amp; 3D Rendering for Global Design Teams",
            INDEX,
        )
        self.assertIn("architectural visualization services", INDEX.lower())
        self.assertNotIn("Monster CG | Architectural Visualization & 3D Rendering Studio.", INDEX)

    def test_technical_service_and_portfolio_come_first(self):
        self.assertIn('href="/services/cad-drafting-services/"', INDEX)
        self.assertIn('href="/portfolio/"', INDEX)
        self.assertIn('id="capabilities"', INDEX)
        self.assertIn('id="selected-work"', INDEX)
        self.assertLess(INDEX.index('id="capabilities"'), INDEX.index('id="selected-work"'))

    def test_primary_calls_to_action_request_a_scope_review(self):
        self.assertIn("Send a Project Brief", INDEX)
        self.assertIn("Explore Capabilities", INDEX)
        self.assertIn("View Selected Work", INDEX)

    def test_professional_service_structured_data_is_valid(self):
        match = re.search(
            r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>',
            INDEX,
            re.S,
        )
        self.assertIsNotNone(match)
        payload = json.loads(match.group(1))
        self.assertEqual(payload["@type"], "ProfessionalService")
        self.assertEqual(payload["name"], "Monster CG")
        self.assertIn("Architectural visualization", payload["description"])
        self.assertNotIn("address", payload)
        self.assertNotIn("priceRange", payload)

    def test_navigation_targets_existing_sections(self):
        hrefs = [
            match.group(2)
            for match in re.finditer(r'\bhref\s*=\s*(["\'])(.*?)\1', INDEX, re.I | re.S)
        ]
        ids = {
            match.group(2)
            for match in re.finditer(r'\bid\s*=\s*(["\'])(.*?)\1', INDEX, re.I | re.S)
        }
        for required_href in (
            "/services/",
            "/portfolio/",
            "/process/",
            "/about/",
            "/contact/",
        ):
            self.assertIn(required_href, hrefs)
        for href in hrefs:
            if href.startswith("#"):
                self.assertIn(href[1:], ids)

    def test_local_html_assets_exist(self):
        root = ROOT.resolve()
        attributes = re.finditer(
            r'\b(?:src|href)\s*=\s*(["\'])(.*?)\1',
            INDEX,
            re.I | re.S,
        )
        for match in attributes:
            value = match.group(2)
            if value.lower().startswith(("http://", "https://", "//", "mailto:", "tel:", "#", "/")):
                continue
            relative = value.split("?", 1)[0].split("#", 1)[0]
            if relative:
                resolved = (root / relative).resolve()
                self.assertTrue(resolved.is_relative_to(root), f"Path escapes ROOT: {relative}")
                self.assertTrue(resolved.exists(), relative)

    def test_javascript_syntax_is_valid(self):
        for relative in ("script.js", "assets/data.js"):
            with self.subTest(relative=relative):
                result = subprocess.run(
                    ["node", "--check", str(ROOT / relative)],
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_project_data_image_paths_exist(self):
        image_paths = re.findall(
            r'(?:image|thumb|cover|coverThumb):\s*"([^"]+)"',
            DATA,
        )
        self.assertGreater(len(image_paths), 100)
        for relative in image_paths:
            self.assertTrue((ROOT / relative).exists(), relative)

    def test_no_remote_scripts_iframes_or_unsupported_claims(self):
        remote_scripts = re.findall(
            r'<script\b[^>]*\bsrc\s*=\s*["\'](?:https?:)?//',
            INDEX,
            re.I,
        )
        self.assertEqual(remote_scripts, [])
        self.assertIsNone(re.search(r'<iframe\b', INDEX, re.I))
        combined = (INDEX + "\n" + DATA).lower()
        for claim in (
            "24-hour delivery",
            "unlimited revisions",
            "guaranteed approval",
            "licensed engineering",
            "permit-ready",
            "contractor-ready",
            "worldwide full-service design",
        ):
            self.assertNotIn(claim, combined)

    def test_contact_methods_work_without_javascript(self):
        self.assertRegex(
            INDEX,
            re.compile(
                r'<a\b[^>]*\bhref\s*=\s*(["\'])mailto:zhangzheng270@gmail\.com\1',
                re.I,
            ),
        )
        self.assertRegex(
            INDEX,
            re.compile(
                r'<a\b[^>]*\bhref\s*=\s*(["\'])https://wa\.me/8619035057372\1',
                re.I,
            ),
        )

    def test_dialog_has_an_explicit_escape_handler(self):
        self.assertRegex(
            SCRIPT,
            r'event\.key\s*===\s*"Escape"\s*&&\s*dialog\?\.open[\s\S]*?closeProject\(\);',
        )

    def test_homepage_uses_conversion_positioning_and_separate_portfolio_link(self):
        self.assertIn(
            "Architectural Visualization &amp; 3D Rendering for Global Design Teams",
            INDEX,
        )
        self.assertIn("architectural visualization services", INDEX.lower())
        self.assertIn("outsource cad drafting services", INDEX.lower())
        self.assertIn('href="/portfolio/"', INDEX)
        self.assertIn('href="/privacy-policy/"', INDEX)

    def test_homepage_does_not_invent_scale_or_client_proof(self):
        lower = INDEX.lower()
        for phrase in (
            "trusted by",
            "projects completed",
            "years of experience",
            "client logos",
            "founded in",
        ):
            self.assertNotIn(phrase, lower)

    def test_homepage_exposes_trackable_inquiry_actions(self):
        self.assertIn('data-track="project-brief"', INDEX)
        self.assertIn('data-track="whatsapp-inquiry"', INDEX)

    def test_homepage_support_images_are_local_and_labelled_non_project(self):
        for relative in (
            "assets/brand/home/hero-production-atmosphere.webp",
            "assets/brand/home/cad-production-detail.webp",
            "assets/brand/home/review-workflow-atmosphere.webp",
        ):
            self.assertTrue((ROOT / relative).is_file(), relative)
        readme = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        self.assertIn("non-project support imagery", readme)

    def test_header_uses_the_existing_brand_mark_without_forced_inversion(self):
        self.assertIn('src="assets/brand/logo-mark.svg"', INDEX)
        self.assertNotIn("filter:brightness(0) invert(1)", STYLES)


if __name__ == "__main__":
    unittest.main()

