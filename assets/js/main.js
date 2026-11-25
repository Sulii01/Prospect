/* ==========================================================================
   PROSPECT spol. s r.o. – interaktivita webu (bez knihoven)
   1) menu  2) animace při scrollu  3) počítadla  4) HMI panel v úvodu
   5) galerie (lightbox)  6) filtr referencí  7) obsah stránky (scrollspy)
   ========================================================================== */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.remove("no-js");
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  // texty podle jazyka stránky (<html lang="cs|en">)
  var LANG = doc.lang === "en" ? "en" : "cs";
  var TXT = {
    cs: { open: "Otevřít menu", close: "Zavřít menu", shown: "Zobrazeno {n} akcí", forq: " pro „{q}“", locale: "cs-CZ" },
    en: { open: "Open menu", close: "Close menu", shown: "Showing {n} projects", forq: " for “{q}”", locale: "en-GB" }
  }[LANG];
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* 1) MENU ---------------------------------------------------------------- */
  var header = $("[data-header]");
  var burger = $("[data-burger]");
  var onScroll = function () { header && header.classList.toggle("is-scrolled", window.scrollY > 20); };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  if (burger) {
    burger.addEventListener("click", function () {
      var open = header.classList.toggle("is-open");
      burger.setAttribute("aria-expanded", open);
      burger.setAttribute("aria-label", open ? TXT.close : TXT.open);
      document.body.style.overflow = open ? "hidden" : "";
    });
    // zavření menu po kliknutí na odkaz (mobil)
    $$(".main-nav a").forEach(function (a) {
      a.addEventListener("click", function () {
        header.classList.remove("is-open");
        burger.setAttribute("aria-expanded", "false");
        document.body.style.overflow = "";
      });
    });
  }

  $$(".mega-toggle").forEach(function (btn) {
    var li = btn.parentElement;
    btn.addEventListener("click", function (ev) {
      ev.stopPropagation();
      var open = li.classList.toggle("is-open");
      btn.setAttribute("aria-expanded", open);
    });
    document.addEventListener("click", function (ev) {
      if (!li.contains(ev.target)) { li.classList.remove("is-open"); btn.setAttribute("aria-expanded", "false"); }
    });
  });
  document.addEventListener("keydown", function (ev) {
    if (ev.key === "Escape") $$(".has-mega.is-open").forEach(function (li) { li.classList.remove("is-open"); });
  });

  /* 2) ANIMACE PŘI SCROLLU --------------------------------------------------- */
  var reveals = $$(".reveal");
  if ("IntersectionObserver" in window && !reduceMotion) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* 3) POČÍTADLA ------------------------------------------------------------- */
  function countUp(el) {
    var target = parseFloat(el.getAttribute("data-count"));
    var suffix = el.getAttribute("data-suffix") || "";
    // rok (1991) počítáme jen od 1950, ať animace nevypadá zvláštně
    var start = target > 1000 ? target - 41 : 0;
    var t0 = null, dur = 1600;
    function step(ts) {
      if (!t0) t0 = ts;
      var p = Math.min((ts - t0) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(start + (target - start) * eased) + suffix;
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  var counters = $$("[data-count]");
  if ("IntersectionObserver" in window && !reduceMotion) {
    var co = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { countUp(en.target); co.unobserve(en.target); }
      });
    }, { threshold: 0.6 });
    counters.forEach(function (el) { co.observe(el); });
  }

  /* 4) HMI PANEL (ilustrační „živá“ data) ------------------------------------ */
  var clock = $("[data-clock]");
  if (clock) {
    var tick = function () { clock.textContent = new Date().toLocaleTimeString(TXT.locale); };
    tick(); setInterval(tick, 1000);
  }
  var vals = { pressure: 4.2, flow: 128.4, level: 72 };
  var fields = {
    pressure: $('[data-val="pressure"]'), flow: $('[data-val="flow"]'), level: $('[data-val="level"]')
  };
  var levelRect = $("[data-level-rect]");
  var canvas = $("[data-trend]");
  var trendData = [];
  for (var i = 0; i < 60; i++) trendData.push(128 + Math.sin(i / 5) * 4);

  function drawTrend() {
    if (!canvas) return;
    var dpr = window.devicePixelRatio || 1;
    var w = canvas.clientWidth, h = canvas.clientHeight;
    if (canvas.width !== w * dpr) { canvas.width = w * dpr; canvas.height = h * dpr; }
    var ctx = canvas.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, w, h);
    ctx.strokeStyle = "rgba(255,255,255,.12)"; ctx.lineWidth = 1;
    for (var g = 1; g < 4; g++) { ctx.beginPath(); ctx.moveTo(0, h * g / 4); ctx.lineTo(w, h * g / 4); ctx.stroke(); }
    var min = 115, max = 142;
    var pts = trendData.map(function (v, idx) {
      return [idx / (trendData.length - 1) * w, h - (v - min) / (max - min) * (h - 10) - 5];
    });
    var grad = ctx.createLinearGradient(0, 0, 0, h);
    grad.addColorStop(0, "rgba(255,235,59,.30)"); grad.addColorStop(1, "rgba(255,235,59,0)");
    ctx.beginPath(); ctx.moveTo(pts[0][0], h);
    pts.forEach(function (p) { ctx.lineTo(p[0], p[1]); });
    ctx.lineTo(w, h); ctx.closePath(); ctx.fillStyle = grad; ctx.fill();
    ctx.beginPath();
    pts.forEach(function (p, idx) { idx ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]); });
    ctx.strokeStyle = "#ffeb3b"; ctx.lineWidth = 1.8; ctx.stroke();
    var last = pts[pts.length - 1];
    ctx.beginPath(); ctx.arc(last[0] - 3, last[1], 3, 0, Math.PI * 2); ctx.fillStyle = "#39e75f"; ctx.fill();
    ctx.fillStyle = "rgba(255,255,255,.85)"; ctx.font = "bold 10px Arial, sans-serif";
    ctx.fillText(canvas.getAttribute("data-label") || "TREND", 8, 14);
  }

  function updateHmi() {
    var t = Date.now() / 1000;
    vals.pressure = 4.2 + Math.sin(t / 3) * 0.12 + (Math.random() - 0.5) * 0.04;
    vals.flow = 128 + Math.sin(t / 4) * 6 + (Math.random() - 0.5) * 1.6;
    vals.level = 72 + Math.sin(t / 9) * 9;
    if (fields.pressure) fields.pressure.textContent = vals.pressure.toFixed(2);
    if (fields.flow) fields.flow.textContent = vals.flow.toFixed(1);
    if (fields.level) fields.level.textContent = vals.level.toFixed(1);
    if (levelRect) {
      // výška vody v nádrži podle hladiny (data-bottom = dno, data-height = max. výška)
      var bottom = parseFloat(levelRect.getAttribute("data-bottom"));
      var hh = parseFloat(levelRect.getAttribute("data-height")) * vals.level / 100;
      levelRect.setAttribute("y", bottom - hh); levelRect.setAttribute("height", hh);
    }
    trendData.push(vals.flow); trendData.shift();
    drawTrend();
  }
  if (fields.flow) {
    updateHmi();
    if (!reduceMotion) setInterval(updateHmi, 900);
    window.addEventListener("resize", drawTrend);
  }

  /* 5) GALERIE / LIGHTBOX ---------------------------------------------------- */
  var lb = $("[data-lightbox]");
  if (lb) {
    var lbImg = $("img", lb), lbCap = $("figcaption", lb);
    var group = [], idx = 0, lastFocus = null;
    var show = function () {
      var a = group[idx];
      lbImg.src = a.getAttribute("href");
      lbImg.alt = (a.querySelector("img") || {}).alt || "";
      lbCap.textContent = a.getAttribute("data-lb") + " · " + (idx + 1) + " / " + group.length;
    };
    var open = function (a) {
      var gallery = a.closest(".gallery");
      group = $$(".g-item", gallery); idx = group.indexOf(a);
      lastFocus = a; show(); lb.hidden = false; document.body.style.overflow = "hidden";
      $(".lb-close", lb).focus();
    };
    var close = function () { lb.hidden = true; document.body.style.overflow = ""; lastFocus && lastFocus.focus(); };
    var move = function (d) { idx = (idx + d + group.length) % group.length; show(); };
    $$(".g-item").forEach(function (a) {
      a.addEventListener("click", function (ev) { ev.preventDefault(); open(a); });
    });
    $(".lb-close", lb).addEventListener("click", close);
    $(".lb-prev", lb).addEventListener("click", function () { move(-1); });
    $(".lb-next", lb).addEventListener("click", function () { move(1); });
    lb.addEventListener("click", function (ev) { if (ev.target === lb) close(); });
    document.addEventListener("keydown", function (ev) {
      if (lb.hidden) return;
      if (ev.key === "Escape") close();
      if (ev.key === "ArrowLeft") move(-1);
      if (ev.key === "ArrowRight") move(1);
    });
    // swipe na mobilu
    var sx = null;
    lb.addEventListener("touchstart", function (ev) { sx = ev.touches[0].clientX; }, { passive: true });
    lb.addEventListener("touchend", function (ev) {
      if (sx === null) return;
      var dx = ev.changedTouches[0].clientX - sx;
      if (Math.abs(dx) > 50) move(dx < 0 ? 1 : -1);
      sx = null;
    });
  }

  /* 6) FILTR A VYHLEDÁVÁNÍ V REFERENCÍCH ------------------------------------ */
  var refs = $("[data-refs]");
  if (refs) {
    var input = $("[data-ref-search]", refs);
    var chips = $$("[data-filter]", refs);
    var blocks = $$(".ref-block", refs);
    var heads = $$(".ref-obor", refs);
    var countEl = $("[data-ref-count]", refs);
    var emptyEl = $("[data-ref-empty]", refs);
    var current = "vse";
    var norm = function (s) { return s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); };
    var items = $$(".ref-list li", refs).map(function (li) {
      return { li: li, text: li.textContent, n: norm(li.textContent) };
    });
    var escapeHtml = function (s) {
      return s.replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; });
    };

    var apply = function () {
      var q = norm(input.value.trim());
      var shown = 0;
      items.forEach(function (it) {
        var match = !q || it.n.indexOf(q) !== -1;
        it.li.hidden = !match;
        if (match && q) {
          var start = it.n.indexOf(q);
          it.li.innerHTML = escapeHtml(it.text.slice(0, start)) + "<mark>" +
            escapeHtml(it.text.slice(start, start + q.length)) + "</mark>" + escapeHtml(it.text.slice(start + q.length));
        } else {
          it.li.textContent = it.text;
        }
      });
      blocks.forEach(function (b) {
        var inObor = current === "vse" || b.getAttribute("data-obor") === current;
        $$(".ref-group", b).forEach(function (g) {
          var lis = $$("li", g);
          g.hidden = q && lis.length ? lis.every(function (li) { return li.hidden; }) : false;
          if (q && !lis.length) g.hidden = true;
        });
        var visible = $$(".ref-list li", b).filter(function (li) { return !li.hidden; }).length;
        b.hidden = !inObor || (q && visible === 0);
        if (!b.hidden) shown += visible;
      });
      heads.forEach(function (h) {
        var o = h.getAttribute("data-obor");
        h.hidden = !blocks.some(function (b) { return b.getAttribute("data-obor") === o && !b.hidden; });
      });
      countEl.textContent = TXT.shown.replace("{n}", shown) + (q ? TXT.forq.replace("{q}", input.value.trim()) : "");
      emptyEl.hidden = shown > 0;
    };

    chips.forEach(function (c) {
      c.addEventListener("click", function () {
        current = c.getAttribute("data-filter");
        chips.forEach(function (x) { x.classList.toggle("is-active", x === c); x.setAttribute("aria-pressed", x === c); });
        var url = new URL(location.href);
        current === "vse" ? url.searchParams.delete("obor") : url.searchParams.set("obor", current);
        history.replaceState(null, "", url);
        apply();
      });
    });
    var timer;
    input.addEventListener("input", function () { clearTimeout(timer); timer = setTimeout(apply, 120); });

    // předvolba z adresy, např. reference.html?obor=plynova-zarizeni
    var pre = new URLSearchParams(location.search).get("obor");
    var preChip = pre && chips.filter(function (c) { return c.getAttribute("data-filter") === pre; })[0];
    if (preChip) preChip.click(); else apply();
  }

  /* 7) SCROLLSPY – zvýraznění aktuální sekce v postranním obsahu ------------ */
  var spy = $("[data-scrollspy]");
  if (spy && "IntersectionObserver" in window) {
    var links = $$("a", spy);
    var map = {};
    links.forEach(function (a) { map[a.getAttribute("href").slice(1)] = a; });
    var so = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          links.forEach(function (a) { a.classList.remove("is-active"); });
          var a = map[en.target.id]; a && a.classList.add("is-active");
        }
      });
    }, { rootMargin: "-30% 0px -60% 0px" });
    Object.keys(map).forEach(function (id) { var el = document.getElementById(id); el && so.observe(el); });
  }
})();
