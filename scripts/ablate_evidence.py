#!/usr/bin/env python3
"""Measure how much of the router's ecosystem preference rests on vendor-run evidence.

Phase 1 produced 24 Claude badges against 5 Codex. That is not automatically a
bug -- a 50/50 split is not the goal -- but it is worth knowing *why*. If most of
the Claude lead comes from Anthropic measuring GPT models in Anthropic's own
harness, that is a finding, not a capability.

Three passes over the same evidence:

    full               everything in skill/benchmarks.json
    independent_only   tier B only (benchmark owners and independent evaluators)
    no_cross_vendor    drop rows where a vendor scored a competitor in its own harness

Then diff the per-capability frontier, and roll that up to the live eval corpus
using each eval's declared dominant capability. Evals whose badge comes from a
hard gate, a low-depth efficiency tie-break, or a product mechanism are reported
separately, because no amount of benchmark filtering can move them.

    python scripts/ablate_evidence.py
"""
from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import compile_benchmark_frontiers as C  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
EVALS = ROOT / "evals" / "routing" / "evals.json"

CODEX_MODELS = ["Astra", "GPT-5.6 Sol", "GPT-5.6 Terra", "GPT-5.6 Luna"]


def filters(raw: dict) -> dict:
    """The three evidence views. Each is a pure predicate over a record."""
    eco = raw["model_ecosystem"]
    spans_both: set[str] = set()
    by_group: dict[str, set] = collections.defaultdict(set)
    for r in raw["records"]:
        for name in ("claude", "codex"):
            if r.get("model") in eco[name]:
                by_group[r["comparability_group"]].add(name)
    for gid, ecos in by_group.items():
        if len(ecos) == 2:
            spans_both.add(gid)

    return {
        "full": lambda r: True,
        "independent_only": lambda r: r.get("source_tier") == "B",
        # A vendor's own harness measuring a competitor. Rows where a vendor only
        # measures itself stay -- those are not the cross-ecosystem claim.
        "no_cross_vendor": lambda r: not (
            r.get("vendor_run") and r.get("comparability_group") in spans_both),
    }


def codex_view(frontier: dict) -> dict:
    """capability -> {codex_model -> preferred}."""
    out: dict[str, dict] = {}
    for f in frontier["capability_frontiers"]:
        out[f["capability"]] = {"__overall__": f["preferred"]}
        for m in f["by_codex_model"]:
            out[f["capability"]][m["codex_model"]] = m["preferred"]
    return out


def main() -> int:
    raw, digest = C.load_raw(ROOT / "skill" / "benchmarks.json")
    preds = filters(raw)

    views = {}
    kept = {}
    for name, pred in preds.items():
        views[name] = codex_view(C.build(raw, digest, evidence_filter=pred, filter_name=name))
        kept[name] = sum(1 for r in raw["records"] if pred(r))

    caps = sorted(views["full"])
    print("=" * 92)
    print("PER-CAPABILITY FRONTIER UNDER EACH EVIDENCE VIEW")
    print("=" * 92)
    print("%-22s %-11s %-28s %-28s" % ("capability", "codex model", "full -> independent_only",
                                       "full -> no_cross_vendor"))
    flips = collections.defaultdict(list)
    for cap in caps:
        for model in ["__overall__"] + CODEX_MODELS:
            f_ = views["full"][cap].get(model)
            if f_ is None:
                continue
            i_ = views["independent_only"][cap].get(model, "n/a")
            n_ = views["no_cross_vendor"][cap].get(model, "n/a")
            mark_i = "" if i_ == f_ else "   <-- FLIP"
            mark_n = "" if n_ == f_ else "   <-- FLIP"
            if i_ != f_:
                flips["independent_only"].append((cap, model, f_, i_))
            if n_ != f_:
                flips["no_cross_vendor"].append((cap, model, f_, n_))
            label = "overall" if model == "__overall__" else model.replace("GPT-5.6 ", "")
            print("%-22s %-11s %-28s %-28s" % (
                cap, label, "%s -> %s%s" % (f_, i_, mark_i), "%s -> %s%s" % (f_, n_, mark_n)))

    print()
    print("records kept: " + ", ".join("%s=%d" % (k, v) for k, v in sorted(kept.items())))

    # ---------------------------------------------------------------- corpus
    evals = json.loads(EVALS.read_text(encoding="utf-8"))["evals"]
    live = [e for e in evals if not e.get("format_outdated") and not e.get("blocked")]
    print()
    print("=" * 92)
    print("LIVE EVAL CORPUS (%d badge-bearing evals)" % len(live))
    print("=" * 92)

    counts = {name: collections.Counter() for name in views}
    driver_counts = collections.Counter()
    changed = []
    for e in live:
        driver = e.get("badge_driver", "capability")
        driver_counts[driver] += 1
        expected = e.get("expected_recommended")
        cap = e.get("capability")
        codex_model = e.get("codex_candidate")
        for name in views:
            if driver != "capability" or not cap:
                counts[name][expected] += 1
                continue
            pref = views[name].get(cap, {}).get(codex_model) or views[name].get(cap, {}).get("__overall__")
            if pref in ("claude", "codex"):
                counts[name][pref] += 1
            else:
                # equivalent / UNRESOLVED -> the router falls through to the
                # efficiency tie-break, which this ablation does not re-derive.
                counts[name]["efficiency-decides"] += 1
        if driver == "capability" and cap:
            f_ = views["full"].get(cap, {}).get(codex_model)
            for name in ("independent_only", "no_cross_vendor"):
                o = views[name].get(cap, {}).get(codex_model)
                if o != f_:
                    changed.append((e["id"], cap, codex_model, name, f_, o))

    for name in ("full", "independent_only", "no_cross_vendor"):
        c = counts[name]
        print("%-18s claude=%-3d codex=%-3d efficiency-decides=%-3d" % (
            name, c["claude"], c["codex"], c["efficiency-decides"]))
    print()
    print("badge drivers: " + ", ".join("%s=%d" % kv for kv in sorted(driver_counts.items())))
    print("  only 'capability' evals can move when evidence is filtered; the rest are")
    print("  decided by a hard gate, a D<=1 efficiency tie-break, or a product mechanism.")

    print()
    if changed:
        print("EVALS WHOSE CAPABILITY VERDICT MOVES UNDER A FILTER")
        for eid, cap, model, name, a, b in changed:
            print("  %-4s %-20s vs %-14s %-18s %s -> %s" % (eid, cap, model, name, a, b))
    else:
        print("No live eval's capability verdict moves under either filter.")

    print()
    print("READ THIS AS: a capability that flips when vendor-run rows are removed was")
    print("resting on one vendor's account of a competitor. A capability that does not")
    print("flip is carried by independent evidence and survives the discount.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
