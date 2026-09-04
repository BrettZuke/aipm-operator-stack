# Transcreation

A skill for translating content with domain precision. Produces translations that preserve meaning, intent, and rhetorical effect - not word-for-word equivalents.

## What this is

Most translation tools optimize for literal accuracy. Transcreation optimizes for the target audience reading the result and having the same reaction as the source audience. This skill teaches Claude (or any LLM) to translate that way - with configurable voice rules, domain terminology, and quality review.

## Skill Structure

```
transcreation/
├── SKILL.md              # Core transcreation skill
├── references/
│   ├── qc-review.md      # Quality review framework (5-dimension scoring)
│   └── workflows.md      # CI workflow templates (GitHub Actions)
├── README.md
├── CHANGELOG.md
└── LICENSE
```

## Quick start

**Claude Code:** Add this folder as a skill.

**Claude Projects:** Upload `SKILL.md` and reference files to project knowledge.

**Custom instructions:** Copy the relevant Parts from `SKILL.md` into your system prompt.

**API calls:** Include `SKILL.md` in your system prompt. Reference files load on demand.

## What it does

**Transcreation skill** (`SKILL.md`) - 5-step translation process with configurable project voice, domain terminology, UI string rules, subagent chunking for large jobs, and delivery checklists.

**QC review** (`references/qc-review.md`) - 5-dimension scored review framework (accuracy, fluency, terminology, voice, completeness). Issue classification by severity and category. Standardized report format.

**CI workflows** (`references/workflows.md`) - GitHub Actions templates for automated translation sync and quality review. Diffs source against targets, translates the delta, validates output, opens PRs, runs QC, posts scored reports as comments.

## Companion skill

This skill uses [stop-slop](https://github.com/hardikpandya/stop-slop) as a final pass to remove AI writing patterns. Install it alongside this skill for best results.

## Configuration

The skill is project-agnostic. Before first use, fill in:

1. **Voice template** (Part 1) - register, audience, person rules, prohibited patterns
2. **Terminology lists** (Part 4) - do-not-translate terms, consistent translation terms, per-language notes
3. **File paths** - source locale path, target locale paths, placeholder syntax

See the Voice Example in Part 1 of `SKILL.md` for a concrete configuration.

## Author

[tobomobo](https://github.com/tobomobo)

## License

MIT
