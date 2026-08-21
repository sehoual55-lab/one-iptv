# Deploying ONE IPTV to GitHub + Vercel

This is a plain static site, so hosting it on Vercel is free and takes a few
minutes. You push the files to a GitHub repository once, connect it to Vercel,
and from then on every change you push goes live automatically.

---

## What's already set up for you

| File | What it does on Vercel |
|------|------------------------|
| `vercel.json` | Clean directory URLs (`/pricing/`), security headers, 1-year caching for `/assets/*` |
| `.gitignore` | Keeps caches, previews and editor junk out of the repo |
| `.vercelignore` | Stops the `tools/` and `google-sheet/` helper folders from being served |
| `404.html` | Vercel automatically serves it for unknown URLs |

You do **not** need a build step, a framework, or any settings — Vercel serves
the HTML exactly as it is.

---

## Option A — GitHub website + Vercel (no command line)

**1. Create the repository on GitHub**

- Go to <https://github.com/new>.
- Name it e.g. `one-iptv` and click **Create repository**.
- On the new repo page click **uploading an existing file**.
- Drag in **everything inside this folder** (index.html, the `assets/`,
  `pricing/`, `blog/` … folders, `vercel.json`, etc.). You can drag the whole
  set at once.
- Click **Commit changes**.

**2. Connect Vercel**

- Go to <https://vercel.com> and sign in with your GitHub account (free).
- Click **Add New… → Project**.
- Pick your `one-iptv` repository and click **Import**.
- Framework preset: **Other** (it auto-detects a static site). Leave every
  build/output field empty.
- Click **Deploy**.

About a minute later you get a live URL like `one-iptv.vercel.app`.

**3. Point your domain at it (one-iptv.online)**

- In the project: **Settings → Domains → Add** → type `one-iptv.online`.
- Vercel shows you the DNS records to set. At your domain registrar, add them
  (usually an `A` record to `76.76.21.21` for the root, and a `CNAME` from
  `www` to `cname.vercel-dns.com`). Vercel verifies and issues HTTPS
  automatically.

Done. To change anything later, edit the file on GitHub (or re-upload it) and
Vercel redeploys within seconds.

---

## Option B — Command line (if you prefer git)

```bash
# from inside this folder
git init
git add .
git commit -m "ONE IPTV website"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/one-iptv.git
git push -u origin main
```

Then either import the repo on vercel.com as in Option A, **or** deploy directly:

```bash
npm i -g vercel
vercel        # first run links the project
vercel --prod # publishes to production
```

---

## Making changes after launch

- **Prices, plans, WhatsApp number, Google-Sheet URL** → edit
  `assets/js/config.js`, commit/push. Live in seconds.
- **Page text** → edit the relevant `index.html` (or regenerate with the
  `tools/` scripts if you're changing shared pieces), commit/push.

That's the whole workflow — no rebuild, no server to manage.
