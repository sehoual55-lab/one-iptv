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
    var coPlanId = null;   // plan chosen on the pricing card

    // Country dialling codes for the phone field.
    var COUNTRIES = [
      ["GB", "🇬🇧", "+44"], ["FR", "🇫🇷", "+33"], ["US", "🇺🇸", "+1"],
      ["IE", "🇮🇪", "+353"], ["BE", "🇧🇪", "+32"], ["CH", "🇨🇭", "+41"],
      ["ES", "🇪🇸", "+34"], ["DE", "🇩🇪", "+49"], ["IT", "🇮🇹", "+39"],
      ["NL", "🇳🇱", "+31"], ["PT", "🇵🇹", "+351"], ["LU", "🇱🇺", "+352"],
      ["CA", "🇨🇦", "+1"], ["MA", "🇲🇦", "+212"], ["DZ", "🇩🇿", "+213"],
      ["TN", "🇹🇳", "+216"]
    ];

    // Icon markup for the payment-method options (matches shell.py ICONS).
    var PAY_ICONS = {
      card: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/></svg>',
      paypal: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M7 20l1.5-9h4a3 3 0 0 0 0-6H7L4.5 20z"/><path d="M10 16h3.5a3.5 3.5 0 0 0 0-7H10.5"/></svg>',
      crypto: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M9.5 8h4a2 2 0 0 1 0 4h-4m0 0h4.3a2 2 0 0 1 0 4H9.5m0-8v10m2-11v1m0 9v1"/></svg>',
      whatsapp: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22h.01c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2zm5.35 13.9c-.2.57-1.16 1.08-1.63 1.15-.42.06-.95.08-1.53-.1-.35-.11-.8-.26-1.38-.51-2.43-1.04-4.01-3.48-4.13-3.64-.12-.16-.99-1.32-.99-2.51s.63-1.78.85-2.02c.22-.24.48-.3.64-.3s.32.01.46.01c.16 0 .34-.04.53.41.2.48.67 1.68.73 1.8.06.12.1.26.02.42-.08.16-.12.26-.24.4-.12.14-.25.31-.36.42-.12.12-.24.25-.1.49.14.24.62 1.03 1.34 1.67.92.82 1.7 1.08 1.94 1.2.24.12.38.1.52-.06.14-.16.6-.7.76-.94.16-.24.32-.2.54-.12.22.08 1.41.66 1.65.78.24.12.4.18.46.28.06.1.06.58-.14 1.15z"/></svg>'
    };

    function selectedPlan() {
      return planById(coPlanId) ||
        (CFG.plans || []).filter(function (p) { return p.featured; })[0] ||
        (CFG.plans || [])[0];
    }

    function methods() { return (CFG.checkout || {}).paymentMethods || []; }

    function selectedMethod() {
      var input = $('input[name="pay"]:checked', modal);
      var id = input ? input.value : (methods()[0] || {}).id;
      return methods().filter(function (m) { return m.id === id; })[0] || methods()[0] || {};
    }

    // French helpers
    function termFr(plan) {
      var t = plan.months + " mois";
      if (plan.bonusMonths) {
        t += " (+" + plan.bonusMonths + " mois offert" + (plan.bonusMonths === 1 ? "" : "s") + ")";
      }
      return t;
    }
    function connFr(n) { return n + " connexion" + (n === 1 ? "" : "s") + " simultanée" + (n === 1 ? "" : "s"); }

    function fillCountries() {
      var sel = $("[data-phone-cc]", modal);
      if (!sel || sel.options.length) return;
      sel.innerHTML = COUNTRIES.map(function (c) {
        return '<option value="' + c[2] + '" data-iso="' + c[0] + '">' + c[1] + " " + c[2] + "</option>";
      }).join("");
    }

    function selectedCountry() {
      var sel = $("[data-phone-cc]", form || modal);
      var opt = sel && sel.selectedOptions ? sel.selectedOptions[0] : null;
      return opt ? (opt.getAttribute("data-iso") || "") : "";
    }

    function fillMethods() {
      var box = $("[data-pay-methods]", modal);
      if (!box) return;
      var legend = box.querySelector("legend");
      var grid = document.createElement("div");
      grid.className = "pay-grid";
      grid.innerHTML = methods().map(function (m, i) {
        return (
          '<label class="pay-opt">' +
            '<input type="radio" name="pay" value="' + esc(m.id) + '"' + (i === 0 ? " checked" : "") + ">" +
            '<span class="pay-opt__icon">' + (PAY_ICONS[m.icon] || "") + "</span>" +
            '<span class="pay-opt__label">' + esc(m.label) + "</span>" +
          "</label>"
        );
      }).join("");
      // keep legend, replace any previous grid
      var old = box.querySelector(".pay-grid");
      if (old) old.remove();
      box.appendChild(grid);
      if (legend) box.insertBefore(legend, grid);
    }

    function updateSummary() {
      var p = selectedPlan();
      if (!p) return;
      var set = function (sel, val) { var el = $(sel, modal); if (el) el.textContent = val; };
      var total = planTotal(p, coConn);
      set("[data-sum-plan]", p.name + " — " + termFr(p));
      set("[data-sum-conn]", connFr(coConn));
      set("[data-sum-total]", total == null ? "Sur demande" : money(total));

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
          error = "Ce champ est obligatoire.";
        } else if (input.type === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(value)) {
          error = "Veuillez saisir une adresse e-mail valide.";
        } else if (input.type === "tel" && value.replace(/[^\d]/g, "").length < 6) {
          error = "Veuillez saisir un numéro de téléphone valide.";
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
        "Nouvelle commande — " + (b.name || "ONE IPTV") + "\n\n" +
        "Formule : " + plan.name + " (" + termFr(plan) + ")\n" +
        "Connexions : " + coConn + "\n" +
        "Total : " + (total == null ? "à confirmer" : money(total)) + "\n" +
        "Paiement : " + data.method + "\n" +
        "Nom : " + data.name + "\n" +
        "E-mail : " + data.email + "\n" +
        "Téléphone : " + data.phone + "\n"
      );
    }

    // Silently append the order to the Google Sheet endpoint (which also emails you).
    // Form-encoded (application/x-www-form-urlencoded) so the body survives Google's
    // internal 302 redirect on /exec — a JSON body would get dropped on that hop and
    // land as an empty row. The Apps Script reads e.parameter for each field.
    function logOrder(plan, data) {
      var endpoint = (CFG.checkout || {}).logEndpoint;
      if (!endpoint) return;
      var brand = CFG.brand || {};
      var total = planTotal(plan, coConn);
      var params = new URLSearchParams();
      params.set("website", brand.domain || brand.url || "");
      params.set("name", data.name || "");
      params.set("email", data.email || "");
      params.set("phone", data.phone || "");
      params.set("country", data.country || "");
      params.set("plan", plan.name + " (" + termFr(plan) + ")");
      params.set("connections", String(coConn));
      params.set("price", total == null ? "" : money(total));
      params.set("payment", data.method || "");
      params.set("paymentLink", data.paymentLink || "");
      params.set("status", "Nouveau");
      try {
        fetch(endpoint, {
          method: "POST",
          mode: "no-cors",
          headers: { "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8" },
          body: params.toString()
        }).catch(function () {});
      } catch (e) { /* never block the order on logging */ }
    }

    function submit(e) {
      e.preventDefault();
      if (!validate()) return;

      var plan = selectedPlan();
      var method = selectedMethod();
      var cc = ($("[data-phone-cc]", form) || {}).value || "";
      var num = ($("#co-phone", form) || {}).value || "";
      var data = {
        name:  ($("#co-name", form)  || {}).value || "",
        email: ($("#co-email", form) || {}).value || "",
        phone: (cc ? cc + " " : "") + num,
        country: selectedCountry(),
        method: method.label || "",
        methodId: method.id || "",
        paymentLink: method.url || "",
        planId: plan.id,
        connections: coConn
      };

      // Log to the sheet + email you (fire-and-forget), for every method.
      logOrder(plan, data);

      // WhatsApp method → open a pre-filled chat.
      if (method.action === "whatsapp") {
        var c = CFG.contact || {};
        var url = "https://wa.me/" + c.whatsappNumber + "?text=" + encodeURIComponent(orderText(data, plan));
        showSuccess(plan, data, "whatsapp");
        window.open(url, "_blank", "noopener");
        return;
      }

      // Redirect method → send to a hosted payment link if one is set.
      if (method.action === "redirect" && method.url) {
        showSuccess(plan, data, "redirect");
        window.setTimeout(function () { window.location.href = method.url; }, 900);
        return;
      }

      // Default: record the order; you follow up with the payment details.
      showSuccess(plan, data, "notify");
    }

    function showSuccess(plan, data, mode) {
      if (!successView || !formView) return;
      formView.hidden = true;
      successView.hidden = false;

      var set = function (sel, val) { var el = $(sel, successView); if (el) el.textContent = val; };
      var total = planTotal(plan, coConn);
      set("[data-ok-name]", data.name);
      set("[data-ok-email]", data.email);
      set("[data-ok-plan]", plan.name + " · " + connFr(coConn));
      set("[data-ok-pay]", data.method);
      set("[data-ok-total]", total == null ? "Sur demande" : money(total));

      var msg = $("[data-ok-message]", successView);
      if (msg) {
        msg.textContent =
          mode === "redirect"
            ? "Redirection vers la page de paiement sécurisé…"
            : mode === "whatsapp"
              ? "Votre commande s'est ouverte dans WhatsApp. Si ce n'est pas le cas, appuyez sur le bouton ci-dessous."
              : "Votre commande a bien été enregistrée. Nous vous envoyons les instructions de paiement très vite — vous pouvez aussi nous écrire sur WhatsApp.";
      }
      panel.scrollTop = 0;
    }

    function reset() {
      if (form) form.reset();
      $$(".field.has-error", modal).forEach(function (f) { f.classList.remove("has-error"); });
      $$(".field-error", modal).forEach(function (f) { f.textContent = ""; });
      if (formView) formView.hidden = false;
      if (successView) successView.hidden = true;
      var firstPay = $('input[name="pay"]', modal);
      if (firstPay) firstPay.checked = true;
      updateSummary();
    }

    function open(planId, connections) {
      if (!modal) return;
      lastFocus = document.activeElement;
      if (planId) {
        coPlanId = planId;
        if (connections == null && connState[planId] != null) connections = connState[planId];
      } else if (!coPlanId) {
        coPlanId = (selectedPlan() || {}).id;
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
      var promoEl = $("[data-checkout-promo]", modal);
      if (promoEl) { promoEl.hidden = true; promoEl.textContent = ""; }
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

      fillCountries();
      fillMethods();
      updateSummary();

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

  /* Check mark used by the plan feature lists and the offer popup. */
  var ICON_CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6"' +
    ' stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    '<polyline points="20 6 9 17 4 12"/></svg>';

  /* --------------------------------------------- 8b. Welcome offer popup */
  /* A standalone offer panel that appears a few seconds after load. It collects
     name / email / WhatsApp number, then hands those straight into the main order
     form on the chosen plan, so there is one ordering pipeline, not two.
     Every string lives in CFG.promo — see config.js. */
  var Promo = (function () {
    var modal, panel, form, lastFocus = null, shown = false;

    function cfg() { return CFG.promo || {}; }
    function plan() { return planById(cfg().planId) || (CFG.plans || [])[0]; }

    function totalMonths(p) { return (p.months || 0) + (p.bonusMonths || 0); }

    function fill() {
      var c = cfg(), p = plan();
      if (!p) return;
      var set = function (sel, val) { var el = $(sel, modal); if (el) el.textContent = val || ""; };

      set("[data-promo-badge]", c.badge);
      set("[data-promo-line1]", c.line1);
      set("[data-promo-line2]", c.line2);
      set("[data-promo-lead]", c.lead);
      set("[data-promo-form-label]", c.formLabel);
      set("[data-promo-submit]", c.cta);
      set("[data-promo-compare]", c.compare);

      var list = $("[data-promo-list]", modal);
      if (list) {
        list.innerHTML = (c.points || []).map(function (pt) {
          var strong = Array.isArray(pt) ? pt[0] : pt;
          var rest = Array.isArray(pt) ? (pt[1] || "") : "";
          return '<li>' + ICON_CHECK + "<span><b>" + esc(strong) + "</b> " + esc(rest) + "</span></li>";
        }).join("");
      }

      var base = planTotal(p, 1);
      set("[data-promo-price]", base == null ? "" : money(base));
      set("[data-promo-per]", p.months ? "/ " + p.months + " months" : "");

      var months = totalMonths(p);
      var pm = $("[data-promo-permonth]", modal);
      if (pm) {
        if (base == null || !months || !c.perMonth) { pm.hidden = true; }
        else {
          pm.hidden = false;
          pm.textContent = c.perMonth
            .replace("{permonth}", money(base / months))
            .replace("{totalmonths}", String(months));
        }
      }

      var ph = function (sel, val) { var el = $(sel, modal); if (el && val) el.placeholder = val; };
      ph("#promo-name", c.namePlaceholder);
      ph("#promo-email", c.emailPlaceholder);
      ph("#promo-phone", c.phonePlaceholder);

      // Country codes: reuse the same list the order form uses.
      var sel = $("[data-promo-cc]", modal);
      var src = $("[data-phone-cc]", $("#checkout-modal"));
      if (sel && src && !sel.options.length) sel.innerHTML = src.innerHTML;
    }

    function validate() {
      var ok = true;
      $$("[data-validate]", form).forEach(function (input) {
        var field = input.closest(".field");
        var msg = field ? $(".field-error", field) : null;
        var value = (input.value || "").trim();
        var error = "";

        if (!value) error = "This field is required.";
        else if (input.type === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(value))
          error = "Please enter a valid email address.";
        else if (input.type === "tel" && value.replace(/[^\d]/g, "").length < 6)
          error = "Please enter a valid phone number.";

        if (field) field.classList.toggle("has-error", !!error);
        if (msg) msg.textContent = error;
        input.setAttribute("aria-invalid", error ? "true" : "false");
        if (error && ok) { input.focus(); ok = false; }
      });
      return ok;
    }

    // Copy the details into the main order form and open it on this plan.
    function handOff() {
      var co = $("#checkout-modal");
      if (!co) return;
      var copy = function (from, to) {
        var a = $(from, modal), b = $(to, co);
        if (a && b) b.value = a.value;
      };
      copy("#promo-name", "#co-name");
      copy("#promo-email", "#co-email");
      copy("#promo-phone", "#co-phone");
      copy("[data-promo-cc]", "[data-phone-cc]");
      close();
      window.setTimeout(function () { Checkout.open(cfg().planId || null); }, 220);
    }

    function submit(e) {
      e.preventDefault();
      if (!validate()) return;
      handOff();
    }

    function open() {
      if (!modal || shown) return;
      lastFocus = document.activeElement;
      fill();
      shown = true;
      modal.classList.add("is-open");
      modal.setAttribute("aria-hidden", "false");
      document.body.classList.add("no-scroll");
      var target = $("#promo-name", modal);
      window.setTimeout(function () { if (target) target.focus(); }, 60);
    }

    function close() {
      if (!modal) return;
      modal.classList.remove("is-open");
      modal.setAttribute("aria-hidden", "true");
      document.body.classList.remove("no-scroll");
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }

    function trapFocus(e) {
      if (e.key !== "Tab" || !modal || !modal.classList.contains("is-open")) return;
      var f = $$('button:not([disabled]), [href], input:not([type="hidden"]), select, textarea', panel)
        .filter(function (el) { return el.offsetParent !== null; });
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }

    function seenKey() { return "oneiptv_promo_seen"; }

    function alreadySeen() {
      var mode = cfg().showOnce || "session";
      if (mode === "always") return false;
      try {
        if (mode === "session") return window.sessionStorage.getItem(seenKey()) === "1";
        var stamp = window.localStorage.getItem(seenKey());
        return !!stamp && (Date.now() - parseInt(stamp, 10)) < 86400000;
      } catch (err) { return false; }
    }

    function markSeen() {
      var mode = cfg().showOnce || "session";
      try {
        if (mode === "session") window.sessionStorage.setItem(seenKey(), "1");
        else if (mode !== "always") window.localStorage.setItem(seenKey(), String(Date.now()));
      } catch (err) { /* storage blocked — nothing to do */ }
    }

    function init() {
      var c = cfg();
      modal = $("#promo-modal");
      if (!modal || !c.enabled) return;
      panel = $(".modal__panel", modal);
      form = $("#promo-form", modal);

      $$("[data-promo-close]", modal).forEach(function (b) { b.addEventListener("click", close); });
      if (form) form.addEventListener("submit", submit);

      var cmp = $("[data-promo-compare]", modal);
      if (cmp) cmp.addEventListener("click", function () { close(); window.location.href = "/pricing/"; });

      document.addEventListener("keydown", function (e) {
        if (e.key === "Escape" && modal.classList.contains("is-open")) close();
      });
      document.addEventListener("keydown", trapFocus);

      if (alreadySeen()) return;

      window.setTimeout(function () {
        var co = $("#checkout-modal");
        if (co && co.classList.contains("is-open")) return;   // never interrupt an order
        if (document.hidden) return;                           // not on a background tab
        markSeen();
        open();
      }, c.delayMs || 7000);
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
    Promo.init();
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
    openPromo: Promo.open,
    closePromo: Promo.close,
    openCheckout: Checkout.open,
    closeCheckout: Checkout.close,
    refresh: refresh
  };
})();
