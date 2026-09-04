# Translation Quality Review

Systematic QC framework for translated content. Use when reviewing, auditing, or scoring translations.

Uses the `stop-slop` skill for AI pattern detection. References the main transcreation skill (SKILL.md) for voice and terminology.

---

## Part 1: Review Dimensions & Scoring

Five dimensions. Each scored 1-10. No rounding, no averaging across dimensions.

| Dimension | Question | 10 looks like | 1 looks like |
|---|---|---|---|
| Accuracy | Same meaning as source? | Every semantic unit preserved. No additions, no omissions. | Meaning distorted or key information missing. |
| Fluency | Reads naturally in target language? | Native speaker for this audience wrote it. | Machine-translation artifacts. Unnatural phrasing. |
| Terminology | Domain terms correct and consistent? | Every domain term uses the established standard. Consistent throughout. | Terms wrong or inconsistent across the file. |
| Voice | Matches the project's voice? | Indistinguishable from content the project would publish. | Wrong register, tone, or violates voice rules. |
| Completeness | Everything translated? | No untranslated strings, no missing segments, all placeholders intact. | Significant gaps, untranslated segments, broken placeholders. |

**Accuracy** - compare source and target segment by segment. Look for semantic shifts, false friends, additions (content in target not in source), and omissions (content in source not in target).

**Fluency** - read the target text without looking at the source. If a sentence makes you pause, it fails. Common failures: calques (source-language syntax leaking into target), over-literal word order, unnatural collocations.

**Terminology** - check every domain term against the do-not-translate list and per-language terminology notes in the transcreation skill (Part 4). Verify consistency: same source term = same target term everywhere in the file.

**Voice** - does the translation sound like the project? Check all voice rules from Part 1 of the transcreation skill. Common failure: AI-generated translations flatten voice into generic corporate neutral.

**Completeness** - structural integrity. Every source key has a target. Every placeholder survives. Every HTML tag is preserved. Common failure: placeholders silently deleted during translation.

### Scoring Bands

| Range | Verdict | Action |
|---|---|---|
| 45-50 | Ship-ready | No changes needed. Minor style preferences don't count against it. |
| 38-44 | Minor issues | Fix flagged items and ship. No structural problems. |
| 30-37 | Significant issues | Revise flagged areas and re-review. Patterns suggest systemic problems. |
| Below 30 | Reject | Retranslate. Fundamental accuracy, fluency, or terminology problems. |

The total is a guide, not a gate. A single CRIT issue at 42/50 still blocks shipping.

---

## Part 2: Issue Classification

Two systems work together: severity and category. Every issue gets both: e.g., "CRIT/TERM" or "MIN/FLUENCY".

### Severity Levels

| Severity | Label | Definition | Action | Example |
|---|---|---|---|---|
| Critical | CRIT | Meaning changed, domain term wrong, placeholder broken, content missing, voice rule violated | Must fix before shipping | Domain term translated when it should stay English; `{{count}}` deleted |
| Major | MAJ | Noticeable quality problem affecting user experience | Should fix before shipping | Wrong register; sentence doesn't parse; key term inconsistent |
| Minor | MIN | Correct but improvable; non-preferred synonym | Fix if convenient; acceptable to ship | Slightly awkward phrasing; word order preference; verbose |
| Style | STY | Voice or style preference, debatable | Note for translator's awareness | Could be shorter; rhythm slightly off |

### Issue Categories

**ACCURACY**
- Mistranslation - target says something different from source
- Addition - content in target not present in source
- Omission - content in source missing from target
- False friend - word that looks similar across languages but means something different
- Semantic shift - subtle meaning drift that changes the implication

**FLUENCY**
- Unnatural phrasing - grammatically correct but no native speaker would write it that way
- Grammar error - subject-verb agreement, case, tense
- Punctuation error - misplaced commas, wrong quotation style for locale. **Exception:** do not flag technically-correct-but-unnecessary punctuation in short UI strings when the string reads naturally without it.
- Spelling error - typos, wrong diacriticals
- Calque - structure borrowed from source language

**TERMINOLOGY**
- Wrong term - incorrect translation of a domain term
- Inconsistent term - same source term translated differently in different locations
- Untranslated term - left in source language when it should be translated
- Over-translated term - translated into target when it should stay in the source language (per do-not-translate list)

