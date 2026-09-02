#!/usr/bin/env python3
"""Shared page shell: <head> SEO, header, mobile nav, footer, checkout modal."""

import os
import re

SITE = "https://www.one-iptv.website"
BRAND = "ONE IPTV"
PHONE_DISPLAY = "+1 (661) 541-3954"
PHONE_TEL = "+16615413954"
EMAIL = "support@one-iptv.website"

NAV = [
    ("Home", "/"),
    ("Features", "/features/"),
    ("Channels", "/channels/"),
    ("Pricing", "/pricing/"),
    ("Devices", "/devices/"),
    ("FAQ", "/faq/"),
    ("Blog", "/blog/"),
    ("Contact", "/contact/"),
]

# ---------------------------------------------------------------- icons ----
ICONS = {
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
    # WhatsApp glyph (filled). Rendered with fill via .icon-fill helper.
    "whatsapp": '<path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22h.01c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2zm0 1.8c2.17 0 4.2.85 5.74 2.38a8.06 8.06 0 0 1 2.37 5.73c0 4.47-3.64 8.11-8.12 8.11a8.2 8.2 0 0 1-4.13-1.13l-.3-.18-3.12.82.83-3.04-.19-.31a8.07 8.07 0 0 1-1.24-4.28c0-4.48 3.64-8.12 8.12-8.12zm-2.67 3.7c-.16 0-.42.06-.64.3-.22.24-.85.83-.85 2.02s.87 2.35.99 2.51c.12.16 1.7 2.6 4.13 3.64.58.25 1.03.4 1.38.51.58.18 1.11.16 1.53.1.47-.07 1.43-.58 1.63-1.15.2-.57.2-1.05.14-1.15-.06-.1-.22-.16-.46-.28-.24-.12-1.43-.7-1.65-.78-.22-.08-.38-.12-.54.12-.16.24-.62.78-.76.94-.14.16-.28.18-.52.06-.24-.12-1.02-.38-1.94-1.2-.72-.64-1.2-1.43-1.34-1.67-.14-.24-.02-.37.1-.49.11-.11.24-.28.36-.42.12-.14.16-.24.24-.4.08-.16.04-.3-.02-.42-.06-.12-.53-1.32-.73-1.8-.19-.47-.39-.4-.53-.41z"/>',
    "play": '<polygon points="5 3 19 12 5 21 5 3"/>',
    "check": '<polyline points="20 6 9 17 4 12"/>',
    "arrow-right": '<line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>',
    "chev-left": '<polyline points="15 18 9 12 15 6"/>',
    "chev-right": '<polyline points="9 18 15 12 9 6"/>',
    "close": '<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>',
    "tv": '<rect x="2" y="4" width="20" height="14" rx="2"/><polyline points="8 21 12 18 16 21"/>',
    "monitor": '<rect x="2" y="3" width="20" height="13" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/>',
    "smartphone": '<rect x="6" y="2" width="12" height="20" rx="2.5"/><line x1="10.5" y1="18.5" x2="13.5" y2="18.5"/>',
    "tablet": '<rect x="4" y="2" width="16" height="20" rx="2.5"/><line x1="10.5" y1="18.5" x2="13.5" y2="18.5"/>',
    "box": '<path d="M21 8v8a2 2 0 0 1-1 1.73l-7 4a2 2 0 0 1-2 0l-7-4A2 2 0 0 1 3 16V8a2 2 0 0 1 1-1.73l7-4a2 2 0 0 1 2 0l7 4A2 2 0 0 1 21 8z"/><polyline points="3.3 7 12 12 20.7 7"/><line x1="12" y1="22" x2="12" y2="12"/>',
    "flame": '<path d="M12 2s4 4.5 4 8a4 4 0 0 1-8 0c0-1 .4-2 1-2.8"/><path d="M12 22a7 7 0 0 0 7-7c0-3-2-5-3.5-7"/><path d="M12 22a7 7 0 0 1-7-7c0-2 1-3.6 2.2-5"/>',
    "zap": '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
    "layers": '<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>',
    "sliders": '<line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><line x1="1" y1="14" x2="7" y2="14"/><line x1="9" y1="8" x2="15" y2="8"/><line x1="17" y1="16" x2="23" y2="16"/>',
    "wifi": '<path d="M5 12.55a11 11 0 0 1 14.08 0"/><path d="M1.42 9a16 16 0 0 1 21.16 0"/><path d="M8.53 16.11a6 6 0 0 1 6.95 0"/><line x1="12" y1="20" x2="12.01" y2="20"/>',
    "headset": '<path d="M3 18v-6a9 9 0 0 1 18 0v6"/><path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3z"/><path d="M3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>',
    "card": '<rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/>',
    "paypal": '<path d="M7 20l1.5-9h4a3 3 0 0 0 0-6H7L4.5 20z"/><path d="M10 16h3.5a3.5 3.5 0 0 0 0-7H10.5"/>',
    "crypto": '<circle cx="12" cy="12" r="9"/><path d="M9.5 8h4a2 2 0 0 1 0 4h-4m0 0h4.3a2 2 0 0 1 0 4H9.5m0-8v10m2-11v1m0 9v1"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><polyline points="2.5 6.5 12 13 21.5 6.5"/>',
    "message": '<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8z"/>',
    "sparkle": '<path d="M12 3l1.9 5.6L19.5 10l-5.6 1.9L12 17.5l-1.9-5.6L4.5 10l5.6-1.4L12 3z"/><path d="M19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8z"/>',
    "cast": '<path d="M2 16.1A5 5 0 0 1 5.9 20"/><path d="M2 12.05A9 9 0 0 1 9.95 20"/><path d="M2 8V6a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2h-6"/><line x1="2" y1="20" x2="2.01" y2="20"/>',
    "lock": '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "users": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>',
}


