# model-effort-router

**Paste a task. Get told which model and effort level to run it on — for Claude and for your OpenCode Go subscription (two models out of the 19 it rates — the Go budget tier, one free Go model and Gemini 4 Argon — in order, each with its own effort) — and which of the two to use.** OpenCode is the default; Claude is recommended where it makes a serious difference. It does *not* run the task; it routes it.

Installed as a Claude Code / claude.ai skill invoked with `/model-secici`.

```
You:    /model-secici  Refactor the payment module across these 40 files to use the new idempotency-key API, update every caller, and make the test suite pass.

model-secici:
  Claude:   Sonnet 5.5 · effort: high
  OpenCode: ✅ RECOMMENDED AI · #1 DeepSeek V4.1 Flash · effort: high · #2 MiMo-V2.6-Pro · effort: default
  Evidence: Mid-difficulty feature work is a tie on the independent DeepSWE (DeepSeek 71.7
            vs Sonnet 5.5 70.5, ±7) at USD 0.13 against Opus 5.5's 1.67 per agent task;
            Claude's lead starts at D=3.
  DeepSeek V4.1 Flash: peak hours cost 2× (04–07 and 09–13 TR time, Mon–Fri); …
```

The badge is **computed, not habitual** — make the task harder and it moves to Claude:

```
You:    /model-secici  Find the race condition that flakes in prod sometimes

model-secici:
  Claude:   ✅ RECOMMENDED AI · Opus 5.5 · effort: xhigh
  OpenCode: #1 MiMo-V2.6-Pro · effort: default · #2 DeepSeek V4.1 Flash · effort: max
  Evidence: D=3 reasoning half has two agreeing AA rows (HLE 61 vs 49, CritPt 32 vs 27);
            the terminal half sets no direction, so the direction decides.
  DeepSeek V4.1 Flash: peak hours cost 2× (04–07 and 09–13 TR time, Mon–Fri); …
  ⚡ Claude /fast available (2.5x faster, 2× price).
```

```
You:    /model-secici  Label these 200 customer reviews as positive/negative

model-secici:
  Claude:   Haiku 5.5 · effort: low
  OpenCode: ✅ RECOMMENDED AI · #1 DeepSeek V4.1 Flash · effort: low · #2 MiMo-V2.6-Flash · effort: default
  Evidence: Labelling is D=0 bulk work, so OpenCode runs it: the Flash tier buys hundreds of
            such batches a month on USD 60 caps and keeps Claude's quota for harder work.
  DeepSeek V4.1 Flash: peak hours cost 2× (04–07 and 09–13 TR time, Mon–Fri); …
```

> The skill body (`skill/SKILL.md`, plus `opencode-benchmarks.md` and `reference.md`) and its output are English. It routes prompts in any language. 🇹🇷 A longer
> Turkish walkthrough is in **[README.tr.md](README.tr.md)** (its iteration-21/22/23 sections are at the top; the rest is the Codex-era history).

---

## What changed in iteration-24 (20 Oct 2026): free models and Gemini 4 Argon

Two requests: try the *free* OpenCode models where they fit, and use the Gemini entitlement that comes with a Google membership where Gemini stands out. The pool is now **19 rated models**
(`skill/opencode-benchmarks.md` §13 has every number and source).

- **Free lane (Rule FR1).** Of the 14 free models on Zen, only **MiniMax M3.1 Flash Free** has a v4.3.2 score *and* a data policy fit for confidential work (zero retention, unlimited on Go):
  AA index 43, and on the Flash tier it leads AutomationBench-AA (73), HLE (48), CritPt (22) and SciCode (53). It now takes `#2` on `deep-reasoning` / `science` and `#1` on `doc-data-understanding`, and is gated out of
  factual recall (hallucination rate 92.8%, the same failure as DeepSeek). The free twins of GLM-5.3-Flash and DeepSeek V4.1 Flash are the first spill-over when a paid window runs out — never a pick.
  Nemotron 3 Ultra scores 23 (budget models 38–46) and logs your prompts; Big Pickle, LL Alpha, Exo, Beam, LongCat 2.5 Preview and Jev have no independent score or train on prompts, so they are never selected.
  Free is "limited time": the rows that used the free model record what they revert to.
