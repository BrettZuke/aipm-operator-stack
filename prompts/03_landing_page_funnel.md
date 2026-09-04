# Landing page / funnel page

For any new marketing page, opt-in, VSL page, confirmation page, or section rebuild.

---

Operate under the Fable Protocol in CLAUDE.md.

Build: {{WHAT, e.g. opt-in page for X offer}}
Client/brand: {{WHO, plus links to brand refs, prior approved pages, or voice files}}
Copy source: {{PROVIDED BELOW / write it from these notes: ...}}
Deploy target: {{VERCEL PROJECT or "new project", plus domain if any}}

Process, in order:
1. Load the high-end-visual-design skill and the premium-funnel-page skill before writing any UI. Pick a named vibe and layout archetype and state them.
2. Keep a reference registry of pages you or the client have approved, and pick the closest winner for this use case and business type; copy its patterns and avoid everything you previously rejected. Then study the brand refs and at least one prior approved page for this client. List the fonts, colors, and patterns you will reuse. Never recolor a prior site for a new vertical; build a fresh identity.
3. Build mobile-first, then desktop. Real content only, no lorem ipsum. SVG line icons only, no emoji anywhere. Fonts via Fontshare or self-hosted; Inter and Roboto are banned. Real photos over AI-generated (Wikimedia Commons API if stock is needed).
4. Verify before calling it done: run `python3 execution/page_qa.py <url>` (from Agentic Workflows). It screenshots 1440px and 390px, fails on console errors, dead links, banned fonts, and banned characters. Paste its output; RESULT must be PASS. Also run `python3 execution/copy_lint.py` on the page copy source.
5. Deploy with the Vercel CLI using the correct token and scope for this client. A client's projects need that client's own token plus --scope <VERCEL_SCOPE>; your own projects use your personal token. Check .env and project memory before guessing. Fetch the live URL and confirm the new content serves.
6. Commit the working tree after the deploy so git stays clean.

Report: live URL, screenshot paths, each verification with its result, and any assumptions made.