**VOICE**
- Wrong register - too formal, too informal, too academic, too casual
- Voice rule violation - any violation of project-specific voice rules (e.g., first-person plural used when forbidden)
- Em dash used - any em dash in any form (if project forbids them)
- AI slop pattern - flag the specific pattern from `stop-slop` (name it)
- Generic flattening - distinctive source voice reduced to corporate neutral

**COMPLETENESS**
- Missing translation - empty target for a source key
- Broken placeholder - placeholder altered, deleted, or malformed
- Broken HTML tag - unclosed tag, deleted tag, reordered nesting
- Untranslated segment - source-language text remaining in target file
- Encoding error - mojibake, wrong character set

---

## Part 3: Review Process

Six steps. Follow in order.

**Single agent vs. subagents:** For small files (under ~100 keys or 5,000 words), one agent runs all six steps sequentially. For large files, the orchestrator handles Steps 1-2 and the file-reading strategy, then each subagent runs Steps 3-5 on its chunk. The orchestrator runs Step 6 on the aggregated results.

### Step 1: Identify the project and load context

Load the transcreation skill for voice definition and terminology. Load `stop-slop`. Read the source locale file as the source of truth.

### Step 2: Classify the content type

Content type determines which dimensions carry the most weight:

| Content type | Primary dimensions | Secondary dimensions |
|---|---|---|
| UI strings | Completeness, Terminology | Fluency (brevity > elegance) |
| Technical descriptions | Accuracy, Terminology | Fluency |
| Glossary definitions | Accuracy, Voice | Fluency |
| FAQ / Guide | Accuracy, Completeness | Voice, Fluency |
| About / Marketing | Voice, Fluency | Accuracy of intent > literal accuracy |

### Reading very long source files

For large i18n files:

1. **Read the file in sections** - use offset/limit reads by namespace prefix. Build a namespace inventory with key counts.
2. **Compare source and target file structure** - identify which namespaces are fully translated, partially translated, or untranslated.
3. **Distribute chunks** - each subagent receives its namespace slice from both source and target files.
4. **Orchestrator assembles** - after subagents return, the orchestrator runs cross-chunk checks.

### Step 3: First pass - structural checks

Mechanical verification before reading for quality:

- [ ] All source keys have corresponding translations (no empty values)
- [ ] All placeholders preserved exactly (character-for-character)
- [ ] All HTML tags preserved and properly nested
- [ ] No source-language text remaining in target (except terms that stay in source language per do-not-translate list)
- [ ] Character encoding correct (no mojibake, no broken diacriticals)
- [ ] Project voice rules not violated in any string

If structural checks fail, log CRIT issues immediately.

### Step 4: Second pass - accuracy and terminology

Read source and target in parallel, segment by segment:

- Does each segment convey the same meaning?
- Are domain terms correctly handled? (kept in source language where required, translated consistently where appropriate)
- Numbers, scores, and formatting preserved?
- Any additions? (Content in target not in source.)
- Any omissions? (Content in source not in target.)

For UI strings: check that source and target have the same number of sentences.

### Step 5: Third pass - fluency and voice

Read the target text ALONE. Do not look at the source. This is the "native reader" pass.

- Does it read naturally? Would a native speaker write it this way?
- Is the register consistent throughout?
- Does it match the project voice?
- **Voice rule check:** Any violations of project-specific voice rules? Flag as CRIT/VOICE.
- For multi-sentence strings, run a stop-slop check. Skip for short UI strings under ~10 words.
- Button labels imperative? Error messages specific?

### Common false positives - do not flag these

- **Target-language capitalization that differs from source.** Spanish, Portuguese, and French do not title-case headings. German capitalizes nouns but not adjectives/verbs. Sentence case is correct in these languages.
- **Missing articles in form labels.** Terse field labels and column headers omit articles in all target languages.
- **Domain terms kept in source language.** Terms on the do-not-translate list staying in the source language is correct, not a completeness issue.
- **Loan words.** Established loan words in the target language are correct.

### Step 6: Score and report

Assign dimension scores based on findings. Compile the issue table. Write summary and recommendation. Use the report format from Part 5.

Scoring guidelines:
- Start at 10 for each dimension. Deduct based on issue count and severity.
- One CRIT issue in a dimension: that dimension cannot score above 5.
- Three or more MAJ issues in a dimension: cap at 6.
- MIN and STY issues reduce scores by 0.5 each, roughly.

---

## Part 4: Content-Type Checklists

### Checklist A: UI Strings

