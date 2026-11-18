#!/usr/bin/env python3
"""Fail when the Turkish mirror silently drops a rule that SKILL.md defines.

    RUNTIME  skill/SKILL.md                   rules sit in `<!-- rule:ID -->...<!-- /rule:ID -->` blocks
    MIRROR   claude-ai/instructions.tr.md     the hand-synced Turkish fallback

The mirror is a translation, so it cannot be diffed against SKILL.md. What it can be
held to is a ledger: every rule id SKILL.md marks must appear in the mirror either as
the same `<!-- rule:ID -->` marker placed next to the translated rule, or in ONE
declared line

    <!-- mirror-omits: ID, ID -->        (empty list = nothing omitted)

A rule that is neither carried nor declared is exactly how iteration-35's mirror lost
D3DIAG's scoring half, A1 and rule 13 without anyone deciding to. The check only proves
the rule was *acknowledged*; whether the translation is faithful stays a review job.
A marker for an id SKILL.md no longer has, an id both carried and omitted, an unknown
omitted id, or a second `mirror-omits` line is also an error.

    python scripts/check_mirror_rules.py [--root PATH]
    python scripts/check_mirror_rules.py --selftest
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RULE = re.compile(r"<!--\s*rule:([A-Za-z0-9_-]+)\s*-->")
OMITS = re.compile(r"<!--\s*mirror-omits:([^>]*?)-->")


def check(skill: str, mirror: str) -> tuple[list[str], list[str]]:
    """Return (uncovered ids, other errors)."""
    wanted = set(RULE.findall(skill))
    carried = set(RULE.findall(mirror))
    lines = OMITS.findall(mirror)
    errors: list[str] = []
    if len(lines) > 1:
        errors.append("the mirror declares `mirror-omits` %d times; it must be one line" % len(lines))
    omitted = {i.strip() for line in lines for i in line.split(",") if i.strip()}
    for i in sorted(carried - wanted):
        errors.append("mirror carries <!-- rule:%s --> but SKILL.md has no such rule (stale marker)" % i)
    for i in sorted(omitted - wanted):
        errors.append("mirror-omits names %r, which SKILL.md does not define" % i)
    for i in sorted(carried & omitted):
        errors.append("rule %r is both carried and listed in mirror-omits; pick one" % i)
    return sorted(wanted - carried - omitted), errors


def selftest() -> list[str]:
    skill = "<!-- rule:A -->\nx\n<!-- /rule:A -->\n<!-- rule:B-1 -->\ny\n<!-- /rule:B-1 -->\n"
    cases = [  # (mirror text, expected uncovered, expect other errors)
        ("<!-- rule:A -->\n<!-- rule:B-1 -->\n<!-- mirror-omits: -->", [], False),
        ("<!-- rule:A -->\n<!-- mirror-omits: B-1 -->", [], False),
        ("<!-- rule:A -->", ["B-1"], False),
        ("<!-- mirror-omits: A, B-1 -->\n<!-- rule:A -->", [], True),
        ("<!-- rule:A -->\n<!-- rule:Z -->\n<!-- mirror-omits: B-1 -->", [], True),
        ("<!-- rule:A -->\n<!-- mirror-omits: B-1 -->\n<!-- mirror-omits: -->", [], True),
        ("<!-- rule:A -->\n<!-- mirror-omits: B-1, Q -->", [], True),
    ]
    fails = []
    for n, (mirror, want, want_err) in enumerate(cases, 1):
        got, errs = check(skill, mirror)
        if got != want or bool(errs) != want_err:
            fails.append("selftest case %d: uncovered %s (want %s), errors %s" % (n, got, want, errs))
    return fails


def main() -> int:
    if "--selftest" in sys.argv:
        fails = selftest()
        for f in fails:
            print("ERROR [mirror-rules] %s" % f)
        print("mirror-rules selftest %s" % ("FAILED" if fails else "OK (7 cases)"))
        return 1 if fails else 0
    broken = selftest()  # seven cheap cases, so CI notices a broken guard too
    if broken:
        print("ERROR [mirror-rules] the guard's own selftest fails: %s" % broken)
        return 1
    root = Path(sys.argv[sys.argv.index("--root") + 1]) if "--root" in sys.argv else ROOT
    skill = (root / "skill" / "SKILL.md").read_text(encoding="utf-8")
    mirror = (root / "claude-ai" / "instructions.tr.md").read_text(encoding="utf-8")
    uncovered, errors = check(skill, mirror)
    for i in uncovered:
        print("ERROR [mirror-rules] rule %s is in skill/SKILL.md but the mirror neither carries "
              "<!-- rule:%s --> nor lists it in <!-- mirror-omits: ... -->" % (i, i))
    for e in errors:
        print("ERROR [mirror-rules] %s" % e)
    if uncovered or errors:
        print("\n%d problem(s). Translate the rule next to its marker, or declare the omission." %
              (len(uncovered) + len(errors)))
        return 1
    n = len(set(RULE.findall(skill)))
    print("mirror rules OK: all %d rule ids in skill/SKILL.md are carried or declared in the mirror" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
