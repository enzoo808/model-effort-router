# Changelog

Routing-policy iterations 21 to 25 (the OpenCode Go era), newest first. Earlier iterations, including the Codex arm, are in [`evals/README.md`](evals/README.md), [`evals/history.tr.md`](evals/history.tr.md) and [`docs/README.legacy.tr.md`](docs/README.legacy.tr.md). The router version is the `routing-policy-version` comment in [`skill/SKILL.md`](skill/SKILL.md); the reasoning behind each rule change is in [`evals/README.md`](evals/README.md).

---

## iteration-25 (3 Nov 2026): `ultracode` is a toggle, not an effort level

Claude Code v2.1.284 turned Ultracode into its own switch: it **no longer forces `xhigh`** and stays on at any effort level
(`code.claude.com/docs/en/model-config`, `.../workflows`; details and sources in `skill/reference.md` §22). Three things follow, and the router now reflects them:

- **The output is a flag, not a level.** `Claude: Sonnet 5.5 · effort: high · ultracode`. The old `effort: ultracode` told you to run `/effort ultracode`, which today leaves your session at its own default (`medium` on Sonnet 5.5) instead of `xhigh`.
- **The level follows difficulty** (Rule UC1): `Effort ← D`, floor `high` (a 30-minute unattended run is where Sonnet 5.5 at `low`/`medium` stops to check in), ceiling `xhigh`. `max` and `ultracode` are still never paired.
- **It is session-wide and quota-heavy.** Every substantive task becomes a workflow, so limits drain faster. An auto-added `Ultracode:` line (Step 7 rule 12) says to start the prompt with `ultracode:` to run *only this task* as a workflow, instead of leaving the toggle on.

Unchanged: the trigger (over 30 minutes and `O = high` or `W = 3 ∧ D ≥ 2`, not one indivisible chain), MECH1 (OpenCode has no equivalent), and no `ultracode` on Haiku 5.5 (now a routing choice — Haiku 5.5 does list `xhigh`). Checked: policy sync, example check, benchmark validator, grader self-test (36/36), and a **fresh-agent run of all 36 prompts: 34/36** (`results/iteration-25/`). `c1` (the old `ultracode` row) missed once on the badge and passed 3/3 on re-run; `r1` (scanned receipts, unrelated to `ultracode`) splits 2/4 across runs and is left open. Two prompts were added: `c2` (D=3 × 180 services → `xhigh · ultracode`) and `c3` (five-phase migration → `high · ultracode`).

---

## iteration-24 (20 Oct 2026): free models and Gemini 4 Argon

Two requests: try the *free* OpenCode models where they fit, and use Gemini where it stands out (first assumed reachable with a Google key; on 26 Oct the user clarified that only Go's Gemini route works). The pool is now **19 rated models**
(`skill/opencode-benchmarks.md` §13 has every number and source).

- **Free lane (Rule FR1).** Of the 14 free models on Zen, only **MiniMax M3.1 Flash Free** has a v4.3.2 score *and* a data policy fit for confidential work (zero retention, unlimited on Go):
  AA index 43, and on the Flash tier it leads AutomationBench-AA (73), HLE (48), CritPt (22) and SciCode (53). It now takes `#2` on `deep-reasoning` / `science` and `#1` on `doc-data-understanding`, and is gated out of
  factual recall (hallucination rate 92.8%, the same failure as DeepSeek). The free twins of GLM-5.3-Flash and DeepSeek V4.1 Flash are the first spill-over when a paid window runs out — never a pick.
  Nemotron 3 Ultra scores 23 (budget models 38–46) and logs your prompts; Big Pickle, LL Alpha, Exo, Beam, LongCat 2.5 Preview and Jev have no independent score or train on prompts, so they are never selected.
  Free is "limited time": the rows that used the free model record what they revert to.
- **Gemini slot (Rule GM1) — Go's Contributor route only (26 Oct).** The Google membership cannot be used inside OpenCode, so Gemini 4 Argon is reachable only as
  `opencode-go/gemini-4-argon-contributor` (USD 60 cap during a 2× promo, 30 after; **Google trains on prompts**). That makes it **non-confidential work only** (NC1). Argon is the first Google model worth a slot:
  AA index 53, the **lowest hallucination rate (15%)** and a 42 Omniscience index of anything rated here, the highest AutomationBench-AA (77.5), HLE 57, ARC-AGI-2 91.3 — but 48 s to a first token, about 3% of its cap
  per heavy task, and behind Claude on Terminal-Bench and finished deliverables. So, under NC1 only, it is `#1` at `D = 3` or `R = 3` on `agentic-code`, `terminal-tool`, `deep-reasoning`, `research-synthesis` and
  `workflow-automation` (and `#2` after an OpenCode shortfall). Confidential work, the default, never sees it, and `research-synthesis` at `R = 3` stays with Claude unless you say the work is non-confidential.
  Details, including the Google-membership facts (USD 10/month Cloud credits are API-only, third-party logins are against Google's terms): `opencode-benchmarks.md` §13.4.
- **Effort (21 Oct):** `D ≥ 2 → max` (was `D = 2 → high`) on DeepSeek V4.1 Flash, GLM-5.3-Flash and MiniMax M3.1 Flash Free — AA measured DeepSeek only at `max`, `high` had only a vendor curve, and `max` costs about 0.3% of the cap per task.
- **Also:** DeepSeek V4.1 Flash's Go cap rose to USD 80; Go's *Contributor* route for Argon (inside the USD 10 plan) trains on prompts, so it is offered only for work you call non-confidential.
- **Checks:** `grade_routing.py --selftest` 34/34 (30 → 34 evals: d1, g1, j1, t1, v1, z1, p1, n1, r1 moved; `w1`–`w4` new); policy sync (42 blocks), pool check (mutation-tested), examples — all green.
  **26 Oct Go-only revision, re-run by fresh agents: the 10 affected evals pass after two fixes (`p1`: A1-OC now says any Claude cell in the badge table moves the badge; `g1`: prompt sharpened to one indivisible decision, golden `#2` corrected).** Earlier cold run (6 fresh Sonnet agents, `evals/routing/results/iteration-24/`): 33/33 routed evals pass** — two corrections first: `w2` exposed a real ambiguity (NC1 said Muse Spark "may" take `#2` on deep-reasoning/science; now it takes `#2` on `research-synthesis` only) and `r1` was an ambiguous prompt (sharpened, rule unchanged). `i1` (exploit PoC) was declined by its agent as a routing-only task and not re-run; that gate is untouched. Not done: the trigger eval. `SKILL.md` 54.7 → 60.0 KB after trimming.

## iteration-23 (14 Oct 2026): budget-first OpenCode, OpenCode by default

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

## iteration-22 (8 Oct 2026): Claude Haiku 5.5

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

## iteration-21 (6 Oct 2026): the Codex arm is gone, OpenCode Go is in

> Pairs and badge rows below are the iteration-21/22 versions; iteration-23 replaced the pairs (premium models
> out, see above) and the badge table.

The second arm used to be Codex/ChatGPT (Luna / Sol / Sol Ultra / Astra). The Codex
subscription ended, so the arm was **re-derived from scratch for OpenCode Go (USD 10/month)**.
Claude's arm is untouched. The last Codex-era policy is the git tag `iteration-20-codex`; the frozen Codex-era files
under `archive/` were later removed from the tree and last exist at commit `7c24c81`.

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

The Codex-era policy (iteration-20 and earlier) is the git tag `iteration-20-codex`; the frozen files that used to sit under `archive/` last exist at commit `7c24c81`.
