#!/usr/bin/env python3
"""
Bundle the whole ONE IPTV site into ONE self-contained HTML file.

Everything is inlined — CSS, JS, images as data URIs — and internal links are
rewritten to hash routes, so the file can be opened by double-clicking it with
no web server. Behaviour (modal, FAQ, carousel, mobile menu) is identical to
the real site.
"""
import base64
import glob
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "ONE-IPTV-preview.html")

# Page URL -> built file, in nav order
PAGES = [
    ("/", "index.html"),
    ("/features/", "features/index.html"),
    ("/channels/", "channels/index.html"),
    ("/pricing/", "pricing/index.html"),
    ("/devices/", "devices/index.html"),
    ("/faq/", "faq/index.html"),
    ("/blog/", "blog/index.html"),
    ("/contact/", "contact/index.html"),
    ("/privacy/", "privacy/index.html"),
    ("/terms/", "terms/index.html"),
    ("/refund-policy/", "refund-policy/index.html"),
    ("/404.html", "404.html"),
]
for f in sorted(glob.glob(os.path.join(ROOT, "blog", "*", "index.html"))):
    slug = os.path.basename(os.path.dirname(f))
    PAGES.append((f"/blog/{slug}/", f"blog/{slug}/index.html"))


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def img_map():
    """Every image asset as a data URI."""
    m = {}
    for path in glob.glob(os.path.join(ROOT, "assets", "img", "*")):
        name = os.path.basename(path)
        ext = name.rsplit(".", 1)[-1].lower()
        if ext not in ("svg", "png", "jpg", "jpeg"):
            continue
        # The 1200x630 social images are never rendered on-page — skip the weight.
        if name.startswith("og-image") or name.startswith("icon-"):
            continue
        mime = {"svg": "image/svg+xml", "png": "image/png",
                "jpg": "image/jpeg", "jpeg": "image/jpeg"}[ext]
        with open(path, "rb") as fh:
            m["/assets/img/" + name] = f"data:{mime};base64," + base64.b64encode(fh.read()).decode()
    return m


IMGS = img_map()


def inline_images(html):
    for src, uri in IMGS.items():
        html = html.replace(f'"{src}"', f'"{uri}"')
    return html


def hash_links(html):
    """Rewrite site-root links to hash routes; leave #anchors, tel:, mailto: alone."""
    def sub(m):
        attr, url = m.group(1), m.group(2)
        if url.startswith("/assets/") or url.startswith("/sitemap") or url.startswith("/site."):
            return m.group(0)
        return f'{attr}="#{url}"'
    return re.sub(r'(href)="(/[^"#]*)"', sub, html)


def split_shell(html):
    """Return (prefix, suffix) around <main id="main"> … </main>."""
    a = html.index('<main id="main">')
    b = html.index("</main>") + len("</main>")
    body_start = html.index("<body>") + len("<body>")
    return html[body_start:a], html[b:]


