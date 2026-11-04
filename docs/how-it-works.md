# How it works

The long form of the README: why the router exists, how it treats evidence, and the steps it runs (Step 0 to Step 7). Only [`skill/SKILL.md`](../skill/SKILL.md) is read when routing; this page is for auditing.

## Why this exists

The failure mode isn't picking a model that's too weak. It's **reflexively picking
the most expensive model** and burning your quota — Claude's 5-hour window *and* a
Go model's per-model dollar cap. Those are the protected resources.

The decision principle, in one sentence:

> **Select the lowest-quota model × effort combination that stays on the
> task-specific capability frontier.** Prefer the stronger candidate when the
> task-relevant performance difference is meaningful; prefer the more
> quota-efficient candidate when capability sits inside a defensible equivalence
> band.

Not "always cheapest". Not "always strongest". Not "highest benchmark score wins".

```
prompt
  → quality gate                     (Step 0)
  → hard gates: capability/safety/availability/retention   (Step 1)
  → task capability profile          (Step 2)
  → R/D/W/C + scope                  (Step 3)
  → candidate model × effort         (Step 4: Claude; Step 4-OC: two OpenCode models, then efforts)
  → benchmark evidence · comparability · equivalence · dominance (Step 5)
  → cross-ecosystem comparison → ✅ RECOMMENDED AI + Evidence line (Step 6)
  → quota guards + data-policy lines (Step 7)
```

## Data honesty

> **Evidence sets the direction and the equivalence band; the capability profile
> decides which evidence applies; efficiency breaks the ties capability leaves
> open. A leaderboard position on its own decides nothing.**

- **Benchmarks are bound to capabilities.** A pure maths prompt gives Terminal-Bench a weight of zero.
- **Comparability is checked first.** Benchmark, version, harness, tool access, scaffold *and* effort must match.
  Traps in the record: Z.ai's launch table (vendor-reported, Terminal-Bench 2.1 88.2 — saturated); AA's Coding Agent
  Index is a harness × model aggregate that *contains* Terminal-Bench 4.0, so it is not a second measurement;
  AA prices differ from Go prices (Muse Spark, DeepSeek peak/off-peak).
- **No interpolation between effort rungs**, and `n/p` (not published) is an answer.
- **A direction needs two independent measurements that agree (BD1);** a single one decides only at `R=3`.
- **The aggregate index never sets a capability direction** — it only licenses the efficiency tie-break.

Raw evidence for the Claude side lives in `../skill/benchmarks.json` / `../skill/benchmark_frontiers.json`
(Codex-era snapshot; the Claude rows are unchanged), and for OpenCode in
`../skill/opencode-benchmarks.md`. Only `SKILL.md` is read when routing.


## How it decides

| Step | What happens |
|---|---|
| **0 · Quality gate** | Four mechanical checks. If any fires → **no model, no badge, one `Clarify:` line.** |
| **1 · Hard gates** | Claude: sub-second/bulk → Haiku 5.5; offensive security → Opus 4.8; biology → Fable 5.1; 1000+ files → Fable 5.1. **OpenCode: offensive security / biology / computer-use → `use Claude` (no models); confidential work removes Muse Spark, Grok 4.7 and GPT 6 Luna; context > 256k removes Qwen3.8 Flash; image input removes GLM-5.3 (premium anyway); bulk/latency → DeepSeek V4.1 Flash.** |
| **2 · Capability profile** | One or two tags (`agentic-code`, `deep-reasoning`, `knowledge-work`, `long-context`, `workflow-automation`, …) — what makes benchmark evidence applicable or not. |
| **3 · Score scope & stakes** | **R**isk, **D**epth, **W**idth, **C**ontext — each 0–3. |
| **4 · Candidate model × effort** | Claude: Haiku 5.5 by Rule H1, else model ← `max(D,C)` + profile; effort ← D (`low/medium/high/xhigh`), a `· ultracode` flag on 3+ phases (never a level of its own), `opusplan`. **OpenCode (4-OC): a pair from the budget tier only (BUD1) — `D ≤ 1` → DeepSeek V4.1 Flash · GLM-5.3-Flash; otherwise a per-capability pair, reordered at `D = 3` / `R = 3`; effort = the model's own variant: `low`/`high`/`max` by `D` where OpenCode offers them, else `default` (MiMo), `xhigh` (Qwen).** |
| **5 · Evidence, equivalence, efficiency** | Comparability → published dispersion only → dominance (Go cap pressure first for OpenCode). |
| **6 · `✅ RECOMMENDED AI`** | Hard gate → MECH1 → applicable capability and its evidence (B1, BD1) read through **SM1: OpenCode unless Claude makes a serious difference**. One badge, one `Evidence:` sentence. |
| **7 · Quota guards** | `R=3` → human-review note. Escalation is a model change. Data-policy and DeepSeek lines are auto-added. |

Two design choices carried over: **risk raises human oversight, not model tier**, and
**when in doubt, round down**.

