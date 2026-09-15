#!/usr/bin/env python3
"""Fail if a worked example in skill/SKILL.md contradicts the rule it illustrates.

The m1 cold-routing failure was a runtime example that omitted the mandatory
`low-confidence` marker its own badge row requires — so a cold agent copied the
shipped example verbatim and failed the eval. An example that disagrees with the
rules is worse than no example, because readers calibrate off examples.

Two checks, both mechanical:

  1. **Well-formed.** Every fenced example block is either a `Clarify:` block
     (no model/badge/Evidence lines) or a full recommendation (a `Claude:` line,
     a `Codex:` line, an `Evidence:` line, exactly one `RECOMMENDED AI` badge).
  2. **Consistent with the goldens.** When an example's prompt matches an eval in
     evals/routing/evals.json, the example's models, efforts, badge side,
     `low-confidence` presence and human-review note must match that golden.
     This is what would have caught m1.

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

MODELS = ["Haiku 4.5", "Sonnet 5", "Opus 4.8", "Opus 5", "Fable 5.1", "Mythos 5.1",
          "Sol Ultra", "Sol", "Terra", "Luna", "Astra", "opusplan"]
BADGE = "recommended ai"


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def line(block: str, label: str) -> str | None:
    for ln in block.splitlines():
        ln = ln.strip()
        if ln.startswith(label + ":"):
            return ln[len(label) + 1:].strip()
    return None


def model_in(text: str) -> str | None:
    for m in MODELS:
        if m in text:
            return m
    return None


def effort_in(text: str) -> str | None:
    m = re.search(r"effort:\s*([\w]+)", text, re.I)
    return m.group(1).lower() if m else None


def examples(skill: str) -> list[tuple[str, str]]:
    """(prompt-ish label, fenced block body). The label is the nearest italic
    line above the fence, if any."""
    # Pair fence lines by index (every line that is exactly ```), so nested blank
    # lines and adjacent blocks can't cause the regex mis-pairing.
    lines = skill.split("\n")
    fences = [i for i, ln in enumerate(lines) if ln.strip() == "```"]
    out = []
    for a, b in zip(fences[0::2], fences[1::2]):
        block = "\n".join(lines[a + 1:b])
        starts = block.lstrip()
        if not (starts.startswith("Claude:") or starts.startswith("Clarify:")):
            continue  # speed-line snippets, format stubs, etc.
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

    # Index evals by a normalised prompt for fuzzy matching.
    eval_by_prompt = [(norm(e["prompt"]), e) for e in evals if e.get("prompt")]

    matched = 0
    for label, block in ex:
        is_clarify = "Clarify:" in block and "Claude:" not in block
        # ---- well-formedness ----
        if is_clarify:
            if "RECOMMENDED AI" in block or "Claude:" in block or "Codex:" in block \
                    or "Evidence:" in block:
                errors.append("blocked example is not clean: %r" % block[:60])
            if "?" not in block:
                errors.append("blocked example has no clarifying question: %r" % block[:60])
            continue
        cl, cx, ev = line(block, "Claude"), line(block, "Codex"), line(block, "Evidence")
        if cl is None or cx is None:
            errors.append("example missing a Claude:/Codex: line: %r" % block[:60])
            continue
        if ev is None:
            errors.append("example missing an Evidence: line: %r" % block[:60])
        badges = sum(1 for t in (cl, cx) if BADGE in t.lower())
        if badges != 1:
            errors.append("example must carry exactly one RECOMMENDED AI badge, found %d: %r"
                          % (badges, (label or block[:50])))

        # ---- consistency with a matching golden ----
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
            if not is_clarify:
                errors.append("%s: golden is blocked but the example produces recommendation lines" % eid)
            continue
        # models + efforts per side
        for side, exline in (("claude", cl), ("codex", cx)):
            exp = golden["expected_" + side]
            if exp.strip().lower().startswith(("unverified", "use claude")):
                continue
            wm = model_in(exp)
            if wm and wm not in exline:
                errors.append("%s %s: example says %r, golden expects %s" % (eid, side, exline, wm))
            we = effort_in(exp)
            xe = effort_in(exline)
            if we and we != xe:
                errors.append("%s %s: example effort %r, golden %r" % (eid, side, xe, we))
        # badge side
        want = golden.get("expected_recommended")
        if want:
            got = "claude" if BADGE in cl.lower() else "codex" if BADGE in cx.lower() else None
            if got != want:
                errors.append("%s: example badge on %r, golden expects %r" % (eid, got, want))
        # low-confidence
        if golden.get("expected_low_confidence"):
            if ev is None or "low-confidence" not in ev.lower().replace(" ", "-"):
                errors.append("%s: golden requires low-confidence but the example Evidence omits it: %r"
                              % (eid, ev))
        # human-review note
        if "human review" in (golden.get("expected_shared_note") or "").lower():
            if "do not apply without human review" not in block.lower():
                errors.append("%s: golden requires the human-review note but the example omits it" % eid)

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
