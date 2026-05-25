# CLAUDE.md — Gratuity Calculator (India)

Context for AI assistants (Claude Code, Copilot, etc.) working on this project. Read fully before acting.

## What This Project Is

A **single-page, static gratuity calculator** for India under the Payment of Gratuity Act, 1972.
Pure vanilla **HTML + CSS + JS** in one file. **No framework, no build step, no backend, no package.json.**
All computation runs client-side in the browser.

## File Inventory

| File | Purpose |
|------|---------|
| `index.html` | The entire app — markup, styles, logic, SEO meta, JSON-LD |
| `vercel.json` | Security headers (CSP, HSTS, X-Frame-Options, etc.), `cleanUrls` |
| `og-image.png` | 1200x630 social share image |
| `robots.txt` | Crawler rules + sitemap pointer |
| `sitemap.xml` | Single-URL sitemap |
| `site.webmanifest` | PWA/mobile metadata |
| `README.md` | Project documentation for users and contributors |
| `CONTRIBUTING.md` | Contribution guidelines |
| `SUPPORT.md` | How to get help and report issues |
| `LICENSE` | MIT License |

**Do not add build tooling.** This is a static site — no framework, no build command. Output directory is the project root.

## Architecture Decisions

- **Single-file is intentional** — `index.html` contains markup, CSS, and JS. Don't split into separate files unless explicitly asked. This makes drag-and-drop deploy trivial.
- **No dependencies** — No npm, no package.json, no node_modules. Keep it this way.
- **Client-side only** — All computation runs in the browser. No backend, no API calls, no data transmission.

## Deployment

- **Provider:** Vercel (static site, no build step)
- **Production URL:** `https://gratuity-calculator-india.vercel.app/`
- **Auto-deploys** from `main` branch via Vercel GitHub integration
- **Branch protection** — only the maintainer can merge to `main`

The production URL is hard-coded in SEO meta tags, sitemap, and robots.txt. The JS auto-syncs `<canonical>` and `og:url` at runtime, but static values must stay correct for crawlers.

## Privacy / Security Guardrails (NON-NEGOTIABLE)

- **100% generic** — Never hard-code anyone's real salary, name, employer, bank, PAN/PF, or location. The only example value allowed is the neutral `50,000` placeholder.
- **Client-side only** — Do not add a backend, do not POST form data anywhere, do not add analytics or trackers that transmit user input. The calculator must never send what a user types off their device.
- **CSP is locked down** — Keep the Content Security Policy in `vercel.json` intact. If you add a script/resource, update CSP deliberately — don't loosen it to `*`.
- **External resources** — Only Google Fonts (already in CSP). The Buy Me a Coffee button is a plain outbound `<a>` link, not an embedded widget/script — keep it that way.

## Gratuity Formula (Do Not Change Without Legal Source)

**Covered employers** (10+ employees):
```
Gratuity = (Basic + DA) x 15 x completed_years / 26
```

**Uncovered employers:**
```
Gratuity = (Basic + DA) x 15 x completed_years / 30
```

- Tax-free cap: Rs 20,00,000 under Section 10(10)
- Final partial year > 6 months rounds up to a full year
- Eligibility: 5 years continuous service (waived on death/disability)

## Editing Conventions

- Indian number formatting uses lakh/crore grouping — preserve the custom `inr()` function
- CSS uses custom properties defined in `:root` — use them for consistency
- Breakpoints: 760px (tablet/stack layout), 440px (phone)
- Touch targets: minimum 44px height on all interactive elements
- Input font-size: 16px minimum (prevents iOS auto-zoom)
- Prefer `prefers-reduced-motion` media query for accessibility

## Code Style

- No comments unless explaining a non-obvious **why**
- No console.log or debugging artifacts
- Use existing CSS variables, don't create new color values inline
- Keep the animation/transition style consistent with existing patterns

## What NOT To Do

- Don't introduce frameworks, bundlers, or build steps
- Don't add analytics, trackers, or telemetry
- Don't split `index.html` into separate files
- Don't change the gratuity math without citing a legal source
- Don't add personal/sensitive data in any file
- Don't loosen the Content Security Policy
