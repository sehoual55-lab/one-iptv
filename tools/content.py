#!/usr/bin/env python3
"""Shared content data + reusable section builders for ONE IPTV."""

from shell import icon, brand_svg, PHONE_DISPLAY, PHONE_TEL, EMAIL, SITE, BRAND

# Contact is WhatsApp-only.
WA_NUM = "16615413954"
WA_URL = f"https://wa.me/{WA_NUM}"
WA = f'<a href="{WA_URL}" target="_blank" rel="noopener">WhatsApp</a>'

# =========================================================== FEATURES ======
FEATURES = [
    ("tv", "Live TV Experience",
     "Follow live programming as it airs, with a channel layout that stays quick to browse "
     "on a TV remote as well as a touchscreen."),
    ("zap", "HD &amp; High-Quality Streaming",
     "Streams are delivered in HD and higher quality where the source and your connection "
     "allow, with adaptive playback on slower networks."),
    ("monitor", "Smart TV Compatibility",
     "ONE IPTV works through compatible IPTV player apps on modern Smart TV platforms, so "
     "most people can watch without extra hardware."),
    ("sliders", "Easy Setup",
     "Install a compatible player, enter the details we send you, and you are watching. "
     "Most setups take a few minutes."),
    ("layers", "Multi-Device Support",
     "Move between your television, phone, tablet or TV box using the same account, "
     "according to the connection limits of your plan."),
    ("calendar", "Flexible Plans",
     "Choose Bronze, Gold, Platinum or Exclusive — 12 to 24 months — and set how many devices "
     "stream at once, with each extra connection discounted."),
]

# ============================================================ DEVICES ======
# icon = fallback line icon; brands = list of (logo-file, is-wide) chips
DEVICES = [
    ("monitor", "Smart TV",
     "Samsung, LG and other modern Smart TV platforms with a compatible IPTV player installed.",
     [("samsung", True), ("lg", True), ("sony", True)]),
    ("tv", "Android &amp; Google TV",
     "Android TV and Google TV sets, dongles and Chromecast, using a player from the Play Store.",
     [("android", False), ("chromecast", False)]),
    ("flame", "Fire TV",
     "Fire TV Stick and Fire TV devices, using a compatible player from the Amazon Appstore.",
     [("amazon", False)]),
    ("cast", "Apple TV &amp; iOS",
     "Apple TV, iPhone and iPad, using a compatible IPTV player installed from the App Store.",
     [("appletv", False), ("apple", False)]),
    ("smartphone", "Phone &amp; Tablet",
     "Android and iOS phones and tablets, so you can keep watching away from the television.",
     [("android", False), ("apple", False)]),
    ("box", "Computer &amp; TV Box",
     "Windows, Linux, Xbox, Roku, Android TV boxes and MAG-style set-top hardware.",
     [("windows", False), ("linux", False), ("xbox", False), ("roku", True)]),
]

# Logos shown in the trust strip
BRAND_STRIP = ["samsung", "lg", "sony", "android", "apple", "amazon", "roku", "windows", "linux"]

# ========================================================= CATEGORIES ======
CATEGORIES = [
    ("live-tv", "Live TV", "Live", "Follow programming as it airs"),
    ("sports", "Sports", "Live", "Fixtures, highlights and analysis"),
    ("movies", "Movies", "On demand", "Feature-length titles to browse"),
    ("series", "Series", "On demand", "Episodic shows, season by season"),
    ("entertainment", "Entertainment", "Mixed", "Lifestyle, music and variety"),
    ("news", "News", "Live", "Rolling coverage and bulletins"),
    ("documentaries", "Documentaries", "On demand", "Factual and long-form features"),
    ("kids", "Kids", "Family", "Family-friendly viewing options"),
]

