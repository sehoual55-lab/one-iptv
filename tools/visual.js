const { chromium } = require('playwright');
const fs = require('fs');

const BASE = 'http://127.0.0.1:8099';
const OUT = '/root/shots';
fs.mkdirSync(OUT, { recursive: true });

const PAGES = [
  ['home', '/'],
  ['features', '/features/'],
  ['channels', '/channels/'],
  ['pricing', '/pricing/'],
  ['devices', '/devices/'],
  ['faq', '/faq/'],
  ['blog', '/blog/'],
  ['article', '/blog/one-iptv-complete-guide-for-beginners/'],
  ['contact', '/contact/'],
  ['404', '/404.html'],
];

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const problems = [];

  // ---------- desktop screenshots ----------
  const desktop = await browser.newContext({ viewport: { width: 1440, height: 950 }, deviceScaleFactor: 1 });
  for (const [name, url] of PAGES) {
    const page = await desktop.newPage();
    const errs = [];
    page.on('console', m => { if (m.type() === 'error' && !/fonts\.(googleapis|gstatic)/.test(m.text()) && !/ERR_TUNNEL/.test(m.text())) errs.push(m.text()); });
    page.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
    page.on('response', r => { if (r.status() >= 400 && !/fonts\./.test(r.url())) errs.push(`HTTP ${r.status()} ${r.url()}`); });
    await page.goto(BASE + url, { waitUntil: 'networkidle' });
    await page.addStyleTag({ content: 'html{scroll-behavior:auto!important}' });
    await page.evaluate(() => { window.scrollTo(0, document.body.scrollHeight); });
    await page.waitForTimeout(500);
    await page.evaluate(() => { window.scrollTo(0, 0); document.querySelectorAll('.reveal').forEach(e => e.classList.add('is-visible')); });
    await page.waitForTimeout(500);
    await page.screenshot({ path: `${OUT}/d-${name}.png`, fullPage: name === 'home' ? false : false });
    if (errs.length) problems.push(`[${name}] ` + errs.join(' | '));
    await page.close();
  }

  // ---------- full-page home ----------
  {
    const page = await desktop.newPage();
    await page.goto(BASE + '/', { waitUntil: 'networkidle' });
    await page.addStyleTag({ content: 'html{scroll-behavior:auto!important}' });
    await page.evaluate(async () => {
      const h = document.body.scrollHeight;
      for (let y = 0; y < h; y += 500) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 90)); }
      window.scrollTo(0, 0);
      document.querySelectorAll('.reveal').forEach(e => e.classList.add('is-visible'));
    });
    await page.waitForTimeout(900);
    await page.screenshot({ path: `${OUT}/d-home-full.png`, fullPage: true });
    await page.close();
  }

  // ---------- interaction tests ----------
  {
    const page = await desktop.newPage();
    const errs = [];
    page.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
    await page.goto(BASE + '/', { waitUntil: 'networkidle' });

    // pricing sync from config
    const price = await page.textContent('[data-plan="gold"] [data-plan-price]');
    if (!price || !/[$€]|XX/.test(price)) problems.push('pricing not synced from config: ' + price);

    // checkout modal
    await page.click('[data-plan="gold"] [data-open-checkout]');
    await page.waitForTimeout(500);
    const open = await page.isVisible('#checkout-modal.is-open');
    if (!open) problems.push('checkout modal did not open');
    const sumPlan = await page.textContent('[data-sum-plan]');
    if (sumPlan !== 'Gold') problems.push('summary plan wrong: ' + sumPlan);
    await page.screenshot({ path: `${OUT}/d-modal.png` });

    // switch plan updates summary
    await page.click('.plan-opt:has(input[value="exclusive"])');
    await page.waitForTimeout(200);
    const sum2 = await page.textContent('[data-sum-plan]');
    if (sum2 !== 'Exclusive') problems.push('plan switch did not update summary: ' + sum2);

    // validation blocks empty submit
    await page.click('[data-checkout-submit]');
    await page.waitForTimeout(300);
    const errText = await page.textContent('#co-name ~ .field-error');
    if (!errText || !errText.trim()) problems.push('validation did not fire on empty submit');
    await page.screenshot({ path: `${OUT}/d-modal-validation.png` });

    // fill + submit -> success view
    await page.fill('#co-name', 'Test Customer');
    await page.fill('#co-phone', '+447700900000');
    await page.evaluate(() => { window.open = () => null; });
    await page.click('[data-checkout-submit]');
    await page.waitForTimeout(500);
    const successVisible = await page.isVisible('[data-checkout-success]');
    if (!successVisible) problems.push('success view did not appear after submit');
    await page.screenshot({ path: `${OUT}/d-modal-success.png` });

    // esc closes
    await page.keyboard.press('Escape');
    await page.waitForTimeout(500);
    if (await page.isVisible('#checkout-modal.is-open')) problems.push('Escape did not close modal');

    // FAQ accordion
    await page.click('.faq-q');
    await page.waitForTimeout(600);
    const h = await page.evaluate(() => document.querySelector('.faq-a').getBoundingClientRect().height);
    if (h < 30) problems.push('FAQ accordion did not expand, height=' + h);
    await page.locator('#faq').scrollIntoViewIfNeeded();
    await page.waitForTimeout(400);
    await page.screenshot({ path: `${OUT}/d-faq-open.png` });

    // film marquee present, full-bleed, clipped (not expanded), and auto-scrolling
    await page.locator('#films').scrollIntoViewIfNeeded();
    await page.waitForTimeout(500);
    const filmRows = await page.locator('#films .film-track').count();
    if (filmRows < 1) problems.push('film marquee missing on home');
    const geo = await page.evaluate(() => {
      const t = document.querySelector('#films .carousel');
      const s = document.querySelector('#films');
      if (!t) return { ok: false };
      return {
        clipped: t.scrollWidth > t.clientWidth + 50 && t.clientWidth < 1600,
        fullBleed: Math.round(s.getBoundingClientRect().width) >= window.innerWidth - 2,
        noText: !document.querySelector('#films .film__meta') ||
                getComputedStyle(document.querySelector('#films .film__meta')).display === 'none',
        sw: t.scrollWidth, cw: t.clientWidth
      };
    });
    if (!geo.clipped) problems.push('film marquee not clipped (sw=' + geo.sw + ' cw=' + geo.cw + ')');
    if (!geo.fullBleed) problems.push('film marquee not full-bleed');
    if (!geo.noText) problems.push('film marquee still shows text');
    // auto-scroll advances within ~2s
    const a0 = await page.evaluate(() => document.querySelector('#films .carousel').scrollLeft);
    await page.waitForTimeout(2600);
    const a1 = await page.evaluate(() => document.querySelector('#films .carousel').scrollLeft);
    if (a1 <= a0) problems.push('film marquee did not auto-scroll (' + a0 + '->' + a1 + ')');

    // sticky header
    await page.evaluate(() => window.scrollTo(0, 800));
    await page.waitForTimeout(400);
    const stuck = await page.evaluate(() => {
      const h = document.querySelector('.site-header');
      return h.classList.contains('is-stuck') && h.getBoundingClientRect().top === 0;
    });
    if (!stuck) problems.push('sticky header not sticking');

    if (errs.length) problems.push('home interactions: ' + errs.join(' | '));
    await page.close();
  }

  // ---------- mobile ----------
  const mobile = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
  for (const [name, url] of [['home', '/'], ['pricing', '/pricing/'], ['devices', '/devices/'], ['article', '/blog/one-iptv-complete-guide-for-beginners/']]) {
    const page = await mobile.newPage();
    await page.goto(BASE + url, { waitUntil: 'networkidle' });
    await page.waitForTimeout(500);
    await page.screenshot({ path: `${OUT}/m-${name}.png` });
    // horizontal overflow check
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    if (overflow > 2) problems.push(`mobile ${name}: horizontal overflow of ${overflow}px`);
    await page.close();
  }

  // mobile menu + modal
  {
    const page = await mobile.newPage();
    await page.goto(BASE + '/', { waitUntil: 'networkidle' });
    await page.click('.burger');
    await page.waitForTimeout(500);
    if (!(await page.isVisible('#mobile-nav.is-open'))) problems.push('mobile nav did not open');
    await page.screenshot({ path: `${OUT}/m-menu.png` });
    await page.click('.burger');
    await page.waitForTimeout(400);
    if (await page.isVisible('#mobile-nav.is-open')) problems.push('mobile nav did not close');

    await page.click('.hero-cta [data-open-checkout]');
    await page.waitForTimeout(500);
    await page.screenshot({ path: `${OUT}/m-modal.png` });
    if (!(await page.isVisible('#checkout-modal.is-open'))) problems.push('mobile modal did not open');
    await page.close();
  }

  // ---------- reduced-motion / no-JS sanity ----------
  {
    const nojs = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 1440, height: 950 } });
    const page = await nojs.newPage();
    await page.goto(BASE + '/pricing/', { waitUntil: 'load' });
    const txt = await page.textContent('body');
    if (!txt.includes('Bronze') || !txt.includes('Exclusive')) problems.push('no-JS: pricing content missing');
    await page.screenshot({ path: `${OUT}/d-nojs-pricing.png` });
    await page.close();
  }

  await browser.close();

  if (problems.length) {
    console.log('PROBLEMS:\n' + problems.map(p => '  ✗ ' + p).join('\n'));
    process.exit(1);
  }
  console.log('✓ All visual/interaction checks passed.');
})();
