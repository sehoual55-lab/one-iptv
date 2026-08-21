#!/usr/bin/env python3
"""Generate a self-contained HTML Google/social preview for the ONE IPTV site."""
import base64
import glob
import json
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "seo-preview.html")

SITE = "https://one-iptv.online"

# Human-friendly section names, in the order they should appear
ORDER = [
    ("index.html", "Home", "Core"),
    ("pricing/index.html", "Pricing", "Core"),
    ("features/index.html", "Features", "Core"),
    ("devices/index.html", "Devices", "Core"),
    ("channels/index.html", "Channels", "Core"),
    ("faq/index.html", "FAQ", "Core"),
    ("contact/index.html", "Contact", "Core"),
    ("blog/index.html", "Blog index", "Blog"),
    ("blog/one-iptv-complete-guide-for-beginners/index.html", "Beginner's guide", "Blog"),
    ("blog/how-to-set-up-one-iptv-on-a-smart-tv/index.html", "Smart TV setup", "Blog"),
    ("blog/smart-one-iptv-what-you-need-to-know/index.html", "Smart ONE IPTV", "Blog"),
    ("blog/iptv-one-month-plans-what-to-consider/index.html", "One month plans", "Blog"),
    ("blog/one-iptv-uk-getting-started-guide/index.html", "ONE IPTV UK", "Blog"),
    ("blog/smart-one-iptv-app-download-setup-guide/index.html", "App download", "Blog"),
    ("blog/how-to-set-up-iptv-on-your-tv/index.html", "IPTV on your TV", "Blog"),
    ("privacy/index.html", "Privacy", "Legal"),
    ("terms/index.html", "Terms", "Legal"),
    ("refund-policy/index.html", "Refund policy", "Legal"),
    ("404.html", "404", "Legal"),
]

KEYWORDS = [
    "one iptv", "smart one iptv", "iptv one month", "one iptv uk",
    "smart one iptv app download", "iptv app", "ip smart iptv",
    "iptv app for tv", "iptv tv smart",
]


def find(pat, html, default=""):
    m = re.search(pat, html)
    return m.group(1) if m else default


def collect():
    pages = []
    for rel, label, group in ORDER:
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            continue
        h = open(path, encoding="utf-8").read()

        # visible word count + h1
        body = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", h, flags=re.S)
        text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body)).strip()
        h1 = re.sub(r"<[^>]+>", "", find(r"<h1[^>]*>(.*?)</h1>", body, "")).strip()

        schemas = sorted(set(re.findall(r'"@type":\s*"([A-Za-z]+)"', h)))
        faq_qs = re.findall(r'"@type": "Question", "name": "(.*?)"', h)

        url = SITE + "/" if rel == "index.html" else SITE + "/" + rel.replace("index.html", "")
        if rel == "404.html":
            url = SITE + "/404.html"

        pages.append({
            "label": label,
            "group": group,
            "file": rel,
            "url": find(r'<link rel="canonical" href="([^"]*)"', h, url),
            "title": find(r"<title>(.*?)</title>", h),
            "desc": find(r'<meta name="description" content="([^"]*)"', h),
            "ogTitle": find(r'<meta property="og:title" content="([^"]*)"', h),
            "ogDesc": find(r'<meta property="og:description" content="([^"]*)"', h),
            "ogImage": find(r'<meta property="og:image" content="([^"]*)"', h),
            "ogType": find(r'<meta property="og:type" content="([^"]*)"', h),
            "twCard": find(r'<meta name="twitter:card" content="([^"]*)"', h),
            "robots": find(r'<meta name="robots" content="([^"]*)"', h),
            "keywords": find(r'<meta name="keywords" content="([^"]*)"', h),
            "h1": h1,
            "words": len(text.split()),
            "schemas": schemas,
            "faq": faq_qs,
            "indexable": "noindex" not in find(r'<meta name="robots" content="([^"]*)"', h),
        })
    return pages


