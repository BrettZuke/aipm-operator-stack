# 14 - Supabase Security Audit (+ production-readiness mandate)

Reusable prompt for a full application security audit of a Supabase/Postgres/Next.js app,
plus the "make it world-class and launch-ready" follow-through. Saved 2026-07-11, run against a live
production dashboard. Paste the whole block below; swap the app name where marked.

## When to use
- Any time before exposing a Supabase-backed app to the public internet.
- After a big schema/RLS/webhook change, re-run the RLS + Database + API sections.
- The second half (coverage, SonarQube, GHAS, Dependabot, PR workflow) is the standing
  production-readiness bar, not a one-off.

## How to run it here (routing)
- Security analysis is security-sensitive: route the audit to the `security-executor` (or a
  fresh-context `verifier` for an unbiased read of my own code), never self-review in the
  main session. Give it the repo path + live URL + this prompt's output format.
- Do the cheap deterministic wins yourself in parallel: Dependabot config, PR template,
  workflow files. Fact-check GHAS/SonarQube availability against the repo's actual plan
  (private repo => GHAS code scanning/secret scanning need GH Advanced Security or the repo
  made public; CodeQL is free on public repos) before promising it is "on".
- Reconcile findings against the tenancy model already verified in memory
  (your own tenant-isolation notes) before escalating: RE-VERIFY, do not assume.

## THE PROMPT

You are a principal application security engineer specializing in Supabase, PostgreSQL,
authentication, and Row-Level Security (RLS).

Perform a complete security audit of <APP NAME>. Analyze all provided files: SQL schema,
migrations, RLS policies, Supabase config, Edge Functions, database functions, API code, auth
code, frontend code that touches Supabase, and environment-variable usage. Assume public
internet exposure. Identify every security issue you can find.

Evaluate specifically:

Row-Level Security: RLS enabled on every user-data table? Which tables are exposed because RLS
is off? Missing policies? USING(true)/WITH CHECK(true) present? Does every policy scope with
auth.uid() or an equivalent ownership model? Can a user read / update / delete another user's
rows? Can anonymous users reach protected data?

Authentication: correct auth.uid() use, service-role misuse, JWT assumptions, trusting
client-provided user IDs, missing ownership validation, session security.

Database security: dangerous SQL functions, SECURITY DEFINER misuse, unsafe RPCs, missing
foreign keys, missing constraints, privilege-escalation paths.

API security: missing authorization, trusting client input, missing validation, broken access
control, insecure endpoints.

Frontend: exposed secrets, wrong assumptions about anon keys, client-side authorization
mistakes, sensitive data leakage.

Storage: bucket policies, public file exposure, unauthorized uploads/downloads.

General: OWASP Top 10, injection, XSS, CSRF where applicable, sensitive logging, information
disclosure.

For every finding: Severity (Critical/High/Medium/Low); Problem; Why it is dangerous (realistic
attack scenario); Evidence (quote the code); Recommended Fix; Replacement Code (corrected
SQL/code).

Then produce: Executive Summary; Risk Score (0-100); Critical/High/Medium/Low findings;
secure replacement RLS policies; secure migration SQL; deployment checklist; anything that must
be fixed before public release. If information is missing, state assumptions rather than guessing.

You are also Lead Engineer, Architect, CTO, Security, DevOps, QA Lead, Product/UX Designer, and
Head of Marketing. Objective: transform this codebase into a world-class, production-ready SaaS
ready for public launch.
- Get to >90% unit test coverage.
- Use SonarQube + GitHub Advanced Security.
- Run every PR (use PRs) through the same workflows.
- Enable Dependabot, at minimum for security patches.
- Course-correct the agent: when it wants to do something silly (e.g. implement SSO with a
  provider from scratch), steer it to a proven implementation. If GHAS flags missing
  rate-limiting on one route, review rate-limiting on ALL routes to industry best-practice.
- Then loop back to #1.