- **Gemini slot (Rule GM1).** Gemini 4 Argon is the first Google model that is worth a slot: AA index 53, the **lowest hallucination rate (15%)** and a 42 Omniscience index of anything rated here, the highest
  AutomationBench-AA (77.5), HLE 57, ARC-AGI-2 91.3. It also takes 48 s to a first token, costs USD 1.99 per AA task (USD 3.98 from 1 Dec) and trails Claude on Terminal-Bench and finished deliverables. So it is
  **metered, not default**: first on the OpenCode line only at `D = 3` or `R = 3` for `agentic-code`, `terminal-tool`, `deep-reasoning`, `research-synthesis` and `workflow-automation`, and `#2` after an OpenCode shortfall.
  Effects: factual-reliability work at `R = 3` now goes to OpenCode (Argon beats Sonnet 5.5 on both Omniscience measures); hard coding and reasoning keep the Claude badge.
- **The membership.** Google AI Pro gives no API key — but it carries **USD 10/month of Google Cloud credits** for the Gemini API (activate them under developers.google.com/program/my-benefits; paid-tier keys are not
  trained on). Logging in to OpenCode with the Google account itself is the route Google's terms prohibit (suspension reports exist), so the router tells you to use an API key. A 503 is Google-side capacity (retry, then Gemini 3.8 Flash);
  a `429 "limit: 0"` on Argon means a free-tier key. Details: `opencode-benchmarks.md` §13.4.
- **Also:** DeepSeek V4.1 Flash's Go cap rose to USD 80; Go's *Contributor* route for Argon (inside the USD 10 plan) trains on prompts, so it is offered only for work you call non-confidential.
- **Checks:** `grade_routing.py --selftest` 34/34 (30 → 34 evals: d1, g1, j1, t1, v1, z1, p1, n1, r1 moved; `w1`–`w4` new); policy sync (42 blocks), pool check (mutation-tested), examples — all green.
  **Cold-agent run (6 fresh Sonnet agents, `evals/routing/results/iteration-24/`): 33/33 routed evals pass** — two corrections first: `w2` exposed a real ambiguity (NC1 said Muse Spark "may" take `#2` on deep-reasoning/science; now it takes `#2` on `research-synthesis` only) and `r1` was an ambiguous prompt (sharpened, rule unchanged). `i1` (exploit PoC) was declined by its agent as a routing-only task and not re-run; that gate is untouched. Not done: the trigger eval. `SKILL.md` 54.7 → 60.0 KB after trimming.

## What changed in iteration-23 (14 Oct 2026): budget-first OpenCode, OpenCode by default

Two requests: some Go models eat their quota in a handful of tasks, and Claude should be the
exception, not the default.

- **Budget-first pool (Rule BUD1).** Each Go model has its own dollar cap, so what matters is how
  many *real* tasks one month of that cap buys (cap ÷ Arena p50 cost per agent task):

  | Tier | Models | Tasks per month of its cap |
  |---|---|---|
  | **Budget** (default pairs) | MiMo-V2.6-Flash 1500 · GLM-5.3-Flash 600 · DeepSeek V4.1 Flash 462 · Qwen3.8 Flash 200 · MiMo-V2.6-Pro 150 | 150–1500 |
  | Non-confidential only | GPT 6 Luna 214 · Muse Spark 1.3 140 (trains on prompts) | — |
  | **Premium** (escalation only) | Qwen3.8 Max 33 · GLM-5.3 23 · Kimi K3 21 · Grok 4.7 10 | 10–33 |

  AA's own cost per index task gives the same split (premium 6–36 % of the cap *per task*, budget
  0.1–1.2 %). The four premium models are **never** `#1`/`#2` of a routed pair; they appear only as
  `#2` through Rule A1-OC, after you say an earlier OpenCode run fell short. GLM-5.3 and Kimi K3
  left the default pairs; the pairs are rebuilt from the independent-evidence consensus **inside the
  budget tier** (`scripts/derive_opencode_rows.py`). Non-confidential no longer re-admits Grok 4.7.
- **OpenCode by default (Rule SM1).** Errand work and everything OpenCode can do well goes to OpenCode.
  The badge goes to Claude only when it makes a serious difference: a hard gate or a context limit,
  a product mechanism (`ultracode`, `opusplan`), `D = 3` coding or deep reasoning (AA Terminal-Bench 4.0
  64 / 60 against 35 for the best budget model, FrontierSWE v2 62 against 18, HLE 61 against 49),
  finished deliverables from `D = 2` (GDPval-AA, Briefcase and AnalystAgent agree), or `R = 3` with a Claude
  lean. **Every `D ≤ 1` task is OpenCode — Haiku 5.5 included** — and so is `D = 2` coding: the independent
  DeepSWE v1.1 (±7) ties DeepSeek V4.1 Flash 71.7 with Opus 5.5 72.3 and Sonnet 5.5 70.5, at USD 0.13 per agent
  task against Opus 5.5's 1.67.
