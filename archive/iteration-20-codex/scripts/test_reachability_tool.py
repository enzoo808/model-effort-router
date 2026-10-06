#!/usr/bin/env python3
"""Deterministic unit tests for the reachability auditor itself.

The auditor's job is to fail when a supported combination has no route. Nothing
was checking that it still *can* fail. A linter that has quietly stopped
reporting looks exactly like a clean repo, which is the worst failure mode a
tool like this has -- so every check gets a fixture that deliberately trips it,
and every check gets a fixture that deliberately does not.

Compact synthetic fixtures, not the 154-prompt corpus: the corpus is data that
changes when the routing rules change, and a test suite pinned to it would have
to be rewritten every time somebody adds a prompt.

No network, no LLM. Run:

    python scripts/test_reachability_tool.py
"""
from __future__ import annotations

import io
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_routing_reachability as R  # noqa: E402

FAILURES: list[str] = []


def check(name: str, got, want) -> None:
    if got != want:
        FAILURES.append("%s\n     got:  %r\n     want: %r" % (name, got, want))
        print("FAIL  %s" % name)
    else:
        print("ok    %s" % name)


def prompt(pid, **over):
    t = {"id": pid, "prompt": "fixture " + pid, "cap": "agentic-code",
         "R": 0, "D": 0, "W": 0, "C": 0, "O": "low", "P": "low", "A": "low",
         "dur_gt30": False, "indiv": False, "builds": False, "agentic_write": False,
         "gates": [], "flags": [], "P_kind": None}
    t.update(over)
    return t


def policy(claude=None, codex=None):
    return {"support_matrix": {
        "claude": claude if claude is not None else {
            "Sonnet 5.5": {"efforts": ["low", "medium"], "modes": []}},
        "codex": codex if codex is not None else {
            "Sol": {"efforts": ["low", "medium"], "modes": []}},
    }}


def build(pol, corpus, review=None):
    after, before = R.route_all(corpus, "after"), R.route_all(corpus, "before")
    return R.build_matrix(pol, corpus, after, before, review or {"flips": {}})


def kinds(problems):
    return sorted({k for _lvl, k, _msg in problems})


def row(matrix, eco, model, cell):
    for r_ in matrix["matrix"]:
        if (r_["ecosystem"], r_["model"], r_["effort_or_mode"]) == (eco, model, cell):
            return r_
    raise AssertionError("no row for %s|%s|%s" % (eco, model, cell))


ALL_ACCEPT = {"flips": {}}


# =====================================================================
# ROUTING: iteration-19 (BEFORE) vs iteration-20 (AFTER)
# =====================================================================

# tier -- Terra is gone; Sol is the one Codex mid tier.
mid = prompt("t-mid", D=2, W=1, C=1, R=1, cap="deep-reasoning")
check("before: a D=2 analysis prompt went to Terra",
      R.cell_of(R.route_codex(mid, "before")), "Terra · high")
check("after: the same prompt goes to Sol -- there is no Terra to drop to",
      R.cell_of(R.route_codex(mid, "after")), "Sol · high")
check("  ...and attribution blames the tier merge alone", R.attribute(mid), ["tier"])

# notch -- N1 retired.
notch = prompt("t-notch", D=2, W=2, C=2, R=1, builds=True, agentic_write=True, cap="agentic-code",
               dur_gt30=True)
check("before: multi-step code writing took the +1 notch to xhigh",
      R.cell_of(R.route_codex(notch, "before")), "Terra · xhigh")
check("after: both arms take high from the same table",
      (R.cell_of(R.route_claude(notch, "after")), R.cell_of(R.route_codex(notch, "after"))),
      ("Sonnet 5.5 · high", "Sol · high"))
check("  ...attribution blames the notch AND the tier (each alone leaves a difference)",
      R.attribute(notch), ["notch", "tier"])
check("  ...and bump() is still monotonic", R.bump("max", "xhigh"), "max")

# e4 -- retired.
e4 = prompt("t-e4", D=3, R=3, W=2, C=2, indiv=True, builds=True, agentic_write=True, cap="agentic-code")
check("before: E4 rewrote Sol max to Astra xhigh on agentic-code",
      R.cell_of(R.route_codex(e4, "before")), "Astra · xhigh")
