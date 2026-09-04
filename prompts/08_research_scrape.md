# Research / scrape

---

Operate under the Fable Protocol in CLAUDE.md.

Task: {{WHAT DATA, from WHERE, roughly how much}}
Deliverable: {{Google Sheet / summary doc / dataset}}

1. Check execution/ for an existing script that already does this or most of it. Reuse and extend before writing new.
2. For Apify: search the store, prefer high-usage actors, and fetch the actor's input schema before calling it. If a run will cost money or credits, state the estimated cost and STOP for approval first. Free and already-paid-for runs proceed without asking.
3. Intermediates go to .tmp/ and never get committed. Deliverables go to cloud (Google Sheets or Docs) where the client can open them.
4. Validate the output before delivering: row counts, spot-check 5 records against the live source, and note gaps or failures honestly instead of padding.

Report: link to the deliverable, row counts, method used, known gaps.
