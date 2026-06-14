const projects = window.PORTFOLIO_PROJECTS || [];
const grid = document.querySelector("#projectGrid");
const heroImage = document.querySelector("#heroImage");
const dialog = document.querySelector("#projectDialog");
const dialogTitle = document.querySelector("#dialogTitle");
const dialogType = document.querySelector("#dialogType");
const dialogSummary = document.querySelector("#dialogSummary");
const dialogTags = document.querySelector("#dialogTags");
const viewerImage = document.querySelector("#viewerImage");
const thumbRail = document.querySelector("#thumbRail");
const closeButton = document.querySelector(".dialog-close");

function projectCategory(project) {
  const text = `${project.title} ${project.type}`.toLowerCase();
  if (text.includes("office")) return "Office";
  if (text.includes("villa")) return "Villa";
  return "Residential";
}

function renderProjects() {
  grid.innerHTML = "";
  projects.forEach((project, index) => {
    const card = document.createElement("article");
    card.className = "project-card reveal";
    card.dataset.category = projectCategory(project);
    card.tabIndex = 0;
    card.setAttribute("role", "button");
    card.setAttribute("aria-label", `Open ${project.title}`);
    card.style.transitionDelay = `${Math.min(index * 90, 360)}ms`;
    card.innerHTML = `
      <div class="project-media">
        <img src="${project.cover}" alt="${project.title}" loading="lazy">
      </div>
      <div class="project-body">
        <div>
          <p class="section-label">${project.type}</p>
          <h3>${project.title}</h3>
        </div>
        <span class="project-count">${project.slides.length} views</span>
        <p>${project.summary}</p>
      </div>
    `;
    card.addEventListener("click", () => openProject(project));
    card.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        openProject(project);
      }
    });
    grid.appendChild(card);
  });
  observeReveals();
}

function openProject(project) {
  dialogTitle.textContent = project.title;
  dialogType.textContent = `${project.type} · ${project.location}`;
  dialogSummary.textContent = project.summary;
  dialogTags.innerHTML = project.services.map((service) => `<span>${service}</span>`).join("");
  thumbRail.innerHTML = "";

  function selectSlide(slide, button) {
    viewerImage.src = slide.image;
    viewerImage.alt = project.title;
    thumbRail.querySelectorAll("button").forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
  }

  project.slides.forEach((slide, index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.setAttribute("aria-label", `View image ${index + 1}`);
    button.innerHTML = `<img src="${slide.thumb}" alt="">`;
    button.addEventListener("click", () => selectSlide(slide, button));
    thumbRail.appendChild(button);
    if (index === 0) {
      selectSlide(slide, button);
    }
  });

  document.body.classList.add("dialog-open");
  if (typeof dialog.showModal === "function") {
    dialog.showModal();
  } else {
    dialog.setAttribute("open", "");
    dialog.classList.add("fallback-open");
  }
}

function closeProject() {
  if (typeof dialog.close === "function") {
    dialog.close();
  } else {
    dialog.removeAttribute("open");
  }
  dialog.classList.remove("fallback-open");
  document.body.classList.remove("dialog-open");
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

function observeReveals() {
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
  document.querySelectorAll(".reveal:not(.visible)").forEach((item) => observer.observe(item));
}

function initHero() {
  const heroProject = projects.find((project) => project.id === "shanghai-duplex") || projects[0];
  if (!heroProject) return;
  heroImage.src = heroProject.cover;
}

closeButton.addEventListener("click", closeProject);
dialog.addEventListener("click", (event) => {
  if (event.target === dialog) closeProject();
});
dialog.addEventListener("cancel", () => {
  dialog.classList.remove("fallback-open");
  document.body.classList.remove("dialog-open");
});

initHero();
renderProjects();
bindFilters();
observeReveals();
