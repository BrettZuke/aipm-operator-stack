# Debug and fix

---

Operate under the Fable Protocol in CLAUDE.md, the debugging order especially.

Bug: {{SYMPTOM, exact error text if you have it}}
Started: {{WHEN, and what changed around then if known}}
Repro: {{STEPS, or "unknown"}}

Rules:
1. Reproduce it yourself first. If you cannot reproduce it, that becomes the task: instrument and reproduce. Do not fix blind.
2. Read the entire error and stack trace before opening any file.
3. State your root-cause hypothesis in one sentence before editing. If you have several, rank up to three and test the cheapest first.
4. Fix the root cause, not the symptom. Re-run the original repro to prove the fix.
5. Grep for the same bug class elsewhere in the codebase and fix siblings.
6. Two failed fix attempts means the diagnosis is wrong: stop editing and re-diagnose from scratch. Do not stack guesses.
7. Do not add fallbacks that hide the failure. Do not weaken or delete tests.

Report: root cause in one sentence, the fix, proof (repro output before and after), and which sibling locations you checked.
