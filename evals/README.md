# model-secici eval set

> **iteration-28 (11 Nov 2026) — Go serves DeepSeek V4.1 Flash 1017; DeepSeek evidence re-based.** Go's catalogue names the served model "DeepSeek V4.1 Flash 1017" and models.dev records that Go moved to that build on 2026-10-20, so every DeepSeek figure is now a 1017 same-revision figure (AA v5 33, AA TB 4.0 34, Vals TB 4.0 31.8, Arena Agent 2.07 ±0.52, GDPval-AA 1746, Briefcase 1570); older figures are labelled previous revision / revision unspecified and back no row or badge cell. `derive_opencode_rows.py` moved six Step 4-OC rows: `agentic-code` / `terminal-tool` (MiMo-V2.6-Pro first, DeepSeek second), `deep-reasoning` and `science` (`#2` DeepSeek instead of GLM-5.3-Flash), `knowledge-work` (DeepSeek first, disjoint 95% intervals on GDPval-AA and Briefcase), `workflow-automation` (GLM-5.3-Flash first), `long-context` (`R ≤ 2` GLM-5.3-Flash · MiMo-V2.6-Pro, `R = 3` reversed); no badge cell changed side. **Moved goldens (10):** `b1`, `b2`, `c1` (agentic-code order), `e1` (two-tag pick: `#1` DeepSeek, `#2` GLM-5.3-Flash), `f1`, `u1` (knowledge-work: DeepSeek · MiMo-V2.6-Pro, DeepSeek line added), `m1` (workflow: GLM-5.3-Flash `max` · DeepSeek `high`), `n1` (science `#2` DeepSeek `high`, DeepSeek line added), `p1` (A1-OC: `#1` MiMo-V2.6-Pro, `#2` Argon, DeepSeek line dropped), `w1` (GM1: Argon `#1`, GLM-5.3-Flash `max` `#2`, DeepSeek line dropped); a1–a5, h1, o1, q1, x1, y1 only had figure wording re-labelled. Factual-recall gate kept, rationale rewritten (Omniscience v1.1: 1017 64.1% / 61.2%, MiMo-V2.6-Pro 60.2%, GLM-5.3-Flash 38.3%); E7's D=2 `high` rule unchanged. Arena tasks/month and net improvement refreshed to one snapshot (10 Nov); DeepSWE refreshed from the benchlm mirror at low confidence. **Checks:** `--selftest` 39/39, `check_policy_sync`, `check_opencode_pool`, `check_examples`, `check_readme_facts` green. **Cold-agent run (`results/iteration-28/`, one fresh sonnet agent per prompt reading only a copy of `skill/SKILL.md`, 33 prompts — every eval the change can move; `i1` skipped as asked, and `k1`, `k2`, `l1`, `s0a`, `s0b` not run because they carry no OpenCode pair and no text the change touched): 33/33 graded pass, 0 failures, so there were no prompt-ambiguity, golden-error or rule-gap cases to classify and no prompt was sharpened.** The grader checks models, efforts, order, badge side, dagger, notes and forbidden strings; it does not compare the free-form Evidence wording, which was not hand-graded. One run per prompt (no repeats), a single model tier. Not run: `i1`, the trigger eval.

> **iteration-27 Stage 2+3 (10 Nov 2026) — approved findings applied; full cold run.** *Applied (user-approved):* **D1** Rule BUD1 states tier membership **by name** (premium five: GLM-5.3, Kimi K3, Kimi K3.1 Pro, Grok 4.7, Qwen3.8 Max; budget: MiMo-V2.6-Pro, GLM-5.3-Flash, MiMo-V2.6-Flash, DeepSeek V4.1 Flash) — the 140/35 thresholds are retired from the rule (`skill_md_must_not_appear` guards them) and `check_opencode_pool.py` checks membership plus the sanity bound that the premium five stay at or below 35 tasks/month (they buy 5-18). The `tasks/mo` column is one single-date Arena snapshot (8 Nov 2026, page header "Nov 8, 2026 - 2,750,973 sessions - 57 models", read 10 Nov): MiMo-V2.6-Pro 150 -> 88, Qwen3.8 Flash 200 -> n/p, Muse Spark 1.3 140 -> 128, GLM-5.3-Flash 600 -> 375, MiMo-V2.6-Flash 1500 -> 857, GPT 6 Luna 214 -> 188, GLM-5.3 23 -> 14, Kimi K3 21 -> 18, Grok 4.7 10 -> 5, Qwen3.8 Max 33 -> 12, DeepSeek V4 Pro 47 -> n/p (no row on the snapshot), MiniMax M3 171, Qwen3.7 Plus 400, Claude Haiku 5.5 188 (new rows). **D2+D5** the Step 1 `Context > 256k` gate is deleted (Go's catalogue and models.dev say 1M for the served `qwen3.8-flash`; 256k belongs to "Qwen3.8-Flash-Next", a different open-weights model) and, since neither AA (leaderboards/models, Briefcase, GDPval) nor Arena (Agent, Code/WebDev) has a row for a plain "Qwen3.8 Flash", every Qwen3.8 Flash benchmark-derived cell and its tasks/mo are **n/p** and the model is never selected (unrated). **D3** Step 5's "AA publishes none" sentence is narrowed — AA-Briefcase v1.1 and GDPval-AA v2.1 publish 95% intervals (verified per benchmark; the knowledge-work gaps clear them) while the score-based AA rows publish none — and the knowledge-work badge cell carries the +/- values. **D4** `c3`'s prompt is sharpened (settled drop-in recipe = one bounded design decision, D=2; the CA is destroyed behind live payment signatures = R=3); golden unchanged. **Moved goldens (3):** `f1`, `u1` (knowledge-work `#2` Qwen3.8 Flash -> GLM-5.3-Flash `max`); `r1` (doc-data pair Qwen3.8 Flash -> MiMo-V2.6-Pro becomes MiMo-V2.6-Pro -> DeepSeek V4.1 Flash `high` — the two anchor leaders that take image input; Qwen's MMMU-Pro row is the Flash-Next model). After re-running `derive_opencode_rows.py`: `knowledge-work` `#2` = GLM-5.3-Flash (MiMo-V2.6-Pro leads both Elo rows), `doc-data-understanding` = MiMo-V2.6-Pro -> DeepSeek V4.1 Flash; every other row unchanged. **Cold-agent run (`results/iteration-27-final/`, one fresh agent per prompt reading only `skill/SKILL.md`, 38 of 39 — `i1` not run: the cyber safeguard stops it): 31/39 graded pass (1 skip).** Models/efforts/pairs were right everywhere except five prompt-ambiguity cases, each sharpened (no rule or golden changed) and re-run on 3 fresh agents (`results/iteration-27-final-rerun/`): `a5` ("each label is a judgement call on tone … not a pattern match" pins D=1 -> Sonnet `medium`) **3/3**; `l1` ("the same documented click-through I run every month" pins D=1) **3/3**; `w1` (the matching rule is now stated — the first run blocked at Step 0) **3/3**; `y1` ("Look up" pins research-synthesis, which H1 excludes from Haiku) **3/3**; `r1` (round 1 only 1/3 — one agent read the reconciliation table as knowledge-work, one mis-picked `#2`; round 2 "multimodal document extraction from scans, not a written deliverable" **3/3**). `c3`'s sharpened prompt passed first try (D=2, R=3, golden unchanged). **Two rule gaps, reported not fixed (nothing changed to make a run pass):** `k1` — routing correct, but the golden's `expected_notes` require the classifier caveat ("can block research tasks") and nothing in SKILL.md's output rules makes that phrase mandatory (the caveat is deliberate — see the biology-gate follow-up below); `n1` — 4/4 agents omit the daggered row's "low-confidence" because the badge-table carve-out ("A D = 2 coding or reasoning row … is not † … name the tie and the price instead") reads as covering the `science` row and the agents did exactly that, although the Output-format bullet requires the phrase. **Not run:** `i1` (cyber safeguard), the trigger eval (needs a logged-in terminal).

