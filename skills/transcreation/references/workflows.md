# CI Workflow Templates

GitHub Actions workflows for automating transcreation and quality review. Both use `anthropics/claude-code-action` with OAuth token auth.

These are templates. Adapt paths, locale lists, and file patterns to your project.

---

## Transcreation Workflow

Diffs source locale against all target locales, finds missing and stale keys, translates the delta, validates output, and opens a PR.

### Trigger

- Weekly schedule (Monday 06:00 UTC)
- Manual dispatch with locale filter and dry-run option

### Jobs

1. **diff** - Detects missing and stale translations by comparing source and target locale files. Uses git history to find stale keys (source text changed since last translation commit).
2. **translate** - Builds a prompt from the diff results and runs the transcreation skill via `claude-code-action`. Validates JSON output and placeholder integrity.
3. **create-pr** - Commits changes and opens a PR with a summary of what was translated.

### Template

```yaml
name: Transcreation

on:
  schedule:
    - cron: '0 6 * * 1'
  workflow_dispatch:
    inputs:
      locale:
        description: 'Target locale (blank = all missing)'
        type: choice
        options:
          - all
          # Add your locales here
          - de
          - es
          - fr
        default: all
      dry_run:
        description: 'Dry run - diff only, no PR'
        type: boolean
        default: false

concurrency:
  group: transcreation
  cancel-in-progress: false

permissions:
  contents: write
  pull-requests: write
  issues: write

jobs:
  diff:
    name: Detect missing and stale translations
    runs-on: ubuntu-latest
    outputs:
      has_work: ${{ steps.diff.outputs.has_work }}
      summary: ${{ steps.diff.outputs.summary }}
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Diff locales against source
        id: diff
        run: |
          python3 << 'PYEOF'
          import json, os, subprocess

          # ---- CONFIGURE THESE ----
          source_path = "public/locales/en/common.json"  # Path to source locale
          locale_dir = "public/locales"                    # Parent directory of locale folders
          locale_file = "common.json"                      # Filename within each locale folder
          all_locales = ["de", "es", "fr"]                 # Target locales
          # --------------------------

          locale_filter = os.environ.get("LOCALE_FILTER", "all")
          locales = all_locales if locale_filter == "all" else [locale_filter]

          source = json.load(open(source_path))
          source_keys = set(source.keys())

          def get_source_at_last_sync(lang):
              """Get source values at the time the locale was last translated."""
              target_path = f"{locale_dir}/{lang}/{locale_file}"
              try:
                  result = subprocess.run(
                      ["git", "log", "-1", "--format=%H", "--", target_path],
                      capture_output=True, text=True, check=True
                  )
                  last_sync_sha = result.stdout.strip()
                  if not last_sync_sha:
                      return None
                  result = subprocess.run(
                      ["git", "show", f"{last_sync_sha}:{source_path}"],
                      capture_output=True, text=True, check=True
                  )
                  return json.loads(result.stdout)
              except (subprocess.CalledProcessError, json.JSONDecodeError):
                  return None

          total_work = 0
          summary_lines = []
          diff_details = {}

          for lang in locales:
              path = f"{locale_dir}/{lang}/{locale_file}"
              if not os.path.exists(path):
                  summary_lines.append(f"{lang}: new locale (all {len(source_keys)} keys)")
                  total_work += len(source_keys)
                  diff_details[lang] = {"new": list(source_keys), "stale": [], "orphaned": []}
                  continue

              target = json.load(open(path))
              target_keys = set(target.keys())

              missing = sorted(source_keys - target_keys)
              orphaned = sorted(target_keys - source_keys)

              stale = []
              source_at_sync = get_source_at_last_sync(lang)
              if source_at_sync:
                  for key in sorted(source_keys & target_keys):
                      old_val = source_at_sync.get(key)
                      new_val = source.get(key)
                      if old_val is not None and old_val != new_val:
                          stale.append(key)

              parts = []
              if missing:
                  parts.append(f"{len(missing)} missing")
              if stale:
                  parts.append(f"{len(stale)} stale")
              if orphaned:
                  parts.append(f"{len(orphaned)} orphaned")
              if not parts:
                  parts.append("up to date")

              summary_lines.append(f"{lang}: {', '.join(parts)}")
              total_work += len(missing) + len(stale)
              diff_details[lang] = {"new": missing, "stale": stale, "orphaned": orphaned}

          summary = "; ".join(summary_lines)
          has_work = "true" if total_work > 0 else "false"

          with open("/tmp/i18n-diff.json", "w") as f:
              json.dump(diff_details, f, indent=2)

          with open(os.environ["GITHUB_OUTPUT"], "a") as f:
              f.write(f"has_work={has_work}\n")
              f.write(f"summary={summary}\n")

          print(f"has_work={has_work}")
          print(f"summary={summary}")
          PYEOF
        env:
          LOCALE_FILTER: ${{ inputs.locale || 'all' }}

      - name: Upload diff details
        if: steps.diff.outputs.has_work == 'true'
        uses: actions/upload-artifact@v4
        with:
          name: i18n-diff
          path: /tmp/i18n-diff.json
          retention-days: 1

  translate:
    name: Translate missing keys
    runs-on: ubuntu-latest
    needs: diff
    if: needs.diff.outputs.has_work == 'true' && inputs.dry_run != true
    steps:
      - uses: actions/checkout@v4

      - name: Download diff details
        uses: actions/download-artifact@v4
        with:
          name: i18n-diff
          path: /tmp/

      - name: Build translation prompt
        id: prompt
        run: |
          python3 << 'PYEOF'
          import json, os

          # ---- CONFIGURE THESE ----
          source_path = "public/locales/en/common.json"
          locale_dir = "public/locales"
          locale_file = "common.json"
          skill_name = "transcreation"  # Name of your transcreation skill
          # --------------------------

          diff = json.load(open("/tmp/i18n-diff.json"))
          source = json.load(open(source_path))

          sections = []
          for lang, d in diff.items():
              if not d["new"] and not d["stale"]:
                  continue

              parts = []
              if d["new"]:
                  keys_with_values = {k: source[k] for k in d["new"]}
                  parts.append(f"NEW KEYS to translate ({len(d['new'])}):\n{json.dumps(keys_with_values, indent=2, ensure_ascii=False)}")
              if d["stale"]:
                  keys_with_values = {k: source[k] for k in d["stale"]}
                  parts.append(f"STALE KEYS to re-translate ({len(d['stale'])}):\n{json.dumps(keys_with_values, indent=2, ensure_ascii=False)}")
              if d["orphaned"]:
                  parts.append(f"ORPHANED KEYS (flag only, do not delete): {d['orphaned']}")

              sections.append(f"### Locale: {lang}\nTarget file: {locale_dir}/{lang}/{locale_file}\n\n" + "\n\n".join(parts))

          prompt = f"Use the {skill_name} skill.\n\n"
          prompt += "The diff has already been computed. Translate ONLY the keys listed below - do not re-translate unchanged keys.\n\n"
          prompt += "For NEW keys: add translations to the target locale file.\n"
          prompt += "For STALE keys: replace the existing translation with a fresh one (the source text changed).\n"
          prompt += "For ORPHANED keys: do not delete them. Note them in your output.\n\n"
          prompt += "Read each target locale file first to maintain consistency with existing translations.\n"
          prompt += "Write updated JSON files back to their locale paths.\n"
          prompt += "Follow all skill rules: preserve placeholders, match brevity.\n\n"
          prompt += "\n\n".join(sections)

          with open(os.environ["GITHUB_OUTPUT"], "a") as f:
              f.write("prompt<<PROMPT_EOF\n")
              f.write(prompt)
              f.write("\nPROMPT_EOF\n")
          PYEOF

      - name: Translate keys
        uses: anthropics/claude-code-action@v1
        timeout-minutes: 30
        with:
          claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
          prompt: ${{ steps.prompt.outputs.prompt }}
          claude_args: |
            --allowedTools "Edit,Write,Read,Glob,Grep"

      - name: Validate JSON output
        run: |
          # ---- CONFIGURE THIS ----
          LOCALE_DIR="public/locales"
          SOURCE_FILE="$LOCALE_DIR/en/common.json"
          LOCALES="de es fr"
          # --------------------------

          ERRORS=0
          for f in "$LOCALE_DIR"/*/common.json; do
            if ! python3 -c "import json; json.load(open('$f'))"; then
              echo "::error::Invalid JSON: $f"
              ERRORS=$((ERRORS + 1))
            fi
          done

          python3 << PYEOF
          import json, sys
          source = json.load(open("$SOURCE_FILE"))
          source_count = len(source)
          for lang in "$LOCALES".split():
              path = f"$LOCALE_DIR/{lang}/common.json"
              try:
                  target = json.load(open(path))
              except (FileNotFoundError, json.JSONDecodeError):
                  continue
              if len(target) < source_count * 0.9:
                  print(f"::error::{lang} has {len(target)} keys, source has {source_count} - possible key loss")
                  sys.exit(1)

              # Placeholder integrity check (i18next double-brace syntax)
              for key in target:
                  if key in source:
                      src_vars = {v.split("}}")[0] for v in source[key].split("{{")[1:] if "}}" in v}
                      tgt_vars = {v.split("}}")[0] for v in target[key].split("{{")[1:] if "}}" in v}
                      if src_vars != tgt_vars:
                          print(f"::warning::Placeholder mismatch in {lang}/{key}: source has {src_vars}, target has {tgt_vars}")
          PYEOF

          if [ "$ERRORS" -gt 0 ]; then
            echo "::error::JSON validation failed"
            exit 1
          fi

      - name: Check for changes
        id: changes
        run: |
          # ---- CONFIGURE THIS ----
          LOCALE_DIR="public/locales"
          # --------------------------
          if git diff --quiet "$LOCALE_DIR/"; then
            echo "changed=false" >> "$GITHUB_OUTPUT"
          else
            echo "changed=true" >> "$GITHUB_OUTPUT"
          fi

      - name: Create PR
        if: steps.changes.outputs.changed == 'true'
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          DIFF_SUMMARY: ${{ needs.diff.outputs.summary }}
        run: |
          BRANCH="i18n/sync-translations-$(date +%Y%m%d-%H%M)"
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git checkout -b "$BRANCH"
          git add public/locales/
          git commit -m "$(cat <<EOF
          i18n: sync translations

          ${DIFF_SUMMARY}

          Generated by transcreation skill.
          EOF
          )"
          git push -u origin "$BRANCH"

          cat > /tmp/pr-body.md << 'BODY_EOF'
          ## Summary

          Automated translation sync using the transcreation Claude Code skill.

          BODY_EOF

          printf '**Diff:** %s\n\n' "$DIFF_SUMMARY" >> /tmp/pr-body.md

          cat >> /tmp/pr-body.md << 'BODY_EOF'
          ## What was done

          - Diffed source locale against all target locales
          - Translated new keys (added to source since last sync)
          - Re-translated stale keys (source text changed since last sync)
          - Unchanged translations were not modified
          - Orphaned keys (removed from source) were left in place for manual review

          ## Review checklist

          The translation-qc workflow runs on this PR and posts a scored review.

          - [ ] QC workflow passed (check PR comments)
          - [ ] Spot-check 5 random strings per locale
          - [ ] Project voice rules enforced
          - [ ] All placeholders preserved
          - [ ] Orphaned keys reviewed (remove or remap as needed)
          BODY_EOF

          gh pr create \
            --title "i18n: sync translations" \
            --body-file /tmp/pr-body.md \
            --label "i18n"
```

