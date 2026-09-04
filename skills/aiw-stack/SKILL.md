---
name: aiw-stack
version: 1.0.0
description: |
  AIW 2.0 Stack — productized agency build pipeline. Walks the student through self-discovery,
  niche scoring, deep niche research via Apify, offer crafting, niche-tailored website factory build,
  and content engine deploy. State-machine driven with hard gates between modules.
  Use when the user wants to run any AIW pipeline step: discovery, score niches, research,
  pick niche, build niche template, craft offer, generate factory brief, tailor factory,
  run factory, deploy engine, walk engine, factory feedback, refine template, status, help.
  Also use when the user says "/aiw-stack", "/start", "/setup", "/discovery", "/score-niches",
  "/research", "/pick-niche", "/build-niche-template", "/craft-offer", "/load-factory-structure",
  "/generate-wf-brief", "/tailor-factory", "/run-factory", "/load-engine-structure",
  "/generate-ce-brief", "/deploy-engine", "/walk-engine", "/factory-feedback",
  "/refine-template", "/status", "/help", or mentions "AIW", "AIW stack", "niche agency".
triggers:
  - start aiw stack
  - run aiw pipeline
  - aiw discovery
  - score niches
  - niche research
  - craft offer
  - website factory
  - content engine
---

# AIW 2.0 Stack

The actual repo lives at:

```
<REPO_ROOT>/AIW2.0STACK/
```

## When this skill activates

1. **Set the working directory** to the repo path above. Every file read, write, and bash command must happen relative to that root, NOT the user's current cwd.
2. **Read `CLAUDE.md`** from the repo root immediately. It is the canonical operating manual: actor model, operator rules, gate chain, 8-module flow, state machine. Treat it as authoritative.
3. **Read `stack-state.json`** from the repo root to determine current state and which gates are open.
4. **Route the user's input** to the matching command file in `.claude/commands/`. If they typed `/start` or just said "start", read and execute `.claude/commands/start.md`. Same for every other command in the map below.

## Command map

| User input | File to execute |
|---|---|
| `/start` or "start" | `.claude/commands/start.md` |
| `/setup` | `.claude/commands/setup.md` |
| `/setup-agency` | `.claude/commands/setup-agency.md` |
| `/discovery` | `.claude/commands/discovery.md` |
| `/score-niches` | `.claude/commands/score-niches.md` |
| `/research` | `.claude/commands/research.md` |
| `/pick-niche` | `.claude/commands/pick-niche.md` |
| `/build-niche-template` | `.claude/commands/build-niche-template.md` |
| `/craft-offer` | `.claude/commands/craft-offer.md` |
| `/load-factory-structure` | `.claude/commands/load-factory-structure.md` |
| `/generate-wf-brief` | `.claude/commands/generate-wf-brief.md` |
| `/tailor-factory` | `.claude/commands/tailor-factory.md` |
| `/run-factory` | `.claude/commands/run-factory.md` |
| `/load-engine-structure` | `.claude/commands/load-engine-structure.md` |
| `/generate-ce-brief` | `.claude/commands/generate-ce-brief.md` |
| `/deploy-engine` | `.claude/commands/deploy-engine.md` |
| `/walk-engine` | `.claude/commands/walk-engine.md` |
| `/factory-feedback` | `.claude/commands/factory-feedback.md` |
| `/refine-template` | `.claude/commands/refine-template.md` |
| `/status` | `.claude/commands/status.md` |
| `/help` | `.claude/commands/help.md` |

## Default greeting (no specific command given)

Behave as `/start`:
1. Read `stack-state.json`.
2. Find the first false gate in the chain.
3. Tell the student: where they are, the next command to run, what that command will do.
4. Wait for them to run it.

## Hard rules (inherited from the repo's CLAUDE.md)

- No em-dashes. Ever.
- No emojis. Ever.
- Plain words, short sentences, calm direct professional tone.
- No buzzwords ("leverage", "synergize", "robust", "seamless", "game-changer", "cutting-edge").
- Match the student's region for slang and currency (USD default, can be GBP/EUR/ZAR/etc).
- Never publish, push, deploy, or send anything without the student's explicit approval.
- Plan first, present, wait, execute.
- One module at a time. Respect the gate chain — refuse to run a command whose prerequisite gate is false.
- If not 100% sure, ask a clarifying question.

## Subfolder boundaries

- Inside `website-factory/`: defer to `website-factory/CLAUDE.md` (its own 13-stage pipeline).
- Inside `content-engine/`: defer to that folder's own CLAUDE.md if present.
- The root only orchestrates handoffs.

## State writes

After every module completes, update `stack-state.json`:
- Flip the relevant gate to `true`.
- Append a history entry with timestamp, command, outcome.
- Save `niche` and `studentName` to the top level when those modules lock.

## The sub-skills

The repo also ships its own skills at `.claude/skills/` (apify-niche-research, brief-compilation, template-capture-and-build, deep-research-synthesis, setup-wizard-toolkit, niche-research-framework). When a command file references a sub-skill by name, read its SKILL.md from the repo's `.claude/skills/<name>/` directory and follow its instructions.
