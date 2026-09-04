#!/usr/bin/env python3
"""Lint copy for the banned patterns. Deterministic gate for any model.

Usage:
  python3 copy_lint.py FILE [FILE...] [--subject "subject line"] [--allow-emoji]

Hard failures (exit 1): em dash, en dash, emoji (unless --allow-emoji is passed
emails), AI lesson-framing phrases, negation-parallel slop, subject over 40
chars. Warnings do not fail. BSD grep misses these unicode chars; use this.
"""
import re
import sys

EM = chr(0x2014)
EN = chr(0x2013)

SLOP_PATTERNS = [
    (r"\bhere'?s the (thing|deal|truth|kicker|catch)\b", "lesson-framing"),
    (r"\b(now|so|but) here'?s\b", "lesson-framing"),
    (r"\blet me be (honest|real|clear|straight)\b", "lesson-framing"),
    (r"\blet me tell you\b", "lesson-framing"),
    (r"\bgreat question\b", "sycophancy"),
    (r"\bNo [^.!?\n]{2,40}[.!?] No [^.!?\n]{2,40}[.!?] (Just|Only)\b", "negation-parallel"),
]

WARN_WORDS = [
    "actually", "literally", "basically", "simply", "game-changer",
    "unlock", "elevate", "delve", "dive in", "seamless", "supercharge",
]


def emoji_count(text):
    n = 0
    for ch in text:
        o = ord(ch)
        if 0x1F000 <= o <= 0x1FAFF or 0x2600 <= o <= 0x27BF or o == 0xFE0F:
            n += 1
    return n


def lint_text(text, label, allow_emoji=False):
    fails, warns = [], []
    em, en = text.count(EM), text.count(EN)
    if em:
        fails.append(f"{em} em dash(es) U+2014")
    if en:
        fails.append(f"{en} en dash(es) U+2013")
    emo = emoji_count(text)
    if emo:
        (warns if allow_emoji else fails).append(f"{emo} emoji")
    for pat, kind in SLOP_PATTERNS:
        for m in re.finditer(pat, text, re.IGNORECASE):
            line = text.count("\n", 0, m.start()) + 1
            fails.append(f"{kind} line {line}: \"{m.group(0)[:60]}\"")
    for w in WARN_WORDS:
        c = len(re.findall(r"\b" + re.escape(w) + r"\b", text, re.IGNORECASE))
        if c:
            warns.append(f"filler \"{w}\" x{c}")
    print(f"== {label}")
    for f in fails:
        print(f"  FAIL {f}")
    for w in warns:
        print(f"  warn {w}")
    if not fails and not warns:
        print("  clean")
    return not fails


def main(argv):
    args = argv[1:]
    allow_emoji = "--allow-emoji" in args
    args = [a for a in args if a != "--allow-emoji"]
    subject = None
    if "--subject" in args:
        i = args.index("--subject")
        subject = args[i + 1]
        del args[i:i + 2]
    ok = True
    if subject is not None:
        ok = lint_text(subject, "subject", allow_emoji) and ok
        if len(subject) > 40:
            print(f"  FAIL subject is {len(subject)} chars (max 40)")
            ok = False
    if not args and subject is None:
        print(__doc__)
        return 2
    for path in args:
        try:
            text = open(path, encoding="utf-8").read()
        except OSError as e:
            print(f"== {path}\n  FAIL cannot read: {e}")
            ok = False
            continue
        ok = lint_text(text, path, allow_emoji) and ok
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
