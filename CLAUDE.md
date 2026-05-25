# CLAUDE.md — Gratuity Calculator (India)

Project context and operating instructions for Claude Code. Read this fully before acting.

## What this project is

A **single-page, static gratuity calculator** for India under the Payment of Gratuity Act, 1972.
Pure vanilla **HTML + CSS + JS** in one file. **No framework, no build step, no backend, no package.json.**
All computation runs client-side in the browser.

## File inventory (do not add build tooling)

| File | Purpose |
|------|---------|
| `index.html` | The entire app — markup, styles, logic, SEO meta, JSON-LD. |
| `vercel.json` | Security headers (CSP, HSTS, X-Frame-Options…), `cleanUrls`. |
| `og-image.png` | 1200×630 social share image. |
| `robots.txt` | Crawler rules + sitemap pointer. |
| `sitemap.xml` | Single-URL sitemap. |
| `site.webmanifest` | PWA/mobile metadata. |

This is a static site — Vercel should detect **no framework** and **no build command**. Output directory is the project root.

## Deploy target

- **Provider:** Vercel
- **Team / scope:** `isbcs-projects` (id `team_Nc7nn3uMSscJJlKyLFFz1J5y`)
- **Project name:** `gratuity-calculator-india`
- **Expected production URL:** `https://gratuity-calculator-india.vercel.app/`
  (This exact slug is hard-coded in the SEO meta tags, sitemap, and robots.txt. Keep the name so the URLs match — otherwise complete the "post-deploy URL fix" below.)

### Deploy command

```bash
# from the project root (the folder containing index.html)
vercel --prod
```

When prompted: set up & deploy → scope = **isbcs-projects** → project name = **gratuity-calculator-india** → framework = **Other** → leave build/output empty. If the Vercel plugin/integration is used instead of the CLI, deploy as a **static project, no build step**.

## PRE-deploy checklist (must do)

1. **Buy Me a Coffee handle** — in `index.html`, find:
   ```
   href="https://www.buymeacoffee.com/YOUR_HANDLE"
   ```
   Replace `YOUR_HANDLE` with the real handle. **Do not deploy with the placeholder.**
2. Confirm no personal data is present (see "Privacy / security guardrails"). Run a quick grep before shipping.

## POST-deploy checklist

1. **Make it public.** In Vercel → Project → Settings → **Deployment Protection** → ensure it is **OFF** (Standard Protection / SSO disabled), so anyone with the link can open it.
2. **If the final URL is NOT** `gratuity-calculator-india.vercel.app`, update the hard-coded domain in these places (the JS auto-syncs `<canonical>` and `og:url` at runtime, but crawlers/social scrapers need the static values correct):
   - `index.html`: `<link rel="canonical">`, `og:url`, `og:image`, `twitter:image`
   - `sitemap.xml`: `<loc>`
   - `robots.txt`: `Sitemap:` line
3. **Verify it works:** load on mobile + desktop, confirm the calculation updates live, confirm `og-image.png` resolves at `/og-image.png`.
4. **Verify headers:** `curl -sI <url>` should show `content-security-policy`, `strict-transport-security`, `x-frame-options: DENY`.
5. (Optional) Submit the sitemap in Google Search Console for indexing.

## Privacy / security guardrails (NON-NEGOTIABLE)

- **This is a public tool. Keep it 100% generic.** Never hard-code anyone's real salary, name, employer, bank, PAN/PF, or location. The only example value allowed is the neutral `50,000` placeholder.
- **Client-side only.** Do not add a backend, do not POST form data anywhere, do not add analytics or trackers that transmit user input. The calculator must never send what a user types off their device.
- **Keep the CSP in `vercel.json` intact.** If you add a script/resource, update CSP deliberately — don't loosen it to `*`.
- Only external resource allowed is **Google Fonts** (already in CSP). The Buy Me a Coffee button is a plain outbound `<a>` link, not an embedded widget/script — keep it that way.

## Editing conventions

- Keep everything in `index.html` — **single-file is intentional** (makes drag-and-drop deploy trivial). Do not split into separate JS/CSS files unless explicitly asked.
- Indian number formatting (lakh/crore grouping) is custom — preserve it.
- Gratuity math: covered employers `(Basic+DA × 15 × completed_years) / 26`; uncovered `/ 30`. Tax-free cap `₹20,00,000`. Final partial year >6 months rounds up. Don't change these without a source.
- Mobile/tablet: breakpoints at 760px (stack) and 440px (phone). Maintain ≥44px touch targets and 16px inputs (prevents iOS zoom).

## Out of scope

- No code beyond this static calculator.
- Don't introduce dependencies, bundlers, or a server.