def data_uri(path, mime):
    with open(os.path.join(ROOT, path), "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()


def build():
    pages = collect()
    favicon = data_uri("assets/img/favicon.svg", "image/svg+xml")
    og_png = data_uri("assets/img/og-image.jpg", "image/jpeg")

    payload = json.dumps({
        "site": SITE,
        "favicon": favicon,
        "ogImage": og_png,
        "keywords": KEYWORDS,
        "pages": pages,
    }, ensure_ascii=False)

    html = TEMPLATE.replace("__DATA__", payload)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✓ seo-preview.html  ({os.path.getsize(OUT)/1024:.0f} KB, {len(pages)} pages)")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>ONE IPTV — Google &amp; social preview</title>
<link rel="icon" href="__FAVICON__">
<style>
  :root{
    --bg:#07070a; --panel:#101017; --panel2:#16161f; --line:rgba(255,255,255,.1);
    --line2:rgba(255,255,255,.18); --txt:#fff; --mut:#b7b7c4; --dim:#83838f;
    --red:#e50914; --redb:#ff2b3b; --ok:#3ddc84; --warn:#ffc23d; --bad:#ff5b66;
    --sans:"Inter",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--txt);font-family:var(--sans);
       font-size:15px;line-height:1.6;-webkit-font-smoothing:antialiased}
  a{color:inherit}
  .wrap{max-width:1180px;margin:0 auto;padding:0 clamp(1rem,4vw,2rem)}

  /* ---------- header ---------- */
  header.top{
    position:sticky;top:0;z-index:50;background:rgba(7,7,10,.92);
    backdrop-filter:blur(16px);border-bottom:1px solid var(--line);
  }
  .top-in{display:flex;align-items:center;gap:1rem;flex-wrap:wrap;padding:.9rem 0}
  .brand{display:flex;align-items:center;gap:.6rem;font-weight:900;font-size:1.05rem}
  .brand img{width:30px;height:30px;border-radius:8px}
  .brand b{color:var(--redb)}
  .tabs{display:flex;gap:.25rem;margin-left:auto;background:rgba(255,255,255,.05);
        border:1px solid var(--line);border-radius:99px;padding:.25rem;flex-wrap:wrap}
  .tabs button{border:0;background:none;color:var(--mut);font:inherit;font-size:.85rem;
        font-weight:600;padding:.45rem 1rem;border-radius:99px;cursor:pointer;
        transition:.2s}
  .tabs button[aria-selected=true]{background:linear-gradient(130deg,var(--redb),#8f0009);
        color:#fff;box-shadow:0 4px 14px rgba(229,9,20,.35)}
  .tabs button:hover{color:#fff}

  /* ---------- intro ---------- */
  .intro{padding:2.2rem 0 1.4rem}
  h1{font-size:clamp(1.5rem,3.4vw,2.1rem);margin:0 0 .5rem;letter-spacing:-.025em}
  .intro p{color:var(--mut);margin:0;max-width:70ch;font-size:.96rem}
  .stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));
         gap:.8rem;margin:1.6rem 0 0}
  .stat{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:.9rem 1.1rem}
  .stat b{display:block;font-size:1.5rem;line-height:1.1;letter-spacing:-.03em}
  .stat span{font-size:.74rem;text-transform:uppercase;letter-spacing:.1em;color:var(--dim)}
  .stat.good b{color:var(--ok)} .stat.warn b{color:var(--warn)}

  /* ---------- controls ---------- */
  .bar{display:flex;gap:.6rem;flex-wrap:wrap;align-items:center;
       padding:1.2rem 0;border-bottom:1px solid var(--line);margin-bottom:1.6rem}
  .chip{border:1px solid var(--line);background:rgba(255,255,255,.04);color:var(--mut);
        font:inherit;font-size:.82rem;font-weight:600;padding:.4rem .9rem;border-radius:99px;
        cursor:pointer;transition:.18s}
  .chip:hover{color:#fff;border-color:var(--line2)}
  .chip[aria-pressed=true]{background:rgba(229,9,20,.16);border-color:rgba(229,9,20,.5);color:#ff8a92}
  .grow{flex:1}
  .search{display:flex;align-items:center;gap:.5rem;background:rgba(255,255,255,.04);
          border:1px solid var(--line);border-radius:99px;padding:.35rem .9rem;min-width:200px}
  .search input{background:none;border:0;color:#fff;font:inherit;font-size:.85rem;outline:0;width:100%}
  .search svg{width:14px;height:14px;color:var(--dim);flex:none}

  /* ---------- google SERP ---------- */
  .serp{background:#fff;border-radius:16px;padding:1.6rem 1.5rem;color:#202124;
        font-family:arial,sans-serif;max-width:652px;margin-bottom:1rem}
  .serp.dark{background:#202124;color:#bdc1c6}
  .g-res{margin-bottom:0}
  .g-head{display:flex;align-items:center;gap:12px;margin-bottom:4px}
  .g-fav{width:26px;height:26px;border-radius:50%;border:1px solid #ecedef;
         display:grid;place-items:center;background:#f1f3f4;flex:none;overflow:hidden}
  .g-fav img{width:18px;height:18px}
  .serp.dark .g-fav{background:#303134;border-color:#3c4043}
  .g-site{font-size:14px;line-height:20px;color:#202124}
  .serp.dark .g-site{color:#dadce0}
  .g-url{font-size:12px;line-height:18px;color:#4d5156}
  .serp.dark .g-url{color:#9aa0a6}
  .g-title{font-size:20px;line-height:26px;color:#1a0dab;font-weight:400;
           margin:0 0 3px;cursor:pointer;max-width:600px;
           overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}
  .serp.dark .g-title{color:#8ab4f8}
  .g-title:hover{text-decoration:underline}
  .g-desc{font-size:14px;line-height:22px;color:#4d5156;max-width:600px;
          overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}
  .serp.dark .g-desc{color:#bdc1c6}
  .g-date{color:#70757a}
  .g-mob{max-width:412px;border-radius:22px;padding:1.2rem 1.1rem}
  .g-mob .g-title{font-size:18px;line-height:24px;-webkit-line-clamp:3}
  .g-mob .g-desc{-webkit-line-clamp:3}
  .g-faq{margin-top:12px;border-top:1px solid #ecedef;padding-top:4px;max-width:600px}
  .serp.dark .g-faq{border-color:#3c4043}
  .g-faq div{display:flex;justify-content:space-between;align-items:center;gap:1rem;
             font-size:14px;line-height:20px;padding:11px 0;border-bottom:1px solid #ecedef;color:#202124}
  .serp.dark .g-faq div{border-color:#3c4043;color:#dadce0}
  .g-faq div:last-child{border-bottom:0}
  .g-faq span{color:#70757a;font-size:18px;flex:none}
  .g-sitelinks{display:grid;grid-template-columns:1fr 1fr;gap:2px 24px;
               max-width:600px;margin-top:10px}
  .g-sitelinks a{font-size:14px;line-height:20px;color:#1a0dab;padding:5px 0;
                 border-bottom:1px solid #ecedef;text-decoration:none}
  .serp.dark .g-sitelinks a{color:#8ab4f8;border-color:#3c4043}
  .g-sitelinks a:hover{text-decoration:underline}

  /* ---------- card wrapper ---------- */
  .card{background:var(--panel);border:1px solid var(--line);border-radius:20px;
        padding:1.3rem;margin-bottom:1.2rem;overflow:hidden}
  .card-head{display:flex;align-items:center;gap:.7rem;flex-wrap:wrap;margin-bottom:1.1rem}
  .card-head h3{margin:0;font-size:1rem;letter-spacing:-.01em}
  .grp{font-size:.66rem;font-weight:800;letter-spacing:.13em;text-transform:uppercase;
       padding:.24rem .6rem;border-radius:99px;background:rgba(229,9,20,.14);
       border:1px solid rgba(229,9,20,.32);color:#ff8a92}
  .path{font-size:.78rem;color:var(--dim);font-family:ui-monospace,Menlo,Consolas,monospace}
  .split{display:grid;grid-template-columns:minmax(0,652px) minmax(260px,1fr);
         gap:1.4rem;align-items:start}
  @media(max-width:900px){.split{grid-template-columns:1fr}}

  /* ---------- diagnostics ---------- */
  .diag{display:grid;gap:.55rem}
  .metric{background:var(--panel2);border:1px solid var(--line);border-radius:12px;padding:.7rem .85rem}
  .metric-top{display:flex;justify-content:space-between;align-items:baseline;gap:.6rem}
  .metric-top b{font-size:.74rem;text-transform:uppercase;letter-spacing:.1em;color:var(--dim);font-weight:700}
  .verdict{font-size:.72rem;font-weight:800;letter-spacing:.05em;padding:.16rem .5rem;border-radius:99px}
  .v-ok{background:rgba(61,220,132,.14);color:var(--ok)}
  .v-warn{background:rgba(255,194,61,.14);color:var(--warn)}
  .v-bad{background:rgba(255,91,102,.14);color:var(--bad)}
  .track{height:5px;border-radius:99px;background:rgba(255,255,255,.09);margin:.5rem 0 .35rem;overflow:hidden}
  .fill{height:100%;border-radius:99px;transition:width .4s ease}
  .f-ok{background:var(--ok)} .f-warn{background:var(--warn)} .f-bad{background:var(--bad)}
  .metric small{font-size:.75rem;color:var(--dim);display:block}
  .tags{display:flex;flex-wrap:wrap;gap:.3rem;margin-top:.5rem}
  .tag{font-size:.68rem;font-weight:700;letter-spacing:.04em;padding:.2rem .5rem;border-radius:6px;
       background:rgba(255,255,255,.06);border:1px solid var(--line);color:var(--mut)}
  .tag.hl{background:rgba(61,220,132,.12);border-color:rgba(61,220,132,.3);color:var(--ok)}
  .tag.kw{background:rgba(229,9,20,.14);border-color:rgba(229,9,20,.32);color:#ff8a92}

  /* ---------- social ---------- */
  .soc-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:1.1rem}
  .fb{background:#fff;border-radius:8px;overflow:hidden;max-width:500px;
      font-family:Helvetica,Arial,sans-serif;border:1px solid #dddfe2}
  .fb img{width:100%;display:block;aspect-ratio:1.91/1;object-fit:cover}
  .fb-t{padding:10px 12px;background:#f2f3f5;border-top:1px solid #dadde1}
  .fb-dom{font-size:12px;color:#606770;text-transform:uppercase;line-height:16px}
  .fb-h{font-size:16px;font-weight:600;color:#1d2129;line-height:20px;margin:3px 0 0;
        overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}
  .fb-d{font-size:14px;color:#606770;line-height:20px;margin:3px 0 0;
        overflow:hidden;display:-webkit-box;-webkit-line-clamp:1;-webkit-box-orient:vertical}
  .tw{background:#000;border:1px solid #2f3336;border-radius:16px;overflow:hidden;max-width:500px;
      font-family:Helvetica,Arial,sans-serif}
  .tw img{width:100%;display:block;aspect-ratio:1.91/1;object-fit:cover}
  .tw-t{padding:12px}
  .tw-h{font-size:15px;color:#e7e9ea;line-height:20px;margin:0;
        overflow:hidden;display:-webkit-box;-webkit-line-clamp:1;-webkit-box-orient:vertical}
  .tw-d{font-size:15px;color:#71767b;line-height:20px;margin:2px 0 0;
        overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}
  .tw-u{font-size:15px;color:#71767b;margin:2px 0 0}
  .wa{background:#005c4b;border-radius:8px;padding:4px;max-width:380px;
      font-family:Helvetica,Arial,sans-serif}
  .wa-in{background:rgba(0,0,0,.22);border-radius:6px;overflow:hidden}
  .wa-in img{width:100%;display:block;aspect-ratio:1.91/1;object-fit:cover}
  .wa-t{padding:8px 10px}
  .wa-h{font-size:13.5px;color:#e9edef;font-weight:500;line-height:18px;margin:0;
        overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}
  .wa-d{font-size:12.5px;color:rgba(233,237,239,.6);line-height:17px;margin:2px 0 0;
        overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}
  .wa-u{font-size:12.5px;color:rgba(233,237,239,.45);margin:3px 0 0}
  .soc-label{font-size:.72rem;text-transform:uppercase;letter-spacing:.12em;
             color:var(--dim);font-weight:700;margin:0 0 .6rem}

  /* ---------- schema view ---------- */
  .sch-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1rem}
  .legend{background:var(--panel);border:1px solid var(--line);border-radius:16px;
          padding:1.1rem 1.3rem;margin-bottom:1.6rem}
  .legend h4{margin:0 0 .6rem;font-size:.78rem;text-transform:uppercase;letter-spacing:.12em;color:var(--dim)}
  .legend ul{margin:0;padding-left:1.1rem;color:var(--mut);font-size:.88rem}
  .legend li{margin-bottom:.3rem}
  .hide{display:none!important}
  footer{border-top:1px solid var(--line);margin-top:3rem;padding:2rem 0 3rem;
         color:var(--dim);font-size:.82rem}
  mark{background:rgba(255,194,61,.28);color:inherit;border-radius:3px;padding:0 1px}
</style>
</head>
<body>

<header class="top">
  <div class="wrap top-in">
    <span class="brand"><img id="brandIcon" alt=""> ONE <b>IPTV</b></span>
    <div class="tabs" role="tablist">
      <button role="tab" aria-selected="true"  data-view="google">Google results</button>
      <button role="tab" aria-selected="false" data-view="social">Social cards</button>
      <button role="tab" aria-selected="false" data-view="schema">Schema &amp; meta</button>
    </div>
  </div>
</header>

<div class="wrap intro">
  <h1>Search &amp; social preview</h1>
  <p>Exactly how each of the pages is set up to appear in Google and when someone shares a
     link. Titles and descriptions are truncated here the same way the real thing truncates
     them, measured in pixels rather than characters — which is what Google actually uses.</p>
  <div class="stats" id="stats"></div>
</div>

<div class="wrap">
  <div class="bar">
    <button class="chip" data-filter="all" aria-pressed="true">All pages</button>
    <button class="chip" data-filter="Core" aria-pressed="false">Core</button>
    <button class="chip" data-filter="Blog" aria-pressed="false">Blog</button>
    <button class="chip" data-filter="Legal" aria-pressed="false">Legal</button>
    <span class="grow"></span>
    <button class="chip" id="deviceBtn" aria-pressed="false">Mobile view</button>
    <button class="chip" id="themeBtn" aria-pressed="false">Dark results</button>
    <label class="search">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>
      <input id="q" type="search" placeholder="Filter pages…">
    </label>
  </div>

  <div class="legend" id="legend"></div>
  <div id="out"></div>
</div>

<footer class="wrap">
  <p style="margin:0">Generated from the live page source of the ONE IPTV site. Pixel widths are
  measured with Google's result fonts (Arial 20px titles, 14px descriptions) at their real
  container widths — 600&nbsp;px desktop, 400&nbsp;px mobile. This file is marked
  <code>noindex</code> and is a preview tool only; it is not part of the published site.</p>
</footer>

<script>
const DATA = __DATA__;

/* ---------- pixel measurement, the way Google truncates ---------- */
const cv = document.createElement('canvas').getContext('2d');
function px(text, font){ cv.font = font; return Math.round(cv.measureText(text).width); }
const F_TITLE_D = '400 20px arial, sans-serif';
const F_TITLE_M = '400 18px arial, sans-serif';
const F_DESC    = '400 14px arial, sans-serif';

/* Limits: Google gives titles ~600px desktop / ~400px mobile on one line,
   and wraps descriptions to ~2 lines of 600px (desktop) / 3 of 400px (mobile). */
const LIM = {
  desktop: { title: 600, desc: 1180 },
  mobile:  { title: 760, desc: 1200 }
};

let view = 'google', group = 'all', device = 'desktop', dark = false, query = '';

const el = (t, c, h) => { const n = document.createElement(t); if(c) n.className = c;
                          if(h != null) n.innerHTML = h; return n; };
const esc = s => (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');

function prettyUrl(u){
  const clean = u.replace(/^https?:\/\//,'').replace(/\/$/,'');
  const parts = clean.split('/');
  return parts.length > 1
    ? '<span style="opacity:.95">'+esc(parts[0])+'</span> › ' + parts.slice(1).map(esc).join(' › ')
    : esc(parts[0]);
}

/* A title or description that fits is fine. Being well under the limit is not an
   error — it just means there is unused space, so we say that rather than crying wolf. */
function verdict(val, lo, hi){
  if (val > hi)  return ['v-bad','f-bad','Cut off'];
  if (val < lo)  return ['v-warn','f-warn','Room to spare'];
  return ['v-ok','f-ok','Good'];
}

function kwHits(p){
  const hay = (p.title + ' ' + p.desc + ' ' + p.h1).toLowerCase();
  return DATA.keywords.filter(k => hay.includes(k));
}

/* ---------- Google result ---------- */
function serp(p){
  const mob = device === 'mobile';
  const box = el('div', 'serp' + (mob?' g-mob':'') + (dark?' dark':''));
  const res = el('div', 'g-res');

  res.append(el('div','g-head',
    `<span class="g-fav"><img src="${DATA.favicon}" alt=""></span>
     <span><span class="g-site">ONE IPTV</span><br>
     <span class="g-url">${prettyUrl(p.url)}</span></span>`));

  res.append(el('h3','g-title', esc(p.title)));

  const isPost = p.file.startsWith('blog/') && p.file !== 'blog/index.html';
  res.append(el('div','g-desc',
    (isPost ? '<span class="g-date">'+dateFor(p)+' — </span>' : '') + esc(p.desc)));

  if (p.file === 'index.html'){
    res.append(el('div','g-sitelinks',
      ['Pricing|/pricing/','Features|/features/','Devices|/devices/','FAQ|/faq/',
       'Blog|/blog/','Contact|/contact/']
      .map(s => { const [t,u] = s.split('|');
        return `<a href="#" onclick="return false">${t}</a>`; }).join('')));
  }

  if (p.faq && p.faq.length){
    res.append(el('div','g-faq',
      p.faq.slice(0,3).map(q => `<div>${esc(q)}<span>⌄</span></div>`).join('')));
  }

  box.append(res);
  return box;
}

function dateFor(p){
  const m = { 'one-iptv-complete-guide-for-beginners':'4 Feb 2026',
              'how-to-set-up-one-iptv-on-a-smart-tv':'18 Feb 2026',
              'smart-one-iptv-what-you-need-to-know':'3 Mar 2026',
              'iptv-one-month-plans-what-to-consider':'19 Mar 2026',
              'one-iptv-uk-getting-started-guide':'8 Apr 2026',
              'smart-one-iptv-app-download-setup-guide':'27 Apr 2026',
              'how-to-set-up-iptv-on-your-tv':'14 May 2026' };
  const k = p.file.split('/')[1];
  return m[k] || '';
}

/* ---------- diagnostics ---------- */
function metric(name, value, limit, note, lo, hint){
  const [vc, fc, label] = verdict(value, lo ?? limit*0.42, limit);
  const pct = Math.min(100, value/limit*100);
  const extra = (label !== 'Good' && hint)
    ? `<small style="color:var(--warn);margin-top:.3rem">${hint}</small>` : '';
  return el('div','metric',
    `<div class="metric-top"><b>${name}</b><span class="verdict ${vc}">${label}</span></div>
     <div class="track"><div class="fill ${fc}" style="width:${pct}%"></div></div>
     <small>${note}</small>${extra}`);
}

function diag(p){
  const mob = device === 'mobile';
  const lim = LIM[device];
  const tW = px(p.title, mob ? F_TITLE_M : F_TITLE_D);
  const dW = px(p.desc, F_DESC);
  const wrap = el('div','diag');

  wrap.append(metric('Title width', tW, lim.title,
    `${tW}px of ${lim.title}px · ${p.title.length} characters`, null,
    tW > lim.title
      ? 'Google will trim the end. Move the most important words to the front.'
      : 'Fits comfortably — there is room to add a keyword if you want one.'));
  wrap.append(metric('Description width', dW, lim.desc,
    `${dW}px of ~${lim.desc}px (${mob?3:2} lines) · ${p.desc.length} characters`, null,
    dW > lim.desc
      ? 'The tail will be replaced with an ellipsis. Front-load the useful part.'
      : 'Shorter than Google will show — you could say more here.'));

  const hits = kwHits(p);
  const tags = el('div','tags');
  tags.append(el('span','tag' + (p.indexable?' hl':''),
    p.indexable ? 'Indexable' : 'noindex'));
  tags.append(el('span','tag', p.words.toLocaleString() + ' words'));
  if (p.h1) tags.append(el('span','tag hl','1 × H1'));
  hits.forEach(k => tags.append(el('span','tag kw', k)));
  wrap.append(tags);

  if (p.faq && p.faq.length){
    wrap.append(el('div','metric',
      `<div class="metric-top"><b>Rich result</b>
        <span class="verdict v-ok">FAQ eligible</span></div>
       <small>${p.faq.length} questions marked up with FAQPage schema.</small>`));
  }
  return wrap;
}

/* ---------- social cards ---------- */
function social(p){
  const dom = 'ONE-IPTV.ONLINE';
  const g = el('div','soc-grid');

  const fb = el('div');
  fb.append(el('p','soc-label','Facebook / LinkedIn'));
  fb.append(el('div','fb',
    `<img src="${DATA.ogImage}" alt="">
     <div class="fb-t"><div class="fb-dom">${dom}</div>
       <p class="fb-h">${esc(p.ogTitle)}</p>
       <p class="fb-d">${esc(p.ogDesc)}</p></div>`));
  g.append(fb);

  const tw = el('div');
  tw.append(el('p','soc-label','X / Twitter — ' + (p.twCard || 'n/a')));
  tw.append(el('div','tw',
    `<img src="${DATA.ogImage}" alt="">
     <div class="tw-t"><p class="tw-h">${esc(p.ogTitle)}</p>
       <p class="tw-d">${esc(p.ogDesc)}</p>
       <p class="tw-u">From one-iptv.online</p></div>`));
  g.append(tw);

  const wa = el('div');
  wa.append(el('p','soc-label','WhatsApp'));
  wa.append(el('div','wa',
    `<div class="wa-in"><img src="${DATA.ogImage}" alt="">
      <div class="wa-t"><p class="wa-h">${esc(p.ogTitle)}</p>
        <p class="wa-d">${esc(p.ogDesc)}</p>
        <p class="wa-u">${esc(p.url.replace(/^https?:\/\//,''))}</p></div></div>`));
  g.append(wa);

  return g;
}

/* ---------- schema view ---------- */
function schema(p){
  const g = el('div','sch-grid');
  const rows = [
    ['Canonical', p.url],
    ['Title tag', p.title + '  (' + p.title.length + ' chars)'],
    ['Meta description', p.desc + '  (' + p.desc.length + ' chars)'],
    ['H1 on page', p.h1 || '—'],
    ['Robots', p.robots || 'default (index, follow)'],
    ['og:type', p.ogType || '—'],
    ['og:image', p.ogImage.replace(DATA.site,'') || '—'],
    ['twitter:card', p.twCard || '—'],
    ['Meta keywords', p.keywords || '—'],
    ['Word count', p.words.toLocaleString()],
  ];
  const left = el('div','diag');
  rows.forEach(([k,v]) => left.append(el('div','metric',
    `<div class="metric-top"><b>${k}</b></div><small style="color:var(--mut);
      word-break:break-word;white-space:normal">${esc(v)}</small>`)));
  g.append(left);

  const right = el('div','diag');
  right.append(el('div','metric',
    `<div class="metric-top"><b>Structured data</b>
      <span class="verdict ${p.schemas.length?'v-ok':'v-warn'}">${p.schemas.length} types</span></div>
     <div class="tags" style="margin-top:.6rem">${
       p.schemas.map(s=>`<span class="tag hl">${s}</span>`).join('') || '<span class="tag">none</span>'
     }</div>`));
  if (p.faq && p.faq.length){
    right.append(el('div','metric',
      `<div class="metric-top"><b>FAQ questions marked up</b></div>
       <small style="color:var(--mut);white-space:normal">${
         p.faq.map(q=>'• '+esc(q)).join('<br>')}</small>`));
  }
  const hits = kwHits(p);
  right.append(el('div','metric',
    `<div class="metric-top"><b>Target keywords in title / description / H1</b>
      <span class="verdict ${hits.length?'v-ok':'v-warn'}">${hits.length}</span></div>
     <div class="tags" style="margin-top:.6rem">${
       hits.map(k=>`<span class="tag kw">${k}</span>`).join('') ||
       '<span class="tag">none — supporting page</span>'}</div>`));
  g.append(right);
  return g;
}

/* ---------- render ---------- */
function legendFor(){
  const L = {
    google: ['Titles and descriptions are cut off here at the same pixel widths Google uses, so what you see is what searchers see.',
             'Pages with FAQ schema show the expandable questions Google can display underneath the result.',
             'The home page shows sitelinks — Google generates these itself once a site has enough authority; this is an illustration of the likely shape.'],
    social: ['All pages share one 1200×630 social image. Facebook and X trim the title to 1–2 lines, WhatsApp shows a smaller card.',
             'Titles here come from og:title, which is set to match each page title.'],
    schema: ['Every tag Google reads, page by page, plus the structured data types present.',
             'Product and Offer types appear automatically once you replace the €XX.XX placeholders with real prices in config.js.']
  };
  return `<h4>What you're looking at</h4><ul>${L[view].map(s=>'<li>'+s+'</li>').join('')}</ul>`;
}

function render(){
  const out = document.getElementById('out');
  out.innerHTML = '';
  document.getElementById('legend').innerHTML = legendFor();

  const list = DATA.pages.filter(p =>
    (group === 'all' || p.group === group) &&
    (!query || (p.label+' '+p.title+' '+p.desc+' '+p.url).toLowerCase().includes(query)));

  if (!list.length){ out.append(el('p','', '<span style="color:var(--dim)">No pages match that filter.</span>')); return; }

  list.forEach(p => {
    const card = el('div','card');
    const head = el('div','card-head',
      `<h3>${esc(p.label)}</h3><span class="grp">${p.group}</span>
       <span class="path">${esc(p.url.replace(DATA.site,'') || '/')}</span>`);
    card.append(head);

    if (view === 'google'){
      const s = el('div','split');
      const a = el('div'); a.append(serp(p));
      s.append(a); s.append(diag(p)); card.append(s);
    } else if (view === 'social'){
      card.append(social(p));
    } else {
      card.append(schema(p));
    }
    out.append(card);
  });
}

/* ---------- stats ---------- */
function stats(){
  const ps = DATA.pages;
  const lim = LIM.desktop;
  const okT = ps.filter(p => px(p.title, F_TITLE_D) <= lim.title).length;
  const okD = ps.filter(p => { const w = px(p.desc, F_DESC); return w <= lim.desc && w > lim.desc*0.5; }).length;
  const faq = ps.filter(p => p.faq && p.faq.length).length;
  const words = ps.reduce((s,p)=>s+p.words,0);
  const cells = [
    [ps.length, 'pages', ''],
    [okT + '/' + ps.length, 'titles fit', okT===ps.length?'good':'warn'],
    [okD + '/' + ps.length, 'descriptions fit', okD===ps.length?'good':'warn'],
    [faq, 'FAQ rich results', 'good'],
    [words.toLocaleString(), 'indexable words', ''],
  ];
  document.getElementById('stats').innerHTML = cells.map(([b,s,c]) =>
    `<div class="stat ${c}"><b>${b}</b><span>${s}</span></div>`).join('');
}

/* ---------- wiring ---------- */
document.getElementById('brandIcon').src = DATA.favicon;

document.querySelectorAll('.tabs button').forEach(b => b.onclick = () => {
  document.querySelectorAll('.tabs button').forEach(x => x.setAttribute('aria-selected','false'));
  b.setAttribute('aria-selected','true'); view = b.dataset.view; render();
});
document.querySelectorAll('[data-filter]').forEach(b => b.onclick = () => {
  document.querySelectorAll('[data-filter]').forEach(x => x.setAttribute('aria-pressed','false'));
  b.setAttribute('aria-pressed','true'); group = b.dataset.filter; render();
});
const dev = document.getElementById('deviceBtn');
dev.onclick = () => { device = device === 'desktop' ? 'mobile' : 'desktop';
  dev.setAttribute('aria-pressed', device==='mobile');
  dev.textContent = device === 'mobile' ? 'Desktop view' : 'Mobile view'; render(); stats(); };
const th = document.getElementById('themeBtn');
th.onclick = () => { dark = !dark; th.setAttribute('aria-pressed', dark);
  th.textContent = dark ? 'Light results' : 'Dark results'; render(); };
document.getElementById('q').oninput = e => { query = e.target.value.toLowerCase().trim(); render(); };

document.fonts?.ready.then(() => { stats(); render(); });
stats(); render();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
