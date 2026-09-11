# model-secici eval set

Use these instead of tracking `skill/SKILL.md` (+ `skill/reference.md`) changes
by hand.

> The detailed chronological run history (iterations 1–8, in Turkish) is in
> [`history.tr.md`](history.tr.md). It's kept because the reasoning behind each
> past rule change is useful when proposing a new one.

## 1. Routing eval (functional correctness)

`routing/evals.json` — the machine-readable copy of the validation table in
`README.tr.md`. The Turkish README stays the source of truth for the human-facing
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
- Live regression set: **32** as of iteration-17.

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
