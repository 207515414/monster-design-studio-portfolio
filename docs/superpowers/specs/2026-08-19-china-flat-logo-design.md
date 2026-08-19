# China Site Flat Logo Design

## Decision

Monster CG keeps the existing global logo asset unchanged for the English and Arabic entry points. The China entry point uses a dedicated black-and-white flat derivative of the same `M` silhouette.

## Scope

- Global assets remain `assets/brand/logo-mark.svg` and are not edited.
- The China-only asset is a new SVG stored under `assets/zh/`.
- The new SVG preserves the original `M` proportions and recognizability.
- Its rendering is monochrome only: black and white, no blue, gradients, shadows, outlines, or 3D effects.
- China homepage, China contact page, China privacy page, and the China favicon use the China-only SVG.
- English and Arabic headers, footers, and favicons continue to use the current global asset.

## Visual Rules

- On dark China-site header backgrounds, render the mark white.
- On light China-site surfaces and browser UI, render the mark black.
- The mark must remain legible at 24 px, 28 px, and 32 px square sizes.
- Text wordmarks remain unchanged; only the square icon differs by locale.

## Validation

- Confirm the global logo file is byte-for-byte unchanged.
- Confirm `/zh/`, `/zh/contact/`, and `/zh/privacy-policy/` reference the China-only asset.
- Confirm English and Arabic entry pages still reference the global asset.
- Capture desktop and mobile header previews before publishing.
