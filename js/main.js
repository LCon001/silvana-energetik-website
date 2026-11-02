(() => {
  "use strict";

  const header = document.getElementById("site-header");
  const heroLogo = document.getElementById("hero-logo");

  /* ---------- Kompakte Navigationsleiste, sobald das Hero-Logo aus dem Bild ist ---------- */
  if (header) {
    if (heroLogo && "IntersectionObserver" in window) {
      new IntersectionObserver(
        ([entry]) => header.classList.toggle("is-scrolled", !entry.isIntersecting),
        { rootMargin: "-64px 0px 0px 0px" }
      ).observe(heroLogo);
    } else {
      header.classList.add("is-scrolled");
    }
  }

  /* ---------- Menü-Overlay ---------- */
  const menu = document.getElementById("menu");
  const toggle = document.querySelector(".menu-toggle");
  const closeBtn = document.querySelector(".menu-close");

  const setMenu = (open) => {
    if (!menu || !toggle) return;
    menu.classList.toggle("is-open", open);
    menu.setAttribute("aria-hidden", String(!open));
    toggle.setAttribute("aria-expanded", String(open));
    document.body.classList.toggle("menu-open", open);
    (open ? menu.querySelector(".menu__nav a") : toggle).focus({ preventScroll: true });
  };

  toggle?.addEventListener("click", () => setMenu(true));
  closeBtn?.addEventListener("click", () => setMenu(false));
  menu?.querySelectorAll("a").forEach((link) => link.addEventListener("click", () => setMenu(false)));
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && menu?.classList.contains("is-open")) setMenu(false);
  });
  window.matchMedia("(min-width: 960px)").addEventListener("change", (e) => {
    if (e.matches && menu?.classList.contains("is-open")) setMenu(false);
  });

  /* ---------- Galerie: Punkte-Anzeige beim Wischen ---------- */
  const track = document.getElementById("gallery-track");
  const dots = document.getElementById("gallery-dots");
  if (track && dots) {
    const items = [...track.children];
    items.forEach(() => dots.appendChild(document.createElement("span")));
    const update = () => {
      const max = track.scrollWidth - track.clientWidth;
      const index = max > 0 ? Math.round((track.scrollLeft / max) * (items.length - 1)) : 0;
      [...dots.children].forEach((dot, i) => dot.classList.toggle("is-active", i === index));
    };
    track.addEventListener("scroll", update, { passive: true });
    update();
  }

  /* ---------- Bild-Großansicht ---------- */
  const lightbox = document.getElementById("lightbox");
  if (lightbox && typeof lightbox.showModal === "function") {
    const img = lightbox.querySelector("img");
    document.querySelectorAll(".gallery__item").forEach((item) => {
      item.addEventListener("click", () => {
        const thumb = item.querySelector("img");
        img.src = item.dataset.full;
        img.alt = thumb.alt;
        lightbox.showModal();
      });
    });
    lightbox.querySelector(".lightbox__close").addEventListener("click", () => lightbox.close());
    lightbox.addEventListener("click", (e) => {
      if (e.target === lightbox) lightbox.close();
    });
  }

  /* ---------- Sanftes Einblenden beim Scrollen ---------- */
  const reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        });
      },
      { rootMargin: "0px 0px -8% 0px" }
    );
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add("is-visible"));
  }

  const year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();
})();
