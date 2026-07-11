# 怪兽设计工作室 B2B 网站改造实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**目标：** 将现有英文作品集改造成面向海外设计事务所、建筑师和商业装修承包商的远程 CAD、技术文档与效果图支持网站，并保持现有图库、交互和联系方式正常工作。

**实现方式：** 保持纯 HTML、CSS 和原生 JavaScript 的静态架构，不增加框架、后台、追踪代码或第三方表单。先用 Python 标准库建立定位、结构、链接和安全回归测试，再重写页面及项目数据，最后通过本地浏览器验证并使用 GitHub 通道推送到 `main`。

**技术栈：** HTML5、CSS3、原生 JavaScript、Python `unittest`、GitHub Pages

---

## 文件结构与职责

- 新建 `tests/test_site.py`：验证定位、服务顺序、页面顺序、结构化数据、链接、资源和宣传边界。
- 修改 `index.html`：负责 SEO、首屏、服务结构、案例顺序、合作流程、询盘内容和结构化数据。
- 修改 `assets/data.js`：负责效果图和技术图纸案例的标题、摘要、标签及能力边界。
- 保持 `script.js`：继续负责安全的 DOM 渲染、筛选、弹窗、移动导航和无障碍交互；只有测试发现结构不兼容时才做最小修改。
- 保持 `styles.css`：复用现有组件和响应式规则；只有浏览器检查发现新文案溢出或层级异常时才做最小修改。
- 保持 `privacy-policy.html`、`robots.txt` 和 `sitemap.xml`：第一版不加入追踪、第三方表单或虚构域名。

### 任务一：建立网站定位与安全回归测试

**文件：**

- 新建：`tests/test_site.py`
- 测试：`index.html`
- 测试：`assets/data.js`

- [ ] **步骤 1：写入当前网站必然无法通过的新定位测试**

```python
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = (ROOT / "index.html").read_text(encoding="utf-8")
DATA = (ROOT / "assets/data.js").read_text(encoding="utf-8")


class SitePositioningTests(unittest.TestCase):
    def test_hero_states_b2b_remote_production_positioning(self):
        self.assertIn(
            "Remote CAD drafting and visualization support for busy design teams.",
            INDEX,
        )
        self.assertIn("overseas interior design studios, architects and fit-out contractors", INDEX)
        self.assertNotIn("Commercial interiors, visualized and delivered with precision.", INDEX)

    def test_technical_service_and_portfolio_come_first(self):
        first_service = INDEX.index("<h3>CAD Drafting &amp; Technical Documentation</h3>")
        visualization_service = INDEX.index("<h3>Interior Visualization</h3>")
        self.assertLess(first_service, visualization_service)
        self.assertLess(INDEX.index('id="drawings"'), INDEX.index('id="work"'))

    def test_primary_calls_to_action_request_a_scope_review(self):
        self.assertIn("Send a Project Brief", INDEX)
        self.assertIn("View Technical Drawings", INDEX)
        self.assertIn("Start with a paid pilot when appropriate", INDEX)

    def test_professional_service_structured_data_is_valid(self):
        match = re.search(
            r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>',
            INDEX,
            re.S,
        )
        self.assertIsNotNone(match)
        payload = json.loads(match.group(1))
        self.assertEqual(payload["@type"], "ProfessionalService")
        self.assertEqual(payload["name"], "Monster Design Studio")
        self.assertIn("CAD drafting", payload["description"])
        self.assertNotIn("address", payload)
        self.assertNotIn("priceRange", payload)

    def test_navigation_targets_existing_sections(self):
        ids = set(re.findall(r'\sid="([^"]+)"', INDEX))
        for anchor in re.findall(r'href="#([^"]+)"', INDEX):
            self.assertIn(anchor, ids)

    def test_local_html_assets_exist(self):
        for value in re.findall(r'(?:src|href)="([^"]+)"', INDEX):
            if value.startswith(("http://", "https://", "mailto:", "tel:", "#")):
                continue
            relative = value.split("?", 1)[0].split("#", 1)[0]
            if relative:
                self.assertTrue((ROOT / relative).exists(), relative)

    def test_project_data_image_paths_exist(self):
        image_paths = re.findall(
            r'(?:image|thumb|cover|coverThumb):\s*"([^"]+)"',
            DATA,
        )
        self.assertGreater(len(image_paths), 100)
        for relative in image_paths:
            self.assertTrue((ROOT / relative).exists(), relative)

    def test_no_remote_scripts_iframes_or_unsupported_claims(self):
        remote_scripts = re.findall(r'<script[^>]+src="https?://', INDEX, re.I)
        self.assertEqual(remote_scripts, [])
        self.assertNotRegex(INDEX, r'<iframe\b')
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
        self.assertIn("mailto:zhangzheng270@gmail.com", INDEX)
        self.assertIn("https://wa.me/8619035057372", INDEX)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **步骤 2：运行测试并确认旧定位导致失败**

运行：

```text
py -3 -m unittest discover -s tests -p "test_*.py" -v
```

预期：定位、服务顺序、行动按钮、结构化数据和不支持用词相关测试失败；既有链接和图片资源测试通过。

- [ ] **步骤 3：提交测试基线**

```text
git add tests/test_site.py
git commit -m "test: add B2B positioning checks"
```

### 任务二：重写页面头部、首屏和导航

**文件：**

- 修改：`index.html:5-92`
- 测试：`tests/test_site.py`

- [ ] **步骤 1：更新 SEO 标题和描述**

使用以下最终文案：

```html
<title>Remote CAD Drafting &amp; Interior Visualization Support | Monster Design Studio</title>
<meta
  name="description"
  content="Remote CAD drafting, technical documentation and interior visualization support for overseas interior design studios, architects and fit-out contractors."