# Glyphs drawn as solid shapes rather than strokes.
_FILLED = {"whatsapp"}


def icon(name, cls=""):
    body = ICONS.get(name, "")
    c = f' class="{cls}"' if cls else ""
    if name in _FILLED:
        return (f'<svg{c} viewBox="0 0 24 24" fill="currentColor" '
                f'aria-hidden="true" focusable="false">{body}</svg>')
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{body}</svg>')


# ---- brand logos (inlined from assets/img/brands/*.svg) ---------------------
_BRAND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "img", "brands")
_BRAND_CACHE = {}


def brand_svg(name, cls="", label=None):
    """Return an inline <svg> for a brand logo, stripped of <title> and sized by CSS."""
    if name not in _BRAND_CACHE:
        path = os.path.join(_BRAND_DIR, name + ".svg")
        with open(path, encoding="utf-8") as fh:
            raw = fh.read()
        # drop the <title> (we set aria-label instead) and any role attr
        raw = re.sub(r"<title>.*?</title>", "", raw, flags=re.S)
        # extract viewBox + inner
        vb = re.search(r'viewBox=[\'"]([^\'"]+)[\'"]', raw)
        vb = vb.group(1) if vb else "0 0 24 24"
        inner = re.search(r"<svg[^>]*>(.*)</svg>", raw, flags=re.S)
        inner = inner.group(1).strip() if inner else ""
        _BRAND_CACHE[name] = (vb, inner)
    vb, inner = _BRAND_CACHE[name]
    c = f' class="{cls}"' if cls else ""
    lab = f' aria-label="{label}" role="img"' if label else ' aria-hidden="true"'
    return f'<svg{c} viewBox="{vb}"{lab} focusable="false">{inner}</svg>'


