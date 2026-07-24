# Monster CG Lead Form Design

## Goal

Capture qualified project briefs without compromising the editorial, portfolio-led tone of the Monster CG homepage.

## Chosen approach

Use Formspree as the form-processing service. It provides a hosted, password-protected submission dashboard and sends new-submission notifications to `zhangzheng270@gmail.com`. The website will not store customer submissions on the VPS.

## Visitor experience

- The homepage keeps its existing `Send a Project Brief` call to action.
- A compact, dismissible project-brief form opens only after a visitor requests it; there is no automatic popup.
- Required fields: work email, required service, project brief.
- Optional fields: contact name, company, target date, WhatsApp, and file link. The initial version does not accept direct file uploads.
- Successful submission shows a clear on-page confirmation and offers WhatsApp as an alternative contact channel.

## Data and privacy

- Formspree receives the submitted data and sends a notification to the owner Gmail address.
- The form includes this statement with a link to the existing privacy policy: “We use your details only to respond to your inquiry and manage your project. We do not sell your information. See our Privacy Policy.”
- No claim that data is never processed by a third-party provider will be made.

## Technical boundaries

- The Formspree endpoint is supplied by the owner after creating a Formspree form; it must not be guessed or committed as a placeholder that makes the live form appear functional.
- Add a honeypot and Formspree-supported anti-spam controls where available.
- Preserve a no-JavaScript fallback to email and WhatsApp.
- Track form-open and successful-submit events through the existing `data-track` convention; do not transmit analytics until an analytics property is configured.

## Verification

- Validate required fields and keyboard-close behavior for the dialog.
- Submit a test lead to verify both the Formspree dashboard and Gmail notification.
- Confirm the form does not submit while the Formspree endpoint is absent.
- Re-run static link and page tests before release.
