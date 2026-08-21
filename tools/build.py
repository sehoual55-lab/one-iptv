#!/usr/bin/env python3
"""Build the ONE IPTV static site."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from shell import (page, icon, ld, SITE, BRAND, PHONE_DISPLAY, PHONE_TEL, EMAIL, NAV)
import content as C
from articles import ARTICLES, article_page

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def emit(path, html):
    """path '' -> index.html, 'pricing' -> pricing/index.html"""
    out = os.path.join(ROOT, path, "index.html") if path else os.path.join(ROOT, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("  ✓ /%s" % (path + "/" if path else ""))


def emit_raw(name, text):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        f.write(text)
    print("  ✓ /%s" % name)


def breadcrumb(trail):
    """trail = [(label, href|None)]"""
    lis = []
    for label, href in trail:
        lis.append(f'<li><a href="{href}">{label}</a></li>' if href else f"<li>{label}</li>")
    return f'<ol class="breadcrumb">{"".join(lis)}</ol>'


def bc_schema(trail):
    items = []
    for i, (label, href) in enumerate(trail, 1):
        entry = {"@type": "ListItem", "position": i, "name": label}
        if href:
            entry["item"] = SITE + href
        items.append(entry)
    return json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList",
                       "itemListElement": items}, ensure_ascii=False)


# ============================================================ SCHEMA =======
ORG_SCHEMA = json.dumps({
    "@context": "https://schema.org",
    "@type": "Organization",
    "@id": SITE + "/#organization",
    "name": BRAND,
    "alternateName": "One IPTV",
    "url": SITE + "/",
    "logo": {"@type": "ImageObject", "url": SITE + "/assets/img/favicon.svg",
             "width": 64, "height": 64},
    "image": SITE + "/assets/img/og-image.svg",
    "description": "ONE IPTV is a modern IPTV service for compatible Smart TVs, streaming "
                   "devices and mobile, with flexible 12 to 24 month plans and human support.",
    "contactPoint": [{
        "@type": "ContactPoint",
        "contactType": "customer support",
        "url": C.WA_URL,
        "availableLanguage": ["English"],
        "areaServed": ["GB", "US", "IE", "EU"]
    }],
    "sameAs": [C.WA_URL]
}, ensure_ascii=False)

WEBSITE_SCHEMA = json.dumps({
    "@context": "https://schema.org",
    "@type": "WebSite",
    "@id": SITE + "/#website",
    "url": SITE + "/",
    "name": BRAND,
    "publisher": {"@id": SITE + "/#organization"},
    "inLanguage": "en"
}, ensure_ascii=False)

SERVICE_SCHEMA = json.dumps({
    "@context": "https://schema.org",
    "@type": "Service",
    "name": "ONE IPTV streaming service",
    "serviceType": "IPTV streaming service",
    "provider": {"@id": SITE + "/#organization"},
    "areaServed": ["GB", "US", "IE", "EU"],
    "audience": {"@type": "Audience", "audienceType": "Smart TV and streaming device owners"},
    "description": "IPTV access for compatible Smart TVs, Android TV, Fire TV, mobile devices "
                   "and TV boxes, available on 12 to 24 month plans.",
    "url": SITE + "/pricing/"
}, ensure_ascii=False)


# ============================================================== HOME =======
def build_home():
    hero = f"""<section class="hero">
  <div class="wrap">
    <div class="hero-grid">
      <div class="hero-copy">
        <span class="eyebrow">Premium IPTV service</span>
        <h1>One IPTV — <span class="accent">Premium IPTV Service</span> for Smart TVs &amp; Devices</h1>
        <p class="hero-sub">Discover a modern IPTV experience with live entertainment, sports,
           movies and TV content on compatible devices — set up in minutes, on the screen you
           already own.</p>
        <div class="hero-cta">
          <a class="btn btn--primary btn--lg" href="/pricing/">View Plans {icon("arrow-right")}</a>
          <button class="btn btn--ghost btn--lg" type="button" data-open-checkout>Get Started</button>
        </div>
        <ul class="trust-line">
          <li>Simple</li><li>Fast</li><li>Flexible</li><li>Multi-Device</li>
        </ul>
        <p style="margin-top:1.6rem;font-size:.92rem">
          Questions before you order? Message us on
          <a href="{C.WA_URL}" data-whatsapp-link target="_blank" rel="noopener"
             style="color:var(--red-bright);font-weight:650">WhatsApp</a>
        </p>
      </div>

      <div class="hero-visual">
        <div class="hero-visual__glow" aria-hidden="true"></div>
        <div class="tv">
          <div class="tv__screen">
            <img src="/assets/img/hero-screen.svg" width="1280" height="800" fetchpriority="high"
                 decoding="async"
                 alt="Illustration of the ONE IPTV interface on a television, showing a featured
                      banner and rows of content cards on a dark red-lit background">
            <span class="tv__scan" aria-hidden="true"></span>
          </div>
        </div>
        <div class="tv__stand" aria-hidden="true"></div>

        <div class="hero-badge hero-badge--a">
          <span class="hero-badge__icon">{icon("cast")}</span>
          <span><strong>Multi-device</strong><small>TV · phone · tablet · box</small></span>
        </div>
        <div class="hero-badge hero-badge--b">
          <span class="hero-badge__icon">{icon("clock")}</span>
          <span><strong>Setup in minutes</strong><small>Guided, step by step</small></span>
        </div>
      </div>
    </div>
  </div>
