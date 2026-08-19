# Global Type System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give the Chinese and English public sites a self-hosted, OFL-licensed sans-serif type system with no system-font dependency.

**Architecture:** Keep the Chinese subset files already added under `assets/fonts/`; add matching local Latin subsets for the English site. Define two explicit `@font-face` families in the CSS entry points and replace existing serif/system stacks with named local families plus generic `sans-serif` fallback.

**Tech Stack:** Static HTML, CSS `@font-face`, local TTF subsets, Python `unittest`, headless Chrome screenshots.

---

### Task 1: Document and test the type-source contract

**Files:**
- Create: `assets/fonts/README.md`
- Modify: `tests/test_seo_architecture.py`

- [ ] **Step 1: Write the failing tests**

```python
def test_public_css_uses_only_self_hosted_font_assets(self):
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    self.assertIn('url("assets/fonts/noto-sans-latin-400.ttf")', css)
    self.assertNotIn("Georgia", css)
    self.assertNotIn("Arial", css)
```

- [ ] **Step 2: Run the targeted test and verify it fails**

Run: `py -3 -m unittest tests.test_seo_architecture.SeoArchitectureTests.test_public_css_uses_only_self_hosted_font_assets -v`

Expected: FAIL because the English stylesheet still references Georgia and Arial.

- [ ] **Step 3: Add the auditable source note**

Create `assets/fonts/README.md` stating that the Chinese and Latin subsets are produced from Noto Sans, licensed under OFL-1.1, self-hosted, and accompanied by `OFL-1.1.txt`.

- [ ] **Step 4: Run the targeted test and commit**

Run: `py -3 -m unittest tests.test_seo_architecture -v`

Expected: PASS after Task 2 implementation.

### Task 2: Apply the local Latin and Chinese families

**Files:**
- Create: `assets/fonts/noto-sans-latin-400.ttf`
- Create: `assets/fonts/noto-sans-latin-500.ttf`
- Create: `assets/fonts/noto-sans-latin-600.ttf`
- Create: `assets/fonts/noto-sans-latin-700.ttf`
- Modify: `styles.css`
- Modify: `zh/zh.css`

- [ ] **Step 1: Produce local Latin subsets**

Request Noto Sans Latin subsets for the English site text at weights 400, 500, 600 and 700, then save them under `assets/fonts/`.

- [ ] **Step 2: Define local English font faces**

Add four `@font-face` declarations to `styles.css`, for example:

```css
@font-face {
  font-family: "Monster Noto Sans Latin";
  src: url("assets/fonts/noto-sans-latin-400.ttf") format("truetype");
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}
```

Set both `--sans` and `--serif` to `"Monster Noto Sans Latin", sans-serif`, then change Arabic-only rules to `sans-serif` without named system fonts.

- [ ] **Step 3: Keep Chinese rules local-only**

Keep `zh/zh.css` on `"Monster Noto Sans SC", sans-serif`; do not add a remote URL or a device-specific font fallback.

- [ ] **Step 4: Run tests and syntax checks**

Run: `py -3 -m unittest discover -s tests -p 'test_*.py' -v`

Run: `git diff --check`

Expected: all tests pass and no whitespace errors are reported.

### Task 3: Preview and prepare release

**Files:**
- Modify: `styles.css`
- Modify: `zh/zh.css`

- [ ] **Step 1: Capture the English and Chinese desktop previews**

Run the local static server and capture `index.html` and `zh/contact/index.html` at 1440 px wide with Chrome headless.

- [ ] **Step 2: Review title wrapping, body readability, and mobile fallback**

Confirm that neither page includes a remote font request and that headings remain readable without decorative serif letterforms.

- [ ] **Step 3: Commit the type system**

```bash
git add styles.css zh/zh.css assets/fonts tests/test_seo_architecture.py
git commit -m "feat: self-host the global type system"
```

- [ ] **Step 4: Hold deployment for visual approval**

Do not push the type-system commit until the user accepts the English and Chinese screenshots.
