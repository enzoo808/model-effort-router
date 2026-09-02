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

- `d1`–`d7`, `n1`–`n3`, `r1`, `r2`, `s1`, `s3`, `5b`, `f1`, `f2` — dual-format,
  auto-graded. This is the live regression set.
- `1`–`22`, `c1`–`c5`, `v1` — legacy single-ecosystem format, marked
  `format_outdated: true`, skipped by the grader. Backfilling them to
  dual-output is the remaining eval-debt.
- `21` is `machine_gradable: false` — an observational check, reviewed by hand.

## 2. Trigger eval (does the description fire at the right times?)

`trigger/trigger_eval_set.json` — 20 queries (10 that should trigger, 10 that
should not, including near-miss cases: a price question, a settings question, a
bare task request that could be confused with model-secici but isn't).

**How to run:** use skill-creator's `scripts/run_eval.py`:
```
python -m scripts.run_eval --eval-set trigger/trigger_eval_set.json \
  --skill-path <installed skill path> --runs-per-query 1 --verbose
```
This spawns a real `claude -p` subprocess per query (default 3 runs × 20 queries
= 60 real calls) — **a quota cost**, which is in direct tension with the router's
own philosophy. Run it rarely, only when the description changes.

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
