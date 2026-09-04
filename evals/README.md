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

**Why a script grader, not an LLM grader:** the output format is a single
fixed-shape line (`Model · effort: X` or
`opusplan · plan: X · execute: Y`) — verifying it is mechanical, not subjective.

The output format switched from Turkish (`efor:`, `doğrulanmadı`,
`İnsan onayı olmadan uygulanmasın.`) to English (`effort:`, `unverified — use
Claude`, `Do not apply without human review.`) when the skill body was ported to
English (2 Sep 2026). The grader and `evals.json` expectations were updated in
the same pass.

### Eval id conventions

- `d1`–`d7`, `n1`–`n3`, `r1`, `r2`, `s1`, `s3`, `5b`, `f1`, `f2`, `m1` —
  dual-format, auto-graded. This is the live regression set (18 as of
  iteration-14).
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

**Latest: `results/2026-09-03.json` — 19/20** (`description` unchanged since the
initial release; run against the iteration-13 skill).
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