- **What this trades away, stated plainly.** At `D = 2` the router now sends coding to OpenCode even though
  Claude still leads AA Terminal-Bench 4.0 there; the split rests on DeepSWE (mid-difficulty tasks) being a
  tie while the Claude lead lives on the hardest anchors. If you would rather pay Claude for `D = 2` coding, it
  is one row of the badge table in `skill/SKILL.md` (and its mirror in `evals/policy/routing_policy.json`).
- **Effort is unchanged.** On the Flash tier `max` at `D = 3` costs about USD 0.25–0.27 per AA task (0.4 % of a
  USD 60 cap), so it stays cheap there; the expensive `max` runs were GLM-5.3 and Kimi K3 (USD 2 per task on a
  USD 15 cap).
- 30 evals (new: `z1`, an `R = 3` regulatory read); the grader now also fails any OpenCode line that names a
  premium model unless the eval sets `allow_premium` (only the shortfall case `p1` does).

---

## What changed in iteration-22 (8 Oct 2026): Claude Haiku 5.5

Haiku 5.5 shipped on 7 Oct at **USD 0.10 / USD 0.50 per MTok** (up to 100k tokens; USD 0.50 / 2.50 above),
1M context and — for the first time on a Haiku — **effort levels**. The router now treats it as the
**cost pick** and says why:

- **Haiku 5.5 replaces Haiku 4.5** on the Claude line (Rule H1). It takes `D=0` work and, new,
  `D=1` *reading/transform* work — summaries, labels, rewrites, translations, answers from text you supply —
  at `low` / `medium`. AA's same-page numbers justify the boundary: reading comprehension is a tie with
  Sonnet 5.5 (AA-LCR 77 vs 78), while the gap is large on exactly the agentic and knowledge-work anchors
  (Terminal-Bench 22 vs 44, AutomationBench 34 vs 59, GDPval-AA 1420 vs 1551, Omniscience 6 vs 21). Those
  stay on Sonnet 5.5, and so does a single-fact lookup (factual recall is `research-synthesis`).
- **It is the cheapest Claude option by a wide margin:** AA cost per task USD 0.08 at High and 0.21 at Max,
  against Sonnet 5.5 USD 0.88 at High — about 11× cheaper for −9 index points. `xhigh`/`max` are never
  emitted (Max burns 162k tokens a task and still sits under Sonnet 5.5 High, Rule E8).
- **The badge moved with it — superseded in iteration-23.** In iteration-22 the `D ≤ 1` price tie-break went
  to **Claude** when the pick was Haiku 5.5. Iteration-23's Rule SM1 sends every `D ≤ 1` task to OpenCode. What
  stays: `latency-volume` means only an explicit **first-token** requirement — bulk work nobody waits on is a
  price question.
- **A Haiku shortfall escalates to Sonnet 5.5** (Rule H2), never to a higher Haiku rung.
- **OpenCode:** Claude Haiku 5.5 is on Go too (cap USD 15, 30-day retention). It is rated as the 16th model and
  is **dominated** there (Rule E9): mid-pack on every independent anchor, and beaten on cap pressure by
  MiMo-V2.6-Flash / GLM-5.3-Flash at equal index and cost. Its place is the Claude line, where no dollar cap applies.
- **Also corrected:** Sonnet 5.5 cache reads halved on 7 Oct, so AA's Sonnet 5.5 Max cost fell to USD 5.46 (from
  7.60); Rule E1 still holds (1.6× instead of 2.2×). Agent Arena costs were refreshed. `/model haiku` resolves to
  Haiku 5.5 on Claude Code v2.1.293+.
- **Honest limits.** AA measured only Haiku 5.5's High and Max rungs — the `low`/`medium` rungs the router emits
  are unmeasured, so cost claims use High as an upper bound. A fresh-agent run of the 29 evals passes (29/29 after
  two corrections, see `evals/README.md`); the D=1 boundary of Rule H1 rests on one reading-comprehension tie (AA-LCR). Evidence: [`skill/opencode-benchmarks.md`](skill/opencode-benchmarks.md) §11 and
  [`skill/reference.md`](skill/reference.md) §19.

