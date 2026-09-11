#!/usr/bin/env python3
"""Audit which model x effort x mode combinations the routing rules can produce.

    POLICY MIRROR   evals/reachability/routing_policy.json   hand-maintained
    CORPUS          evals/reachability/corpus.json           152 labelled prompts
    MATRIX          evals/reachability/reachability-matrix.json   GENERATED

The routing eval (`evals/routing/`) measures CORRECTNESS: given a prompt, is the
golden answer produced? This script measures COVERAGE: given the whole rule set,
is there any prompt at all that reaches `Sonnet 5 · ultracode`? Those are
different questions and a suite that passes the first can be silently dead on the
second.

A combination the product supports but no rule can reach is a routing bug unless
somebody wrote down why it should be unreachable. That "unless" is the
`intentional_zero` table below -- every zero must be claimed by a reason, and an
unclaimed zero fails the run.

Usage:
    python scripts/check_routing_reachability.py            # write the matrix
    python scripts/check_routing_reachability.py --check    # fail if stale
    python scripts/check_routing_reachability.py --before   # route under the old rules
    python scripts/check_routing_reachability.py --report   # human-readable histograms
"""
from __future__ import annotations

import argparse
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POLICY = ROOT / "evals" / "reachability" / "routing_policy.json"
CORPUS = ROOT / "evals" / "reachability" / "corpus.json"
REVIEW = ROOT / "evals" / "reachability" / "flip-review.json"
OUT = ROOT / "evals" / "reachability" / "reachability-matrix.json"

RUNGS = ["low", "medium", "high", "xhigh", "max"]
FLAGSHIP_CAPS = {"agentic-code", "terminal-tool", "deep-reasoning", "science",
                 "computer-use", "workflow-automation"}
CLAUDE_FLAGSHIPS = {"Opus 5", "Opus 4.8", "Fable 5.1", "Mythos 5.1"}
CODEX_FLAGSHIPS = {"Sol", "Astra"}

# Dominant capability -> which arm the badge defaults to, conditioned on which
# Codex model is on the line. Mirrors SKILL.md Step 6's badge table.
BADGE = {
    "agentic-code":          ("claude", "codex"),
    "terminal-tool":         ("claude", "codex"),
    "science":               ("claude", "codex"),
    "knowledge-work":        ("claude", "claude"),
    "workflow-automation":   ("claude", "codex"),
    "computer-use":          ("claude", "codex"),
    "latency-volume":        ("codex", "codex"),
    "parallel-independent":  ("codex", "codex"),
    "long-context":          ("claude", "claude"),
    "deep-reasoning":        ("claude", "claude"),
    "research-synthesis":    ("claude", "claude"),
    "doc-data-understanding": ("claude", "claude"),
}


def rung_max(a: str, b: str) -> str:
    return a if RUNGS.index(a) >= RUNGS.index(b) else b


def bump(rung: str, cap_at: str) -> str:
    """One rung up, never past `cap_at` -- and never DOWN.

    A "+1 notch" that lowers a rung is not a notch. The cap exists to stop the
    notch climbing to `max`; it must not pull a rung that some other rule
    already put at `max` back down. Getting this wrong silently deleted
    `Sol - max` from every route the notch touched.
    """
    nxt = RUNGS[min(RUNGS.index(rung) + 1, len(RUNGS) - 1)]
    capped = nxt if RUNGS.index(nxt) <= RUNGS.index(cap_at) else cap_at
    return rung_max(rung, capped)


# --------------------------------------------------------------------------
# The routing engine. A `variant` is the SET of iteration-18 deltas that are
# switched on, so one engine produces both sides of the report -- and, by
# switching exactly one delta off at a time, attributes every decision flip to
# the rule that caused it without anybody hand-labelling which rule it was.
# --------------------------------------------------------------------------

DELTAS = ("ultracode", "ultra", "notch_cap", "rung3", "E4")
BEFORE: frozenset = frozenset()
AFTER: frozenset = frozenset(DELTAS)


def _variant(variant) -> frozenset:
    if variant == "before":
        return BEFORE
    if variant == "after":
        return AFTER
    return frozenset(variant)

def ultracode_fires(t: dict, variant) -> bool:
    """`ultracode` buys dynamic workflow orchestration, so it keys on O, not W.

    The width disjunct survives only with a depth qualifier. 100+ units of work
    that each need judgement (a 180-service auth-bypass audit) is orchestration
    at scale; 150 files of `userId` -> `accountId` is one mechanical edit
    repeated, and buying orchestration for it is pure quota waste. W alone
    cannot tell those apart -- both are W=3 -- so the per-unit depth does.
    """
    if "ultracode" not in _variant(variant):
        return t["W"] == 3 and t["dur_gt30"] and not (t["D"] == 3 and t["R"] == 3)
    return (t["dur_gt30"]
            and (t["O"] == "high" or (t["W"] == 3 and t["D"] >= 2))
            and not t["indiv"])


