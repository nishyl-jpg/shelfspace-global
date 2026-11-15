# Three Cape Town business launches: design

Date: 2026-11-15

## Intent

Give the owner three launch-ready businesses he can start working on the
ground immediately, in this order: decor, produce, alcohol. He is one person
with under R50,000 of his own capital, so every plan must start lean, earn
early, and tell investors honestly what their money buys.

| Business | Name | What it sells |
|---|---|---|
| Decor | Mooimaak | Home improvement styling, newborn baby rooms, event decor and management |
| Produce | Groengeld | Standing weekly fruit and veg orders for restaurants and households |
| Alcohol | Ship in a Bottle | Imported ready-to-drink cocktails (BuzzBallz-style), online, to public and businesses |

Positioning for all three: mid-market Cape Town (Southern and Northern
Suburbs families, neighbourhood restaurants, bars and event buyers).

## Goals

Per business, five deliverables:

1. **Website** that can go live: static, mobile-first, own visual identity.
2. **Business model**: customers, offer and price list, unit costs, start-up
   budget, 12-month forecast with stated assumptions, risks.
3. **Content playbook**: which platforms and why, account setup steps, a
   90-day calendar, and ready-to-post captions and scripts.
4. **Legal and ground-work plan**: every registration, licence and rule that
   applies, with authority, cost, lead time and order; then a week-by-week
   checklist of what the owner physically does.
5. **Investor proposal**: the ask, use of funds, returns, the profit split
   between owner and investors, and exit terms.

## Non-goals

- Card payment, user accounts or a backend. Orders go by WhatsApp and an
  order form until each company has a registered entity and bank account.
- Registering anything on the owner's behalf, or contacting brand owners.
- Publishing. Everything stays on the working branch until he says go.

## Anti-goals

- Invented numbers presented as fact. Every figure is either sourced or
  labelled as an assumption to verify on the ground.
- An alcohol site that sells before a licence exists. It launches in
  "licence pending, join the list" mode, with age gate, and switches to
  ordering only when the licence number is filled in.
- Legal text that reads as final advice. Each legal section names the points
  a lawyer or accountant must sign off before investor money is taken.
- Promising investors returns. Forecasts show a cautious, expected and
  strong case.

## Constraints

- Repo is a live static GitHub Pages site (ShelfSpace). New work must not
  touch existing pages.
- Owner's own capital is under R50,000 across all three.
- Liquor: Western Cape licence and import registrations take months; import
  rights to a named brand depend on the brand owner.

## Approaches considered

1. **Three static sites plus written packs in this repo (chosen).** Each
   business gets a folder with its site and a `pack/` of documents. Matches
   the existing setup, costs nothing to host, can move to its own domain
   later. Trade-off: no online payment at launch.
2. **Hosted shop platform (Shopify or similar).** Real checkout from day
   one, but monthly fees, needs a registered business and bank account
   first, and cannot be built or shown from here.
3. **One combined site for all three.** Less work, but three unrelated
   audiences, and investors in one business would be looking at the others.

Chosen: 1, because it launches now on zero hosting cost and each business
stays separable for its own investors.

## Structure

```
mooimaak/           index.html (site), pack/
groengeld/          index.html (site, with standing-order builder), pack/
ship-in-a-bottle/   index.html (site, age gate, licence-pending mode), pack/
launch/index.html   private hub linking all sites and packs (noindex)
```

Each `pack/` holds four pages: `business-model.html`, `content-playbook.html`,
`legal-and-groundwork.html`, `investor-proposal.html`. Pack pages carry
`noindex` and are not linked from the public sites.

### Sites

- **Mooimaak**: three service lines with packages and from-prices, gallery
  placeholders the owner replaces with real work, quote request that opens a
  pre-filled WhatsApp message.
- **Groengeld**: choose household box or restaurant list, pick items and
  delivery days, see an estimated weekly total, send the standing order by
  WhatsApp. Prices come from one editable list at the top of the file.
- **Ship in a Bottle**: age gate, range, trade enquiry for bars and events,
  waiting list while the licence is pending; a single setting switches on
  ordering.

Phone number, email and prices sit in one clearly marked block per site.

### Investor terms (my proposal, for his lawyer to finalise)

Because his cash is small and his work is the main input, each business is
its own company. Investors get a minority stake plus first claim on
distributions until their money is back; after that profit splits by
shareholding. Exact percentages are set per business from its forecast, and
he keeps control (over 50%) of each.

### Calls I made

- "Ship in a bottle" is taken as the alcohol store's name.
- Research is done by web search during the build; anything not confirmed is
  marked "verify".
- Stock or placeholder imagery only; no generated photos passed off as
  the owner's own work.

## Left to the builder

Visual identity per brand, exact package pricing, forecast assumptions,
calendar content, and page layout.
