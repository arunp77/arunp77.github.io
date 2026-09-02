(() => {
  "use strict";
  const button = document.querySelector(".right-side-list .dropbtn");
  const menu = document.querySelector(".right-side-list .dropdown-content");
  if (!button || !menu) return;

  const closeMenu = () => {
    menu.classList.remove("is-open");
    button.setAttribute("aria-expanded", "false");
  };

  button.addEventListener("click", event => {
    event.stopPropagation();
    const willOpen = !menu.classList.contains("is-open");
    menu.classList.toggle("is-open", willOpen);
    button.setAttribute("aria-expanded", String(willOpen));
  });

  menu.addEventListener("click", event => event.stopPropagation());
  document.addEventListener("click", closeMenu);
  document.addEventListener("keydown", event => {
    if (event.key === "Escape") {
      closeMenu();
      button.focus();
    }
  });
})();
