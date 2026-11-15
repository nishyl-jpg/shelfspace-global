// Checks for the three business sites and their launch packs.
// Usage: node tests/check.js [mooimaak|groengeld|ship-in-a-bottle|all]
const http = require('http');
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const PACK = ['business-model', 'content-playbook', 'legal-and-groundwork', 'investor-proposal'];
const ALL = ['mooimaak', 'groengeld', 'ship-in-a-bottle'];
const which = process.argv[2] || 'all';
const targets = which === 'all' ? ALL : [which];
const TYPES = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml', '.png': 'image/png' };

const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split('?')[0]);
  if (p.endsWith('/')) p += 'index.html';
  const file = path.join(ROOT, p);
  if (!file.startsWith(ROOT) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
    res.writeHead(404); return res.end('not found');
  }
  res.writeHead(200, { 'Content-Type': TYPES[path.extname(file)] || 'application/octet-stream' });
  fs.createReadStream(file).pipe(res);
});

let failed = 0;
function ok(cond, label) {
  if (cond) console.log('  pass  ' + label);
  else { failed++; console.log('  FAIL  ' + label); }
}
const waText = (href) => decodeURIComponent((href.split('text=')[1] || '').replace(/\+/g, ' '));
const waEncoded = (href) => /^https:\/\/wa\.me\/\d+\?text=[^\s"'&<>]+$/.test(href);

async function common(page, base, biz) {
  const urls = [`/${biz}/`, ...PACK.map((p) => `/${biz}/pack/${p}.html`)];
  for (const u of urls) {
    const res = await page.goto(base + u);
    ok(res.status() === 200, `${u} loads`);
    if (res.status() !== 200) continue;
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
    ok(!overflow, `${u} has no sideways scroll at 360px`);
    const html = await page.content();
    if (u.includes('/pack/')) {
      ok(/<meta[^>]+name="robots"[^>]+noindex/.test(html), `${u} is noindex`);
      ok(html.length > 6000, `${u} has real content`);
    } else {
      ok(!/href="[^"]*(pack\/|launch\/)/.test(html), `${u} does not link to private pages`);
    }
  }
}

async function mooimaak(page, base) {
  await page.goto(base + '/mooimaak/');
  await page.selectOption('#q-service', { index: 2 });
  await page.selectOption('#q-package', { index: 1 });
  await page.fill('#q-name', 'Tom & "Ann"');
  const service = await page.$eval('#q-service', (s) => s.selectedOptions[0].textContent.trim());
  const pack = await page.$eval('#q-package', (s) => s.selectedOptions[0].textContent.trim());
  const href = await page.$eval('#q-send', (a) => a.href);
  ok(waEncoded(href), 'quote link is an encoded WhatsApp link');
  const text = waText(href);
  ok(text.includes(service) && text.includes(pack.split(' (')[0]), 'quote message names the service and package');
  ok(text.includes('Tom & "Ann"'), 'quote message keeps special characters');
}

async function groengeld(page, base) {
  await page.goto(base + '/groengeld/');
  const fee = await page.evaluate(() => CONFIG.deliveryFee);
  const total = await page.evaluate(() => weeklyTotal([{ price: 25, qty: 2 }, { price: 40, qty: 1 }], 2));
  ok(total === 180 + 2 * fee, `weeklyTotal adds delivery fee below the free threshold (${total})`);
  const big = await page.evaluate(() => weeklyTotal([{ price: CONFIG.freeDeliveryOver, qty: 1 }], 1));
  const over = await page.evaluate(() => CONFIG.freeDeliveryOver);
  ok(big === over, 'weeklyTotal drops the fee at the free threshold');
  ok(await page.$eval('#send', (a) => a.getAttribute('aria-disabled') === 'true' && !a.getAttribute('href')), 'send is disabled with nothing selected');
  const plus = await page.$$('[data-plus]');
  await plus[plus.length - 1].click();
  ok(await page.$eval('#send', (a) => a.getAttribute('aria-disabled') === 'true'), 'send stays disabled below the minimum order');
  ok(/Minimum order/.test(await page.textContent('#hint')), 'hint explains the minimum order');
  await (await page.$$('[data-minus]')).pop().click();
  await plus[0].click(); await plus[0].click(); await plus[1].click();
  const names = await page.$$eval('[data-item-name]', (els) => els.slice(0, 2).map((e) => e.textContent.trim()));
  const href = await page.$eval('#send', (a) => a.href);
  ok(waEncoded(href), 'order link is an encoded WhatsApp link');
  const text = waText(href);
  ok(names.every((n) => text.includes(n)), 'order message lists the chosen items');
  ok(/2 x/.test(text) && /Total/i.test(text) && /Deliver/i.test(text), 'order message has quantities, delivery days and total');
}

async function groengeldPages(page, base) {
  for (const f of ['selection', 'combos', 'rewards']) {
    const res = await page.goto(base + '/groengeld/' + f + '.html');
    ok(res.status() === 200, f + '.html loads');
    ok(!(await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth)), f + '.html has no sideways scroll at 360px');
    const html = await page.content();
    ok(!/href="[^"]*(pack\/|launch\/)/.test(html), f + '.html does not link to private pages');
    const hrefs = await page.$$eval('[data-wa]', (as) => as.map((a) => a.href));
    ok(hrefs.length > 0 && hrefs.every((h) => waEncoded(h)), f + '.html WhatsApp links are encoded');
  }
}

async function ship(page, base) {
  await page.goto(base + '/ship-in-a-bottle/');
  ok(!(await page.isVisible('#site')), 'content hidden before the age gate is answered');
  await page.click('#age-no');
  ok(!(await page.isVisible('#site')) && (await page.isVisible('#age-refused')), 'under 18 stays locked out');
  await page.goto(base + '/ship-in-a-bottle/');
  await page.click('#age-yes');
  ok(await page.isVisible('#site'), 'over 18 sees the site');
  ok((await page.$$('[data-order]')).length === 0, 'no order buttons without a licence number');
  ok(await page.isVisible('#waitlist'), 'waiting list shown without a licence number');
  await page.goto(base + '/ship-in-a-bottle/?licence=TEST123');
  await page.click('#age-yes');
  ok((await page.$$('[data-order]')).length > 0, 'order buttons appear with a licence number');
  ok((await page.textContent('footer')).includes('TEST123'), 'licence number printed in the footer');
  const hrefs = await page.$$eval('a[href*="wa.me"]', (as) => as.map((a) => a.href));
  ok(hrefs.length > 0 && hrefs.every((h) => /^https:\/\/wa\.me\/\d+\?text=[^\s&]+$/.test(h)), 'WhatsApp links are encoded');
}

(async () => {
  await new Promise((r) => server.listen(0, r));
  const base = 'http://127.0.0.1:' + server.address().port;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 360, height: 740 } });
  const specific = { mooimaak, groengeld, 'ship-in-a-bottle': ship };
  for (const biz of targets) {
    console.log('\n' + biz);
    await common(page, base, biz);
    if (biz === 'groengeld') await groengeldPages(page, base);
    try { await specific[biz](page, base); } catch (e) { failed++; console.log('  FAIL  ' + e.message.split('\n')[0]); }
  }
  if (which === 'all') {
    const res = await page.goto(base + '/launch/');
    ok(res.status() === 200, '/launch/ hub loads');
  }
  await browser.close(); server.close();
  console.log(failed ? `\n${failed} check(s) failed` : '\nAll checks passed');
  process.exit(failed ? 1 : 0);
})();
