/* ==========================================================================
   ONE IPTV — main.js
   Sticky header · mobile nav · FAQ accordion · carousel · pricing sync ·
   checkout modal · scroll reveal
   All prices / contact details come from assets/js/config.js
   ========================================================================== */
(function () {
  "use strict";

  var CFG = window.ONE_IPTV_CONFIG || {};
  var $  = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---------------------------------------------------------------- utils */
  // A plan is a placeholder while it has no real numeric base price.
  function isPlaceholder(plan) {
    if (typeof plan === "object" && plan) {
      return plan.basePrice == null || isNaN(Number(plan.basePrice));
    }
    return !plan || /x/i.test(String(plan));
  }

  function money(amount) {
    var c = CFG.currency || { symbol: "€", position: "before" };
    var n = Number(amount);
    var s = (isNaN(n) ? amount : n.toFixed(2));
    return c.position === "after" ? s + " " + c.symbol : c.symbol + s;
  }

  // Legacy helper kept for the checkout summary; passes strings/numbers through money().
  function formatPrice(v) {
    if (v === "" || v == null) return "";
    return money(v);
  }

  function planById(id) {
    return (CFG.plans || []).filter(function (p) { return p.id === id; })[0] || null;
  }

  function connConfig() {
    return CFG.connections || { min: 1, max: 5, default: 1, extraDiscount: 0.15 };
  }

  function clampConn(n) {
    var c = connConfig();
    n = parseInt(n, 10) || c.default || 1;
    return Math.max(c.min || 1, Math.min(c.max || 5, n));
  }

  // total = base × (1 + (1 − discount) × (connections − 1))
  function planTotal(plan, connections) {
    if (isPlaceholder(plan)) return null;
    var c = connConfig();
    var d = typeof c.extraDiscount === "number" ? c.extraDiscount : 0.15;
    var base = Number(plan.basePrice);
    return base * (1 + (1 - d) * (Math.max(1, connections) - 1));
  }

  // What the extra connections would have cost at full price (for "you save X").
  function planSaving(plan, connections) {
    if (isPlaceholder(plan) || connections <= 1) return 0;
    var c = connConfig();
    var d = typeof c.extraDiscount === "number" ? c.extraDiscount : 0.15;
    return Number(plan.basePrice) * d * (connections - 1);
  }

  // The PAID term (bonus months are shown separately as "+N free").
  function termLabel(plan) {
    return plan.months + (plan.months === 1 ? " month" : " months");
  }

  // Per-plan selected connection count lives here.
  var connState = {};
  function getConn(id) {
    if (connState[id] == null) {
      var p = planById(id);
      connState[id] = clampConn((connConfig().default) || 1);
    }
    return connState[id];
  }

  function esc(str) {
    return String(str == null ? "" : str)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  /* ---------------------------------------------- 1. Contact details sync */
  function syncContact() {
    var c = CFG.contact;
    if (!c) return;
    // Contact is WhatsApp-only.
    $$("[data-whatsapp-link]").forEach(function (el) {
      el.setAttribute("href", "https://wa.me/" + c.whatsappNumber);
    });
  }

  /* ------------------------------------------------- 2. Sticky header UI */
  function initHeader() {
    var header = $(".site-header");
    if (!header) return;
    var ticking = false;
    function update() {
      header.classList.toggle("is-stuck", window.scrollY > 12);
      ticking = false;
    }
    window.addEventListener("scroll", function () {
      if (!ticking) { window.requestAnimationFrame(update); ticking = true; }
    }, { passive: true });
    update();
  }

  /* --------------------------------------------------- 3. Mobile nav menu */
  function initMobileNav() {
    var burger = $(".burger");
    var drawer = $("#mobile-nav");
    if (!burger || !drawer) return;

    function setOpen(open) {
      burger.setAttribute("aria-expanded", open ? "true" : "false");
      drawer.classList.toggle("is-open", open);
      drawer.setAttribute("aria-hidden", open ? "false" : "true");
      document.body.classList.toggle("no-scroll", open);
    }

    burger.addEventListener("click", function () {
      setOpen(burger.getAttribute("aria-expanded") !== "true");
    });

    drawer.addEventListener("click", function (e) {
      if (e.target.closest("a")) setOpen(false);
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && burger.getAttribute("aria-expanded") === "true") {
        setOpen(false);
        burger.focus();
      }
    });

    window.addEventListener("resize", function () {
      if (window.innerWidth > 960) setOpen(false);
    });

    setOpen(false);
  }

  /* ------------------------------------------------------ 4. FAQ accordion */
  function initFaq() {
    $$(".faq-item").forEach(function (item) {
      var btn    = $(".faq-q", item);
      var panel  = $(".faq-a", item);
      if (!btn || !panel) return;
      if (btn.getAttribute("data-faq-wired") === "1") return;  // bind once
      btn.setAttribute("data-faq-wired", "1");

      function setOpen(open) {
        item.classList.toggle("is-open", open);
        btn.setAttribute("aria-expanded", open ? "true" : "false");
        panel.style.maxHeight = open ? panel.scrollHeight + "px" : "0px";
      }

      btn.addEventListener("click", function () {
        var willOpen = btn.getAttribute("aria-expanded") !== "true";
        // close siblings within the same list (single-open accordion)
        var list = item.parentElement;
        if (list) {
          $$(".faq-item.is-open", list).forEach(function (other) {
            if (other !== item) {
              other.classList.remove("is-open");
              var ob = $(".faq-q", other), op = $(".faq-a", other);
              if (ob) ob.setAttribute("aria-expanded", "false");
              if (op) op.style.maxHeight = "0px";
            }
          });
        }
        setOpen(willOpen);
      });

      setOpen(btn.getAttribute("aria-expanded") === "true");
    });

    // keep open panels sized correctly on resize
    var t;
    window.addEventListener("resize", function () {
      clearTimeout(t);
      t = setTimeout(function () {
        $$(".faq-item.is-open .faq-a").forEach(function (p) {
          p.style.maxHeight = p.scrollHeight + "px";
        });
      }, 140);
    });
  }

  /* --------------------------------------------------------- 5. Carousel */
  function initCarousel() {
    $$("[data-carousel]").forEach(function (shell) {
      var track = $(".carousel", shell);
      var prev  = $("[data-carousel-prev]", shell);
      var next  = $("[data-carousel-next]", shell);
      if (!track) return;
      if (shell.getAttribute("data-carousel-wired") === "1") { return; }
      shell.setAttribute("data-carousel-wired", "1");

      function step() {
        var first = track.firstElementChild;
        var w = first ? first.getBoundingClientRect().width : 260;
        return Math.max(w + 18, track.clientWidth * 0.7);
      }
      if (prev) prev.addEventListener("click", function () { track.scrollBy({ left: -step(), behavior: "smooth" }); });
      if (next) next.addEventListener("click", function () { track.scrollBy({ left:  step(), behavior: "smooth" }); });

      function updateBtns() {
        var max = track.scrollWidth - track.clientWidth - 2;
        if (prev) prev.disabled = track.scrollLeft <= 2;
        if (next) next.disabled = track.scrollLeft >= max;
        if (prev) prev.style.opacity = prev.disabled ? ".4" : "1";
        if (next) next.style.opacity = next.disabled ? ".4" : "1";
      }
      track.addEventListener("scroll", updateBtns, { passive: true });
      window.addEventListener("resize", updateBtns);
      updateBtns();
    });
  }

  /* ------------------------------------------------- 5b. Auto-scroll strip */
  function initAutoScroll() {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    $$("[data-autoscroll]").forEach(function (shell) {
      if (shell.getAttribute("data-autoscroll-wired") === "1") return;
      shell.setAttribute("data-autoscroll-wired", "1");

      var track = $(".carousel", shell);
      if (!track) return;
      var timer = null, paused = false;

      function step() {
        var first = track.firstElementChild;
        var w = first ? first.getBoundingClientRect().width : 150;
        var gap = parseFloat(getComputedStyle(track).columnGap || getComputedStyle(track).gap) || 12;
        var advance = w + gap;
        var max = track.scrollWidth - track.clientWidth;
        if (max <= 4) return;                       // nothing to scroll yet
        if (track.scrollLeft >= max - 4) {
          track.scrollTo({ left: 0, behavior: "smooth" });   // loop back
        } else {
          track.scrollBy({ left: advance, behavior: "smooth" });
        }
      }

      function start() { if (!timer && !paused) timer = window.setInterval(step, 2000); }
      function stop() { if (timer) { window.clearInterval(timer); timer = null; } }

      // Pause while the user is interacting, resume afterwards.
      shell.addEventListener("mouseenter", function () { paused = true; stop(); });
      shell.addEventListener("mouseleave", function () { paused = false; start(); });
      shell.addEventListener("focusin", function () { paused = true; stop(); });
      shell.addEventListener("focusout", function () { paused = false; start(); });
      track.addEventListener("touchstart", function () { paused = true; stop(); }, { passive: true });
      track.addEventListener("touchend", function () {
        paused = false; window.setTimeout(start, 3000);
      }, { passive: true });

      // Pause when the tab/section is off-screen to save cycles.
      if ("IntersectionObserver" in window) {
        new IntersectionObserver(function (entries) {
          entries.forEach(function (e) {
            if (e.isIntersecting) { paused = false; start(); }
            else { paused = true; stop(); }
          });
        }, { threshold: 0.15 }).observe(shell);
      } else {
        start();
      }
    });
  }

  /* ---------------------------------------------------- 6. Pricing sync */
  function renderPlanCard(card) {
    var plan = planById(card.getAttribute("data-plan"));
    if (!plan) return;
    var conn = getConn(plan.id);
    var c = connConfig();

    var set = function (sel, val) { var el = $(sel, card); if (el) el.textContent = val; };

    set("[data-plan-name]", plan.name);

    // Term subtitle under the name, e.g. "15 months  +3 months free"
    var termEl = $("[data-plan-term]", card);
    if (termEl) {
      var bonus = plan.bonusMonths
        ? ' <span class="plan__bonus">+' + plan.bonusMonths + " month" +
          (plan.bonusMonths === 1 ? "" : "s") + " free</span>"
        : "";
      termEl.innerHTML = termLabel(plan) + bonus;
    }

    // Price line: amount + "/ 15 months"
    var priceEl = $("[data-plan-price]", card);
    var total = planTotal(plan, conn);
    if (priceEl) priceEl.textContent = (total == null) ? "$XX.XX" : money(total);
    var perEl = $("[data-plan-per]", card);
    if (perEl) perEl.textContent = "/ " + termLabel(plan);

    // Badge
    var badgeEl = $("[data-plan-badge]", card);
    if (badgeEl) {
      if (plan.badge) { badgeEl.textContent = plan.badge; badgeEl.hidden = false; }
      else badgeEl.hidden = true;
    }

    // Stepper display
    set("[data-conn-count]", conn);
    var lbl = $("[data-conn-label]", card);
    if (lbl) lbl.textContent = conn === 1 ? "connection" : "connections";
    var dec = $("[data-conn-dec]", card), inc = $("[data-conn-inc]", card);
    if (dec) dec.disabled = conn <= (c.min || 1);
    if (inc) inc.disabled = conn >= (c.max || 5);

    // Connection note — matches the reference wording, with live saving added.
    var note = $("[data-conn-note]", card);
    if (note) {
      var pct = Math.round((c.extraDiscount || 0.15) * 100);
      var base = "First connection at the normal price · each additional <b>" + pct + "% cheaper</b>";
      if (!isPlaceholder(plan) && conn > 1) {
        base += " · you save " + money(planSaving(plan, conn));
      }
      note.innerHTML = base;
    }

    // Features
    var listEl = $("[data-plan-features]", card);
    if (listEl && plan.features && plan.features.length) {
      listEl.innerHTML = plan.features.map(function (f) {
        return '<li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6"' +
               ' stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
               '<polyline points="20 6 9 17 4 12"/></svg><span>' + esc(f) + "</span></li>";
      }).join("");
    }
  }

  function syncPricing() {
    $$("[data-plan]").forEach(function (card) {
      renderPlanCard(card);

      // Wire the stepper once per card.
      if (card.getAttribute("data-conn-wired") === "1") return;
      var id = card.getAttribute("data-plan");
      var dec = $("[data-conn-dec]", card), inc = $("[data-conn-inc]", card);
      if (dec) dec.addEventListener("click", function () {
        connState[id] = clampConn(getConn(id) - 1); renderPlanCard(card);
      });
      if (inc) inc.addEventListener("click", function () {
        connState[id] = clampConn(getConn(id) + 1); renderPlanCard(card);
      });
      card.setAttribute("data-conn-wired", "1");
    });
  }

  /* ----------------------------------- 7. Product schema (real prices only) */
  function injectOfferSchema() {
    var plans = CFG.plans || [];
    var real = plans.filter(function (p) { return !isPlaceholder(p); });
    if (!real.length) return;   // never publish invented prices

    var brand = CFG.brand || {};
    var cur = (CFG.currency || {}).code || "EUR";
    var data = {
      "@context": "https://schema.org",
      "@type": "Product",
      "name": brand.name + " Subscription Plans",
      "description": "Subscription access plans for " + brand.name + " on compatible Smart TVs and streaming devices.",
      "brand": { "@type": "Brand", "name": brand.name },
      "offers": real.map(function (p) {
        return {
          "@type": "Offer",
          "name": brand.name + " — " + p.name + " (1 connection)",
          "price": Number(p.basePrice).toFixed(2),
          "priceCurrency": cur,
          "availability": "https://schema.org/InStock",
          "url": (brand.url || "") + "/pricing/"
        };
      })
    };
    var s = document.createElement("script");
    s.type = "application/ld+json";
    s.textContent = JSON.stringify(data);
    document.head.appendChild(s);
  }

  /* ---------------------------------------------------- 8. Checkout modal */
  var Checkout = (function () {
    var modal, panel, form, successView, formView, lastFocus = null;

    var coConn = clampConn((connConfig().default) || 1);

    function fillPlanOptions() {
      var picker = $("[data-plan-picker]", modal);
      if (!picker) return;
      picker.innerHTML = (CFG.plans || []).map(function (p, i) {
        var t = planTotal(p, coConn);
        return (
          '<label class="plan-opt">' +
            '<input type="radio" name="plan" value="' + esc(p.id) + '"' + (i === 0 ? " checked" : "") + ">" +
            '<span class="plan-opt__label">' + esc(p.name) + "</span>" +
            '<span class="plan-opt__price" data-opt-price="' + esc(p.id) + '">' +
              (t == null ? "On request" : esc(money(t))) + "</span>" +
          "</label>"
        );
      }).join("");
      picker.addEventListener("change", updateSummary);
    }

    function selectedPlan() {
      var input = $('input[name="plan"]:checked', modal);
      return input ? planById(input.value) : (CFG.plans || [])[0];
    }

    function refreshOptionPrices() {
      (CFG.plans || []).forEach(function (p) {
        var el = $('[data-opt-price="' + p.id + '"]', modal);
        if (!el) return;
        var t = planTotal(p, coConn);
        el.textContent = (t == null) ? "On request" : money(t);
      });
    }

    function updateConnUI() {
      var c = connConfig();
      var set = function (sel, val) { var el = $(sel, modal); if (el) el.textContent = val; };
      set("[data-co-conn-count]", coConn);
      var lbl = $("[data-co-conn-label]", modal);
      if (lbl) lbl.textContent = coConn === 1 ? "connection" : "connections";
      var dec = $("[data-co-conn-dec]", modal), inc = $("[data-co-conn-inc]", modal);
      if (dec) dec.disabled = coConn <= (c.min || 1);
      if (inc) inc.disabled = coConn >= (c.max || 5);
    }

    function updateSummary() {
      var p = selectedPlan();
      if (!p) return;
      var set = function (sel, val) { var el = $(sel, modal); if (el) el.textContent = val; };
      var total = planTotal(p, coConn);
      set("[data-sum-plan]", p.name);
      set("[data-sum-duration]",
        termLabel(p) + (p.bonusMonths ? " (incl. " + p.bonusMonths + " free)" : ""));
      set("[data-sum-conn]", coConn + (coConn === 1 ? " device" : " devices"));
      set("[data-sum-total]", total == null ? "On request" : money(total));
      refreshOptionPrices();
      updateConnUI();

      var note = $("[data-sum-note]", modal);
      if (note) note.hidden = !isPlaceholder(p);
    }

    function validate() {
      var ok = true;
      $$("[data-validate]", form).forEach(function (input) {
        var field = input.closest(".field");
        var msg = field ? $(".field-error", field) : null;
        var value = (input.value || "").trim();
        var error = "";

        if (!value) {
          error = "This field is required.";
        } else if (input.type === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(value)) {
          error = "Please enter a valid email address.";
        } else if (input.type === "tel" && value.replace(/[^\d]/g, "").length < 6) {
          error = "Please enter a valid phone number.";
        }

        if (field) field.classList.toggle("has-error", !!error);
        if (msg) msg.textContent = error;
        input.setAttribute("aria-invalid", error ? "true" : "false");
        if (error && ok) { input.focus(); ok = false; }
      });
      return ok;
    }

    function orderText(data, plan) {
      var b = CFG.brand || {};
      var total = planTotal(plan, coConn);
      return (
        "New order request — " + (b.name || "ONE IPTV") + "\n\n" +
        "Plan: " + plan.name + " (" + termLabel(plan) +
          (plan.bonusMonths ? ", incl. " + plan.bonusMonths + " free" : "") + ")\n" +
        "Connections: " + coConn + "\n" +
        "Price: " + (total == null ? "to be confirmed" : money(total)) + "\n" +
        "Name: " + data.name + "\n" +
        "WhatsApp: " + data.phone + "\n" +
        (data.notes ? "Notes: " + data.notes + "\n" : "")
      );
    }

    // Silently append the order to the configured Google Sheet endpoint.
    // Uses a "simple" text/plain POST so the browser sends it without a CORS
    // preflight (Google Apps Script web apps don't answer preflight requests).
    function logOrder(plan, data) {
      var endpoint = (CFG.checkout || {}).logEndpoint;
      if (!endpoint) return;
      var total = planTotal(plan, coConn);
      var payload = {
        name: data.name,
        email: "",                       // site is WhatsApp-only
        phone: data.phone,
        plan: plan.name + (plan.bonusMonths ? " (" + plan.months + "+" + plan.bonusMonths + " mo)" : ""),
        price: total == null ? "" : money(total),
        connections: coConn,
        payment: "En attente",
        status: "Nouveau",
        notes: data.notes || ""
      };
      try {
        fetch(endpoint, {
          method: "POST",
          mode: "no-cors",
          headers: { "Content-Type": "text/plain;charset=utf-8" },
          body: JSON.stringify(payload)
        }).catch(function () {});
      } catch (e) { /* never block the order on logging */ }
    }

    function submit(e) {
      e.preventDefault();
      if (!validate()) return;

      var plan = selectedPlan();
      var data = {
        name:  ($("#co-name", form)  || {}).value || "",
        phone: ($("#co-phone", form) || {}).value || "",
        notes: ($("#co-notes", form) || {}).value || "",
        planId: plan.id,
        planName: plan.name,
        connections: coConn
      };

      var co = CFG.checkout || {};
      var url;

      // Log the order to the Google Sheet (fire-and-forget) whatever mode is used.
      logOrder(plan, data);

      /* --- redirect to a hosted, PCI-compliant checkout ------------------- */
      if (co.mode === "redirect") {
        url = (co.paymentUrls || {})[plan.id];
        if (url) {
          showSuccess(plan, data, "redirect");
          window.setTimeout(function () { window.location.href = url; }, 900);
          return;
        }
      }

      /* --- POST to your own endpoint / form service ---------------------- */
      if (co.mode === "endpoint" && co.endpoint) {
        var btn = $("[data-checkout-submit]", form);
        if (btn) { btn.disabled = true; btn.textContent = "Sending…"; }
        fetch(co.endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data)
        }).then(function () {
          showSuccess(plan, data, "endpoint");
        }).catch(function () {
          showSuccess(plan, data, "handoff");
        }).then(function () {
          if (btn) { btn.disabled = false; btn.textContent = "Continue to Checkout"; }
        });
        return;
      }

      /* --- default: hand the order off to WhatsApp ------------------------ */
      var c = CFG.contact || {};
      var body = orderText(data, plan);
      url = "https://wa.me/" + c.whatsappNumber + "?text=" + encodeURIComponent(body);
      showSuccess(plan, data, "handoff");
      window.open(url, "_blank", "noopener");
    }

    function showSuccess(plan, data, mode) {
      if (!successView || !formView) return;
      formView.hidden = true;
      successView.hidden = false;

      var set = function (sel, val) { var el = $(sel, successView); if (el) el.textContent = val; };
      var total = planTotal(plan, coConn);
      set("[data-ok-plan]", plan.name + " · " + coConn + (coConn === 1 ? " device" : " devices"));
      set("[data-ok-name]", data.name);
      set("[data-ok-phone]", data.phone);
      set("[data-ok-total]", total == null ? "On request" : money(total));

      var msg = $("[data-ok-message]", successView);
      if (msg) {
        msg.textContent =
          mode === "redirect"
            ? "Taking you to our secure payment page…"
            : mode === "endpoint"
              ? "Your order request has been received. We will confirm the next step on WhatsApp shortly."
              : "Your order summary has opened in WhatsApp so you can send it to our team. If it didn't open, tap the button below.";
      }
      panel.scrollTop = 0;
    }

    function reset() {
      if (form) form.reset();
      $$(".field.has-error", modal).forEach(function (f) { f.classList.remove("has-error"); });
      $$(".field-error", modal).forEach(function (f) { f.textContent = ""; });
      if (formView) formView.hidden = false;
      if (successView) successView.hidden = true;
      var first = $('input[name="plan"]', modal);
      if (first) first.checked = true;
      updateSummary();
    }

    function open(planId, connections) {
      if (!modal) return;
      lastFocus = document.activeElement;
      if (planId) {
        var radio = $('input[name="plan"][value="' + planId + '"]', modal);
        if (radio) radio.checked = true;
        // Carry the connection count chosen on the pricing card, if any.
        if (connections == null && connState[planId] != null) connections = connState[planId];
      }
      if (connections != null) coConn = clampConn(connections);
      updateSummary();
      modal.classList.add("is-open");
      modal.setAttribute("aria-hidden", "false");
      document.body.classList.add("no-scroll");
      var focusTarget = $("#co-name", modal) || $(".modal__close", modal);
      window.setTimeout(function () { if (focusTarget) focusTarget.focus(); }, 60);
    }

    function close() {
      if (!modal) return;
      modal.classList.remove("is-open");
      modal.setAttribute("aria-hidden", "true");
      document.body.classList.remove("no-scroll");
      if (lastFocus && lastFocus.focus) lastFocus.focus();
      window.setTimeout(reset, 320);
    }

    function trapFocus(e) {
      if (e.key !== "Tab" || !modal.classList.contains("is-open")) return;
      var focusables = $$(
        'button:not([disabled]), [href], input:not([type="hidden"]), select, textarea, [tabindex]:not([tabindex="-1"])',
        panel
      ).filter(function (el) { return el.offsetParent !== null; });
      if (!focusables.length) return;
      var first = focusables[0], last = focusables[focusables.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }

    function init() {
      modal = $("#checkout-modal");
      if (!modal) return;
      panel = $(".modal__panel", modal);
      form = $("#checkout-form", modal);
      formView = $("[data-checkout-form-view]", modal);
      successView = $("[data-checkout-success]", modal);

      fillPlanOptions();
      updateSummary();

      // Modal connection stepper
      var mdec = $("[data-co-conn-dec]", modal), minc = $("[data-co-conn-inc]", modal);
      if (mdec) mdec.addEventListener("click", function () { coConn = clampConn(coConn - 1); updateSummary(); });
      if (minc) minc.addEventListener("click", function () { coConn = clampConn(coConn + 1); updateSummary(); });

      // note text from config
      var secure = $("[data-secure-note]", modal);
      if (secure && CFG.checkout && CFG.checkout.secureNote) {
        secure.textContent = " " + CFG.checkout.secureNote;
      }

      if (form) form.addEventListener("submit", submit);

      $$("[data-checkout-close]", modal).forEach(function (btn) {
        btn.addEventListener("click", close);
      });

      document.addEventListener("keydown", function (e) {
        if (e.key === "Escape" && modal.classList.contains("is-open")) close();
      });
      document.addEventListener("keydown", trapFocus);

      // Global openers
      document.addEventListener("click", function (e) {
        var trigger = e.target.closest("[data-open-checkout]");
        if (!trigger) return;
        e.preventDefault();
        open(trigger.getAttribute("data-open-checkout") || null);
      });
    }

    return { init: init, open: open, close: close };
  })();

  /* ------------------------------------------------------ 9. Scroll reveal */
  function initReveal() {
    var els = $$(".reveal");
    if (!els.length) return;
    if (!("IntersectionObserver" in window) ||
        window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      els.forEach(function (el) { el.classList.add("is-visible"); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.06 });
    els.forEach(function (el, i) {
      el.style.transitionDelay = (Math.min(i % 4, 3) * 70) + "ms";
      io.observe(el);
    });
  }

  /* ------------------------------------------- 10. Active nav + misc */
  function initActiveNav() {
    var path = window.location.pathname.replace(/\/index\.html$/, "/").replace(/\.html$/, "");
    if (path === "") path = "/";
    $$(".nav a, .mnav-link").forEach(function (a) {
      var href = a.getAttribute("href") || "";
      if (href.indexOf("#") === 0 || href.indexOf("http") === 0) return;
      var clean = href.replace(/^\.\//, "/").replace(/\/index\.html$/, "/").replace(/\.html$/, "");
      if (clean === path || (path === "/" && (clean === "/" || clean === "/index"))) {
        a.classList.add("is-active");
        a.setAttribute("aria-current", "page");
      }
    });
  }

  function initYear() {
    $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
  }

  /* -------------------------------------------------------------- Boot */
  function boot() {
    syncContact();
    initHeader();
    initMobileNav();
    initFaq();
    initCarousel();
    initAutoScroll();
    syncPricing();
    injectOfferSchema();
    Checkout.init();
    initReveal();
    initActiveNav();
    initYear();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }

  /* Re-run the per-DOM initialisers after page content is swapped.
     Document-level listeners (checkout openers, Escape) are not re-bound. */
  function refresh() {
    syncContact();
    initFaq();
    initCarousel();
    initAutoScroll();
    syncPricing();
    initReveal();
    initYear();
  }

  window.ONE_IPTV = {
    openCheckout: Checkout.open,
    closeCheckout: Checkout.close,
    refresh: refresh
  };
})();