</section>
"""

    intro = f"""<section class="section section--tight">
  <div class="wrap">
    <div class="grid grid-2" style="align-items:center;gap:clamp(1.8rem,5vw,3.5rem)">
      <div class="reveal">
        <span class="eyebrow">About</span>
        <h2>Television that follows the screen you are sitting in front of</h2>
        <p>ONE IPTV delivers television over your internet connection instead of a dish or an
           aerial. That single change is what makes everything else possible: the same account
           works on the television in the living room, the tablet in the kitchen and the phone
           on the train, and getting started means installing an app rather than booking an
           engineer.</p>
        <p>We keep the commercial side just as simple. Four plans — Bronze, Gold, Platinum and
           Exclusive — running from 12 up to 24 months, with the longer terms adding bonus months
           free. If you would like a shorter term to
           <a href="/blog/iptv-one-month-plans-what-to-consider/">try it first</a>, just ask.</p>
        <p style="margin-bottom:0">If you would rather talk it through than read about it, message
           us on <a href="{C.WA_URL}" data-whatsapp-link target="_blank" rel="noopener">WhatsApp</a>.</p>
      </div>
      <div class="grid" style="gap:1rem" >
        <div class="card reveal">
          <div class="card__icon">{icon("sparkle")}</div>
          <h3>Built for real living rooms</h3>
          <p>Menus that make sense on a TV remote, not just a mouse. Big targets, clear rows,
             and nothing hidden three levels deep.</p>
        </div>
        <div class="card reveal">
          <div class="card__icon">{icon("headset")}</div>
          <h3>Real people on WhatsApp</h3>
          <p>Setup problems are far easier to solve in a quick chat. Message us and we will stay
             with it until the picture is on the screen.</p>
        </div>
        <div class="card reveal">
          <div class="card__icon">{icon("shield")}</div>
          <h3>No card details on this site</h3>
          <p>Our order form collects your name, WhatsApp number and chosen plan — nothing more.
             Payment is completed through a secure provider or with our team.</p>
        </div>
      </div>
    </div>
  </div>
</section>
"""

    tl = [
        ("sliders", "Choose a plan",
         "Pick Bronze, Gold, Platinum or Exclusive — 12 to 24 months, and set how many devices "
         "stream at once."),
        ("whatsapp", "Get your details",
         "We send your credentials on WhatsApp with a setup guide written for the device you "
         "told us about."),
        ("download", "Install an IPTV app",
         "Download a compatible player from your device's own app store — Smart TV, Android "
         "TV, Fire TV or mobile."),
        ("play", "Enter and watch",
         "Type the details in once. The app builds your list, and from then on you just open "
         "it."),
    ]
    tl_cards = "".join(f"""
      <li class="tl-step reveal">
        <div class="tl-step__top">
          <span class="tl-num">{i}</span>
          <span class="tl-line" aria-hidden="true"></span>
        </div>
        <div class="tl-card">
          <span class="tl-icon">{icon(ic)}</span>
          <h3>{title}</h3>
          <p>{body}</p>
        </div>
      </li>""" for i, (ic, title, body) in enumerate(tl, 1))

    steps = f"""<section class="section" id="how-it-works">
  <div class="glow glow--dim" style="width:560px;height:560px;top:-140px;left:-180px;opacity:.4"></div>
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">How it works</span>
      <h2>From order to first channel in four steps</h2>
      <p>The same path applies whether you are setting up a Smart TV, a Fire TV Stick or a phone.</p>
    </div>
    <ol class="timeline">{tl_cards}
    </ol>
    <p class="center mt-lg" style="margin-bottom:0">
      <a class="btn btn--outline" href="/blog/one-iptv-complete-guide-for-beginners/">
        Read the full beginner's guide {icon("arrow-right")}</a>
    </p>
  </div>
</section>
"""

    extra = ld(ORG_SCHEMA) + ld(WEBSITE_SCHEMA) + ld(SERVICE_SCHEMA) + \
        ld(C.faq_schema(C.FAQ_MAIN[:6]))

    body = (hero + C.strip_section() + C.film_marquee() + intro + C.features_section() + steps +
            C.devices_section() +
            C.brand_strip_section("Works with the brands you already own") +
            C.pricing_section() +
            C.faq_section(C.FAQ_MAIN[:6], heading="ONE IPTV — Common Questions",
                          intro="A quick pass over what people ask most. The "
                                "<a href='/faq/' style='color:var(--red-bright)'>full FAQ</a> "
                                "goes deeper.") +
            C.blog_preview() + C.contact_section())

    emit("", page(
        title="ONE IPTV | Premium IPTV Service",
        description="Discover ONE IPTV, a modern IPTV experience for compatible Smart TVs and "
                    "streaming devices. Explore plans, features, setup guides and support.",
        path="/",
        keywords="one iptv, smart one iptv, iptv one month, one iptv uk, iptv app, "
                 "iptv app for tv, ip smart iptv, iptv tv smart",
        body=body, extra_head=extra))


# ========================================================== FEATURES =======
def build_features():
    trail = [("Home", "/"), ("Features", None)]
    hero = f"""<section class="page-hero">
  <div class="wrap">
    {breadcrumb(trail)}
    <span class="eyebrow">Features</span>
    <h1>ONE IPTV Features</h1>
    <p class="lead">Everything ONE IPTV does is aimed at one outcome: getting a picture on the
       screen quickly, and keeping it there. Here is what that looks like in practice.</p>
  </div>
