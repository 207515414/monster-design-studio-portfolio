# China Site Premium UI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the Chinese home page as a premium, responsive, conversion-led experience that is immediately understandable to homeowners as well as professional project teams.

**Architecture:** Keep `/zh/index.html` as the static entry point and retain the current Nginx routing contract. Use semantic HTML for content and conversion paths, CSS custom properties and media queries for the art direction and responsive layouts, and a small optional local JavaScript enhancement for scroll reveal and mobile consultation state. All base content remains available without JavaScript.

**Tech Stack:** Static HTML, CSS, vanilla JavaScript, local WebP/JPG assets, Python `unittest`, headless Chrome screenshot review.

---

## File structure

- Modify: `zh/index.html` — semantic sections, C-end and team pathways, local interaction hooks, metadata.
- Modify: `zh/zh.css` — premium visual system, desktop motion, mobile composition and reduced-motion fallback.
- Create: `zh/zh.js` — optional reveal and mobile consultation interactions; no external dependencies.
- Modify: `zh/contact/index.html` — C-end friendly WeChat consultation prompt and material checklist.
- Modify: `tests/test_seo_architecture.py` — regression checks for plain-language owner path, local interaction script and no-JavaScript consultation route.
- Modify: `README.md` — document the China-site responsive and motion verification command if needed.

### Task 1: Lock the C-end conversion contract

**Files:**
- Modify: `tests/test_seo_architecture.py`
- Test: `tests/test_seo_architecture.py`

- [ ] **Step 1: Write the failing test**

```python
def test_china_homepage_has_plain_language_owner_path_and_local_motion(self):
    page = (ROOT / "zh/index.html").read_text(encoding="utf-8")
    script = ROOT / "zh/zh.js"
    self.assertIn("让空间，在施工前就被看见", page)
    self.assertIn("我是业主", page)
    self.assertIn("户型图、现场照片或参考图片", page)
    self.assertIn("发资料，获取项目建议", page)
    self.assertIn('src="zh.js"', page)
    self.assertTrue(script.is_file(), script)
```

- [ ] **Step 2: Run the focused test to verify it fails**

Run: `py -3 -m unittest tests.test_seo_architecture.SeoArchitectureTests.test_china_homepage_has_plain_language_owner_path_and_local_motion -v`

Expected: FAIL because the upgraded owner-path language and `zh/zh.js` do not yet exist.

- [ ] **Step 3: Commit the red test**

```bash
git add tests/test_seo_architecture.py
git commit -m "test: define China-site owner conversion contract"
```

### Task 2: Rebuild the Chinese home-page information architecture

**Files:**
- Modify: `zh/index.html`
- Test: `tests/test_seo_architecture.py`

- [ ] **Step 1: Replace the hero with direct service and audience clarity**

Use this hero structure, preserving the existing local hero image and `/zh/contact/` route:

```html
<p class="eyebrow">MONSTER CG / SPATIAL VISUALIZATION</p>
<h1>让空间，<em>在施工前就被看见</em></h1>
<p class="hero-lede">图纸深化、高品质效果表现与三维动画。服务住宅、酒店与商业空间，让业主和项目团队在投入前把空间想清楚。</p>
<div class="hero-actions">
  <a class="button" href="#owner-path">我是业主，看看我的项目</a>
  <a class="text-button" href="#team-path">我是设计师 / 项目团队</a>
</div>
```

- [ ] **Step 2: Add the owner path before the team path**

Create an `id="owner-path"` section with this plain-language message and a contact route:

```html
<h2>还没有专业图纸，也可以先开始。</h2>
<p>户型图、现场照片或参考图片都可以。我们先帮你看清装修后空间的氛围和关键细节，再进入下一步沟通。</p>
<a class="button" href="/zh/contact/">发资料，获取项目建议</a>
```

- [ ] **Step 3: Add a distinct `id="team-path"` section**

```html
<h2>给设计与项目团队的清晰支持。</h2>
<p>图纸表达、提案效果图与动画内容，帮助团队把设计意图、空间节点和展示重点说清楚。</p>
<a class="text-button" href="/zh/contact/">咨询项目合作</a>
```

- [ ] **Step 4: Convert services into customer-result cards**

Use local assets only and use these concise results:

```html
<h3>图纸深化</h3><p>让施工要看的信息更清楚。</p>
<h3>空间效果表现</h3><p>装修和投入前，先看清空间会是什么样。</p>
<h3>三维动画</h3><p>把动线、氛围和空间故事讲明白。</p>
```

- [ ] **Step 5: Add visual proof labels and an owner-friendly process**

For each local visual, show a neutral label such as `住宅空间 / 效果表现` or `酒店与商业空间 / 氛围展示` and a `概念呈现` note. Replace abstract process wording with `发资料 → 说清楚想看的内容 → 制作与阶段确认 → 收到约定文件`.

- [ ] **Step 6: Run the focused test to verify it still fails**

Run: `py -3 -m unittest tests.test_seo_architecture.SeoArchitectureTests.test_china_homepage_has_plain_language_owner_path_and_local_motion -v`

