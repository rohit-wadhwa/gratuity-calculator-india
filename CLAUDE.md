# CLAUDE.md — Gratuity Calculator (India)

**Read this fully before acting on any task in this repo.**

## What this project is

A single-page, static gratuity calculator for India under the **Payment of Gratuity Act, 1972**. Vanilla HTML + CSS + JS in one file. **No framework, no build step, no backend, no package.json.** All computation runs client-side in the browser. Public tool, shared with colleagues and (eventually) ranked on Google.

## Live deployment

- **URL:** https://gratuity-calculator-india.vercel.app/
- **Vercel account:** Rohit Wadhwa's **personal Hobby** account (NOT the `isbcs-projects` team)
- **Project name:** `gratuity-calculator-india`
- **Deploy command:** `vercel --prod` from this folder (`.vercel/` already linked)
- **Deploy protection:** Standard Protection **Disabled** — must stay disabled so the URL is public

## File inventory

| File | Purpose | Editable? |
|------|---------|-----------|
| `index.html` | Entire app — markup, styles, logic, SEO meta, JSON-LD, analytics tags. | ✅ Primary edit target |
| `vercel.json` | Security headers (CSP, HSTS, X-Frame-Options, Referrer-Policy, Permissions-Policy), `cleanUrls`. | ✅ Only when adding new external resources |
| `robots.txt` | Crawler rules + sitemap pointer. | Rarely |
| `sitemap.xml` | Single-URL sitemap for Google indexing. | Update `<lastmod>` on major changes |
| `site.webmanifest` | PWA / mobile home-screen metadata. | Rarely |
| `og-image.png` | 1200×630 social share image. | Regenerate via `generate-og-image.py` if design palette changes |
| `generate-og-image.py` | Python script (Pillow) that regenerates the OG image. | If palette / typography changes materially |
| `README.md`, `LICENSE`, `CONTRIBUTING.md`, `SUPPORT.md` | Repo housekeeping. | Standard |

Static site. Vercel auto-detects: no framework, no build command, output = project root.

---

## The rules (non-negotiable)

### 🔒 Privacy — this is a PUBLIC tool

- **Zero personal data ever.** No real salary figures, names, employer, bank details, PAN, PF numbers, or locations in any file. The only example value permitted is the neutral `50,000` placeholder in the Basic + DA input.
- **Client-side only.** All math happens in the browser. Never add a backend, never POST form data, never add trackers that transmit user input.
- **Analytics allowed:** Vercel Web Analytics + Speed Insights only. Both are cookie-less and do NOT read form field values — only page views and referrers. Do not add Google Analytics, Meta Pixel, or any other third-party tracker.

### 🛡️ CSP — keep it strict

The current CSP whitelists exactly what's needed and nothing more:
- Google Fonts (`fonts.googleapis.com`, `fonts.gstatic.com`)
- Vercel Analytics (`vitals.vercel-insights.com`, `vercel.live`)
- Self only for everything else

**When adding any external resource** (widget, image, script, iframe), you must explicitly whitelist its exact host in `vercel.json` CSP. **Never** use `*` wildcards for `script-src`, `default-src`, or `frame-src`.

**Never re-add third-party widgets with iframes** (BuyMeACoffee widget, Intercom, Drift, etc.). We tried the BMC floating widget — it kept fighting the CSP and rendered a broken iframe. The rule now is: **any external service = plain styled `<a>` link, opens in new tab**. Zero third-party JS, zero iframe complexity, faster page load.

### 📐 Design conventions

- **Single-file architecture is intentional.** Do not split into separate CSS/JS files. Drag-and-drop deploy must stay trivial.
- **Gratuity math (do not change without a legal source):**
  - Covered employers: `(Basic + DA) × 15 × completed_years ÷ 26`
  - Uncovered: `÷ 30` instead
  - Tax-free cap: `₹20,00,000` under Section 10(10) of the Income-Tax Act
  - Partial year >6 months rounds up; ≤6 months drops
- **Mobile-first responsive:**
  - Tablet breakpoint: 760px (stacks to single column)
  - Phone breakpoint: 440px
  - Touch targets ≥44px, inputs ≥16px font size (prevents iOS auto-zoom)
- **Indian number formatting** (lakh/crore comma grouping) is custom — preserve it.

---

## Current design (as of Aug 22, 2026)

Ledger direction — a bank passbook / salary slip, not a designed web page.