check("after: Sol max stays Sol max",
      R.cell_of(R.route_codex(e4, "after")), "Sol · max")
check("  ...attribution blames E4 alone", R.attribute(e4), ["e4"])

# gates -- the >=1M-token and computer-use Astra gates are retired; 1000+ files stays.
gui = prompt("t-gui", D=2, R=2, W=1, C=1, cap="computer-use", gates=["computer_use"])
check("before: a GUI-driving task gated to Astra",
      R.cell_of(R.route_codex(gui, "before")), "Astra · high")
check("after: it scores normally and lands on Sol",
      R.cell_of(R.route_codex(gui, "after")), "Sol · high")
big = prompt("t-big", D=2, R=1, W=3, C=3, gates=["files_1000plus"], cap="agentic-code")
check("the 1000+ file positioning gate still routes to Astra in both",
      (R.cell_of(R.route_codex(big, "before")), R.cell_of(R.route_codex(big, "after"))),
      ("Astra · high", "Astra · high"))

# Luna is D=0 only, on either side.
check("Luna stays the D=0 tier", R.cell_of(R.route_codex(prompt("t-lo", D=0, R=1), "after")), "Luna · low")
check("  ...and a D=0 task at R>=2 goes to Sol low, not Luna",
      R.cell_of(R.route_codex(prompt("t-lo2", D=0, R=2), "after")), "Sol · low")

# Ultra needs D=3 and P=high; on Sol it rides on the one tier.
check("three strands at D=3 reach Sol Ultra",
      R.cell_of(R.route_codex(prompt("t-u", D=3, R=2, W=1, C=2, P="high", P_kind="strands", dur_gt30=True,
                                     cap="parallel-independent"), "after")), "Sol Ultra · xhigh")

# The iteration-18 rules are baked in, not switched: orchestration at W=2 reaches ultracode
# in BOTH variants now, and mechanical width does not.
multi = prompt("t-multi", D=2, W=2, C=2, O="high", dur_gt30=True, builds=True, agentic_write=True)
check("orchestration at W=2 reaches ultracode (iteration-18, now unconditional)",
      (R.cell_of(R.route_claude(multi, "before")), R.cell_of(R.route_claude(multi, "after"))),
      ("Sonnet 5.5 · ultracode", "Sonnet 5.5 · ultracode"))
mech = prompt("t-mech", D=1, W=3, C=1, dur_gt30=True, builds=True)
check("150 files of one mechanical rename never fires ultracode",
      R.cell_of(R.route_claude(mech, "after")), "Sonnet 5.5 · medium")

# M1: max needs D=3 AND R=3 AND a flagship AND an indivisible decision -- on Sol too.
indivisible = prompt("t-indiv", D=3, R=3, W=2, C=2, indiv=True, builds=True, cap="deep-reasoning")
check("M1 emits Sol max on an indivisible D=3 R=3 decision",
      R.cell_of(R.route_codex(indivisible, "after")), "Sol · max")
check("  ...and never Luna max", R.cell_of(R.route_codex(prompt("t-l", D=0, R=1), "after")), "Luna · low")

# ------------------------------------------------ the badge
def bdg(cap, D=2, cx_model="Sol", cl_model="Sonnet 5.5", cx_mode=None, cl_mode=None, O="low", eff="high", R_=1):
    t = prompt("b", cap=cap, D=D, O=O, R=R_)
    return R.badge(t, {"model": cl_model, "effort": eff, "mode": cl_mode},
                   {"model": cx_model, "effort": eff, "mode": cx_mode}, "after")

check("agentic-code against Sol falls to efficiency -> Codex", bdg("agentic-code"), "codex")
check("knowledge-work against Sol keeps a benchmark direction -> Claude", bdg("knowledge-work"), "claude")
check("science against Sol -> Claude, against Astra -> Codex",
      (bdg("science"), bdg("science", cx_model="Astra")), ("claude", "codex"))
