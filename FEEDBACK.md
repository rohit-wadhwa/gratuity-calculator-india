# Feedback for Claude Code — v2.0.0 Audit

**Audited:** 22 Aug 2026 · **Live URL:** https://gratuity-calculator-india.vercel.app/ · **Auditor:** Claude (web chat, `frontend-design` skill)

## TL;DR

You did materially better work than my baseline. Real bug fixes (timezone-safe dates, correct 6-month rounding, proper number-to-words), real UX wins (mobile panel reorder, print stylesheet, `aria-pressed`, `execCommand` fallback), zero regressions.

Below: **what to keep doing**, **what to fix**, and **what to consider**. Each item cites the UI UX Pro Max rule or the deliberate design decision it violates, so the feedback is checkable.

---

## ✅ Keep doing this

These were unprompted, correct, and non-obvious. Worth adding to your default patterns:

1. **Timezone-safe date input.** Replacing `<input type="date">` with 3-part `DD/MM/YYYY` inputs and building `new Date(yy, mm-1, dd)` locally instead of parsing `'YYYY-MM-DD'` (which is UTC and reads a day early west of GMT). The inline code comment calling this out is exactly right.
2. **Rounding boundary correctness.** `rem === 6 && days > 0` counts as "over six months" — matches the Act's *"in excess of six months"* wording. Old code checked `> 6` and missed the edge.
3. **Recursive number-to-words.** `three(n)` handling hundreds + tens + ones properly, so `₹11,63,463` says *"eleven lakh sixty-three thousand four hundred sixty-three"* not *"eleven lakh 63 463"*.
4. **`:focus-visible` with `@supports not selector(...)` fallback** for older browsers. Textbook progressive enhancement.
5. **`role="group"` + `aria-pressed` on segmented controls.** Correct pattern (tablist would imply tab-panel wiring, which isn't the case).
6. **Mobile panel reorder via `.has-result` body class.** After a calc, result surfaces above inputs on phone — user isn't scrolling to see their answer.
7. **`<noscript>` fallback + print stylesheet + `execCommand` clipboard fallback.** Quality-floor items done without announcing them.
8. **Version metadata in footer.** Small pattern, huge support value.

---

## 🔴 Must fix (three items)

### 1. Screen reader spam on the certificate

**Where:** `<div class="certificate" aria-live="polite" aria-atomic="true">`

**Problem:** `aria-atomic="true"` re-announces the entire block on every state change, and `calc()` fires on every keystroke. So typing "50000" into Basic causes the screen reader to say *"Rupees zero only ... Rupees seventy-five thousand only ... Rupees seven lakh fifty thousand only ..."* five times in a row. Same on every date-part change.

**Skill rule violated:** `contextual-live-badge-updates` (Accessibility, Priority 1 CRITICAL):
> *"Announce a changed count/status as a complete contextual phrase without moving focus; use one appropriate live/status region and atomic updates only when needed."*

Atomic here is the anti-pattern.

**Fix:** Debounce the announcement. Either:

- **Option A (simpler):** Remove `aria-live` from `.certificate`. Add a **separate visually-hidden `<div id="sr-status" aria-live="polite" role="status">`** near the amount. Populate it from `calc()` but debounced to 500ms after last input:

```js
var srTimer;
function announce(msg){
  clearTimeout(srTimer);
  srTimer = setTimeout(function(){ $('sr-status').textContent = msg; }, 500);
}
// in calc(), after computing g:
announce(elig ? ('Gratuity ' + inr(g) + '. ' + (g <= CAP ? 'Fully tax-free.' : 'Partially taxable.'))
             : ('Not yet eligible. Need ' + (5-full) + ' more year' + (5-full!==1?'s':'') + '.'));
```

- **Option B (correct-but-more-work):** Keep `aria-live` but drop `aria-atomic`, and only re-populate `#amount` when the final numeric value actually changes (compare to a stored previous value).

Either fixes the spam.

### 2. `§` (section mark) changed to `₹` (rupee mark) — signature element lost

**Where:** `.cite .mark` in header, `.notes-head::before` above "The formula".

**Problem:** The original design used `§` deliberately — gratuity IS structured by Act sections (Sec. 4(1), Sec. 4(2), Sec. 10(10)). The section mark tied the visual language to the legal/gazette subject, per the frontend-design principle *"Structure is information ... should encode something true about the content, not decorate it."*

Changing `§` → `₹` removes that connection. `₹` is a currency mark; it's redundant on a page already labeled "Gratuity Calculator" and full of `₹` values in the breakdown table. Two rupee marks fighting for eyeball is worse than one section mark doing real work.

**Fix:** Revert both to `§`. If the concern was font rendering (`§` looks off in Playfair), keep it in Playfair Display specifically — that face renders it beautifully.

**Also change:** `.cert-label .ref` currently says `Sec. 4(2)`. This is fine (more accessible than `§ 4(2)`), so keep that one. The `§` mark only belongs in the eyebrow/notes-head positions.

### 3. Local is v2.0.1, deployed is still v2.0.0

Local `index.html` has `APP_VERSION = '2.0.1'`; the live site fetched via `curl` still shows `<meta name="version" content="2.0.0">`. Drift.

**Fix:** `vercel --prod` from this folder. Also update `<meta name="version">` from `2.0.0` → `2.0.1` in the HTML head (currently only the JS constant is bumped).

---

## 🟡 Should fix (four items)

### 4. Skip link is missing

**Skill rule:** `skip-links` (Accessibility, Priority 1 CRITICAL):
> *"Skip to main content for keyboard users."*

Not present. Add before `<div class="page">`:
```html
<a href="#result-block" class="skip-link">Skip to calculator</a>
```
Style it so it's invisible until focused (standard pattern). Give the calculator `<main id="result-block">` (already has `<main>`, just add the id).

### 5. `theme-color` is too light for iOS Safari

**Current:** `#ECEFF3` (very light grey). iOS Safari uses this to tint the browser chrome — this value makes the chrome nearly indistinguishable from white/off-white system UI.

**Fix:** Use one of the darker tokens for stronger presence:
- `#0F1A2F` (ink) — most striking, matches favicon background
- `#1B5E48` (accent) — brand-forward option

Also update `site.webmanifest` `theme_color` and `background_color` to match. Currently both are `#ECEFF3` — background is fine, theme should be dark.

### 6. `.warn` hardcodes `#F7E4E1` instead of using a design token

**Where:** `.warn { ... background: #F7E4E1; ... }` in the CSS.

Every other color reference in the file uses `var(--…)`. This one hardcodes a value. Add `--danger-soft: #F7E4E1;` to `:root` and reference `var(--danger-soft)` in `.warn`. Same treatment for the `--neg` you already have — consider `--danger` as a clearer name.

**Skill rule:** `Typography & Color` (Priority 6): *"Semantic color tokens ... no raw hex in components."*

### 7. PWA icons array is empty

**Where:** `site.webmanifest` has `"icons": []`.

**Effect:** PWA install prompts fail on Android; iOS "Add to Home Screen" falls back to a generic icon.

**Fix:** Generate a 192×192 and 512×512 PNG from the `§`-in-navy-rounded-square favicon design. Either extend `generate-og-image.py` to output them, or one-shot in Python:

```python
from PIL import Image, ImageDraw, ImageFont
for size in [192, 512]:
    img = Image.new("RGB", (size, size), (15, 26, 47))  # --ink
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Bold.ttf", int(size*0.62))
    txt = "§"
    bb = d.textbbox((0,0), txt, font=f)
    d.text(((size-(bb[2]-bb[0]))/2 - bb[0], (size-(bb[3]-bb[1]))/2 - bb[1]), txt, font=f, fill=(246,240,224))
    img.save(f"icon-{size}.png", "PNG")
```

Then add to `site.webmanifest`:
```json
"icons": [
  { "src": "/icon-192.png", "sizes": "192x192", "type": "image/png" },
  { "src": "/icon-512.png", "sizes": "512x512", "type": "image/png" }
]
```

---

## 🟢 Consider (three items — judgment calls)

### 8. Palette drift from "distinctly Indian" brief

Original brief specified **sindoor vermilion `#B23A2F` + warm parchment `#F6F0E0`** — deliberately grounded in Indian visual vernacular (sindoor/gulal reference, gazette paper). You shipped **forest green `#1B5E48` + cool grey-blue `#ECEFF3`** — closer to a generic fintech/government-services palette.

Looking at your own `data/colors.csv`, this reads as a hybrid of Row 6 (Financial Dashboard: green accent for positive indicators) + Row 13 (Government/Public Service: navy primary, light bg). That's a defensible read of the subject as "statutory financial tool."

But it trades **specificity for safety**. The `frontend-design` principle:
> *"The subject's own world, its materials, instruments, artifacts, and vernacular, is where distinctive choices come from."*

**No action required if intentional.** But if the palette shift was auto-derived from generic "financial" heuristics rather than a considered rejection of the Indian-specific direction, this is worth reconsidering. Alternatively: keep the light + navy structure but restore the vermilion accent — the compromise gets you Government-App legibility with actual Indian character.

### 9. `vercel.json` `ignoreCommand` skips all non-main deploys

```json
"ignoreCommand": "if [ \"$VERCEL_GIT_COMMIT_REF\" == \"main\" ]; then exit 1; else exit 0; fi"
```

This blocks preview deployments on feature branches (Vercel's most useful collaboration feature). May be intentional (locks builds to main) or an artifact of a template. If Rohit wants preview URLs for branches shared with colleagues, remove this block.

### 10. First mention of "DA" isn't expanded

The abbreviation "DA" appears in the input label and result rows before the hint text expands it. Screen reader users hear "dee ay" without context. Wrap the first visible occurrence:

```html
<label for="basic">Monthly Basic + <abbr title="Dearness Allowance">DA</abbr></label>
```

Minor accessibility enhancement.

---

## Suggested prompt to hand back to Claude Code

Save the above as `FEEDBACK.md` in the project root. Then in Claude Code:

> Read `FEEDBACK.md`. Address the three items under "Must fix" and the four under "Should fix" in a single pass. Skip the three "Consider" items unless I say otherwise. Preserve every improvement you made in v2.0.0 (timezone-safe dates, rounding, number-to-words, focus-visible, mobile panel reorder, etc.). Bump `APP_VERSION` to `2.0.2` and `<meta name="version">` to match. Deploy with `vercel --prod` after.

---

## Notes on tooling

- I could not run `vercel --prod` from the web chat (Vercel MCP token scope is limited to a different team). All deploys still need to happen from Rohit's Mac.
- The `ui-ux-pro-max` skill files are installed at `.claude/skills/ui-ux-pro-max/` — I read `SKILL.md`, `data/catalog-summary.json`, `data/products.csv`, and `data/colors.csv` to ground this feedback. The rules cited above are verbatim from that SKILL.md.
- No security or privacy regressions in v2.0.0. All 6 security headers present on the live site; grep for personal data on live HTML came back clean.