/>
```

Open Graph 和 Twitter 标题统一为 `Remote CAD Drafting & Interior Visualization Support | Monster Design Studio`，描述统一为上述服务描述；现有 canonical、图片地址和 Twitter 卡片类型保持不变。

- [ ] **步骤 2：加入真实且范围有限的结构化数据**

在 `</head>` 前加入：

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "Monster Design Studio",
  "url": "https://207515414.github.io/monster-design-studio-portfolio/",
  "image": "https://207515414.github.io/monster-design-studio-portfolio/assets/public/projects/riverfront-residence/04.webp",
  "description": "Remote CAD drafting, technical documentation and interior visualization support for overseas interior design studios, architects and fit-out contractors.",
  "email": "mailto:zhangzheng270@gmail.com",
  "telephone": "+86 190 3505 7372",
  "sameAs": [
    "https://www.facebook.com/people/Monster-Design/61590582893820/",
    "https://www.instagram.com/seol_nk97/",
    "https://www.linkedin.com/company/monster-studio-design/"
  ],
  "serviceType": [
    "CAD drafting",
    "Interior technical documentation",
    "Drawing development",
    "Interior visualization"
  ]
}
</script>
```

- [ ] **步骤 3：更新导航顺序**

导航使用以下顺序，并保留移动菜单结构：

```html
<a href="#capabilities">Services</a>
<a href="#drawings">Drawings</a>
<a href="#work">Visualization</a>
<a href="#process">Process</a>
<a href="#about">About</a>
<a href="#contact">Contact</a>
```

- [ ] **步骤 4：更新首屏文案和按钮**

```html
<p class="eyebrow">Remote Production Partner for Interior Project Teams</p>
<h1>Remote CAD drafting and visualization support for busy design teams.</h1>
<p class="hero-copy">
  Monster Design Studio helps overseas interior design studios, architects and fit-out contractors add flexible
  production capacity for technical drawings, documentation and presentation visuals.
</p>
<div class="hero-actions">
  <a class="button primary" href="#contact">Send a Project Brief</a>
  <a class="button secondary" href="#drawings">View Technical Drawings</a>
  <a class="button text-link" href="https://wa.me/8619035057372" target="_blank" rel="noreferrer">WhatsApp</a>
</div>
```

首屏标签改为 `CAD Drafting`、`Interior Elevations`、`Technical Documentation`、`Drawing Coordination`、`Interior Visualization`、`Paid Pilot Available`。

