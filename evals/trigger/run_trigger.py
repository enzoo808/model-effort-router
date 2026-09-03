#!/usr/bin/env python3
"""Trigger eval for model-secici — standalone, Windows-safe.

Tests whether the skill's `description` makes Claude reach for the skill on
queries that should route through it, and leave it alone on near-misses.

skill-creator's own `scripts/run_eval.py` uses `select.select()` on a subprocess
pipe, which raises WinError 10038 on Windows. This does the same job with
`subprocess.run(..., timeout=)` and has no skill-creator dependency.

Usage:
    python evals/trigger/run_trigger.py \
        --eval-set evals/trigger/trigger_eval_set.json \
        --skill-path skill \
        --out evals/trigger/results/<label>.json

Each query spawns one real `claude -p` subprocess — a quota cost. Run it only
when the `description` frontmatter changes. A query counts as "triggered" when
the first tool call is Skill/Read pointing at model-secici (the installed skill
or a temp probe command written into <out dir>/.claude/commands/).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


def parse_skill_md(skill_dir: Path) -> tuple[str, str]:
    """Return (name, description) from skill_dir/SKILL.md frontmatter."""
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        raise ValueError("SKILL.md has no frontmatter")
    fm = m.group(1).splitlines()
    name = desc = ""
    i = 0
    while i < len(fm):
        line = fm[i]
        if line.startswith("name:"):
            name = line.split(":", 1)[1].strip().strip("\"'")
        elif line.startswith("description:"):
            val = line.split(":", 1)[1].strip()
            if val in (">", "|", ">-", "|-", ">+", "|+"):
                cont = []
                i += 1
                while i < len(fm) and (fm[i].startswith("  ") or fm[i].startswith("\t")):
                    cont.append(fm[i].strip())
                    i += 1
                desc = " ".join(cont)
                continue
            desc = val.strip("\"'")
        i += 1
    return name, desc


def run_one(query: str, skill_name: str, desc: str, project_root: str, timeout: int) -> tuple[bool, str]:
    uid = uuid.uuid4().hex[:8]
    clean = f"{skill_name}-skill-{uid}"
    cdir = Path(project_root) / ".claude" / "commands"
    cdir.mkdir(parents=True, exist_ok=True)
    cfile = cdir / f"{clean}.md"
    indented = "\n  ".join(desc.split("\n"))
    cfile.write_text(
        f"---\ndescription: |\n  {indented}\n---\n\n# {skill_name}\n\nThis skill handles: {desc}\n",
        encoding="utf-8",
    )
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    try:
        p = subprocess.run(
            ["claude", "-p", query, "--output-format", "stream-json", "--verbose"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            cwd=project_root, env=env, timeout=timeout,
        )
        for line in p.stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            if ev.get("type") != "assistant":
                continue
            for c in ev.get("message", {}).get("content", []):
                if c.get("type") != "tool_use":
                    continue
                name = c.get("name", "")
                inp = c.get("input", {}) or {}
                blob = json.dumps(inp)
                target = inp.get("skill") or inp.get("file_path") or blob[:80]
                if name in ("Skill", "Read") and (clean in blob or skill_name in blob):
                    return True, f"triggered via {name}({target})"
                return False, f"first tool={name}({target})"
        return False, "no tool_use"
    except subprocess.TimeoutExpired:
        return False, "timeout"
    except Exception as e:  # noqa: BLE001
        return False, f"error: {e}"
    finally:
        cfile.unlink(missing_ok=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--eval-set", default=str(Path(__file__).parent / "trigger_eval_set.json"))
    ap.add_argument("--skill-path", required=True, help="Directory containing SKILL.md")
    ap.add_argument("--out", required=True, help="Where to write the JSON result (its parent dir hosts the temp probe commands)")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--timeout", type=int, default=180)
    a = ap.parse_args()

    eval_set = json.loads(Path(a.eval_set).read_text(encoding="utf-8"))
    name, desc = parse_skill_md(Path(a.skill_path))
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    project_root = str(out.parent)
    print(f"skill: {name}\ndesc:  {desc}\n", file=sys.stderr)

    results: list[dict] = []
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(run_one, it["query"], name, desc, project_root, a.timeout): it for it in eval_set}
        for f in as_completed(futs):
            it = futs[f]
            trig, why = f.result()
            ok = trig == it["should_trigger"]
            results.append({"query": it["query"], "should_trigger": it["should_trigger"],
                            "triggered": trig, "why": why, "pass": ok})
            print(f"  [{'PASS' if ok else 'FAIL'}] exp={it['should_trigger']} got={trig} ({why}) | {it['query'][:66]}", file=sys.stderr)

    order = [it["query"] for it in eval_set]
    results.sort(key=lambda r: order.index(r["query"]))
    passed = sum(r["pass"] for r in results)
    summary = {"total": len(results), "passed": passed, "failed": len(results) - passed}
    out.write_text(json.dumps({"skill_name": name, "description": desc,
                               "results": results, "summary": summary}, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8")
    print(f"\n{passed}/{len(results)} passed  →  {out}", file=sys.stderr)
    sys.exit(1 if summary["failed"] else 0)


if __name__ == "__main__":
    main()