def ultra_fires(t: dict, variant) -> bool:
    if t["D"] != 3:
        return False
    if "ultra" not in _variant(variant):
        # Only already-independent TARGETS counted. Strands of work inside one
        # job did not.
        return t["P"] == "high" and t.get("P_kind") == "targets"
    return t["P"] == "high"


def rung3_escalation(t: dict) -> bool:
    """Soft frontier escalation: Opus 5 -> Fable 5.1, Sol -> Astra.

    Anthropic's own wording is the trigger: 'if your evals at xhigh or max still
    fall short on demanding reasoning or long-horizon agentic work'. A stated
    shortfall is required -- a long session on its own is not enough, because the
    aggregate evidence puts Fable 5.1 inside the equivalence band against Opus 5
    at higher cost per task.
    """
    return ("prior_run_fell_short" in t["flags"]
            and t["A"] == "high"
            and t["cap"] in FLAGSHIP_CAPS)


def route_claude(t: dict, variant) -> dict:
    v = _variant(variant)
    if t.get("step0_block"):
        return {"model": None, "effort": None, "mode": None, "note": "step0-block"}

    gates = set(t["gates"])
    mode = None
    floor = None

    if "latency_volume" in gates:
        return {"model": "Haiku 4.5", "effort": None, "mode": None, "note": "gate:latency"}

    if "offensive_security" in gates:
        model = "Mythos 5.1" if "glasswing" in t["flags"] else "Opus 4.8"
        floor = "xhigh"
        gate = "offensive"
    elif "biology" in gates:
        model, gate = "Fable 5.1", "biology"
    elif "files_1000plus" in gates:
        model, gate = "Fable 5.1", "frontier-scale"
    else:
        gate = None
        D, C, W, R = t["D"], t["C"], t["W"], t["R"]
        haiku_ok = "context_over_200k" not in gates
        if D == 0 and W == 0 and C <= 1 and R <= 1 and haiku_ok:
            model = "Haiku 4.5"
        elif max(D, C) <= 2 or D < 3:
            model = "Sonnet 5"
        else:
            model = "Opus 5" if (t["cap"] in FLAGSHIP_CAPS and t["builds"]) else "Sonnet 5"

        # Step 7 Rule 2 -- escalation is a model change, never an effort change.
        if "escalation" in t["flags"] or "prior_run_fell_short" in t["flags"]:
            if model == "Sonnet 5":
                model = "Opus 5"
            elif model == "Haiku 4.5":
                model = "Sonnet 5"
        if "rung3" in v and model == "Opus 5" and rung3_escalation(t):
            model = "Fable 5.1"

    if model == "Haiku 4.5":
        # SKILL.md Step 4: "Haiku 4.5 selected -> leave the effort field blank."
        # The gate branch returned early with no effort, but the SCORED branch can
        # also land on Haiku, and it used to fall through to the D table and emit
        # `Haiku 4.5 - low` -- an effort on a model that has no effort parameter.
        return {"model": model, "effort": None, "mode": None, "note": gate or "scored"}

    effort = {0: "low", 1: "medium", 2: "high", 3: "xhigh"}[t["D"]]
    if t["D"] == 3 and t["R"] == 3 and model in CLAUDE_FLAGSHIPS and t["indiv"]:
        effort = "max"
    if floor:
        effort = rung_max(effort, floor)

    # opusplan overrides the Opus 5 branch.
    if (model == "Opus 5" and gate is None and t["D"] == 3 and max(t["D"], t["C"]) == 3
            and t.get("structured_design") and t.get("front_loaded") and t["W"] >= 2):
        plan = "max" if t["R"] == 3 else "xhigh"
        return {"model": "opusplan", "effort": "plan:%s/execute:medium" % plan,
                "mode": "opusplan", "note": "opusplan"}

    if model != "Haiku 4.5" and effort != "max" and ultracode_fires(t, variant):
        effort, mode = "ultracode", "ultracode"

    return {"model": model, "effort": effort, "mode": mode, "note": gate or "scored"}


