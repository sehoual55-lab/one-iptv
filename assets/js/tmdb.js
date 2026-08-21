/* ==========================================================================
   ONE IPTV — TMDB film & series showcase
   Loads live posters from The Movie Database into the catalogue carousels.
   Fully progressive: if the API is unreachable, the built-in fallback
   artwork that ships in the HTML stays exactly as it is.
   Config lives in config.js -> ONE_IPTV_CONFIG.tmdb
   ========================================================================== */
(function () {
  "use strict";

  var CFG = (window.ONE_IPTV_CONFIG || {}).tmdb;
  if (!CFG || !CFG.enabled || !CFG.apiKey) return;

  var host = null;   // resolved per boot() so SPA-injected sections work too
  var $ = function (s, r) { return (r || document).querySelector(s); };

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function api(path) {
    var join = path.indexOf("?") === -1 ? "?" : "&";
    return "https://api.themoviedb.org/3" + path + join +
      "api_key=" + encodeURIComponent(CFG.apiKey) +
      "&language=" + encodeURIComponent(CFG.language || "en-US");
  }

  function year(item) {
    var d = item.release_date || item.first_air_date || "";
    return d ? d.slice(0, 4) : "";
  }

  function ratingBadge(item) {
    var v = item.vote_average;
    if (!v) return "";
    return '<span class="film__score">' +
      '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2l2.9 6.3 6.9.6-5.2 4.6 1.6 6.8L12 17.3 5.8 20.9l1.6-6.8L2.2 8.9l6.9-.6z"/></svg>' +
      v.toFixed(1) + "</span>";
  }

  function typeLabel(t) { return t === "tv" ? "Series" : "Film"; }

  function card(item, type) {
    var title = item.title || item.name || "Untitled";
    var poster = item.poster_path ? CFG.imageBase + item.poster_path : null;
    var yr = year(item);
    var meta = [typeLabel(type), yr].filter(Boolean).join(" · ");

    // No poster? skip — keeps the row clean.
    if (!poster) return "";

    return '' +
      '<article class="film" tabindex="0" aria-label="' + esc(title) + (yr ? " (" + yr + ")" : "") + '">' +
        '<div class="film__poster">' +
          '<img loading="lazy" decoding="async" width="342" height="513" ' +
               'src="' + esc(poster) + '" alt="Poster for ' + esc(title) + '">' +
          ratingBadge(item) +
          '<span class="film__play" aria-hidden="true">' +
            '<svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span>' +
        '</div>' +
        '<div class="film__meta">' +
          '<h3 class="film__title">' + esc(title) + '</h3>' +
          '<p class="film__sub">' + esc(meta) + '</p>' +
        '</div>' +
      '</article>';
  }

  // Fallback poster tiles built from our own category artwork, used if a row
  // cannot be filled from TMDB (offline, blocked, rate-limited). Keeps the
  // section looking intentional instead of leaving an empty rail.
  // Full literal paths so the offline single-file preview can inline them.
  var FALLBACK = [
    ["/assets/img/cat-live-tv.svg", "Live TV", "Live"],
    ["/assets/img/cat-sports.svg", "Sports", "Live"],
    ["/assets/img/cat-movies.svg", "Movies", "On demand"],
    ["/assets/img/cat-series.svg", "Series", "On demand"],
    ["/assets/img/cat-entertainment.svg", "Entertainment", "Mixed"],
    ["/assets/img/cat-news.svg", "News", "Live"],
    ["/assets/img/cat-documentaries.svg", "Documentaries", "On demand"],
    ["/assets/img/cat-kids.svg", "Kids", "Family"]
  ];

  function fallbackCards() {
    return FALLBACK.map(function (f) {
      return '' +
        '<a class="film" href="/channels/" aria-label="' + esc(f[1]) + '">' +
          '<div class="film__poster">' +
            '<img loading="lazy" decoding="async" width="300" height="450" ' +
                 'src="' + f[0] + '" alt="' + esc(f[1]) + ' artwork">' +
            '<span class="film__play" aria-hidden="true">' +
              '<svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span>' +
          '</div>' +
          '<div class="film__meta"><h3 class="film__title">' + esc(f[1]) +
            '</h3><p class="film__sub">' + esc(f[2]) + '</p></div>' +
        '</a>';
    }).join("");
  }

  // Marquee tracks loop, so give them enough cards to always overflow.
  function fill(track, html) {
    if (!html) return false;
    if (track.hasAttribute("data-tmdb-notext")) html = html + html;  // duplicate for looping
    track.innerHTML = html;
    return true;
  }

  function renderRow(row, items) {
    var track = $('[data-tmdb-track="' + row.id + '"]');
    if (!track) return false;
    var cards = items.slice(0, CFG.maxPerRow || 18)
      .map(function (it) { return card(it, row.type); })
      .filter(Boolean).join("");
    return fill(track, cards);
  }

  function renderFallback(row) {
    var track = $('[data-tmdb-track="' + row.id + '"]');
    if (track) fill(track, fallbackCards());
  }

  function fetchRow(row) {
    return fetch(api(row.path))
      .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
      .then(function (data) {
        var items = (data && data.results) || [];
        if (!items.length) throw new Error("empty");
        return renderRow(row, items);
      });
  }

  function boot() {
    host = document.querySelector("[data-tmdb]");
    if (!host) return;
    // Skip if this section is already populated (avoids double-loading on SPA nav).
    if (host.getAttribute("data-tmdb-done") === "1") return;
    host.setAttribute("data-tmdb-done", "1");

    var rows = CFG.rows || [];
    var done = 0, ok = 0;
    var settled = false;

    rows.forEach(function (row) {
      fetchRow(row)
        .then(function (rendered) { if (rendered) ok++; else renderFallback(row); })
        .catch(function () { renderFallback(row); })
        .then(function () {
          done++;
          if (done === rows.length && !settled) { settled = true; finish(ok); }
        });
    });

    // Safety timeout: if the network hangs, fill any still-loading row.
    setTimeout(function () {
      if (settled) return;
      settled = true;
      rows.forEach(function (row) {
        var track = $('[data-tmdb-track="' + row.id + '"]');
        if (track && $(".skeleton", track)) renderFallback(row);
      });
      finish(ok);
    }, 6000);
  }

  function finish(ok) {
    host.classList.remove("is-loading");
    host.classList.toggle("tmdb-live", ok > 0);
    if (window.ONE_IPTV && window.ONE_IPTV.refresh) {
      // let the carousel controller re-measure the new tiles
      window.ONE_IPTV.refresh();
    }
    // Attribution is only required when we actually used TMDB data.
    var attr = $("[data-tmdb-attr]");
    if (attr) attr.hidden = ok === 0;
  }

  // Expose a loader so SPA navigation (e.g. the local preview) can populate
  // film rows on pages injected after initial load.
  window.ONE_IPTV_TMDB = { load: boot };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
