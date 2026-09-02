/* ==========================================================================
   ONE IPTV — SITE CONFIGURATION
   --------------------------------------------------------------------------
   This is the ONLY file you need to edit to change prices, plans, contact
   details and the film catalogue. Everything on the site reads from here.
   ========================================================================== */

window.ONE_IPTV_CONFIG = {

  /* ----------------------------------------------------------------------
     1. BRAND & CONTACT
     ---------------------------------------------------------------------- */
  brand: {
    name: "ONE IPTV",
    domain: "one-iptv.website",
    url: "https://www.one-iptv.website"
  },

  contact: {
    // Contact is WhatsApp-only. This is the number used for every wa.me link.
    whatsappNumber: "16615413954",       // no "+", international format
    hours: "Support available 7 days a week"
  },

  /* ----------------------------------------------------------------------
     2. CURRENCY
     ---------------------------------------------------------------------- */
  currency: {
    code: "GBP",       // ISO code, used by Product/Offer schema
    symbol: "£",
    position: "before" // "before" => £19.99   |   "after" => 19.99 £
  },

  /* ----------------------------------------------------------------------
     3. CONNECTIONS (the +/- selector on each pricing card)
     ----------------------------------------------------------------------
     A "connection" is one device streaming at the same time. The first
     connection is charged at the plan's full price; every additional one is
     discounted by `extraDiscount`.

       total = basePrice × (1 + (1 − extraDiscount) × (connections − 1))

     With extraDiscount 0.15, a €40 plan with 3 connections costs
       40 × (1 + 0.85 × 2) = €108.00
     ---------------------------------------------------------------------- */
  connections: {
    min: 1,
    max: 5,
    default: 1,
    extraDiscount: 0.15      // 0.15 = each extra connection is 15% cheaper
  },

  /* ----------------------------------------------------------------------
     4. PLANS  —  EDIT YOUR PRICES HERE
     ----------------------------------------------------------------------
     `basePrice` is the price for ONE connection, as a NUMBER (not a string).

        basePrice: null     -> shows €XX.XX placeholder, no price in SEO data
        basePrice: 39.99    -> real price, stepper maths and Offer schema live

     `months`      = the paid term.
     `bonusMonths` = extra months given free on top (0 = none).
     ---------------------------------------------------------------------- */
  plans: [
    {
      id: "bronze",
      name: "Bronze",
      months: 12,
      bonusMonths: 0,
      basePrice: 39.99,
      tagline: "12 months",
      badge: null,
      featured: false,
      features: [
        "25,000+ live TV channels",
        "100,000+ movies & series",
        "4K / FHD / HD quality",
        "All US & international channels",
        "Compatible with all devices",
        "TV guide (EPG)",
        "Netflix, Prime Video & more",
        "100% stable servers",
        "24/7 technical support",
        "Instant delivery"
      ]
    },
    {
      id: "gold",
      name: "Gold",
      months: 15,
      bonusMonths: 3,
      basePrice: 49.99,
      tagline: "15 months",
      badge: "Most popular",
      featured: true,
      features: [
        "25,000+ live TV channels",
        "100,000+ movies & series",
        "4K / FHD / HD quality",
        "All US & international channels",
        "Compatible with all devices",
        "TV guide (EPG)",
        "Netflix, Prime Video & more",
        "100% stable servers",
        "24/7 technical support",
        "Instant delivery"
      ]
    },
    {
      id: "platinum",
      name: "Platinum",
      months: 15,
      bonusMonths: 3,
      basePrice: 59.99,
      tagline: "15 months",
      badge: null,
      featured: false,
      features: [
        "25,000+ live TV channels",
        "100,000+ movies & series",
        "4K / FHD / HD quality",
        "All US & international channels",
        "Compatible with all devices",
        "TV guide (EPG)",
        "Netflix, Prime Video & more",
        "100% stable servers",
        "24/7 technical support",
        "Instant delivery"
      ]
    },
    {
      id: "exclusive",
      name: "Exclusive",
      months: 24,
      bonusMonths: 3,
      basePrice: 84.99,
      tagline: "24 months",
      badge: "Best value",
      featured: false,
      features: [
        "130,000+ live TV channels",
        "140,000+ movies & series",
        "4K / FHD / HD quality",
        "All international channels",
        "Compatible with all devices",
        "TV guide (EPG)",
        "Netflix, Prime Video & more",
        "100% stable servers",
        "24/7 technical support",
        "Instant delivery"
      ]
    }
  ],

  /* ----------------------------------------------------------------------
     5. FILM & SERIES SHOWCASE (TMDB)
     ----------------------------------------------------------------------
     Pulls live posters from The Movie Database so the catalogue section
     always looks current. If the API is unreachable the section falls back
     to the built-in category artwork, so the page never breaks.

     NOTE: this key is visible to anyone who views the page source — that is
     unavoidable for any browser-side API call. TMDB read keys are low risk
     (read-only, free, rate-limited) but you can rotate it any time at
     themoviedb.org → Settings → API.

     Attribution is required by TMDB's terms and is rendered under the rows.
     ---------------------------------------------------------------------- */
  tmdb: {
    enabled: true,
    apiKey: "eb88f8554c5c594b1b82a59672ee98f4",
    language: "en-US",
    imageBase: "https://image.tmdb.org/t/p/w342",
    backdropBase: "https://image.tmdb.org/t/p/w780",
    maxPerRow: 18,
    rows: [
      { id: "trending-movies", label: "Trending films", path: "/trending/movie/week", type: "movie" }
      // To show more rows again, add e.g.:
      // { id: "trending-series", label: "Popular series", path: "/trending/tv/week", type: "tv" },
      // { id: "top-movies", label: "Top rated films", path: "/movie/top_rated", type: "movie" }
    ]
  },

  /* ----------------------------------------------------------------------
     6. CHECKOUT
     ----------------------------------------------------------------------
     No card details are ever collected or stored by this website.

     mode options:
       "handoff"  — collect details, then send the order via WhatsApp or
                    email so you can invoice the customer manually. (default)
       "redirect" — collect details, then redirect to a hosted checkout URL
                    (Stripe Payment Link, PayPal, Paddle, Lemon Squeezy…).
       "endpoint" — POST the order as JSON to your own backend / form service.
     ---------------------------------------------------------------------- */
  checkout: {
    // Payment methods shown in the order modal (French labels).
    // action: "notify"   -> record the order (sheet + email) and show a
    //                       "we'll send you the payment details" confirmation.
    //         "whatsapp" -> open a pre-filled WhatsApp chat with the order.
    //         "redirect" -> send the customer to `url` (paste a Stripe/PayPal
    //                       hosted link). If url is empty it falls back to notify.
    paymentMethods: [
      { id: "card",     label: "Carte bancaire",   icon: "card",     action: "notify",   url: "" },
      { id: "paypal",   label: "PayPal",           icon: "paypal",   action: "notify",   url: "" },
      { id: "crypto",   label: "Virement / Crypto", icon: "crypto",   action: "notify",   url: "" },
      { id: "whatsapp", label: "Via WhatsApp",     icon: "whatsapp", action: "whatsapp", url: "" }
    ],

    /* --------------------------------------------------------------------
       ORDER DELIVERY
       Every order is (1) saved to your Google Sheet AND (2) emailed to the
       address configured inside the Apps Script (google-sheet/Code.gs →
       NOTIFY_EMAIL). Paste the Apps Script web-app URL below. If the chosen
       payment method is "WhatsApp", the order also opens a WhatsApp chat.
       -------------------------------------------------------------------- */
    logEndpoint: "https://script.google.com/macros/s/AKfycbztudtvafjfhDworDH1Bw8p9P5f4_rSL68gEK-LC1fSlwLkx3_af5MkD5SMi90DIhAv/exec",

    secureNote: "Aucune donnée de carte n'est saisie sur ce site. Après votre commande, nous vous envoyons les instructions de paiement sécurisé."
  },

  /* ----------------------------------------------------------------------
     6b. WELCOME POPUP
     Opens the order form on a chosen plan shortly after the page loads.
       enabled  – master switch, set to false to turn the popup off
       planId   – which plan the form opens on ("exclusive", "gold", ...)
       delayMs  – wait before it appears
       showOnce – "session" (once per browser session), "day", or "always"
       message  – line shown above the order summary (leave "" to hide it)
     ---------------------------------------------------------------------- */
  promo: {
    enabled: true,
    planId: "exclusive",
    delayMs: 7000,
    showOnce: "session",
    message: "Offre Exclusive — 24 mois + 3 mois offerts, notre meilleur tarif."
  },

  /* ----------------------------------------------------------------------
     7. TRUST LINE (hero)
     ---------------------------------------------------------------------- */
  trustPoints: ["Simple", "Fast", "Flexible", "Multi-Device"]
};
