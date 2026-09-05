#!/usr/bin/env bash
# Optional: install Anthropic's own skills from Anthropic's public repository.
#
# These are NOT part of this repo and are NOT redistributed by it. They are
# Anthropic's proprietary materials, published by Anthropic at
# https://github.com/anthropics/skills, and their use is governed by your own
# agreement with Anthropic (their Consumer or Commercial Terms).
#
# This script does nothing more than fetch them from Anthropic directly, onto
# your own machine, for your own use with Claude Code. Read the LICENSE.txt that
# comes with each one. If you are not comfortable with those terms, do not run
# this, and nothing else in this repo depends on it.
#
# Usage:  ./install-extra-skills.sh
set -euo pipefail

DEST="${HOME}/.claude/skills"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# docx/pdf/pptx/xlsx are the reason to bother: they let Claude produce real client
# deliverables instead of markdown you then have to reformat by hand.
WANT="docx pdf pptx xlsx frontend-design webapp-testing canvas-design skill-creator"

cat <<'NOTICE'
These skills belong to Anthropic, not to this repo.

  Source:  https://github.com/anthropics/skills
  Licence: proprietary, governed by your agreement with Anthropic.
           Each skill ships its own LICENSE.txt. Read it.

Press Enter to fetch them, or Ctrl+C to stop.
NOTICE
read -r _

echo "Fetching from Anthropic..."
git clone --quiet --depth 1 https://github.com/anthropics/skills.git "$TMP/anthropic"

mkdir -p "$DEST"
INSTALLED=0
for s in $WANT; do
  if [ -d "$TMP/anthropic/skills/$s" ]; then
    rm -rf "${DEST:?}/$s"
    cp -R "$TMP/anthropic/skills/$s" "$DEST/"
    echo "  installed  $s"
    INSTALLED=$((INSTALLED + 1))
  else
    echo "  not found  $s (Anthropic may have renamed or removed it)"
  fi
done

echo
echo "Installed $INSTALLED skills into $DEST"
echo "Restart Claude Code, then ask it to make you a PDF or a spreadsheet to check."
echo
echo "Skipped on purpose: brand-guidelines, which applies Anthropic's own brand"
echo "colours and typography. Not what you want on a client's website."