**A warning, from experience.** The first redesign moved off the cream+green+Fraunces cluster and landed on parchment `#F6F0E0` + vermilion `#B23A2F` — which is *also* an AI-default pairing (cream + terracotta), the exact one this file warns about below. Real users called it out as looking AI-generated. If a palette proposal is warm cream, beige, or parchment paired with a rust/terracotta/vermilion accent, reject it and pick a different ground.

**Palette:**
- Ground: `#ECEFF3` (cool ledger grey-blue)
- Card: `#FFFFFF` (input panel)
- Panel: `#F4F6F9` (result panel)
- Ink: `#0F1A2F` (legal navy)
- Accent: `#1B5E48` (deep ledger green)
- Negative: `#9B2C22` (oxblood — "not yet eligible" and date errors ONLY)
- Rule: `#1E2B45` · Hairline: `#C9D2DC`
- Gold (partial-tax highlight): `#6B4F0F`
- Secondary ink: `#4A5563` · Muted ink: `#6B7683`

Accent green means "this is a live figure". Oxblood means "this does not qualify". Never let the two swap — a green "not eligible" badge reads as approval. There is no page texture or noise overlay; the cream needed warmth, the ledger ground does not.

All foreground/background pairs clear WCAG AA (4.5:1); most clear AAA. Re-run the check before changing any token:

```bash
python3 - <<'EOF'
def lum(h):
    h=h.lstrip('#'); c=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    c=[x/12.92 if x<=0.03928 else ((x+0.055)/1.055)**2.4 for x in c]
    return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2]
def cr(a,b):
    l1,l2=sorted([lum(a),lum(b)],reverse=True); return round((l1+0.05)/(l2+0.05),2)
for n,a,b in [('ink-3/panel','#4A5563','#F4F6F9'),('gold/gold-soft','#6B4F0F','#F2E7C8'),
              ('accent/card','#1B5E48','#FFFFFF'),('negative/card','#9B2C22','#FFFFFF'),
              ('ink-4/card','#6B7683','#FFFFFF')]:
    print(n, cr(a,b))
EOF
```
`--ink-4` is scoped to placeholder text and the decorative `•` separators in the header citation — never to text that carries meaning. Keep it that way.

**Typography:**
- Display: **Playfair Display** (transitional serif, law-journal feel)
- Body: **IBM Plex Sans** (humanist, by Indian type designer)
- Numeric: **IBM Plex Mono** (amount, breakdown values)

**Signature elements:**
- Header cites the actual Act: `§ PAYMENT OF GRATUITY ACT, 1972 • SEC. 4 • REPUBLIC OF INDIA`
- Result panel styled as a "certificate" — double top rule, `Estimated payout / § 4(2)` label
- Rupee marks (₹) as the ornament before the header citation and section headings, matching the favicon. **Do not use `§`** — it is US/German legal convention; Indian Acts and judgments write "Section 4" or "Sec. 4". The payout reference reads `Sec. 4(2)`.
- The ornament is set in IBM Plex Sans, not Playfair, so `₹` (U+20B9) is certain to render.
- Underline-only inputs for the salary field; **boxed `DD / MM / YYYY` inputs for dates** (feels like filling a form)
- BMC button labeled **"Buy me a chai"** (India, not SF)
- Amount words in cheque-writing register: *"Rupees eleven lakh sixty-three thousand only"*
- Favicon is the rupee glyph `₹` on navy — **not** `§`. The section mark tested worse; people scan for the currency symbol.

## Versioning

The live version shows in the footer (`v2.0.0 · 22 Aug 2026`) so you can tell at a glance what is deployed. This follows the same convention as the other apps in `~/mini_project` — a constant at the top of the script, rendered into an element:

```js
var APP_VERSION='2.0.0';   // bump on each deploy to identify the running version
var BUILD_DATE='2026-08-22';
```

`APP_VERSION` is the single source of truth and is also exposed as `window.APP_VERSION`. Never hard-code the version into the footer text — it will drift.

**Bump on every deploy that changes what a user sees.** Patch for copy or colour tweaks, minor for a new field or section, major for a redesign or a change to how input works. Update `BUILD_DATE` at the same time.

Check what is actually live:

```bash
curl -s https://gratuity-calculator-india.vercel.app | grep -oE "APP_VERSION='[^']*'|BUILD_DATE='[^']*'"
```

Version history:
- `2.0.1` — `§` replaced with `₹` ornament; payout reference reads `Sec. 4(2)`
- `2.0.0` — ledger palette, typed `DD / MM / YYYY` date fields, accessibility pass
- `1.0.0` — initial parchment build (superseded; its cream + vermilion palette read as AI-generated)

**UI rules that came out of the design audit:**