def route_codex(t: dict, variant) -> dict:
    v = _variant(variant)
    if t.get("step0_block"):
        return {"model": None, "effort": None, "mode": None, "note": "step0-block"}

    gates = set(t["gates"])
    mode = None
    floor = None

    if "latency_volume" in gates:
        return {"model": "Luna", "effort": "low", "mode": None, "note": "gate:latency"}
    if "offensive_security" in gates:
        if "daybreak" not in t["flags"]:
            return {"model": None, "effort": None, "mode": None, "note": "declined:offensive"}
        model, floor, gate = "Astra", "xhigh", "offensive+daybreak"
    elif "biology" in gates:
        return {"model": None, "effort": None, "mode": None, "note": "declined:biology-unverified"}
    elif "files_1000plus" in gates or "corpus_1m" in gates:
        model, gate = "Astra", "frontier-scale"
    elif "computer_use" in gates:
        model, gate = "Astra", "computer-use"
    else:
        gate = None
        D, C, W, R = t["D"], t["C"], t["W"], t["R"]
        if D == 0 and W == 0 and C <= 1 and R <= 1:
            model = "Luna"
        elif max(D, C) <= 2 or D < 3:
            model = "Terra"
        elif ultra_fires(t, variant):
            model, mode = "Sol", "ultra"
        elif t["cap"] in FLAGSHIP_CAPS and t["builds"]:
            model = "Sol"
        else:
            model = "Terra"

        if "escalation" in t["flags"] or "prior_run_fell_short" in t["flags"]:
            if model == "Terra":
                model = "Sol"
            elif model == "Luna":
                model = "Terra"
        if "rung3" in v and model == "Sol" and rung3_escalation(t):
            model = "Astra"

    effort = {0: "low", 1: "medium", 2: "high", 3: "xhigh"}[t["D"]]
    if t["D"] == 3 and t["R"] == 3 and model in CODEX_FLAGSHIPS and t["indiv"]:
        effort = "max"

    # +1 agentic-coding notch. Never on Astra.
    if t.get("agentic_write") and model in ("Terra", "Sol"):
        cap_at = "xhigh" if (model == "Terra" or "notch_cap" in v) else "max"
        effort = bump(effort, cap_at)

    if floor:
        effort = rung_max(effort, floor)

    # Rule E4 -- capability-scoped. Astra xhigh outscores Sol max on the AA index
    # at near-parity cost and far fewer output tokens, but only where the
    # task-specific evidence agrees (agentic-code / terminal-tool). HLE puts Astra
    # behind on deep-reasoning, so E4 must not fire there.
    if ("E4" in v and model == "Sol" and effort == "max"
            and t["cap"] in ("agentic-code", "terminal-tool")):
        model, effort = "Astra", "xhigh"
        mode = mode  # Ultra, if it was on, rides along -- Astra supports it.

    return {"model": model, "effort": effort, "mode": mode, "note": gate or "scored"}


def badge(t: dict, cl: dict, cx: dict) -> str | None:
    if cl["model"] is None and cx["model"] is None:
        return None
    if cx["model"] is None:
        return "claude"
    if cl["model"] is None:
        return "codex"
    if t["D"] <= 1:
        return "codex" if cl["model"] == "Haiku 4.5" else "claude"
    col = 1 if cx["model"] == "Astra" else 0
    row = BADGE.get(t["cap"])
    return row[col] if row else "claude"


def cell_name(model: str | None, effort: str | None, mode: str | None) -> str:
    if model is None:
        return "(no model)"
    if model == "opusplan":
        return "opusplan"
    label = model
    if mode == "ultra":
        label += " Ultra"
    if effort:
        label += " · " + effort
    return label


def attribute(t: dict) -> list:
    """Which iteration-18 delta(s) changed this prompt's route.

    Switch exactly one delta off and see whether the route falls back to what the
    old rules produced. Deterministic, so nobody has to hand-label "the rule
    responsible" in a review table and then let the label rot. A flip with an
    empty attribution is a rule INTERACTION -- no single delta explains it -- and
    the reviewer is told so rather than shown a guess.
    """
    before = (cell_of(route_claude(t, BEFORE)), cell_of(route_codex(t, BEFORE)))
    after = (cell_of(route_claude(t, AFTER)), cell_of(route_codex(t, AFTER)))
    if before == after:
        return []
    blamed = []
    for d in DELTAS:
        minus = AFTER - {d}
        if (cell_of(route_claude(t, minus)), cell_of(route_codex(t, minus))) == before:
            blamed.append(d)
    if blamed:
        return blamed
    # No single delta restores the old route; report every delta that moves it.
    return sorted(d for d in DELTAS
                  if (cell_of(route_claude(t, AFTER - {d})),
                      cell_of(route_codex(t, AFTER - {d}))) != after) or ["rule-interaction"]


def cell_of(d: dict) -> str:
    return cell_name(d["model"], d["effort"], d["mode"])


def route_all(corpus: list, variant) -> list:
    out = []
    for t in corpus:
        cl, cx = route_claude(t, variant), route_codex(t, variant)
        out.append({"id": t["id"], "claude": cl, "codex": cx,
                    "badge": badge(t, cl, cx)})
    return out


# --------------------------------------------------------------------------
# Reachability matrix
# --------------------------------------------------------------------------

