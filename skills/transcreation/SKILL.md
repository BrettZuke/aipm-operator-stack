---
name: transcreation
description: "Transcreation skill for multilingual content. Produces translations that preserve meaning, intent, and rhetorical effect - not word-for-word equivalents. Applies a project's voice in the target language. Trigger on: translate, transcreate, ins Deutsche, into English, auf Englisch, auf Deutsch, i18n, localize, sync translations."
metadata:
  trigger: Translating content between languages, localizing UI strings, syncing i18n files
  author: tobomobo
---

# Transcreation

Translate content with domain precision. This skill handles UI strings, FAQ text, glossary definitions, marketing copy, and technical documentation. Every translation must be terminologically exact, tonally correct, and free of slop.

Uses the `stop-slop` skill for AI writing pattern removal.

See [references/qc-review.md](references/qc-review.md) for the quality review framework. See [references/workflows.md](references/workflows.md) for CI automation templates.

---

## Part 1: Voice Configuration

Define the project voice before translating. Every project needs these decisions made upfront.

### Voice Template

Fill this out per project. The answers constrain every translation decision.

```
Project: [name]
Register: [Technical / Conversational / Formal / Marketing]
Audience: [Who reads this? What do they already know?]
Person: [First-person plural allowed? Third-person? Passive?]
Punctuation: [Em dashes? Exclamation marks? Oxford comma?]
Tone gradient: [How does register shift across content types?]
```

### Register by Content Type

| Content type | Register |
|---|---|
| UI strings (buttons, labels, scores) | Neutral, functional. Zero decoration. |
| Technical descriptions | Technical, specific. Name mechanisms and what they reveal. |
| Remediation / action items | Direct and actionable. Tell the user what to do. |
| Glossary definitions | Educational, concise. Explain once, with precision. |
| FAQ answers | Conversational but factual. Respect the reader's intelligence. |
| About / marketing | More expressive, but never breathless. Substance over excitement. |

### Prohibited Patterns (defaults)

These apply unless the project voice explicitly overrides them:

- Vague buzzwords: "seamlessly", "bulletproof", "military-grade", "cutting-edge"
- False urgency: "Act now!", "Don't miss out!", "Time is running out!"
- Exclamation marks in UI strings
- Em dashes (use ` - ` instead)
- AI slop patterns (see `stop-slop` skill)

### Voice Example

Here is how a specific project might fill in the template:

```
Project: am-i.exposed
Register: Technical privacy tool. Direct over diplomatic. Precise over warm.
Audience: Bitcoin users who understand transactions, addresses, UTXOs.
Person: Never "we/us/our". Use passive voice or refer to tool by name.
Punctuation: No em dashes. No exclamation marks in UI.
```

---

## Part 2: Translation Process

Five steps. Every translation goes through all five. No shortcuts.

### Step 0: Classify content type

Before writing a single word, classify the source:

- **(a) UI strings** - key-value pairs in i18n files (JSON, YAML, XLIFF, etc.)
- **(b) Technical descriptions** - feature explanations, process descriptions
- **(c) Glossary definitions** - educational content, term definitions
- **(d) Guide / FAQ content** - help pages, frequently asked questions, methodology
- **(e) About / marketing** - landing pages, feature descriptions, promotional content

Classification determines which rules dominate. UI strings prioritize brevity and consistency. Glossary entries prioritize clarity. About/marketing prioritizes natural flow.

### Step 0b: Determine translation scope

Before translating, determine whether this is a **full translation** (new locale, empty target file) or a **partial update** (target file exists with some translations). For partial updates, diff the source against the target to classify every key:

| State | How to detect | Action |
|---|---|---|
| **New** | Key exists in source but not in target | Translate. Primary task for partial updates. |
| **Changed** | Key exists in both, but source value differs from what was originally translated | Re-translate. The source text changed. |
| **Unchanged** | Key exists in both, source value matches what was translated | Keep the existing translation. Do not re-translate. |
| **Orphaned** | Key exists in target but not in source | Flag for removal. Report to user - the key may have been renamed. |

**How to diff for UI strings:**

1. Read the source locale file - this is the canonical key list.
2. Read the target locale file.
3. Build three lists: keys in source but not target (new), keys in target but not source (orphaned), and keys in both (existing).
4. For the "existing" set: compare source values to infer whether the source changed. If unsure, keep the existing translation and flag it for review rather than re-translating blindly.