</section>
"""
    deep = f"""<section class="section section--tight">
  <div class="wrap" style="max-width:900px">
    <h2>What "premium" actually means here</h2>
    <p>Plenty of IPTV sites lead with numbers — channel counts, uptime percentages, stream
       totals. We have deliberately left those off this page, because the honest answer is that
       what any given customer can watch depends on their plan, their connection and what the
       service carries at the time. Publishing a figure we cannot stand behind would tell you
       nothing useful.</p>
    <p>What we can describe is the experience. A player that opens fast and remembers where you
       were. A channel list that is navigable with a remote, not just a mouse. Adaptive playback
       that steps down gracefully when the Wi-Fi wobbles instead of freezing. And a support line
       staffed by people who have set this up on the same television you own.</p>

    <h2>Quality and playback</h2>
    <p>Streams are delivered in HD and higher quality where the source and your connection allow.
       That caveat matters: no service can deliver a higher-quality picture than the source
       provides, and none can beat the physics of your broadband. In practice, most households
       on a stable 20 Mbps connection get a comfortable HD experience on one screen, with more
       headroom needed if several people watch at once.</p>
    <div class="callout">
      <p><strong>A practical tip.</strong> If your television sits near the router, run an
        Ethernet cable to it. It is the single change that fixes more buffering complaints than
        anything else we suggest — Wi-Fi across a house is the weak link far more often than the
        broadband itself.</p>
    </div>

    <h2>Working across devices</h2>
    <p>The account is not tied to a box. Install a compatible <strong>IPTV app</strong> on the
       television, then the same details on a phone or tablet, and you can move between them.
       Your plan sets how many streams can run at the same moment; installing on additional
       devices does not consume that allowance by itself. See the
       <a href="/devices/">devices page</a> for the full compatibility picture.</p>

    <h2>Setup, honestly described</h2>
    <p>Most people are watching within about ten minutes: install a player, type in the details
       we send, wait for the list to load. Some setups take longer — an older Smart TV with a
       restricted app store, for instance, may need a cheap streaming stick to work around it.
       We would rather tell you that up front than have you discover it after paying. Our
       <a href="/blog/how-to-set-up-iptv-on-your-tv/">setup guide</a> covers both the smooth
       path and the awkward one.</p>
  </div>
</section>
"""
    body = (hero + C.features_section(heading="Why Choose ONE IPTV?") + deep +
            C.strip_section() + C.film_marquee() + C.pricing_section(with_switch=False) +
            C.contact_section())
    emit("features", page(
        title="ONE IPTV Features | Live TV, HD Streaming & Smart TV Support",
        description="Explore ONE IPTV features: live TV, HD and higher-quality streaming, Smart "
                    "TV compatibility, easy setup, multi-device support and flexible plans.",
        path="/features/",
        keywords="one iptv features, iptv app, iptv tv smart, smart one iptv",
        body=body, extra_head=ld(bc_schema(trail)) + ld(SERVICE_SCHEMA)))


# ========================================================== CHANNELS =======
def build_channels():
    trail = [("Home", "/"), ("Channels", None)]
    cards = "".join(f"""
      <article class="card reveal">
        <div class="card__icon">{icon(ic)}</div>
        <h3>{name}</h3>
        <p>{body}</p>
      </article>""" for ic, name, body in [
        ("tv", "Live channels", "Programming as it airs, arranged into categories you can scan "
                                "quickly from the sofa."),
        ("play", "On-demand titles", "Films and episodic series you can start whenever, rather "
                                     "than waiting for a schedule."),
        ("globe", "International options", "Content from a range of regions, which is often the "
                                           "reason people move to IPTV in the first place."),
        ("users", "Family viewing", "Categories suitable for younger viewers, kept separate so "
                                    "they are easy to find."),
    ])
    hero = f"""<section class="page-hero">
  <div class="wrap">
    {breadcrumb(trail)}
    <span class="eyebrow">Channels</span>
    <h1>Explore Your Entertainment</h1>
    <p class="lead">ONE IPTV organises what is available into clear categories — live, on demand,
       sport, news, family — so finding something to watch takes seconds rather than scrolling.</p>
  </div>
</section>
"""
    honesty = f"""<section class="section section--tight">
  <div class="wrap" style="max-width:880px">
    <h2>Why we do not publish a channel count</h2>
    <p>It is the first thing many IPTV sites shout about, and it is the least reliable number on
       the page. Counts get inflated by duplicates, by regional variants of the same feed, and by
       entries that have not worked in months. More importantly, what is available genuinely
       changes — and what <em>you</em> can access depends on your plan and your region.</p>
    <p>So rather than print a figure, we will answer the specific question. Tell us what you
       actually want to watch, and we will tell you plainly whether the service carries it before
       you spend anything. Message us on
       <a href="{C.WA_URL}" data-whatsapp-link target="_blank" rel="noopener">WhatsApp</a>
       or use the <a href="/contact/">contact form</a>.</p>
    <div class="callout">
      <p><strong>On broadcaster names and logos.</strong> You will not find third-party network
        logos anywhere on this site. ONE IPTV is independent and has no affiliation with, or
        endorsement from, any television network or broadcaster. Category artwork on this page is
        our own illustration.</p>
    </div>
  </div>
</section>
"""
    body = (hero + C.film_marquee() +
            f"""<section class="section section--tight"><div class="wrap">
              <div class="grid grid-4">{cards}</div></div></section>""" +
            honesty + C.pricing_section(with_switch=False) + C.contact_section())
    emit("channels", page(
        title="ONE IPTV Channels & Categories | Live TV, Sports, Movies",
        description="Browse the content categories available through ONE IPTV — live TV, sports, "
                    "movies, series, entertainment, news and family viewing on compatible devices.",
        path="/channels/",
        keywords="one iptv channels, iptv app, live tv, iptv tv smart",
        body=body, extra_head=ld(bc_schema(trail))))


# =========================================================== PRICING =======
def build_pricing():
    trail = [("Home", "/"), ("Pricing", None)]
    hero = f"""<section class="page-hero">
  <div class="wrap">
    {breadcrumb(trail)}
    <span class="eyebrow">Pricing</span>
    <h1>ONE IPTV Plans &amp; Pricing</h1>
    <p class="lead">Four plans — Bronze, Gold, Platinum and Exclusive — from 12 to 24 months. The
       longer the term, the better the value, and the top plans add bonus months free.</p>
    <p style="margin-top:1.4rem">
      <a class="btn btn--primary btn--lg" href="#pricing">See the plans {icon("arrow-right")}</a>
      <a class="btn btn--ghost btn--lg" href="{C.WA_URL}" data-whatsapp-link target="_blank"
         rel="noopener" style="margin-left:.5rem">{icon("whatsapp")}WhatsApp</a>
    </p>
  </div>