- [ ] **步骤 5：运行定位测试**

运行：

```text
py -3 -m unittest discover -s tests -p "test_*.py" -v
```

预期：首屏和结构化数据测试通过；服务顺序和不支持用词测试仍可能失败。

### 任务三：重排并重写服务、图纸、作品和合作流程

**文件：**

- 修改：`index.html:94-370`
- 测试：`tests/test_site.py`

- [ ] **步骤 1：将定位板块改成专业团队说明**

标题使用 `Production support that fits into your existing team.`，正文明确说明工作室补充远程产能，不接管客户关系，也不代表当地报批或专业签章能力。

- [ ] **步骤 2：将服务板块精简为三项并确定顺序**

第一项必须使用：

```html
<h3>CAD Drafting &amp; Technical Documentation</h3>
<ul>
  <li>Interior plans and drawing updates</li>
  <li>Interior elevations and details</li>
  <li>Construction-documentation support</li>
  <li>Drawing organization and coordination</li>
  <li>Production based on supplied project information</li>
</ul>
```

第二项使用 `Interior Visualization`，包含商业和酒店室内效果图、设计深化视觉、提案图片和客户沟通图片。第三项使用 `Design Presentation & FF&E Support`，包含材料方向、家具方向、情绪板和提案整理。

- [ ] **步骤 3：把 `#drawings` 移到 `#work` 之前**

图纸标题改为 `Technical drawing support for defined project scopes.`，说明公开图纸经过匿名处理，服务依据客户提供的信息开展，不代表当地工程认证或盖章。

- [ ] **步骤 4：把综合项目板块定位为可视化作品**

板块标题改为 `Visualization work for design development and client communication.`，保留现有筛选和 `projectGrid`，不修改类别值。

- [ ] **步骤 5：把行业板块改成三类合作场景**

三个卡片分别为：

- `Overflow Production Capacity`：项目高峰期补充明确范围的绘图和效果图产能。
- `Defined Remote Packages`：按已确认资料、节点、交付物和修改轮次执行。
- `Privacy-Conscious Collaboration`：公开案例匿名化，具体项目按保密要求处理。

- [ ] **步骤 6：重写工作室介绍和五步流程**

工作室介绍强调“作为客户现有团队的远程生产伙伴”。五步流程使用：

1. `Share Your Drawings & Brief`
2. `Scope, Schedule & Quotation`
3. `Start with a Paid Pilot When Appropriate`
4. `Production & Consolidated Review`
5. `Approved File Delivery`

页面中必须出现完整句子 `Start with a paid pilot when appropriate.`，以满足定位测试并避免承诺所有客户都必须试单。

- [ ] **步骤 7：重写询盘区**

标题使用 `Send us a project brief for a scope review.`，说明客户应提供项目类型、地点、面积、现有图纸、所需服务、文件格式、目标日期和预算范围。保留现有邮箱、WhatsApp 和社交链接；主按钮使用 `Send Your Project Brief`。

- [ ] **步骤 8：运行全部 Python 测试和 JavaScript 语法检查**

运行：

```text
py -3 -m unittest discover -s tests -p "test_*.py" -v
node --check script.js
node --check assets/data.js
```

预期：服务顺序、板块顺序、行动按钮、结构化数据、导航和现有资源检查通过；不支持用词测试可能继续因旧案例文字失败。

### 任务四：重写案例数据并清除不支持的宣传用词

**文件：**

- 修改：`assets/data.js:1-226`
- 测试：`tests/test_site.py`

- [ ] **步骤 1：调整五个效果图项目的销售角色**

使用以下标题：

- `Commercial Hotel Interior Visualization Support`
- `Luxury Residential Visualization Package`
- `Villa FF&E & Presentation Support`
- `Private Residence FF&E Presentation`
- `Workplace Interior & Furniture Presentation`

每个摘要说明其用于设计深化、提案或客户沟通。保留现有地点、状态、图片、尺寸和真实项目范围，不把概念图片描述为已建成项目。