**Subagent implications:** When spawning subagents for a partial update, each subagent's prompt should clearly state which keys to translate (new), which to re-translate (changed), and which existing translations to use as consistency context (unchanged). Do not send unchanged keys as part of the translation task - include them as read-only reference.

### Step 1: Understand before writing

**For UI strings (small batch, under ~100 keys):** Read all source keys and their existing target translations before writing anything. For larger batches, this step happens per-chunk inside each subagent - see Part 6.

**For UI strings:** Read the namespaced key. `finding.H1_title` tells you this is a finding title for item H1. `settings.theme_label` is a settings label. That context determines register, length, and grammar.

**For long-form content:** Read the entire source. Identify the argument structure, the rhetorical devices, the intended emotional arc. Mark section boundaries and key claims.

### Step 2: Extract intent

**For UI strings:** State in one phrase what the user learns or does. "Address Reuse Detected" = the tool found a repeated pattern. "Export Results" = the user downloads data.

**For long-form content:** State the core argument in one sentence. Identify what the reader should think, feel, or do after reading. Note any rhetorical devices worth preserving.

### Step 3: Write in target language

**For UI strings:** Match the source's brevity and register. If the source is three words, aim for three words. If the target language needs five, use five, but never pad. Translate the intent, not the syntax.

**For long-form content:** Write as if composing from scratch in the target language. A native reader should not detect translation. Preserve argument structure and rhetorical devices, but rebuild sentences to sound natural.

### Step 4: Stop-slop pass

**When to apply:** Long-form content (glossary definitions, FAQ answers, about page, guide sections) and multi-sentence UI strings. Skip for short UI strings - labels, buttons, headings, scores, and any string under ~10 words.

**How to invoke:** The orchestrator and single-agent translations should invoke the `stop-slop` skill via the Skill tool for the final assembled output. Subagents apply the checklist manually (they cannot invoke skills).

Check for:
- Connective tissue added during translation ("in this regard", "it should be noted")
- Parallel structures that crept in from the source language
- Passive voice where the source used active (note: passive may be appropriate depending on project voice rules)
- Hedges and softeners absent from the source ("perhaps", "might", "it seems")
- Filler adverbs ("basically", "essentially", the target-language equivalents)
- Any word in the translation that has no corresponding word or intent in the source
- Project-specific voice violations (check Part 1 voice configuration)

---

## Part 3: UI String Rules

These rules apply to all translations of i18n key-value files (JSON, YAML, XLIFF, etc.).

**1. Consult the source of truth.** Before translating any UI term, read the source locale file for the established wording.

**2. Check existing translations.** Before writing, read the target locale file. If the term has been translated before, match it. Consistency across the app is non-negotiable.

**3. Brevity is mandatory.** UI labels occupy fixed space. If the target language runs longer than the source, abbreviate. Never add words absent from the source.

**4. Preserve placeholders exactly.** Never translate text inside placeholder delimiters. `{{count}}` stays `{{count}}`. `{name}` stays `{name}`. `%s` stays `%s`. Identify the project's placeholder syntax and preserve it character-for-character.

Common placeholder formats:
- i18next: `{{variable}}`
- ICU MessageFormat: `{variable}`
- printf-style: `%s`, `%d`, `%1$s`
- Ruby/Python: `%{variable}`

**5. Preserve HTML/markup tags exactly.** `<span>`, `<b>`, `<br/>`, `<1>`, `<0>` stay as-is. Translate only the text content between tags. Never reorder tags.

**6. One source term = one target term, everywhere.** The same concept gets the same translation within a locale. Never use different terms for the same concept in different screens. Refer to the project's terminology list.

**7. Use namespaced keys for context.** The key hierarchy tells you the UI element type, which determines grammar and register.

**8. Button labels use imperative verbs.** "Scan" = "Scannen" (DE), not "Scan-Vorgang". "Export" = "Exportieren", not "Der Export".

**9. Error messages: specific, not generic.** If the source says "Invalid address for this network", translate the specific error.

**10. Length ceiling: ~150% of source.** If the source string is 20 characters, the target should not exceed 30. German compounds may push this. Use judgment, but flag anything that doubles the source length.

