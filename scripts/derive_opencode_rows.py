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
  4. Models within TIE of the top consensus form the *leading band* (printed for audit).
  5. Rule PO1 orders each Step 4-OC pair (iteration-33). Pair membership comes from
     evals/policy/routing_policy.json (check_opencode_pool.py holds it to the top 4 of the
     consensus); the order is derived here, and check_opencode_pool.py fails if the table differs:
       - quality order: the model that may lead (>= MIN_ANCHORS anchors) first, then the higher
         consensus. The right-hand column (D = 3 or R = 3) keeps it: the leader goes first.
       - left column (D <= 2, R <= 2): the leader stays first only if its lead is a direction
         under Rule BD1, read head-to-head on the tag's anchors that rate both models: no anchor
         favours the other model, and either one anchor shows disjoint published intervals
         (Arena ci_pm, the Elo boards' ci_95) or at least two anchors agree. Otherwise the two are
         tied and the more cap-efficient one goes first.
       - cap efficiency = tasks per month = Go monthly limit (the model's weight on the shared
         allowance) / Arena p50 cost per real agent task -- the Step 5 "Go cap pressure
         (cost/task / cap)" quantity. A PROXY: one Arena snapshot, Arena prices are not Go's meter.
         Chosen over Go's own "Est. requests / 5 hr" column because Arena's figure has a published
         method (p50 over real agent tasks, so a verbose model pays for its tokens) while Go's
         estimate assumes a typical request whose token mix is not published; the two agree on
         every tie the table has today (opencode-benchmarks.md section 19).
Where an anchor publishes error margins (DeepSWE) a difference smaller than the combined
margin is reported as a tie, not a ranking.

    python scripts/derive_opencode_rows.py --selftest   # PO1 unit cases (check_opencode_pool runs them too)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "skill" / "opencode-evidence.json"
POLICY = ROOT / "evals" / "policy" / "routing_policy.json"
ARENA = "Arena Agent Arena (net outcome vs avg model, %)"
MIN_ANCHORS = 2
TIE = 0.10  # consensus points that still count as "the same band"

# which anchors feed which capability's consensus (aggregates / partial versions excluded)
TAGS = {
    "agentic-code": ["AA Terminal-Bench 4.0", "DeepSWE v1.1 (Mercor/Datacurve)",
                     "Arena Agent Arena (net outcome vs avg model, %)", "Terminal-Bench 2.1 (Vals)",
                     "Terminal-Bench 4.0 (Vals)",   # iteration-29: wired in (it was in the evidence file since iteration-28 but not read here)
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

# iteration-23 (Rule BUD1): the pair is chosen inside the BUDGET tier. The premium models burn
# 4-10% of their monthly Go cap per real agent task (Arena p50), the budget tier 0.1-0.7% --
# see tasks_per_month in evals/policy/routing_policy.json.
# iteration-27: MiniMax M3.1 Flash Free left Go (the paid MiniMax M3.1 Flash is unrated, so its scores are
# NOT copied from the Free listing) and is no longer routable. Gemini 4 Argon is metered by its USD 30 cap
# and reported next to the premium models (Rule GM1) instead of competing for the budget slot. Kimi K3.1 Pro
# joins the premium reference (A1-OC only).
# iteration-27 Stage 2 (D2+D5): Qwen3.8 Flash is unrated -- AA and Arena publish no row for Go's served
# qwen3.8-flash (1M context); every row under that name is 'Qwen3.8-Flash-Next', a different open-weights
# 256k model, so its benchmark cells are n/p and it never leads or joins a pair.
# iteration-32: Hy4 enters the budget tier (USD 60 cap, 0.54 Arena p50 = 0.9% of cap per task -- budget-class
# cap pressure) and Qwen4 Max the premium reference (USD 15 cap, 1.47 p50 = 9.8% of cap -- premium-class).
# Hy4's rows carry no rung label, so they are n/p for the badge table but feed this consensus (as
# GLM-5.3-Flash's unlabelled rows do). Qwen4 Max is rated but never emitted: it is not in BUD1's budget
# names and A1-OC does not name it yet (its knowledge-work slot swap is a pending judgement call).
ROUTABLE = ["MiMo-V2.6-Pro", "GLM-5.3-Flash", "MiMo-V2.6-Flash", "DeepSeek V4.1 Flash", "Hy4"]
GEMINI = ["Gemini 4 Argon", "Gemini 3.8 Flash"]
NC1_ONLY = ["Muse Spark 1.3", "GPT 6 Luna"]
PREMIUM = ["GLM-5.3", "Kimi K3", "Kimi K3.1 Pro", "Grok 4.7", "Qwen3.8 Max", "Qwen4 Max"]   # A1-OC only; reported, never led with
DOMINATED = ["DeepSeek V4 Pro", "MiniMax M3", "Claude Haiku 5.5"]
UNRATED = ["MiniMax M3.1 Flash",   # AA entity of the Free listing; the paid Go listing is never selected
           "Qwen3.8 Flash"]        # no row for the served model ('Qwen3.8-Flash-Next' rows are n/p for it)


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


def interval(anc: dict, m: str) -> tuple[float, float] | None:
    """Published interval for model m on this anchor, or None (score rows publish none)."""
    if m in (anc.get("ci_95") or {}):
        lo, hi = anc["ci_95"][m]
        return float(lo), float(hi)
    pm = (anc.get("ci_pm") or {}).get(m)
    if pm is not None and m in anc["values"]:
        return anc["values"][m] - pm, anc["values"][m] + pm
    return None


def head_to_head(data: dict, tag: str, a: str, b: str) -> dict:
    """Anchors of the tag that rate both a and b: which way each one points (a's view)."""
    out = {"agree": [], "agree_interval": [], "disagree": [], "tie": []}
    for name in TAGS[tag]:
        anc = data["anchors"][name]
        va, vb = anc["values"].get(a), anc["values"].get(b)
        if va is None or vb is None:
            continue
        ia, ib = interval(anc, a), interval(anc, b)
        short = name.split(" (")[0]
        if ia and ib and not (ia[1] < ib[0] or ib[1] < ia[0]):
            out["tie"].append(short)           # overlapping published intervals: a tie, not opposition
            continue
        if va == vb:
            out["tie"].append(short)
            continue
        a_better = (va > vb) == anc["higher_better"]
        if a_better:
            out["agree"].append(short)
            if ia and ib:
                out["agree_interval"].append(short)
        else:
            out["disagree"].append(short)
    return out


def bd1_direction(h2h: dict) -> bool:
    """Rule BD1 read on a pair: nothing disagrees, and an interval clears or two anchors agree."""
    return not h2h["disagree"] and (len(h2h["agree_interval"]) >= 1 or len(h2h["agree"]) >= 2)


def tasks_per_month(data: dict, policy: dict, m: str) -> float:
    """PO1's efficiency proxy: Go monthly limit / Arena p50 cost per real agent task."""
    cap = policy["pool"]["models"][m]["cap_usd"]
    p50 = data["anchors"][ARENA]["cost_per_task_p50_usd"].get(m)
    return cap / p50 if (cap and p50) else 0.0


def quality_order(data: dict, tag: str, pair: list[str]) -> list[str]:
    models = list(dict.fromkeys(ROUTABLE + NC1_ONLY + pair))   # the band's percentile frame (main())
    score = {m: (s, n) for m, s, n, _d in consensus(data, tag, models)}

    def key(m: str):
        s, n = score.get(m, (0.0, 0))
        return (n >= MIN_ANCHORS, round(s, 6), n, -pair.index(m))
    return sorted(pair, key=key, reverse=True)


def po1_order(data: dict, policy: dict, tag: str, pair: list[str], column: str) -> tuple[list[str], str]:
    """Rule PO1. column 'left' = D <= 2 and R <= 2; 'right' = D = 3 or R = 3."""
    tag = "agentic-code" if tag == "terminal-tool" else tag
    q1, q2 = quality_order(data, tag, pair)
    if column == "right":
        return [q1, q2], "leader first"
    h = head_to_head(data, tag, q1, q2)
    if bd1_direction(h):
        return [q1, q2], f"BD1 direction for {q1} ({', '.join(h['agree'])})"
    e1, e2 = tasks_per_month(data, policy, q1), tasks_per_month(data, policy, q2)
    first = [q2, q1] if e2 > e1 else [q1, q2]
    return first, (f"tie (agree {h['agree'] or '-'}, disagree {h['disagree'] or '-'}) -> cap-efficient first "
                   f"({first[0]} {max(e1, e2):.0f} vs {min(e1, e2):.0f} tasks/mo)")


def selftest() -> list[str]:
    """PO1 unit cases on synthetic data; returns the failures (empty = pass)."""
    anc = lambda vals, **kw: {"values": vals, "higher_better": True, **kw}  # noqa: E731
    pol = {"pool": {"models": {"X": {"cap_usd": 15}, "Y": {"cap_usd": 100}}}}
    cases = [
        # (anchors, left order expected, right order expected (None = no clear leader), why)
        ({"A1": anc({"X": 50, "Y": 40}), "A2": anc({"X": 30, "Y": 20})}, ["X", "Y"], ["X", "Y"],
         "two agreeing anchors"),
        ({"A1": anc({"X": 50, "Y": 40}), "A2": anc({"X": 10})}, ["Y", "X"], ["X", "Y"],
         "one shared anchor -> tie -> efficient first; X alone may lead"),
        ({"A1": anc({"X": 50, "Y": 40}), "A2": anc({"X": 20, "Y": 30})}, ["Y", "X"], None,
         "split -> tie -> efficient first"),
        ({"A1": anc({"X": 5.0, "Y": 1.0}, ci_pm={"X": 1.0, "Y": 1.0}), "A2": anc({"X": 9})}, ["X", "Y"], ["X", "Y"],
         "disjoint published interval"),
        ({"A1": anc({"X": 5.0, "Y": 4.0}, ci_pm={"X": 1.0, "Y": 1.0}), "A2": anc({"X": 9, "Y": 8}),
          "A3": anc({"X": 7, "Y": 6})}, ["X", "Y"], ["X", "Y"], "overlap is a tie, not opposition; two others agree"),
    ]
    fails = []
    for anchors, want, want_right, why in cases:
        data = {"anchors": {**anchors, ARENA: {"values": {}, "higher_better": True,
                                               "cost_per_task_p50_usd": {"X": 0.15, "Y": 0.15}}}}
        TAGS["_selftest"] = list(anchors)
        got, _ = po1_order(data, pol, "_selftest", ["X", "Y"], "left")
        right, _ = po1_order(data, pol, "_selftest", ["Y", "X"], "right")
        if got != want:
            fails.append(f"PO1 selftest '{why}': left {got}, want {want}")
        if want_right and right != want_right:
            fails.append(f"PO1 selftest '{why}': right column {right}, want {want_right}")
    TAGS.pop("_selftest", None)
    return fails


def claude_gap(data: dict, tag: str) -> list[str]:
    out = []
    for a in TAGS[tag]:
        anc = data["anchors"][a]
        v = anc["values"]
        opus, sonnet = v.get("Claude Opus 5.5"), v.get("Claude Sonnet 5.5")
        if opus is None and sonnet is None:
            continue
        pool = {m: x for m, x in v.items() if m in ROUTABLE or m in NC1_ONLY}
        if not pool:
            continue
        pick = max if anc["higher_better"] else min
        best_m = pick(pool, key=pool.get)
        ci = anc.get("ci_pm", {})
        prem = {m: x for m, x in v.items() if m in PREMIUM}
        prem_txt = ""
        if prem:
            pm = pick(prem, key=prem.get)
            if (prem[pm] > pool[best_m]) == anc["higher_better"] and prem[pm] != pool[best_m]:
                prem_txt = f"; premium {pm} {prem[pm]}"
        out.append(f"{a}: Claude {opus}/{sonnet} vs best budget {best_m} {pool[best_m]}"
                   + (f" (published +-{ci.get(best_m)})" if ci.get(best_m) else "") + prem_txt)
    return out


def main() -> int:
    if "--selftest" in sys.argv:
        fails = selftest()
        print("\n".join(fails) if fails else "PO1 selftest: all cases pass")
        return 1 if fails else 0
    data = json.loads(DATA.read_text(encoding="utf-8"))
    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    as_json = "--json" in sys.argv
    result = {}
    for tag in TAGS:
        # the budget tier competes for the slot: percentiles are taken inside it (+ NC1 models)
        eligible = ROUTABLE + NC1_ONLY
        rows = consensus(data, tag, eligible)
        lead_pool = [r for r in rows if r[0] in ROUTABLE and r[2] >= MIN_ANCHORS]
        top = lead_pool[0][1] if lead_pool else 0.0
        band = [r[0] for r in lead_pool if top - r[1] <= TIE]
        po1 = {}
        row = policy["step4_oc_rows"].get(tag)
        if row:
            for col, key in (("left", "r_le_2"), ("right", "r_eq_3")):
                order, why = po1_order(data, policy, tag, row[key], col)
                po1[col] = {"order": order, "why": why}
        result[tag] = {"band": band, "ranking": [(m, round(s, 2), n) for m, s, n, _d in rows],
                       "po1": po1, "claude": claude_gap(data, tag)}
        if not as_json:
            print(f"\n== {tag}  (anchors: {len(TAGS[tag])}, band = within {TIE:.2f} of the top eligible)")
            for m, s, n, d in rows:
                mark = "*" if m in band else " "
                tier = "" if m in ROUTABLE else "  [NC1]"
                print(f" {mark} {m:22s} {s:.2f}  n={n}  {' '.join(d)}{tier}")
            ref = consensus(data, tag, ROUTABLE + NC1_ONLY + PREMIUM + DOMINATED)
            prem = [f"{m} {sc:.2f}" for m, sc, _n, _d in ref if m in PREMIUM][:4]
            print("    premium reference (A1-OC only, percentiles over the full pool):", ", ".join(prem))
            gem = consensus(data, tag, ROUTABLE + NC1_ONLY + GEMINI)
            gtxt = [f"{m} {sc:.2f} (n={n})" for m, sc, n, _d in gem if m in GEMINI]
            print("    gemini reference (Rule GM1, percentiles with the budget tier):", ", ".join(gtxt) or "no row")
            for col, v in po1.items():
                print(f"    PO1 {col:5s}> {' · '.join(v['order'])}   [{v['why']}]")
            for line in result[tag]["claude"]:
                print("    claude>", line)
    if as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
