#!/usr/bin/env python3
"""Grade model-secici routing outputs against evals.json.

Usage:
    python grade_routing.py --results-dir results/iteration-9

Expects one raw-text file per eval in --results-dir, named "eval-<id>.txt",
containing exactly what the skill printed for that eval's prompt (nothing
else -- don't include your own commentary in the file).

Since 5 August 2026 the skill outputs BOTH a "Claude: ..." line and a
"Codex: ..." line for every (non-blocked) prompt. This script grades each
side independently against evals.json's "expected_claude"/"expected_codex"
fields, plus optional shared/claude-only note checks. Pure string/regex
matching, no LLM involved, deterministic and free to re-run after every
SKILL.md/reference.md edit.
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Order matters for the first-match lookup below: a longer name that contains a
# shorter one must come first. "Sol" is a substring of "Sol Ultra"; "Fable 5" of
# "Fable 5.1"; "Mythos 5" of "Mythos 5.1".
MODEL_NAMES = ["Haiku 4.5", "Sonnet 5", "Opus 4.8", "Opus 5",
               "Fable 5.1", "Fable 5", "Mythos 5.1",
               "Sol Ultra", "Sol", "Terra", "Luna"]

# Marker the Codex line uses when it declines to recommend a model.
UNVERIFIED = "unverified"


def extract_line(output: str, label: str) -> str | None:
    """First line starting with '<label>:' (e.g. 'Claude:' or 'Codex:'), label stripped."""
    for line in output.splitlines():
        line = line.strip()
        if line.startswith(label + ":"):
            return line[len(label) + 1:].strip()
    return None


def grade_side(expected: str, actual_line: str | None, side: str) -> tuple[bool, str]:
    if actual_line is None:
        return False, f"no '{side}:' line in the output"

    if expected.strip().lower().startswith(UNVERIFIED):
        if UNVERIFIED not in actual_line.lower():
            return False, f"{side}: expected '{UNVERIFIED}', got: '{actual_line}'"
        return True, f"{side}: unverified (correct)"

    if "opusplan" in expected:
        if "opusplan" not in actual_line:
            return False, f"{side}: expected 'opusplan', got: '{actual_line}'"
        m = re.search(r"plan:\s*(\w+).*?execute:\s*(\w+)", expected, re.IGNORECASE | re.DOTALL)
        om = re.search(r"plan:\s*(\w+).*?execute:\s*(\w+)", actual_line, re.IGNORECASE | re.DOTALL)
        if not m:
            return False, f"{side}: evals.json expected_{side.lower()} format is broken (script bug)"
        if not om:
            return False, f"{side}: output has no 'plan: X . execute: Y' pattern"
        if om.group(1).lower() != m.group(1).lower():
            return False, f"{side}: plan effort '{om.group(1)}', expected '{m.group(1)}'"
        if om.group(2).lower() != m.group(2).lower():
            return False, f"{side}: execute effort '{om.group(2)}', expected '{m.group(2)}'"
        return True, f"{side}: opusplan correct (plan={om.group(1)}, execute={om.group(2)})"

    expected_model = next((n for n in MODEL_NAMES if n in expected), None)
    if expected_model is None:
        return False, f"{side}: no recognised model name in expected_{side.lower()} (script bug)"
    if expected_model not in actual_line:
        return False, f"{side}: '{expected_model}' not in output (output: '{actual_line}')"
    for other in MODEL_NAMES:
        if other == expected_model or other in expected_model:
            continue
        if other in actual_line:
            return False, f"{side}: unexpected model '{other}' appears in the output"

    em = re.search(r"effort:\s*(\w+)", expected, re.IGNORECASE)
    if em:
        om = re.search(r"effort:\s*(\w+)", actual_line, re.IGNORECASE)
        if not om:
            return False, f"{side}: expected 'effort: {em.group(1)}' but there is no effort field"
        if om.group(1).lower() != em.group(1).lower():
            return False, f"{side}: effort '{om.group(1)}', expected '{em.group(1)}'"
    elif re.search(r"effort:\s*\w+", actual_line, re.IGNORECASE):
        return False, f"{side}: there should be no effort field (Haiku) but the output has one"

    return True, f"{side}: {expected_model} correct" + (f", effort={em.group(1)}" if em else "")


def grade_blocked(output: str) -> tuple[bool, str]:
    for name in MODEL_NAMES:
        if name in output:
            return False, f"no model should be recommended but '{name}' was found"
    if "Claude:" in output or "Codex:" in output:
        return False, "Step 0 should block but Claude:/Codex: lines were produced"
    if "?" not in output:
        return False, "expected a clarifying question but no '?' found"
    return True, "no model recommended, clarifying question present"


def grade_one(item: dict, output: str) -> tuple[bool, str]:
    if item.get("blocked"):
        return grade_blocked(output)

    claude_line = extract_line(output, "Claude")
    codex_line = extract_line(output, "Codex")
    ok_c, msg_c = grade_side(item["expected_claude"], claude_line, "Claude")
    if not ok_c:
        return False, msg_c
    ok_x, msg_x = grade_side(item["expected_codex"], codex_line, "Codex")
    if not ok_x:
        return False, msg_x

    notes_ok = []
    for note_key, label in (("expected_shared_note", "shared note"), ("expected_claude_note", "Claude note")):
        needle = item.get(note_key)
        if needle and needle.lower() not in output.lower():
            return False, f"expected {label} ('{needle}') not in the output"
        if needle:
            notes_ok.append(label)

    evidence = f"{msg_c}; {msg_x}"
    if notes_ok:
        evidence += f"; notes ok ({', '.join(notes_ok)})"
    return True, evidence


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--evals", default=str(Path(__file__).parent / "evals.json"))
    parser.add_argument("--results-dir", required=True, help="Directory containing eval-<id>.txt raw output files")
    args = parser.parse_args()

    evals = json.loads(Path(args.evals).read_text(encoding="utf-8"))["evals"]
    results_dir = Path(args.results_dir)

    results = []
    for item in evals:
        out_file = results_dir / f"eval-{item['id']}.txt"
        if not item.get("machine_gradable", True):
            evidence = "subjective/observational eval -- can't be checked deterministically, review by hand"
            if out_file.exists():
                evidence += f" ({out_file})"
            results.append({"id": item["id"], "eval_name": item["eval_name"], "passed": "manual", "evidence": evidence})
            continue
        if item.get("format_outdated"):
            results.append({"id": item["id"], "eval_name": item["eval_name"], "passed": "manual",
                             "evidence": "old (single-ecosystem) format -- dual-output expectation not added, needs backfill"})
            continue
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
    manual = sum(1 for r in results if r["passed"] == "manual")

    for r in results:
        status = {True: "PASS", False: "FAIL", None: "SKIP", "manual": "MANUAL"}[r["passed"]]
        print(f"[{status}] #{r['id']} {r['eval_name']}: {r['evidence']}")

    print(f"\n{passed}/{len(results) - manual} passed (among auto-graded), "
          f"{failed} failed, {missing} skipped (no output file), {manual} manual/old-format")

    summary_path = results_dir / "grading.json"
    summary_path.write_text(json.dumps({
        "results": results,
        "summary": {"passed": passed, "failed": failed, "skipped": missing, "total": len(results)},
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Details: {summary_path}")

    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()
