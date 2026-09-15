#!/usr/bin/env python3
"""Prove that the machine-readable routing policy and the SHIPPED skill agree.

    MIRROR   evals/reachability/routing_policy.json    audited by the reachability tool
    RUNTIME  skill/SKILL.md                            the only file the router reads

The reachability audit reads the mirror. The product reads SKILL.md. Nothing
forced those two to describe the same rules, and in this repo they once did not:
a whole audit pass validated an iteration-18 rule set while the shipped skill
still implemented iteration-17. Every zero the audit certified was a zero of a
policy nobody could run.

The guard is deliberately the smallest thing that actually fails, not a second
SKILL.md parser:

  * SKILL.md carries `<!-- routing-policy-version: X -->` and the mirror carries
    `policy_version: X`. They must match.
  * Each rule in the mirror lists `skill_md_assertion` -- substrings that must be
    present in SKILL.md -- and, where it replaced an older rule,
    `skill_md_must_not_appear` -- the superseded wording, which must be gone.

Change the mirror and forget SKILL.md: the new assertion is missing -> FAIL.
Reword SKILL.md's rule and forget the mirror: the old assertion is missing, or
the negative assertion reappears -> FAIL. Either way somebody has to look at both
files in the same commit, which is the whole point.

An assertion is a *quotation*, so keep it short and distinctive. Asserting a
whole paragraph makes the guard fail on a typo fix and teaches people to delete
assertions.

    python scripts/check_policy_sync.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POLICY = ROOT / "evals" / "reachability" / "routing_policy.json"
SKILL = ROOT / "skill" / "SKILL.md"
MARKER = re.compile(r"<!--\s*routing-policy-version:\s*(\S+?)\s*-->")


def main() -> int:
    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    skill = SKILL.read_text(encoding="utf-8")
    errors: list[str] = []

    declared = policy.get("policy_version")
    m = MARKER.search(skill)
    if not declared:
        errors.append("routing_policy.json has no policy_version")
    elif not m:
        errors.append("skill/SKILL.md carries no <!-- routing-policy-version: ... --> marker; "
                      "routing_policy.json declares %r" % declared)
    elif m.group(1) != declared:
        errors.append("policy version mismatch: routing_policy.json says %r, skill/SKILL.md says "
                      "%r. One of them was changed without the other." % (declared, m.group(1)))

    # --- canonical rule blocks: the strong check --------------------------------
    # Each rule id must appear in SKILL.md as a marked block
    #   <!-- rule:ID -->\n<body>\n<!-- /rule:ID -->
    # whose body EQUALS the canonical string in routing_policy.json rule_blocks.
    # Verbatim equality, not substring: the defining sentence cannot drift.
    checked = 0
    blocks = policy.get("rule_blocks", {}).get("blocks", {})
    if not blocks:
        errors.append("routing_policy.json has no rule_blocks; nothing anchors the derived-signal "
                      "rules to SKILL.md.")
    for rule_id, canonical in sorted(blocks.items()):
        checked += 1
        m2 = re.search(r"<!-- rule:%s -->\n(.*?)\n<!-- /rule:%s -->" % (re.escape(rule_id),
                                                                        re.escape(rule_id)),
                       skill, re.S)
        if not m2:
            errors.append("rule %r: routing_policy.json defines it but skill/SKILL.md has no "
                          "<!-- rule:%s -->...<!-- /rule:%s --> block." % (rule_id, rule_id, rule_id))
            continue
        found = m2.group(1).strip()
        if found != canonical.strip():
            errors.append("rule %r: the block in skill/SKILL.md does not match the canonical text in "
                          "routing_policy.json rule_blocks.\n"
                          "        SKILL.md: %r\n"
                          "        policy  : %r\n"
                          "      Edit both together." % (rule_id, found[:160], canonical.strip()[:160]))

    # --- superseded wording that must be gone -----------------------------------
    for needle in policy.get("skill_md_must_not_appear", []):
        checked += 1
        if needle in skill:
            errors.append("skill/SKILL.md still contains superseded wording that routing_policy.json "
                          "records as replaced:\n        %r" % needle)

    if not checked:
        errors.append("routing_policy.json declares no assertions at all, so this guard would "
                      "pass against any SKILL.md.")

    for e in errors:
        print("ERROR [policy-sync] %s" % e)
    if errors:
        print("\n%d error(s). The audit must never validate a policy the skill does not ship."
              % len(errors))
        return 1
    print("policy sync OK: skill/SKILL.md and routing_policy.json both at %r (%d rule blocks + "
          "negative assertions verified)" % (declared, checked))
    return 0


if __name__ == "__main__":
    sys.exit(main())
