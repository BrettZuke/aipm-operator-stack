# Audit / review (read only)

---

Operate under the Fable Protocol in CLAUDE.md.

Audit target: {{REPO, DIRECTORY, or FEATURE}}
Focus: {{security / correctness / data accuracy / all}}

Rules:
1. Work SOLO. No subagents, no swarms, no Workflow tool. One careful pass.
2. Read only. Change nothing during the audit.
3. Verify every finding by tracing the actual code path before reporting it. No theoretical findings; "could potentially" without a concrete triggering scenario does not get reported.
4. For each finding: severity (CRITICAL / HIGH / MEDIUM / LOW), file and line, one-sentence defect, and the concrete failure scenario (which inputs and state trigger it, what breaks for whom).
5. Rank by severity. Skip style nits unless asked.
6. End with the ranked list and wait for approval before fixing anything.
