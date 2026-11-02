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

  /* ---------- Galerie-Karussell: Pfeile, Punkte, langsames Auto-Blättern ---------- */
  const carousel = document.getElementById("gallery");
  const track = document.getElementById("gallery-track");
  const dots = document.getElementById("gallery-dots");
  if (carousel && track && dots) {
    const AUTOPLAY_MS = 4500;
    const items = [...track.children];
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
    let stops = [];
    let timer = null;
    let paused = false;
    let inView = false;

    const maxScroll = () => track.scrollWidth - track.clientWidth;
    const padLeft = () => parseFloat(getComputedStyle(track).paddingLeft) || 0;

    // Scroll-Positionen, an denen ein Bild links einrastet (die letzten Bilder teilen sich das Ende)
    const measure = () => {
      const max = maxScroll();
      const positions = items.map((item) => Math.min(item.offsetLeft - padLeft(), max));
      stops = positions.filter((pos, i) => i === 0 || pos - positions[i - 1] > 2);
      dots.replaceChildren(
        ...stops.map((_, i) => {
          const dot = document.createElement("button");
          dot.type = "button";
          dot.setAttribute("aria-label", `Bild ${i + 1} von ${stops.length}`);
          dot.addEventListener("click", () => {
            goTo(i);
            restart();
          });
          return dot;
        })
      );
      update();
    };

    const currentIndex = () => {
      const x = track.scrollLeft;
      let best = 0;
      stops.forEach((pos, i) => {
        if (Math.abs(pos - x) < Math.abs(stops[best] - x)) best = i;
      });
      return best;
    };

    const goTo = (i) => {
      const index = (i + stops.length) % stops.length;
      track.scrollTo({ left: stops[index], behavior: reducedMotion.matches ? "auto" : "smooth" });
    };

    const update = () => {
      const index = currentIndex();
      [...dots.children].forEach((dot, i) => {
        dot.classList.toggle("is-active", i === index);
        dot.setAttribute("aria-current", i === index ? "true" : "false");
      });
    };

    const stop = () => {
      clearInterval(timer);
      timer = null;
    };
    const start = () => {
      stop();
      if (reducedMotion.matches || paused || !inView || document.hidden || stops.length < 2) return;
      timer = setInterval(() => goTo(currentIndex() + 1), AUTOPLAY_MS);
    };
    const restart = () => start();

    carousel.querySelector(".gallery__nav--prev").addEventListener("click", () => {
      goTo(currentIndex() - 1);
      restart();
    });
    carousel.querySelector(".gallery__nav--next").addEventListener("click", () => {
      goTo(currentIndex() + 1);
      restart();
    });

    let scrollTick;
    track.addEventListener("scroll", () => {
      cancelAnimationFrame(scrollTick);
      scrollTick = requestAnimationFrame(update);
    }, { passive: true });

    const pause = () => {
      paused = true;
      stop();
    };
    const resume = () => {
      paused = false;
      start();
    };
    carousel.addEventListener("pointerenter", pause);
    carousel.addEventListener("pointerleave", resume);
    carousel.addEventListener("focusin", pause);
    carousel.addEventListener("focusout", resume);
    track.addEventListener("touchstart", pause, { passive: true });
    track.addEventListener("touchend", () => setTimeout(resume, AUTOPLAY_MS), { passive: true });
    document.addEventListener("visibilitychange", start);

    if ("IntersectionObserver" in window) {
      new IntersectionObserver(([entry]) => {
        inView = entry.isIntersecting;
        start();
      }, { threshold: 0.35 }).observe(carousel);
    } else {
      inView = true;
    }

    let resizeTimer;
    window.addEventListener("resize", () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(measure, 150);
    });
    measure();
    start();
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
