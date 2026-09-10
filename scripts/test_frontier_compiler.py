#!/usr/bin/env python3
"""Deterministic unit tests for the frontier compiler's comparison semantics.

These are the cases the routing evals cannot reach. "Two scores whose confidence
intervals overlap" is not a prompt you can hand a cold agent -- it is a property
of the compiler, and it is far better tested here, exactly, than inferred from a
routing decision three layers downstream.

No network, no LLM, no fixtures on disk. Run:

    python scripts/test_frontier_compiler.py
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import compile_benchmark_frontiers as C  # noqa: E402

FAILURES: list[str] = []


def check(name: str, got, want) -> None:
    if got != want:
        FAILURES.append("%s\n     got:  %r\n     want: %r" % (name, got, want))
        print("FAIL  %s" % name)
    else:
        print("ok    %s" % name)


def base_meta(**over) -> dict:
    meta = {
        "evidence_classes": {k: "" for k in
                             ("model_intrinsic", "ecosystem_end_to_end", "vendor_relative",
                              "aggregate", "efficiency_only", "unclassified")},
        "evidence_precedence": {"order": [
            {"class": "model_intrinsic", "source_tier": "B", "weight": 4},
            {"class": "ecosystem_end_to_end", "source_tier": "B", "weight": 4},
            {"class": "vendor_relative", "source_tier": "A", "weight": 2},
            {"class": "vendor_relative", "source_tier": "C", "weight": 1},
            {"class": "aggregate", "source_tier": "B", "weight": 1},
            {"class": "unclassified", "source_tier": "*", "weight": 0},
        ]},
        "model_ecosystem": {
            "claude": ["Opus 5", "Fable 5.1"],
            "codex": ["Astra", "GPT-5.6 Sol"],
            "current_roster": ["Opus 5", "Fable 5.1", "Astra", "GPT-5.6 Sol"],
        },
        "no_dispersion_rule": {"min_fraction_of_spread": 0.15},
        "effort_rung_order": ["low", "medium", "high", "xhigh", "max"],
        "comparability_groups": {},
        "excluded_from_direction": [],
        "records": [],
        "routing_rules": {"rules": []},
        "compiled": "2026-09-10",
    }
    meta.update(over)
    return meta


def row(rid, model, score, group="g", bench="B", ver="1", **extra):
    r = {"id": rid, "model": model, "score": score, "score_unit": "percent",
         "benchmark": bench, "benchmark_version": ver, "capability": "cap",
         "comparability_group": group, "evidence_class": "model_intrinsic",
         "source_tier": "B", "harness": "H", "effort": None, "vendor_run": False}
    r.update(extra)
    return r


def group(cls="model_intrinsic", tier="B", saturated=False, band=None):
    return {"description": "", "evidence_class": cls, "source_tier": tier,
            "saturated": saturated, "equivalence_band": band or {"kind": "none"}}


def direction(meta, cap="cap"):
    return C.compile_capability(cap, meta["records"], meta)


# ---------------------------------------------------------------- CI overlap
m = base_meta()
m["comparability_groups"] = {"g": group(band={"kind": "published_ci", "value": 5.0})}
m["records"] = [row("a", "Opus 5", 70.0), row("b", "Astra", 73.0), row("c", "GPT-5.6 Sol", 60.0)]
f = direction(m)
check("CI-overlapping gap (3.0) inside a published 5.0 CI -> equivalent",
      f["comparisons"][0]["direction"], "equivalent")
check("  ...and the caller is told to fall through to efficiency",
      f["efficiency_tiebreak_required"], True)

# ------------------------------------------------------------ CI no overlap
m = base_meta()
m["comparability_groups"] = {"g": group(band={"kind": "published_ci", "value": 2.0})}
m["records"] = [row("a", "Opus 5", 70.0), row("b", "Astra", 73.0), row("c", "GPT-5.6 Sol", 60.0)]
check("CI-non-overlapping gap (3.0) outside a published 2.0 CI -> a winner",
      direction(m)["comparisons"][0]["direction"], "codex")

# ------------------------------- published SE is doubled into a 95% interval
m = base_meta()
m["comparability_groups"] = {"g": group(band={"kind": "published_se", "value": 2.0})}
m["records"] = [row("a", "Opus 5", 70.0), row("b", "Astra", 73.0), row("c", "GPT-5.6 Sol", 60.0)]
c0 = direction(m)["comparisons"][0]
check("published SE 2.0 becomes a 4.0 band (95% convention)", c0["band"], 4.0)
check("  ...so a 3.0 gap is equivalent", c0["direction"], "equivalent")

# ------------------------------- an SE published for a DIFFERENT benchmark
m = base_meta()
m["comparability_groups"] = {"g": group(band={"kind": "published_se", "value": 2.0,
                                              "applies_to": ["OtherBench"]})}
m["records"] = [row("a", "Opus 5", 70.0), row("b", "Astra", 73.0), row("c", "GPT-5.6 Sol", 60.0)]
c0 = direction(m)["comparisons"][0]
check("an SE published for another benchmark does NOT carry over",
      c0["band_basis"], "spread_rule_0.15")

# ------------------------------------------------ same score, different cost
m = base_meta()
m["comparability_groups"] = {"g": group()}
m["records"] = [row("a", "Fable 5.1", 62.0, cost_per_task_usd=7.63),
                row("b", "Astra", 62.0, cost_per_task_usd=3.26),
                row("c", "GPT-5.6 Sol", 55.0, cost_per_task_usd=1.99)]
f = direction(m)
check("same score / different cost -> equivalent, not a cost-based winner",
      f["comparisons"][0]["direction"], "equivalent")
check("  ...and efficiency is explicitly handed the decision",
      f["efficiency_tiebreak_required"], True)

# ------------------------------------------------ same cost, real score gap
m = base_meta()
m["comparability_groups"] = {"g": group()}
m["records"] = [row("a", "Fable 5.1", 52.0, cost_per_task_usd=3.00),
                row("b", "Astra", 59.0, cost_per_task_usd=3.00),
                row("c", "GPT-5.6 Sol", 40.0, cost_per_task_usd=3.00)]
check("same cost / meaningful score gap -> the stronger side wins",
      direction(m)["comparisons"][0]["direction"], "codex")

# ------------------------------------------- vendor disagreement, precedence
m = base_meta()
m["comparability_groups"] = {
    "indep": group("model_intrinsic", "B"),
    "vend": group("vendor_relative", "A"),
}
m["records"] = [
    row("i1", "Fable 5.1", 52.0, group="indep"), row("i2", "Astra", 59.0, group="indep"),
    row("i3", "GPT-5.6 Sol", 40.0, group="indep"),
    row("v1", "Fable 5.1", 55.8, group="vend", evidence_class="vendor_relative",
        source_tier="A", vendor_run=True),
    row("v2", "GPT-5.6 Sol", 37.3, group="vend", evidence_class="vendor_relative",
        source_tier="A", vendor_run=True),
]
f = direction(m)
check("independent (w4) beats a disagreeing vendor table (w2)", f["preferred"], "codex")
check("  ...and says so in the rationale", "codex=4" in f["rationale"], True)

# --------------------------------------- vendor disagreement, precedence tie
m = base_meta()
m["comparability_groups"] = {"a": group("vendor_relative", "A"), "b": group("vendor_relative", "A")}
m["records"] = [
    row("a1", "Fable 5.1", 80.0, group="a", evidence_class="vendor_relative", source_tier="A"),
    row("a2", "Astra", 60.0, group="a", evidence_class="vendor_relative", source_tier="A"),
    row("b1", "Fable 5.1", 60.0, group="b", evidence_class="vendor_relative", source_tier="A"),
    row("b2", "Astra", 80.0, group="b", evidence_class="vendor_relative", source_tier="A"),
]
f = direction(m)
check("two equally-weighted vendor tables pointing opposite ways -> UNRESOLVED",
      f["preferred"], "UNRESOLVED")
check("  ...never an average of the two", f["confidence"], "none")

# ------------------------------------------------------------- saturation
m = base_meta()
m["comparability_groups"] = {"g": group(saturated=True)}
m["records"] = [row("a", "Fable 5.1", 85.02), row("b", "Astra", 87.27),
                row("c", "GPT-5.6 Sol", 85.77)]
check("a group declared saturated sets no direction",
      direction(m)["comparisons"][0]["direction"], "UNRESOLVED")

# --------------------------------------------------------- single ecosystem
m = base_meta()
m["comparability_groups"] = {"g": group()}
m["records"] = [row("a", "Fable 5.1", 65.0), row("b", "Opus 5", 63.6)]
check("a group with only one ecosystem sets no direction",
      direction(m)["comparisons"][0]["direction"], "UNRESOLVED")

# ------------------------------------------------------ declared exclusion
m = base_meta()
m["comparability_groups"] = {"g": group()}
m["excluded_from_direction"] = [{"benchmark": "B", "benchmark_version": None, "reason": "funded by a party"}]
m["records"] = [row("a", "Fable 5.1", 20.0), row("b", "Astra", 90.0), row("c", "GPT-5.6 Sol", 10.0)]
c0 = direction(m)["comparisons"][0]
check("a declared exclusion beats even a huge gap", c0["direction"], "UNRESOLVED")
check("  ...and records why", c0["reason"].startswith("declared excluded:"), True)

# ------------------------------- two benchmarks in one source are NOT pooled
m = base_meta()
m["comparability_groups"] = {"g": group("vendor_relative", "C")}
m["records"] = [
    row("h1", "Fable 5.1", 65.0, bench="HLE", evidence_class="vendor_relative", source_tier="C"),
    row("h2", "Astra", 57.2, bench="HLE", evidence_class="vendor_relative", source_tier="C"),
    row("f1", "Fable 5.1", 87.8, bench="FrontierMath", evidence_class="vendor_relative", source_tier="C"),
    row("f2", "Astra", 97.6, bench="FrontierMath", evidence_class="vendor_relative", source_tier="C"),
]
f = direction(m)
check("one source publishing two benchmarks yields two cells, not one pooled score",
      len(f["comparisons"]), 2)
check("  ...pointing opposite ways, so the capability is UNRESOLVED",
      f["preferred"], "UNRESOLVED")

# ------------------------------------------- model-conditional disagreement
m = base_meta()
m["comparability_groups"] = {"g": group()}
m["records"] = [row("a", "Fable 5.1", 52.0), row("b", "Astra", 59.0), row("c", "GPT-5.6 Sol", 40.0)]
by = {x["codex_model"]: x["preferred"] for x in direction(m)["by_codex_model"]}
check("the same capability can favour Claude against one Codex model...",
      by["GPT-5.6 Sol"], "claude")
check("  ...and Codex against another", by["Astra"], "codex")

# ------------------------- a two-row subset must not shrink the band
m = base_meta()
m["comparability_groups"] = {"g": group()}
m["records"] = [row("a", "Fable 5.1", 55.8), row("b", "Astra", 57.7),
                row("c", "GPT-5.6 Sol", 37.3), row("d", "Opus 5", 52.3)]
sub = [x for x in direction(m)["by_codex_model"] if x["codex_model"] == "Astra"][0]
check("band comes from the full cell, so a 1.9 gap stays equivalent in a 2-model view",
      sub["cells"][0]["direction"], "equivalent")

# ------------------------------------------------- no effort interpolation
m = base_meta()
m["comparability_groups"] = {"g": group()}
m["records"] = [
    row("e1", "Astra", 51.0, effort="high", cost_per_task_usd=1.72),
    row("e3", "Astra", 53.0, effort="max", cost_per_task_usd=3.26),
]
curve = C.compile_effort_curves(m["records"], m)[0]
check("a rung that was never published does not appear in the curve",
      [p["effort"] for p in curve["points"]], ["high", "max"])
check("  ...specifically, no xhigh is invented between them",
      any(p["effort"] == "xhigh" for p in curve["points"]), False)

# ---------------------------------------- a higher rung that buys nothing
m = base_meta()
m["comparability_groups"] = {"g": group()}
m["records"] = [
    row("x1", "Astra", 53.0, effort="xhigh", cost_per_task_usd=2.31),
    row("x2", "Astra", 53.0, effort="max", cost_per_task_usd=3.26),
    row("x3", "Astra", 40.0, effort="low", cost_per_task_usd=0.82),
]
curve = C.compile_effort_curves(m["records"], m)[0]
check("a higher rung with no score gain and a higher cost is marked dominated",
      [d["rung"] for d in curve["dominated_rungs"]], ["max"])

# ------------------------------------------------------------ determinism
m = base_meta()
m["comparability_groups"] = {"g": group()}
m["records"] = [row("a", "Fable 5.1", 52.0), row("b", "Astra", 59.0)]
a = C.dumps(C.build(copy.deepcopy(m), "deadbeef"))
b = C.dumps(C.build(copy.deepcopy(m), "deadbeef"))
check("two builds of identical input are byte-identical", a, b)

print()
if FAILURES:
    print("%d FAILURE(S)" % len(FAILURES))
    for f_ in FAILURES:
        print("  - " + f_)
    sys.exit(1)
print("all frontier-compiler tests passed")