# =============================================================== FAQ =======
FAQ_MAIN = [
    ("What is ONE IPTV?",
     "<p>ONE IPTV is an IPTV service that delivers television over your internet connection "
     "rather than through a satellite dish or an aerial. You subscribe to a plan, we send you "
     "the connection details, and you enter them into a compatible IPTV player app on the "
     "device you want to watch on. Because everything travels over the internet, the same "
     "account can follow you from the television in the living room to a phone on the train.</p>"),

    ("How does ONE IPTV work?",
     "<p>There are three parts to it: the service that delivers the streams, a player "
     "application on your device that knows how to display them, and the credentials that "
     "link the two. After you order, our team sends you your login details along with a short "
     "setup guide written for your specific device. You install a compatible player, enter the "
     "details once, and the app builds your channel list. From then on you simply open the app.</p>"),

    ("How can I set up ONE IPTV?",
     "<p>Setup follows the same four steps on nearly every device. Choose a plan and complete "
     "your order; wait for your credentials to arrive by email; install a compatible IPTV "
     "player from your device's app store; and enter the details we sent you. Our "
     "<a href=\"/blog/one-iptv-complete-guide-for-beginners/\">beginner's guide</a> walks "
     "through the whole process, and if you would rather be talked through it, message us on "
     f"{WA} and we will guide you every step of the way.</p>"),

    ("Can I use ONE IPTV on a Smart TV?",
     "<p>Yes — a Smart TV is one of the most common ways people watch. Modern Samsung, LG, "
     "Android TV and Google TV sets can all install an IPTV player from their own app store, "
     "and once that player has your details it behaves much like any other TV app. If your "
     "television is older or its app store is limited, an inexpensive Android TV box or "
     "streaming stick plugged into an HDMI port achieves the same result. Our "
     "<a href=\"/blog/how-to-set-up-one-iptv-on-a-smart-tv/\">Smart TV setup guide</a> covers "
     "both routes.</p>"),

    ("Is there an IPTV one month plan?",
     "<p>Our standard plans run from 12 months (Bronze) up to 24 months (Exclusive), because a "
     "longer term is far better value per month. That said, if you would prefer a shorter term "
     "to try the service on your own connection and hardware first, message us on "
     f"{WA} and we will sort one out for you. Our article on "
     "<a href=\"/blog/iptv-one-month-plans-what-to-consider/\">trying IPTV short-term</a> "
     "explains what to test during those first weeks before you commit to a longer plan.</p>"),

    ("What devices are compatible with ONE IPTV?",
     "<p>Broadly, anything that can run a modern IPTV player application: Smart TVs, Android "
     "TV and Google TV, Fire TV devices, Android and iOS phones and tablets, Android TV boxes, "
     "MAG-style set-top boxes, and computers through a desktop player. Our "
     "<a href=\"/devices/\">devices page</a> lists the main categories. If you are unsure "
     "whether your specific model will work, send us the make and model before you order and "
     "we will tell you honestly.</p>"),

    ("How do I download a compatible IPTV app?",
     "<p>Use the official app store on the device itself — the Samsung or LG store on a Smart "
     "TV, the Play Store on Android TV, the Amazon Appstore on Fire TV, or the App Store on "
     "iOS. Search for an IPTV player, install it, and open it once so it registers on the "
     "device. We then send you the details to enter. We deliberately do not host application "
     "files ourselves; installing player apps from their official stores is safer and keeps "
     "them updating properly. Our "
     "<a href=\"/blog/smart-one-iptv-app-download-setup-guide/\">app download guide</a> "
     "explains what to look for.</p>"),

    ("How do I set up Smart ONE IPTV?",
     "<p>People often use \"smart one iptv\" as shorthand for running ONE IPTV on a smart "
     "device, and the process is the one described above: install a compatible player on your "
     "Smart TV, enter the credentials we send you, and let the app load your list. Note that "
     "several third-party IPTV player applications on the market use similar names. ONE IPTV "
     "is an independent service and is not affiliated with, endorsed by or connected to any "
     "of those applications — we simply tell you which players are known to work well with "
     "our service. See our "
     "<a href=\"/blog/smart-one-iptv-what-you-need-to-know/\">Smart ONE IPTV explainer</a> "
     "for the full picture.</p>"),

    ("Can I use ONE IPTV in the UK?",
     "<p>ONE IPTV can be used in the UK on a normal home broadband connection — the service "
     "is not tied to a particular country, and UK customers make up a meaningful share of the "
     "people we help set up. What we would say plainly is that you remain responsible for "
     "using the service in line with UK law and for holding any rights or permissions the "
     "content you watch requires. Our "
     "<a href=\"/blog/one-iptv-uk-getting-started-guide/\">ONE IPTV UK guide</a> covers "
     "connection requirements and the practical points worth knowing.</p>"),

    ("How do I contact ONE IPTV support?",
     "<p>The fastest route is WhatsApp: message us on "
     f"{WA} and you will reach a person who can help with setup, plans or troubleshooting. "
     "You can also use the form on our <a href=\"/contact/\">contact page</a>. Have your "
     "device make and model handy — it makes the conversation much quicker.</p>"),
]