---

## Translation QC Workflow

Triggers on PRs that touch locale files. Detects changed locales, runs a scoped QC review per locale in parallel, and posts a scored report as a PR comment.

### Trigger

- PRs that modify locale files
- Manual dispatch with PR number

### Jobs

1. **detect** - Finds which locale files changed in the PR.
2. **review** - Matrix job: one QC review per changed locale, using `claude-code-action` with the qc-review skill.
3. **comment** - Collects all review reports and posts them as a single PR comment (updates existing comment on re-run).

### Template

```yaml
name: Translation QC

on:
  pull_request:
    paths:
      # ---- CONFIGURE THIS ----
      - 'public/locales/*/common.json'
      # --------------------------
  workflow_dispatch:
    inputs:
      pr_number:
        description: 'PR number to review'
        type: number
        required: true

concurrency:
  group: translation-qc-${{ github.event.pull_request.number || inputs.pr_number }}
  cancel-in-progress: true

permissions:
  contents: read
  pull-requests: write
  issues: write

jobs:
  detect:
    name: Detect changed locales
    runs-on: ubuntu-latest
    outputs:
      locales: ${{ steps.detect.outputs.locales }}
      has_changes: ${{ steps.detect.outputs.has_changes }}
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Determine PR ref
        id: pr
        run: |
          if [ "${{ github.event_name }}" = "workflow_dispatch" ]; then
            echo "ref=${{ inputs.pr_number }}" >> "$GITHUB_OUTPUT"
          else
            echo "ref=${{ github.event.pull_request.number }}" >> "$GITHUB_OUTPUT"
          fi

      - name: Detect changed locale files
        id: detect
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          # ---- CONFIGURE THIS ----
          LOCALE_PATTERN='^public/locales/.*/common.json$'
          SOURCE_LOCALE='en'
          # --------------------------

          FILES=$(gh pr diff "${{ steps.pr.outputs.ref }}" --name-only | grep "$LOCALE_PATTERN" || true)

          if [ -z "$FILES" ]; then
            echo "has_changes=false" >> "$GITHUB_OUTPUT"
            echo "locales=[]" >> "$GITHUB_OUTPUT"
            exit 0
          fi

          LOCALES=$(echo "$FILES" | sed 's|public/locales/\(.*\)/common.json|\1|' | sort -u | grep -v "^${SOURCE_LOCALE}$" || true)

          if [ -z "$LOCALES" ]; then
            echo "has_changes=false" >> "$GITHUB_OUTPUT"
            echo "locales=[]" >> "$GITHUB_OUTPUT"
            exit 0
          fi

          JSON=$(echo "$LOCALES" | jq -R . | jq -s -c .)
          echo "locales=$JSON" >> "$GITHUB_OUTPUT"
          echo "has_changes=true" >> "$GITHUB_OUTPUT"

  review:
    name: QC review (${{ matrix.locale }})
    runs-on: ubuntu-latest
    needs: detect
    if: needs.detect.outputs.has_changes == 'true'
    strategy:
      matrix:
        locale: ${{ fromJson(needs.detect.outputs.locales) }}
      fail-fast: false
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.head.sha || github.sha }}
          fetch-depth: 0

      - name: Extract changed keys for this locale
        id: scope
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          PR_NUM="${{ github.event.pull_request.number || inputs.pr_number }}"
          LOCALE="${{ matrix.locale }}"
          # ---- CONFIGURE THIS ----
          TARGET="public/locales/${LOCALE}/common.json"
          # --------------------------

          CHANGED_KEYS=$(gh pr diff "$PR_NUM" -- "$TARGET" \
            | grep '^+' | grep -v '^+++' \
            | sed -n 's/^+[[:space:]]*"\([^"]*\)".*/\1/p' \
            | sort -u)

          KEY_COUNT=$(echo "$CHANGED_KEYS" | grep -c . || true)

          if [ "$KEY_COUNT" -gt 200 ]; then
            echo "scope=full" >> "$GITHUB_OUTPUT"
            echo "scope_note=Large change ($KEY_COUNT keys). Review the full file." >> "$GITHUB_OUTPUT"
          elif [ "$KEY_COUNT" -gt 0 ]; then
            KEYS_CSV=$(echo "$CHANGED_KEYS" | tr '\n' ', ' | sed 's/,$//')
            echo "scope=scoped" >> "$GITHUB_OUTPUT"
            echo "scope_note=Review ONLY these changed keys (not the full file): ${KEYS_CSV}" >> "$GITHUB_OUTPUT"
          else
            echo "scope=none" >> "$GITHUB_OUTPUT"
          fi

      - name: Run QC review
        if: steps.scope.outputs.scope != 'none'
        uses: anthropics/claude-code-action@v1
        timeout-minutes: 20
        with:
          claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
          prompt: |
            Use the qc-review skill. Review the ${{ matrix.locale }} translation at public/locales/${{ matrix.locale }}/common.json against the source at public/locales/en/common.json. Language pair: EN -> ${{ matrix.locale }}. Content type: UI strings.

            ${{ steps.scope.outputs.scope_note }}

            Produce the full scored report in the exact format specified by the skill. Focus on: accuracy, fluency, terminology consistency, voice, and completeness (all placeholders preserved).

            Write the report to /tmp/qc-report-${{ matrix.locale }}.md. Output only the report, no other commentary.
          claude_args: |
            --allowedTools "Read,Glob,Grep,Write"

      - name: Upload review report
        if: steps.scope.outputs.scope != 'none'
        uses: actions/upload-artifact@v4
        with:
          name: qc-report-${{ matrix.locale }}
          path: /tmp/qc-report-${{ matrix.locale }}.md
          retention-days: 30

  comment:
    name: Post QC results
    runs-on: ubuntu-latest
    needs: [detect, review]
    if: always() && needs.detect.outputs.has_changes == 'true' && needs.review.result != 'skipped'
    steps:
      - name: Download all review reports
        uses: actions/download-artifact@v4
        with:
          pattern: qc-report-*
          path: /tmp/reports/
          merge-multiple: false
        continue-on-error: true

      - name: Check for reports
        id: check
        run: |
          if find /tmp/reports -name '*.md' 2>/dev/null | grep -q .; then
            echo "has_reports=true" >> "$GITHUB_OUTPUT"
          else
            echo "has_reports=false" >> "$GITHUB_OUTPUT"
          fi

      - name: Determine PR number
        if: steps.check.outputs.has_reports == 'true'
        id: pr
        run: |
          if [ "${{ github.event_name }}" = "workflow_dispatch" ]; then
            echo "number=${{ inputs.pr_number }}" >> "$GITHUB_OUTPUT"
          else
            echo "number=${{ github.event.pull_request.number }}" >> "$GITHUB_OUTPUT"
          fi

      - name: Assemble and post comment
        if: steps.check.outputs.has_reports == 'true'
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          PR_NUMBER="${{ steps.pr.outputs.number }}"

          {
            echo "## Translation QC Report"
            echo ""
            echo "Automated quality review using the \`qc-review\` Claude Code skill."
            echo ""

            for report in /tmp/reports/qc-report-*/qc-report-*.md; do
              if [ -f "$report" ]; then
                LOCALE=$(basename "$report" .md | sed 's/qc-report-//')
                echo "---"
                echo ""
                echo "### Locale: \`$LOCALE\`"
                echo ""
                cat "$report"
                echo ""
              fi
            done

            echo "---"
            echo ""
            echo "*Generated with [Claude Code](https://claude.ai/code) using \`qc-review\` skill.*"
          } > /tmp/combined-report.md

          # Update existing comment or create new one
          EXISTING=$(gh api "repos/${{ github.repository }}/issues/${PR_NUMBER}/comments" \
            --jq '.[] | select(.body | startswith("## Translation QC Report")) | .id' \
            | head -1)

          if [ -n "$EXISTING" ]; then
            gh api "repos/${{ github.repository }}/issues/comments/${EXISTING}" \
              -X PATCH \
              -F body=@/tmp/combined-report.md
          else
            gh pr comment "$PR_NUMBER" --body-file /tmp/combined-report.md
          fi
```

---

## Setup

1. Rename the workflow files from `.yml.example` to `.yml` (or copy the templates above).
2. Add the `CLAUDE_CODE_OAUTH_TOKEN` secret to your repository.
3. Adjust the `CONFIGURE THESE` sections to match your project's locale file paths and structure.
4. Ensure your transcreation and qc-review skills are discoverable by Claude Code (symlinked into `.claude/skills/` or installed as dependencies).

### Security Notes

- The diff summary is passed through an environment variable (not `${{ }}` interpolation) to prevent shell/Python injection via commit messages or key names.
- The `CLAUDE_CODE_OAUTH_TOKEN` is used for Claude Code API access, not for git operations. Git operations use the default `GITHUB_TOKEN`.
