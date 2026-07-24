(function () {
  var STORAGE_KEY = "cookie_consent";

  function setConsent(value) {
    localStorage.setItem(STORAGE_KEY, value);
    if (window.gtag) {
      gtag("consent", "update", { analytics_storage: value });
    }
  }

  function showBanner() {
    var banner = document.createElement("div");
    banner.id = "cookie-consent-banner";
    banner.style.cssText =
      "position:fixed;left:0;right:0;bottom:0;z-index:99999;" +
      "background:#0b0b0f;color:#eee;padding:14px 18px;" +
      "font:14px/1.5 -apple-system,Segoe UI,Roboto,Arial,sans-serif;" +
      "display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:center;" +
      "box-shadow:0 -2px 10px rgba(0,0,0,.3);";

    var text = document.createElement("span");
    text.textContent =
      "This site uses cookies for analytics to see how visitors use it. " +
      "You can accept or decline.";

    var acceptBtn = document.createElement("button");
    acceptBtn.textContent = "Accept";
    acceptBtn.style.cssText =
      "background:#4f7cff;color:#fff;border:0;border-radius:4px;padding:6px 16px;cursor:pointer;";

    var declineBtn = document.createElement("button");
    declineBtn.textContent = "Decline";
    declineBtn.style.cssText =
      "background:transparent;color:#eee;border:1px solid #666;border-radius:4px;padding:6px 16px;cursor:pointer;";

    acceptBtn.onclick = function () {
      setConsent("granted");
      banner.remove();
    };
    declineBtn.onclick = function () {
      setConsent("denied");
      banner.remove();
    };

    banner.appendChild(text);
    banner.appendChild(acceptBtn);
    banner.appendChild(declineBtn);
    document.body.appendChild(banner);
  }

  document.addEventListener("DOMContentLoaded", function () {
    if (!localStorage.getItem(STORAGE_KEY)) {
      showBanner();
    }
  });
})();