</section>
"""
    explain = f"""<section class="section section--tight">
  <div class="wrap" style="max-width:900px">
    <h2>How to choose your plan</h2>
    <p>All four plans carry the same service — the difference is the length and, on the top plan,
       how much content is included. <strong>Bronze</strong> (12 months) is the entry point.
       <strong>Gold</strong> (15 months, plus 3 free) is the most popular balance of price and
       term. <strong>Platinum</strong> matches Gold's term with priority handling, and
       <strong>Exclusive</strong> (24 months, plus 3 free) gives the lowest effective monthly rate
       and the widest content.</p>
    <p>Not sure you want to commit for a year yet? Our guide on
       <a href="/blog/iptv-one-month-plans-what-to-consider/">trying IPTV short-term</a> explains
       what to test first, and you can always ask us about a shorter starter term on WhatsApp.</p>

    <h2>The connection control</h2>
    <p>Every plan has a + / − control for how many devices stream at the same time. The first
       connection is the plan price; each additional connection is 15% cheaper. Set it to match
       your household and the total updates instantly.</p>

    <h2>What every plan includes</h2>
    <ul>
      <li>Thousands of live channels plus a large films and series library.</li>
      <li>4K / FHD / HD quality where the source and your connection allow.</li>
      <li>A TV guide (EPG) and compatibility with all major devices.</li>
      <li>24/7 technical support and instant delivery of your details.</li>
    </ul>

    <h2>How payment works</h2>
    <p>This website never asks for card details. When you submit the order form, we collect only
       your name, WhatsApp number and chosen plan — enough to confirm the order and send your
       setup details. Payment itself is completed either through a secure, PCI-compliant payment
       provider or arranged directly with our support team. If you see any website asking you to
       type card numbers into a plain form, that is a reason to close the tab, here or anywhere
       else.</p>
  </div>
</section>
"""
    faq_items = [C.FAQ_MAIN[4], C.FAQ_EXTRA[1], C.FAQ_EXTRA[3], C.FAQ_EXTRA[4]]
    body = (hero + C.pricing_section(heading="Choose your plan") + explain +
            C.faq_section(faq_items, heading="Pricing questions",
                          intro="What people ask before they order.") +
            C.contact_section())
    emit("pricing", page(
        title="ONE IPTV Pricing | Bronze, Gold, Platinum & Exclusive Plans",
        description="ONE IPTV plans and pricing. Compare Bronze, Gold, Platinum and Exclusive — "
                    "12 to 24 month plans with a per-connection discount — and see what each includes.",
        path="/pricing/",
        keywords="one iptv pricing, one iptv plans, iptv subscription, iptv one month",
        body=body, extra_head=ld(bc_schema(trail)) + ld(C.faq_schema(faq_items))))


# =========================================================== DEVICES =======
def build_devices():
    trail = [("Home", "/"), ("Devices", None)]
    hero = f"""<section class="page-hero">
  <div class="wrap">
    {breadcrumb(trail)}
    <span class="eyebrow">Devices</span>
    <h1>Watch ONE IPTV on Your Favorite Devices</h1>
    <p class="lead">If it runs a modern IPTV app, it almost certainly runs ONE IPTV. Here is what
       works, what to watch out for, and what to do when a television will not cooperate.</p>
  </div>
</section>
"""
    detail = f"""<section class="section section--tight">
  <div class="wrap" style="max-width:900px">
    <h2>Smart TVs</h2>
    <p>Modern Samsung and LG televisions can install an <strong>IPTV app for TV</strong> directly
       from their own app store, and once installed it behaves like any other TV app. This is the
       route most of our customers take. Sets from roughly the last five years are usually fine;
       older models sometimes have an app store that no longer receives new titles, which is worth
       checking before you order.</p>

    <h2>Android TV and Google TV</h2>
    <p>These are the easiest platforms to work with, because the Play Store carries several
       well-maintained IPTV players. That applies to televisions with Android TV built in as well
       as to dongles and boxes running it. If you are buying hardware specifically for this, an
       Android TV device is the least troublesome choice.</p>

    <h2>Fire TV</h2>
    <p>Fire TV Sticks and Fire TV devices work well and are inexpensive, which makes them a common
       fix for an older television — plug one into a spare HDMI port and the TV's own limitations
       stop mattering. Install a compatible player from the Amazon Appstore on the device itself.</p>

    <h2>Phones and tablets</h2>
    <p>Android and iOS both have capable players. Phones are handy for watching away from home;
       tablets get used in kitchens and gardens more than people expect. Setup is the same three
       steps: install, enter details, watch.</p>

    <h2>TV boxes and set-top hardware</h2>
    <p>Android TV boxes and MAG-style set-top boxes are supported. These suit people who want a
       dedicated device for television rather than adding another app to a smart TV. If you are
       using set-top hardware, tell us the model when you order — the setup steps differ slightly
       and we will send the right instructions.</p>

    <div class="callout">
      <p><strong>Where to get the app.</strong> Always install player applications from the
        official store on the device itself. We do not host application files, and we would advise
        against downloading IPTV player installers from links sent over messaging apps — that is a
        well-worn route for malware, and the app will not update properly afterwards. Our
        <a href="/blog/smart-one-iptv-app-download-setup-guide/">app download guide</a> covers this
        in more depth.</p>
    </div>

    <h2>Not sure about your model?</h2>
    <p>Send us the make and model before you order — message us on
      <a href="{C.WA_URL}" data-whatsapp-link target="_blank" rel="noopener">WhatsApp</a>
      or use the <a href="/contact/">contact form</a> — and we will tell you honestly whether it
      will work, and what the alternative is if it will not.</p>
  </div>