- **Every interactive control has a `:focus-visible` ring** (`2px solid var(--accent)`, 3px offset) — inputs, segmented buttons, the share button, and FAQ summaries. The underline inputs previously used `outline:none` with only a border-colour change; that state change measures 2.38:1, below the 3:1 focus-appearance threshold, so the ring is doing the work, not the colour.
- **No input below 16px.** `input[type="date"]` had a 15px override that triggered iOS focus-zoom.
- **On phones the result panel rises above the form** once there is a number to show (`body.has-result` + `order:-1` under 760px). Stacked below, the payout sat off-screen behind the keyboard while typing. `calc()` owns that class — keep the toggle in both branches.
- **Body copy is capped at 68ch.** `.notes li` ran the full 900px container.
- **A print stylesheet exists** — people screenshot or print this to send to HR. It drops the noise and keeps the certificate panel.
- **`<noscript>` explains the page needs JS** and points at the written-out formula below.
- **Field hints are IBM Plex Sans, not Playfair italic.** Serif italic at 12.5px was the weakest legibility on the page. Playfair italic stays for the display register — amount-in-words, the empty state, the privacy line, the `.aux` annotation.

---

## Redesigning the UI — use UI UX Pro Max

You have the `ui-ux-pro-max-cli` skill installed globally, but the project-local skill files are missing. Set them up once:

```bash
# From this project folder:
uipro init --ai claude
```

That writes skill files into `.claude/skills/ui-ux-pro-max/` and related folders. Only after that will Claude Code load the skill for design tasks in this project.

**When invoking a redesign, use a prompt like:**

> Redesign the UI of `index.html` using the `ui-ux-pro-max` skill. Subject: statutory gratuity calculator for Indian salaried employees under the Payment of Gratuity Act, 1972. Audience: white-collar workers using it to estimate what they're owed when they leave a job. Keep all functionality intact (calculation logic, form fields, mobile/tablet breakpoints, Vercel Analytics tags, strict CSP). Do NOT add any third-party widgets or iframes — third-party services must be plain styled `<a>` links only. Ground the design in the subject's world (Indian legal/financial vernacular, salary-slip touchpoints, gazette notifications) rather than defaulting to AI-cluster palettes (cream+terracotta, black+acid-green, broadsheet).

---

## Correctness invariants (do not regress)

These were bugs once. Keep them fixed.

- **No native `<input type="date">`.** It was removed for a reason: Chrome's picker opens on the current month and the year list is a cramped scroll strip, so reaching a 2005 joining date took ~20 scroll steps. Real users could not find their year. Dates are now three typed boxes (`dojD`/`dojM`/`dojY`, `exitD`/`exitM`/`exitY`) — digits only, auto-advance on fill, backspace steps back. Do not reintroduce a date picker.
- **Dates are assembled as LOCAL dates.** `readDate(prefix)` builds `new Date(yy,mm-1,dd)` from the three boxes. Never construct one from a `'YYYY-MM-DD'` string — that parses as UTC midnight and reads back a day early west of GMT. Same for the default last-working-day: local getters, never `toISOString().slice(0,10)`.
- **`readDate` distinguishes `partial` from `invalid`.** A half-typed year must not flash an error mid-keystroke; only a complete-but-impossible date (32/01, Feb 30) does.
- **">6 months rounds up" counts days, not just whole months.** `cy()` returns `{full, rem, days, rounded}`; `rounded` bumps when `rem>6 || (rem===6 && days>0)`. Six months and zero days is dropped; six months and one day rounds up.
- **FAQPage JSON-LD must mirror the on-page `<details>` questions exactly** — same count, same wording. Google requires FAQ rich-result content to be visible on the page. Verify with:
  ```bash
  python3 -c "import re,json,io;h=io.open('index.html',encoding='utf-8').read();s=[q['name'] for q in json.loads(re.findall(r'<script type=\"application/ld\+json\">(.*?)</script>',h,re.S)[1])['mainEntity']];p=re.findall(r'<summary>(.*?)</summary>',h);print(s==p)"
  ```