check("D<=1 skips the capability rows: efficiency decides -> Codex", bdg("knowledge-work", D=1), "codex")
check("a mechanism beats an efficiency fall-through: opusplan on agentic-code -> Claude",
      bdg("agentic-code", cl_model="opusplan", cl_mode="opusplan"), "claude")
check("...O=high (ultracode) on agentic-code -> Claude", bdg("agentic-code", O="high"), "claude")
check("...but a benchmark DIRECTION beats a mechanism: knowledge-work + Ultra -> Claude",
      bdg("knowledge-work", cx_mode="ultra"), "claude")
check("Ultra beats an efficiency fall-through -> Codex",
      bdg("agentic-code", cx_mode="ultra"), "codex")
check("two mechanisms cancel and the capability row decides",
      bdg("agentic-code", cx_mode="ultra", O="high"), "codex")
check("an unlisted capability takes the lighter configuration; a tie goes to Codex",
      bdg("instruction-following"), "codex")
check("R=3 widens the bar for parity: a single-row LEAN decides instead of efficiency",
      (bdg("agentic-code", R_=1), bdg("agentic-code", R_=3)), ("codex", "claude"))
check("  ...but a cell with no lean still falls to efficiency at R=3",
      bdg("computer-use", R_=3), "codex")
check("  ...and D<=1 skips the capability rows even at R=3 (both arms clear the bar)",
      bdg("agentic-code", D=0, R_=3), "codex")
check("  ...and a lean that points to Codex is followed too",
      bdg("doc-data-understanding", R_=3), "codex")

# ------------------------------------------------ the badge table cannot drift from the compiler
FRONTIER = json.loads((Path(__file__).resolve().parent.parent / "skill" / "benchmark_frontiers.json")
                      .read_text(encoding="utf-8"))
hints = {(c["capability"], m["codex_model"]): m["badge_hint"]
         for c in FRONTIER["capability_frontiers"] for m in c["by_codex_model"]}
drift = []
for (cap, cx_model), h in sorted(hints.items()):
    col = {"GPT-6.1 Sol": 0, "Astra": 1}.get(cx_model)
    if col is None or cap not in R.BADGE20:
        continue
    side, direction, lean = R.BADGE20[cap][col]
    want_direction = h["basis"] == "direction_rows"
    if (direction != want_direction or (want_direction and side != h["toward"])
            or (not want_direction and lean != h["lean"])):
        drift.append("%s vs %s: BADGE20 says %s/%s/lean=%s, compiler says %s/%s/lean=%s"
                     % (cap, cx_model, side, direction, lean, h["toward"], h["basis"], h["lean"]))
check("BADGE20 agrees with the compiled badge_hint on every capability it can see", drift, [])

# =====================================================================
# MATRIX STATUSES
# =====================================================================

# The real INTENTIONAL table is about the real roster; these fixtures need a
# blank slate, or a rationale written for the shipped rules would silence a zero
# this section is deliberately creating.
REAL_INTENTIONAL = dict(R.INTENTIONAL)
R.INTENTIONAL.clear()

# Four cells at 25% each: big enough that nothing trips the 28% over-selection bar.
FULL = {"Sonnet 5.5": {"efforts": ["low", "medium", "high", "xhigh", "max"], "modes": []}}
TERRA = {"Sol": {"efforts": ["low", "medium", "high", "xhigh"], "modes": []}}  # the one Codex mid tier
BALANCED = ([prompt("t-lo%d" % i, D=0, R=2) for i in range(4)]
            + [prompt("t-md%d" % i, D=1, R=2) for i in range(4)]
            + [prompt("t-hi%d" % i, D=2, R=2, C=2) for i in range(4)]
            + [prompt("t-xh%d" % i, D=3, R=2, C=2) for i in range(4)])
m = build(policy(claude=FULL, codex=TERRA), BALANCED)
check("a cell a prompt lands on is HEALTHY",
      row(m, "claude", "Sonnet 5.5", "low")["status"], "HEALTHY")
check("  ...and records which prompts reached it",
      row(m, "claude", "Sonnet 5.5", "low")["representative_prompt_ids"],
      ["t-lo0", "t-lo1", "t-lo2", "t-lo3"])
