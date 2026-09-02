#!/usr/bin/env python3
"""Blog article page assembly."""
import json

from shell import page, icon, ld, SITE, BRAND, PHONE_DISPLAY, PHONE_TEL
import content as C
import posts_a as A
import posts_b as B
import posts_c as Cc

ARTICLES = {
    "one-iptv-complete-guide-for-beginners": A.BEGINNERS,
    "how-to-set-up-one-iptv-on-a-smart-tv": A.SMART_TV,
    "smart-one-iptv-what-you-need-to-know": A.SMART_ONE,
    "iptv-one-month-plans-what-to-consider": A.ONE_MONTH,
    "one-iptv-uk-getting-started-guide": B.UK_GUIDE,
    "smart-one-iptv-app-download-setup-guide": B.APP_DOWNLOAD,
    "how-to-set-up-iptv-on-your-tv": B.TV_SETUP,
    "iptv-on-xbox-one-does-it-work": Cc.XBOX_ONE,
    "iptv-app-for-tv-how-to-choose": Cc.APP_FOR_TV,
}


def _related(post):
    others = [p for p in C.POSTS if p["slug"] != post["slug"]][:3]
    return f"""<section class="section section--tight">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Keep reading</span>
      <h2>Related guides</h2>
    </div>
    <div class="grid grid-3">{C.blog_cards(others)}
    </div>
  </div>
</section>
"""


def _cta(post):
    return f"""<section class="section section--tight">
  <div class="wrap">
    <div class="cta-panel reveal" style="text-align:center">
      <span class="eyebrow">Ready when you are</span>
      <h2>Get ONE IPTV set up today</h2>
      <p class="lead" style="max-width:58ch;margin-inline:auto">Choose a plan, tell us your
         device, and we will send your details with setup instructions written for it. Stuck at
         any point? Message us and we will walk you through it.</p>
      <p style="margin-top:1.8rem;display:flex;gap:.7rem;flex-wrap:wrap;justify-content:center">
        <a class="btn btn--primary btn--lg" href="/pricing/">View Plans {icon("arrow-right")}</a>
        <button class="btn btn--ghost btn--lg" type="button" data-open-checkout>Get Started</button>
        <a class="btn btn--outline btn--lg" href="https://wa.me/16615413954" data-whatsapp-link
           target="_blank" rel="noopener">{icon("whatsapp")}WhatsApp</a>
      </p>
    </div>
  </div>
</section>
"""


def article_page(post, body_html):
    url = f"/blog/{post['slug']}/"
    trail = [("Home", "/"), ("Blog", "/blog/"), (post["title"], None)]
    crumbs = "".join(
        f'<li><a href="{href}">{label}</a></li>' if href else f"<li>{label}</li>"
        for label, href in trail
    )

    article_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post["title"],
        "description": post["desc"],
        "image": SITE + f"/assets/img/{post['img']}.svg",
        "datePublished": post["date"],
        "dateModified": post["date"],
        "author": {"@type": "Organization", "name": BRAND, "url": SITE + "/"},
        "publisher": {"@id": SITE + "/#organization"},
        "mainEntityOfPage": {"@type": "WebPage", "@id": SITE + url},
        "inLanguage": "en",
        "keywords": post["kw"]
    }, ensure_ascii=False)

    bcs = json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i, "name": label,
             **({"item": SITE + href} if href else {})}
            for i, (label, href) in enumerate(trail, 1)
        ]
    }, ensure_ascii=False)

    hero = f"""<article>
<header class="article-hero">
  <div class="wrap" style="max-width:820px">
    <ol class="breadcrumb">{crumbs}</ol>
    <span class="eyebrow">{post['tag']}</span>
    <h1>{post['title']}</h1>
    <p class="lead">{post['excerpt']}</p>
    <div class="article-meta">
      <span>Published <time datetime="{post['date']}">{C.fmt_date(post['date'])}</time></span>
      <span>{post['read']}</span>
      <span>By the {BRAND} team</span>
    </div>
  </div>
</header>

<div class="section section--tight">
  <div class="wrap">
    <img src="/assets/img/{post['img']}.svg" alt="" width="800" height="450" loading="lazy"
         decoding="async" style="border-radius:var(--r-lg);border:1px solid var(--border);
         max-width:820px;margin:0 auto 2.5rem;width:100%">
    <div class="prose">
{body_html}
      <div class="article-nav">
        <a class="btn btn--ghost" href="/blog/">{icon("chev-left")} All guides</a>
        <a class="btn btn--primary" href="/pricing/">View plans {icon("arrow-right")}</a>
      </div>
    </div>
  </div>
</div>
</article>
"""

    extra_head = ld(article_schema) + ld(bcs)
    if post.get("faqs"):
        extra_head += ld(C.faq_schema(post["faqs"]))

    return page(
        title=post["seo_title"],
        description=post["desc"],
        path=url,
        og_type="article",
        keywords=post["kw"],
        body=hero + _cta(post) + _related(post),
        extra_head=extra_head,
    )