---

## What changed in iteration-21 (6 Oct 2026): the Codex arm is gone, OpenCode Go is in

> Pairs and badge rows below are the iteration-21/22 versions; iteration-23 replaced the pairs (premium models
> out, see above) and the badge table.

The second arm used to be Codex/ChatGPT (Luna / Sol / Sol Ultra / Astra). The Codex
subscription ended, so the arm was **re-derived from scratch for OpenCode Go (USD 10/month)**.
Claude's arm is untouched. The last Codex-era policy is the git tag `iteration-20-codex`
and `archive/iteration-20-codex/`.

- **Two models, in order, each with its own effort.** The router first *selects* the two
  best of the pool for the task (`#1`, `#2`), then picks each one's effort.
- **The 15 main models** (+ Haiku 5.5 as the 16th, see above) — chosen from the 30 on `opencode.ai/docs/go` (the other 15 are
  superseded, preview, free, vision-experimental or have no independent measurement):

  | Role | Models |
  |---|---|
  | Coding (consensus of 5 independent anchors) | **DeepSeek V4.1 Flash** (DeepSWE 71.7 ±6.3, Agent Arena 4.02 at USD 0.12) · **GLM-5.3** (leads the hardest anchors: TB 4.0, FrontierSWE v2) |
  | Reasoning / science | **MiMo-V2.6-Pro** (HLE 49, CritPt 27 — thin coding evidence) · **Kimi K3** |
  | Factual research | **GLM-5.3** (lowest hallucination) — **never DeepSeek (96.5% hallucination rate)** |
  | Long context / documents / images | **Kimi K3** (AA-LCR 89, MMMU-Pro 81) · Qwen3.8 Flash |
  | Workflow / latency / bulk | **DeepSeek V4.1 Flash** (AutomationBench-AA 69, 222 tok/s) · GLM-5.3-Flash · MiMo-V2.6-Flash |
  | Knowledge-work | MiMo-V2.6-Pro · Qwen3.8 Flash · **Grok 4.7** (non-confidential only) |
  | Escalation | Kimi K3 (coding) · Qwen3.8 Max (knowledge-work) |
  | Opt-in, non-confidential | Muse Spark 1.3 Contributor (AA 48, but **trains on your prompts**) · GPT 6 Luna (30-day retention) |
  | Rated, **dominated**, never emitted | DeepSeek V4 Pro · MiniMax M3 · Kimi K2.7 Code · Qwen3.7 Plus · Claude Haiku 5.5 |

- **Caps are per model.** Go gives each model its own monthly dollar cap (USD 15 for the
  expensive ones, 30 or 60 for the cheap ones); the 5-hour window is 20% of it and the weekly
  50%. So the router reserves the USD 15 models for `D ≥ 2`, sends `D ≤ 1` to the USD 60
  Flash tier, and names the next model of a tier chain when a window runs out.
- **Effort is the variant OpenCode actually offers for that model.** Researched in models.dev:
  GLM-5.3, GLM-5.3-Flash and DeepSeek V4.1 Flash expose `low`/`high`/`max`; **MiMo-V2.6 exposes
  none** (thinking is always on, so the router writes `default`); Kimi K3 only `max`; Grok 4.7
  `low`…`xhigh`; Qwen3.8 `low`/`medium`/`xhigh`. `medium` and `xhigh` are *rejected* on the
  `low`/`high`/`max` models, so they are never written. On those three models `D ≤ 1 → low`,
  **`D = 2 → high`, `D = 3 → max`**: DeepSeek's own paper finds effort 60–80 recovers most of
  `max`'s accuracy at under half the tokens (and `max` adds 1.6–1.8× agent tokens for marginal
  gains), and Z.ai's Code Bench has GLM-5.3 `high` 31.4% @ ~50k tokens vs `max` 34.5% @ ~75k —
  vendor-reported own-model curves, used to pick a rung, never a cross-ecosystem direction. AA
  measured only `low`/`max` (GLM-5.3 34 → 45, Kimi K3 30 → 44) and DeepSeek V4.1 Flash
  non-reasoning (25 vs 39 at `max`). `GLM-5.3 · low` is dominated by GLM-5.3-Flash (42 at a
  quarter of the cost), so the Pro tier is never emitted low. No interpolation.