- **No `aggregateRating` in the WebApplication schema.** A self-declared 4.9 with reviewCount 1 is a structured-data policy violation. It was removed deliberately.
- **Segmented controls use `role="group"` + `aria-pressed`**, not `role="tablist"` without `role="tab"` children (invalid ARIA). `press()` keeps the class and the attribute in sync — update both together.
- **The live region is `.certificate`, not the whole result panel.** A panel-wide `aria-live` re-announces every field on every keystroke.
- **Amount-in-words is spelled out** ("Rupees eleven lakh sixty-three thousand only"), via `ONES`/`TENS`/`two()`/`three()`. Don't collapse it back to pushing bare digits.
- **`window.isSecureContext` guard on the copy button**, with a `execCommand('copy')` textarea fallback — `navigator.clipboard` is undefined on plain http.
- **Reversed dates show `#dateErr`**, they do not silently blank the panel.
- **`site.webmanifest` colours track the palette** — `theme_color` and `background_color` both `#ECEFF3`, matching the `<meta name="theme-color">` in `index.html`.

### Smoke test before deploy

```bash
python3 -m http.server 8791    # then open http://localhost:8791/
```
Check: last-working-day prefills to today across the three boxes, typing `12042005` straight into the joining DD box lands as `12/04/2005` with focus auto-advancing, a ten-year run shows a non-zero payout with spelled-out words, `32` as a day and a reversed range each show their own red warning, `÷ 30` changes the number, DevTools console is clean.

---

## Deploy playbook

### Pre-deploy checks
```bash
# 1. No personal data anywhere
grep -riE "201667|Rohit Wadhwa|SFIN385|SourceFuse|HSBC|AQDPR|PBCHD|Mohali|125249" .
# Expected: no matches. If any, halt.

# 2. BMC handle points to real handle (not YOUR_HANDLE placeholder)
grep "buymeacoffee.com" index.html
# Should show: buymeacoffee.com/rohit.wadhwa

# 3. Sitemap and canonical URLs match live URL
grep "gratuity-calculator-india" sitemap.xml robots.txt
```

### Deploy
```bash
vercel --prod
```

### Post-deploy verification
```bash
# Headers landed
curl -sI https://gratuity-calculator-india.vercel.app | grep -iE "content-security|strict-transport|x-frame|x-content|referrer"

# No console errors — open DevTools in Chrome, hard refresh (Cmd-Shift-R), check Console tab

# OG image resolves
curl -sI https://gratuity-calculator-india.vercel.app/og-image.png | head -1

# Analytics enabled in Vercel dashboard:
#   Project → Analytics tab → Enable
#   Project → Speed Insights tab → Enable
#   Redeploy for scripts to fire
```

### After significant changes
Update `sitemap.xml` `<lastmod>` to today's date. Optionally submit the sitemap URL in Google Search Console.

---

## SEO — what's already in place

- Title + meta description tuned for "gratuity calculator" keyword cluster
- Open Graph + Twitter Card meta with 1200×630 `og-image.png`
- **JSON-LD structured data**: `WebApplication`, `FAQPage`, `BreadcrumbList` — enables Google rich results
- On-page FAQ section (feeds the FAQPage schema)
- `robots.txt` + `sitemap.xml`
- Canonical URL (auto-synced by JS to actual live URL)
- Semantic HTML: `<main>`, `<section>`, `<header>`, aria-labels
- Core Web Vitals tracked via Vercel Speed Insights (Google ranking signal)

**Realistic ranking outlook:** competing against ClearTax, BankBazaar, Groww on `.vercel.app` subdomain won't beat them quickly. Real levers if we ever get serious: custom domain, original written content, inbound links, 6–12 months of patience.

---

## Known constraints / lessons

- **Vercel MCP in web-chat Claude has no access to Rohit's personal Hobby account.** It can only see the `isbcs-projects` team (read-only). All deploys to the personal `gratuity-calculator-india` project must happen locally via `vercel --prod`. Do not tell the user "I can deploy this" from the web chat — I can't.
- **Iframe widgets are more trouble than they're worth.** BuyMeACoffee widget was tried and failed the CSP dance. Plain `<a>` link solved the same problem in one line.
- **Large file writes (>25KB) via Claude Desktop filesystem MCP time out.** For big rewrites, prefer `Filesystem:edit_file` with targeted diffs over `Filesystem:write_file` with the whole file.
- **Skills installed via `npm install -g` are for Claude Code CLI only.** They do NOT work in the web/desktop chat interface. When user asks for "UI UX Pro Max" or similar, hand off with a specific prompt to run in Claude Code.

---

## Out of scope

- No code beyond this static calculator.
- No dependencies, bundlers, servers, or databases.
- No third-party tracking beyond Vercel Analytics.
- No embedded widgets, iframes, or scripts from unknown domains.
- No AI-generated stock imagery, "generated" logos, or auto-content.

---

**Last updated:** August 22, 2026
**Live version:** deployed, awaiting redesign via UI UX Pro Max (after `uipro init --ai claude`)