</section>
"""
    faq_items = [C.FAQ_MAIN[3], C.FAQ_MAIN[5], C.FAQ_MAIN[6], C.FAQ_EXTRA[0]]
    body = (hero + C.devices_section(heading="Compatible device types") +
            C.brand_strip_section("Compatible with all major platforms") + detail +
            C.faq_section(faq_items, heading="Device questions",
                          intro="Compatibility, apps and connections.") +
            C.pricing_section(with_switch=False) + C.contact_section())
    emit("devices", page(
        title="ONE IPTV Devices | Smart TV, Android TV, Fire TV & Mobile",
        description="See which devices work with ONE IPTV — Smart TV, Android TV, Fire TV, "
                    "smartphone, tablet and TV box — plus setup notes for each.",
        path="/devices/",
        keywords="iptv app for tv, iptv tv smart, one iptv devices, smart one iptv",
        body=body, extra_head=ld(bc_schema(trail)) + ld(C.faq_schema(faq_items))))


# =============================================================== FAQ =======
def build_faq():
    trail = [("Home", "/"), ("FAQ", None)]
    all_items = C.FAQ_MAIN + C.FAQ_EXTRA
    hero = f"""<section class="page-hero">
  <div class="wrap">
    {breadcrumb(trail)}
    <span class="eyebrow">FAQ</span>
    <h1>ONE IPTV — Frequently Asked Questions</h1>
    <p class="lead">Everything we get asked about ONE IPTV, answered without the marketing gloss.
       If your question is not here, message us on
       <a href="{C.WA_URL}" data-whatsapp-link target="_blank" rel="noopener"
          style="color:var(--red-bright)">WhatsApp</a>.</p>
  </div>
</section>
"""
    body = (hero +
            C.faq_section(C.FAQ_MAIN, heading="About the service",
                          intro="The essentials — what ONE IPTV is, how it works, and how to set "
                                "it up.") +
            C.faq_section(C.FAQ_EXTRA, heading="Practical questions",
                          intro="Connections, devices, plans and what to do when something is "
                                "not working.", start=100) +
            C.contact_section())
    emit("faq", page(
        title="ONE IPTV FAQ | Setup, Plans, Devices & Support",
        description="Answers to common ONE IPTV questions — what it is, how it works, Smart TV "
                    "setup, IPTV one month plans, device compatibility, UK use and support.",
        path="/faq/",
        keywords="one iptv faq, smart one iptv, iptv one month, one iptv uk, iptv app",
        body=body, extra_head=ld(bc_schema(trail)) + ld(C.faq_schema(all_items))))


# =========================================================== CONTACT =======
def build_contact():
    trail = [("Home", "/"), ("Contact", None)]
    hero = f"""<section class="page-hero">
  <div class="wrap">
    {breadcrumb(trail)}
    <span class="eyebrow">Contact</span>
    <h1>Need Help?</h1>
    <p class="lead">Our support team is available on WhatsApp to help with setup, plans and general
       questions. A quick message is usually fastest.</p>
    <p style="margin-top:1.6rem">
      <a class="phone-cta" href="{C.WA_URL}" data-whatsapp-link target="_blank" rel="noopener">
        <span class="phone-cta__icon">{icon("whatsapp")}</span>
        <span><small>Message us on</small><strong>WhatsApp</strong></span>
      </a>
    </p>
  </div>
</section>
"""
    form = f"""<section class="section section--tight">
  <div class="wrap">
    <div class="grid grid-2" style="gap:clamp(1.8rem,4vw,3rem);align-items:start">
      <div class="reveal">
        <h2>Send us a message</h2>
        <p>Tell us what you are trying to do and which device you are using — the make and model
           if you have it. That one detail lets us skip several rounds of back-and-forth.</p>
        <form class="form-grid" id="contact-form" method="post" action="#"
              onsubmit="event.preventDefault();var m=document.getElementById('contact-sent');
                        if(m){{m.hidden=false;m.scrollIntoView({{behavior:'smooth',block:'center'}});}}
                        this.reset();">
          <div class="field">
            <label for="c-name">Full name</label>
            <input id="c-name" name="name" type="text" autocomplete="name" required
                   placeholder="Your full name">
          </div>
          <div class="field">
            <label for="c-phone">WhatsApp number</label>
            <input id="c-phone" name="phone" type="tel" autocomplete="tel" required
                   placeholder="+44 7700 900000">
          </div>
          <div class="field">
            <label for="c-topic">What is this about?</label>
            <select id="c-topic" name="topic">
              <option>Choosing a plan</option>
              <option>Setup help</option>
              <option>Device compatibility</option>
              <option>Playback problem</option>
              <option>Billing or renewal</option>
              <option>Something else</option>
            </select>
          </div>
          <div class="field">
            <label for="c-message">Message</label>
            <textarea id="c-message" name="message" required
                      placeholder="Tell us what you need — and which device you are using."></textarea>
          </div>
          <button class="btn btn--primary btn--lg" type="submit">
            Send message {icon("arrow-right")}</button>
          <p class="modal__note" id="contact-sent" hidden style="color:var(--red-bright)">
            Thanks — your message is ready to send. This demo form does not transmit data yet;
            connect it to your form service to go live. In the meantime, message us on WhatsApp.</p>
          <p style="font-size:.78rem;color:var(--text-dim);margin:0">
            We use your details only to answer your enquiry. Never send payment card details
            through this form.</p>
        </form>
      </div>

      <div class="grid reveal" style="gap:1rem">
        <div class="card">
          <div class="card__icon">{icon("whatsapp")}</div>
          <h3>WhatsApp us</h3>
          <p style="margin-bottom:1rem">Fastest route for setup problems and plan questions — and
             easy for sending screenshots or model numbers.</p>
          <a class="btn btn--primary btn--block" href="{C.WA_URL}" data-whatsapp-link
             target="_blank" rel="noopener">{icon("whatsapp")}Chat on WhatsApp</a>
        </div>
        <div class="card">
          <div class="card__icon">{icon("clock")}</div>
          <h3>Before you get in touch</h3>
          <p style="margin-bottom:0">Have your device make and model ready, and note whether the
             problem affects one channel or everything. It halves the time it takes to fix.</p>
        </div>
      </div>
    </div>
  </div>