check("  ...and every other populated cell is healthy too",
      sorted({row(m, "claude", "Sonnet 5.5", c)["status"]
              for c in ("medium", "high", "xhigh")}), ["HEALTHY"])

POL3 = policy(claude=FULL, codex=TERRA)
check("an unreached, unclaimed, supported cell is UNINTENTIONALLY_UNREACHABLE",
      row(m, "claude", "Sonnet 5.5", "max")["status"], "UNINTENTIONALLY_UNREACHABLE")
check("  ...and the linter turns that into an ERROR",
      "unreachable" in kinds(R.lint(POL3, m, BALANCED, ALL_ACCEPT)), True)

# An INTENTIONAL claim silences it -- and only it.
saved = dict(R.INTENTIONAL)
try:
    R.INTENTIONAL["claude|Sonnet 5.5|max"] = ("INTENTIONALLY_UNREACHABLE", "fixture reason")
    m2 = build(POL3, BALANCED)
    check("a claimed zero is INTENTIONALLY_UNREACHABLE, not a bug",
          row(m2, "claude", "Sonnet 5.5", "max")["status"], "INTENTIONALLY_UNREACHABLE")
    check("  ...carries its rationale into the generated matrix",
          row(m2, "claude", "Sonnet 5.5", "max")["rationale"], "fixture reason")
    check("  ...and the linter stays quiet about it",
          "unreachable" in kinds(R.lint(POL3, m2, BALANCED, ALL_ACCEPT)), False)

    # UNSUPPORTED means the product cannot do it. Emitting it anyway is an error.
    R.INTENTIONAL["claude|Sonnet 5.5|low"] = ("UNSUPPORTED", "fixture capability limit")
    m3 = build(POL3, BALANCED)
    check("a cell declared UNSUPPORTED is marked unsupported in the matrix",
          row(m3, "claude", "Sonnet 5.5", "low")["supported"], False)
    check("  ...and emitting it anyway is an ERROR",
          "unsupported-but-emitted" in kinds(R.lint(POL3, m3, BALANCED, ALL_ACCEPT)), True)
finally:
    R.INTENTIONAL.clear()
    R.INTENTIONAL.update(saved)

# A cell the rules emit that the support matrix does not list at all has no row,
# which makes every other check blind to it.
NARROW = policy(claude={"Sonnet 5.5": {"efforts": ["low"], "modes": []}}, codex=TERRA)
check("a cell missing from the support matrix entirely is an ERROR",
      "emitted-cell-not-in-support-matrix" in kinds(
          R.lint(NARROW, build(NARROW, BALANCED), BALANCED, ALL_ACCEPT)), True)
check("  ...and a complete support matrix is silent",
      "emitted-cell-not-in-support-matrix" in kinds(
          R.lint(POL3, build(POL3, BALANCED), BALANCED, ALL_ACCEPT)), False)

# A model with no effort parameter must never be handed one, on ANY branch --
# the scored branch used to fall through to the D table and emit "Haiku 4.5- low".
HAIKU_POL = policy(claude={"Haiku 4.5": {"efforts": [], "modes": []},
                           "Sonnet 5.5": {"efforts": ["low"], "modes": []}},
                   codex={"Luna": {"efforts": ["low"], "modes": []},
                          "Sol": {"efforts": ["low"], "modes": []}})
scored_haiku = prompt("t-haiku", D=0, W=0, C=0, R=0)
check("Haiku reached by SCORING carries no effort, just like the gate branch",
      R.cell_of(R.route_claude(scored_haiku, "after")), "Haiku 4.5")
check("  ...so no effort cell is emitted for it",
      "emitted-cell-not-in-support-matrix" in kinds(
          R.lint(HAIKU_POL, build(HAIKU_POL, [scored_haiku]), [scored_haiku], ALL_ACCEPT)), False)

R.INTENTIONAL.update(REAL_INTENTIONAL)

# Over-selection: one cell swallowing the corpus.
pol = policy(claude={"Sonnet 5.5": {"efforts": ["low"], "modes": []}},
             codex={"Sol": {"efforts": ["low"], "modes": []}})