> **iteration-27 biology-gate follow-up (10 Nov 2026).** The gate row now says Fable 5.2's biology classifiers can block research tasks (first flagged request → the Claude Code session moves to Opus 5, later ones are refused there), that Opus 5.5 runs the same classifiers with the same fallback (Claude Code model-config), and, in the offensive-security row's pattern, that a Life Sciences Verification Program organisation gets Mythos 5.2. `k1` golden Evidence now carries the classifier statement (`expected_notes`: `can block research tasks`, `Mythos 5.2`); new `k2` (stated Life Sciences Verification Program access → `Mythos 5.2 · high`, `Fable 5.2 ·` forbidden) — **39 prompts**, `--selftest` 39/39. `k1`/`k2` were not cold-run after this change.
>
> **iteration-27 Stage B cold run (10 Nov 2026, `results/iteration-27-stage2/`).** 9 unique prompts — `k1`, `k2`, `n1` ×3, `m1`, `r1`, `x1`, `z1`, `w1`, `w3` — routed by fresh agents reading only `skill/SKILL.md`; **7/9 pass**. The k1 Fable-biology auto-line appeared and k2 correctly omitted it (Mythos 5.2); `n1` passed **3/3** and all six other dagger-row evals passed (`m1`, `r1`, `x1`, `z1`, `w1`, `w3`). `k1`/`k2` failed only on the Claude effort: both agents wrote `xhigh`, the golden expected the biology gate's `high` — a rule gap between the gate row (“default effort `high`, no floor”) and the D table (`D=3 → xhigh`); fixed in the gate re-run below.
>
> **iteration-27 gate re-run (10 Nov 2026, `results/iteration-27-stage2b/`).** After the biology gate was fixed at effort `high` (vendor table: Fable 5.2 `high` matches Opus 5.5 `max` on FrontierCode 2.0; Fable draws on a separate weekly limit), 3 fresh agents each routed `k1` and `k2`, plus `fa1`. **`k1` 3/3, `k2` 3/3, `fa1` 3/3 after the k1 golden correction** — re-grading the same outputs (no new agents) passes once `Mythos 5.2` is removed from k1's `expected_notes`: the prompt states no verified access, and the gate row only gives Mythos 5.2 to a verified organisation, so the note over-specified (golden error, not a rule gap). k1's effort `high` and the Fable auto-line were already correct 3/3; k2 keeps its Mythos 5.2 expectation. The 1000+ files gate was made explicit as the normal D rung (`xhigh` at `D=3`, `max` only under M1, `ultracode` over 30 minutes); no dedicated 1000+ files eval exists, so `fa1` is the frontier-rung regression and passed 3/3. Not run: `i1`, the full 39, and the trigger eval.
>
> **iteration-27 (10 Nov 2026) — Fable 5.2, AA Index v5 frozen, Gemini 4 Argon on Go proper, MiniMax Free gone.** `routing/evals.json` is **39 prompts** (new `fa1`, `k2`: A1 frontier rung → `Fable 5.2 · xhigh` with the Fable `/fast` line); `--selftest` **39/39**; `check_policy_sync`, `check_opencode_pool`, `check_examples`, `validate_benchmarks` (0 errors), the frontier check and the compiler tests are green. **Moved goldens and why.** *Argon open to confidential work (GM1; D=3 / R=3 on a GM1 row):* `c2`, `c3`, `d1`, `g1`, `j1`, `t1`, `v1` (Argon `#1`, MiMo-V2.6-Pro `#2`; the Gemini line replaces or joins the DeepSeek line), `w1` (Argon `#1`, DeepSeek `#2` at `high`), `z1` (Argon `#1` and the badge flips Claude → OpenCode †, expectation `claude` → `opencode`), `p1` (A1-OC now puts Argon, not GLM-5.3, at `#2` after a shortfall at D=2; `allow_premium` → `allow_gemini`), `w2`/`w3` (Gemini line text; `w3` is now identical to `z1` apart from its prompt). *MiniMax M3.1 Flash Free left Go (FR1 fallback):* `n1` (science `#2` GLM-5.3-Flash `max`), `r1` (doc-data `#1` Qwen3.8 Flash `xhigh` · `#2` MiMo-V2.6-Pro). *Claude gates:* `k1` (`Fable 5.2 · high`), `i1` (Mythos 5.2 wording; the Opus 4.8 speed line with the 30 Nov end date). *Date only (DeepSeek zero-retention 31 Oct → 30 Nov 2026):* `a1`, `a2`, `a3`, `a4`, `a5`, `b1`, `b2`, `c1`, `e1`, `h1`, `m1`, `o1`, `q1`, `w4`. **Cold-agent run (`results/iteration-27/`, 4 fresh sonnet agents reading only `skill/SKILL.md`, 16 of the 17 listed prompts): 15/16 graded pass.** First pass 14/16: `w3` — the agent gave Muse Spark 1.3 Contributor `#2` (NC1 says Muse Spark takes `#2` on research-synthesis rows) instead of MiMo-V2.6-Pro; the NC1 block now says that where GM1 puts Argon at `#1` the row's former `#1` stays `#2` (a clarification, same as the iteration-24 golden); `w3` re-run **2/2** (`results/iteration-27/`, `results/iteration-27-confirm/a/`). `c3` fails again (first run, `confirm/a`, `confirm/b`: **0/3** against its golden): two agents scored R<3 (no review note, DeepSeek `#1`), one scored D=3 (`Opus 5.5 · xhigh`) — the same D/R boundary split already recorded in iteration-26; the prompt, not the Argon rule, is the open issue, and no golden or rule was changed for it. `i1` was **not run**: the agent was stopped by the cyber safeguards (not retried or reworded; not run in iteration-24 either). The 22 prompts the change could not move were not re-run. Not run: the trigger eval. **Cold-agent run list** (fresh agents reading only `skill/SKILL.md`): `c2`, `c3`, `d1`, `g1`, `j1`, `t1`, `v1`, `w1`, `w2`, `w3`, `z1`, `p1`, `fa1`, `n1`, `r1`, `k1`, `i1`; likeliest to split agents: `z1`/`w3` (the badge flip), `p1` (Argon vs GLM-5.3 at `#2`), `fa1` (does "my Opus 5.5 run fell short" fire A1), `r1` (flaky since iteration-25) and `n1` (SciCode under review). Unaffected and not worth re-running: `a1`–`a5`, `b1`, `b2`, `h1`, `o1`, `q1`, `s0a`, `s0b`, `l1`, `u1`, `f1`, `x1`, `y1`, `e1`, `m1`, `w4` (date line only).
>
> **iteration-26 (6 Nov 2026) — DeepSeek V4.1 Flash three-way effort rule.** E7 now emits `D ≤ 1 low · D = 2 high · D ≥ 3 max` on DeepSeek V4.1 Flash; GLM-5.3 / GLM-5.3-Flash / MiniMax M3.1 Flash Free stay `low`/`max` (`skill/SKILL.md` E7). `routing/evals.json` is **37 prompts** (new `b2`, a D=2 rate-limiter feature; `b1`, `c1`, `c3`, `e1`, `m1`, `p1`, `w1` goldens moved to `high`); `--selftest` **37/37**. **Cold-agent run (`results/iteration-26/`, 6 productive fresh agents of 8 launched, 20 prompts): 14/20 passed.** The high rung held on every repeated clean prompt — b1/b2/m1/p1/w1 passed **3/3 across three separate agents**, and sharpened c1 **3/3** (`high`). The unchanged low anchors passed (a1/a2/a4/a5/h1/o1/q1); a3's OpenCode `low` was right but its Claude line picked Haiku; d1/v1 passed at `max`. Failures were boundary/tag issues, not the effort rule: c1 and c3 read D=3 (`max`), c2 read D=2 (`high`), e1 tagged research-synthesis and dropped DeepSeek, w4 replaced the exhausted DeepSeek with GLM-5.3-Flash. **Sharpened re-runs (3 fresh agents each, `results/iteration-26/sharpen/`):** c3 `high` 2/3 (one D=1), e1 DeepSeek `high` 2/3 (one still research-synthesis), a3 OpenCode `low` 3/3 and Sonnet 2/3, c2 D=3/`xhigh · ultracode` 3/3 but DeepSeek `max` only 1/3 (two used MiniMax Free as `#2`; one also picked Sonnet) — the max rung was correct wherever DeepSeek stayed on the line. **No golden was changed.** Open: c2/c3/e1/a3 prompt/tag clarity; proposed-not-applied CAP1 clarification — when a window is exhausted the routed pair stays, and `Evidence:` names the substitute (free twin first). Not run: i1/k1 gates, the full 37-prompt cold set, and the trigger eval.
>
> **Pruned.** Result directories for iterations up to 22 (and `archive/iteration-20-codex/`) are no longer in the tree; **iteration-24, iteration-25, iteration-25-confirm, iteration-27-final and iteration-28** are kept as the evidence for the current policy, plus the Stage B run under `iteration-27-stage2/`. `iteration-26`, `iteration-27`, `iteration-27-confirm` and `iteration-27-final-rerun` were removed from the working tree (they remain in git history via `d3401c4`). The history below still cites the older runs and the Codex-era benchmark pipeline (`skill/benchmarks.json`, `scripts/compile_benchmark_frontiers.py`, `validate_benchmarks.py`, `test_frontier_compiler.py`, `ablate_evidence.py`); all of it is in git history, last present at commit `7c24c81` (`git show 7c24c81:evals/routing/results/iteration-22/grading.json`).