FAQ_EXTRA = [
    ("What internet speed do I need for ONE IPTV?",
     "<p>As a practical rule, around 15–25 Mbps gives a comfortable HD experience on one "
     "device, and more headroom helps if several people in the house stream at once or if you "
     "want higher-resolution playback. Consistency matters more than the headline number: a "
     "steady 20 Mbps behaves far better than a connection that spikes to 100 and then drops. "
     "Where possible, connect the television by Ethernet rather than Wi-Fi.</p>"),
    ("Can I watch on more than one device at the same time?",
     "<p>Your plan determines how many simultaneous connections your account allows. You can "
     "install the player on as many devices as you like — the limit applies to how many are "
     "actively streaming at the same moment. If everyone in the household wants to watch "
     "something different at once, tell us before you order and we will make sure your plan "
     "matches.</p>"),
    ("What happens if a stream buffers or stops working?",
     "<p>Start with the usual suspects: restart the player app, then the device, then the "
     "router. If one particular channel is affected and everything else is fine, the issue is "
     "usually upstream of us and often resolves on its own. If everything buffers, it points "
     "to the connection between your device and your router. Either way, message us — we would "
     "rather spend five minutes diagnosing it than have you guess.</p>"),
    ("Do you offer a free trial?",
     "<p>Ask us. Trial availability changes and we would rather tell you what is actually on "
     f"offer today than publish a promise we might not be able to keep. Message us on "
     f"{WA} and we will tell you where things "
     "stand. If you would like a shorter starter term before committing to a longer plan, just "
     "ask and we will arrange it.</p>"),
    ("How do I cancel or change my plan?",
     "<p>Contact us before your current period ends and we will handle it. Plans do not roll "
     "over silently without you knowing — if you want to stop, stop; if you want to move from "
     "monthly to annual, we will apply what you have already paid where we reasonably can.</p>"),
    ("What do search terms like &quot;ip smart iptv&quot; or &quot;iptv tv smart&quot; mean?",
     "<p>They are all variations on the same question, and you will see plenty of them: "
     "<em>ip smart iptv</em>, <em>iptv tv smart</em>, <em>smart iptv tv</em>, <em>iptv smart "
     "tv app</em>. Word order shifts because people type the words that matter to them in the "
     "order they think of them, and IPTV terminology has never settled into one standard "
     "phrase.</p><p>Underneath, they nearly always mean one of two things: <strong>how do I get "
     "IPTV working on my smart television</strong>, or <strong>which IPTV app should I install "
     "on it</strong>. Both are answered the same way — install a compatible player from your "
     "television's own app store and enter the credentials your provider sends you. Our "
     "<a href=\"/blog/how-to-set-up-one-iptv-on-a-smart-tv/\">Smart TV guide</a> covers the "
     "first, and our <a href=\"/blog/smart-one-iptv-app-download-setup-guide/\">app download "
     "guide</a> the second. You do not need to find a product that matches the exact phrase you "
     "searched for.</p>"),

    ("Is ONE IPTV affiliated with any third-party IPTV app?",
     "<p>No. ONE IPTV is an independent brand. Application names that sound similar belong to "
     "their own developers, and platform names such as Android TV or Fire TV belong to their "
     "respective owners. We reference them only to describe which devices our service is "
     "compatible with — never to imply a partnership that does not exist.</p>"),
]


def faq_schema(items):
    import json
    import re
    def strip(html):
        return re.sub(r"<[^>]+>", "", html).replace("&amp;", "&").strip()
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": strip(a)}}
            for q, a in items
        ]
    }, ensure_ascii=False)