# Every zero must be claimed. Key is "<ecosystem>|<model>|<effort_or_mode>".
INTENTIONAL = {
    "claude|Sonnet 5|max": ("INTENTIONALLY_UNREACHABLE",
        "Rule E1: Sonnet 5 max scores 38 at $5.09 while Opus 5 xhigh scores 50 at $4.88. "
        "Stronger and cheaper, so there is no task on which the premium is rational. "
        "The escalation target is Opus 5 · xhigh."),
    "claude|Opus 5|low": ("INTENTIONALLY_RARE",
        "Opus 5 is selected at D=3, and D=3 maps to xhigh. The only path down is an explicit "
        "user escalation on a D=0 task, which is coherent but vanishingly rare."),
    "claude|Opus 4.8|low": ("INTENTIONALLY_UNREACHABLE",
        "Opus 4.8 is reachable only through the offensive-security gate, which carries an xhigh floor."),
    "claude|Opus 4.8|medium": ("INTENTIONALLY_UNREACHABLE", "Same xhigh floor."),
    "claude|Opus 4.8|high": ("INTENTIONALLY_UNREACHABLE", "Same xhigh floor."),
    "claude|Opus 4.8|max": ("INTENTIONALLY_RARE",
        "Structurally reachable -- the offensive-security gate does not bypass the effort table, so "
        "D=3 AND R=3 AND an indivisible novel-design decision would emit it -- but deliberately "
        "unrepresented, for two reasons. (1) Evidence: benchmarks.json carries ZERO records for "
        "Opus 4.8 at any rung, so there is no published effort curve to justify spending the top "
        "rung on it; Rule E3 already holds `max` back on Opus 5, where a curve does exist and the "
        "gain is one index point. (2) Scope: reaching this cell needs an offensive-security prompt "
        "whose output is irreversible against a live target, and this audit does not author "
        "operational examples for gated task categories. The gate's own routing role is carried by "
        "Opus 4.8 xhigh and Opus 4.8 ultracode, both reachable. Abstract placeholder only."),
    "claude|Mythos 5.1|low": ("INTENTIONALLY_UNREACHABLE", "Same xhigh floor, plus Glasswing access."),
    "claude|Mythos 5.1|medium": ("INTENTIONALLY_UNREACHABLE", "Same xhigh floor, plus Glasswing access."),
    "claude|Mythos 5.1|high": ("INTENTIONALLY_UNREACHABLE", "Same xhigh floor, plus Glasswing access."),
    "claude|Mythos 5.1|xhigh": ("INTENTIONALLY_RARE",
        "Conditional access. Reachable only when the user states Project Glasswing access."),
    "claude|Mythos 5.1|max": ("INTENTIONALLY_RARE",
        "Same reasoning as Opus 4.8 max -- the offensive gate is the only route, `max` needs an "
        "indivisible novel-design decision at D=3 AND R=3 on top, there is no Mythos 5.1 effort "
        "curve in the evidence store, and the audit authors no operational offensive prompts. "
        "Conditional access (Project Glasswing) narrows it further."),
    "claude|Mythos 5.1|ultracode": ("INTENTIONALLY_RARE", "Conditional access."),
    "claude|Fable 5.1|low": ("INTENTIONALLY_RARE",
        "Fable 5.1 is gated to biology, 1000+ files, or a stated flagship-tier shortfall. "
        "All three imply real depth, so the bottom rungs are coherent but rare."),
    "claude|Fable 5.1|medium": ("INTENTIONALLY_RARE", "Same reason."),
    "claude|Haiku 4.5|low": ("UNSUPPORTED", "Haiku 4.5 has no effort parameter."),
    "claude|Haiku 4.5|medium": ("UNSUPPORTED", "Haiku 4.5 has no effort parameter."),
    "claude|Haiku 4.5|high": ("UNSUPPORTED", "Haiku 4.5 has no effort parameter."),
    "claude|Haiku 4.5|xhigh": ("UNSUPPORTED", "Haiku 4.5 has no effort parameter."),
    "claude|Haiku 4.5|max": ("UNSUPPORTED", "Haiku 4.5 has no effort parameter."),
    "claude|Haiku 4.5|ultracode": ("UNSUPPORTED", "ultracode needs xhigh support; Haiku has none."),
    "codex|Terra|max": ("UNSUPPORTED",
        "learn.chatgpt.com: max and Ultra are Astra/Sol only. Rule E2 independently shows "
        "Terra max is dominated by Sol high (42 at $1.40 vs 42 at $0.81)."),
    "codex|Luna|max": ("UNSUPPORTED", "max is Astra/Sol only."),
    "codex|Luna|medium": ("INTENTIONALLY_UNREACHABLE",
        "Luna is the volume tier. Its long-context recall drops to ~41% against Sol's ~91%, so "
        "the router deliberately never sends D>=1 codebase work to it -- that work goes to Terra."),
    "codex|Luna|high": ("INTENTIONALLY_UNREACHABLE", "Same reason."),
    "codex|Luna|xhigh": ("INTENTIONALLY_UNREACHABLE", "Same reason."),
    "codex|Luna|ultra": ("UNSUPPORTED", "Ultra is Astra/Sol only."),
    "codex|Terra|ultra": ("UNSUPPORTED", "Ultra is Astra/Sol only."),
    "codex|Sol|low": ("INTENTIONALLY_RARE",
        "Sol is reached at D=3, or by escalation from Terra which keeps the rung. A D=0 escalation "
        "is coherent but vanishingly rare."),
    "codex|Sol|medium": ("INTENTIONALLY_RARE", "Same reason as Sol low."),
    "codex|Astra|low": ("INTENTIONALLY_RARE",
        "Astra is gate-reached. A 1000+ file or 1M-corpus task at D=0 is coherent but rare."),
    "codex|Sol Ultra|low": ("INTENTIONALLY_UNREACHABLE", "Ultra requires D=3, which maps to xhigh or above."),
    "codex|Sol Ultra|medium": ("INTENTIONALLY_UNREACHABLE", "Ultra requires D=3."),
    "codex|Sol Ultra|high": ("INTENTIONALLY_UNREACHABLE",
        "Ultra requires D=3. Holding Ultra at D=3 is deliberate: it runs ~4 collaborating agents, "
        "so it costs roughly 4x, and at D<=2 Terra already clears the bar."),
    "codex|Sol Ultra|max": ("INTENTIONALLY_UNREACHABLE",
        "Ultra and `max` ask for contradictory labels, so no consistent prompt reaches this cell. "
        "Ultra needs P=high -- 3+ strands that proceed without waiting on each other and merge at "
        "the end. `max` needs `indivisible_single_chain` -- the difficulty is ONE indivisible "
        "novel-design or formal decision. A task cannot be both, and routing_policy.json's P "
        "definition says so outright ('one coherent decision sliced up after the fact ... is ONE "
        "boundary decision, not four strands'). Two prompts DID reach Sol Ultra max under the old "
        "rules, but neither was indivisible: the rung came from the +1 agentic notch climbing to "
        "`max`, which iteration-18 caps at xhigh because Step 7 Rule 2 makes escalation a model "
        "change, not an effort change, and because Rule E3 refuses `max` for breadth-driven work. "
        "Both prompts were breadth-driven migrations, so that is the rule working. Enforced by the "
        "corpus-contradiction lint below, not just asserted here."),
    "codex|Astra Ultra|low": ("INTENTIONALLY_UNREACHABLE", "See Astra Ultra xhigh."),
    "codex|Astra Ultra|medium": ("INTENTIONALLY_UNREACHABLE", "See Astra Ultra xhigh."),
    "codex|Astra Ultra|high": ("INTENTIONALLY_UNREACHABLE", "See Astra Ultra xhigh."),
    "codex|Astra Ultra|xhigh": ("INTENTIONALLY_UNREACHABLE",
        "Ultra does run on Astra (learn.chatgpt.com, 10 Sep 2026), but both routes to Astra close "
        "this cell. (1) Every GATE route to Astra is a deciding gate, and a deciding gate bypasses "
        "Step 4, where path (a) -- the only thing that switches Ultra on -- lives. (2) Iteration-18 "
        "added a second, non-gate route: Rule E4 rewrites `Sol - max` to `Astra - xhigh`, and mode "
        "rides along. That door is shut too, because `Sol Ultra - max` is itself unreachable (see "
        "its entry: Ultra needs P=high, `max` needs indivisible, and nothing is both). Recorded as "
        "a known structural gap rather than papered over: the workload that would need it (1000+ "
        "files AND 3+ genuinely independent targets) is real but narrow, and opening it would mean "
        "letting a mode survive a deciding gate, which is a larger change than this audit's "
        "evidence supports."),
    "codex|Astra Ultra|max": ("INTENTIONALLY_UNREACHABLE",
        "Both reasons stack: the Astra Ultra gap above, and the Ultra-vs-indivisible contradiction "
        "recorded under Sol Ultra max."),
}


