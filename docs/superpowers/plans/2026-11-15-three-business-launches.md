# Three Business Launches Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a launch-ready website and a four-document launch pack for each of Mooimaak (decor), Groengeld (produce) and Ship in a Bottle (imported ready-to-drink alcohol).

**Architecture:** Static HTML, one folder per business, no build step, matching the existing GitHub Pages repo. Each site is a single self-contained `index.html` with one `CONFIG` block for contact details and prices. Pack pages share one stylesheet.

**Tech Stack:** HTML, CSS, vanilla JavaScript. Playwright (pre-installed) for checks.

**Spec:** `docs/superpowers/specs/2026-11-15-three-business-launches-design.md`

## Global Constraints

- Do not modify `index.html`, `mall.html`, `waitlist.html`, `404.html`, `CNAME` or any other existing file.
- Spelling is exactly: Mooimaak, Groengeld, Ship in a Bottle.
- Every pack page and `launch/index.html` carries `<meta name="robots" content="noindex">`. Public sites never link to `pack/` or `launch/`.
- Every figure is sourced (link) or tagged `verify` in the text.
- No card payment. Orders and quotes open a pre-filled `https://wa.me/<number>?text=` link.
- Each site has one `const CONFIG = {...}` block holding `whatsapp`, `email` and prices.
- Ship in a Bottle: `CONFIG.licenceNumber` empty means waiting-list mode and no order buttons; non-empty shows ordering and prints the number in the footer.
- Forecasts show cautious, expected and strong cases. No promised returns.
- Legal and investor pages list the points needing a lawyer's or accountant's sign-off.

## Review Focus

1. Phone width (360px): no horizontal scroll on any site or pack page.
2. Groengeld order with nothing selected: send button disabled, not an empty WhatsApp message.
3. Ship in a Bottle visitor who answers "under 18": site content stays hidden; no way round by scrolling.
4. Ship in a Bottle with empty `licenceNumber`: no order link anywhere in the page.
5. WhatsApp messages with `&`, quotes or line breaks in item names: text is URL-encoded.

## File Structure

```
launch/pack.css                     shared styles for all pack pages
launch/index.html                   private hub linking sites and packs
tests/check.js                      Playwright checks for everything below
mooimaak/index.html                 site
mooimaak/pack/{business-model,content-playbook,legal-and-groundwork,investor-proposal}.html
groengeld/index.html                site with standing-order builder
groengeld/pack/(same four)
ship-in-a-bottle/index.html         site with age gate and licence mode
ship-in-a-bottle/pack/(same four)
```

---

### Task 1: Checks, shared pack styles and hub

**Files:** Create `tests/check.js`, `launch/pack.css`, `launch/index.html`

**Interfaces:**
- Produces: `node tests/check.js [mooimaak|groengeld|ship-in-a-bottle|all]`, exit code 0 on pass. Serves the repo root on a local port itself.
- Produces: `launch/pack.css` classes `.pack`, `.verify` (inline tag), `.signoff` (lawyer/accountant box), `table`, `.cases` (three-case forecast table), `.checklist`.

- [ ] Step 1: Write `tests/check.js`. For each business it asserts: site and four pack pages return 200; no horizontal overflow at 360px (`scrollWidth <= clientWidth`); pack pages have the noindex meta; site HTML contains no `pack/` or `launch/` link; every `wa.me` href has an encoded `text=` parameter.
- [ ] Step 2: Run `node tests/check.js all`. Expected: FAIL (pages missing).
- [ ] Step 3: Write `launch/pack.css` and `launch/index.html` (links to three sites and twelve pack pages).
- [ ] Step 4: Commit.

### Task 2: Mooimaak site

**Files:** Create `mooimaak/index.html`

- [ ] Step 1: Add to `tests/check.js`: choosing a service and package then pressing the quote button yields a `wa.me` href whose decoded text contains the service and package names.
- [ ] Step 2: Build the site: hero, three service lines (Home, Nursery, Events) each with three packages and from-prices from `CONFIG`, how-it-works, gallery placeholders, quote form, FAQ, footer.
- [ ] Step 3: Run `node tests/check.js mooimaak` for the site assertions. Expected: site checks pass.
- [ ] Step 4: Commit.