# ============================================================ POSTS ========
POSTS = [
    {
        "slug": "one-iptv-complete-guide-for-beginners",
        "title": "ONE IPTV: Complete Guide for Beginners",
        "seo_title": "ONE IPTV: Complete Guide for Beginners | ONE IPTV",
        "desc": "A plain-English introduction to ONE IPTV — what IPTV is, what you need, how "
                "setup works on each device, and what to check before you order.",
        "excerpt": "New to IPTV? Start here. What it is, what you need, how setup actually "
                   "works, and the questions worth asking before you order.",
        "img": "blog-beginners-guide",
        "tag": "Getting started",
        "date": "2026-02-04",
        "read": "9 min read",
        "kw": "one iptv, iptv app, iptv app for tv, iptv tv smart",
    },
    {
        "slug": "how-to-set-up-one-iptv-on-a-smart-tv",
        "title": "How to Set Up ONE IPTV on a Smart TV",
        "seo_title": "How to Set Up ONE IPTV on a Smart TV | ONE IPTV",
        "desc": "Step-by-step setup for ONE IPTV on Samsung, LG, Android TV and Google TV, "
                "plus what to do when your television's app store falls short.",
        "excerpt": "Samsung, LG, Android TV or Google TV — the exact steps, plus what to do "
                   "when your TV's app store lets you down.",
        "img": "blog-smart-tv-setup",
        "tag": "Setup",
        "date": "2026-02-18",
        "read": "8 min read",
        "kw": "iptv tv smart, iptv app for tv, one iptv, smart one iptv",
    },
    {
        "slug": "smart-one-iptv-what-you-need-to-know",
        "title": "Smart ONE IPTV: What You Need to Know",
        "seo_title": "Smart ONE IPTV: What You Need to Know | ONE IPTV",
        "desc": "What people mean by &quot;smart one iptv&quot;, how the service and the player app "
                "are different things, and how to avoid the common mix-ups.",
        "excerpt": "The phrase covers two different things — a service and a player app. "
                   "Here's how to tell them apart and why it matters.",
        "img": "blog-smart-one-iptv",
        "tag": "Explainer",
        "date": "2026-03-03",
        "read": "7 min read",
        "kw": "smart one iptv, ip smart iptv, one iptv, iptv app",
    },
    {
        "slug": "iptv-one-month-plans-what-to-consider",
        "title": "IPTV One Month Plans: What to Consider",
        "seo_title": "IPTV One Month Plans: What to Consider | ONE IPTV",
        "desc": "Why a one month IPTV plan is the sensible way to test a service, what to "
                "check during those 30 days, and when a longer plan makes sense.",
        "excerpt": "A month is long enough to learn everything you need to know. Here's what "
                   "to actually test while the clock runs.",
        "img": "blog-one-month-plans",
        "tag": "Plans",
        "date": "2026-03-19",
        "read": "8 min read",
        "kw": "iptv one month, one iptv, iptv app",
    },
    {
        "slug": "one-iptv-uk-getting-started-guide",
        "title": "ONE IPTV UK: Getting Started Guide",
        "seo_title": "ONE IPTV UK: Getting Started Guide | ONE IPTV",
        "desc": "Setting up ONE IPTV in the UK — broadband requirements, router and Wi-Fi "
                "advice, device choices and the responsibilities that come with IPTV.",
        "excerpt": "UK broadband, routers, device choices and the responsibilities that come "
                   "with running IPTV at home.",
        "img": "blog-uk-guide",
        "tag": "Regional",
        "date": "2026-04-08",
        "read": "9 min read",
        "kw": "one iptv uk, one iptv, iptv one month",
    },
    {
        "slug": "smart-one-iptv-app-download-setup-guide",
        "title": "Smart ONE IPTV App Download: Setup Guide",
        "seo_title": "Smart ONE IPTV App Download: Setup Guide | ONE IPTV",
        "desc": "How to safely download and set up a compatible IPTV app on Smart TV, "
                "Android TV, Fire TV and mobile — and why the official store matters.",
        "excerpt": "Where to get a player app safely, how to enter your details, and why "
                   "sideloading random APKs is a bad trade.",
        "img": "blog-app-download",
        "tag": "Setup",
        "date": "2026-04-27",
        "read": "8 min read",
        "kw": "smart one iptv app download, iptv app, smart one iptv",
    },
    {
        "slug": "how-to-set-up-iptv-on-your-tv",
        "title": "How to Set Up IPTV on Your TV",
        "seo_title": "How to Set Up IPTV on Your TV | ONE IPTV",
        "desc": "A device-agnostic walkthrough for getting IPTV running on any television, "
                "including older sets, plus a troubleshooting checklist that actually helps.",
        "excerpt": "Any television, any age. The universal setup path, plus a troubleshooting "
                   "checklist worth bookmarking.",
        "img": "blog-tv-setup",
        "tag": "Setup",
        "date": "2026-05-14",
        "read": "9 min read",
        "kw": "iptv app for tv, iptv tv smart, iptv app, one iptv",
    },
    {
        "slug": "iptv-on-xbox-one-does-it-work",
        "title": "IPTV on Xbox One: Does It Work, and How to Watch",
        "seo_title": "IPTV on Xbox One: Does It Work? | ONE IPTV",
        "desc": "Can you get IPTV on Xbox One, does it actually work, and how do you watch? "
                "The three routes that exist, what each is like to live with, and the one "
                "we recommend.",
        "excerpt": "Can you get it, does it work, how do you watch — answered honestly, "
                   "including when the console is the wrong tool for the job.",
        "img": "blog-xbox-one",
        "img_ext": "webp",
        "og_img": "/assets/img/blog-xbox-one-og.jpg",
        "img_alt": "A family watching a large wall-mounted TV showing the ONE IPTV logo, with a media cabinet and streaming devices below the screen",
        "tag": "Devices",
        "date": "2026-08-26",
        "read": "8 min read",
        "kw": "iptv on xbox one, can you get iptv on xbox one, does iptv work on xbox one, "
              "how to watch iptv on xbox one, one iptv, iptv app",
        "faqs": [
            ("Can you get IPTV on Xbox One?",
             "Yes — either through a media player app from the Microsoft Store, where one is "
             "available in your region, or through the console's browser. Neither is as smooth "
             "as a dedicated streaming device, but both can play your subscription."),
            ("Does IPTV work on Xbox One?",
             "It does, provided the app you install accepts a playlist URL or a server login and "
             "your connection is stable. The console is capable of the playback; the limitation "
             "is the choice of software, not the hardware."),
            ("How do I watch IPTV on Xbox One?",
             "Install a compatible player from the store, enter the server address, username and "
             "password we send you, and open a channel. If no suitable player is listed, use a "
             "streaming stick on a spare HDMI port instead — same subscription, better "
             "experience."),
            ("Does it work the same on Xbox Series X and Series S?",
             "Broadly yes. The newer consoles run a more current browser and the same store, so "
             "the same routes apply, and both handle high-bitrate streams comfortably. The app "
             "selection remains the constraint."),
            ("Will my subscription work on the console and my TV at the same time?",
             "That depends on how many simultaneous connections your plan includes. One "
             "connection means one stream at a time; if two people watch at once, you need two. "
             "The connection count is adjustable when you order."),
        ],
    },
    {
        "slug": "iptv-app-for-tv-how-to-choose",
        "title": "IPTV App for TV: How to Choose the Right Player",
        "seo_title": "IPTV App for TV: How to Choose a Player | ONE IPTV",
        "desc": "How to pick an IPTV app for your TV: the three families of player, what "
                "separates a good one from a bad one, and how to switch players safely.",
        "excerpt": "The app is what you touch every evening. Here's how to tell a good player "
                   "from a bad one before you waste a night on the wrong choice.",
        "img": "blog-iptv-app",
        "img_ext": "webp",
        "og_img": "/assets/img/blog-iptv-app-og.jpg",
        "img_alt": "A family on a sofa watching an IPTV app for TV open on a large screen in a London living room",
        "tag": "Apps",
        "date": "2026-09-01",
        "read": "9 min read",
        "kw": "iptv app for tv, iptv app, iptv tv smart, ip smart iptv, smart one iptv",
    },
]