corpus = [prompt("t-%d" % i, D=0, R=2) for i in range(10)]
m = build(pol, corpus)
check("a cell covering most of the corpus is OVER_SELECTED",
      row(m, "claude", "Sonnet 5.5", "low")["status"], "OVER_SELECTED")
check("  ...reported as a WARN, not an ERROR",
      [lvl for lvl, k, _ in R.lint(pol, m, corpus, ALL_ACCEPT) if k == "over-selected"],
      ["WARN", "WARN"])

# Route lost between the two rule sets: a GUI task used to land on Astra, now on Sol.
pol = policy(codex={"Astra": {"efforts": ["low", "medium", "high"], "modes": []},
                    "Sol": {"efforts": ["low", "medium", "high"], "modes": []}})
corpus = [prompt("t-gui", D=2, R=2, W=1, C=1, cap="computer-use", gates=["computer_use"])]
m = build(pol, corpus)
check("a cell reachable before and not after is flagged lost",
      row(m, "codex", "Astra", "high")["lost_by_this_pass"], True)
check("  ...and the linter warns about it",
      "route-lost" in kinds(R.lint(pol, m, corpus, ALL_ACCEPT)), True)
check("a cell reachable after and not before is flagged recovered",
      row(m, "codex", "Sol", "high")["recovered_by_this_pass"], True)


# =====================================================================
# PLATFORM-FORCED CELLS
# =====================================================================

pol = policy(claude={"Haiku 4.5": {"efforts": [], "modes": []},
                     "Sonnet 5.5": {"efforts": ["low"], "modes": []}})
corpus = [prompt("t-fast", gates=["latency_volume"], cap="latency-volume"),
          prompt("t-1", D=0, R=2)]
m = build(pol, corpus)
haiku = row(m, "claude", "Haiku 4.5", "(no effort parameter)")
check("a model with no effort parameter gets one row, marked platform_forced",
      haiku["platform_forced"], True)
check("  ...whose status is PLATFORM_FORCED, never HEALTHY -- the platform filled "
      "that cell in, not the policy", haiku["status"], "PLATFORM_FORCED")
check("  ...and a policy-selected cell is not marked forced",
      row(m, "claude", "Sonnet 5.5", "low")["platform_forced"], False)
check("  ...with no lint complaint in the healthy case",
      "platform-forced-model-given-an-effort" in kinds(R.lint(pol, m, corpus, ALL_ACCEPT)),
      False)

forged = json.loads(json.dumps(m))
forged["matrix"].append(dict(haiku, effort_or_mode="high", platform_forced=False,
                             observed_after=1, representative_prompt_ids=["t-fast"]))
check("an effort emitted on an effortless model IS an ERROR",
      "platform-forced-model-given-an-effort" in kinds(R.lint(pol, forged, corpus, ALL_ACCEPT)),
      True)


# =====================================================================
# INTEGRITY CHECKS
# =====================================================================

# Conditional access: Mythos 5.1 requires stated Glasswing access.
pol = policy(claude={"Mythos 5.1": {"efforts": ["xhigh"], "modes": []}})
corpus = [prompt("t-glass", D=3, R=2, cap="terminal-tool",
                 gates=["offensive_security"], flags=["glasswing"])]
m = build(pol, corpus)
check("Mythos reached WITH stated access is clean",
      "conditional-access-leak" in kinds(R.lint(pol, m, corpus, ALL_ACCEPT)), False)
leaky = json.loads(json.dumps(m))
no_flag = [dict(corpus[0], flags=[])]
check("Mythos reached WITHOUT stated access is an ERROR",
      "conditional-access-leak" in kinds(R.lint(pol, leaky, no_flag, ALL_ACCEPT)), True)

# A model in the support matrix that produces no row at all.
pol = policy(claude={"Sonnet 5.5": {"efforts": ["low"], "modes": []}})
corpus = [prompt("t-1", D=0, R=2)]
m = build(pol, corpus)
m["matrix"] = [r_ for r_ in m["matrix"] if r_["model"] != "Sonnet 5.5"]
check("a roster model with no matrix row at all is an ERROR",
      "model-missing-from-matrix" in kinds(R.lint(pol, m, corpus, ALL_ACCEPT)), True)

