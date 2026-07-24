const projects = Array.isArray(window.PORTFOLIO_PROJECTS) ? window.PORTFOLIO_PROJECTS : [];
const drawingSets = Array.isArray(window.CONSTRUCTION_SETS) ? window.CONSTRUCTION_SETS : [];

const grid = document.querySelector("#projectGrid");
const drawingGrid = document.querySelector("#drawingGrid");
const dialog = document.querySelector("#projectDialog");
const dialogTitle = document.querySelector("#dialogTitle");
const dialogType = document.querySelector("#dialogType");
const dialogSummary = document.querySelector("#dialogSummary");
const dialogMeta = document.querySelector("#dialogMeta");
const dialogTags = document.querySelector("#dialogTags");
const dialogNote = document.querySelector("#dialogNote");
const viewerImage = document.querySelector("#viewerImage");
const thumbRail = document.querySelector("#thumbRail");
const closeButton = document.querySelector(".dialog-close");
const nextProjectButton = document.querySelector("#nextProjectButton");
const navToggle = document.querySelector(".nav-toggle");
const primaryNav = document.querySelector("#primaryNav");

let activeCollection = [];
let activeIndex = 0;
let lastTrigger = null;

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function appendList(parent, items) {
  const list = el("ul");
  items.forEach((item) => {
    const li = el("li", "", item);
    list.appendChild(li);
  });
  parent.appendChild(list);
}

function setImage(image, slide, fallbackAlt) {
  image.src = slide.image;
  image.alt = fallbackAlt;
  if (slide.width) image.width = slide.width;
  if (slide.height) image.height = slide.height;
}

function renderProjectCards() {
  if (!grid) return;
  grid.textContent = "";

  projects.forEach((project, index) => {
    const card = el("button", "project-card reveal");
    card.type = "button";
    card.dataset.category = project.category || "Other";
    card.setAttribute("aria-label", `Open project: ${project.title}`);
    card.style.transitionDelay = `${Math.min(index * 80, 320)}ms`;
    if (index === 0) card.classList.add("project-card-featured");

    const media = el("span", "project-media");
    const image = document.createElement("img");
    image.src = project.cover;
    image.alt = `${project.title} project preview`;
    image.width = project.slides?.[0]?.width || 1500;
    image.height = project.slides?.[0]?.height || 1000;
    image.loading = index === 0 ? "eager" : "lazy";
    media.appendChild(image);

    const body = el("span", "project-body");
    body.appendChild(el("span", "project-index", String(index + 1).padStart(2, "0")));
    body.appendChild(el("span", "section-label", project.projectType || project.type || "Project"));
    body.appendChild(el("strong", "project-title", project.title));
    body.appendChild(el("span", "project-summary", project.summary));

    const meta = el("span", "project-meta");
    [project.location, project.status, project.scope].filter(Boolean).forEach((item) => {
      meta.appendChild(el("span", "", item));
    });
    body.appendChild(meta);

    card.appendChild(media);
    card.appendChild(body);
    card.addEventListener("click", () => openItem(projects, index, card));
    grid.appendChild(card);
  });

  observeReveals();
}

function renderDrawingCards() {
  if (!drawingGrid) return;
  drawingGrid.textContent = "";

  drawingSets.forEach((set, index) => {
    const card = el("button", "drawing-card reveal");
    card.type = "button";
    card.setAttribute("aria-label", `Open drawing set: ${set.title}`);
    card.style.transitionDelay = `${Math.min(index * 80, 240)}ms`;

    const media = el("span", "drawing-media");
    const image = document.createElement("img");
    image.src = set.cover;
    image.alt = `${set.title} anonymized drawing preview`;
    image.width = set.slides?.[0]?.width || 1600;
    image.height = set.slides?.[0]?.height || 1236;
    image.loading = "lazy";
    media.appendChild(image);

    const body = el("span", "drawing-body");
    body.appendChild(el("span", "section-label", set.scope));
    body.appendChild(el("strong", "drawing-title", set.title));
    body.appendChild(el("span", "drawing-summary", set.summary));

    const meta = el("span", "drawing-meta");
    meta.appendChild(el("span", "", `${set.sheetCount} sheets`));
    meta.appendChild(el("span", "", `${set.previewCount || set.slides.length} public previews`));
    meta.appendChild(el("span", "", set.status));
    body.appendChild(meta);

    card.appendChild(media);
    card.appendChild(body);
    card.addEventListener("click", () => openItem(drawingSets, index, card));
    drawingGrid.appendChild(card);
  });

  observeReveals();
}