def post_by_slug(slug):
    return next(p for p in POSTS if p["slug"] == slug)


def fmt_date(iso):
    from datetime import date
    y, m, d = (int(x) for x in iso.split("-"))
    return date(y, m, d).strftime("%d %B %Y").lstrip("0")


# ==================================================== SECTION BUILDERS =====
def features_section(heading="Why Choose ONE IPTV?", level="h2"):
    cards = "".join(f"""
        <article class="card reveal">
          <div class="card__icon">{icon(ic)}</div>
          <h3>{title}</h3>
          <p>{body}</p>
        </article>""" for ic, title, body in FEATURES)
    return f"""<section class="section" id="features">
  <div class="glow glow--dim" style="width:520px;height:520px;top:-120px;right:-160px"></div>
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Features</span>
      <{level}>{heading}</{level}>
      <p>Everything is built around one idea: television should be easy to start watching,
         on whatever screen happens to be nearest.</p>
    </div>
    <div class="grid grid-3">{cards}
    </div>
  </div>
</section>
"""


def carousel_section(heading="Explore Your Entertainment"):
    tiles = "".join(f"""
        <a class="tile" href="/channels/" aria-label="{name} category">
          <img src="/assets/img/cat-{slug}.svg" alt="{name} category artwork" loading="lazy"
               decoding="async" width="300" height="400">
          <span class="tile__overlay">
            <span class="tile__tag">{tag}</span>
            <h3>{name}</h3>
            <p>{desc}</p>
          </span>
        </a>""" for slug, name, tag, desc in CATEGORIES)
    return f"""<section class="section" id="channels" data-carousel>
  <div class="glow glow--red" style="width:600px;height:600px;bottom:-200px;left:-220px;opacity:.35"></div>
  <div class="wrap">
    <div class="section-head reveal" style="text-align:left;max-width:none;display:flex;
         flex-wrap:wrap;gap:1rem;align-items:flex-end;justify-content:space-between">
      <div style="max-width:640px">
        <span class="eyebrow">Categories</span>
        <h2 style="margin-bottom:.5rem">{heading}</h2>
        <p style="margin:0">Browse by category and jump straight into what you feel like watching.
           Exact availability depends on your plan and on what the service carries at the time.</p>
      </div>
      <div class="carousel-nav" data-carousel-nav>
        <button class="carousel-btn" type="button" data-carousel-prev
                aria-label="Scroll categories left">{icon("chev-left")}</button>
        <button class="carousel-btn" type="button" data-carousel-next
                aria-label="Scroll categories right">{icon("chev-right")}</button>
      </div>
    </div>
    <div class="carousel-shell">
      <div class="carousel" role="region" aria-label="Content categories" tabindex="0">{tiles}
      </div>
    </div>
    <p class="pricing-note" style="margin-top:.5rem">Category artwork is illustrative. ONE IPTV does
       not use third-party broadcaster logos and is not affiliated with any television network.</p>
  </div>
</section>
"""


# TMDB rows shown in the film showcase. Must match config.js -> tmdb.rows ids.
TMDB_ROWS = [
    ("trending-movies", "Trending films"),
]


def film_showcase(heading="Films &amp; Series You'll Recognise"):
    """Live TMDB poster rows with a skeleton placeholder and static fallback tiles.
    If JS/TMDB is unavailable, the fallback category tiles remain visible."""
    def skeletons(n=8):
        return "".join('<div class="skeleton" aria-hidden="true"></div>' for _ in range(n))

    # Fallback tiles use our own category artwork so no-JS users still see content.
    fallback = "".join(f"""
        <a class="tile" href="/channels/" aria-label="{name}">
          <img src="/assets/img/cat-{slug}.svg" alt="{name} artwork" loading="lazy"
               decoding="async" width="300" height="400">
          <span class="tile__overlay"><span class="tile__tag">{tag}</span>
            <h3>{name}</h3><p>{desc}</p></span>
        </a>""" for slug, name, tag, desc in CATEGORIES[:6])

    rows = "".join(f"""
      <div class="tmdb-row" data-carousel>
        <div class="tmdb-row__head">
          <h3>{label}</h3>
          <div class="tmdb-row__nav carousel-nav" data-carousel-nav>
            <button class="carousel-btn" type="button" data-carousel-prev
                    aria-label="Scroll {label} left">{icon("chev-left")}</button>
            <button class="carousel-btn" type="button" data-carousel-next
                    aria-label="Scroll {label} right">{icon("chev-right")}</button>
          </div>
        </div>
        <div class="carousel-shell">
          <div class="carousel film-track" data-tmdb-track="{rid}" role="region"
               aria-label="{label}" tabindex="0">{skeletons()}</div>
        </div>
      </div>""" for rid, label in TMDB_ROWS)

    return f"""<section class="section" id="films">
  <div class="glow glow--red" style="width:640px;height:640px;top:-160px;right:-240px;opacity:.28"></div>
  <div class="wrap">
    <div class="section-head reveal" style="text-align:left;max-width:none">
      <span class="eyebrow">Films &amp; Series</span>
      <h2 style="margin-bottom:.5rem">{heading}</h2>
      <p style="margin:0;max-width:70ch">A live look at popular films and series, so you can see the
         kind of titles people watch. Actual availability depends on your plan and on what the
         service carries at the time — ask us about anything specific before you order.</p>
    </div>

    <div class="tmdb-rows is-loading reveal" data-tmdb>{rows}
    </div>

    <noscript>
      <div class="grid grid-3" style="margin-top:1.5rem">{fallback}</div>
    </noscript>

    <p class="tmdb-attr" data-tmdb-attr hidden>
      Film and series data and images provided by
      <a href="https://www.themoviedb.org/" target="_blank" rel="noopener">The Movie Database (TMDB)</a>.
      This product uses the TMDB API but is not endorsed or certified by TMDB.
    </p>
    <p class="pricing-note" style="margin-top:1rem;text-align:left">Posters are shown for
       illustration. ONE IPTV is not affiliated with the studios, distributors or networks behind
       any title.</p>
  </div>
</section>
"""


