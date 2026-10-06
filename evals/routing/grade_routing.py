#!/usr/bin/env python3
"""Grade model-secici routing outputs against evals.json (iteration-21: Claude + OpenCode Go).

Usage:
    python grade_routing.py --results-dir results/iteration-21

Expects one raw-text file per eval in --results-dir, named "eval-<id>.txt",
containing exactly what the skill printed for that eval's prompt (nothing
else -- don't include your own commentary in the file).

Since iteration-21 the skill outputs a "Claude: ..." line and an "OpenCode: ..."
line that names TWO models in order, each with its own effort:

    OpenCode: [✅ RECOMMENDED AI · ]#1 <Model> · effort: <e> · #2 <Model> · effort: <e>

and exactly one of the two lines carries the "RECOMMENDED AI" badge, plus one
"Evidence:" line. This script grades the Claude side and BOTH OpenCode picks
(model AND effort AND order) independently against evals.json's
"expected_claude" / "expected_opencode" fields, checks which side carries the
badge against "expected_recommended", and checks that an Evidence line is present
and non-trivial -- deliberately WITHOUT comparing its wording, which is free-form
by design. Optional "expected_notes" (substrings that must appear) and
"forbidden" (substrings that must not) cover the auto-added data-policy lines
and the confidentiality default. Pure string/regex matching, no LLM involved,
deterministic and free to re-run after every SKILL.md edit.

The iteration-20 (Codex) version of this grader and its evals are archived under
archive/iteration-20-codex/routing/.
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Longer names that contain a shorter one must come first.
CLAUDE_MODELS = ["Haiku 4.5", "Sonnet 5.5", "Opus 4.8", "Opus 5.5",
                 "Fable 5.1", "Fable 5", "Mythos 5.1"]

# All 30 models on the OpenCode Go page. The 15 main ones are routable; any of the
# other 15 appearing on an OpenCode line is a regression this list exists to catch.
OPENCODE_MODELS = sorted([
    "MiMo-V2.6-Pro", "MiMo-V2.6-Flash", "MiMo-V2.5-Pro", "MiMo-V2.5",
    "GLM-5.3-Flash", "GLM-5.3", "GLM-5.2",
    "Kimi K3", "Kimi K2.7 Code", "Kimi K2.6",
    "Grok 4.7", "Grok 4.6",
    "Muse Spark 1.3 Contributor", "Muse Spark 1.2 Contributor", "Muse Spark",
    "DeepSeek V4.1 Flash", "DeepSeek V4 Pro", "DeepSeek V4 Flash Vision", "DeepSeek V4 Flash",
    "GPT 6 Luna", "GPT 5.6 Luna",
    "Qwen3.8 Flash", "Qwen3.8 Max", "Qwen3.7 Plus",
    "MiniMax M3", "MiniMax M2.7",
    "LongCat 2.5 Preview", "LongCat-2.0", "Hy4 Preview", "Hy3", "Space Bunny",
], key=len, reverse=True)

DECLINE_MARKERS = ("unverified", "use claude")
BADGE_TEXT = "recommended ai"
MIN_EVIDENCE_CHARS = 20


def extract_line(output: str, label: str) -> str | None:
    """First line starting with '<label>:' (e.g. 'Claude:' or 'OpenCode:'), label stripped."""
    for line in output.splitlines():
        line = line.strip()
        if line.startswith(label + ":"):
            return line[len(label) + 1:].strip()
    return None


def first_model(text: str, names: list[str]) -> str | None:
    for n in names:
        if n in text:
            return n
    return None


def check_effort(expected: str, actual: str, side: str, allow_none: bool = False) -> tuple[bool, str]:
    em = re.search(r"effort:\s*(\w+)", expected, re.IGNORECASE)
    om = re.search(r"effort:\s*(\w+)", actual, re.IGNORECASE)
    if em:
        if not om:
            return False, f"{side}: expected 'effort: {em.group(1)}' but there is no effort field"
        if om.group(1).lower() != em.group(1).lower():
            return False, f"{side}: effort '{om.group(1)}', expected '{em.group(1)}'"
    elif om and not allow_none:
        return False, f"{side}: there should be no effort field (Haiku) but the output has one"
    return True, ""


def grade_claude(expected: str, actual_line: str | None) -> tuple[bool, str]:
    side = "Claude"
    if actual_line is None:
        return False, "no 'Claude:' line in the output"

    if "opusplan" in expected:
        if "opusplan" not in actual_line:
            return False, f"{side}: expected 'opusplan', got: '{actual_line}'"
        m = re.search(r"plan:\s*(\w+).*?execute:\s*(\w+)", expected, re.IGNORECASE | re.DOTALL)
        om = re.search(r"plan:\s*(\w+).*?execute:\s*(\w+)", actual_line, re.IGNORECASE | re.DOTALL)
        if not m:
            return False, f"{side}: evals.json expected_claude format is broken (script bug)"
        if not om:
            return False, f"{side}: output has no 'plan: X . execute: Y' pattern"
        if om.group(1).lower() != m.group(1).lower():
            return False, f"{side}: plan effort '{om.group(1)}', expected '{m.group(1)}'"
        if om.group(2).lower() != m.group(2).lower():
            return False, f"{side}: execute effort '{om.group(2)}', expected '{m.group(2)}'"
        return True, f"{side}: opusplan correct (plan={om.group(1)}, execute={om.group(2)})"

    expected_model = first_model(expected, CLAUDE_MODELS)
    if expected_model is None:
        return False, f"{side}: no recognised model name in expected_claude (script bug)"
    if expected_model not in actual_line:
        return False, f"{side}: '{expected_model}' not in output (output: '{actual_line}')"
    for other in CLAUDE_MODELS:
        if other == expected_model or other in expected_model:
            continue
        if other in actual_line:
            return False, f"{side}: unexpected model '{other}' appears in the output"
    ok, msg = check_effort(expected, actual_line, side)
    if not ok:
        return False, msg
    em = re.search(r"effort:\s*(\w+)", expected, re.IGNORECASE)
    return True, f"{side}: {expected_model} correct" + (f", effort={em.group(1)}" if em else "")


def split_picks(text: str) -> dict[str, str]:
    """'#1 X · effort: a · #2 Y · effort: b' -> {'1': 'X · effort: a', '2': 'Y · effort: b'}"""
    parts = re.split(r"#\s*([12])\b", text)
    picks = {}
    # parts = [prefix, '1', seg1, '2', seg2]
    for i in range(1, len(parts) - 1, 2):
        picks[parts[i]] = parts[i + 1]
    return picks


def grade_opencode(expected: str, actual_line: str | None) -> tuple[bool, str]:
    side = "OpenCode"
    if actual_line is None:
        return False, "no 'OpenCode:' line in the output"

    exp_lower = expected.strip().lower()
    if exp_lower.startswith(DECLINE_MARKERS):
        if not any(m in actual_line.lower() for m in DECLINE_MARKERS):
            return False, f"{side}: expected a decline ('unverified' / 'use Claude'), got: '{actual_line}'"
        if first_model(actual_line, OPENCODE_MODELS) is not None and "#1" in actual_line:
            return False, f"{side}: a decline must not name pool models, got: '{actual_line}'"
        return True, f"{side}: decline (correct)"

    exp = split_picks(expected)
    act = split_picks(actual_line)
    if set(exp) != {"1", "2"}:
        return False, f"{side}: evals.json expected_opencode must name #1 and #2 (script bug)"
    if set(act) != {"1", "2"}:
        return False, f"{side}: the line must name exactly '#1' and '#2' picks, got: '{actual_line}'"

    msgs = []
    for rank in ("1", "2"):
        want = first_model(exp[rank], OPENCODE_MODELS)
        if want is None:
            return False, f"{side}: no recognised model in expected #{rank} (script bug)"
        if first_model(act[rank], OPENCODE_MODELS) != want:
            return False, f"{side}: #{rank} should be '{want}', got: '{act[rank].strip()}'"
        for other in OPENCODE_MODELS:
            if other == want or other in want:
                continue
            if other in act[rank]:
                return False, f"{side}: #{rank} also names unexpected model '{other}'"
        ok, msg = check_effort(exp[rank], act[rank], f"{side} #{rank}")
        if not ok:
            return False, msg
        em = re.search(r"effort:\s*(\w+)", exp[rank], re.IGNORECASE)
        msgs.append(f"#{rank} {want}" + (f" {em.group(1)}" if em else ""))
    return True, f"{side}: " + ", ".join(msgs)


def badge_sides(output: str) -> list[str]:
    found = []
    for label in ("Claude", "OpenCode"):
        line = extract_line(output, label)
        if line and BADGE_TEXT in line.lower():
            found.append(label.lower())
    return found


def grade_evidence(output: str, want_low_confidence: bool) -> tuple[bool, str]:
    """Evidence line must exist and say something. Its wording is never matched."""
    line = extract_line(output, "Evidence")
    if line is None:
        return False, "no 'Evidence:' line in the output"
    if len(line) < MIN_EVIDENCE_CHARS:
        return False, f"'Evidence:' line is too short to be a real justification: '{line}'"
    normalised = line.lower().replace("-", " ")
    has_low = "low confidence" in normalised
    if want_low_confidence and not has_low:
        return False, f"expected the Evidence line to flag low confidence, got: '{line}'"
    if not want_low_confidence and has_low:
        return False, f"the Evidence line flags low confidence but this row carries no dagger: '{line}'"
    return True, "evidence line present"


def grade_blocked(output: str) -> tuple[bool, str]:
    for name in CLAUDE_MODELS + OPENCODE_MODELS:
        if name in output:
            return False, f"no model should be recommended but '{name}' was found"
    if "Claude:" in output or "OpenCode:" in output:
        return False, "Step 0 should block but Claude:/OpenCode: lines were produced"
    if "Evidence:" in output:
        return False, "Step 0 should block but an Evidence: line was produced"
    if "?" not in output:
        return False, "expected a clarifying question but no '?' found"
    if BADGE_TEXT in output.lower():
        return False, "Step 0 should block but a RECOMMENDED AI badge was produced"
    return True, "no model recommended, no badge, clarifying question present"


def grade_one(item: dict, output: str) -> tuple[bool, str]:
    if item.get("blocked"):
        return grade_blocked(output)

    ok_c, msg_c = grade_claude(item["expected_claude"], extract_line(output, "Claude"))
    if not ok_c:
        return False, msg_c
    ok_o, msg_o = grade_opencode(item["expected_opencode"], extract_line(output, "OpenCode"))
    if not ok_o:
        return False, msg_o

    sides = badge_sides(output)
    if len(sides) > 1:
        return False, f"more than one RECOMMENDED AI badge ({', '.join(sides)}) -- exactly one is allowed"
    badge_msg = ""
    want = (item.get("expected_recommended") or "").strip().lower()
    if want:
        if want not in ("claude", "opencode"):
            return False, f"expected_recommended must be 'claude' or 'opencode' (got '{want}')"
        if not sides:
            return False, f"no RECOMMENDED AI badge found; expected it on the {want} line"
        if sides[0] != want:
            return False, f"badge is on '{sides[0]}', expected '{want}'"
        badge_msg = f"; recommended={sides[0]} (correct)"
        ok_e, msg_e = grade_evidence(output, bool(item.get("expected_low_confidence")))
        if not ok_e:
            return False, msg_e
        badge_msg += "; evidence ok"

    low = output.lower()
    extras = []
    if item.get("expected_shared_note"):
        if item["expected_shared_note"].lower() not in low:
            return False, f"expected note ('{item['expected_shared_note']}') not in the output"
        extras.append("review note")
    for needle in item.get("expected_notes", []):
        if needle.lower() not in low:
            return False, f"expected text ('{needle}') not in the output"
        extras.append(needle)
    for needle in item.get("forbidden", []):
        if needle.lower() in low:
            return False, f"forbidden text ('{needle}') appears in the output"

    msg = f"{msg_c}; {msg_o}{badge_msg}"
    if extras:
        msg += f"; notes ok ({', '.join(extras)})"
    return True, msg


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--evals", default=str(Path(__file__).parent / "evals.json"))
    parser.add_argument("--results-dir", required=True, help="Directory containing eval-<id>.txt raw output files")
    parser.add_argument("--selftest", action="store_true",
                        help="grade each eval's own 'golden_output' (if present) instead of --results-dir; "
                             "proves the grader and the goldens agree")
    args = parser.parse_args()

    evals = json.loads(Path(args.evals).read_text(encoding="utf-8"))["evals"]
    results_dir = Path(args.results_dir)

    results = []
    for item in evals:
        out_file = results_dir / f"eval-{item['id']}.txt"
        if args.selftest:
            output = (item.get("golden_output") or "").strip()
            if not output:
                results.append({"id": item["id"], "eval_name": item["eval_name"], "passed": None,
                                "evidence": "no golden_output to self-test"})
                continue
        else:
            if not out_file.exists():
                results.append({"id": item["id"], "eval_name": item["eval_name"], "passed": None,
                                "evidence": f"output file not found: {out_file}"})
                continue
            output = out_file.read_text(encoding="utf-8").strip()
        passed, evidence = grade_one(item, output)
        results.append({"id": item["id"], "eval_name": item["eval_name"], "passed": passed, "evidence": evidence})

    passed = sum(1 for r in results if r["passed"] is True)
    failed = sum(1 for r in results if r["passed"] is False)
    missing = sum(1 for r in results if r["passed"] is None)

    for r in results:
        status = {True: "PASS", False: "FAIL", None: "SKIP"}[r["passed"]]
        print(f"[{status}] #{r['id']} {r['eval_name']}: {r['evidence']}")

    print(f"\n{passed}/{len(results)} passed, {failed} failed, {missing} skipped (no output file)")

    if not args.selftest:
        results_dir.mkdir(parents=True, exist_ok=True)
        summary_path = results_dir / "grading.json"
        summary_path.write_text(json.dumps({
            "results": results,
            "summary": {"passed": passed, "failed": failed, "skipped": missing, "total": len(results)},
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        print(f"Details: {summary_path}")

    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()
