# Probamo website

Marketing site for Probamo — manual QA for startups and AI-era builders.
Hosted on Cloudflare Workers; every push to `main` deploys automatically.

## Structure

- `public/` — the website (HTML, CSS, JS, fonts, images, `_headers`)
- `src/index.js` — Worker that handles the contact form (`POST /api/contact`) and serves `public/`
- `wrangler.jsonc` — Cloudflare config
- `tools/build_service_pages.py` — content for the service landing pages (`/website-qa`, `/webshop-qa`, …). Edit it and run `python3 tools/build_service_pages.py` to regenerate the pages in `public/`.

## Contact form

Enquiries are sent through Proton SMTP from `forms@probamo.com` to `sara@probamo.com` (the public address on the site is testing@probamo.com).
Secrets are set in Cloudflare (Workers & Pages → probamo-website → Settings → Variables and Secrets):

- `SMTP_TOKEN` — Proton SMTP token for forms@probamo.com (required)
- `TURNSTILE_SECRET` — Cloudflare Turnstile secret key (optional spam check)

## Run locally

```bash
npm install
npx wrangler dev
```

Put local secrets in `.dev.vars` (ignored by git).