- [ ] All keys have translations (no empty values, no source language left unless intentional)
- [ ] Placeholders preserved exactly
- [ ] HTML tags preserved and properly closed
- [ ] Button labels are imperative verbs
- [ ] Error messages are specific
- [ ] Project voice rules enforced everywhere
- [ ] Consistent terminology within each namespace
- [ ] Consistent terminology across related namespaces
- [ ] No UI string exceeds ~150% of source length
- [ ] Same source term maps to the same target term everywhere (cross-namespace check)
- [ ] Do-not-translate terms kept in source language

### Checklist B: Long-Form / Glossary / FAQ

- [ ] Central argument preserved
- [ ] Rhetorical devices reproduced, not flattened
- [ ] Section structure preserved
- [ ] No hedges or softeners added that aren't in the source
- [ ] No AI slop patterns in multi-sentence strings
- [ ] Project voice rules enforced
- [ ] Links and references still valid
- [ ] Technical descriptions accurate
- [ ] Domain-specific values (amounts, scores) preserved exactly

### Checklist C: About / Marketing Copy

- [ ] Headlines transcreated (not literally translated)
- [ ] CTAs action-oriented and natural in target language
- [ ] Project voice rules enforced (voice violations are most common in marketing)
- [ ] No hype or FUD introduced
- [ ] No domain-inappropriate jargon
- [ ] Voice matches the project personality
- [ ] No AI-generated filler ("in today's world", "it's worth noting")

---

## Part 5: Report Format

Every review produces this structure. No exceptions.

````markdown
## Translation Quality Review

**Project:** [project name]
**Content type:** [UI strings / Glossary / FAQ / About]
**Language pair:** [EN -> DE / EN -> ES / etc.]
**File(s) reviewed:** [path or description]
**Date:** [YYYY-MM-DD]

### Scores

| Dimension | Score | Notes |
|---|---|---|
| Accuracy | X/10 | [One sentence] |
| Fluency | X/10 | [One sentence] |
| Terminology | X/10 | [One sentence] |
| Voice | X/10 | [One sentence] |
| Completeness | X/10 | [One sentence] |
| **Total** | **XX/50** | **[Ship-ready / Minor issues / Significant issues / Reject]** |

### Issues

| # | Severity | Category | Location | Source | Current | Suggested fix | Notes |
|---|---|---|---|---|---|---|---|
| 1 | CRIT | VOICE | key.name | "source text" | "current translation" | "suggested fix" | Explanation |
| 2 | MAJ | TERM | key.name | "source text" | "term A" / "term B" | Pick one, use everywhere | Inconsistent term |

### Patterns

[If 3+ issues share a root cause, name the pattern here. List affected locations.]

### Summary

[2-3 sentences. Overall assessment.]

### Recommendation

**[Ship / Fix and ship / Revise and re-review / Retranslate]**
[One sentence explaining the recommendation.]
````

---

## Part 6: Subagent Strategy for Large Reviews

### Model Recommendations

| Role | Model | Why |
|---|---|---|
| Orchestrator | Opus | Cross-chunk consistency, pattern identification, final scoring |
| QC subagents | Sonnet | Structured comparison against checklists and terminology |

### When to Use Subagents

- UI string files over ~100 keys
- Multiple documents submitted for review at once
- Full-locale translation audits

Do not use subagents for single documents under 5,000 words or string files under ~100 keys.

### How to Chunk

Chunk by namespace prefix. Each namespace or namespace group = one subagent.

### What Each Subagent Receives

1. This QC review framework
2. The transcreation skill's voice definition and terminology
3. The `stop-slop` checklist
4. Their chunk of source + target text - **embedded directly in the subagent prompt as text**
5. A brief: project name, language pair, content type

**Critical: no filesystem handoff.** Embed source and target key-value pairs directly in the subagent's prompt text.

### What Each Subagent Returns

Each subagent returns a scored report for its chunk as **inline text in the final message**, using the exact format from Part 5. No file writes, no filesystem paths.

### Orchestrator Responsibilities

After collecting all subagent reports, the orchestrator:

1. **Aggregates dimension scores** - weighted by chunk size.
2. **Merges issue tables** - all issues into one consolidated table. Renumber sequentially.
3. **Runs cross-chunk consistency check** - verify that the same source term maps to the same target term across ALL namespaces. Flag divergences.
4. **Runs cross-chunk voice check** - verify all project voice rules are enforced everywhere.
5. **Identifies cross-chunk patterns** - AI slop in some chunks but not others points to mixed human/machine translation.
6. **Produces one consolidated report** - single report, single score, single recommendation.
