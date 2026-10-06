#!/usr/bin/env python3
"""Prove that skill/SKILL.md's OpenCode arm matches the machine-readable policy.

    MIRROR   evals/policy/routing_policy.json   the 15-model pool, Step 4-OC rows, badge table
    RUNTIME  skill/SKILL.md                      the only file the router reads

Checks (all mechanical, all fail loudly):

  1. The roster table names exactly the 15 pool models, with the same Go cap.
  2. Every Step 4-OC row (R<=2 pair, R=3 pair, NC1 variants) equals the mirror,
     and no row ever emits a model whose status is `dominated`.
  3. The badge table (side at R<=2, side at R=3, dagger) equals the mirror.
  4. Every OpenCode line in a worked example names only routable pool models, an
     effort that OpenCode actually offers for that model (policy `opencode_variants`), never `GLM-5.3 · low` / `Kimi K3 · low`, and never a
     USD 15-cap model at `low` (only the latency row's GPT 6 Luna is exempt).
  5. No model outside the 15 appears in a Step 4-OC row or an example.

    python scripts/check_opencode_pool.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POLICY = ROOT / "evals" / "policy" / "routing_policy.json"
SKILL = ROOT / "skill" / "SKILL.md"


def cells(row: str) -> list[str]:
    return [c.strip() for c in row.strip().strip("|").split("|")]


def table_after(skill: str, heading: str, heading_is_header: bool = False) -> list[list[str]]:
    """Data rows of the first markdown table after `heading` (the header row is dropped).
    If `heading` is itself the table's header line, pass heading_is_header=True."""
    i = skill.find(heading)
    if i < 0:
        return []
    rows, started = [], False
    for ln in (skill[i:].split("\n") if heading_is_header else skill[i:].split("\n")[1:]):
        s = ln.strip()
        if s.startswith("|"):
            started = True
            if set(s.replace("|", "").strip()) <= set("-: "):
                continue
            rows.append(cells(s))
        elif started:
            break
    return rows if heading_is_header else rows[1:]


def models_in(text: str, names: list[str]) -> list[str]:
    pat = "|".join(re.escape(n) for n in sorted(names, key=len, reverse=True))
    return re.findall(pat, text)


def strip_md(s: str) -> str:
    return re.sub(r"[*`]", "", s).strip()