# ---------------------------------------------------------------- head -----
def head(title, description, path, *, og_type="website", extra_head="", image="/assets/img/og-image.png",
         keywords=""):
    canonical = SITE + path
    kw = f'\n  <meta name="keywords" content="{keywords}">' if keywords else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">{kw}
  <link rel="canonical" href="{canonical}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
  <meta name="theme-color" content="#07070a">
  <meta name="author" content="{BRAND}">

  <!-- Open Graph -->
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="{BRAND}">
  <meta property="og:locale" content="en_US">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE}{image}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{BRAND} — premium IPTV service for Smart TVs and streaming devices">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{SITE}{image}">
  <meta name="twitter:image:alt" content="{BRAND} — premium IPTV service for Smart TVs and streaming devices">

  <link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/assets/img/icon-512.png" sizes="512x512" type="image/png">
  <link rel="apple-touch-icon" href="/assets/img/icon-180.png">
  <link rel="manifest" href="/site.webmanifest">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" as="style"
        href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap">
  <link rel="stylesheet"
        href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap"
        media="print" onload="this.media='all'">
  <noscript><link rel="stylesheet"
        href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap"></noscript>

  <link rel="stylesheet" href="/assets/css/styles.css">
  <script>document.documentElement.className+=" js";</script>
{extra_head}</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
"""


# -------------------------------------------------------------- header -----
def header():
    nav_links = "".join(f'<a href="{href}">{label}</a>' for label, href in NAV)
    mnav_links = "".join(
        f'<a class="mnav-link" href="{href}">{label}<span>{icon("chev-right")}</span></a>'
        for label, href in NAV
    )
    return f"""<header class="site-header">
  <div class="wrap header-inner">
    <a class="logo" href="/" aria-label="{BRAND} home">
      <span class="logo__mark">{icon("play")}</span>
      <span class="logo__text">ONE <b>IPTV</b></span>
    </a>

    <nav class="nav" aria-label="Primary">
      {nav_links}
    </nav>

    <div class="header-actions">
      <a class="header-phone header-wa" href="#" data-whatsapp-link target="_blank" rel="noopener"
         aria-label="Message {BRAND} on WhatsApp">
        {icon("whatsapp")}<span>WhatsApp</span>
      </a>
      <a class="btn btn--ghost btn--sm" href="/contact/">Contact Us</a>
      <button class="btn btn--primary btn--sm" type="button" data-open-checkout>Get Started</button>
      <button class="burger" type="button" aria-expanded="false" aria-controls="mobile-nav"
              aria-label="Open navigation menu"><span></span></button>
    </div>
  </div>
</header>

<div class="mobile-nav" id="mobile-nav" aria-hidden="true">
  <nav aria-label="Mobile">
    {mnav_links}
  </nav>
  <div class="mnav-actions">
    <a class="btn btn--ghost btn--block" href="#" data-whatsapp-link target="_blank" rel="noopener">
      {icon("whatsapp")}<span>WhatsApp us</span>
    </a>
    <button class="btn btn--primary btn--block" type="button" data-open-checkout>Get Started</button>
  </div>