function fillMeta(item) {
  dialogMeta.textContent = "";
  const rows = [
    ["Location", item.location],
    ["Project Type", item.projectType || item.type],
    ["Status", item.status],
    ["Scope of Work", item.scope],
  ];
  if (item.sheetCount) rows.push(["Drawing Set", `${item.sheetCount} sheets / ${item.previewCount || item.slides.length} public preview pages`]);

  rows.forEach(([label, value]) => {
    if (!value) return;
    const dt = el("dt", "", label);
    const dd = el("dd", "", value);
    dialogMeta.appendChild(dt);
    dialogMeta.appendChild(dd);
  });
}

function fillTags(item) {
  dialogTags.textContent = "";
  const tags = item.tags || item.services || [];
  tags.forEach((tag) => {
    dialogTags.appendChild(el("span", "", tag));
  });
}

function selectSlide(item, slide, button) {
  if (!slide) return;
  setImage(viewerImage, slide, `${item.title} preview image`);
  thumbRail.querySelectorAll("button").forEach((thumb) => {
    thumb.classList.remove("active");
    thumb.removeAttribute("aria-current");
  });
  button.classList.add("active");
  button.setAttribute("aria-current", "true");
}

function fillThumbnails(item) {
  thumbRail.textContent = "";
  const slides = item.slides || [];
  slides.forEach((slide, index) => {
    const button = el("button");
    button.type = "button";
    button.setAttribute("aria-label", `View image ${index + 1} of ${slides.length}`);
    const image = document.createElement("img");
    image.src = slide.thumb || slide.image;
    image.alt = "";
    image.width = 240;
    image.height = 156;
    image.loading = "lazy";
    button.appendChild(image);
    button.addEventListener("click", () => selectSlide(item, slide, button));
    thumbRail.appendChild(button);
    if (index === 0) selectSlide(item, slide, button);
  });
}

function openItem(collection, index, trigger) {
  const item = collection[index];
  if (!item || !dialog) return;

  activeCollection = collection;
  activeIndex = index;
  lastTrigger = trigger || document.activeElement;

  dialogTitle.textContent = item.title;
  dialogType.textContent = item.category === "Technical" ? "Technical Documentation" : item.projectType || item.type || "Project";
  dialogSummary.textContent = item.description || item.summary || "";
  fillMeta(item);
  fillTags(item);
  dialogNote.textContent = item.technicalNote || "Selected images are shown for portfolio review. Complete source files and confidential proposal materials are not published.";
  fillThumbnails(item);
  nextProjectButton.textContent = item.category === "Technical" ? "Next Drawing Set" : "Next Project";

  document.body.classList.add("dialog-open");
  if (typeof dialog.showModal === "function") {
    dialog.showModal();
  } else {
    dialog.setAttribute("open", "");
    dialog.classList.add("fallback-open");
  }
  closeButton.focus();
}

function closeProject() {
  if (!dialog) return;
  if (typeof dialog.close === "function" && dialog.open) {
    dialog.close();
  } else {
    dialog.removeAttribute("open");
    dialog.classList.remove("fallback-open");
    document.body.classList.remove("dialog-open");
    if (lastTrigger && typeof lastTrigger.focus === "function") lastTrigger.focus();
  }
}

function openNextItem() {
  if (!activeCollection.length) return;
  const nextIndex = (activeIndex + 1) % activeCollection.length;
  openItem(activeCollection, nextIndex, lastTrigger);
}