def main() -> int:
    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    skill = SKILL.read_text(encoding="utf-8")
    pool = policy["pool"]["models"]
    outside = policy["pool"]["outside_main_pool"]
    names = list(pool)
    errors: list[str] = []

    # 1 -- roster -----------------------------------------------------------------
    roster = table_after(skill, "**OpenCode Go pool — the 15 main models**")
    roster_caps = {}
    for r in roster:
        if len(r) < 7 or not r[0].isdigit():
            continue
        roster_caps[strip_md(r[1])] = int(re.sub(r"\D", "", strip_md(r[5])) or 0)
    if set(roster_caps) != set(names):
        errors.append("roster table names %s; policy pool is %s" %
                      (sorted(set(roster_caps) ^ set(names)), len(names)))
    for m, cap in roster_caps.items():
        if m in pool and pool[m]["cap_usd"] != cap:
            errors.append("roster cap for %s is USD %d, policy says USD %d" % (m, cap, pool[m]["cap_usd"]))
    if len(roster_caps) != 15:
        errors.append("roster must hold exactly 15 models, found %d" % len(roster_caps))

    # 2 -- Step 4-OC rows ---------------------------------------------------------
    rows = table_after(skill, "| Dominant capability | `R ≤ 2` → `#1` · `#2` |", True)
    if not rows:
        errors.append("could not find the Step 4-OC table in SKILL.md")
    want = policy["step4_oc_rows"]
    seen = set()
    for r in rows:
        if len(r) < 4:
            continue
        cap_cell, r2, r3, evid = r[0], r[1], r[2], r[3]
        tags = re.findall(r"`([a-z-]+)`", cap_cell)
        key_tags = [t for t in tags if t in want or t in
                    ("agentic-code", "terminal-tool", "deep-reasoning", "knowledge-work",
                     "workflow-automation", "long-context", "research-synthesis",
                     "doc-data-understanding", "science", "latency-volume")]
        if "D ≤ 1" in cap_cell and not key_tags:
            key_tags = ["D<=1"]
        if "anything else" in cap_cell:
            key_tags = ["other"]
        if not key_tags:
            continue  # orchestration / anything else are checked below
        a = models_in(r2, names)
        b = models_in(r3, names) if strip_md(r3) != "same" else a
        for t in key_tags:
            seen.add(t)
            w = want.get(t)
            if not w:
                errors.append("Step 4-OC row %r has no entry in the policy" % t)
                continue
            if a != w["r_le_2"]:
                errors.append("row %r R<=2: SKILL.md %s, policy %s" % (t, a, w["r_le_2"]))
            if b != w["r_eq_3"]:
                errors.append("row %r R=3: SKILL.md %s, policy %s" % (t, b, w["r_eq_3"]))
        if "NC1" in evid:
            m = re.search(r"NC1:\s*\**([^*·]+?)\s*·\s*([^*—]+?)\**\s*[—-]", evid)
            nc_tag = key_tags[0]
            nc_key = nc_tag + "+NC1"
            if nc_key in want:
                got = models_in(evid[evid.find("NC1"):], names)[:2]
                variant = want[nc_key]["r_le_2"]
                it = iter(variant)
                if not got or not all(g in it for g in got):  # got must be a subsequence of the variant
                    errors.append("row %r NC1 variant: SKILL.md %s, policy %s" % (nc_tag, got, variant))
    for t in want:
        if "+NC1" in t:
            continue
        if t not in seen:
            errors.append("policy row %r is missing from the Step 4-OC table" % t)

    # no emitted row may name a dominated or outside model
    oc_text = skill[skill.find("### OpenCode Go — Step 4-OC"):skill.find("#### OpenCode Go — effort")]
    table_only = "\n".join(ln for ln in oc_text.split("\n") if ln.strip().startswith("|"))
    for m, meta in pool.items():
        if meta["status"] == "dominated":
            for r in rows:
                if len(r) >= 3 and (m in r[1] or m in r[2]):
                    errors.append("Step 4-OC emits dominated model %s in row %r" % (m, r[0][:40]))
    for o in outside:
        for r in rows:
            if len(r) >= 3 and (o in r[1] or o in r[2]):
                errors.append("Step 4-OC emits %s, which is outside the 15-model pool" % o)

    # 3 -- badge table ------------------------------------------------------------
    brow = table_after(skill, "| Dominant capability | `R ≤ 2` | `R = 3` | Evidence to name |", True)
    wantb = policy["badge_table"]
    seenb = set()
    for r in brow:
        if len(r) < 4:
            continue
        tags = [t for t in re.findall(r"`([a-z-]+)`", r[0]) if t in wantb]
        for t in tags:
            seenb.add(t)
            w = wantb[t]
            s2 = "opencode" if "OpenCode" in r[1] else "claude" if "Claude" in r[1] else None
            s3 = "opencode" if "OpenCode" in r[2] else "claude" if "Claude" in r[2] else None
            dag = "†" in r[1] or "†" in r[2]
            if s2 != w["r_le_2"] or s3 != w["r_eq_3"]:
                errors.append("badge row %r: SKILL.md (%s, %s), policy (%s, %s)" %
                              (t, s2, s3, w["r_le_2"], w["r_eq_3"]))
            if dag != w["low_confidence"]:
                errors.append("badge row %r dagger: SKILL.md %s, policy %s" % (t, dag, w["low_confidence"]))
        if "orchestration" in r[0] and "orchestration" in wantb:
            seenb.add("orchestration")
            if "Claude" not in r[1] or "Claude" not in r[2]:
                errors.append("badge row orchestration must read Claude at both R levels")
    for t in wantb:
        if t not in seenb:
            errors.append("policy badge row %r is missing from SKILL.md" % t)

    # 4/5 -- worked examples ---------------------------------------------------------
    lines = skill.split("\n")
    fences = [i for i, ln in enumerate(lines) if ln.strip() == "```"]
    n_ex = 0
    for a, b in zip(fences[0::2], fences[1::2]):
        block = "\n".join(lines[a + 1:b])
        oc = next((ln.strip()[len("OpenCode:"):].strip() for ln in block.split("\n")
                   if ln.strip().startswith("OpenCode:")), None)
        if oc is None or "<" in oc:
            continue
        n_ex += 1
        if oc.lower().startswith(("use claude", "unverified")):
            continue
        parts = re.split(r"#\s*[12]\b", oc)[1:]
        for p in parts:
            used = models_in(p, names + outside)
            if not used:
                errors.append("example OpenCode pick names no pool model: %r" % p[:60])
                continue
            model = used[0]
            if model in outside:
                errors.append("example names %s, outside the 15-model pool" % model)
                continue
            st = pool[model]["status"]
            if st == "dominated":
                errors.append("example emits dominated model %s" % model)
            em = re.search(r"effort:\s*(\w+)", p)
            eff = em.group(1) if em else None
            allowed = policy["effort"]["opencode_variants"].get(model)
            if allowed is None:
                errors.append("no OpenCode variant list in the policy for %s" % model)
            elif eff not in allowed:
                errors.append("effort %r for %s is not an OpenCode variant of that model %s" % (eff, model, allowed))
            if eff == "low" and model in ("GLM-5.3", "Kimi K3"):
                errors.append("%s · low is dominated (Rule E6) and must never be emitted" % model)
            if eff == "low" and pool[model]["cap_usd"] == 15 and model != "GPT 6 Luna":
                errors.append("USD 15-cap model %s at low violates Rule CAP1 (D<=1 goes to the Flash tier)" % model)
            if st in ("routable-nc1",) and model != "Grok 4.7" and "non-confidential" not in block \
                    and "nothing confidential" not in block and "Luna" in model:
                errors.append("%s emitted without a stated non-confidentiality (Rule NC1)" % model)

    if n_ex == 0:
        errors.append("no OpenCode example lines found in SKILL.md — the parser or the file broke")

    for e in errors:
        print("ERROR [opencode-pool] %s" % e)
    if errors:
        print("\n%d error(s). The shipped OpenCode arm must match the policy mirror." % len(errors))
        return 1
    print("opencode pool OK: %d pool models, %d Step 4-OC rows, %d badge rows, %d example lines match the policy"
          % (len(roster_caps), len(seen), len(seenb), n_ex))
    return 0


if __name__ == "__main__":
    sys.exit(main())
