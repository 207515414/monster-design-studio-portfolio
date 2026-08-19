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
    def test_china_site_is_a_separate_chinese_entry_point(self):
        chinese_home = ROOT / "zh/index.html"
        chinese_contact = ROOT / "zh/contact/index.html"
        chinese_privacy = ROOT / "zh/privacy-policy/index.html"
        for path in (chinese_home, chinese_contact, chinese_privacy):
            with self.subTest(path=path):
                self.assertTrue(path.is_file(), path)
        if not chinese_home.is_file():
            return

        page = chinese_home.read_text(encoding="utf-8")
        self.assertIn('lang="zh-CN"', page)
        self.assertIn("图纸深化", page)
        self.assertIn("空间效果表现", page)
        self.assertIn("三维动画", page)
        self.assertIn("住宅、酒店与商业空间", page)
        self.assertIn('assets/zh/china-site-hero.webp', page)
        self.assertTrue((ROOT / "assets/zh/china-site-hero.webp").is_file())
        for relative in (
            "assets/zh/drawing-detail.webp",
            "assets/zh/visualization-detail.webp",
            "assets/zh/animation-detail.webp",
        ):
            self.assertTrue((ROOT / relative).is_file(), relative)
            self.assertIn(relative, page)
        self.assertIn('class="service-image"', page)
        self.assertNotIn("外包", page)
        self.assertNotIn("WhatsApp", page)
        self.assertNotIn("Facebook", page)

    def test_china_contact_page_uses_the_confirmed_wechat_qr_code(self):
        contact = (ROOT / "zh/contact/index.html").read_text(encoding="utf-8")
        qr_code = ROOT / "assets/zh/wechat-qr.jpg"
        self.assertTrue(qr_code.is_file(), qr_code)
        self.assertIn("assets/zh/wechat-qr.jpg", contact)
        self.assertIn("z-787-00", contact)
        self.assertNotIn("二维码将在上线前", contact)

    def test_china_homepage_has_plain_language_owner_path_and_local_motion(self):
        page = (ROOT / "zh/index.html").read_text(encoding="utf-8")
        script = ROOT / "zh/zh.js"
        self.assertIn("让空间，在施工前就被看见", page)
        self.assertIn("我是业主", page)
        self.assertIn("户型图、现场照片或参考图片", page)
        self.assertIn("发资料，获取项目建议", page)
        self.assertIn('src="zh.js"', page)
        self.assertTrue(script.is_file(), script)

    def test_china_reveal_content_stays_visible_without_javascript(self):
        css = (ROOT / "zh" / "zh.css").read_text(encoding="utf-8")
        self.assertIn(".js .reveal {", css)
        self.assertIn(".js .reveal.is-visible {", css)

    def test_china_site_self_hosts_an_openly_licensed_readable_font(self):
        css = (ROOT / "zh" / "zh.css").read_text(encoding="utf-8")
        self.assertIn("font-family: \"Monster Noto Sans SC\"", css)
        self.assertIn("url(\"../assets/fonts/noto-sans-sc-400.ttf\")", css)
        self.assertTrue((ROOT / "assets/fonts/OFL-1.1.txt").is_file())

    def test_public_css_uses_only_self_hosted_font_assets(self):
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        self.assertIn('url("assets/fonts/noto-sans-latin-400.ttf")', css)
        self.assertIn('font-family: "Monster Noto Sans Latin"', css)
        self.assertNotIn("Georgia", css)
        self.assertNotIn("Arial", css)
        self.assertNotIn("http", css)

    def test_china_contact_page_explains_what_an_owner_can_send(self):
        contact = (ROOT / "zh/contact/index.html").read_text(encoding="utf-8")
        self.assertIn("住宅 / 酒店 / 商业空间 / 团队合作", contact)
        self.assertIn("预计开始时间", contact)

    def test_china_ip_redirect_is_server_side_and_can_be_overridden(self):
        redirect_config = ROOT / "deploy/nginx/china-ip-redirect.conf"
        country_map = ROOT / "deploy/nginx/cloudflare-country-map.conf"
        install_guide = ROOT / "deploy/nginx/README.md"
        self.assertTrue(redirect_config.is_file(), redirect_config)
        self.assertTrue(country_map.is_file(), country_map)
        self.assertTrue(install_guide.is_file(), install_guide)
        config = redirect_config.read_text(encoding="utf-8") + country_map.read_text(encoding="utf-8")
        guide = install_guide.read_text(encoding="utf-8")
        self.assertIn("$http_cf_ipcountry", config)
        self.assertNotIn("geoip2", config.lower())
        self.assertIn("CN", config)
        self.assertIn("/zh/", config)
        self.assertIn("monster_locale", config)
        self.assertIn("VPN", guide)

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

    def test_strengthened_pages_are_substantial_and_well_linked(self):
        strengthened_pages = (*INDUSTRY_PAGES,
            "portfolio/index.html",
            "portfolio/commercial-hotel-visualization/index.html",
            "portfolio/shanghai-duplex/index.html",
            "portfolio/guangzhou-villa/index.html",
            "portfolio/riverfront-residence/index.html",
            "portfolio/bank-office/index.html",
            "blog/index.html",
            "blog/what-files-are-needed-for-a-3d-rendering-project/index.html",
            "blog/architectural-visualization-brief/index.html",
            "blog/paid-rendering-test-project/index.html",
            "blog/architectural-rendering-cost-factors/index.html",
        )
        for relative in strengthened_pages:
            with self.subTest(relative=relative):
                page = (ROOT / relative).read_text(encoding="utf-8")
                visible = re.sub(r"<script\b.*?</script>|<style\b.*?</style>|<[^>]+>", " ", page, flags=re.I | re.S)
                words = re.findall(r"[A-Za-zÀ-ÿ']+", visible)
                internal_links = set(re.findall(r'href="(/[^"]+)"', page, re.I))
                self.assertGreaterEqual(len(words), 175, relative)
                self.assertGreaterEqual(len(internal_links), 6, relative)

    def test_changed_sitemap_entries_have_real_lastmod_dates(self):
        root = ET.parse(ROOT / "sitemap.xml").getroot()
        namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
        changed = {
            "https://monster-cg.com/portfolio/",
            "https://monster-cg.com/blog/",
            *(f"https://monster-cg.com/{relative.removesuffix('index.html')}" for relative in INDUSTRY_PAGES),
        }
        dated = {
            node.find(f"{namespace}loc").text
            for node in root.findall(f"{namespace}url")
            if node.find(f"{namespace}lastmod") is not None
        }
        self.assertTrue(changed.issubset(dated), sorted(changed - dated))


if __name__ == "__main__":
    unittest.main()