</section>
"""
    body = hero + form + C.faq_section(
        [C.FAQ_MAIN[9], C.FAQ_EXTRA[2], C.FAQ_EXTRA[4]],
        heading="Support questions",
        intro="Before you message, these cover the most common situations.") + C.contact_section(
        heading="Still stuck? Message us.")

    contact_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "ContactPage",
        "name": "Contact ONE IPTV",
        "url": SITE + "/contact/",
        "mainEntity": {
            "@type": "Organization",
            "@id": SITE + "/#organization",
            "name": BRAND,
            "url": C.WA_URL
        }
    }, ensure_ascii=False)

    emit("contact", page(
        title="Contact ONE IPTV | Message Us on WhatsApp",
        description="Contact ONE IPTV support on WhatsApp for help with setup, plans and general "
                    "questions, or send us a message through the contact form.",
        path="/contact/",
        keywords="one iptv contact, one iptv support, iptv help",
        body=body, extra_head=ld(bc_schema(trail)) + ld(contact_schema)))


# ============================================================== BLOG =======
def build_blog_index():
    trail = [("Home", "/"), ("Blog", None)]
    hero = f"""<section class="page-hero">
  <div class="wrap">
    {breadcrumb(trail)}
    <span class="eyebrow">Blog</span>
    <h1>ONE IPTV Guides &amp; Setup Help</h1>
    <p class="lead">Practical, jargon-free walkthroughs for getting IPTV working — whichever
       device you own and wherever you are watching from.</p>
  </div>
</section>
"""
    listing = f"""<section class="section section--tight">
  <div class="wrap">
    <div class="grid grid-3">{C.blog_cards(C.POSTS)}
    </div>
  </div>
</section>
"""
    blog_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "Blog",
        "name": "ONE IPTV Blog",
        "url": SITE + "/blog/",
        "publisher": {"@id": SITE + "/#organization"},
        "blogPost": [
            {"@type": "BlogPosting",
             "headline": p["title"],
             "url": SITE + "/blog/" + p["slug"] + "/",
             "datePublished": p["date"],
             "description": p["desc"]}
            for p in C.POSTS
        ]
    }, ensure_ascii=False)

    emit("blog", page(
        title="ONE IPTV Blog | IPTV Setup Guides & Tips",
        description="ONE IPTV guides: beginner walkthroughs, Smart TV setup, IPTV one month "
                    "plans, UK getting started, app download help and troubleshooting.",
        path="/blog/",
        keywords="one iptv blog, iptv setup guide, smart one iptv, iptv one month, one iptv uk",
        body=hero + listing + C.contact_section(),
        extra_head=ld(bc_schema(trail)) + ld(blog_schema)))


def build_articles():
    for slug, builder in ARTICLES.items():
        post = C.post_by_slug(slug)
        emit("blog/" + slug, article_page(post, builder))


# ============================================================= LEGAL =======
LEGAL_PAGES = {
    "privacy": (
        "Privacy Policy | ONE IPTV",
        "How ONE IPTV collects, uses and protects the personal information you provide "
        "through this website.",
        "Privacy Policy",
        """
    <p><em>Last updated: 1 August 2026</em></p>
    <p>This policy explains what personal information ONE IPTV collects through
       one-iptv.website, why we collect it, and what we do with it. It is written to be read,
       not to be skimmed past.</p>

    <h2>What we collect</h2>
    <p>We collect only what you type into our forms: your name, WhatsApp number, the plan you
       selected, and any notes you add about your device. If you contact us on WhatsApp, we keep
       the correspondence needed to help you.</p>
    <p><strong>We do not collect payment card details on this website.</strong> No card fields
       exist on any page. Payment is completed either through a PCI-compliant third-party
       payment provider — who handle card data under their own terms — or arranged directly
       with our support team.</p>

    <h2>Why we use it</h2>
    <ul>
      <li>To confirm your order and send your access details and setup instructions.</li>
      <li>To answer support enquiries and troubleshoot problems with you.</li>
      <li>To keep the records we are required to keep for the service we provide.</li>
    </ul>
    <p>We do not sell your information, and we do not pass it to advertisers.</p>

    <h2>Cookies and analytics</h2>
    <p>This website is built as static pages and does not set advertising or tracking cookies
       by default. If analytics or a chat widget is added later, this section will be updated
       to name the provider and describe what it stores before it goes live.</p>

    <h2>How long we keep it</h2>
    <p>We keep order and support records for as long as your account is active and for a
       reasonable period afterwards to handle billing questions and legal obligations. Ask us
       to delete your data and we will do so wherever we are not required to retain it.</p>

    <h2>Your rights</h2>
    <p>Depending on where you live — including under the UK GDPR and EU GDPR — you may have the
       right to access, correct, export or delete the personal data we hold about you, and to
       object to certain processing. To exercise any of these, contact us using the details
       below and we will respond within the timeframe the applicable law requires.</p>

    <h2>Security</h2>
    <p>We take reasonable technical and organisational measures to protect the information you
       give us. No system is perfect, and we will tell you promptly if a breach affects your
       data.</p>

    <h2>Contact</h2>
    <p>Questions about this policy, or about the data we hold: message us on
       <a href="WA_URL_TXT" target="_blank" rel="noopener">WhatsApp</a>.</p>