def film_marquee():
    """Full-bleed, text-free poster strip that auto-scrolls every 2 seconds.
    Live TMDB posters (single trending row); falls back to category artwork."""
    skeletons = "".join('<div class="skeleton skeleton--poster" aria-hidden="true"></div>'
                        for _ in range(12))
    return f"""<section class="film-strip" id="films" aria-label="Popular films and series">
  <div class="tmdb-rows is-loading" data-tmdb>
    <div class="film-marquee-shell" data-carousel data-autoscroll>
      <div class="carousel film-track film-marquee" data-tmdb-track="trending-movies"
           data-tmdb-notext role="region" aria-label="Popular film posters" tabindex="0">{skeletons}</div>
      <span class="film-strip__fade film-strip__fade--l" aria-hidden="true"></span>
      <span class="film-strip__fade film-strip__fade--r" aria-hidden="true"></span>
    </div>
  </div>
  <p class="tmdb-attr wrap" data-tmdb-attr hidden style="justify-content:center">
    Film data and images provided by
    <a href="https://www.themoviedb.org/" target="_blank" rel="noopener">The Movie Database (TMDB)</a>.
    Posters are illustrative; ONE IPTV is not affiliated with the studios behind any title.
  </p>
</section>
"""


def _brand_chip(logo, wide):
    cls = "brand-chip brand-chip--wide" if wide else "brand-chip"
    return f'<span class="{cls}">{brand_svg(logo)}</span>'


def devices_section(heading="Watch ONE IPTV on Your Favorite Devices"):
    cards = "".join(f"""
        <article class="card device-brand reveal">
          <div class="device-brand__logos">{"".join(_brand_chip(l, w) for l, w in brands)}</div>
          <h3>{name}</h3>
          <p>{body}</p>
        </article>""" for ic, name, body, brands in DEVICES)
    return f"""<section class="section" id="devices">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Devices</span>
      <h2>{heading}</h2>
      <p>One account, whichever screen is closest. Install a compatible IPTV app, enter the
         details we send you, and you are watching.</p>
    </div>
    <div class="grid grid-3">{cards}
    </div>
    <p class="pricing-note">
      <strong style="color:var(--text-muted)">Easy setup on compatible devices.</strong>
      Not sure whether your model qualifies? Message us on
      <a href="{WA_URL}" data-whatsapp-link target="_blank" rel="noopener"
        style="color:var(--red-bright)">WhatsApp</a> with the make and model and we will tell you
      before you order.
    </p>
    <p class="pricing-note" style="margin-top:.6rem;font-size:.8rem">
      Brand and platform names and logos shown here are the property of their respective owners
      and indicate device compatibility only. ONE IPTV is independent and is not affiliated with,
      sponsored by or endorsed by any of them.
    </p>
  </div>
</section>
"""


def brand_strip_section(heading=None):
    logos = "".join(f'<span title="{l.title()}">{brand_svg(l, label=l.title())}</span>'
                    for l in BRAND_STRIP)
    head = f'<p class="center" style="color:var(--text-dim);font-size:.82rem;letter-spacing:.1em;text-transform:uppercase;margin-bottom:1rem">{heading}</p>' if heading else ""
    return f"""<section class="section--tight" style="padding-block:2.4rem">
  <div class="wrap">
    {head}
    <div class="brand-strip reveal">{logos}</div>
  </div>
</section>
"""


