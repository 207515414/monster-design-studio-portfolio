# Monster Global Type System

## Objective

Use a consistent, readable and auditable type system for the Chinese and English public sites without relying on a visitor's installed fonts or a third-party font CDN.

## Licensing decision

- Base font: Noto Sans, including the Simplified Chinese CJK variant and Latin glyphs required by the English site.
- License: SIL Open Font License 1.1 (OFL-1.1).
- Distribution: self-host only. The site will not request fonts from Google Fonts, Adobe Fonts or another font service at runtime.
- Evidence: commit the exact font binaries used, the unmodified OFL-1.1 license text, and a source note in `assets/fonts/README.md`.
- Naming: CSS may use a Monster-specific family alias as a technical selector, but the site must not represent Noto glyphs as an original Monster typeface.

## Visual rules

- Chinese and English use the same sans-serif family structure.
- Body text: 400 weight for relaxed, highly legible reading.
- Navigation, labels and buttons: 600 weight, with restrained tracking for scanability.
- Display headings: 600 weight, not 700+; use more line-height and less negative letter spacing than the current editorial serif treatment.
- Remove Georgia, Times New Roman, Arial, Helvetica, PingFang SC, Microsoft YaHei, Songti SC, STSong and Tahoma from the public-site font stacks.
- The Arabic locale is not restyled in this scope; it retains a safe generic sans-serif fallback until an Arabic font with its own documented license is selected.

## Assets and loading

- Chinese pages load only the small Chinese subsets needed by the Chinese pages, in weights 400, 500, 600 and 700.
- English pages load self-hosted Latin subsets in weights 400, 500, 600 and 700.
- All `@font-face` rules use `font-display: swap` and explicit weight declarations.
- Missing glyphs fall back to the browser's generic `sans-serif`, preserving legibility without pretending that a system-specific font is part of the design.

## Verification

- Automated tests assert that Chinese and English public CSS reference only local font URLs and that `assets/fonts/OFL-1.1.txt` exists.
- Verify no CSS references Google, Adobe, or a remote font URL.
- Review desktop and mobile screenshots for both language entry points.
- Keep the font source and subset procedure documented so a future update is reproducible.