"""),

    "terms": (
        "Terms of Service | ONE IPTV",
        "The terms that apply when you use the ONE IPTV website and subscribe to the "
        "ONE IPTV service.",
        "Terms of Service",
        """
    <p><em>Last updated: 1 August 2026</em></p>
    <p>These terms apply to your use of one-iptv.website and to any ONE IPTV plan you purchase.
       By ordering, you agree to them.</p>

    <h2>1. What the service is</h2>
    <p>ONE IPTV provides access to an IPTV streaming service and related technical support.
       Access is delivered as credentials that you enter into a compatible third-party IPTV
       player application on your own device. We do not supply the player application, and we
       do not supply the device.</p>

    <h2>2. What we do not promise</h2>
    <p>We describe the service honestly, which means being clear about limits. We do not
       guarantee that any specific channel, event, network or title will be available, that
       availability will remain unchanged, that the service will be uninterrupted or error-free,
       or that any particular picture quality will be achievable on your connection. Content
       availability depends on your plan, your region, your device, your internet connection,
       and what the service carries at the time.</p>

    <h2>3. Your responsibilities</h2>
    <ul>
      <li>You are responsible for using the service in accordance with all laws and regulations
          that apply where you are located, including copyright and broadcasting law.</li>
      <li>You are responsible for ensuring you hold any rights, licences or permissions required
          for the content you choose to access.</li>
      <li>You must not share, resell or redistribute your credentials. Accounts are for the
          number of simultaneous connections your plan allows.</li>
      <li>You are responsible for your own internet connection and equipment.</li>
    </ul>
    <p>If you are unsure whether your intended use is lawful where you live, seek advice before
       ordering. We would rather you asked than assumed.</p>

    <h2>4. Orders and payment</h2>
    <p>Orders placed through this website are requests, which we confirm before access begins.
       This website does not process card payments; payment is completed through a secure
       third-party payment provider or directly with our support team. Prices displayed as
       placeholders are not offers and are not binding until confirmed by us in writing.</p>

    <h2>5. Suspension and termination</h2>
    <p>We may suspend or terminate access where credentials are shared or resold, where the
       service is used unlawfully, or where payment is not completed. We will tell you why.</p>

    <h2>6. No third-party affiliation</h2>
    <p>ONE IPTV is an independent brand. Names of devices, platforms, operating systems and
       third-party IPTV player applications referenced on this site belong to their respective
       owners and are used only to describe compatibility. Their use does not imply any
       partnership, sponsorship, endorsement or affiliation, including with any application
       whose name resembles ours.</p>

    <h2>7. Liability</h2>
    <p>To the fullest extent permitted by law, our liability is limited to the amount you paid
       for the plan in question. Nothing in these terms limits liability that cannot lawfully be
       limited, including for death or personal injury caused by negligence, or for fraud.</p>

    <h2>8. Changes</h2>
    <p>We may update these terms. Material changes will be reflected in the date at the top of
       this page, and continued use after a change means you accept the updated terms.</p>

    <h2>9. Contact</h2>
    <p>Questions about these terms: message us on
       <a href="WA_URL_TXT" target="_blank" rel="noopener">WhatsApp</a>.</p>
"""),

    "refund-policy": (
        "Refund Policy | ONE IPTV",
        "How refunds and cancellations work for ONE IPTV subscription plans — when we "
        "refund, when we usually cannot, and how to cancel or change your plan.",
        "Refund Policy",
        """
    <p><em>Last updated: 1 August 2026</em></p>
    <p>We would rather sort a problem out than argue about a refund. This page explains how we
       approach both.</p>

    <h2>Before you buy</h2>
    <p>The best protection against a refund request is not needing one. Start with the
       <a href="/pricing/">one month plan</a> if you have not used the service before, and tell
       us your device and location beforehand so we can flag any compatibility issue while it
       still costs you nothing.</p>

    <h2>If something is not working</h2>
    <p>Contact us first. Most reported problems turn out to be a setting on the device, a
       router issue or an app that needs reinstalling, and we can usually resolve them in a few
       minutes over WhatsApp. Message us on
       <a href="WA_URL_TXT" target="_blank" rel="noopener">WhatsApp</a>.</p>

    <h2>When we refund</h2>
    <p>Where we cannot deliver working access to the service you paid for, and we cannot resolve
       it within a reasonable period, we will refund you. We handle these case by case rather
       than hiding behind a rigid clause — but we will always tell you the outcome clearly and
       promptly.</p>

    <h2>When we usually cannot refund</h2>
    <ul>
      <li>Where the service works as described but a specific channel, event or title you hoped
          for is not available — which is why we encourage you to ask us about specific content
          before ordering.</li>
      <li>Where the problem is caused by your own internet connection or hardware and persists
          after we have helped you diagnose it.</li>
      <li>Where credentials have been shared, resold or used in breach of our
          <a href="/terms/">terms</a>.</li>
      <li>Where a substantial part of the plan period has already been used.</li>
    </ul>

    <h2>Cancelling</h2>
    <p>Plans do not renew silently without your knowledge. To stop, or to change plan length,
       contact us before your current period ends and we will handle it.</p>

    <h2>Statutory rights</h2>
    <p>Nothing in this policy affects the rights you have under the consumer law that applies
       where you live.</p>

    <h2>Contact</h2>
    <p>Message us on <a href="WA_URL_TXT" target="_blank" rel="noopener">WhatsApp</a>.</p>
