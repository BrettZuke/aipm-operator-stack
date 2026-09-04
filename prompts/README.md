# Prompt Library

Task templates with the working discipline baked in per task type. Open the template,
fill the `{{BLANKS}}`, paste the whole thing as your message.

`00_universal_wrapper.md` is the default for anything with no specific template.

Two things make these work:

1. **The operating protocol** in your `~/.claude/CLAUDE.md`. It loads in every session,
   every project, every model: investigate before editing, verify with evidence before
   claiming done, report failures first, root-cause debugging.
2. **Deterministic gates** in `execution/`: `copy_lint.py` (banned characters and slop
   phrases), `page_qa.py` (screenshots both widths, console errors, dead links, banned
   fonts), `deploy_verify.py` (proves new content is actually live). The templates call
   them so the model cannot skip or fudge verification.

## Files

- `00_universal_wrapper.md`: default wrapper for any task
- `01_spec_first.md`: bigger builds, see the plan before work starts
- `02_debug_fix.md`: bugs and broken things
- `03_landing_page_funnel.md`: pages, funnels, sections
- `06_audit_review.md`: audits and reviews, read only
- `07_ship_deploy.md`: deploys
- `08_research_scrape.md`: scraping and research
- `14_supabase_security_audit.md`: Supabase security and production readiness

## Honest limits

This transfers discipline, not raw capability. A model with this scaffolding will verify
its work, finish its turns, make decisions instead of asking, and report honestly. Slice
big work into spec, execute, review, and use `01_spec_first.md` for anything expensive so
you approve the plan before tokens burn.
