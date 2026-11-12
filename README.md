# Probamo website

Marketing site for Probamo — manual QA for startups and AI-era builders.
Hosted on Cloudflare Workers; every push to `main` deploys automatically.

## Structure

- `public/` — the website (HTML, CSS, JS, fonts, images, `_headers`)
- `src/index.js` — Worker that handles the contact form (`POST /api/contact`) and serves `public/`
- `wrangler.jsonc` — Cloudflare config

## Contact form

Enquiries are sent through Proton SMTP from `forms@probamo.com` to `sara@probamo.com`.
Secrets are set in Cloudflare (Workers & Pages → probamo-website → Settings → Variables and Secrets):

- `SMTP_TOKEN` — Proton SMTP token for forms@probamo.com (required)
- `TURNSTILE_SECRET` — Cloudflare Turnstile secret key (optional spam check)

## Run locally

```bash
npm install
npx wrangler dev
```

Put local secrets in `.dev.vars` (ignored by git).