def build_matrix(policy: dict, corpus: list, results_after: list, results_before: list,
                 review: dict | None = None) -> dict:
    review = review or {"flips": {}}
    sup = policy["support_matrix"]
    by_id = {t["id"]: t for t in corpus}

    def observe(results):
        seen: dict[str, list] = {}
        for r in results:
            for eco in ("claude", "codex"):
                d = r[eco]
                if d["model"] is None:
                    continue
                if d["model"] == "opusplan":
                    k = "claude|opusplan|plan/execute split"
                else:
                    label = d["model"] + (" Ultra" if d["mode"] == "ultra" else "")
                    effort = d["effort"] if d["effort"] else "(no effort parameter)"
                    k = "%s|%s|%s" % (eco, label, effort)
                seen.setdefault(k, []).append(r["id"])
        return seen

    obs_after, obs_before = observe(results_after), observe(results_before)

    rows = []
    for eco in ("claude", "codex"):
        for model, spec in sup[eco].items():
            # A "cell" is a value the router can write in the effort field of THIS
            # model's line. That is the effort rungs, plus 'ultracode' (which the
            # Claude arm writes into the effort field). 'ultra' is not an effort
            # field value -- it is a model-label change, represented by the
            # separate 'Sol Ultra' / 'Astra Ultra' rows below. 'opusplan' is not
            # an Opus 5 effort -- it replaces the whole model line and has its own
            # row appended after this loop.
            slots = list(spec["efforts"])
            if "ultracode" in spec["modes"]:
                slots.append("ultracode")
            # A model with no effort parameter still produces one row, but that row
            # is the PLATFORM forcing the field blank -- not the policy choosing a
            # rung. Counting it as a healthy policy-selected route would let an arm
            # look covered because a product limitation filled the cell in.
            forced = not slots
            if forced:
                slots = ["(no effort parameter)"]
            variants = [(model, slots)]
            if "ultra" in spec["modes"]:
                variants.append((model + " Ultra", list(spec["efforts"])))
            for label, cells in variants:
                for cell in cells:
                    key = "%s|%s|%s" % (eco, label, cell)
                    hits_after = obs_after.get(key, [])
                    hits_before = obs_before.get(key, [])
                    claimed = INTENTIONAL.get(key)
                    supported = True
                    if claimed and claimed[0] == "UNSUPPORTED":
                        supported = False
                    if hits_after:
                        status = "PLATFORM_FORCED" if forced else "HEALTHY"
                        if not forced and len(hits_after) > len(corpus) * 0.28:
                            status = "OVER_SELECTED"
                    elif claimed:
                        status = claimed[0]
                    else:
                        status = "UNINTENTIONALLY_UNREACHABLE"
                    rows.append({
                        "ecosystem": eco,
                        "model": label,
                        "effort_or_mode": cell,
                        "supported": supported,
                        "platform_forced": forced,
                        "reachable_by_current_rules": bool(hits_after) or (
                            claimed is not None and claimed[0] in
                            ("INTENTIONALLY_RARE",)),
                        "observed_before": len(hits_before),
                        "observed_after": len(hits_after),
                        "representative_prompt_ids": hits_after[:4],
                        "recovered_by_this_pass": bool(hits_after) and not hits_before,
                        "lost_by_this_pass": bool(hits_before) and not hits_after,
                        "status": status,
                        "rationale": claimed[1] if claimed else None,
                    })

    # opusplan is a Claude Code mode with no effort cell of its own. It gets a row
    # only when some Claude model actually declares the mode -- otherwise a policy
    # that does not offer opusplan would be told opusplan is unreachable.
    for eco_key, label in ([("claude", "opusplan")]
                           if any("opusplan" in spec["modes"] for spec in sup["claude"].values())
                           else []):
        hits_a = obs_after.get("claude|opusplan|plan/execute split", [])
        hits_b = obs_before.get("claude|opusplan|plan/execute split", [])
        rows.append({
            "ecosystem": "claude", "model": "opusplan", "effort_or_mode": "plan/execute split",
            "supported": True, "platform_forced": False,
            "reachable_by_current_rules": bool(hits_a),
            "observed_before": len(hits_b), "observed_after": len(hits_a),
            "representative_prompt_ids": hits_a[:4],
            "recovered_by_this_pass": False, "lost_by_this_pass": False,
            "status": "HEALTHY" if hits_a else "UNINTENTIONALLY_UNREACHABLE",
            "rationale": None,
        })

    rows.sort(key=lambda r: (r["ecosystem"], r["model"], r["effort_or_mode"]))

    def hist(results, key, field):
        h: dict[str, int] = {}
        for r in results:
            d = r[key]
            h[cell_name(d["model"], d["effort"] if field == "cell" else None, d["mode"])] = \
                h.get(cell_name(d["model"], d["effort"] if field == "cell" else None, d["mode"]), 0) + 1
        return dict(sorted(h.items()))

    def badges(results):
        h: dict[str, int] = {}
        for r in results:
            h[str(r["badge"])] = h.get(str(r["badge"]), 0) + 1
        return dict(sorted(h.items()))

    flips = []
    before_by_id = {r["id"]: r for r in results_before}
    for r in results_after:
        b = before_by_id[r["id"]]
        a_cl = cell_name(r["claude"]["model"], r["claude"]["effort"], r["claude"]["mode"])
        b_cl = cell_name(b["claude"]["model"], b["claude"]["effort"], b["claude"]["mode"])
        a_cx = cell_name(r["codex"]["model"], r["codex"]["effort"], r["codex"]["mode"])
        b_cx = cell_name(b["codex"]["model"], b["codex"]["effort"], b["codex"]["mode"])
        if a_cl != b_cl or a_cx != b_cx:
            verdict, note = (review["flips"].get(r["id"]) or [None, None])[:2]
            flips.append({"id": r["id"], "prompt": by_id[r["id"]]["prompt"][:170],
                          "claude_before": b_cl, "claude_after": a_cl,
                          "codex_before": b_cx, "codex_after": a_cx,
                          "badge_before": b["badge"], "badge_after": r["badge"],
                          "rules_responsible": attribute(by_id[r["id"]]),
                          "verdict": verdict or "UNREVIEWED",
                          "review_note": note})

    return {
        "generator": "scripts/check_routing_reachability.py",
        "how_to_read": (
            "GENERATED -- do not hand-edit. One row per supported model x effort/mode cell. "
            "'observed_after' counts how many of the 152 corpus prompts land on that cell under the "
            "current rules; 'observed_before' does the same under the rules at commit 35ff226. A zero "
            "with no rationale is a bug: either the corpus is missing the workload (fix the corpus) or "
            "no rule can reach the cell (fix the rules). Counts are a diagnostic, never a target -- "
            "this file must not be used to flatten the distribution."
        ),
        "corpus_size": len(corpus),
        "matrix": rows,
        "histograms": {
            "claude_model_before": hist(results_before, "claude", "model"),
            "claude_model_after": hist(results_after, "claude", "model"),
            "claude_cell_before": hist(results_before, "claude", "cell"),
            "claude_cell_after": hist(results_after, "claude", "cell"),
            "codex_model_before": hist(results_before, "codex", "model"),
            "codex_model_after": hist(results_after, "codex", "model"),
            "codex_cell_before": hist(results_before, "codex", "cell"),
            "codex_cell_after": hist(results_after, "codex", "cell"),
            "badge_before": badges(results_before),
            "badge_after": badges(results_after),
        },
        "decision_flips": flips,
    }