</div>
"""


# -------------------------------------------------------------- footer -----
def footer():
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="logo" href="/" aria-label="{BRAND} home">
          <span class="logo__mark">{icon("play")}</span>
          <span class="logo__text">ONE <b>IPTV</b></span>
        </a>
        <p>ONE IPTV is a modern IPTV service built for compatible Smart TVs, streaming
           boxes and mobile devices — with straightforward plans and human support.</p>
        <p style="margin-top:1.1rem">
          <a class="phone-cta" href="#" data-whatsapp-link target="_blank" rel="noopener">
            <span class="phone-cta__icon">{icon("whatsapp")}</span>
            <span><small>Message us on</small><strong>WhatsApp</strong></span>
          </a>
        </p>
      </div>

      <div class="footer-col">
        <h4>Explore</h4>
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/features/">Features</a></li>
          <li><a href="/channels/">Channels</a></li>
          <li><a href="/pricing/">Pricing</a></li>
          <li><a href="/devices/">Devices</a></li>
        </ul>
      </div>

      <div class="footer-col">
        <h4>Support</h4>
        <ul>
          <li><a href="/faq/">FAQ</a></li>
          <li><a href="/contact/">Contact</a></li>
          <li><a href="/blog/">Blog</a></li>
          <li><a href="#" data-whatsapp-link target="_blank" rel="noopener">WhatsApp us</a></li>
        </ul>
      </div>

      <div class="footer-col">
        <h4>Guides</h4>
        <ul>
          <li><a href="/blog/one-iptv-complete-guide-for-beginners/">Beginner's guide</a></li>
          <li><a href="/blog/how-to-set-up-one-iptv-on-a-smart-tv/">Smart TV setup</a></li>
          <li><a href="/blog/iptv-one-month-plans-what-to-consider/">IPTV one month plans</a></li>
          <li><a href="/blog/one-iptv-uk-getting-started-guide/">ONE IPTV UK</a></li>
          <li><a href="/blog/smart-one-iptv-app-download-setup-guide/">App download guide</a></li>
          <li><a href="/blog/iptv-app-for-tv-how-to-choose/">Choosing an IPTV app</a></li>
          <li><a href="/blog/iptv-on-xbox-one-does-it-work/">IPTV on Xbox One</a></li>
        </ul>
      </div>
    </div>

    <div class="disclaimer">
      <p><strong>Service disclaimer.</strong> ONE IPTV provides access to an IPTV streaming
      service and related technical support. Availability of any particular content, feature
      or stream depends on your plan, your internet connection, your device and the content
      that is available through the service at the time. Nothing on this website should be
      read as a guarantee of specific content, specific networks, uninterrupted availability
      or a fixed number of streams.</p>
      <p><strong>No third-party affiliation.</strong> ONE IPTV is an independent brand. Device,
      platform and application names referenced on this site — including Smart TV platforms,
      Android TV, Fire TV, and any third-party IPTV player applications — are the property of
      their respective owners and are mentioned only to describe device compatibility. Their
      mention does not imply any partnership, sponsorship, endorsement or affiliation.</p>
      <p><strong>Customer responsibility.</strong> Customers are responsible for using the
      service in line with the laws and regulations that apply where they live, and for
      ensuring they hold any rights or permissions required for the content they choose to
      access. If you have questions about what is available in your country, contact us
      before ordering.</p>
      <p><strong>Payments.</strong> This website does not collect, process or store payment
      card details. Orders placed through the order form are handed to our support team or to
      a PCI-compliant third-party payment provider to complete.</p>
    </div>

    <div class="footer-bottom">
      <p style="margin:0">© <span data-year>2026</span> {BRAND}. All rights reserved.</p>
      <nav aria-label="Footer">
        <a href="/privacy/">Privacy Policy</a>
        <a href="/terms/">Terms of Service</a>
        <a href="/refund-policy/">Refund Policy</a>
        <a href="/sitemap.xml">Sitemap</a>
      </nav>
    </div>
  </div>
</footer>

<a class="fab-call fab-wa" href="#" data-whatsapp-link target="_blank" rel="noopener"
   aria-label="Message {BRAND} on WhatsApp">{icon("whatsapp")}</a>
"""


