# Contributing

Thanks for your interest in improving the Gratuity Calculator! This guide will help you get started.

## Ground Rules

1. **Single-file architecture** — All app code lives in `index.html`. Don't split it into separate JS/CSS files or add a build step.
2. **No dependencies** — No npm, no frameworks, no bundlers. Vanilla HTML + CSS + JS only.
3. **Privacy first** — Never add analytics, trackers, or anything that transmits user input off-device. This is a core promise of the tool.
4. **Don't change the math** — The gratuity formula is defined by the Payment of Gratuity Act, 1972. Don't change it without citing a legal source in your PR.

## What We'd Love Help With

- Accessibility improvements (ARIA, keyboard navigation, screen reader testing)
- UI/UX refinements (better mobile experience, animations, visual polish)
- SEO enhancements (structured data, meta tags)
- Localization (Hindi, regional languages)
- Bug fixes
- Documentation improvements

## How to Contribute

1. **Fork** the repo and clone your fork
2. Create a **feature branch** from `main`:
   ```bash
   git checkout -b feature/your-improvement
   ```
3. Make your changes in `index.html` (or supporting files like `vercel.json` if needed)
4. Test on both **desktop and mobile** — check the calculator still works end to end
5. **Commit** with a clear message describing what and why
6. **Push** to your fork and open a **Pull Request** against `main`

## PR Guidelines

- Keep PRs focused — one improvement per PR
- Describe what you changed and why in the PR description
- Include before/after screenshots for visual changes
- Make sure the gratuity calculation still works correctly after your changes
- Don't include personal data (real salaries, names, etc.) in examples or test values

## Testing Checklist

Before submitting, verify:

- [ ] Calculator produces correct results (try: Rs 50,000 basic, 10 years, covered = Rs 2,88,462)
- [ ] Responsive layout works on mobile (< 440px) and tablet (< 760px)
- [ ] Both input modes work (dates and manual years)
- [ ] Both employer types work (covered/uncovered)
- [ ] Tax calculation is correct (free under 20L, partial above)
- [ ] No console errors

## Code Style

- No comments unless explaining a non-obvious **why**
- Use the existing CSS custom properties (variables in `:root`)
- Maintain 44px minimum touch targets on interactive elements
- Keep `input[type="number"]` at 16px font-size (prevents iOS auto-zoom)
- Indian number formatting uses lakh/crore grouping — preserve the custom `inr()` function

## Security

- Don't loosen the Content Security Policy in `vercel.json`
- Don't add inline scripts that would require `unsafe-eval`
- Don't add external resources beyond Google Fonts
- If you find a security issue, please open an issue (or email privately for sensitive findings)

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
