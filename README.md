# ONE IPTV — one-iptv.online

A complete, dependency-free static website. No build step, no Node, no framework.
Upload the files and it runs.

---

## 1. What's in the box

```
/
├── index.html                  Home
├── features/                   /features/
├── channels/                   /channels/
├── pricing/                    /pricing/
├── devices/                    /devices/
├── faq/                        /faq/
├── blog/                       /blog/  + 7 full article pages
├── contact/                    /contact/
├── privacy/  terms/  refund-policy/
├── 404.html
├── sitemap.xml
├── robots.txt
├── site.webmanifest
├── .htaccess                   Apache config (clean URLs, caching, gzip)
├── _headers                    Netlify / Cloudflare Pages headers
└── assets/
    ├── css/styles.css          The whole design system, one file
    ├── js/config.js            ← EDIT THIS ONE (prices, phone, checkout)
    ├── js/main.js              Behaviour: nav, modal, FAQ, carousel
    └── img/                    SVG artwork (~90 KB total) + social images
```

The `tools/` folder contains the Python generator used to build the HTML. You do
**not** need it to run the site — it is included so pages can be regenerated
consistently if you want to change shared content later
(`python3 tools/build.py`, then `python3 tools/verify.py` to check).

---

## 2. Uploading

Drop everything except `tools/` into your web root and you're live. It works on
shared hosting (cPanel), Netlify, Vercel, Cloudflare Pages, GitHub Pages, or any
static host.

**One thing to check:** the site uses directory URLs (`/pricing/`, not
`/pricing.html`). Almost every host serves `index.html` from a folder
automatically. The included `.htaccess` handles Apache; `_headers` handles
Netlify and Cloudflare Pages.

---

## 3. Setting your prices  ← the main thing you'll want to change

Open **`assets/js/config.js`**. It's the single source of truth — every price on
every page reads from it.

There are **4 plans** — Bronze (12 mo, $39.99), Gold (15 mo +3 free, $49.99),
Platinum (15 mo +3 free, $59.99) and Exclusive (24 mo +3 free, $84.99). Each has
a `basePrice`, the price for **one connection**:

```js
plans: [
  {
    id: "gold",
    name: "Gold",
    months: 15,
    bonusMonths: 3,       // extra free months shown as "+3 months free"
    basePrice: 49.99,     // price for one connection (a NUMBER, not a string)
    ...
  },
```

Change `basePrice` on any plan, save, upload — the pricing cards, the connection
stepper maths, the checkout modal and the SEO data all update.

**Currency:** the site ships in **USD ($)** to match the reference. To switch to
euros, set `currency.symbol` to `"€"` and `currency.code` to `"EUR"` in the same
file (use `position: "after"` for `19.99 €`).

### The connection stepper (+ / −)

Each plan card has a +/− control for how many devices stream at once. The first
connection is full price; every extra one is discounted. You control this in one
place:

```js
connections: {
  min: 1, max: 5, default: 1,
  extraDiscount: 0.15     // each extra connection is 15% cheaper
},
```

The total is `basePrice × (1 + (1 − extraDiscount) × (connections − 1))`. With a
$40 base and 3 connections that's $40 × (1 + 0.85 × 2) = **$108.00**. The chosen
connection count follows the customer into the checkout order summary.

### Why prices are placeholders right now

While a plan's `basePrice` is `null`, the site deliberately:

- shows `$XX.XX` with a note explaining prices are being confirmed,
- shows "Prices are being finalised" in the checkout summary,
- and **publishes no Product/Offer structured data at all**.

The moment you put real numbers in, that structured data starts being emitted
automatically with the correct currency. This means Google is never given
invented prices, which is exactly what you want.

## 3b. The films & series showcase (TMDB)

The "Films & Series You'll Recognise" rows on the home and channels pages pull
live posters from **The Movie Database (TMDB)**. It's already wired to your key:

```js
tmdb: {
  enabled: true,
  apiKey: "eb88f8554c5c594b1b82a59672ee98f4",
  ...
}
```

- To turn it off, set `enabled: false` — the rows fall back to the built-in
  artwork automatically.
- To change what's shown, edit the `rows` array (any TMDB endpoint works, e.g.
  `/movie/popular`, `/tv/top_rated`, `/trending/all/day`).
- **If TMDB is ever unreachable**, each row quietly falls back to your own
  category artwork, so the section never looks broken.
- **Note:** a browser-side API key is visible in the page source — that's
  unavoidable for any client-side call. TMDB read keys are low-risk (read-only,
  free, rate-limited). You can rotate it any time at themoviedb.org → Settings →
  API. TMDB attribution is shown under the rows, as their terms require.

The posters are labelled as illustrative, with a clear note that ONE IPTV isn't
affiliated with the studios behind any title.

---

## 4. Changing the WhatsApp number

Contact across the whole site is **WhatsApp-only** — no phone dialler, no email.
Change one value in `config.js` and every WhatsApp button, link and order
handoff updates:

```js
contact: {
  whatsappNumber: "16615413954",   // no "+", international format
}
```

That single number drives the header chip, footer, contact page, the floating
button, every "Message us on WhatsApp" link, and where completed orders are sent.

---

## 5. Connecting a real payment provider

The checkout modal collects name, WhatsApp number and plan — **never card
details, never email**. That's deliberate: taking card numbers directly makes
you liable for PCI compliance. Three ways to finish the transaction, set by
`checkout.mode`:

### `"handoff"` (default — works right now)

The order summary opens in WhatsApp so you can confirm the order and invoice the
customer directly.

### `"redirect"` — Stripe, PayPal, Paddle, Lemon Squeezy…

```js
checkout: {
  mode: "redirect",
  paymentUrls: {
    "bronze":    "https://buy.stripe.com/xxxxxxxx",
    "gold":      "https://buy.stripe.com/yyyyyyyy",
    "platinum":  "https://buy.stripe.com/zzzzzzzz",
    "exclusive": "https://buy.stripe.com/wwwwwwww"
  }
}
```

Create one Payment Link per plan in your provider's dashboard, paste them in.
The customer fills the form, sees a confirmation, and is sent to the secure
hosted checkout. Card data never touches your site.

### `"endpoint"` — your own backend or a form service

```js
checkout: { mode: "endpoint", endpoint: "https://formspree.io/f/xxxxxx" }
```

The order is POSTed as JSON. Works with Formspree, Netlify Forms, Basin, or your
own API.

---

## 5b. Saving every order to your Google Sheet

Every order can be logged automatically to your **"One IPTV — Commandes"**
Google Sheet — on top of the WhatsApp hand-off, in any checkout mode. It fills
these columns: Date · Nom · Email · Téléphone · Formule · Prix · Connexions ·
Paiement · Statut.

Set it up once (about 5 minutes):

1. Open your sheet, then **Extensions → Apps Script**.
2. Delete the sample code, paste the whole of **`google-sheet/Code.gs`** (included
   in this package — your sheet ID is already filled in), and Save.
3. **Deploy → New deployment → Web app.** Execute as **Me**, access **Anyone**.
   Authorise, then copy the **Web app URL**.
4. In `assets/js/config.js`, paste that URL:

   ```js
   checkout: { logEndpoint: "https://script.google.com/macros/s/AKfy…/exec" }
   ```

5. Re-upload `config.js`. Done — place a test order and a new row appears in the
   sheet within a second or two.

Notes: the site is WhatsApp-only, so the **Email** column is left blank and the
**Téléphone** column holds the customer's WhatsApp number. New orders arrive with
Paiement = "En attente" and Statut = "Nouveau" — change those yourself as you
process each order. Logging never blocks the order: if the sheet is unreachable,
the WhatsApp hand-off still happens.

---

## 6. Editing content

Each page is plain, readable HTML — open it in any editor and change the text.

For shared pieces (header, footer, feature cards, FAQ answers, plan features),
edit the relevant file in `tools/` and re-run `python3 tools/build.py`. That
keeps all 19 pages consistent instead of you editing the footer nineteen times:

| To change… | Edit |
|---|---|
| Header, footer, legal disclaimer, checkout modal | `tools/shell.py` |
| Feature cards, devices, categories, FAQ, blog metadata | `tools/content.py` |
| Page copy for home / features / pricing / etc. | `tools/build.py` |
| Blog article text | `tools/posts_a.py`, `tools/posts_b.py` |

The contact form on `/contact/` is a front-end demo — point its `action` at your
form service or wire it to the same endpoint as the checkout to make it live.

---

## 7. SEO — what's already done

- Unique title + meta description on all 19 pages, canonical URLs throughout
- Open Graph + Twitter card metadata with a 1200×630 social image
- `sitemap.xml` (all pages, with dates) and `robots.txt`
- Structured data: Organization, WebSite, Service, BreadcrumbList, FAQPage,
  Blog, BlogPosting, ContactPage — and Product/Offer once real prices are set
- Semantic HTML, one `<h1>` per page, descriptive `alt` text, skip link
- Keyword coverage across `one iptv`, `smart one iptv`, `iptv one month`,
  `one iptv uk`, `smart one iptv app download`, `iptv app`, `ip smart iptv`,
  `iptv app for tv`, `iptv tv smart` — written into natural sentences, not
  stuffed
- 7 full-length articles (roughly 1,000–1,400 words each) targeting the
  keyword cluster, cross-linked to each other and to the commercial pages

### After you go live

1. Add the site to Google Search Console and submit `sitemap.xml`.
2. Test a few URLs in the Rich Results Test — the FAQ pages should show FAQ
   rich results as eligible.
3. Set your real prices so Product/Offer data starts being published.
4. If you have social profiles, add them to the `sameAs` array in the
   Organization schema (`tools/build.py`, `ORG_SCHEMA`) and rebuild.

---

## 8. Legal notes worth keeping

The site was deliberately written to avoid claims that would be hard to defend:

- No channel counts, uptime guarantees, or "unlimited" claims anywhere.
- No third-party broadcaster logos, and no implied affiliation with any network,
  device manufacturer, or similarly-named IPTV player app — stated explicitly in
  the footer, the FAQ, and the terms.
- Neutral wording ("available content", "compatible services") throughout.
- Customer responsibility for lawful use is stated plainly rather than buried.
- No card details collected anywhere on the site.

If you change the copy, keeping these intact is worth the effort — they're the
difference between a site that reads as a real business and one that reads as a
liability. And if you later obtain rights or licences for specific content, that
copy can be updated to match what you're actually authorised to offer.

---

## 9. Browser support

Modern Chrome, Edge, Firefox and Safari (last ~2 years). The site degrades
gracefully: with JavaScript disabled, every page still renders fully with all
content and working navigation — only the modal and accordion animations are
lost.