**11. Don't add pedantic punctuation.** UI strings prioritize natural flow over grammar-book correctness.

**12. Capitalization follows target-language rules.** English title-cases headings; most other languages do not. Spanish and Portuguese capitalize only the first word. German capitalizes nouns but not adjectives/verbs. French capitalizes only the first word.

**13. Enforce project voice rules.** If the source violates the project voice (e.g., uses first-person plural when the project forbids it), fix it in translation.

---

## Part 4: Domain Terminology

Every project needs two terminology lists. Fill these out before starting any translation work.

### Do-Not-Translate Terms

Terms that stay in the source language in all targets. Typically: brand names, technical standards, protocol names, widely-adopted loan terms.

```
List your do-not-translate terms here, e.g.:
> Bitcoin, UTXO, API, OAuth, GraphQL, Kubernetes, Docker
```

### Terms That Must Be Translated Consistently

| Source term | Context | Notes |
|---|---|---|
| [term] | [where it appears] | [each language has one translation, used everywhere] |
| [term] | [where it appears] | [may keep as loan word in some languages] |

### Per-Language Notes

**German (de):**
- Sie-form vs. du-form: check existing translations for convention
- Compound words: German compounds can grow long; balance accuracy with readability
- Keep established technical loan words ("Cluster", "Server", "App")
- "Transaktion" not "Überweisung" (implies bank transfer)

**Spanish (es):**
- Latin American vs. Peninsular: check existing translations for convention
- Keep loan words where natural in the domain
- Formal usted vs. informal tú: match existing convention

**Portuguese (pt):**
- Brazilian vs. European: check existing translations for convention
- Similar loan word patterns to Spanish

**French (fr):**
- Formal vous register (default for tools/products)
- French typography: non-breaking space before `:`, `?`, `!`, `;`
- L'Académie française preferences vs. common usage: prefer what users actually write

**Japanese (ja):**
- Katakana for established loan words
- Honorific level: match existing convention (usually desu/masu)
- UI strings often shorter than English - leverage this

**Chinese (zh):**
- Simplified vs. Traditional: confirm which variant
- No spaces between characters (except around Latin text/numbers)

Add per-language notes for any target language the project supports.

---

## Part 5: Long-Form Content

For glossary definitions, FAQ answers, guide sections, and about page copy, apply the full transcreation process (Steps 0-4). Do not line-translate.

### Voice in Long-Form

Long-form content communicates three things:
1. **Education.** Explain what the system does and how.
2. **Actionability.** Tell the user what to do about it.
3. **Empowerment.** The user can accomplish what they came to do. Specific techniques work.

No FUD. No hype. State what the tool does. Let the reader evaluate.

### Rhetorical Devices Worth Preserving

| Device | Example | Handling |
|---|---|---|
| Specific reference codes | "H3: Round Amount Detection" | Keep the code. Translate the name. |
| Numeric context | "A score below 40 indicates..." | Keep the number. Adapt formatting to locale. |
| Product name reference | "[Product] detects this pattern" | Keep product name. Never translate brand names. |
| Concrete example | "If you send exactly 0.1 BTC..." | Translate the framing. Keep domain-specific values. |

---

## Part 6: Subagent Strategy

For large translation jobs, split work across subagents. Each subagent operates independently but follows the same rules.

### Model Recommendations

| Role | Model | Why |
|---|---|---|
| Orchestrator | Opus | Judgment calls, cross-chunk consistency, assembly |
| UI string subagents | Sonnet | Formulaic strings, well-constrained by terminology |
| Long-form subagents | Opus | Creative language work, voice preservation |

### When to Use Subagents

**UI strings - full translation:** Always use subagents for files over ~500 keys. A single agent can handle one namespace of up to ~500 keys.

**UI strings - partial update:** Run the Step 0b diff first. If the total number of new + changed keys is under ~100, a single agent is fine. If the delta exceeds ~100 keys or spans 3+ namespaces, use subagents.

**Ad-hoc batches** under ~100 keys: a single agent is fine regardless of scope.

### Reading Very Long Source Files

Before chunking, the orchestrator must scan the full source file and the full target file. For large files:

1. **Read the file in sections** - use offset/limit reads by namespace prefix.
2. **Build a namespace inventory** - list every top-level namespace prefix and its key count.
3. **Scan existing target translations** - read the target locale file. Run the Step 0b diff.
4. **Write the consistency brief** - using the inventory and a sample of keys from each namespace.