def build():
    home = read("index.html")
    prefix, suffix = split_shell(home)

    # Strip the external stylesheet/script tags from the suffix; we inline them.
    suffix = re.sub(r'<script src="/assets/js/[^"]+"[^>]*></script>\s*', "", suffix)
    suffix = suffix.replace("</body>", "").replace("</html>", "")

    prefix = hash_links(inline_images(prefix))
    suffix = hash_links(inline_images(suffix))

    # ---- collect each page's <main> content + title -------------------------
    pages_js = []
    for url, rel in PAGES:
        html = read(rel)
        title = re.search(r"<title>(.*?)</title>", html).group(1)
        inner = html[html.index('<main id="main">') + len('<main id="main">'):html.index("</main>")]
        inner = hash_links(inline_images(inner))
        pages_js.append((url, title, inner))

    css = read("assets/css/styles.css")
    cfg = read("assets/js/config.js")
    js = read("assets/js/main.js")
    # tmdb.js fallback references /assets/img/cat-*.svg — inline those so the
    # offline single-file preview shows fallback posters too.
    tmdb_js = inline_images(read("assets/js/tmdb.js"))

    # Font is fetched from Google; keep it but the system stack covers offline use.
    font_link = (
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
        'family=Inter:wght@400;500;600;700;800;900&display=swap">'
    )

    # ---- serialise pages into a JS object ----------------------------------
    def esc(s):
        return (s.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${"))

    entries = ",\n".join(
        f'{url!r}: {{ title: {title!r}, html: `{esc(inner)}` }}'.replace("'", '"', 2)
        for url, title, inner in pages_js
    )
    # keys/titles need to be valid JS strings — rebuild carefully
    entries = ",\n".join(
        '"%s": { title: "%s", html: `%s` }' % (
            url, title.replace('"', '\\"'), esc(inner))
        for url, title, inner in pages_js
    )

    favicon = IMGS.get("/assets/img/favicon.svg", "")

    banner = """
<div id="pv-bar">
  <span class="pv-dot"></span>
  <strong>Local preview</strong>
  <span class="pv-sep"></span>
  <span class="pv-url" id="pv-url">one-iptv.website/</span>
  <span class="pv-grow"></span>
  <span class="pv-note">Every page and every button works. Links open in this file.</span>
  <button id="pv-hide" type="button" aria-label="Hide preview bar">Hide</button>
</div>
"""

    bar_css = """
#pv-bar{position:fixed;left:0;right:0;bottom:0;z-index:2000;display:flex;align-items:center;
  gap:.7rem;padding:.6rem clamp(.8rem,3vw,1.4rem);background:rgba(10,10,14,.94);
  backdrop-filter:blur(14px);border-top:1px solid rgba(255,255,255,.12);
  font-size:.8rem;color:#b7b7c4;font-family:var(--font)}
#pv-bar strong{color:#fff;font-weight:700;letter-spacing:.02em}
#pv-bar .pv-dot{width:8px;height:8px;border-radius:50%;background:#3ddc84;
  box-shadow:0 0 10px #3ddc84;flex:none}
#pv-bar .pv-sep{width:1px;height:16px;background:rgba(255,255,255,.16)}
#pv-bar .pv-url{font-family:ui-monospace,Menlo,Consolas,monospace;color:#ff8a92}
#pv-bar .pv-grow{flex:1}
#pv-bar .pv-note{color:#83838f}
#pv-bar button{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.16);
  color:#fff;font:inherit;font-size:.76rem;font-weight:600;padding:.3rem .8rem;
  border-radius:99px;cursor:pointer}
#pv-bar button:hover{background:rgba(229,9,20,.22);border-color:rgba(229,9,20,.5)}
#pv-bar.pv-off{transform:translateY(110%)}
#pv-bar{transition:transform .3s cubic-bezier(.22,1,.36,1)}
body{padding-bottom:46px}
.fab-call{bottom:64px!important}
@media(max-width:760px){#pv-bar .pv-note{display:none}}
"""

    router = """
<script>
(function(){
  var PAGES = window.__PV_PAGES__;
  var main  = document.getElementById('main');
  var bar   = document.getElementById('pv-bar');
  var urlEl = document.getElementById('pv-url');

  function route(){
    var h = location.hash.replace(/^#/, '') || '/';
    if (!PAGES[h]) {
      // unknown path -> show the real 404 page, like the live site would
      h = PAGES['/404.html'] ? '/404.html' : '/';
    }
    var p = PAGES[h];
    main.innerHTML = p.html;
    document.title = p.title;
    if (urlEl) urlEl.textContent = 'one-iptv.website' + (h === '/' ? '/' : h);

    // active nav state
    document.querySelectorAll('.nav a, .mnav-link').forEach(function(a){
      var href = (a.getAttribute('href') || '').replace(/^#/, '');
      var on = href === h;
      a.classList.toggle('is-active', on);
      if (on) a.setAttribute('aria-current','page'); else a.removeAttribute('aria-current');
    });

    if (window.ONE_IPTV && window.ONE_IPTV.refresh) window.ONE_IPTV.refresh();
    if (window.ONE_IPTV_TMDB && window.ONE_IPTV_TMDB.load) window.ONE_IPTV_TMDB.load();
    window.scrollTo(0, 0);
  }

  // in-page anchors (#faq etc.) inside a routed page shouldn't trigger routing
  window.addEventListener('hashchange', function(){
    var h = location.hash.replace(/^#/, '');
    if (h && h.charAt(0) !== '/') {
      var t = document.getElementById(h);
      if (t) { t.scrollIntoView({behavior:'smooth'}); return; }
    }
    route();
  });

  if (bar) {
    document.getElementById('pv-hide').onclick = function(){
      bar.classList.add('pv-off');
      document.body.style.paddingBottom = '0';
    };
  }

  route();
})();
</script>
"""

    out = f"""<!DOCTYPE html>
<html lang="en" class="js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>ONE IPTV | Premium IPTV Service</title>
<link rel="icon" href="{favicon}">
{font_link}
<style>
{css}
{bar_css}
</style>
</head>
<body>
{prefix}
<main id="main"></main>
{suffix}
{banner}
<script>
{cfg}
</script>
<script>window.__PV_PAGES__ = {{
{entries}
}};</script>
<script>
{js}
</script>
<script>
{tmdb_js}
</script>
{router}
</body>
</html>
"""

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(out)
    print(f"✓ ONE-IPTV-preview.html  ({os.path.getsize(OUT)/1024:.0f} KB, {len(PAGES)} pages inlined)")


if __name__ == "__main__":
    build()
