# China Flat Logo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a China-only black-and-white flat rendering of the established Monster CG M mark without changing global-logo assets.

**Architecture:** A new SVG in `assets/zh/` retains the original M path and rounded-square proportion but removes blue and gray guide lines. Only Chinese documents use it; English and Arabic continue using the global asset.

**Tech Stack:** Static HTML, SVG, Python unittest, Chrome screenshots.

---

### Task 1: Add the locale-owned mark and test its boundary

**Files:** Create `assets/zh/logo-mark-flat.svg`; modify `tests/test_seo_architecture.py`, `zh/index.html`, `zh/contact/index.html`, and `zh/privacy-policy/index.html`.

- [ ] Write a failing test that requires the China-only SVG, rejects `#0071e3` and `#8e8e93` within it, confirms the three Chinese pages reference it, and confirms English and Arabic still reference `assets/brand/logo-mark.svg`.
- [ ] Create a 512-square SVG with a white rounded background and this unchanged M path filled `#101514`: `M132 354V158h48l76 96 76-96h48v196h-50V240l-58 74h-32l-58-74v114z`.
- [ ] Replace only Chinese favicons and header icons with the new asset.
- [ ] Run `python -m unittest discover -s tests -v` and `git diff --exit-code -- assets/brand/logo-mark.svg`; commit only the passing change.

### Task 2: Validate real usage before publishing

**Files:** Verify `zh/index.html` and `zh/contact/index.html`.

- [ ] Capture desktop and mobile local screenshots of the Chinese homepage and confirm the 28 px icon is sharp with no layout movement.
- [ ] Present the screenshots and wait for user approval; do not push before approval.

### Task 3: Release after visual approval

**Files:** Verify the reviewed commit.

- [ ] Push the reviewed commit to GitHub `main`.
- [ ] Provide the established Alibaba Cloud `git pull --ff-only origin main` command.
- [ ] Verify public `/zh/`, `/zh/contact/`, and `/zh/privacy-policy/` return 200 and reference `logo-mark-flat.svg` after the server pull.