# ------------------------------------------------------ checkout modal -----
def modal():
    return f"""<div class="modal" id="checkout-modal" role="dialog" aria-modal="true"
     aria-labelledby="checkout-title" aria-hidden="true">
  <div class="modal__backdrop" data-checkout-close></div>
  <div class="modal__panel">
    <button class="modal__close" type="button" data-checkout-close aria-label="Close checkout">
      {icon("close")}
    </button>

    <div data-checkout-form-view>
      <h2 id="checkout-title">Finalisez votre commande</h2>
      <p class="modal__lead">Vérifiez votre formule et renseignez vos coordonnées pour continuer.</p>

      <div class="summary">
        <div class="summary__row"><span>Abonnement</span><span data-sum-plan>—</span></div>
        <div class="summary__row"><span>Connexions</span><span data-sum-conn>—</span></div>
        <div class="summary__row summary__row--total"><span>Total à régler</span><span data-sum-total>—</span></div>
        <p style="font-size:.78rem;margin:.8rem 0 0;color:var(--text-dim)" data-sum-note hidden>
          Le tarif est en cours de finalisation. Validez votre commande et nous vous confirmerons
          le montant exact avant tout paiement.
        </p>
      </div>

      <form id="checkout-form" novalidate>
        <div class="field">
          <label for="co-name">Nom complet</label>
          <input id="co-name" name="name" type="text" autocomplete="name"
                 placeholder="Jean Dupont" data-validate required>
          <span class="field-error" role="alert"></span>
        </div>

        <div class="field">
          <label for="co-email">Adresse e-mail</label>
          <input id="co-email" name="email" type="email" autocomplete="email"
                 placeholder="jean.dupont@email.fr" data-validate required>
          <span class="field-error" role="alert"></span>
        </div>

        <div class="field">
          <label for="co-phone">Téléphone</label>
          <div class="phone-row">
            <select id="co-phone-cc" class="phone-cc" data-phone-cc aria-label="Indicatif pays"></select>
            <input id="co-phone" name="phone" type="tel" autocomplete="tel"
                   placeholder="6 12 34 56 78" data-validate required>
          </div>
          <span class="field-error" role="alert"></span>
        </div>

        <fieldset class="pay-methods" data-pay-methods>
          <legend>Mode de paiement</legend>
          <!-- options injected from config.checkout.paymentMethods -->
        </fieldset>

        <button class="btn btn--primary btn--lg btn--block" type="submit" data-checkout-submit>
          Continuer vers le paiement
        </button>

        <p class="modal__note">
          {icon("lock")}<span data-secure-note> Aucune donnée de carte n'est saisie sur ce site.</span>
        </p>
        <p class="modal__note" style="margin-top:.5rem">
          Une question ?
          <a href="#" data-whatsapp-link target="_blank" rel="noopener"
             style="color:var(--red-bright);font-weight:650">WhatsApp <span data-phone-display>{PHONE_DISPLAY}</span></a>
        </p>
        <button class="modal__cancel" type="button" data-checkout-close>Annuler</button>
      </form>
    </div>

    <div class="modal-success" data-checkout-success hidden>
      <div class="modal-success__icon">{icon("check")}</div>
      <h2>Commande reçue</h2>
      <p data-ok-message>Merci — nous revenons vers vous très vite.</p>
      <div class="summary">
        <div class="summary__row"><span>Nom</span><span data-ok-name>—</span></div>
        <div class="summary__row"><span>E-mail</span><span data-ok-email>—</span></div>
        <div class="summary__row"><span>Formule</span><span data-ok-plan>—</span></div>
        <div class="summary__row"><span>Paiement</span><span data-ok-pay>—</span></div>
        <div class="summary__row summary__row--total"><span>Total</span><span data-ok-total>—</span></div>
      </div>
      <a class="btn btn--primary btn--block" href="#" data-whatsapp-link target="_blank" rel="noopener">
        {icon("whatsapp")}Nous contacter sur WhatsApp
      </a>
      <button class="btn btn--ghost btn--block" type="button" data-checkout-close
              style="margin-top:.7rem">Fermer</button>
    </div>
  </div>
</div>
"""


def scripts():
    return """<script src="/assets/js/config.js"></script>
<script src="/assets/js/main.js" defer></script>
<script src="/assets/js/tmdb.js" defer></script>
</body>
</html>
"""


def page(*, title, description, path, body, extra_head="", og_type="website", keywords="",
         image="/assets/img/og-image.png"):
    return (
        head(title, description, path, og_type=og_type, extra_head=extra_head,
             keywords=keywords, image=image)
        + header()
        + '<main id="main">\n'
        + body
        + "\n</main>\n"
        + footer()
        + modal()
        + scripts()
    )


def ld(json_str):
    return f'  <script type="application/ld+json">{json_str}</script>\n'