- [ ] **步骤 2：调整三类技术图纸标题和边界**

使用以下标题：

- `Interior CAD Documentation Support`
- `Interior Elevation & Detail Development`
- `Electrical & Low-Voltage Drawing Coordination`

删除 `contractor-ready documentation`，改为 `detail communication for contractor review`；明确这些图纸是基于客户资料的匿名生产示例，不表示工程认证。

- [ ] **步骤 3：运行全部自动测试**

运行：

```text
py -3 -m unittest discover -s tests -p "test_*.py" -v
node --check script.js
node --check assets/data.js
```

预期：全部测试通过，两个 JavaScript 文件语法检查退出码为 0。

- [ ] **步骤 4：提交网站内容改造**

```text
git add index.html assets/data.js tests/test_site.py
git commit -m "Reposition site for B2B production support"
```

### 任务五：本地浏览器与无障碍验证

**文件：**

- 验证：`index.html`
- 条件修改：`styles.css`
- 条件修改：`script.js`

- [ ] **步骤 1：启动本地静态服务器**

运行：

```text
py -3 -m http.server 8080
```

预期：`http://127.0.0.1:8080/` 返回状态 200。

- [ ] **步骤 2：检查桌面端和移动端**

桌面使用约 1440×900，移动端使用约 390×844。检查首屏文字无溢出、导航可打开关闭、服务顺序正确、图纸位于效果图之前、项目弹窗可打开关闭和切换、WhatsApp 与邮箱链接正确。

- [ ] **步骤 3：检查键盘和 JavaScript 失败后的基本可用性**

使用 Tab、Enter 和 Escape 检查导航和弹窗；禁用 JavaScript 或直接检查 HTML，确认服务说明和联系方式仍可见。

- [ ] **步骤 4：仅在出现实际问题时做最小修复**

若长标题在移动端溢出，只调整现有断点内的字号或换行规则；若新结构导致选择器失效，只修改对应选择器。不得增加外部依赖、追踪代码或未经批准的新板块。

- [ ] **步骤 5：重新运行完整验证**

运行：

```text
py -3 -m unittest discover -s tests -p "test_*.py" -v
node --check script.js
node --check assets/data.js
git diff --check
```

预期：自动测试全部通过、JavaScript 语法正常、Git 差异无空白错误。

### 任务六：通过 GitHub 通道推送并核对线上版本

**文件：**

- 推送：`.agents/product-marketing.md`
- 推送：`docs/superpowers/specs/2026-07-11-b2b-positioning-design.md`
- 推送：`docs/superpowers/plans/2026-07-11-b2b-positioning-implementation.md`
- 推送：`tests/test_site.py`
- 推送：`index.html`
- 推送：`assets/data.js`
- 条件推送：`styles.css`
- 条件推送：`script.js`

- [ ] **步骤 1：重新获取 GitHub `main` 最新提交**

预期远端基线为审计时确认的 `e8f8433677e2917b32df07ddd2f4748dfe8f2163`；如果已变化，先比较差异，不能覆盖新改动。

- [ ] **步骤 2：使用 GitHub 通道写入批准和验证后的文件**

每个更新操作必须使用远端返回的当前文件 SHA；新增文件使用创建操作。提交信息清楚区分定位文档、测试和网站改造，不删除无关文件。

- [ ] **步骤 3：重新读取 GitHub 文件并核对内容**

检查 `index.html` 包含新 H1、第一主服务和结构化数据；检查 `assets/data.js` 包含八个新案例标题；检查测试和中文定位文档均已存在。

- [ ] **步骤 4：等待 GitHub Pages 更新并核对线上文件**

对 `index.html`、`assets/data.js`、`script.js` 和 `styles.css` 分别进行线上与批准版本的换行标准化比较。

预期：四个文本文件一致；线上首页显示新的 B2B 定位，现有图片、弹窗和联系方式正常。

- [ ] **步骤 5：提交最终汇报**

汇报 GitHub 提交、具体修改、测试结果、线上核对结果，以及仍未处理的公开 Git 历史素材风险。不得声称未验证的广告效果或客户增长。