# A mode the product claims that nothing reaches.
pol = policy(codex={"Sol": {"efforts": ["low", "xhigh"], "modes": ["ultra"]}},
             claude={"Sonnet 5.5": {"efforts": ["low"], "modes": []}})
corpus = [prompt("t-1", D=0, R=2)]
m = build(pol, corpus)
check("a supported mode no prompt reaches is a WARN",
      "mode-dead" in kinds(R.lint(pol, m, corpus, ALL_ACCEPT)), True)
corpus2 = [prompt("t-1", D=0, R=2),
           prompt("t-u", D=3, R=2, W=1, C=2, P="high", P_kind="strands",
                  cap="parallel-independent", dur_gt30=True)]
m2 = build(pol, corpus2)
check("  ...and is silent once something reaches the mode",
      "mode-dead" in kinds(R.lint(pol, m2, corpus2, ALL_ACCEPT)), False)

# Contradictory labels: a task cannot be 3+ independent strands AND indivisible.
pol = policy()
bad = [prompt("t-bad", D=3, R=3, P="high", P_kind="strands", indiv=True)]
check("P=high together with indivisible_single_chain is an ERROR",
      "contradictory-labels" in kinds(R.lint(pol, build(pol, bad), bad, ALL_ACCEPT)), True)

# Width at D<=1 labelled as orchestration.
pol = policy()
sloppy = [prompt("t-sloppy", D=1, W=3, O="high", dur_gt30=True)]
check("W=3 at D<=1 labelled O=high is a WARN",
      "width-masquerading-as-orchestration" in kinds(
          R.lint(pol, build(pol, sloppy), sloppy, ALL_ACCEPT)), True)


# =====================================================================
# FLIP REVIEW
# =====================================================================

pol = policy(codex={"Sol": {"efforts": ["low", "medium", "high", "xhigh"], "modes": []}})
corpus = [prompt("t-multi", D=2, W=2, C=2, builds=True, agentic_write=True, cap="agentic-code")]
m = build(pol, corpus)
check("a flip with no verdict is UNREVIEWED in the matrix",
      m["decision_flips"][0]["verdict"], "UNREVIEWED")
check("  ...and the linter refuses it", "flip-unreviewed" in kinds(
      R.lint(pol, m, corpus, ALL_ACCEPT)), True)
check("  ...while the rule attribution is computed, not declared",
      m["decision_flips"][0]["rules_responsible"], ["notch", "tier"])

accepted = {"flips": {"t-multi": ["ACCEPT", "fixture sign-off"]}}
m = build(pol, corpus, accepted)
check("an ACCEPTed flip passes", "flip-unreviewed" in kinds(
      R.lint(pol, m, corpus, accepted)), False)
check("  ...and carries its note into the generated matrix",
      m["decision_flips"][0]["review_note"], "fixture sign-off")

rejected = {"flips": {"t-multi": ["REJECT", "fixture rejection"]}}
m = build(pol, corpus, rejected)
check("a REJECTed flip is an ERROR -- fix the rule, do not ship the flip",
      "flip-rejected" in kinds(R.lint(pol, m, corpus, rejected)), True)

stale = {"flips": {"t-multi": ["ACCEPT", "ok"], "t-gone": ["ACCEPT", "no longer flips"]}}
m = build(pol, corpus, stale)
check("a sign-off for a prompt that no longer flips is a WARN",
      "flip-review-stale" in kinds(R.lint(pol, m, corpus, stale)), True)


# =====================================================================
# HISTOGRAMS AND STALENESS
# =====================================================================

pol = policy(claude={"Sonnet 5.5": {"efforts": ["low", "medium"], "modes": []}})
corpus = [prompt("t-1", D=0, R=2), prompt("t-2", D=0, R=2), prompt("t-3", D=1, R=2)]
m = build(pol, corpus)
h = m["histograms"]
check("the cell histogram counts every prompt exactly once",
      sum(h["claude_cell_after"].values()), len(corpus))
check("  ...and buckets them by cell",
      h["claude_cell_after"], {"Sonnet 5.5 · low": 2, "Sonnet 5.5 · medium": 1})