Expected: FAIL because `zh/zh.js` is intentionally not present yet.

### Task 3: Implement premium visual system and motion enhancement

**Files:**
- Modify: `zh/zh.css`
- Create: `zh/zh.js`
- Modify: `zh/index.html`
- Test: `tests/test_seo_architecture.py`

- [ ] **Step 1: Build responsive CSS layers**

Add these component-level concerns to `zh/zh.css`:

```css
.hero { min-height: min(920px, 100svh); overflow: clip; }
.hero-media img { transform: scale(1.06); transition: transform 1.2s cubic-bezier(.2,.7,.2,1); }
.hero.is-visible .hero-media img { transform: scale(1); }
.reveal { opacity: 0; transform: translateY(28px); transition: opacity .7s ease, transform .7s ease; }
.reveal.is-visible { opacity: 1; transform: none; }
@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation-duration: .01ms !important; transition-duration: .01ms !important; } }
@media (max-width: 800px) { .hero { min-height: 760px; } .hero-actions { display: grid; } }
```

Complete the component styling with dark-green layers, warm-copper accents, image-led service cards, editorial grid spacing, a fixed mobile consultation control, and touch states equivalent to desktop hover states.

- [ ] **Step 2: Create the minimal optional motion script**

Create `zh/zh.js`:

```js
document.documentElement.classList.add("js");

const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const revealTargets = document.querySelectorAll(".reveal, .hero");

if (reducedMotion || !("IntersectionObserver" in window)) {
  revealTargets.forEach((element) => element.classList.add("is-visible"));
} else {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.16 });
  revealTargets.forEach((element) => observer.observe(element));
}
```

- [ ] **Step 3: Include the local deferred script**

```html
<script src="zh.js" defer></script>
```

- [ ] **Step 4: Run the focused test to verify it passes**

Run: `py -3 -m unittest tests.test_seo_architecture.SeoArchitectureTests.test_china_homepage_has_plain_language_owner_path_and_local_motion -v`

Expected: PASS.

- [ ] **Step 5: Commit the home-page and motion work**

```bash
git add zh/index.html zh/zh.css zh/zh.js tests/test_seo_architecture.py
git commit -m "feat: elevate China-site UI and owner conversion path"
```

### Task 4: Upgrade WeChat contact language for C-end enquiries

**Files:**
- Modify: `zh/contact/index.html`
- Modify: `tests/test_seo_architecture.py`
- Test: `tests/test_seo_architecture.py`

- [ ] **Step 1: Write the failing contact-language test**

```python
def test_china_contact_page_explains_what_an_owner_can_send(self):
    contact = (ROOT / "zh/contact/index.html").read_text(encoding="utf-8")
    self.assertIn("住宅 / 酒店 / 商业空间 / 团队合作", contact)
    self.assertIn("预计开始时间", contact)
```

- [ ] **Step 2: Run the focused test to verify it fails**

Run: `py -3 -m unittest tests.test_seo_architecture.SeoArchitectureTests.test_china_contact_page_explains_what_an_owner_can_send -v`

Expected: FAIL because the WeChat prompt does not yet contain the complete C-end intake guidance.

- [ ] **Step 3: Add the exact WeChat preparation prompt**

```html
<p>添加微信时请备注：住宅 / 酒店 / 商业空间 / 团队合作、所在城市和预计开始时间。</p>
<p>有户型图、现场照片、CAD 或参考图，直接发来即可；资料不完整也可以先沟通。</p>
```

- [ ] **Step 4: Run the focused test to verify it passes**

Run: `py -3 -m unittest tests.test_seo_architecture.SeoArchitectureTests.test_china_contact_page_explains_what_an_owner_can_send -v`

Expected: PASS.

- [ ] **Step 5: Commit the contact-path update**

```bash
git add zh/contact/index.html tests/test_seo_architecture.py
git commit -m "feat: clarify WeChat intake for China-site owners"
```

### Task 5: Run full verification and inspect both responsive layouts

**Files:**
- Verify: `zh/index.html`, `zh/zh.css`, `zh/zh.js`, `zh/contact/index.html`

- [ ] **Step 1: Run automated verification**

Run:

```bash
py -3 -m unittest discover -s tests -p 'test_*.py' -v
node --check zh/zh.js
node --check script.js
node --check assets/data.js
git diff --check
```

Expected: all tests pass, JavaScript syntax checks pass, and `git diff --check` produces no output.

- [ ] **Step 2: Generate and review desktop screenshot**

Run a local static server and capture `http://127.0.0.1:<port>/zh/` at `1440px` width. Confirm hero purpose, owner CTA, service cards, motion-ready layout, and WeChat conversion section are visible.

- [ ] **Step 3: Generate and review mobile screenshot**

Capture `http://127.0.0.1:<port>/zh/` at `390px` width. Confirm no clipped navigation, minimum 44px touch targets, readable Chinese line lengths, accessible CTA before a long scroll, and visible fixed consultation control.

- [ ] **Step 4: Commit verification-ready changes**

```bash
git status --short
git add zh tests/test_seo_architecture.py README.md
git commit -m "test: verify premium China-site experience"
```
