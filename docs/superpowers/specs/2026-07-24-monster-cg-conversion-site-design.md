# Monster CG Conversion-Focused Website Design

## Goal

Rebuild Monster CG as an English-first, conversion-focused B2B website for architectural visualization and CAD production support. The site must attract qualified organic-search traffic and project inquiries from the United States, Canada, and the UAE while keeping all company claims truthful.

## Audience and positioning

Primary audience:

- Architects and interior design studios.
- Real-estate developers and hospitality teams.
- Fit-out contractors.

Positioning:

> Architectural Visualization & CAD Production Partner for Global Design Teams.

Monster CG provides remote architectural visualization, 3D interior/exterior rendering, commercial/hospitality visualization, CAD drafting, and interior elevation/shop-drawing support. It must not claim licensed architectural, engineering, permit, stamping, BIM, MEP, structural, animation, VR, or other unsupported services.

## Trust policy

The design may convey a mature, reliable production partner through professional visual direction, clear scope, delivery workflow, file requirements, confidentiality language, and an optional paid-pilot offer. It must not invent team size, founding date, project count, client logos, testimonials, awards, local offices, turnaround guarantees, savings figures, or software compatibility claims.

## Homepage architecture

The homepage is a conversion page, not a full portfolio.

1. **Immersive hero**
   - Original large-format architectural image.
   - H1: `Architectural Visualization & 3D Rendering for Global Design Teams`.
   - Supporting text naturally references architectural visualization services, 3D rendering services, and CAD production support.
   - Primary CTA: `Send a Project Brief`.
   - Secondary CTA: `Explore Capabilities`.

2. **Audience pathways**
   - Cards for Architects & Interior Studios, Developers & Hospitality, and Fit-out Contractors.
   - Each card explains a real workflow problem and links to an industry page.

3. **Capability split**
   - Architectural Visualization.
   - CAD Production Support.
   - Each links to a dedicated service hub and supporting service pages.

4. **Production workflow and assurance**
   - Project inputs, scope confirmation, production, consolidated review, final delivery.
   - Include confidentiality and paid-pilot language without unsupported guarantees.

5. **Selected work**
   - Four to six real portfolio previews only.
   - Link to the separate portfolio rather than building a full image wall on the homepage.

6. **Inquiry conversion block**
   - State the useful inputs: plans, elevations, models, reference images, requested deliverables, and target date.
   - Provide Email and WhatsApp; a future form can be tracked when analytics is added.

7. **Footer**
   - Contact details, language selector, and Privacy Policy.
   - The Privacy Policy content remains consistent with the existing policy.

## Visual direction

- Original editorial gallery aesthetic: deep graphite, warm off-white, restrained copper accent, generous whitespace, fine navigation typography, and image-led sections.
- Draw inspiration only from the high-level visual principles seen on architectural-visualization competitors: large images, limited copy over images, and strong portfolio rhythm. Do not copy their layout, source code, text, logos, or assets.
- Use real Monster CG portfolio images for case-study evidence.
- Generate a small set of clearly non-project, original support imagery for hero/banner composition, production-workflow backgrounds, drawing-detail contexts, and visual transitions. Do not present generated images as client projects.

## Portfolio boundary

Portfolio remains a separate experience. It owns project browsing and project detail pages. The homepage links to selected work only and should never duplicate the full portfolio grid.

## SEO strategy

### Language and regional structure

- English is the default locale at `/`.
- UAE Arabic pages live at `/ar-ae/`.
- A visible `EN / العربية` selector links to the equivalent page.
- Browser language or timezone may show a non-blocking Arabic-language suggestion. The site must not automatically redirect users by timezone, IP, or browser language.
- Each equivalent pair uses self-canonicals and reciprocal `hreflang="en"`, `hreflang="ar-AE"`, and `x-default` annotations where appropriate.

### Keyword ownership

| Page or cluster | Primary commercial topic |
| --- | --- |
| Homepage | architectural visualization services |
| Services hub | architectural visualization and CAD production support |
| Interior-rendering page | 3D interior rendering services |
| Exterior-rendering page | 3D exterior rendering services |
| Commercial/hospitality page | commercial rendering services / hospitality rendering services |
| CAD drafting page | outsource CAD drafting services |
| Elevation/shop-drawing page | shop drawing services outsourcing / interior elevation drafting |
| Architect industry page | 3D rendering services for architects |
| Blog and FAQ | rendering cost factors, project-file requirements, visualization briefs, paid-pilot workflow |
| UAE Arabic cluster | Arabic UAE equivalents of the supported visualization and CAD-production topics; no false local-office claim |

Avoid city-doorway pages, keyword stuffing, and unsupported local-service claims. Country references must describe remote availability for a market, not a physical presence.

## Measurement

Google Search Console is the initial source of truth. Before launch, capture baseline clicks, impressions, average position, indexed pages, and current query/page performance. Review the same measures monthly, with separate tracking for priority service pages.

Add GA4 after the redesign to measure:

- Primary and secondary CTA clicks.
- Email clicks.
- WhatsApp clicks.
- Contact-form starts and submissions, if a form is introduced.
- Language-switch usage.

Success is measured by qualified organic impressions and clicks first, then inquiry actions. No traffic or ranking outcome is guaranteed.

## Technical and quality requirements

- Preserve production HTTPS, canonical non-www domain, real contact methods, robots, sitemap, and privacy policy.
- Maintain a static, crawlable architecture compatible with Nginx and the current VPS deployment.
- Retain responsive behavior, accessible navigation, descriptive image alt text, self-canonical URLs, unique title tags, unique descriptions, and one H1 per indexable page.
- Keep generated support images distinct from project work.
- Extend automated tests before implementation to verify the new homepage conversion links, privacy-policy link, language links, locale metadata, and keyword ownership.

## Out of scope

- Claiming unverified capability or company proof.
- Copying competitor code, layouts, images, copy, or trademarks.
- Launching paid advertising.
- Creating a non-English locale beyond UAE Arabic.
