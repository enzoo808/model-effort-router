#!/usr/bin/env python3
"""Derive the OpenCode pair per capability from independent multi-source evidence.

    python scripts/derive_opencode_rows.py            # print the consensus tables
    python scripts/derive_opencode_rows.py --json     # machine-readable

Input: skill/opencode-evidence.json (independent anchors only; aggregates and
single-version fragments are excluded from the consensus).

Method (deliberately simple, so that it can be audited by eye):
  1. For each capability tag, take its anchors. For each anchor, rank the models that
     have a value (open pool models only — Claude rows are reported separately).
  2. A model's anchor score = percentile of its rank among those models (1.0 best).
  3. consensus = mean anchor score over the anchors where the model has a value; a model
     needs >= MIN_ANCHORS values to be eligible to lead (no single-row champions).
  4. Models within TIE of the top consensus form the *leading band*; the router orders
     the band by cap pressure (Go cap tier, then cost/task) unless depth says otherwise.
Where an anchor publishes error margins (DeepSWE) a difference smaller than the combined
margin is reported as a tie, not a ranking.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "skill" / "opencode-evidence.json"
MIN_ANCHORS = 2
TIE = 0.10  # consensus points that still count as "the same band"

# which anchors feed which capability's consensus (aggregates / partial versions excluded)
TAGS = {
    "agentic-code": ["AA Terminal-Bench 4.0", "DeepSWE v1.1 (Mercor/Datacurve)",
                     "Arena Agent Arena (net outcome vs avg model, %)", "Terminal-Bench 2.1 (Vals)",
                     "FrontierSWE v2"],
    "deep-reasoning": ["AA-HLE", "CritPt", "ARC-AGI-2"],
    "knowledge-work": ["GDPval-AA (Elo)", "AA-Briefcase", "AA-AnalystAgent", "AA Harvey LAB (legal)"],
    "workflow-automation": ["AA AutomationBench", "AA Tau3 Banking", "AA ITBench", "AA EnterpriseOps-Gym",
                            "tau2-bench"],
    "long-context": ["AA-LCR", "MLCR-AA"],
    "research-synthesis": ["AA-Omniscience Index", "AA-Omniscience hallucination rate (lower better)"],
    "science": ["AA-SciCode", "CritPt"],
    "doc-data-understanding": ["GDP.pdf", "AA-MMMU-Pro (multimodal)"],
}

ROUTABLE = ["MiMo-V2.6-Pro", "GLM-5.3", "Kimi K3", "GLM-5.3-Flash", "MiMo-V2.6-Flash",
            "DeepSeek V4.1 Flash", "Qwen3.8 Flash", "Qwen3.8 Max"]
NC1_ONLY = ["Grok 4.7", "Muse Spark 1.3", "GPT 6 Luna"]
DOMINATED = ["DeepSeek V4 Pro", "MiniMax M3"]


def percentiles(values: dict[str, float], higher_better: bool, models: list[str]) -> dict[str, float]:
    items = [(m, values[m]) for m in models if m in values]
    items.sort(key=lambda kv: kv[1], reverse=higher_better)
    n = len(items)
    out = {}
    for i, (m, _v) in enumerate(items):
        out[m] = 1.0 if n == 1 else (n - 1 - i) / (n - 1)
    return out


def consensus(data: dict, tag: str, models: list[str]) -> list[tuple[str, float, int, list[str]]]:
    per: dict[str, list[tuple[str, float]]] = {m: [] for m in models}
    for a in TAGS[tag]:
        anc = data["anchors"][a]
        pct = percentiles(anc["values"], anc["higher_better"], models)
        for m, p in pct.items():
            per[m].append((a, p))
    rows = []
    for m, lst in per.items():
        if not lst:
            continue
        rows.append((m, sum(p for _a, p in lst) / len(lst), len(lst), [f"{a.split(' (')[0]}:{p:.2f}" for a, p in lst]))
    rows.sort(key=lambda r: -r[1])
    return rows


def claude_gap(data: dict, tag: str) -> list[str]:
    out = []
    for a in TAGS[tag]:
        anc = data["anchors"][a]
        v = anc["values"]
        opus, sonnet = v.get("Claude Opus 5.5"), v.get("Claude Sonnet 5.5")
        if opus is None and sonnet is None:
            continue
        pool = {m: x for m, x in v.items() if not m.startswith("Claude")}
        if not pool:
            continue
        best_m = (max if anc["higher_better"] else min)(pool, key=pool.get)
        ci = anc.get("ci_pm", {})
        out.append(f"{a}: Claude {opus}/{sonnet} vs best open {best_m} {pool[best_m]}"
                   + (f" (published +-{ci.get(best_m)})" if ci.get(best_m) else ""))
    return out


def main() -> int:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    as_json = "--json" in sys.argv
    result = {}
    for tag in TAGS:
        eligible = ROUTABLE + NC1_ONLY + DOMINATED
        rows = consensus(data, tag, eligible)
        lead_pool = [r for r in rows if r[0] in ROUTABLE and r[2] >= MIN_ANCHORS]
        top = lead_pool[0][1] if lead_pool else 0.0
        band = [r[0] for r in lead_pool if top - r[1] <= TIE]
        result[tag] = {"band": band, "ranking": [(m, round(s, 2), n) for m, s, n, _d in rows],
                       "claude": claude_gap(data, tag)}
        if not as_json:
            print(f"\n== {tag}  (anchors: {len(TAGS[tag])}, band = within {TIE:.2f} of the top eligible)")
            for m, s, n, d in rows:
                mark = "*" if m in band else " "
                tier = "" if m in ROUTABLE else ("  [NC1]" if m in NC1_ONLY else "  [dominated]")
                print(f" {mark} {m:22s} {s:.2f}  n={n}  {' '.join(d)}{tier}")
            for line in result[tag]["claude"]:
                print("    claude>", line)
    if as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
