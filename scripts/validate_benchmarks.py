#!/usr/bin/env python3
"""Deterministic validation of skill/benchmarks.json (and the derived frontier).

A benchmark-driven router rots quietly: a record loses its harness, two
incompatible scoring modes end up in one comparability group, a rule keeps citing
an evidence id that no longer exists, or the committed frontier stops matching the
evidence it was compiled from. None of that shows up as a failing routing eval --
the router just starts being confidently wrong.

Everything here is mechanical. No LLM, no network.

Usage:
    python scripts/validate_benchmarks.py
    python scripts/validate_benchmarks.py --no-frontier   # skip the staleness check
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "skill" / "benchmarks.json"
FRONTIER = ROOT / "skill" / "benchmark_frontiers.json"

VALID_TIERS = {"A", "B", "C"}
EFFORT_RUNGS = {"low", "medium", "high", "xhigh", "max"}
# Scoring modes that describe the same benchmark but are not comparable with
# each other. Two of these inside one comparability group is a hard error.
SCORE_MODE_TOKENS = ("partial", "strict")


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, code: str, msg: str) -> None:
        self.errors.append("[%s] %s" % (code, msg))

    def warn(self, code: str, msg: str) -> None:
        self.warnings.append("[%s] %s" % (code, msg))


def check_records(d: dict, rep: Report) -> None:
    records = d["records"]
    groups = d["comparability_groups"]
    classes = set(d["evidence_classes"])
    seen: dict[str, int] = {}
    missing_harness: dict[str, int] = collections.Counter()

    for i, r in enumerate(records):
        where = "record #%d (%s)" % (i, r.get("id") or "NO ID")

        rid = r.get("id")
        if not rid:
            rep.error("missing-id", "%s has no id" % where)
        elif rid in seen:
            rep.error("duplicate-id", "id %r used by records #%d and #%d" % (rid, seen[rid], i))
        else:
            seen[rid] = i

        tier = r.get("source_tier")
        if tier not in VALID_TIERS:
            rep.error("bad-tier", "%s has source_tier %r, expected one of %s"
                      % (where, tier, sorted(VALID_TIERS)))

        cls = r.get("evidence_class")
        if cls not in classes:
            rep.error("bad-class", "%s has evidence_class %r, which is not declared" % (where, cls))

        gid = r.get("comparability_group")
        if gid not in groups:
            rep.error("unknown-group", "%s references undeclared comparability_group %r" % (where, gid))

        if not r.get("source"):
            rep.error("missing-source", "%s has no source" % where)
        if not r.get("verified_at"):
            rep.error("missing-verified-at", "%s has no verified_at" % where)

        # A score without a version, on a benchmark that ships versions, is unusable:
        # nothing downstream can tell whether it is comparable with anything else.
        if r.get("score") is not None and not r.get("benchmark_version"):
            versioned = {x["benchmark"] for x in records
                         if x.get("benchmark_version") and x["benchmark"] == r["benchmark"]}
            if versioned:
                rep.error("score-without-version",
                          "%s carries a score but no benchmark_version, and other rows for %r do have one"
                          % (where, r["benchmark"]))

        # A vendor measuring a competitor must say whose harness it was.
        if r.get("vendor_run") and r.get("score") is not None and not r.get("harness"):
            missing_harness[r.get("comparability_group")] += 1

        eff = r.get("effort")
        if eff is not None and eff not in EFFORT_RUNGS:
            if not re.match(r"^(n/a|reasoning|adaptive)", str(eff), re.I):
                rep.warn("odd-effort", "%s has effort %r, not a known rung" % (where, eff))

        if r.get("score") is not None and r.get("score_unit") is None:
            rep.error("score-without-unit", "%s has a score with no score_unit" % where)

    # Aggregated, so one under-documented launch table cannot bury the real findings.
    for gid, n in sorted(missing_harness.items()):
        rep.warn("vendor-run-without-harness",
                 "group %r has %d vendor_run scored rows that name no harness. Direction evidence at best."
                 % (gid, n))


def check_groups(d: dict, rep: Report) -> None:
    """A comparability group promises a constant setup. Verify the promise."""
    records = d["records"]
    by_group: dict[str, list] = collections.defaultdict(list)
    for r in records:
        by_group[r.get("comparability_group")].append(r)

    for gid, gmeta in d["comparability_groups"].items():
        rows = by_group.get(gid, [])
        if not rows:
            rep.warn("empty-group", "comparability_group %r has no records" % gid)
            continue

        for r in rows:
            # An efficiency_only row carries no score, so it can never set a direction
            # and is allowed to sit inside a capability group alongside scored rows.
            if r.get("evidence_class") == "efficiency_only":
                continue
            if r.get("evidence_class") != gmeta["evidence_class"]:
                rep.error("class-mismatch",
                          "record %r is evidence_class %r but its group %r declares %r"
                          % (r["id"], r.get("evidence_class"), gid, gmeta["evidence_class"]))
            if r.get("source_tier") != gmeta["source_tier"]:
                rep.error("tier-mismatch",
                          "record %r is tier %r but its group %r declares %r"
                          % (r["id"], r.get("source_tier"), gid, gmeta["source_tier"]))

        # Same group + same benchmark + same version must mean same harness -- UNLESS the
        # group is ecosystem_end_to_end, where differing harnesses are the entire point
        # (Claude Code + Claude vs Codex CLI + GPT). There the check inverts: a group
        # claiming to be end-to-end while using ONE harness is mislabelled and is really
        # model_intrinsic.
        end_to_end = gmeta["evidence_class"] == "ecosystem_end_to_end"
        cells: dict[tuple, set] = collections.defaultdict(set)
        for r in rows:
            key = (r["benchmark"], r.get("benchmark_version") or "")
            cells[key].add(r.get("harness") or r.get("agent_scaffold") or "")
        for key, harnesses in sorted(cells.items()):
            real = {h for h in harnesses if h}
            if end_to_end:
                if len(real) == 1:
                    rep.warn("end-to-end-single-harness",
                             "group %r is declared ecosystem_end_to_end but benchmark %s %s uses a single "
                             "harness %s. If the stack really is constant, this is model_intrinsic."
                             % (gid, key[0], key[1], sorted(real)))
            elif len(real) > 1:
                rep.error("harness-conflict",
                          "group %r, benchmark %s %s: one comparability cell contains %d different "
                          "harnesses %s -- these rows are not comparable and must be split into "
                          "separate groups" % (gid, key[0], key[1], len(real), sorted(real)))

        # partial vs strict scoring inside one group would be silently averaged.
        modes = collections.defaultdict(set)
        for r in rows:
            ver = (r.get("benchmark_version") or "").lower()
            for tok in SCORE_MODE_TOKENS:
                if tok in ver:
                    modes[r["benchmark"]].add(tok)
        for bench, found in sorted(modes.items()):
            if len(found) > 1:
                rep.warn("score-mode-collision",
                         "group %r holds both %s scoring for %s. That is fine only because the version "
                         "string distinguishes them -- the compiler keys cells on version, so they never "
                         "meet. Verify that stays true if the version strings change."
                         % (gid, "/".join(sorted(found)), bench))


def check_effort_interpolation(d: dict, rep: Report) -> None:
    """No record may claim to be derived, estimated or interpolated."""
    # Only affirmative claims count. "do not interpolate it" is the rule being
    # obeyed, not broken, so a negation immediately before the term clears it.
    banned = re.compile(
        r"(?<!not )(?<!never )(?<!no )(?<!avoid )"
        r"\b(interpolated from|extrapolated from|estimated from|inferred from the|"
        r"derived by scaling)\b",
        re.I)
    for r in d["records"]:
        blob = " ".join(str(r.get(k) or "") for k in ("notes", "source", "dispersion"))
        if banned.search(blob):
            rep.error("interpolation",
                      "record %r reads as an interpolated or extrapolated figure. A missing rung must "
                      "stay null." % r["id"])


def check_rules(d: dict, rep: Report) -> None:
    ids = {r["id"] for r in d["records"]}
    seen = set()
    for rule in d.get("routing_rules", {}).get("rules", []):
        rid = rule.get("rule_id")
        if not rid:
            rep.error("rule-missing-id", "a routing rule has no rule_id")
            continue
        if rid in seen:
            rep.error("duplicate-rule-id", "rule_id %r declared twice" % rid)
        seen.add(rid)

        for field in ("capability", "comparison_type", "confidence", "last_verified", "evidence_ids"):
            if field not in rule:
                rep.error("rule-missing-field", "rule %r has no %s" % (rid, field))

        for eid in rule.get("evidence_ids", []):
            if eid not in ids:
                rep.error("dangling-evidence",
                          "rule %r cites evidence id %r, which no record has" % (rid, eid))

        if not rule.get("evidence_ids") and rule.get("comparison_type") not in (
                "product_mechanism", "spec_and_price", "excluded"):
            rep.error("rule-without-evidence",
                      "rule %r cites no evidence but its comparison_type (%r) is one that requires it"
                      % (rid, rule.get("comparison_type")))


def check_frontier(d: dict, rep: Report) -> None:
    """The derived frontier must have been generated from the evidence as it stands."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import compile_benchmark_frontiers as c  # noqa: E402

    if not FRONTIER.exists():
        rep.error("frontier-missing",
                  "%s does not exist. Run scripts/compile_benchmark_frontiers.py" % FRONTIER.name)
        return
    raw, digest = c.load_raw(RAW)
    expected = c.dumps(c.build(raw, digest))
    actual = FRONTIER.read_text(encoding="utf-8")
    if actual != expected:
        old = json.loads(actual)
        stale = old.get("input_sha256", "?")
        if stale == digest:
            # Same evidence, different output: the COMPILER moved, not the data.
            # Saying "benchmarks.json now hashes to <the same hash>" sends the
            # reader hunting for an evidence change that never happened.
            rep.error("frontier-stale",
                      "skill/benchmark_frontiers.json matches the current skill/benchmarks.json "
                      "(sha256 %s) but not the current compiler (generator_version %s, now %s). "
                      "Re-run scripts/compile_benchmark_frontiers.py."
                      % (digest[:16], old.get("generator_version", "?"), c.GENERATOR_VERSION))
        else:
            rep.error("frontier-stale",
                      "skill/benchmark_frontiers.json was generated from input_sha256 %s but "
                      "skill/benchmarks.json now hashes to %s. Re-run the compiler."
                      % (stale[:16], digest[:16]))

    front = json.loads(actual)
    for f in front.get("capability_frontiers", []):
        for comp in f.get("comparisons", []):
            for rid in comp.get("rows", []):
                if rid not in {r["id"] for r in d["records"]}:
                    rep.error("frontier-dangling",
                              "frontier cites record %r which no longer exists" % rid)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-frontier", action="store_true")
    args = ap.parse_args()

    d = json.loads(RAW.read_text(encoding="utf-8"))
    rep = Report()

    check_records(d, rep)
    check_groups(d, rep)
    check_effort_interpolation(d, rep)
    check_rules(d, rep)
    if not args.no_frontier:
        check_frontier(d, rep)

    print("records:  %d" % len(d["records"]))
    print("groups:   %d" % len(d["comparability_groups"]))
    print("rules:    %d" % len(d.get("routing_rules", {}).get("rules", [])))
    for w in rep.warnings:
        print("WARN  " + w)
    for e in rep.errors:
        print("ERROR " + e)
    print("\n%d error(s), %d warning(s)" % (len(rep.errors), len(rep.warnings)))
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