check("  ...with a before column for the same corpus",
      h["claude_cell_before"], {"Sonnet 5.5 · low": 2, "Sonnet 5.5 · medium": 1})
check("declined and blocked prompts contribute to no cell",
      build(pol, [prompt("t-x", R=2, step0_block=True)])["histograms"]["claude_cell_after"],
      {"(no model)": 1})
check("  ...and produce no matrix hit",
      row(build(pol, [prompt("t-x", R=2, step0_block=True)]),
          "claude", "Sonnet 5.5", "low")["observed_after"], 0)
check("the badge histogram is produced (D<=1 -> efficiency -> Codex)", sorted(h["badge_after"]), ["codex"])

# Staleness: --check must fail when the committed matrix does not match.
with tempfile.TemporaryDirectory() as tmp:
    out = Path(tmp) / "matrix.json"
    real_out, real_argv = R.OUT, sys.argv
    try:
        R.OUT = out
        sys.argv = ["check_routing_reachability.py", "--check"]
        check("--check fails when the matrix file is missing", R.main(), 1)
        sys.argv = ["check_routing_reachability.py"]
        R.main()
        sys.argv = ["check_routing_reachability.py", "--check"]
        check("  ...passes right after a write", R.main(), 0)
        io.open(out, "a", encoding="utf-8").write("\n")
        check("  ...and fails again on a one-byte change", R.main(), 1)
    finally:
        R.OUT, sys.argv = real_out, real_argv

# =====================================================================
# SHIPPED GOLDENS -- the mirror must reproduce the routing eval's answers
# =====================================================================
#
# The routing eval is graded by COLD AGENTS reading skill/SKILL.md, which is the
# real test and cannot run here. This is the cheap half of it: the policy mirror
# and the shipped goldens must at least agree. If a rule change would move a
# golden, this fails in seconds instead of after a round of agent runs -- and if
# a golden legitimately moves, the mismatch is the reminder to re-run the evals
# cold and update evals/routing/evals.json in the same commit.
#
# The R/D/W/C/O/P labels are hand-read from SKILL.md Steps 1-3 for each prompt.