# Plan cards are populated from config.js by main.js (syncPricing), but we also
# render name, term, price and features into the static HTML so the section is
# fully readable with JavaScript disabled and for search engines.
# Fields: (id, name, months, bonusMonths, base_price, badge, featured, features)
# These MIRROR config.js — keep them in step.
_FEAT_STD = [
    "25,000+ live TV channels", "100,000+ movies & series", "4K / FHD / HD quality",
    "All US &amp; international channels", "Compatible with all devices", "TV guide (EPG)",
    "Netflix, Prime Video &amp; more", "100% stable servers", "24/7 technical support",
    "Instant delivery",
]
_FEAT_EXC = [
    "130,000+ live TV channels", "140,000+ movies &amp; series", "4K / FHD / HD quality",
    "All international channels", "Compatible with all devices", "TV guide (EPG)",
    "Netflix, Prime Video &amp; more", "100% stable servers", "24/7 technical support",
    "Instant delivery",
]
PLAN_SHELL = [
    ("bronze", "Bronze", 12, 0, "39.99", None, False, _FEAT_STD),
    ("gold", "Gold", 15, 3, "49.99", "Most popular", True, _FEAT_STD),
    ("platinum", "Platinum", 15, 3, "59.99", None, False, _FEAT_STD),
    ("exclusive", "Exclusive", 24, 3, "84.99", "Best value", False, _FEAT_EXC),
]


def _plan_card(plan_id, name, months, bonus, base_price, badge, featured, features):
    badge_html = (f'<span class="plan__badge" data-plan-badge>{badge}</span>'
                  if badge else '<span class="plan__badge" data-plan-badge hidden></span>')
    bonus_html = (f' <span class="plan__bonus">+{bonus} month{"s" if bonus != 1 else ""} free</span>'
                  if bonus else "")
    term_txt = f'{months} month{"s" if months != 1 else ""}'
    price_txt = f"£{base_price}" if base_price else "£XX.XX"   # keep symbol in step with config.js currency
    feats = "".join(f'<li>{icon("check")}<span>{f}</span></li>' for f in features)
    return f"""
      <article class="card plan{' plan--featured' if featured else ''} reveal" data-plan="{plan_id}">
        {badge_html}
        <p class="plan__name" data-plan-name>{name}</p>
        <p class="plan__term" data-plan-term>{term_txt}{bonus_html}</p>
        <p class="plan__price">
          <span class="amount" data-plan-price>{price_txt}</span>
          <span class="per" data-plan-per>/ {term_txt}</span>
        </p>

        <div class="stepper" data-plan-stepper role="group"
             aria-label="Number of simultaneous connections for {name}">
          <button class="stepper__btn" type="button" data-conn-dec aria-label="Fewer connections">&minus;</button>
          <span class="stepper__val">
            <b data-conn-count>1</b>
            <span data-conn-label>connection</span>
          </span>
          <button class="stepper__btn" type="button" data-conn-inc aria-label="More connections">+</button>
        </div>
        <p class="plan__conn-note" data-conn-note>First connection at full price · each extra
           <b>15% off</b></p>

        <ul class="plan__list" data-plan-features>{feats}</ul>
        <button class="btn {'btn--primary' if featured else 'btn--ghost'} btn--block"
                type="button" data-open-checkout="{plan_id}">Order Now</button>
      </article>"""


def pricing_section(heading="Choose Your Plan", with_switch=False):
    cards = "".join(_plan_card(*p) for p in PLAN_SHELL)
    return f"""<section class="section" id="pricing">
  <div class="glow glow--red" style="width:640px;height:640px;top:-160px;left:50%;
       transform:translateX(-50%);opacity:.28"></div>
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Pricing</span>
      <h2>{heading}</h2>
      <p>Transparent pricing, no hidden extras. Use the + / − control on each plan to set how many
         devices stream at once — the price updates automatically, with every extra connection
         discounted.</p>
    </div>
    <div class="pricing-grid pricing-grid--4">{cards}
    </div>
    <p class="pricing-note">
      First connection at the normal price · each additional connection 15% cheaper. Questions
      before you order? Message us on
      <a href="{WA_URL}" data-whatsapp-link target="_blank" rel="noopener"
        style="color:var(--red-bright)">WhatsApp</a>. No payment card details are collected on
      this website.
    </p>
  </div>
</section>
"""


def faq_section(items, heading="Frequently Asked Questions", intro=None, start=0):
    intro = intro or ("Straight answers to the questions we are asked most. If yours is not "
                      "here, call us — we would rather explain it properly.")
    blocks = []
    for i, (q, a) in enumerate(items, start=start):
        blocks.append(f"""
      <div class="faq-item">
        <h3 style="margin:0">
          <button class="faq-q" type="button" aria-expanded="false" aria-controls="faq-a-{i}"
                  id="faq-q-{i}">
            <span>{q}</span>
            <span class="faq-q__icon" aria-hidden="true"></span>
          </button>
        </h3>
        <div class="faq-a" id="faq-a-{i}" role="region" aria-labelledby="faq-q-{i}">
          <div class="faq-a__inner">{a}</div>
        </div>
      </div>""")
    return f"""<section class="section" id="faq">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">FAQ</span>
      <h2>{heading}</h2>
      <p>{intro}</p>
    </div>
    <div class="faq">{''.join(blocks)}
    </div>
  </div>
</section>
"""


