# Monster CG font assets

The public site self-hosts the font files in this directory. It does not request fonts from a third-party font service at runtime.

## Source and license

- Source family: Noto Sans and Noto Sans CJK SC, downloaded from the official Noto project distribution.
- License: SIL Open Font License 1.1. The complete, unmodified license is stored in `OFL-1.1.txt`.
- `noto-sans-latin-*.ttf`: Latin files used by the English site.
- `noto-sans-sc-*.ttf`: Simplified Chinese subsets used by `/zh/`.

The `Monster Noto Sans Latin` and `Monster Noto Sans SC` names are CSS family aliases only. Monster CG does not claim ownership of the Noto glyph designs or represent them as a newly created font.

## Delivery rules

- Font files are served from this site under `assets/fonts/`.
- CSS uses `font-display: swap`.
- The only fallback is the generic `sans-serif` family, not a named system font.