GOLDENS = [
    ("5b", "Sonnet 5.5 · ultracode", "Sol Ultra · xhigh",
     dict(cap="terminal-tool", R=1, D=3, W=3, C=3, P="high", P_kind="targets", dur_gt30=True)),
    ("i1", "Sonnet 5.5 · ultracode", "Sol Ultra · xhigh",
     dict(cap="parallel-independent", R=1, D=3, W=3, C=2, P="high", P_kind="targets",
          dur_gt30=True)),
    ("x1", "Fable 5.1 · ultracode", "Astra · high",
     dict(cap="terminal-tool", R=1, D=2, W=3, C=3, O="high", dur_gt30=True, builds=True,
          agentic_write=True, gates=["files_1000plus"])),
    ("d3", "Opus 4.8 · ultracode", "(no model)",
     dict(cap="terminal-tool", R=2, D=3, W=3, C=2, dur_gt30=True, builds=True,
          gates=["offensive_security"])),
    ("a1", "Opus 4.8 · ultracode", "Astra · xhigh",
     dict(cap="terminal-tool", R=2, D=3, W=3, C=2, dur_gt30=True, builds=True,
          gates=["offensive_security"], flags=["daybreak"])),
    ("d6", "opusplan", "Sol · max",
     dict(cap="deep-reasoning", R=3, D=3, W=3, C=3, O="high", A="high", dur_gt30=True,
          indiv=True, builds=True, agentic_write=True, structured_design=True,
          front_loaded=True)),
    ("f1", "Fable 5.1 · max", "Astra · max",
     dict(cap="agentic-code", R=3, D=3, W=3, C=3, O="high", dur_gt30=True, indiv=True,
          builds=True, agentic_write=True, gates=["files_1000plus"])),
    ("h1", "Opus 5.5 · max", "Sol · max",
     dict(cap="deep-reasoning", R=3, D=3, W=1, C=2, dur_gt30=True, indiv=True, builds=True)),
    ("t1", "Opus 5.5 · xhigh", "Sol · xhigh",
     dict(cap="terminal-tool", R=2, D=3, W=1, C=2, dur_gt30=True, builds=True)),
    ("b1", "Sonnet 5.5 · high", "Sol · high",
     dict(cap="agentic-code", R=1, D=2, W=2, C=2, dur_gt30=True, builds=True,
          agentic_write=True)),
    ("d2", "Sonnet 5.5 · high", "Sol · high",
     dict(cap="agentic-code", R=1, D=2, W=2, C=2, dur_gt30=True, builds=True,
          agentic_write=True)),
    ("x2", "Sonnet 5.5 · high", "Sol · high",
     dict(cap="workflow-automation", R=1, D=2, W=1, C=2, dur_gt30=True, builds=True)),
    ("m1", "Sonnet 5.5 · xhigh", "Sol · xhigh",
     dict(cap="deep-reasoning", R=3, D=3, W=1, C=1, dur_gt30=True)),
    ("q1", "Opus 5.5 · xhigh", "Sol · xhigh",
     dict(cap="deep-reasoning", R=3, D=3, W=1, C=1, dur_gt30=True, flags=["escalation"])),
    ("n1", "Sonnet 5.5 · medium", "Sol · medium",
     dict(cap="agentic-code", R=1, D=1, W=2, C=0, dur_gt30=True, builds=True)),
    ("k1", "Sonnet 5.5 · medium", "Sol · medium",
     dict(cap="agentic-code", R=1, D=1, W=1, C=1, builds=True)),
    ("g1", "Sonnet 5.5 · high", "Sol · high",
     dict(cap="computer-use", R=2, D=2, W=2, C=1, dur_gt30=True, builds=True,
          gates=["computer_use"])),
    ("a2", "Sonnet 5.5 · medium", "Sol · medium",
     dict(cap="long-context", R=0, D=1, W=3, C=3, gates=["corpus_1m", "context_over_200k"])),
    ("d4", "Fable 5.1 · high", "(no model)",
     dict(cap="science", R=1, D=2, W=1, C=2, gates=["biology"])),
    ("f2", "Sonnet 5.5 · xhigh", "Sol · xhigh",
     dict(cap="deep-reasoning", R=1, D=3, W=0, C=1)),
    ("p1", "Opus 5.5 · xhigh", "Sol · xhigh",
     dict(cap="deep-reasoning", R=1, D=3, W=0, C=0, dur_gt30=True, builds=True)),
    # iteration-18 stabilization boundary evals
    ("o1", "Opus 5.5 · ultracode", "Sol · xhigh",
     dict(cap="agentic-code", R=3, D=3, W=3, C=2, dur_gt30=True, builds=True,
          agentic_write=True, indiv=False)),
    ("sh1", "Opus 5.5 · high", "Sol · high",
     dict(cap="terminal-tool", R=1, D=2, W=1, C=1, builds=False, agentic_write=False,
          flags=["escalation"])),
    # iteration-20: E4 retired -- the same labels that used to reach Astra xhigh stay on Sol max
    ("e4p", "Opus 5.5 · max", "Sol · max",
     dict(cap="agentic-code", R=3, D=3, W=2, C=2, indiv=True, dur_gt30=True, builds=True,
          agentic_write=True)),
    ("fr1", "Fable 5.1 · xhigh", "Astra · xhigh",
     dict(cap="agentic-code", R=2, D=3, W=2, C=3, A="high", dur_gt30=True, builds=True,
          agentic_write=True, flags=["escalation", "prior_run_fell_short"])),
]

for eid, want_cl, want_cx, labels in GOLDENS:
    task = prompt("eval-" + eid, **labels)
    check("golden %s still routes to %s / %s" % (eid, want_cl, want_cx),
          (R.cell_of(R.route_claude(task, "after")), R.cell_of(R.route_codex(task, "after"))),
          (want_cl, want_cx))

print()
if FAILURES:
    print("%d FAILURE(S)" % len(FAILURES))
    for f_ in FAILURES:
        print("  - " + f_)
    sys.exit(1)
print("all reachability-tool tests passed")
