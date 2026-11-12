const menuToggle = document.querySelector(".menu-toggle");
const mobileNav = document.getElementById("mobile-nav");

if (menuToggle && mobileNav) {
  const setMenu = (open) => {
    mobileNav.hidden = !open;
    menuToggle.setAttribute("aria-expanded", String(open));
    menuToggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  };

  menuToggle.addEventListener("click", () => setMenu(mobileNav.hidden));

  mobileNav.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => setMenu(false));
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !mobileNav.hidden) {
      setMenu(false);
      menuToggle.focus();
    }
  });

  // Close the mobile menu if the window grows to desktop width
  window.matchMedia("(min-width: 901px)").addEventListener("change", (event) => {
    if (event.matches) setMenu(false);
  });
}