- **Pair order follows depth (Rule PO1).** At `D ≤ 2` and `R ≤ 2` `#1` is the most cap-efficient model inside the leading consensus band; at `D = 3` or `R = 3` the leader on the hardest anchors goes first (GLM-5.3 for coding). It orders the pair only; the badge still follows BD1.
- **Token cost kept low.** `SKILL.md` was cut from 60 KB to 44 KB (rosters, Step 5/6 prose and examples compressed; every Claude carve-out and rule block kept) and `Evidence:` is capped at one sentence of ≤ 30 words. Details live in `skill/opencode-benchmarks.md`, which is never loaded to route.
- **Confidential by default.** Grok 4.7 and GPT 6 Luna keep prompts 30 days and Muse Spark
  Contributor trains on them, so all three are out of the pool unless you say the work is
  non-confidential (Rule NC1). DeepSeek's zero-retention agreement is valid through
  31 Oct 2026 and renewed monthly — the router prints that caveat.
- **Multi-source, not one benchmark.** A first pass used only Artificial Analysis and over-ranked
  MiMo-V2.6-Pro. The router now rests on every independent source that publishes the pool —
  AA (13 components), DeepSWE v1.1 (Mercor/Datacurve, with error margins), Arena (Agent / Code /
  Text), Vals, FrontierSWE v2, ARC-AGI, Gray Swan — compiled into `skill/opencode-evidence.json`;
  `scripts/derive_opencode_rows.py` reproduces each capability's consensus and
  `check_opencode_pool.py` fails if a routing row leaves the top 4. Findings: **DeepSeek V4.1
  Flash is the best coding consensus** and sits on a USD 60 cap (and is #3 by tokens on OpenCode),
  but hallucinates (96.5%); MiMo-V2.6-Pro has almost no independent coding evidence; Kimi K3 is a
  *contested* coder (TB 4.0 13, yet Agent Arena #1 open and Vals TB 2.1 81) with weak
  prompt-injection resistance; GLM-5.3 leads the hardest coding anchors. Details and quirks:
  **[`skill/opencode-benchmarks.md`](skill/opencode-benchmarks.md) §10**.

### What the badge says now (iteration-23)

Claude holds the badge on: every gate OpenCode declines (offensive security, biology, computer-use);
the product mechanisms OpenCode lacks (`ultracode`, `opusplan`); **`D = 3`** `agentic-code` /
`terminal-tool` / `deep-reasoning` (three independent rows agree); **`knowledge-work` from `D = 2`**; and
`R = 3` work with a Claude lean (marked low-confidence for science, research and documents). OpenCode holds it
for every `D ≤ 1` task, `D = 2` coding and reasoning, latency, and the *contested* rows — workflow-automation
(open models lead ITBench) and long-context (AA-LCR vs MLCR-AA disagree) — the thin ones marked low-confidence.

---

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

Raw evidence for the Claude side lives in `skill/benchmarks.json` / `skill/benchmark_frontiers.json`
(Codex-era snapshot; the Claude rows are unchanged), and for OpenCode in
`skill/opencode-benchmarks.md`. Only `SKILL.md` is read when routing.

---

## Install

It's a [Claude skill](https://docs.claude.com/en/docs/claude-code/skills) — a
`model-secici/` folder. Only `SKILL.md` is read when routing; the rest are there
for auditing a rule.

```bash
git clone https://github.com/enzoo808/model-effort-router.git
cd model-effort-router
```

### Claude Code

**macOS / Linux:** `./install.sh` · **Windows (PowerShell):** `.\install.ps1`

**Or by hand:**
```bash
mkdir -p ~/.claude/skills/model-secici
cp skill/*.md skill/*.json ~/.claude/skills/model-secici/
```

Start a new Claude Code session, then `/model-secici  <your task>`. It also triggers on
"which model should I use for this?".

### claude.ai / Claude Desktop (native custom skill)

Requires a Pro / Max / Team / Enterprise plan with **code execution** enabled. Download
**[`dist/model-secici.zip`](dist/model-secici.zip)** (rebuild with `.\build-claude-ai-zip.ps1`),
then **claude.ai → Settings → Features → Custom Skills → Upload**. No code execution? Use the
plain-text fallback in [`claude-ai/instructions.tr.md`](claude-ai/instructions.tr.md) (Turkish).

### OpenCode Go

There is no skill mechanism on the OpenCode side — the router just produces the `OpenCode:`
line (two models, each with an effort) for you to act on. In OpenCode, pick the model by its
id `opencode-go/<model-id>` and cycle the effort with `variant_cycle` (MiMo-V2.6 has no variant — nothing to cycle).

---

## How it decides

| Step | What happens |
|---|---|
| **0 · Quality gate** | Four mechanical checks. If any fires → **no model, no badge, one `Clarify:` line.** |
| **1 · Hard gates** | Claude: sub-second/bulk → Haiku 5.5; offensive security → Opus 4.8; biology → Fable 5.1; 1000+ files → Fable 5.1. **OpenCode: offensive security / biology / computer-use → `use Claude` (no models); confidential work removes Muse Spark, Grok 4.7 and GPT 6 Luna; context > 256k removes Qwen3.8 Flash; image input removes GLM-5.3 (premium anyway); bulk/latency → DeepSeek V4.1 Flash.** |
| **2 · Capability profile** | One or two tags (`agentic-code`, `deep-reasoning`, `knowledge-work`, `long-context`, `workflow-automation`, …) — what makes benchmark evidence applicable or not. |
| **3 · Score scope & stakes** | **R**isk, **D**epth, **W**idth, **C**ontext — each 0–3. |
| **4 · Candidate model × effort** | Claude: Haiku 5.5 by Rule H1, else model ← `max(D,C)` + profile; effort ← D (`low/medium/high/xhigh`), `ultracode` on 3+ phases, `opusplan`. **OpenCode (4-OC): a pair from the budget tier only (BUD1) — `D ≤ 1` → DeepSeek V4.1 Flash · GLM-5.3-Flash; otherwise a per-capability pair, reordered at `D = 3` / `R = 3`; effort = the model's own variant: `low`/`high`/`max` by `D` where OpenCode offers them, else `default` (MiMo), `xhigh` (Qwen).** |
| **5 · Evidence, equivalence, efficiency** | Comparability → published dispersion only → dominance (Go cap pressure first for OpenCode). |
| **6 · `✅ RECOMMENDED AI`** | Hard gate → MECH1 → applicable capability and its evidence (B1, BD1) read through **SM1: OpenCode unless Claude makes a serious difference**. One badge, one `Evidence:` sentence. |
| **7 · Quota guards** | `R=3` → human-review note. Escalation is a model change. Data-policy and DeepSeek lines are auto-added. |

Two design choices carried over: **risk raises human oversight, not model tier**, and
**when in doubt, round down**.

---

## Examples

| Task | Claude | OpenCode `#1` · `#2` | Recommended |
|---|---|---|---|
| Label 200 reviews positive/negative | `Haiku 5.5 · low` | DeepSeek V4.1 Flash `low` · MiMo-V2.6-Flash `default` | **OpenCode** — `D=0` bulk work; the Flash tier on USD 60 caps keeps Claude's quota |
| Summarise a 2-page transcript into five bullets | `Haiku 5.5 · medium` | DeepSeek V4.1 Flash `low` · GLM-5.3-Flash `low` | **OpenCode** — `D=1` reading work, AA-LCR 77 vs 78 |
| Draft the weekly steering-committee status memo | `Sonnet 5.5 · medium` | DeepSeek V4.1 Flash `low` · GLM-5.3-Flash `low` | **OpenCode** — `D=1`; Haiku 5.5 is out of knowledge-work |
| Live-chat reply, first words within about a second | `Haiku 5.5 · low` | DeepSeek V4.1 Flash `low` · MiMo-V2.6-Flash `default` | **OpenCode** — first-token bound; DeepSeek has a measured 1.1 s |
| Which year did the EU AI Act's GPAI obligations start? | `Sonnet 5.5 · low` | GLM-5.3-Flash `low` · MiMo-V2.6-Flash `default` | **OpenCode** — factual recall excludes Haiku and DeepSeek |
| Bump `MAX_RETRIES` 3→5 in the prod config | `Sonnet 5.5 · low` + review note | DeepSeek V4.1 Flash `low` · GLM-5.3-Flash `low` | **OpenCode** — `D=0`, both clear the bar |
| Refactor the payment module across 40 files | `Sonnet 5.5 · high` | DeepSeek V4.1 Flash `high` · MiMo-V2.6-Pro `default` | **OpenCode** — `D=2`; DeepSWE ties, USD 0.13 vs 1.67 per task |
| Stand up staging from scratch (Terraform, 12 services, seed, smoke) | `Sonnet 5.5 · ultracode` | DeepSeek V4.1 Flash `high` · MiMo-V2.6-Pro `default` | **Claude** — three phases; `ultracode` has no OpenCode equivalent (MECH1) |
| Find the race condition that flakes in prod | `Opus 5.5 · xhigh` | MiMo-V2.6-Pro `default` · DeepSeek V4.1 Flash `max` | **Claude** — `D=3`, two agreeing AA rows on the reasoning half |
| Design and implement the irreversible transaction boundary | `Opus 5.5 · max` + review note | MiMo-V2.6-Pro `default` · DeepSeek V4.1 Flash `max` | **Claude** — `D=3`, `R=3` |
| Redesign auth for 200 services from scratch | `opusplan · plan: max · execute: medium` | MiMo-V2.6-Pro `default` · GLM-5.3-Flash `max` | **Claude** — `opusplan` mechanism |
| Wire a Jira → Slack → on-call n8n flow | `Sonnet 5.5 · high` | DeepSeek V4.1 Flash `high` · GLM-5.3-Flash `high` | **OpenCode**, low-confidence — AutomationBench is a tie and ITBench favours the open models |
| Summarise 400 pages of filings into one memo | `Sonnet 5.5 · high` | MiMo-V2.6-Pro `default` · DeepSeek V4.1 Flash `high` | **Claude** — knowledge-work from `D=2` |
| Read 30 scanned receipts into a reconciliation table | `Sonnet 5.5 · high` | Qwen3.8 Flash `xhigh` · MiMo-V2.6-Pro `default` | **OpenCode**, low-confidence — both take images |
| Non-confidential conference pricing deck | `Sonnet 5.5 · high` | MiMo-V2.6-Pro `default` · Qwen3.8 Flash `xhigh` | **Claude** — knowledge-work; Grok 4.7 stays premium |
| Read 3 regulator pages before labels go to print tonight | `Sonnet 5.5 · high` + review note | MiMo-V2.6-Pro `default` · GLM-5.3-Flash `high` | **Claude**, low-confidence — `R=3` and a single Omniscience lean |
| An earlier OpenCode attempt at a 30-file migration fell short | `Sonnet 5.5 · high` | DeepSeek V4.1 Flash `high` · **GLM-5.3** `max` | **Claude** — Rule A1-OC adds the premium `#2` and hands the badge over |
| Exploit PoC for a CVE | `Opus 4.8 · xhigh` | `use Claude` | **Claude** — the other arm declines |
| Call somatic variants from tumour/normal exomes | `Fable 5.1 · high` | `unverified — use Claude` | **Claude** — availability gate |
| "Fix this code" | *(no model, no badge — asks: which code? broken how? done = ?)* | | |

---

## Validation

`evals/routing/evals.json` is a deterministic regression set (30 prompts) graded by
`evals/routing/grade_routing.py` (pure regex, no LLM): Claude model + effort, **both OpenCode
picks (model, effort, order)**, which side carries the badge, a non-trivial `Evidence:` line
(whose `low-confidence` flag must match the row's dagger), plus required / forbidden text
for the auto-added lines and the confidentiality default.

```bash
python evals/routing/grade_routing.py --selftest --results-dir /tmp/x   # goldens vs grader
python scripts/check_policy_sync.py        # SKILL.md rule blocks == evals/policy/routing_policy.json
python scripts/check_opencode_pool.py      # pool, Step 4-OC rows, badge table, examples, per-model variants, consensus top-4
python scripts/derive_opencode_rows.py     # print the independent-evidence consensus per capability
python scripts/check_examples.py           # every worked example agrees with its golden
```

> **Status (14 Oct 2026).** Iteration-23: the grader self-test (30/30), policy sync, pool/badge-table check and example check are green; the goldens are rule-derived and **not yet confirmed by a cold-agent run**. The last cold-agent run (iteration-22, 29/29, `evals/README.md`) predates the budget-first pool and the OpenCode-default badge. The **trigger eval is a proxy only** (nested `claude -p` fails to
> authenticate here); run `evals/trigger/run_trigger.py` from a logged-in terminal for the real result.

Run history and the reasoning behind every rule change is in
[`evals/README.md`](evals/README.md).

## Contributing

Corrections to model specs, prices, caps, retention terms, effort defaults or **benchmark
records** are very welcome — cite the primary source and add the harness/effort/date next to
the number. Rule changes must keep the checks above green. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).
