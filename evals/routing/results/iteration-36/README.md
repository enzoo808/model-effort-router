# iteration-36 runs (18 Nov 2026)

Two small runs; no full 49-eval cold run (one clause of `SKILL.md` changed).

## `tr-router/`: the Turkish mirror as the router

Two fresh Claude Sonnet 5.5 agents (`claude-sonnet-5-5`), seven prompts each, read **only** `claude-ai/instructions.tr.md`
and a file of prompts (never `SKILL.md`, never the goldens). 13 evals chosen by the rules fixed in the mirror, plus `pr1`,
an ad-hoc schema-migration probe that is **not** in `evals.json` (no eval has a schema migration). Graded by
`grade_routing.py`; every one of these 13 passed in English in `results/iteration-35`.

| id | rule under test | first pass (Turkish) | after mirror fix |
|---|---|---|---|
| `p1` | A1-OC shortfall, Claude cell, Argon `#2` | pass | |
| `fa1` | A1, flagship list | pass except the `/fast` line* | |
| `dg1` | D3DIAG read-only analysis | pass | |
| `da1` | D=3 analysis on a flagship tag | pass | |
| `c2` | D3DIAG bisect drives the artefact, `ultracode` | pass except the `/fast` line* | |
| `sc1` | D=3 science on the flagship list | pass except the `/fast` line* | |
| `ar1` | D=3 workflow-automation | pass except the `/fast` line* | |
| `g1` | M1 `max` | pass | |
| `kw1` | knowledge-work badge, `R=3` | pass | |
| `u1` | knowledge-work badge, `R ≤ 2` (OpenCode †) | pass | |
| `e1` | W counts what is acted on (400 pages, `C=3`) | pass | |
| `pr1` | schema migration is `R=2` (probe, hand-graded) | pass: Sonnet 5.5 `low`, DeepSeek · GLM-5.3-Flash `low`, OpenCode | |
| `c3` | `R=3` right-hand column, GM1 | **fail**: `#1 Hy4` instead of Argon | **pass** (`rerun/`) |
| `w3` | NC1 exception, `D`, `R=3` | **fail**: scored `D=1` (Claude `medium`), Muse `#2` | **fail again** (`D=1`, Claude `medium`; no Muse this time) |

\* The `/fast` speed line is a declared omission of the mirror (Claude.ai has no `/fast`); grading copies with that one line
appended passes all four. The raw files are untouched.

**What the failures were.** `c3` and `w3` failed only in Turkish: the mirror lacked the Step 4-OC procedure (right-hand column
for `D = 3` *or* `R = 3`, GM1 on top) and the D examples for the non-coding columns (a multi-source synthesis is `D=2`). Both
added to the mirror; `c3` re-run once with a fresh agent passes. `w3` re-run once still fails: a fresh agent reads "tell me what
each of three pages says" as three single-source summaries (`D=1`) although the mirror now lists multi-source synthesis as `D=2`.
This is a **finding**, not a mirror defect that was proven: neither the mirror nor `SKILL.md` states whether reading several
sources and reporting each separately is a synthesis; the English agents of iteration-35 scored `D=2`. No third agent was run.

## `en-rerun/`: `SKILL.md` as the router

One fresh Sonnet 5.5 agent, the four evals that depend on the `D = 3` `agentic-code` / `terminal-tool` badge cell
(`c2`, `dg1`, `v1`, `d1`): **4/4 pass**, so the pointer clause changed nothing. Caveat: for `d1` the agent said it copied the
worked example in `SKILL.md` for that exact prompt, so `d1` tests little.
