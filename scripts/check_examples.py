#!/usr/bin/env python3
"""Fail if a worked example in skill/SKILL.md contradicts the rule it illustrates.

The m1 cold-routing failure (iteration-16) was a runtime example that omitted the
mandatory `low-confidence` marker its own badge row requires — so a cold agent
copied the shipped example verbatim and failed the eval. An example that disagrees
with the rules is worse than no example, because readers calibrate off examples.

Two checks, both mechanical:

  1. **Well-formed.** Every fenced example block is either a `Clarify:` block
     (no model/badge/Evidence lines) or a full recommendation (a `Claude:` line,
     an `OpenCode:` line, an `Evidence:` line, exactly one `RECOMMENDED AI` badge,
     and — unless the OpenCode arm declined — exactly a `#1` and a `#2` pick).
  2. **Consistent with the goldens.** When an example's prompt matches an eval in
     evals/routing/evals.json, the example's models, efforts, badge side,
     `low-confidence` presence and human-review note must match that golden.

    python scripts/check_examples.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skill" / "SKILL.md"
EVALS = ROOT / "evals" / "routing" / "evals.json"

CLAUDE_MODELS = ["Haiku 4.5", "Sonnet 5.5", "Opus 4.8", "Opus 5.5", "Fable 5.1", "Mythos 5.1", "opusplan"]
BADGE = "recommended ai"
DECLINE = ("unverified", "use claude")


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def line(block: str, label: str) -> str | None:
    for ln in block.splitlines():
        ln = ln.strip()
        if ln.startswith(label + ":"):
            return ln[len(label) + 1:].strip()
    return None


def claude_model(text: str) -> str | None:
    for m in CLAUDE_MODELS:
        if m in text:
            return m
    return None


def effort_in(text: str) -> str | None:
    m = re.search(r"effort:\s*([\w]+)", text, re.I)
    return m.group(1).lower() if m else None


def picks(text: str) -> list[tuple[str, str | None]]:
    """'#1 X · effort: a · #2 Y · effort: b' -> [('X','a'), ('Y','b')]"""
    parts = re.split(r"#\s*[12]\b", text)[1:]
    out = []
    for p in parts:
        name = p.split("·")[0].strip().replace("✅ RECOMMENDED AI", "").strip()
        out.append((name, effort_in(p)))
    return out


def examples(skill: str) -> list[tuple[str, str]]:
    """(prompt-ish label, fenced block body). The label is the nearest italic
    line above the fence, if any."""
    lines = skill.split("\n")
    fences = [i for i, ln in enumerate(lines) if ln.strip() == "```"]
    out = []
    for a, b in zip(fences[0::2], fences[1::2]):
        block = "\n".join(lines[a + 1:b])
        starts = block.lstrip()
        if not (starts.startswith("Claude:") or starts.startswith("Clarify:")):
            continue  # format stubs, etc.
        if "<" in block:
            continue  # a format template, not an example
        label = ""
        for ln in reversed(lines[max(0, a - 6):a]):
            t = ln.strip()
            if t.startswith("*") and "\"" in t:
                label = t.strip("*").strip()
                break
        out.append((label, block))
    return out


def main() -> int:
    skill = SKILL.read_text(encoding="utf-8")
    evals = json.loads(EVALS.read_text(encoding="utf-8"))["evals"]
    errors: list[str] = []
    ex = examples(skill)
    if not ex:
        print("ERROR [examples] no worked examples found in SKILL.md — the parser or the file broke")
        return 1

    eval_by_prompt = [(norm(e["prompt"]), e) for e in evals if e.get("prompt")]

    matched = 0
    for label, block in ex:
        is_clarify = "Clarify:" in block and "Claude:" not in block
        if is_clarify:
            if "RECOMMENDED AI" in block or "Claude:" in block or "OpenCode:" in block \
                    or "Evidence:" in block:
                errors.append("blocked example is not clean: %r" % block[:60])
            if "?" not in block:
                errors.append("blocked example has no clarifying question: %r" % block[:60])
            continue
        cl, oc, ev = line(block, "Claude"), line(block, "OpenCode"), line(block, "Evidence")
        if cl is None or oc is None:
            errors.append("example missing a Claude:/OpenCode: line: %r" % block[:60])
            continue
        if ev is None:
            errors.append("example missing an Evidence: line: %r" % block[:60])
        badges = sum(1 for t in (cl, oc) if BADGE in t.lower())
        if badges != 1:
            errors.append("example must carry exactly one RECOMMENDED AI badge, found %d: %r"
                          % (badges, (label or block[:50])))
        declined = any(m in oc.lower() for m in DECLINE) and "#1" not in oc
        if not declined:
            pk = picks(oc)
            if len(pk) != 2:
                errors.append("OpenCode line must name exactly #1 and #2: %r" % oc[:80])
            for name, eff in pk:
                if not eff:
                    errors.append("OpenCode pick %r has no effort: %r" % (name, oc[:80]))
        if "opusplan" in cl and "⚠️" not in block:
            errors.append("opusplan example is missing the ⚠️ effort warning: %r" % (label or block[:50]))

        nlabel = norm(label)
        golden = None
        for np, e in eval_by_prompt:
            if not np:
                continue
            a, b = (nlabel, np) if len(nlabel) <= len(np) else (np, nlabel)
            if a and a in b:
                golden = e
                break
        if golden is None:
            continue
        matched += 1
        eid = golden["id"]
        if golden.get("blocked"):
            errors.append("%s: golden is blocked but the example produces recommendation lines" % eid)
            continue

        # Claude side
        exp_c = golden["expected_claude"]
        wm = claude_model(exp_c)
        if wm and wm not in cl:
            errors.append("%s claude: example says %r, golden expects %s" % (eid, cl, wm))
        we, xe = effort_in(exp_c), effort_in(cl)
        if we and we != xe:
            errors.append("%s claude: example effort %r, golden %r" % (eid, xe, we))

        # OpenCode side
        exp_o = golden["expected_opencode"]
        if exp_o.strip().lower().startswith(DECLINE):
            if not declined:
                errors.append("%s opencode: golden declines but the example names models: %r" % (eid, oc[:80]))
        elif declined:
            errors.append("%s opencode: example declines but the golden expects models" % eid)
        else:
            for rank, ((en, ee), (an, ae)) in enumerate(zip(picks(exp_o), picks(oc)), start=1):
                if en not in an:
                    errors.append("%s opencode #%d: example says %r, golden expects %r" % (eid, rank, an, en))
                if ee != ae:
                    errors.append("%s opencode #%d: example effort %r, golden %r" % (eid, rank, ae, ee))

        want = golden.get("expected_recommended")
        if want:
            got = "claude" if BADGE in cl.lower() else "opencode" if BADGE in oc.lower() else None
            if got != want:
                errors.append("%s: example badge on %r, golden expects %r" % (eid, got, want))
        low = ev is not None and "low-confidence" in ev.lower().replace(" ", "-")
        if golden.get("expected_low_confidence") and not low:
            errors.append("%s: golden requires low-confidence but the example Evidence omits it: %r" % (eid, ev))
        if not golden.get("expected_low_confidence") and low:
            errors.append("%s: example Evidence says low-confidence but the golden's row carries no dagger: %r"
                          % (eid, ev))
        if "human review" in (golden.get("expected_shared_note") or "").lower():
            if "do not apply without human review" not in block.lower():
                errors.append("%s: golden requires the human-review note but the example omits it" % eid)
        for needle in golden.get("expected_notes", []):
            if needle.lower() not in block.lower():
                errors.append("%s: golden requires %r but the example omits it" % (eid, needle))

    for e in errors:
        print("ERROR [examples] %s" % e)
    if errors:
        print("\n%d error(s). A shipped example must never contradict the rule it illustrates." % len(errors))
        return 1
    print("examples OK: %d worked examples, %d cross-checked against goldens, none contradict a rule"
          % (len(ex), matched))
    return 0


if __name__ == "__main__":
    sys.exit(main())