# --------------------------------------------------------------------------
# Lint
# --------------------------------------------------------------------------

def lint(policy: dict, matrix: dict, corpus: list, review: dict) -> list:
    problems = []
    for row in matrix["matrix"]:
        key = "%s|%s|%s" % (row["ecosystem"], row["model"], row["effort_or_mode"])
        if row["status"] == "UNINTENTIONALLY_UNREACHABLE":
            problems.append(("ERROR", "unreachable",
                             "%s is supported but no corpus prompt reaches it and no rationale "
                             "claims the zero" % key))
        if not row["supported"] and row["observed_after"]:
            problems.append(("ERROR", "unsupported-but-emitted",
                             "%s is a product capability limit but the rules emit it on %s"
                             % (key, row["representative_prompt_ids"])))
        if row["status"] == "OVER_SELECTED":
            problems.append(("WARN", "over-selected",
                             "%s covers %d of %d corpus prompts -- check nothing better is being "
                             "shadowed" % (key, row["observed_after"], matrix["corpus_size"])))
        if row["lost_by_this_pass"]:
            claimed = " (zero is claimed: %s)" % row["status"] if row["rationale"] else ""
            problems.append(("WARN", "route-lost",
                             "%s was reachable under the previous rules and is not any more%s"
                             % (key, claimed)))

    # Conditional-access models must never appear without the access being stated.
    by_id = {t["id"]: t for t in corpus}
    for row in matrix["matrix"]:
        if row["model"].startswith("Mythos"):
            for pid in row["representative_prompt_ids"]:
                if "glasswing" not in by_id[pid]["flags"]:
                    problems.append(("ERROR", "conditional-access-leak",
                                     "Mythos 5.1 reached on %s without stated Glasswing access" % pid))

    # Every flip must be signed off, and no sign-off may outlive its flip. A flip
    # count is a number; this is the review.
    flipped = {f["id"] for f in matrix["decision_flips"]}
    for f in matrix["decision_flips"]:
        if f["verdict"] == "UNREVIEWED":
            problems.append(("ERROR", "flip-unreviewed",
                             "%s flips (%s -> %s / %s -> %s) with no verdict in flip-review.json"
                             % (f["id"], f["claude_before"], f["claude_after"],
                                f["codex_before"], f["codex_after"])))
        elif f["verdict"] == "REJECT":
            problems.append(("ERROR", "flip-rejected",
                             "%s is reviewed REJECT -- fix the rule or the label rather than "
                             "shipping the flip: %s" % (f["id"], f["review_note"])))
        elif f["verdict"] not in ("ACCEPT", "UNCERTAIN"):
            problems.append(("ERROR", "flip-verdict-unknown",
                             "%s carries verdict %r, which is not ACCEPT / REJECT / UNCERTAIN"
                             % (f["id"], f["verdict"])))
    for pid in sorted(review.get("flips", {})):
        if pid not in flipped:
            problems.append(("WARN", "flip-review-stale",
                             "flip-review.json signs off %s, which no longer flips -- delete the "
                             "entry or move it to rejected_during_review" % pid))

    # A label pair the rules treat as mutually exclusive must never co-occur.
    # `ultra` needs P=high (3+ strands that do not wait on each other); `max`
    # needs an indivisible single chain. A prompt carrying both would silently
    # manufacture a Sol Ultra - max route that the product ordering forbids, and
    # the zero recorded for that cell would become a lie.
    for t in corpus:
        if t["P"] == "high" and t["indiv"]:
            problems.append(("ERROR", "contradictory-labels",
                             "%s is labelled P=high AND indivisible_single_chain; a task that "
                             "splits into 3+ independent strands is not one indivisible decision"
                             % t["id"]))
        if t["O"] == "high" and t["W"] == 3 and t["D"] <= 1:
            problems.append(("WARN", "width-masquerading-as-orchestration",
                             "%s is W=3 at D<=1 but labelled O=high -- repeating one mechanical "
                             "step across many units is width, not orchestration" % t["id"]))

    # A model the platform gives no effort parameter must never be emitted with one.
    forced_models = {("%s|%s" % (eco, m))
                     for eco in ("claude", "codex")
                     for m, spec in policy["support_matrix"][eco].items()
                     if not spec["efforts"]}
    for row in matrix["matrix"]:
        key2 = "%s|%s" % (row["ecosystem"], row["model"])
        if key2 in forced_models and not row["platform_forced"] and row["observed_after"]:
            problems.append(("ERROR", "platform-forced-model-given-an-effort",
                             "%s|%s has no effort parameter but the rules emitted '%s' on %s"
                             % (key2, row["effort_or_mode"], row["effort_or_mode"],
                                row["representative_prompt_ids"])))

    # A cell the rules emit that the support matrix does not even list is worse
    # than one marked unsupported: it has no row, so every other check above is
    # blind to it. Re-route the corpus and demand a row for everything observed.
    known = {"%s|%s|%s" % (r["ecosystem"], r["model"], r["effort_or_mode"])
             for r in matrix["matrix"]}
    for res in route_all(corpus, AFTER):
        for eco in ("claude", "codex"):
            d = res[eco]
            if d["model"] is None:
                continue
            if d["model"] == "opusplan":
                key3 = "claude|opusplan|plan/execute split"
            else:
                label = d["model"] + (" Ultra" if d["mode"] == "ultra" else "")
                key3 = "%s|%s|%s" % (eco, label, d["effort"] or "(no effort parameter)")
            if key3 not in known:
                problems.append(("ERROR", "emitted-cell-not-in-support-matrix",
                                 "the rules emit %s on %s, but the support matrix lists no such "
                                 "cell -- so no reachability row covers it" % (key3, res["id"])))

    # Every roster model must appear in the policy support matrix.
    sup = policy["support_matrix"]
    for eco in ("claude", "codex"):
        for model in sup[eco]:
            if not any(r["model"] == model or r["model"].startswith(model + " ")
                       for r in matrix["matrix"]):
                problems.append(("ERROR", "model-missing-from-matrix",
                                 "%s / %s is in the support matrix but produced no matrix row"
                                 % (eco, model)))

    # A mode that no supported model carries is a dead product claim.
    for eco in ("claude", "codex"):
        modes = {m for spec in sup[eco].values() for m in spec["modes"]}
        for mode in modes:
            if mode == "opusplan":
                continue
            carriers = [r for r in matrix["matrix"]
                        if r["ecosystem"] == eco and (r["effort_or_mode"] == mode
                                                      or r["model"].endswith(" Ultra"))
                        and r["observed_after"]]
            if not carriers:
                problems.append(("WARN", "mode-dead",
                                 "%s / mode '%s' is supported but no corpus prompt reaches it on "
                                 "any model" % (eco, mode)))
    return problems


