---
name: asset-hosting-and-scrapers
description: Use when hosting large files (video, VSLs, anything over Vercel's 100MB limit or bandwidth budget), when an Apify token hits its monthly quota, when any API returns Cloudflare 403 error 1010, or when a scrape needs a fallback route.
---

# Asset hosting and scraper operations

## Cloudflare R2: the default big-file host

Any static asset too big for Vercel (100MB per-file limit) or too bandwidth-hungry for the Hobby 100GB transfer cap goes to R2 on your Cloudflare account. Free tier: 10GB storage, zero egress forever.

- Creds in AW/.env: CF_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, CF_API_TOKEN. S3-compatible endpoint `https://<CF_ACCOUNT_ID>.r2.cloudflarestorage.com`, region auto.
- One command: `python execution/r2_upload.py <local_path> <bucket> <key>`: creates the bucket if missing, multipart upload, enables the public pub-<id>.r2.dev domain, prints the URL.
- Existing buckets: `the client program-media` (the client videos, <YOUR_R2_PUBLIC_HOST>), `<BUCKET>` (a client VSL).
- Vercel integration pattern: keep the local file in the repo as the re-upload source, add its dir to .vercelignore, point the src at the R2 URL. the client's funnels are the worked example (see the client-funnels-ops).
- Compress video BEFORE uploading masters: `ffmpeg -i master.mp4 -c:v libx264 -preset slow -crf 21 -profile:v high -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 128k -ac 2 out.mp4` (CRF 21 is visually lossless at 1080p, typically 5-10x smaller). Re-encoding already-optimized web video saves ~nothing; measure before promising savings.
- rclone against R2: inline `:s3,...` connection strings break on https endpoints; use env-var remote config (RCLONE_CONFIG_R2_TYPE etc).
- r2.dev public URLs are rate-limited at very high traffic; a custom domain needs the DNS zone on Cloudflare (clientprogram.example.com is not, by choice).

## Apify: eleven tokens, never stall on quota

"Monthly usage hard limit exceeded" is NOT a blocker and never a reason to top up. The setup deliberately uses 11 free-tier accounts ($5 credit each per month, so ~$55/mo of scraping). Fall through in order.

The pool lives in `.env`: `APIFY_API_TOKEN` (slot 1) then `APIFY_TOKEN`, `APIFY_TOKEN_2` … `APIFY_TOKEN_11`. Only apify-1 and apify-2 are still MCP servers in ~/.claude.json (the other eight were moved out on 2026-08-12 because ten MCP servers cost ~900MB per session), so ANY loader that reads only ~/.claude.json sees 2 of 11 tokens. Do not write a new one.

Single source of truth: `execution/apify_pool.py` → `apify_tokens()`. Import it rather than re-deriving the pool:

    import sys; sys.path.insert(0, "execution")
    from apify_pool import apify_tokens

Run it directly (`python3 execution/apify_pool.py`) to print the pool masked. Reference fall-through implementation: `run_actor_with_fallback()` in `execution/scrape_creator_dossier.py`. Balances and hard limits across all 11: `python3 execution/check_apify_balances.py` (add `--raise-to 5` if an account's hard spend limit is $0, which blocks paid actors even with credit left). In-session MCP calls only reach the first two accounts (mcp__apify-1__…, mcp__apify-2__…); for the full pool, go through a script.

The content-intelligence cron is a separate repo and gets the pool from its own `APIFY_TOKENS` GitHub secret (comma-separated). Adding a token to `.env` does NOT reach it: re-push with `gh secret set APIFY_TOKENS --repo BrettZuke/content-intelligence`.

Scrape routing lessons: Reddit blocks datacenter fetchers, browser-UA curl, jina reader, AND the generic rag-web-browser; a Reddit-specific store actor works (pay-per-result, cents). Prefer the free ladder first: curl with browser UA, then Playwright MCP (real browser, but the shared profile can be locked by a parallel session), then a specialized Apify actor.

## The universal Cloudflare 1010 rule

Any API fronted by Cloudflare (Supabase management API, Make.com, many webinar platforms, others) 403s with body "error code: 1010" on default python/urllib/curl user agents. It looks like an auth or scope error; it is not. Send a desktop browser User-Agent header and the same token works. Check this FIRST when a scripted API call 403s.

## Hard stops

- Never leave a client page serving heavy video from Vercel when R2 exists; bandwidth exhaustion took a live funnel to 81% of its monthly cap once.
- Never conclude "token lacks permission" from a Cloudflare-fronted 403 until the browser-UA retry has been tried (a wrong scope conclusion cost a debugging session).
- Paid scraper actors: keep single-run cost under ~$1 without asking; state the cost in the report.

## When NOT to use this skill

- Which scraper actor for creator intel: the analyze-creator and spy skills. Site deploys: the per-property deploy skills.

## Provenance and maintenance

Written 2026-07-03. Apify pool section rewritten 2026-08-29 (11 tokens, pool moved to .env, shared loader added).

- Re-verify R2 access: `python execution/r2_upload.py --help` and an ls via rclone env-remote (no uploads).
- Re-verify the token chain: `python3 execution/apify_pool.py` (expect 11) and `python3 execution/check_apify_balances.py` for live per-account credit.