def contact_section(heading="Need Help?"):
    return f"""<section class="section" id="contact">
  <div class="wrap">
    <div class="cta-panel reveal">
      <div class="grid grid-2" style="align-items:center;gap:clamp(1.6rem,4vw,3rem)">
        <div>
          <span class="eyebrow">Support</span>
          <h2>{heading}</h2>
          <p class="lead">Our support team is available on WhatsApp to help with setup, plans and
             general questions. A quick message is usually faster than typing out a long form.</p>
          <div style="display:flex;flex-wrap:wrap;gap:.8rem;margin-top:1.6rem">
            <a class="phone-cta" href="{WA_URL}" data-whatsapp-link target="_blank" rel="noopener">
              <span class="phone-cta__icon">{icon("whatsapp")}</span>
              <span><small>Message us on</small><strong>WhatsApp</strong></span>
            </a>
          </div>
          <div style="display:flex;flex-wrap:wrap;gap:.7rem;margin-top:1.2rem">
            <a class="btn btn--primary" href="{WA_URL}" data-whatsapp-link target="_blank" rel="noopener">
              {icon("whatsapp")}Chat on WhatsApp</a>
            <a class="btn btn--ghost" href="/contact/">{icon("message")}Contact Us</a>
          </div>
        </div>
        <div class="grid" style="gap:.9rem">
          <div class="card" style="padding:1.3rem">
            <div style="display:flex;gap:.9rem;align-items:flex-start">
              <span class="card__icon" style="width:42px;height:42px;margin:0;border-radius:12px">
                {icon("headset")}</span>
              <div><h3 style="font-size:1rem;margin-bottom:.2rem">Setup assistance</h3>
                <p style="font-size:.9rem">We will walk you through installing a compatible app
                   and entering your details, device by device.</p></div>
            </div>
          </div>
          <div class="card" style="padding:1.3rem">
            <div style="display:flex;gap:.9rem;align-items:flex-start">
              <span class="card__icon" style="width:42px;height:42px;margin:0;border-radius:12px">
                {icon("sliders")}</span>
              <div><h3 style="font-size:1rem;margin-bottom:.2rem">Plan questions</h3>
                <p style="font-size:.9rem">Not sure whether to start with one month or commit for
                   longer? Ask, and we will give you a straight answer.</p></div>
            </div>
          </div>
          <div class="card" style="padding:1.3rem">
            <div style="display:flex;gap:.9rem;align-items:flex-start">
              <span class="card__icon" style="width:42px;height:42px;margin:0;border-radius:12px">
                {icon("wifi")}</span>
              <div><h3 style="font-size:1rem;margin-bottom:.2rem">Playback troubleshooting</h3>
                <p style="font-size:.9rem">Buffering, a channel that will not load, a new router —
                   we will help you work out where the problem sits.</p></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
"""


def img_src(p):
    """Blog thumbnail path. Posts default to generated SVG artwork; a post can set
    "img_ext" (e.g. "webp") when it uses a real photograph instead."""
    return f"/assets/img/{p['img']}.{p.get('img_ext', 'svg')}"


def og_src(p):
    """Social-card image for a post: a JPG when one exists, else the site default."""
    return p.get("og_img", "/assets/img/og-image.png")


def blog_cards(posts, limit=None):
    items = posts[:limit] if limit else posts
    return "".join(f"""
      <article class="card post-card reveal">
        <a href="/blog/{p['slug']}/" class="post-card__media" tabindex="-1" aria-hidden="true">
          <img src="{img_src(p)}" alt="" loading="lazy" decoding="async"
               width="800" height="450">
        </a>
        <div class="post-card__body">
          <div class="post-card__meta">
            <span class="tag">{p['tag']}</span>
            <time datetime="{p['date']}">{fmt_date(p['date'])}</time>
            <span>{p['read']}</span>
          </div>
          <h3><a href="/blog/{p['slug']}/">{p['title']}</a></h3>
          <p>{p['excerpt']}</p>
          <span class="post-card__link">Read the guide {icon("arrow-right")}</span>
        </div>
      </article>""" for p in items)


def blog_preview():
    return f"""<section class="section" id="blog">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Blog</span>
      <h2>Guides &amp; Setup Help</h2>
      <p>Practical walkthroughs written for people setting up IPTV for the first time —
         no jargon, no filler.</p>
    </div>
    <div class="grid grid-3">{blog_cards(POSTS, 3)}
    </div>
    <p class="center mt-lg" style="margin-bottom:0">
      <a class="btn btn--ghost" href="/blog/">View all guides {icon("arrow-right")}</a>
    </p>
  </div>
</section>
"""


def strip_section():
    items = [
        ("Multi-device", "One account, many screens"),
        ("Quick setup", "Minutes, not afternoons"),
        ("Flexible terms", "12 to 24 months"),
        ("Human support", "Message us on WhatsApp"),
    ]
    cells = "".join(f"""
      <div class="strip__item"><h3>{a}</h3><p>{b}</p></div>""" for a, b in items)
    return f"""<section class="strip">
  <div class="wrap"><div class="strip__grid">{cells}
  </div></div>
</section>
"""