def dumps(obj: dict) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="exit 1 if the committed matrix is stale")
    ap.add_argument("--report", action="store_true", help="print histograms and findings")
    args = ap.parse_args()

    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))["prompts"]
    review = json.loads(REVIEW.read_text(encoding="utf-8"))

    after = route_all(corpus, "after")
    before = route_all(corpus, "before")
    matrix = build_matrix(policy, corpus, after, before, review)
    text = dumps(matrix)

    if args.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != text:
            print("STALE: %s does not match the policy + corpus. Re-run the script." % OUT)
            return 1
        print("reachability matrix is up to date")
    else:
        io.open(OUT, "w", encoding="utf-8", newline="\n").write(text)
        print("wrote %s" % OUT)

    problems = lint(policy, matrix, corpus, review)
    errors = [p for p in problems if p[0] == "ERROR"]
    for level, kind, msg in problems:
        print("%-5s [%s] %s" % (level, kind, msg))

    if args.report:
        h = matrix["histograms"]
        for name in ("claude_cell_before", "claude_cell_after",
                     "codex_cell_before", "codex_cell_after",
                     "badge_before", "badge_after"):
            print("\n== %s ==" % name)
            for k, v in sorted(h[name].items(), key=lambda kv: (-kv[1], kv[0])):
                print("  %-34s %d" % (k, v))
        print("\n== decision flips: %d ==" % len(matrix["decision_flips"]))
        tally: dict[str, int] = {}
        by_rule: dict[str, int] = {}
        for f in matrix["decision_flips"]:
            tally[f["verdict"]] = tally.get(f["verdict"], 0) + 1
            for rule in f["rules_responsible"]:
                by_rule[rule] = by_rule.get(rule, 0) + 1
        for k, v in sorted(tally.items()):
            print("  %-34s %d" % (k, v))
        print("  -- flips by rule --")
        for k, v in sorted(by_rule.items(), key=lambda kv: (-kv[1], kv[0])):
            print("  %-34s %d" % (k, v))

    print("\n%d error(s), %d warning(s)"
          % (len(errors), len(problems) - len(errors)))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