"""),
}


def build_legal():
    for slug, (title, desc, h1, bodytext) in LEGAL_PAGES.items():
        trail = [("Home", "/"), (h1, None)]
        text = bodytext.replace("WA_URL_TXT", C.WA_URL)
        body = f"""<section class="page-hero">
  <div class="wrap">
    {breadcrumb(trail)}
    <h1>{h1}</h1>
  </div>
</section>
<section class="section section--tight">
  <div class="wrap"><div class="prose">{text}</div></div>
</section>
"""
        emit(slug, page(title=title, description=desc, path=f"/{slug}/", body=body,
                        extra_head=ld(bc_schema(trail))))


# ============================================================== 404 ========
def build_404():
    html = page(
        title="Page not found | ONE IPTV",
        description="The page you are looking for could not be found on one-iptv.website. "
                    "Head back to the ONE IPTV home page, browse plans, or call our support team.",
        path="/404.html",
        extra_head='  <meta name="robots" content="noindex, follow">\n',
        body=f"""<section class="page-hero" style="padding-block:clamp(4rem,10vw,8rem)">
  <div class="wrap">
    <span class="eyebrow">404</span>
    <h1>That page has gone off air</h1>
    <p class="lead">The link may be out of date, or the address may have a typo in it. Here are
       the places most people are heading.</p>
    <p style="margin-top:1.8rem;display:flex;gap:.7rem;flex-wrap:wrap;justify-content:center">
      <a class="btn btn--primary" href="/">Back to home</a>
      <a class="btn btn--ghost" href="/pricing/">View plans</a>
      <a class="btn btn--ghost" href="/blog/">Setup guides</a>
      <a class="btn btn--outline" href="{C.WA_URL}" data-whatsapp-link target="_blank" rel="noopener">
        {icon("whatsapp")}WhatsApp us</a>
    </p>
  </div>
</section>
""")
    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("  ✓ /404.html")


# ====================================================== SITEMAP / ROBOTS ===
def build_sitemap():
    from datetime import date
    today = date.today().isoformat()
    urls = [
        ("/", "1.0", "weekly", today),
        ("/pricing/", "0.9", "weekly", today),
        ("/features/", "0.8", "monthly", today),
        ("/devices/", "0.8", "monthly", today),
        ("/channels/", "0.8", "monthly", today),
        ("/faq/", "0.8", "monthly", today),
        ("/blog/", "0.7", "weekly", today),
        ("/contact/", "0.7", "monthly", today),
    ]
    urls += [(f"/blog/{p['slug']}/", "0.6", "monthly", p["date"]) for p in C.POSTS]
    urls += [("/privacy/", "0.3", "yearly", today),
             ("/terms/", "0.3", "yearly", today),
             ("/refund-policy/", "0.3", "yearly", today)]

    entries = "\n".join(f"""  <url>
    <loc>{SITE}{u}</loc>
    <lastmod>{lm}</lastmod>
    <changefreq>{cf}</changefreq>
    <priority>{pr}</priority>
  </url>""" for u, pr, cf, lm in urls)

    emit_raw("sitemap.xml", f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{entries}
</urlset>
""")

    emit_raw("robots.txt", f"""# robots.txt for {SITE}
User-agent: *
Allow: /

# Nothing here needs crawling
Disallow: /404.html

Sitemap: {SITE}/sitemap.xml
""")

    emit_raw("site.webmanifest", json.dumps({
        "name": "ONE IPTV",
        "short_name": "ONE IPTV",
        "description": "Premium IPTV service for Smart TVs and streaming devices.",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#07070a",
        "theme_color": "#07070a",
        "icons": [
            {"src": "/assets/img/favicon.svg", "sizes": "any", "type": "image/svg+xml"},
            {"src": "/assets/img/icon-180.png", "sizes": "180x180", "type": "image/png"},
            {"src": "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png",
             "purpose": "any maskable"}
        ]
    }, indent=2))

    emit_raw("_headers", """/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: SAMEORIGIN
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), microphone=(), camera=()

/assets/*
  Cache-Control: public, max-age=31536000, immutable
""")

    emit_raw(".htaccess", """# ONE IPTV — Apache configuration
Options -Indexes
DirectoryIndex index.html
ErrorDocument 404 /404.html

# Clean URLs: /pricing -> /pricing/index.html
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteBase /
  # Add trailing slash to directory requests
  RewriteCond %{REQUEST_FILENAME} -d
  RewriteCond %{REQUEST_URI} !/$
  RewriteRule ^(.*)$ /$1/ [R=301,L]
</IfModule>

<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css application/javascript image/svg+xml \\
    application/json application/xml
</IfModule>

<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/css "access plus 1 year"
  ExpiresByType application/javascript "access plus 1 year"
  ExpiresByType image/svg+xml "access plus 1 year"
  ExpiresByType text/html "access plus 1 hour"
</IfModule>

<IfModule mod_headers.c>
  Header set X-Content-Type-Options "nosniff"
  Header set Referrer-Policy "strict-origin-when-cross-origin"
</IfModule>
""")


# ============================================================== MAIN =======
def main():
    print("Building ONE IPTV …")
    build_home()
    build_features()
    build_channels()
    build_pricing()
    build_devices()
    build_faq()
    build_contact()
    build_blog_index()
    build_articles()
    build_legal()
    build_404()
    build_sitemap()
    print("Done.")


if __name__ == "__main__":
    main()
