#!/usr/bin/env python3
"""Compile skill/benchmarks.json into skill/benchmark_frontiers.json.

Three layers, kept apart on purpose:

    RAW EVIDENCE      skill/benchmarks.json        hand-maintained, 100+ records
    DERIVED FRONTIER  skill/benchmark_frontiers.json   GENERATED, never hand-edited
    RUNTIME RULE      skill/SKILL.md               prose the router actually reads

The router reads neither of the first two at runtime. This compiler exists so the
path from a raw score to a routing rule is mechanical and auditable instead of a
judgement call buried in prose.

The hard constraint on this script: **it never interprets a number on its own.**
Every threshold, every grouping, every precedence weight is DECLARED in
benchmarks.json. Where the declared metadata does not settle a comparison, the
output is UNRESOLVED. It never averages, never splits a difference, never prefers
the newer number, and never fills a missing effort rung.

Usage:
    python scripts/compile_benchmark_frontiers.py            # write the frontier
    python scripts/compile_benchmark_frontiers.py --check    # fail if stale
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
from pathlib import Path

GENERATOR_VERSION = "1.1"

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "skill" / "benchmarks.json"
OUT = ROOT / "skill" / "benchmark_frontiers.json"

# Directions a comparison can land on. UNRESOLVED is a first-class outcome.
CLAUDE, CODEX, EQUIVALENT, UNRESOLVED = "claude", "codex", "equivalent", "UNRESOLVED"


def load_raw(path: Path) -> tuple[dict, str]:
    """Return the parsed evidence store and the sha256 of its exact bytes."""
    data = path.read_bytes()
    return json.loads(data.decode("utf-8")), hashlib.sha256(data).hexdigest()


def ecosystem_of(model: str, eco_map: dict) -> str | None:
    for eco in (CLAUDE, CODEX):
        if model in eco_map[eco]:
            return eco
    return None


def precedence_weight(cls: str, tier: str, table: list) -> int:
    """Declared weight for an (evidence_class, source_tier) pair. Unlisted -> 0."""
    for row in table:
        if row["class"] == cls and row["source_tier"] in (tier, "*"):
            return row["weight"]
    return 0


# The ONLY things that may set a direction, in order. Anything else -> UNRESOLVED.
#
# What is deliberately NOT here: a fraction of the roster's observed score spread.
# Until this pass the compiler fell back to `0.15 * spread` whenever no dispersion
# was published, which reads as statistics and is not: spread is how far apart the
# models happen to sit, not how precisely either score was measured. On a cell
# where four models span 40-59 it declares any gap over ~2.9 points a win, and on
# a two-row cell it would call every comparison a win. Removing it turns most
# cells UNRESOLVED, which is the honest answer -- "not published" already is one
# everywhere else in this repo.
DIRECTION_BASIS = ("published_ci", "published_se", "repeated_trial_variance",
                   "owner_practical_threshold")


def band_for(group: dict, benchmark: str, rule: dict, spread: float) -> tuple[float | None, str]:
    """The equivalence band for one comparability group, from declared metadata only.

    Returns (band, basis). band is None whenever the declared metadata gives no
    MEASURE OF UNCERTAINTY, which the caller treats as UNRESOLVED. Observed spread
    is carried through the output as a diagnostic and never used here.
    """
    eb = group.get("equivalence_band") or {"kind": "none"}
    kind = eb.get("kind")
    value = eb.get("value")
    if kind not in DIRECTION_BASIS or value is None:
        return None, "no_published_dispersion"
    applies = eb.get("applies_to")
    if applies is not None and benchmark not in applies:
        # Dispersion published for a different benchmark in the same group does
        # not carry over to this one.
        return None, "dispersion_published_for_another_benchmark"
    if kind == "published_ci":
        return float(value), "published_ci"
    if kind == "published_se":
        # 95% interval from a standard error, the conventional multiplier.
        return 2.0 * float(value), "published_se_x2"
    if kind == "repeated_trial_variance":
        # A standard deviation over repeated runs under one harness, same convention.
        return 2.0 * float(value), "repeated_trial_sd_x2"
    return float(value), "owner_practical_threshold"


def excluded_reason(benchmark: str, version, table: list) -> str | None:
    """Declared per-benchmark exclusions. A cell listed here can never set a direction."""
    for row in table:
        if row["benchmark"] != benchmark:
            continue
        if row.get("benchmark_version") not in (None, version):
            continue
        return row["reason"]
    return None


def compare_group(rows: list, group: dict, eco_map: dict, rule: dict,
                  spread_override: float | None = None, excluded: list | None = None) -> dict:
    """Compare the two ecosystems inside ONE (group, benchmark, version) cell.

    A comparability group asserts a constant evaluator and harness, but a single
    source often publishes several DIFFERENT benchmarks under that one harness.
    Those are not comparable with each other, so the caller splits by benchmark
    and version before calling this. Without that split the compiler would happily
    compare an ARC-AGI-3 score against an HLE score.
    """
    best: dict[str, dict] = {}
    for r in rows:
        eco = ecosystem_of(r["model"], eco_map)
        if eco is None:
            continue
        if eco not in best or r["score"] > best[eco]["score"]:
            best[eco] = r
    scores = [r["score"] for r in rows if ecosystem_of(r["model"], eco_map)]
    # The band describes how discriminating the BENCHMARK is, so it is always taken
    # from the full cell. Looking at a two-model subset must not shrink it -- with
    # two rows the spread is the gap itself and every comparison would "win".
    spread = spread_override if spread_override is not None else (
        (max(scores) - min(scores)) if len(scores) >= 2 else 0.0)

    out = {
        "cell": "%s | %s%s" % (rows[0]["comparability_group"], rows[0]["benchmark"],
                               " " + rows[0]["benchmark_version"] if rows[0].get("benchmark_version") else ""),
        "group": rows[0]["comparability_group"],
        "benchmark": rows[0]["benchmark"],
        "benchmark_version": rows[0].get("benchmark_version"),
        "evidence_class": group["evidence_class"],
        "source_tier": group["source_tier"],
        "observed_spread": round(spread, 4),
        "rows": sorted(r["id"] for r in rows),
    }

    why_excluded = excluded_reason(out["benchmark"], out["benchmark_version"], excluded or [])
    if why_excluded:
        out["direction"] = UNRESOLVED
        out["reason"] = "declared excluded: " + why_excluded
        return out
    if group.get("saturated"):
        out["direction"] = UNRESOLVED
        out["reason"] = "group declared saturated -- differences are compressed, ranking not robust"
        return out
    if len(best) < 2:
        out["direction"] = UNRESOLVED
        out["reason"] = "only one ecosystem present in this group"
        return out

    band, basis = band_for(group, out["benchmark"], rule, spread)
    gap = best[CLAUDE]["score"] - best[CODEX]["score"]
    out["best"] = {eco: {"model": r["model"], "score": r["score"], "id": r["id"]}
                   for eco, r in sorted(best.items())}
    out["gap_claude_minus_codex"] = round(gap, 4)
    # DIAGNOSTIC ONLY. How the gap compares with how far apart the roster happens
    # to sit. Useful for spotting a cell worth chasing a published CI for. It is
    # not a confidence statement and never sets `direction`.
    out["gap_over_observed_spread_diagnostic"] = (
        None if spread <= 0 else round(abs(gap) / spread, 4))
    out["band"] = None if band is None else round(band, 4)
    out["band_basis"] = basis

    if gap == 0:
        # Equality is not an inference, so it needs no interval. This keeps the
        # "same score, different cost" case alive -- the router must still be told
        # to fall through to the efficiency tie-break there.
        out["direction"] = EQUIVALENT
        out["reason"] = "identical scores; efficiency decides"
    elif band is None:
        out["direction"] = UNRESOLVED
        out["reason"] = ("no measure of uncertainty is published for this cell (%s), so the gap "
                         "sets no direction -- see DIRECTION_BASIS" % basis)
    elif abs(gap) <= band:
        out["direction"] = EQUIVALENT
        out["reason"] = "gap %.4g is inside the %.4g band" % (gap, band)
    else:
        out["direction"] = CLAUDE if gap > 0 else CODEX
        out["reason"] = "gap %.4g exceeds the %.4g band" % (gap, band)
    return out


def compile_capability(cap: str, records: list, meta: dict) -> dict:
    """Roll every comparability group covering `cap` up into one frontier entry."""
    eco_map = meta["model_ecosystem"]
    roster = set(eco_map["current_roster"])
    groups_meta = meta["comparability_groups"]
    prec = meta["evidence_precedence"]["order"]
    rule = meta["direction_setting_hierarchy"]

    # Cell = (comparability group, benchmark, version). One source publishing five
    # benchmarks yields five cells, never one pooled comparison.
    cells: dict[tuple, list] = {}
    for r in records:
        if r.get("score") is None or not r.get("model"):
            continue
        if r["model"] not in roster:
            continue
        if cap not in [c.strip() for c in (r.get("capability") or "").split(",")]:
            continue
        key = (r["comparability_group"], r["benchmark"], r.get("benchmark_version") or "")
        cells.setdefault(key, []).append(r)

    excluded = meta.get("excluded_from_direction", [])
    comparisons = []
    for key in sorted(cells):
        gmeta = groups_meta.get(key[0])
        if gmeta is None:
            continue
        comparisons.append(compare_group(cells[key], gmeta, eco_map, rule, excluded=excluded))

    tally: dict[str, int] = {}
    for c in comparisons:
        if c["direction"] == UNRESOLVED:
            continue
        w = precedence_weight(c["evidence_class"], c["source_tier"], prec)
        tally[c["direction"]] = tally.get(c["direction"], 0) + w

    ranked = sorted(tally.items(), key=lambda kv: (-kv[1], kv[0]))
    if not ranked or ranked[0][1] == 0:
        preferred, confidence = UNRESOLVED, "none"
        why = "no comparison in any group carried a non-zero precedence weight"
    elif len(ranked) > 1 and ranked[0][1] - ranked[1][1] < 1:
        preferred, confidence = UNRESOLVED, "none"
        why = "groups disagree and no precedence step separates them (%s)" % (
            ", ".join("%s=%d" % kv for kv in ranked))
    else:
        preferred = ranked[0][0]
        margin = ranked[0][1] - (ranked[1][1] if len(ranked) > 1 else 0)
        confidence = "high" if margin >= 4 else "medium" if margin >= 2 else "low"
        why = "precedence-weighted tally %s" % ", ".join("%s=%d" % kv for kv in ranked)

    basis = sorted({c["group"] for c in comparisons if c["direction"] != UNRESOLVED})
    return {
        "capability": cap,
        "preferred": preferred,
        "confidence": confidence,
        "rationale": why,
        "basis_groups": basis,
        "efficiency_tiebreak_required": preferred in (EQUIVALENT, UNRESOLVED),
        "by_codex_model": compile_by_codex_model(cap, cells, meta),
        "comparisons": comparisons,
    }


def compile_by_codex_model(cap: str, cells: dict, meta: dict) -> list:
    """The same roll-up, but conditioned on WHICH Codex model is on the line.

    'Best Claude vs best Codex' is the wrong question for a router: the Codex
    candidate is usually Terra or Sol, and Astra only appears behind a gate. A
    capability can genuinely favour Claude against Sol and not against Astra, and
    collapsing that into one verdict is how a badge ends up wrong half the time.
    """
    eco_map = meta["model_ecosystem"]
    groups_meta = meta["comparability_groups"]
    prec = meta["evidence_precedence"]["order"]
    rule = meta["direction_setting_hierarchy"]

    excluded = meta.get("excluded_from_direction", [])

    def full_spread(rows):
        sc = [r["score"] for r in rows if ecosystem_of(r["model"], eco_map)]
        return (max(sc) - min(sc)) if len(sc) >= 2 else 0.0

    out = []
    for codex_model in [m for m in eco_map["codex"] if m in eco_map["current_roster"]]:
        tally: dict[str, int] = {}
        used = []
        for key in sorted(cells):
            rows = cells[key]
            gmeta = groups_meta.get(key[0])
            if gmeta is None:
                continue
            subset = [r for r in rows
                      if ecosystem_of(r["model"], eco_map) == CLAUDE or r["model"] == codex_model]
            if not any(r["model"] == codex_model for r in subset):
                continue
            if not any(ecosystem_of(r["model"], eco_map) == CLAUDE for r in subset):
                continue
            c = compare_group(subset, gmeta, eco_map, rule,
                              spread_override=full_spread(rows), excluded=excluded)
            used.append({"cell": c["cell"], "direction": c["direction"], "reason": c["reason"],
                         "best": c.get("best")})
            if c["direction"] == UNRESOLVED:
                continue
            tally[c["direction"]] = tally.get(c["direction"], 0) + precedence_weight(
                gmeta["evidence_class"], gmeta["source_tier"], prec)
        if not used:
            continue
        ranked = sorted(tally.items(), key=lambda kv: (-kv[1], kv[0]))
        if not ranked or ranked[0][1] == 0:
            preferred, confidence = UNRESOLVED, "none"
        elif len(ranked) > 1 and ranked[0][1] - ranked[1][1] < 1:
            preferred, confidence = UNRESOLVED, "none"
        else:
            preferred = ranked[0][0]
            margin = ranked[0][1] - (ranked[1][1] if len(ranked) > 1 else 0)
            confidence = "high" if margin >= 4 else "medium" if margin >= 2 else "low"
        out.append({
            "codex_model": codex_model,
            "preferred": preferred,
            "confidence": confidence,
            "tally": dict(sorted(tally.items())),
            "cells": used,
        })
    return out


def compile_effort_curves(records: list, meta: dict) -> list:
    """Per-model effort curves, within one comparability group only.

    A rung is marked dominated when a LOWER rung in the same group costs less and
    scores NO BETTER. That needs no equivalence band -- a gain of zero or below is
    not a measurement question -- which is why removing the spread fallback does
    not disarm Rules E1 and E3: their evidence is a tie or a loss at higher cost,
    not a small positive gap talked down.

    A gain that is positive but small goes to `unresolved_rungs` instead, where it
    stays until somebody publishes an interval for the benchmark. Calling it
    dominated would be exactly the manufactured confidence this pass removed.

    No interpolation: a rung that was never published simply does not appear.
    """
    rule = meta["direction_setting_hierarchy"]
    groups_meta = meta["comparability_groups"]
    roster = set(meta["model_ecosystem"]["current_roster"])
    order = meta["effort_rung_order"]

    buckets: dict[tuple, list] = {}
    for r in records:
        if r.get("score") is None or not r.get("model") or r.get("effort") is None:
            continue
        if r["model"] not in roster or r["effort"] not in order:
            continue
        buckets.setdefault((r["model"], r["comparability_group"]), []).append(r)

    curves = []
    for (model, gid) in sorted(buckets):
        rows = buckets[(model, gid)]
        if len(rows) < 2:
            continue
        gmeta = groups_meta.get(gid)
        if gmeta is None:
            continue
        rows.sort(key=lambda r: order.index(r["effort"]))
        scores = [r["score"] for r in rows]
        spread = max(scores) - min(scores)
        band, basis = band_for(gmeta, rows[0]["benchmark"], rule, spread)
        points = [{"effort": r["effort"], "score": r["score"],
                   "cost_per_task_usd": r.get("cost_per_task_usd"),
                   "id": r["id"]} for r in rows]
        dominated, unresolved = [], []
        for i, hi in enumerate(rows):
            dom = unres = None
            for lo in rows[:i]:
                gain = hi["score"] - lo["score"]
                hc, lc = hi.get("cost_per_task_usd"), lo.get("cost_per_task_usd")
                if hc is None or lc is None or hc <= lc:
                    continue
                entry = {
                    "rung": hi["effort"], "dominated_by": lo["effort"],
                    "score_gain": round(gain, 4), "band": None if band is None else round(band, 4),
                    "cost_delta_usd": round(hc - lc, 4), "ids": [hi["id"], lo["id"]],
                }
                if gain <= 0:
                    entry["basis"] = "no_gain_at_higher_cost"
                    dom = entry
                    break
                if band is not None and gain <= band:
                    entry["basis"] = "gain_inside_published_band"
                    dom = entry
                    break
                # Positive gain with nothing to say whether it is real. Keep looking
                # for a lower rung that actually dominates; if none does, the closest
                # lower rung is the most informative thing to report.
                entry["basis"] = "positive_gain_no_published_dispersion"
                unres = entry
            if dom is not None:
                dominated.append(dom)
            elif unres is not None:
                unresolved.append(unres)
        curves.append({
            "model": model, "group": gid, "band": None if band is None else round(band, 4),
            "band_basis": basis, "points": points, "dominated_rungs": dominated,
            "unresolved_rungs": unresolved,
        })
    return curves


def compile_rule_provenance(meta: dict, by_id: dict) -> list:
    out = []
    for rule in meta.get("routing_rules", {}).get("rules", []):
        recs = [by_id[e] for e in rule["evidence_ids"] if e in by_id]
        out.append({
            "rule_id": rule["rule_id"],
            "summary": rule["summary"],
            "capability": rule["capability"],
            "comparison_type": rule["comparison_type"],
            "confidence": rule["confidence"],
            "last_verified": rule["last_verified"],
            "evidence_ids": sorted(rule["evidence_ids"]),
            "evidence_classes": sorted({r["evidence_class"] for r in recs}),
            "source_tiers": sorted({r["source_tier"] for r in recs}),
            "comparability_groups": sorted({r["comparability_group"] for r in recs}),
            "any_vendor_run": any(bool(r.get("vendor_run")) for r in recs),
            "all_vendor_run": bool(recs) and all(bool(r.get("vendor_run")) for r in recs),
        })
    return out


class SpreadFallbackResurrected(Exception):
    """A fraction-of-spread band was reintroduced. It is not uncertainty."""


def build(raw: dict, digest: str, evidence_filter=None, filter_name: str = "full") -> dict:
    hierarchy = raw["direction_setting_hierarchy"]
    if "min_fraction_of_spread" in hierarchy or "no_dispersion_rule" in raw:
        raise SpreadFallbackResurrected(
            "benchmarks.json declares a fraction-of-spread equivalence band. Observed spread is "
            "not statistical uncertainty -- see direction_setting_hierarchy. Remove it.")
    for gid, g in raw["comparability_groups"].items():
        kind = (g.get("equivalence_band") or {}).get("kind", "none")
        if kind not in DIRECTION_BASIS + ("none",):
            raise SpreadFallbackResurrected(
                "comparability group %r declares equivalence_band kind %r, which is not in the "
                "declared direction-setting hierarchy %s" % (gid, kind, list(DIRECTION_BASIS)))
    records = raw["records"]
    if evidence_filter is not None:
        records = [r for r in records if evidence_filter(r)]
    by_id = {r["id"]: r for r in raw["records"]}

    caps = sorted({c.strip() for r in raw["records"] for c in (r.get("capability") or "").split(",")
                   if c.strip() and c.strip() != "aggregate"})
    frontiers = [compile_capability(c, records, raw) for c in caps]

    return {
        "generator": "scripts/compile_benchmark_frontiers.py",
        "generator_version": GENERATOR_VERSION,
        "evidence_filter": filter_name,
        "input_file": "skill/benchmarks.json",
        "input_sha256": digest,
        "input_compiled": raw.get("compiled"),
        "how_to_read": (
            "GENERATED FILE -- do not hand-edit; run the compiler. 'preferred' is which ecosystem the "
            "declared evidence favours for that capability, or UNRESOLVED when the declared metadata does "
            "not settle it. UNRESOLVED and 'equivalent' both mean the router must fall through to the "
            "efficiency tie-break; they are not failures. A cell is UNRESOLVED whenever no confidence "
            "interval, standard error, repeated-trial dispersion or benchmark-owner significance "
            "threshold is published for it -- however large the gap looks; observed spread is not "
            "uncertainty. 'gap_over_observed_spread_diagnostic' shows which cells are worth chasing a "
            "real interval for and sets nothing. Nothing here is read at runtime -- SKILL.md "
            "carries the compact rules and this file is how those rules are audited."
        ),
        "capability_frontiers": frontiers,
        "effort_curves": compile_effort_curves(records, raw),
        "rule_provenance": compile_rule_provenance(raw, by_id),
    }


def dumps(obj: dict) -> str:
    """One canonical serialisation, so two runs are byte-identical."""
    return json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if the committed frontier is stale or missing")
    ap.add_argument("--raw", default=str(RAW))
    ap.add_argument("--out", default=str(OUT))
    args = ap.parse_args()

    raw, digest = load_raw(Path(args.raw))
    text = dumps(build(raw, digest))
    out = Path(args.out)

    if args.check:
        if not out.exists():
            print("STALE: %s does not exist. Run the compiler." % out)
            return 1
        current = out.read_text(encoding="utf-8")
        if current != text:
            old = json.loads(current).get("input_sha256", "?")
            print("STALE: %s does not match skill/benchmarks.json." % out)
            print("  frontier was generated from input_sha256 %s" % old[:16])
            print("  benchmarks.json is now                   %s" % digest[:16])
            print("  Fix: python scripts/compile_benchmark_frontiers.py")
            return 1
        print("frontier is up to date (input_sha256 %s)" % digest[:16])
        return 0

    io.open(out, "w", encoding="utf-8", newline="\n").write(text)
    data = json.loads(text)
    print("wrote %s" % out)
    print("  input_sha256      %s" % digest[:16])
    print("  capabilities      %d" % len(data["capability_frontiers"]))
    print("  effort curves     %d" % len(data["effort_curves"]))
    print("  rules traced      %d" % len(data["rule_provenance"]))
    for f in data["capability_frontiers"]:
        print("  %-24s %-11s %s" % (f["capability"], f["preferred"], f["confidence"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
