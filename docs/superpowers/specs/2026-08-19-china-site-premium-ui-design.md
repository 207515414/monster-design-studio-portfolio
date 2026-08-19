# China Site: Premium UI and C-End Clarity

## Objective

Make `/zh/` feel like a premium spatial-visualization studio within the first screen, while enabling a homeowner, hotel owner, or shop owner to understand the service without industry vocabulary.

## Positioning

Monster CG creates three practical project outputs: drawing detailing, spatial visualization, and 3D animation. The China site speaks to two clear paths:

- **Owners:** homes, villas, hotels, stores, and offices that need to see and confirm a space before construction or presentation.
- **Professional teams:** design studios and project teams that need clear drawings, proposal visuals, or animation support.

No scale, client, award, timetable, or construction claim may be invented.

## Experience direction

The site uses a cinematic dark-green and warm-copper art direction, oversized Chinese typography, original local visual assets, and restrained motion. The goal is a composed, high-end experience rather than decoration.

### Desktop

- Full-screen hero with layered reveal, image parallax, and an immediately visible service statement.
- Service cards use image-led hover states and structured output labels.
- Scroll-driven section reveals, a pinned capability sequence, and a visual case strip establish rhythm.
- Two audience paths are clear and visually distinct.

### Mobile

- The hero is re-composed for vertical reading; important service and consultation actions appear before a long scroll.
- Cards become tap-friendly stacked panels; hover-only interactions have an equivalent tap/state treatment.
- Motion honours `prefers-reduced-motion` and avoids a heavy JavaScript runtime.
- A fixed consultation control provides an immediate route to the WeChat contact page.

## Content architecture

1. **Hero — what we do, who it is for, and two paths**
   - Headline: “让空间，在施工前就被看见”
   - Plain service statement: drawing detailing, high-quality visual presentation, and 3D animation.
   - Primary owner CTA: “我是业主，看看我的项目”
   - Secondary team CTA: “我是设计师 / 项目团队”

2. **What you receive**
   - Drawing detailing: “让施工要看的信息更清楚。”
   - Visual presentation: “装修和投入前，先看清空间会是什么样。”
   - 3D animation: “把动线、氛围和空间故事讲明白。”

3. **Audience paths**
   - Owner language: send a layout, site photo, or reference image; use the output to confirm atmosphere and key decisions before communicating with the construction team.
   - Team language: provide presentation visuals, drawing communication, and animation outputs for active project work.

4. **Professional method**
   - Send available material → clarify the goal and deliverables → make and confirm at milestones → receive the agreed files.
   - The material checklist names layout plans, CAD, on-site photos, and reference images.

5. **Visual proof**
   - An image-first case strip labels each item by space type and the relevant service. It only uses original support images and labels them as concept presentation where required.

6. **WeChat conversion**
   - CTA: “发资料，获取项目建议”.
   - Contact page asks the visitor to add project type, city, existing material, and intended start time when contacting WeChat `z-787-00`.

## Interaction and resilience

- CSS provides the visual motion; JavaScript is optional enhancement only.
- All content and contact routes work when JavaScript is unavailable.
- Motion is disabled or reduced for `prefers-reduced-motion`.
- Existing Chinese IP routing and English cookie preference must remain unchanged.

## Verification

- Automated tests check the C-end plain-language message, the visible dual audience paths, contact CTA and local assets.
- Existing content, link, metadata, and Nginx tests continue to pass.
- Desktop and mobile screenshots are reviewed locally before publication.