function bindFilters() {
  document.querySelectorAll(".filter").forEach((button) => {
    button.addEventListener("click", () => {
      const filter = button.dataset.filter;
      document.querySelectorAll(".filter").forEach((item) => item.classList.remove("active"));
      button.classList.add("active");
      document.querySelectorAll(".project-card").forEach((card) => {
        card.hidden = filter !== "all" && card.dataset.category !== filter;
      });
    });
  });
}

function closeMobileNav() {
  if (!navToggle || !primaryNav) return;
  navToggle.setAttribute("aria-expanded", "false");
  document.body.classList.remove("nav-open");
}

function bindMobileNav() {
  if (!navToggle || !primaryNav) return;
  navToggle.addEventListener("click", () => {
    const isOpen = navToggle.getAttribute("aria-expanded") === "true";
    navToggle.setAttribute("aria-expanded", String(!isOpen));
    document.body.classList.toggle("nav-open", !isOpen);
  });
  primaryNav.querySelectorAll("a").forEach((link) => link.addEventListener("click", closeMobileNav));
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeMobileNav();
  });
  window.addEventListener("resize", () => {
    if (window.innerWidth > 980) closeMobileNav();
  });
}

function observeReveals() {
  const reveals = document.querySelectorAll(".reveal:not(.visible)");
  if (!("IntersectionObserver" in window)) {
    reveals.forEach((item) => item.classList.add("visible"));
    return;
  }
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12 },
  );
  reveals.forEach((item) => observer.observe(item));
}

closeButton?.addEventListener("click", closeProject);
nextProjectButton?.addEventListener("click", openNextItem);
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && dialog?.open) {
    event.preventDefault();
    closeProject();
  }
});
dialog?.addEventListener("click", (event) => {
  if (event.target === dialog) closeProject();
});
dialog?.addEventListener("close", () => {
  dialog.classList.remove("fallback-open");
  document.body.classList.remove("dialog-open");
  if (lastTrigger && typeof lastTrigger.focus === "function") lastTrigger.focus();
});
dialog?.querySelector('a[href="#contact"]')?.addEventListener("click", (event) => {
  event.preventDefault();
  closeProject();
  window.location.hash = "contact";
});

renderProjectCards();
renderDrawingCards();
bindFilters();
bindMobileNav();
observeReveals();

const projectBriefDialog = document.querySelector("#projectBriefDialog");
const projectBriefForm = document.querySelector("#projectBriefForm");
const projectBriefStatus = projectBriefForm?.querySelector(".lead-status");
const projectBriefSubmit = projectBriefForm?.querySelector('button[type="submit"]');

function openProjectBrief(event) {
  event.preventDefault();
  if (typeof projectBriefDialog?.showModal === "function") projectBriefDialog.showModal();
  else projectBriefDialog?.setAttribute("open", "");
}

document.querySelectorAll("[data-open-project-brief]").forEach((link) => link.addEventListener("click", openProjectBrief));
projectBriefDialog?.querySelector(".lead-dialog-close")?.addEventListener("click", () => projectBriefDialog.close());
projectBriefDialog?.addEventListener("click", (event) => { if (event.target === projectBriefDialog) projectBriefDialog.close(); });
projectBriefForm?.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!projectBriefForm.reportValidity()) return;
  const payload = Object.fromEntries(new FormData(projectBriefForm).entries());
  projectBriefStatus.textContent = "Sending your project brief…";
  projectBriefStatus.classList.remove("success");
  projectBriefSubmit.disabled = true;
  try {
    const response = await fetch("/api/leads", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "We could not send your brief.");
    projectBriefForm.reset();
    projectBriefStatus.textContent = "Thank you. Your project brief has been received.";
    projectBriefStatus.classList.add("success");
  } catch (error) {
    projectBriefStatus.textContent = `${error.message} Please email or WhatsApp us instead.`;
  } finally {
    projectBriefSubmit.disabled = false;
  }
});

document.querySelectorAll("[data-track]").forEach((link) => {
  link.addEventListener("click", () => {
    document.documentElement.dataset.lastCta = link.dataset.track;
  });
});

