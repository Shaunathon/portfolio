// Switch the right-hand panel on the home page from the left-hand menu, and
// shade the sticky header once the page scrolls. Without JavaScript every
// panel shows, stacked, and the menu links jump to them.

(function () {
  document.documentElement.classList.add("js");

  document.addEventListener("DOMContentLoaded", function () {
    var header = document.querySelector(".site-header.sticky");
    if (header) {
      var onScroll = function () { header.classList.toggle("scrolled", window.scrollY > 4); };
      window.addEventListener("scroll", onScroll, { passive: true });
      onScroll();
    }

    var panels = Array.prototype.slice.call(document.querySelectorAll(".panel"));
    if (!panels.length) return;
    var links = Array.prototype.slice.call(document.querySelectorAll(".side [data-panel]"));
    var ids = panels.map(function (p) { return p.id; });
    // Old links to #work (from the first version) land on the case studies.
    var aliases = { work: "case-studies", contact: null };
    var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var current = null;

    function target() {
      var id = decodeURIComponent(location.hash.slice(1));
      if (id in aliases) id = aliases[id];
      return ids.indexOf(id) >= 0 ? id : null;
    }

    function show(id, moveFocus) {
      if (!id || id === current) return;
      panels.forEach(function (p) {
        var on = p.id === id;
        p.hidden = !on;
        p.classList.toggle("entering", on && current !== null);
      });
      links.forEach(function (a) {
        if (a.dataset.panel === id) a.setAttribute("aria-current", "true");
        else a.removeAttribute("aria-current");
      });
      current = id;
      if (moveFocus) {
        var heading = document.getElementById(id).querySelector("h1, h2");
        window.scrollTo({ top: 0, behavior: reduceMotion ? "auto" : "smooth" });
        if (heading) heading.focus({ preventScroll: true });
      }
    }

    // Keep the browser from jumping to the panel; we scroll to the top instead.
    if ("scrollRestoration" in history) history.scrollRestoration = "manual";

    show(target() || "about", false);
    if (target()) window.scrollTo(0, 0);

    window.addEventListener("hashchange", function () {
      // An empty hash (Back to the first view) means About; other anchors,
      // such as the skip link or #contact, leave the panel alone.
      var id = location.hash.length > 1 ? target() : "about";
      if (id) show(id, true);
    });
  });
})();
