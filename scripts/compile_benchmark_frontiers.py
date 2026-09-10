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

GENERATOR_VERSION = "1.0"

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


def band_for(group: dict, benchmark: str, rule: dict, spread: float) -> tuple[float | None, str]:
    """The equivalence band for one comparability group, from declared metadata only.

    Returns (band, basis). band is None only when the declared metadata gives no
    way to compute one, which the caller treats as UNRESOLVED rather than as zero.
    """
    eb = group.get("equivalence_band") or {"kind": "none"}
    kind = eb.get("kind")
    if kind == "published_ci" and eb.get("value") is not None:
        return float(eb["value"]), "published_ci"
    if kind == "published_se" and eb.get("value") is not None:
        applies = eb.get("applies_to")
        if applies is None or benchmark in applies:
            # 95% interval from a standard error, the conventional multiplier.
            return 2.0 * float(eb["value"]), "published_se_x2"
        # SE published for a different benchmark in the same group does not carry over.
    # No published dispersion: fall back to the declared spread rule.
    frac = rule.get("min_fraction_of_spread")
    if frac is None or spread <= 0:
        return None, "no_dispersion_and_no_spread_rule"
    return float(frac) * spread, "spread_rule_%g" % frac


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
    out["band"] = None if band is None else round(band, 4)
    out["band_basis"] = basis

    if band is None:
        out["direction"] = UNRESOLVED
        out["reason"] = "no published dispersion and no spread rule applies"
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
    rule = meta["no_dispersion_rule"]

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
    rule = meta["no_dispersion_rule"]

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

    A rung is marked dominated when a LOWER rung in the same group scores at least
    as well within the declared band while costing less. No interpolation: a rung
    that was never published simply does not appear.
    """
    rule = meta["no_dispersion_rule"]
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
        dominated = []
        for i, hi in enumerate(rows):
            for lo in rows[:i]:
                gain = hi["score"] - lo["score"]
                hc, lc = hi.get("cost_per_task_usd"), lo.get("cost_per_task_usd")
                if band is None or hc is None or lc is None:
                    continue
                if gain <= band and hc > lc:
                    dominated.append({
                        "rung": hi["effort"], "dominated_by": lo["effort"],
                        "score_gain": round(gain, 4), "band": round(band, 4),
                        "cost_delta_usd": round(hc - lc, 4),
                        "ids": [hi["id"], lo["id"]],
                    })
                    break
        curves.append({
            "model": model, "group": gid, "band": None if band is None else round(band, 4),
            "band_basis": basis, "points": points, "dominated_rungs": dominated,
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


def build(raw: dict, digest: str, evidence_filter=None, filter_name: str = "full") -> dict:
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
            "efficiency tie-break; they are not failures. Nothing here is read at runtime -- SKILL.md "
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