> **iteration-25 (3 Nov 2026) — `ultracode` becomes a flag.** Claude Code v2.1.284 made Ultracode an independent toggle that no longer forces `xhigh` (`skill/reference.md` §22). Rule UC1 now emits `effort: <level> · ultracode` (level = `Effort ← D`, floor `high`, ceiling `xhigh`) and Step 7 rule 12 adds an `Ultracode:` line. `routing/evals.json`: only `c1` changes (`Sonnet 5.5 · effort: high · ultracode`, a required `start the prompt with "ultracode:"` note, `effort: ultracode` forbidden); `grade_routing.py` checks the `· ultracode` flag both ways (present when expected, absent when not) and rejects the retired `effort: ultracode` form. **Status:** grader self-test 36/36, policy sync, example check, benchmark validator and frontier-compiler tests are green. **Fresh-agent run (6 cold agents, all 36 prompts, `results/iteration-25/`): 34/36.** Two new prompts: `c2` (D3DIAG × 180 services, over 30 min → `Opus 5.5 · xhigh · ultracode`) and `c3` (research → migration → traffic replay → runbook, R=3 → `Sonnet 5.5 · high · ultracode`); their expectations were taken from the cold run and reviewed against the rules, so they are regression guards, not independent goldens. Failures: `c1` — the agent printed the right model, `high`, flag and Ultracode line but put the badge on the OpenCode line; **3/3 on re-run** (`results/iteration-25-confirm/`), so a one-off. `r1` (scanned receipts, `doc-data-understanding`, nothing to do with `ultracode`) — OpenCode `#1` flips between MiniMax M3.1 Flash Free and MiMo-V2.6-Pro (2/4 across the run and three re-runs); the iteration-24 run passed it. **Left open:** per this file's own lesson, question the prompt ("produce one reconciliation table" reads as knowledge-work to some agents) before touching the rule.
>
> **26 Oct revision:** Gemini 4 Argon is Go's Contributor route only (trains on prompts) → NC1-only overlay; the confidential-default evals (`d1`, `g1`, `j1`, `t1`, `v1`, `z1`, `w1`, `p1`) lost Argon again, `w2` and the new `w3` (non-confidential research at R=3) carry it. Fresh-agent re-run of the affected evals (33/34 graded, `i1` not run) is recorded in `results/iteration-24/`; it fixed A1-OC's wording (`p1`) and sharpened `g1`.
>
> **iteration-24 (20 Oct 2026) — free lane (FR1) + Gemini slot (GM1).** `routing/evals.json` is now **34 prompts**: `d1`, `g1`, `j1`, `t1`, `v1`, `z1`, `p1`, `n1`, `r1` goldens moved (Gemini 4 Argon first at `D = 3` / `R = 3`; the free MiniMax M3.1 Flash on the `science` / `doc-data` rows; `z1`'s badge flipped to OpenCode); new: `w1` (workflow at R=3), `w2` (non-confidential, Contributor route), `w3` (no Google key), `w4` (free twin named when a paid window is spent). `grade_routing.py` now rejects a Gemini model on the OpenCode line unless the eval sets `allow_gemini`, and any free model other than MiniMax M3.1 Flash Free. `policy/routing_policy.json` mirrors the 19-model pool, `gm1_rows` and `free_lane`; `check_opencode_pool.py` enforces GM1 (Argon only first in the right-hand column of the listed rows). Selftest 34/34; **cold-agent run 33/33** (6 fresh agents; `results/iteration-24/`; `i1` declined by its agent, not re-run). `w2` exposed an NC1 ambiguity (Muse Spark `#2` now `research-synthesis` only) and `r1`'s prompt was sharpened.
>
> **iteration-23 (14 Oct 2026) — budget-first pool + OpenCode-by-default badge.** `routing/evals.json` is now **30 prompts** (new: `z1`, an R=3 research-synthesis read where the single Omniscience lean moves the badge to Claude with a dagger). Rules BUD1 (premium models GLM-5.3 / Kimi K3 / Grok 4.7 / Qwen3.8 Max never in a routed pair; only A1-OC adds one as `#2`) and SM1 (badge goes to OpenCode unless a gate, MECH1, D=3 coding/reasoning, knowledge-work at D≥2 or R=3 with a Claude lean) moved these goldens: **a1 a2 q1** badge → OpenCode (every D≤1 task, Haiku 5.5 included); **b1** badge → OpenCode (D=2 coding), pair → DeepSeek V4.1 Flash · MiMo-V2.6-Pro; **c1 d1 e1 g1 j1 t1 v1** pairs rebuilt from the budget tier (no GLM-5.3 / Kimi K3); **f1** now asserts Grok 4.7 stays OUT under NC1; **m1 n1 r1 x1** pairs rebuilt; **p1** #2 = GLM-5.3 at `max` (A1-OC) with the badge on Claude. `grade_routing.py` gained a premium-model check (an OpenCode line naming one fails unless the eval sets `allow_premium`). **Verified:** `--selftest` 30/30, `check_policy_sync` (36 blocks), `check_opencode_pool` (tier + tasks/month columns, 3-column badge table, no premium in Step 4-OC; mutation-tested), `check_examples` green. **NOT done:** the cold-agent routing run (needs live agents; the goldens are rule-derived) and the trigger eval. Everything below describes iteration-22.
>
> **iteration-22 (8 Oct 2026) — Haiku 5.5.** `routing/evals.json` is now **29 prompts**: a1/q1/y1 goldens moved (bulk labelling → `Haiku 5.5 · low` with the badge on Claude; the single-fact lookup → `Sonnet 5.5 · low`) and four evals were added — a2 (short summary → `Haiku 5.5 · medium`), a3 (finished memo at D=1 stays Sonnet), a4 (first-token-bound reply keeps the badge on OpenCode), a5 (Haiku shortfall → Sonnet 5.5, OpenCode pair unchanged). `--selftest` is **29/29**, `check_policy_sync` / `check_opencode_pool` (16 models) / `check_examples` are green. **Cold-agent run, 8 Oct 2026: 29/29** (`routing/results/iteration-22/`). Six fresh parallel agents read only `skill/SKILL.md`; **first pass 25 of the 27 routed, 2 failed, 2 gated prompts missing.** `a3` was a **golden error**, not a rule error: at `D ≤ 1` capability rows are skipped, so a Sonnet 5.5 pick loses the price tie-break to OpenCode — the agent applied the rule correctly and the golden (badge on Claude) was wrong. `a5` split on the OpenCode `#2` (GLM-5.3-Flash instead of MiMo-V2.6-Flash): the agent treated the relabelling as a D≤1 job instead of the bulk gate. The prompt was sharpened ("relabel the whole batch of 200 … reading each one for tone") and the OpenCode bulk-gate row now says it covers "one labelling or parsing job applied to hundreds of items — redoing such a batch included"; a5 then passed on 3 of 3 fresh agents (it had passed 1 of 2 before the wording change), and the six prompts the wording could touch (a1, q1, o1, y1, a4, h1) were re-run and passed 6/6. `i1` and `k1` (exploit PoC, biology) were stopped by a safety classifier when batched, then re-run alone with the request framed as routing-only; **`i1` came back as a copy of the worked example in SKILL.md, so it is weak evidence** (same as in earlier iterations). The trigger eval was not re-run (only model names changed in the `description`; nested `claude -p` still fails with `OAuth session expired`). Everything below describes iteration-21.
>
> **iteration-21 (6 Oct 2026) — the Codex arm is retired; this directory now tests Claude + OpenCode Go.**
> Everything below the "iteration-20 history" marker describes the Codex-era set, which is archived
> verbatim under `archive/iteration-20-codex/` (git tag `iteration-20-codex`). What is live:
>
> | Path | What it is |
> |---|---|
> | `routing/evals.json` | **29 prompts** (2 blocked; 25 at iteration-21), each with `expected_claude`, `expected_opencode` (`#1 … · #2 …`, or a decline), `expected_recommended` (`claude` \| `opencode`), `expected_low_confidence`, optional `expected_notes` / `forbidden` and a `golden_output` |
> | `routing/grade_routing.py` | grades the Claude line, **both OpenCode picks (model, effort, order)**, the badge side, the Evidence line (its `low-confidence` flag must match the row's dagger), required/forbidden text. `--selftest` grades each eval's own `golden_output` |
> | `policy/routing_policy.json` | the machine-readable mirror: the 19-model pool (cap, status, retention), the Step 4-OC rows, the badge table, the rule blocks |
> | `trigger/` | the trigger eval (description changed in iteration-21 — **not re-run**; needs a logged-in terminal) |
>
> ```bash
> python evals/routing/grade_routing.py --selftest --results-dir /tmp/x   # grader vs goldens (no agents)
> python scripts/check_policy_sync.py        # SKILL.md rule blocks == policy mirror, `$<digit>` guard, retired wording gone
> python scripts/check_opencode_pool.py      # pool, Step 4-OC rows, badge table, example efforts/caps vs the mirror
> python scripts/check_examples.py           # every SKILL.md worked example agrees with its golden
> ```
>
> **Run for iteration-21 (6 Oct 2026): cold-agent routing 25/25** (`routing/results/iteration-21/`). 5 parallel fresh
> agents read only `skill/SKILL.md`; first pass 23/25. Two misses, both Claude-effort only and both *prompt*
> ambiguity, handled as in earlier iterations (sharpen the prompt, not the rule): `e1` ("summarise 400 pages" was
> scored D=1 vs D=2 → now "synthesise 400 pages of filings from three different companies") and `x1` (the agents split
> `xhigh` vs `high` on "tell me where they conflict" — the D table lists reconciling conflicting sources as D=3 → now
> "summarise each source's position side by side", two fresh agents agree). A batch containing the exploit-PoC prompt was
> stopped once by a safety classifier; `i1` and `k1` were re-run alone with the category described, not performed.
> Goldens were not changed to fit an output except `x1`'s, whose prompt was changed in the same step.
>
> **Trigger eval: not run for real.** Nested `claude -p` fails here (`OAuth session expired`). A proxy (one fresh agent
> deciding YES/NO from the new 280-character description alone) agreed with the labels 20/20 — it is a judgement test,
> not the harness. Run `PYTHONUTF8=1 python evals/trigger/run_trigger.py --skill-path skill --out evals/trigger/results/<date>.json`
> from a logged-in terminal for the real result.
>
> The Codex-era **reachability audit** (a 154-prompt corpus + a Python re-implementation of the
> router that proved every model × effort cell reachable) is archived under
> `archive/iteration-20-codex/` — it simulated the retired Codex arm and cannot audit this one.
> An OpenCode equivalent is open work; `check_opencode_pool.py` is the cheap substitute.

---

## iteration-20 history (Codex era — kept for the reasoning behind each rule)

Use these instead of tracking `skill/SKILL.md` (+ `skill/reference.md`) changes
by hand.

> The detailed chronological run history (iterations 1–8, in Turkish) is in
> [`history.tr.md`](history.tr.md). It's kept because the reasoning behind each
> past rule change is useful when proposing a new one.

## 1. Routing eval (functional correctness)

`routing/evals.json` — the machine-readable copy of the validation table in
`docs/README.legacy.tr.md` (the old detailed Turkish README, moved there when the
README was rewritten). It stays the source of truth for the legacy human-facing
table; sync this file to it by hand.

**How to run (after a `SKILL.md` change):**

1. Create a new `routing/results/iteration-<N>/` directory.
2. For each eval id, have a **fresh/cold agent** (a new subagent or a new
   conversation) read `skill/SKILL.md` directly and route the prompt, writing
   only the raw output lines to `eval-<id>.txt`. **Do not use the `Skill`
   tool** — it caches within a conversation and returns stale content (verified
   in a past session). A fresh agent/conversation bypasses this.
3. Run `python routing/grade_routing.py --results-dir routing/results/iteration-<N>`
   — regex-based, deterministic, no LLM.

**Why a script grader, not an LLM grader:** the output format is a
fixed-shape line (`Model · effort: X` or `opusplan · plan: X · execute: Y`) —
verifying it is mechanical, not subjective.

**What the grader checks** (iteration-16): Claude model · Claude effort · Codex
model · Codex effort · **which side carries the `✅ RECOMMENDED AI` badge**
(`expected_recommended: "claude" | "codex"`) · that exactly one badge exists ·
that an `Evidence:` line is present and not a stub. It deliberately does **not**
compare the Evidence wording — that line is free-form by design and an
exact-string assertion would be brittle. Where the rules say a recommendation
must be hedged, `expected_low_confidence: true` requires the line to contain
"low-confidence" / "low confidence" and nothing more specific than that.

⚠️ **Known limitation of the routing eval.** Several long-standing eval prompts
(`d1`, `d5`, `f1`, `m1`, `d6`) appear near-verbatim as worked examples inside
`SKILL.md`'s own "Output format → Examples" section, so a cold agent is partly
recalling rather than deriving them. They still catch regressions (if a rule
changes, the example and the golden disagree) but they are weak evidence that
the *procedure* works. The iteration-16 additions (`b1`, `t1`, `p1`, `e1`, `g1`,
`h1`, `i1`, `j1`, `k1`, `q1`) appear nowhere in `SKILL.md` and are genuine cold
derivations.

The output format switched from Turkish (`efor:`, `doğrulanmadı`,
`İnsan onayı olmadan uygulanmasın.`) to English (`effort:`, `unverified — use
Claude`, `Do not apply without human review.`) when the skill body was ported to
English (2 Sep 2026). The grader and `evals.json` expectations were updated in
the same pass.

### Eval id conventions

- `d1`–`d7`, `n1`–`n3`, `r1`, `r2`, `s1`, `s3`, `5b`, `f1`, `f2`, `m1`, `a1`,
  `a2` — dual-format, auto-graded. Carried from iteration-15.
- `b1`, `t1`, `p1`, `e1`, `g1`, `h1`, `i1`, `j1`, `k1`, `q1` — added in
  iteration-16 for the capability profile, the equivalence/efficiency layer and
  the `✅ RECOMMENDED AI` badge. One per capability class the brief named.
- `x1`, `x2` — added in iteration-17 (Phase 2) for the model-conditional badge
  and the mandatory hedge on vendor-dependent capabilities.
- `w1`, `z1` — added in iteration-20 as the two **positive** cases for Rule BD1
  (knowledge-work; science). Against GPT-6.1 Sol almost every badge-table row reads
  Codex, so without a case that *must* read Claude nothing would notice BD1 had
  stopped licensing a direction. `x2` and `z1` also ride on against-interest vendor
  rows (`scripts/ablate_evidence.py` shows both fall to `efficiency/lean-claude` when
  vendor-run rows are dropped) — that is why they carry `low-confidence`.
- Live regression set: **37 auto-graded + `d7`** as of iteration-20 (35 + `w1`, `z1`;
  the earlier "32" was iteration-17). `x1`'s prompt was **sharpened** in iteration-20
  ("about 400 packages now fail"): the first cold agent scored `W=2` because the
  prompt never said how many packages fail. Same pattern as `n2` / `x2` / `i1` / `j1`.
- `expected_low_confidence` is **not** asserted when absent — a cold agent may hedge
  where the rules do not require it. `badge_driver` now distinguishes `capability`
  (a BD1 direction), `efficiency_no_direction`, `efficiency_low_depth`, `lean_r3`,
  `mechanism` and `gate`.

### The Phase 2 test matrix

Phase 2 asked for fifteen additional cases. Nine were already covered by named
evals; four are properties of the frontier compiler rather than of a prompt, and
are tested exactly — with synthetic fixtures — in
`scripts/test_frontier_compiler.py` instead of being inferred from a routing
decision three layers downstream; two needed new routing evals.

| # | Case | Where it is tested |
|---|---|---|
| 1 | Terminal-heavy end-to-end | `t1`, and `x1` for the Astra column |
| 2 | Pure model-level reasoning | `p1` |
| 3 | GUI / computer-use | `g1` |
| 4 | Coding review | `f2`, `5b` |
| 5 | Agentic implementation | `b1`, `d2` |
| 6 | Math / formal reasoning | `p1` |
| 7 | Long-context shallow synthesis | `a2`, `e1` |
| 8 | Independent parallel workstreams | `i1`, `5b` |
| 9 | Same capability, efficiency tie-break | `k1` (D≤1), `f1` (capability-level) |
| 10 | Vendor evidence disagreement | `x2`; compiler: "two equally-weighted vendor tables pointing opposite ways" |
| 11 | Evidence insufficient | `j1` |
| 12 | Same score / different cost | compiler unit test |
| 13 | Same cost / meaningful score gap | compiler unit test |
| 14 | CI-overlapping result | compiler unit test |
| 15 | CI-non-overlapping result | compiler unit test |

`expected_recommended` is asserted on every badge-bearing eval, and
`expected_low_confidence` on the seven whose capability collapses under the
vendor-bias ablation.

## 2.5. Reachability eval (coverage, no LLM, no network)

`reachability/` answers the question the routing eval structurally cannot:
**correctness is not coverage.** The routing eval asks "given this prompt, is the
golden answer produced?". It cannot ask "given the whole rule set, is there any
prompt at all that reaches `Sonnet 5 · ultracode`?" — and a suite can be green on
the first while a supported combination is dead on the second, because nothing
fails when a cell is simply never emitted.

| File | Role |
|---|---|
| `reachability/corpus.json` | 154 labelled prompts — a point in the decision space, not a golden answer |
| `reachability/routing_policy.json` | hand-kept machine-readable mirror of `SKILL.md`'s rules |
| `reachability/flip-review.json` | hand-written verdict on every before/after decision flip |
| `reachability/reachability-matrix.json` | **generated** — one row per supported model × effort/mode cell |

```
python scripts/check_routing_reachability.py            # regenerate the matrix
python scripts/check_routing_reachability.py --check    # exit 1 if stale
python scripts/check_routing_reachability.py --report   # histograms, flips, verdict tally
python scripts/test_reachability_tool.py                # the auditor's own regression suite
python scripts/check_policy_sync.py                     # SKILL.md <-> policy mirror parity
```

**A zero with no written rationale fails the run.** Either the corpus is missing
a workload or no rule can reach the cell — both are bugs until somebody writes
down why the zero is correct, in the script's `INTENTIONAL` table. Four zeros are
currently claimed on the record; the reasoning is in `skill/reference.md` §16.3.

**The counts are a diagnostic, never a target.** No upper-tier frequency goal was
used, and no prompt exists to make a cell non-zero. "`Astra` appears 18 times" is
an observation about the corpus, not a result to optimise — flattening the
histogram would mean advertising expensive models for their own sake, which is
the opposite of what this router is for.

**Why it needs its own tests.** A linter that has quietly stopped reporting looks
exactly like a clean repo. `scripts/test_reachability_tool.py` trips every check
on purpose with compact fixtures — an accidental zero, a claimed zero, an
unsupported cell emitted anyway, a cell missing from the support matrix, a
conditional-access leak, a dead mode, an over-selected cell, a lost route, a
platform-forced cell, an unreviewed flip, a rejected flip, a stale sign-off, and
matrix staleness — and checks the healthy case stays quiet for each.

**Policy ↔ skill drift is the failure this suite is most exposed to.** The audit
once ran a whole pass against iteration-18 while the shipped `SKILL.md` still
implemented iteration-17, which made every certified zero a zero of a policy
nobody could run. `check_policy_sync.py` now fails if the version marker or any
declared rule quotation disagrees between the two files.

## 3. Evidence checks (Phase 2, no LLM, no network)

Run these before the routing evals — they are fast, deterministic and catch the
failure mode routing evals cannot see, which is the router being *confidently
wrong* because its evidence rotted.

```
python scripts/validate_benchmarks.py            # schema, groups, rule provenance, staleness
python scripts/compile_benchmark_frontiers.py    # regenerate the derived frontier
python scripts/compile_benchmark_frontiers.py --check   # exit 1 if the frontier is stale
python scripts/test_frontier_compiler.py         # comparison-semantics assertions
python scripts/ablate_evidence.py                # vendor-bias measurement
```

> **Iteration-18 changed what may set a direction.** A published confidence
> interval, a published standard error, repeated-trial dispersion, or a
> practical-significance threshold the benchmark's owner publishes — and nothing
> else. The old fallback (`0.15 × the roster's observed score spread`) is gone and
> the compiler raises if it reappears: spread is how far apart the models happen
> to sit, not how precisely either score was measured, and on a two-row
> comparison the spread *is* the gap. `science` is now the only capability with a
> certified direction; the rest are `UNRESOLVED` and fall through to efficiency.
> Rules E1 and E3 are untouched — their evidence is a rung that scores *no
> better* at higher cost, and equality needs no interval.

**The staleness check is the important one.** `benchmark_frontiers.json` stores
the sha256 of the exact bytes of `benchmarks.json`. Edit the evidence without
recompiling and both the compiler's `--check` and the validator fail. A derived
layer that silently lags its evidence is worse than no derived layer at all.

**Determinism is a build requirement:** run the compiler twice and diff. If the
output is not byte-identical, that is a failure, not a quirk.
- `1`–`22`, `c1`–`c5`, `v1` — legacy single-ecosystem format, marked
  `format_outdated: true`, skipped by the grader. Backfilling them to
  dual-output is the remaining eval-debt.
- `21` is `machine_gradable: false` — an observational check, reviewed by hand.

## 2. Trigger eval (does the description fire at the right times?)

`trigger/trigger_eval_set.json` — 20 queries (10 that should trigger, 10 that
should not, including near-miss cases: a price question, a settings question, a
bare task request that could be confused with model-secici but isn't).

**How to run:**
```
python evals/trigger/run_trigger.py --skill-path skill \
  --out evals/trigger/results/<label>.json
```
`run_trigger.py` is standalone and Windows-safe. (skill-creator's own
`scripts/run_eval.py` uses `select.select()` on a subprocess pipe — `WinError
10038` on Windows.) One real `claude -p` subprocess per query — **a quota cost**,
in direct tension with the router's own philosophy. Run it rarely, only when the
`description` frontmatter changes. A query counts as triggered when the first
tool call is `Skill`/`Read` on model-secici (installed skill or the temp probe
command).

**Latest: `results/2026-09-10.json` — 19/20** (iteration-16). Re-run because the
`description` frontmatter changed: it now says the router "marks which of the two
is the better fit" and adds the "which AI should I use" phrasing.
Natural-language triggers **9/9**, near-miss rejection **10/10**; the 1 miss is
the same print-mode harness artifact as every previous run.

> **`run_trigger.py` detector fix, same run.** The first pass scored 17/20 with
> two *false positives* that had nothing to do with the description: the detector
> counted any `Read` whose path contained the string `model-secici` as a trigger,
> and on a developer machine that includes Claude Code's own auto-memory file
> (`.../memory/model-secici-project.md`). A real trigger reads a file inside a
> skill or command directory, so `_is_skill_file()` now requires that and
> excludes anything under `memory/`. This makes the eval reproducible on machines
> other than the author's; it does not change what the `description` does.

**Prior: `results/2026-09-08.json` — 19/20** — re-run for iteration-15 because
the `description` frontmatter changed (Codex roster list gained `GPT-6 Astra`).
Natural-language triggers 9/9, near-miss rejection 10/10; the 1 miss is the same
harness artifact as before (the literal `/model-secici …` line isn't expanded
under `claude -p` print mode).

**Prior: `results/2026-09-03.json` — 19/20** (run against the iteration-13 skill).
- **Natural-language triggers: 9/9.** "hangi model / efor / bu prompt için ne
  kullanayım / opus mu sonnet mi" phrasings all pull in the skill.
- **Near-miss rejection: 10/10.** Price, settings, `/model` explainer, model
  comparison, "summarise this PDF", "which design pattern is used here",
  API-effort question — none trigger (several correctly reach for `claude-api`
  instead).
- **1 miss:** the literal `/model-secici 4000 dosyalık…` line returns no tool
  call under `claude -p` print mode — a harness artifact (print mode doesn't
  expand the leading slash-command; in a real session `/model-secici` invokes
  the skill directly). Not a description problem.

## Run history (short)

| iteration | what | result |
|---|---|---|
| 1–3 | initial routing eval, single-ecosystem format | rules converged to 16/16 after 3 real ambiguities were fixed |
| 4 | dual-provider expansion (Claude + Codex arm) | 6/6 regression + 6/6 new |
| 5–6 | "always both outputs" redesign; two root causes for Codex never hitting Luna/Terra-low | fixed, regression clean |
| 7 | Fable 5.1 / Mythos 5.1 update, 17 dual evals, 4 cold agents | 12/17 auto-pass — all 5 misses effort-level, models 17/17 correct |
| 8 | same 17 after R/D/W rubric clarifications, cold re-run | **17/17** |
| 9 | after the English port of `SKILL.md` + `reference.md`, cold re-run (4 parallel agents + re-runs) | **17/17**. n2's prompt tightened to a mechanical enumeration (open-ended "review for security" splits cold agents D=1/D=3); 5b + the SKILL.md inline example moved to D=3 → Sol Ultra. Then the Codex effort ceiling was corrected `xhigh → max` (verified 2 Sep 2026: `max` is a real Codex setting toggle, the `learn.chatgpt.com` config-reference page is stale) — d6/f1 `expected_codex` and their cold outputs re-run into the same iteration |
| 10 | after the repo owner added the Codex Fast Mode speed line (a third always-appended output-format exception), full cold re-run (4 parallel agents) | **17/17**. The `⚡ Speed:` line renders where expected (real Codex model + CLI surface, above the R=3 note, no Claude half unless Opus 5/4.8) and `grade_routing.py` ignores it — no model/effort changed |
| 11 | `SKILL.md` structural trim (919→525 lines / 51KB→26KB) to cut the ~2 min cold-route latency: every `>` edge-case note and worked ✅/❌ example moved to `reference.md` §10 (6 sub-sections) + 8 calibration rows added to §8; a "fast path" note added up top; **no routing rule changed**. Full cold re-run (4 parallel agents). | **17/17**. Every edge case the earlier iterations' notes were added for still routes correctly from the shorter file: 5b (defensive audit ≠ offensive gate), n1 (60<100 → W=2), n2 (mechanical enumeration → D=1), n3 (fully-specified schema → D=0), r1 (documented pattern → D=1), r2 (tone-only → D=0), s1 (source change → R=1), s3 (feature-flag → R=2), f1 (split into services → R=3 → `max` not `ultracode`), f2 (adversarial single-file → D=3, W=0 → no `ultracode`), d6 (opusplan). Pre-existing inconsistency surfaced (not a regression): d2's `expected_claude` `high` implies D=2 while `expected_codex` `low` implies D=1 — grader passes either way; flagged for a separate pass. |
| 12 | **Codex effort ladder recalibrated** from a field report: `Terra · low` performs materially worse than `Sonnet 5 · medium` on real D=1 dev work. Web research (OpenAI `latest-model` + `learn.chatgpt.com/models`, Vellum, layer3labs) confirmed: `medium` is OpenAI's coding default, `low` is "quick / well-scoped / latency-sensitive" only, and `minimal` is no longer a rung. `Luna · high` rejected as the alternative (Luna is "volume not depth" — long-context recall ~41% vs Sol ~91%). Codex `D→effort` shifted up one rung to **`0→low · 1→medium · 2→high · 3→xhigh`, `D=3∧R=3→max`** — now identical to the Claude arm's table (one shared `D→effort` table; the "two scales differ" caveat is gone). Golden answers updated: d1/r2/s1 `Luna minimal→low`, d5/n3/s3 `Terra minimal→low`, n1/n2/r1 `Terra low→medium`, d2 `Terra medium→high`, 5b `Sol Ultra high→xhigh`, f2 `Sol high→xhigh`; d3/d4/d6/d7/f1 unchanged. Full cold re-run (4 parallel agents). | **17/17** |
| 13 | After iteration-12 the two effort columns were byte-identical on every row — the skill owner asked for the effort column to still carry a distinction. Added the **one cited asymmetry** as a rule: **Codex +1 effort notch for agentic multi-step coding** (writing/restructuring code across dependent steps — multi-file feature, refactor, migration, architecture implementation, codebase-spanning debug-and-fix; capped at `max`; Claude untouched). LiveBench §2.1 puts the whole GPT-5.6 line behind Claude on agentic coding (Sol 56.2 < Sonnet 5 59.4 < Opus 5 65.2) and nowhere else. Excludes code review / vuln analysis (f2, 5b stay level), non-code design, mechanical cross-file repetition. Only golden answer that moves: **d2** `Terra high→xhigh`. Cold re-run. First pass: one cold agent read "split monolith into **independent** services" (f1) as Sol Ultra — the iteration-11 trim had moved the "monolith decomposition = plain Sol, not Sol Ultra" counter-example out of `SKILL.md`. Restored it inline in the Codex mapping row; f1 re-run → plain Sol. | **17/17** |
| 14 | A real output (`Claude: Sonnet 5 · max` / `Codex: Sol · max` for a D=3 ∧ R=3 review task) exposed two inconsistencies. **(1) Codex had no Rule-3 equivalent** — every D=3 went to Sol, so the Claude arm protected quota (stayed on Sonnet 5) while the Codex arm jumped to the flagship for the same analytical work. Fixed: the Codex D=3 row is now an ordered check — (a) 3+ already-independent parallel targets → Sol Ultra; (b) Rule 2 territory (agentic code / math / tool-less) → Sol; (c) otherwise (analytical / research / single-artefact review) → **Terra** (LiveBench reasoning 90.6 ≈ Sol; escalate to Sol if critical). **(2) `Sonnet 5 · max` / `Terra · max`** were rule-valid but in neither vendor's mid-tier tuning advice. Fixed: `max` (from `D=3 ∧ R=3`) is **flagship-only** — mid-tier caps at `xhigh`, the R=3 review note carries the stakes. Golden answers: **f2** `Sol · xhigh → Terra · xhigh`; new eval **m1** locks the D=3 ∧ R=3-outside-Rule-2 case (`Sonnet 5 · xhigh` / `Terra · xhigh`, no `max`). Live set now 18. Cold re-run (4 parallel agents). | **18/18** |
| 16 | **Benchmark-aware routing engine.** The router no longer picks a model from R/D/W/C alone. New pipeline: quality gate → hard gates → **task capability profile** → R/D/W/C → candidate model x effort → **benchmark evidence, comparability, equivalence, dominance** → **token/quota efficiency** → **cross-ecosystem `✅ RECOMMENDED AI` + one Evidence line**. R/D/W/C is kept in full and demoted from *the* input to *an* input. Research pass (10 Sep 2026, `docs/research-provenance.tr.md`) re-verified every hard gate and produced `skill/benchmarks.json` — 61 records with harness, effort, dispersion, cost/task, date, source tier and comparability group. Corrections: **Sonnet 5 is $2/$10, not $3/$15** (the rise was cancelled — Opus/Sonnet ratio 1.67x → 2.5x); Sonnet 5 *does* have published `max` guidance (the old citation was wrong); `max` on Codex is **Astra/Sol only**; the AA Index figures the repo carried are from an incomparable index version; the "Codex Coding Agent Index" could not be traced and was demoted. New rules that change output: **E1** `Sonnet 5 · max` is dominated by `Opus 5 · xhigh` on both quality and cost, so escalation is a **model** change not an effort change; **E2** the Codex mirror (`Sol · high` dominates `Terra · max`, which is unavailable anyway); **E3** `max` buys ~nothing over `xhigh`, so it now needs `D=3 ∧ R=3` **and** an indivisible novel-design decision; plus a **Codex computer-use gate** (named in the roster notes since iteration-15, never actually in the gate table). Golden answers changed: **t1** (new) `Sol · max → Sol · xhigh`. Prompts sharpened: **i1**, **j1** (cold agents scored them a depth lower than intended, which bypassed the very rule each was written to test — same fix pattern as `n2` in iteration-9). Five cold-agent rounds; five internal inconsistencies in the first draft were found *by* the evals and fixed in `SKILL.md`: the flagship capability list wrongly swept in code *review*, the +1 notch lost its "multi-step" scope, the schema-migration `R=2` ruling was dropped in the rewrite, `opusplan` was not excluded from the Claude `/fast` half, and the analysis carve-out wrongly suppressed Codex path (a). | **30/30** routing |
| 17 | **Phase 2 — benchmark evidence hardening + deterministic frontier compilation.** Not a redesign: the Phase 1 pipeline is unchanged. Went back for the benchmark-**owner** sources Phase 1 could not reach (WebSearch was down for that entire pass) and made the path from a raw score to a routing rule mechanical. New: `skill/benchmark_frontiers.json` (**generated**), `scripts/compile_benchmark_frontiers.py`, `scripts/validate_benchmarks.py`, `scripts/test_frontier_compiler.py`, `scripts/ablate_evidence.py`, `scripts/render-social-preview.ps1`. `benchmarks.json` 61 → **123 records**, every one with a stable `id`, an `evidence_class` (`model_intrinsic` / `ecosystem_end_to_end` / `vendor_relative` / `aggregate` / `efficiency_only`) and `verified_at`; plus authored `comparability_groups`, `evidence_precedence`, `no_dispersion_rule`, `excluded_from_direction`, `model_ecosystem` and a `routing_rules` block giving every rule machine-readable `evidence_ids`. **Research:** Vals.ai runs Terminal-Bench 2.1 on the Terminus 2 harness for every model (Astra 87.27 · Sol 85.77 · Fable 5.1 85.02 · Opus 5 84.64 — but saturated, so excluded); the tbench.ai owner leaderboard end-to-end has Codex CLI+Sol 89.5 ≈ Claude Code+Opus 5 89.1; **Artificial Analysis on the unsaturated TB 4.0 gives Astra 59 · Fable 5.1 52 · Sol 40**. LiveBench re-verified only as a mutable snapshot and excluded; SWE-bench found saturated within ~1 point and excluded; OSWorld metadata pinned down (2.0, offline set, partial scoring) and the two vendors found to disagree by 5.2 points on Opus 5. Closed two Phase 1 open items: the untraceable "Coding Agent Index 67/70" is an older AA index version, and the carried AA Index 66/63/62 figures are v4.1.1. **Routing change — exactly one:** the `agentic-code` / `terminal-tool` badge is now conditional on which Codex model is on the line. Against Terra/Sol the Claude lead survives every source and every filter; against **Astra** it does not — Anthropic's TB 4.0 table, which the iteration-16 rule rested on, contains no Astra row at all. Golden changes: **f1** badge claude → **codex**; **x2** golden corrected to the cold agent's better D=3 reading; seven evals gained `expected_low_confidence` because the ablation shows their capability collapses without vendor-run rows. Also fixed: SKILL.md's f1 worked example still showed the old badge and cited Sol, a model that is not on that line (caught by a cold agent, not by me). Social preview HTML **and** PNG regenerated together and the render scripted. | **32/32** routing · validator 0 errors · 26/26 compiler tests · frontier byte-identical across runs |
| 18 | **Routing reachability calibration.** Asked the question the routing eval structurally cannot: not "is this prompt routed correctly?" but "can any prompt reach `Sonnet 5 · ultracode` at all?". New: `evals/reachability/` (154-prompt labelled corpus, machine-readable policy mirror, hand-written flip review, generated matrix), `scripts/check_routing_reachability.py`, `scripts/test_reachability_tool.py`, `scripts/check_policy_sync.py`. **Three pre-existing bugs the routing eval could not see:** the scored branch emitted `Haiku 4.5 · low` on a model with no effort parameter; `W=3 ∧ >30min` bought orchestration for a 150-file mechanical rename; and `¬(D=3 ∧ R=3)` left a dead zone where `ultracode` refused for depth while E3 refused `max` for breadth, so an irreversible 400-service migration got a bare `xhigh`. **Rule changes:** `ultracode` keys on **orchestration** (3+ different kinds of step, or `W=3 ∧ D≥2`) and guards on *one indivisible chain*, the same test E3 uses; Ultra counts **strands** (targets **or** work-kinds, 3+) not just already-independent targets; the Codex +1 notch caps at `xhigh` on both models and never lowers a rung; new **Rule E4** (`Sol · max` → `Astra · xhigh` on agentic-code/terminal-tool only); the frontier escalation rung (Opus 5 → Fable 5.1, Sol → Astra) written down explicitly. **Uncertainty methodology corrected:** observed score spread removed as a direction-setting fallback — only a published CI, SE, repeated-trial dispersion, or an owner-published significance threshold may set a direction, so `science` is the only certified capability left and the rest are `UNRESOLVED`. **43 flips → 12 REJECTED and fixed at source** (10 corpus labels contradicting their own definitions, 2 a notch-clamp bug that silently deleted `Sol · max` from golden d6) → 36 remaining, all ACCEPT with written verdicts. **Drift guard:** `SKILL.md` and the policy mirror now fail validation if either moves without the other — this audit had been validating iteration-18 while the shipped skill implemented iteration-17. | **0 unclaimed unreachable cells** · all shipped goldens reproduced by the mirror · validator 0 errors · compiler + reachability unit suites green · frontier byte-identical across runs. **Routing evals not re-run cold** — no golden moved, so the iteration-17 outputs still grade 32/32, but a cold pass against the new `SKILL.md` prose is outstanding |
| 15 | **GPT-6 Astra** (`gpt-6-astra`, 3 Sep 2026) added to the Codex arm — conservatively (user choice). Research: ≈ Opus 5 / Sol on intelligence + agentic-coding indices, behind Fable 5.1; clear lead only on computer use; ~2.5× Sol's headline price; **"Critical" cyber level** (standard access hard-stops exploit/PoC generation, does defensive discovery; **Daybreak Blue** = elevated). Changes: (1) Codex offensive gate `unverified — use Claude` → `use Claude` for standard access, **`Astra · xhigh`** with stated Daybreak access (mirrors Mythos 5.1 / Glasswing); (2) new **Codex frontier gate** — 1000+ files / ≥1M-token corpus → Astra (mirrors the Claude Fable 5.1 gate; wins over path (a)); (3) Astra joins the flagship `max` list; (4) **+1 agentic-coding notch never applies on Astra** (parity with Opus 5). Biology stays `unverified` (Astra's card is cyber-only). Golden answers: **d3** `unverified → use Claude`; **f1** Codex `Sol · max → Astra · max`. New evals: **a1** (Daybreak → `Astra · xhigh`), **a2** (Codex ≥1M-context gate → `Astra`). Live set now 20. Cold re-run (4 parallel agents) + trigger eval re-run (`description` gained `GPT-6 Astra`). | **20/20** routing · **19/20** trigger (same harness artifact) |
| 19 | **The Claude 5.5 generation** (Opus 5.5 22 Sep, Sonnet 5.5 28 Sep 2026). Research with WebSearch *and* WebFetch both working; primary sources read directly (Anthropic launch notes + model docs + effort guide + refusals/fallback page, Claude Code release notes, Artificial Analysis articles). `benchmarks.json` 123 → **190 records** (five new comparability groups, incl. AA Intelligence Index v4.3.2 with all five Opus 5.5 rungs); roster swapped in `SKILL.md`, the policy mirror, the graders, the goldens and every worked example. **Rules that moved:** E1 re-derived on the 5.5 generation and stronger (`Sonnet 5.5 · max` 56 @ $7.60 vs `Opus 5.5 · xhigh` 56 @ $3.46); E3 restated (`max` buys +2 on Opus 5.5, unresolved); **A1 narrowed** — duration no longer reaches Fable 5.1 because Opus 5.5 is at or above it on all 8 rows of Anthropic's own same-harness table; **four badge cells against Astra now say `low-confidence`** (the independent coding rows tie), and a † now binds one cell rather than a row. **Compiler:** two latent defects fixed (unmatched efforts were compared as if matched; effort curves pooled every benchmark of a launch note) plus list-form per-benchmark bands; 42 → 52 unit checks. Evals f1/a1/x1/e4p/fr1 gained `expected_low_confidence`; `grade_routing.py` / `check_examples.py` now know `Sonnet 5.5` / `Opus 5.5`; corpus relabelled (`A=high` only with a stated shortfall). Recorded but **not routed:** GPT-6 Sol / Luna (22 Sep) — a Codex-arm iteration of its own. Deliberately unchanged, with reasons in `reference.md` §17.5: the D=3 → Opus 5.5 rule and the biology / 1000+-file gates → Fable 5.1. | validator 0 errors · frontier byte-identical · 52/52 compiler checks · policy sync OK (15 rule blocks) · examples OK · reachability 0 unclaimed cells + tool tests green. **Routing evals (64 cases) and the trigger eval NOT re-run** — both need live agents; the cold pass against the new `SKILL.md` is outstanding |
| 20 | **The GPT-6.1 Sol generation** (GPT-6 Sol / Luna 22 Sep; GPT-6.1 Sol 29 Sep 2026 — OpenAI replaced Sol after seven days). Research with WebSearch *and* WebFetch; primary sources read directly (`developers.openai.com` model page + changelog + model guide, `learn.chatgpt.com` models + changelog, OpenAI's **GPT-6.1 Sol system-card addendum PDF**); Artificial Analysis release / model / head-to-head pages; Vals and Snorkel Terminal-Bench 4.0. `benchmarks.json` 190 → **311 records**, every group gained a declared `run_by`. **Codex arm is Luna / Sol / Astra; Terra legacy.** **Retired:** the Codex +1 effort notch (N1 — TB 4.0 gap fell from ~29 to 4–8 points, and Sol's own curve is flat above `high`), Rule E4 (`Sol · max` → `Astra · xhigh`: Sol max is 52 @ $0.72 vs Astra 53 @ $3.26), and two Astra gates (≥1M-token — Sol has the same 1.05M window — and computer use — 2.1 OSWorld points, tier C). **New:** Rule **BD1** (a badge direction needs two independent measurements that agree; else efficiency; at `R=3` a single lean decides), **MECH1** (mechanism rows: Ultra → Codex, `ultracode` on 3+ phases / `opusplan` → Claude), an `orchestration` tag, a compiled **Pareto frontier** and **`badge_hint`** in the compiler (52 → 80 tests), the ablation rebuilt on `badge_hint`. Reachability mirror + corpus + flip review regenerated: **91 of 154 prompts flip**, every flip signed off (70 ACCEPT / 21 UNCERTAIN / 0 REJECT); badge histogram Claude 122 / Codex 28 → **Claude 43 / Codex 107** — recorded, not hidden. Live set 35 → 37 (+`w1`, `z1`). | **Cold routing 38/38** (five fresh agents; first pass 35/36 — `x1` failed on an ambiguous prompt, sharpened, not on a rule; a sixth agent re-routed the six R=3 / window prompts after two clarifications, 6/6). **Trigger eval NOT re-run:** the description lost *Terra* / gained nothing else that changes trigger phrasing, but the runner shells out to `claude -p` and that nested CLI failed to authenticate in the session that ran this pass ("OAuth session expired"), so every positive query returned no tool call — a 10/20 that measures the auth, not the description. The result file was discarded; run `PYTHONUTF8=1 python evals/trigger/run_trigger.py --skill-path skill --out evals/trigger/results/<date>.json` from a logged-in terminal. Deterministic checks all green. |