### How to Chunk

Chunk by key namespace prefix. Group related namespaces to keep context together. Each chunk should be 100-500 keys.

### What Every Subagent Receives

1. This skill's rules (embed the relevant Parts - typically Parts 1-4 and the delivery checklist)
2. The stop-slop checklist from Step 4 (subagents apply it manually)
3. The consistency brief (see template below)
4. Their assigned chunk - source keys and any existing target translations, **embedded directly in the subagent prompt as text**

**Critical: no filesystem handoff.** Subagents cannot access `/tmp/` or other temporary directories. Embed the source keys and any existing target translations directly in the subagent's prompt text.

### Subagent Output Contract

Every subagent must return its translation as **inline JSON in the final message text**. No file writes. No filesystem paths. The orchestrator parses the returned text directly.

Format: a JSON object where keys are the source file keys and values are the translated strings.

```json
{
  "finding.H1_title": "Adresswiederverwendung erkannt",
  "finding.H1_desc": "Diese Adresse wurde in mehreren Transaktionen verwendet"
}
```

The orchestrator should strip code fences defensively when parsing.

### Consistency Brief Template

Write this before spawning any subagent. Every subagent gets the same brief.

```
## Consistency Brief
**Direction:** [EN->DE / EN->ES / etc.]
**Target locale:** [locale code]
**Content type:** [UI strings / Glossary / Guide / About]
**Audience:** [from Part 1 voice config]
**Terminology decisions:** [List any ambiguous terms and the chosen translation]
  - "[term]" -> [chosen translation]
  - "[term]" -> [chosen translation]
**Voice note:** [Key voice constraints from Part 1]
**Do not:**
  - Do not translate terms from the do-not-translate list
  - Do not add explanatory text absent from source
  - [Project-specific prohibitions]
```

### Error Recovery

- **Malformed JSON:** Strip code fences and retry parse. One retry. If it fails again, the orchestrator translates that chunk directly.
- **Missing keys:** Diff the returned keys against the assigned chunk. Re-prompt with just the missing keys.
- **Terminology inconsistency across chunks:** The orchestrator fixes these during recombination.
- **Truncated output:** Re-prompt: "Your output was truncated. Continue from the last complete key-value pair."

### Recombination

After all subagents return:

1. Assemble chunks in source order
2. Review joins between chunks - no register shifts
3. Cross-chunk terminology check: same source term must map to same target term everywhere
4. Final stop-slop pass on long-form content and multi-sentence strings - invoke the `stop-slop` skill via the Skill tool
5. Spot-check five random strings against the consistency brief
6. Verify project voice rules are respected in every string

---

## Part 7: Delivery Checklist

Run every item. No exceptions.

### Single-agent translations

- [ ] Read the full source before writing anything
- [ ] Can state the intent of each string/section in one sentence
- [ ] Reproduced rhetorical devices, not just words
- [ ] Rhythm is natural in the target language
- [ ] Translation matches the project's voice
- [ ] Stop-slop pass complete on multi-sentence strings and long-form content
- [ ] Project voice rules enforced (check Part 1)
- [ ] No em dashes anywhere (unless project allows them)

### Additional for UI strings

- [ ] Consulted source locale file for established wording
- [ ] Checked existing translations in target locale file for consistency
- [ ] All placeholders preserved exactly as-is
- [ ] All HTML/markup tags preserved exactly
- [ ] Domain terms handled per do-not-translate list
- [ ] No UI string introduces words absent from the source
- [ ] No string exceeds ~150% of source character length
- [ ] Button labels use imperative verbs in target language
- [ ] Namespaced key context was used to determine register and grammar

### Additional for subagent translations

- [ ] Consistency brief written and reviewed before spawning subagents
- [ ] Every subagent received the brief, this skill's rules, and the stop-slop checklist
- [ ] Each subagent applied stop-slop to multi-sentence strings in its chunk
- [ ] Joins between chunks reviewed
- [ ] Final stop-slop pass across long-form content and multi-sentence strings
- [ ] Terminology consistent across all chunks
- [ ] Five random strings spot-checked against consistency brief
- [ ] Project voice rules respected in every chunk