### Task 3: Mooimaak pack

**Files:** Create the four pages in `mooimaak/pack/`

- [ ] Step 1: Research by web search: Cape Town decor and event pricing, company registration, tax, consumer and privacy law, public liability insurance, event permits. Record sources.
- [ ] Step 2: Write `business-model.html` (customers, packages and prices, unit costs, start-up budget under the owner's capital, 12-month three-case forecast, risks).
- [ ] Step 3: Write `content-playbook.html` (platform choice, account setup steps, 90-day calendar, at least 30 ready-to-post captions or scripts).
- [ ] Step 4: Write `legal-and-groundwork.html` (requirements table: item, authority, cost, lead time, order; sign-off box; week-by-week ground-work checklist for 12 weeks).
- [ ] Step 5: Write `investor-proposal.html` (ask, use of funds, three-case returns, profit split, control and exit terms, sign-off box).
- [ ] Step 6: Run `node tests/check.js mooimaak`. Expected: PASS.
- [ ] Step 7: Commit.

### Task 4: Groengeld site

**Files:** Create `groengeld/index.html`

**Interfaces:**
- Produces: `weeklyTotal(items, daysPerWeek) -> number` exposed on `window` (sum of price times quantity, times delivery days, plus `CONFIG.deliveryFee` per day when below `CONFIG.freeDeliveryOver`).

- [ ] Step 1: Add checks: `weeklyTotal([{price:25,qty:2},{price:40,qty:1}], 2)` equals `180 + 2*CONFIG.deliveryFee` when under the free threshold; send button is disabled with nothing selected; with items selected the decoded WhatsApp text lists each item, quantity, delivery days and total.
- [ ] Step 2: Build the site: hero, household vs restaurant switch, item list from `CONFIG.items`, quantity steppers, delivery-day picker, live weekly total, send by WhatsApp, how it works, areas served, FAQ.
- [ ] Step 3: Run `node tests/check.js groengeld` site assertions. Expected: pass.
- [ ] Step 4: Commit.

### Task 5: Groengeld pack

Same six content steps as Task 3, with research on: Cape Town Market (Epping) buying, produce price levels and mark-ups, food premises certificate of acceptability, vehicle and cold-chain needs, restaurant credit terms. Run `node tests/check.js groengeld`. Commit.

### Task 6: Ship in a Bottle site

**Files:** Create `ship-in-a-bottle/index.html`

- [ ] Step 1: Add checks: before answering the age gate, main content is not visible; answering "No" keeps it hidden and shows a refusal message; answering "Yes" reveals it; with `licenceNumber` empty the page contains no element with `data-order` and shows the waiting-list form; setting it via `?licence=TEST123` (test-only override) shows order buttons and the number in the footer.
- [ ] Step 2: Build the site: age gate, hero, range from `CONFIG.products`, public and trade sections, waiting list or ordering by licence mode, responsible-drinking and no-under-18 notice, delivery rules, FAQ, footer.
- [ ] Step 3: Run `node tests/check.js ship-in-a-bottle` site assertions. Expected: pass.
- [ ] Step 4: Commit.

### Task 7: Ship in a Bottle pack

Same six content steps as Task 3, with research on: Western Cape liquor licence types, process, cost and timing; liquor import requirements (customs registration, import certificate, duties, labelling); online sale and delivery rules; alcohol advertising rules on social platforms; brand-owner import rights. The ground-work plan starts with the licence application and brand-owner approach. Run `node tests/check.js ship-in-a-bottle`. Commit.

### Task 8: Whole-build verification

- [ ] Step 1: Run `node tests/check.js all`. Expected: PASS.
- [ ] Step 2: Screenshot each site at phone and desktop width and inspect.
- [ ] Step 3: `git diff main --stat` shows no existing file changed.
- [ ] Step 4: Commit and push.
