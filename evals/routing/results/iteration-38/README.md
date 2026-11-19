# iteration-38 cold run (20 Nov 2026)

Full 53-eval regression set after the iteration-38 change (TG1, the Claude-only tool gate; four new evals `tg1`-`tg4`),
plus the 24-id Turkish mirror pass. Graded by `evals/routing/grade_routing.py` (regex, no LLM). Branch `iteration-38-tool-gate`
at `15eaa11`. Goldens were never shown to any agent.

**English: 49/53 on the first pass (`o2`, `w3`, `tg3`, `tg4` failed). After one re-run each: `o2` passes (N); `tg3` and `tg4` failed
again and the goldens were corrected (class G, see below); `w3` failed again (class A, a repeat of the iteration-37 finding).
With the two corrected goldens the first-pass files grade 50/53 (`o2`, `w3`, `tg4`-Haiku remain) and the re-run files pass
`o2`, `tg3`, `tg4`; the only open English item is `w3`: 52/53 effective.**

**Turkish mirror (24 ids): 10/24 raw; 18/24 with the declared `/fast` lines appended to grading copies; 20/24 after one re-run
(`tg1`, `tg2` pass). Open: `c2` (A), `p1` (A), `w3` (A) and `j1` (declared omission of the mirror).**

## Method

- **Agents:** 10 first-pass fresh Claude Sonnet 5.5 agents (Agent tool, `model: sonnet`; a preflight agent first answered
  `claude-sonnet-5-5`), plus two re-run agents. Every result file starts with `MODEL:`; all 34 files carry `claude-sonnet-5-5`
  (batch 2 wrote it as "Claude Sonnet 5.5 (claude-sonnet-5-5)").
- **Batches (English, `evals.json` order from the todo, 53 ids, each exactly once):** 1 `a1 s0a a2 a3 a4 a5 s0b b1` ·
  2 `b2 c1 c2 c3 o2 o3 d1 e1` · 3 `f1 g1 h1 i1 j1 k1 k2 l1` · 4 `m1 n1 o1 p1 q1 r1 t1 u1` · 5 `sc1 dr1 da1 dg1 kw1 v1 x1` ·
  6 `y1 z1 w1 w2 w3 w4 fa1` · 7 `ter1 al1 ar1 tg1 tg2 tg3 tg4`.
- **Isolation:** a temp dir outside the repo held the 4-file install set (`SKILL.md`, `opencode-benchmarks.md`,
  `opencode-evidence.json`, `reference.md`) and `batches/batch<N>.txt` (ids and prompts only, written by
  `~/model-secici-iter38/cold_run_todo.py --materialize`). Turkish: a second temp dir with only `instructions.tr.md` and
  `tr-<N>.txt`. Agents wrote `eval-<id>.txt` first, then reported only the output lines; results were copied here afterwards.
- **Turkish ids (24):** `c2 c3 d1 g1 i1 j1 k1 k2 | l1 p1 t1 sc1 dr1 da1 dg1 v1 | z1 w1 w2 w3 fa1 ar1 tg1 tg2`.
- **Re-runs:** each failing eval once in a new fresh agent (English `o2 w3 tg3 tg4` in `rerun/`; Turkish `c2 p1 w3 tg1 tg2` in
  `tr-router/rerun/`; `j1` and the `/fast` omissions were not re-run).
- **`/fast` grading copies:** `tr-router/fast-copies/` holds copies of the raw Turkish files with the declared `⚡ Claude /fast
  available (2.5x faster, 2× price).` line appended **only** to the eight files whose sole raw failure was that missing line
  (`d1 i1 t1 sc1 v1 w2 fa1 ar1`; `i1` also gets ` Opus 4.8 fast mode ends 30 Nov 2026.`). A blanket append is wrong: `dr1 da1 dg1`
  forbid the line (Sonnet 5.5 has none). Raw files are untouched.

## English batches (first pass)

| batch | ids | first pass |
|---|---|---|
| 1 | a1 s0a a2 a3 a4 a5 s0b b1 | 8/8 |
| 2 | b2 c1 c2 c3 o2 o3 d1 e1 | 7/8 (`o2`) |
| 3 | f1 g1 h1 i1 j1 k1 k2 l1 | 8/8 |
| 4 | m1 n1 o1 p1 q1 r1 t1 u1 | 8/8 |
| 5 | sc1 dr1 da1 dg1 kw1 v1 x1 | 7/7 |
| 6 | y1 z1 w1 w2 w3 w4 fa1 | 6/7 (`w3`) |
| 7 | ter1 al1 ar1 tg1 tg2 tg3 tg4 | 5/7 (`tg3`, `tg4`) |

## TG1 table

| eval | what it tests | run 1 | run 2 | result |
|---|---|---|---|---|
| `tg1` (EN) | cold run on fresh Sonnet 5.5 subagents | `Claude: ✅ RECOMMENDED AI · Sonnet 5.5 · effort: high` / `OpenCode: use Claude — Go serves Claude Haiku 5.5 only, so no Sonnet 5.5 subagent can start.` | n/a | **pass** |
| `tg2` (TR prompt, EN skill) | same, Turkish prompt | identical to `tg1` | n/a | **pass** |
| `tg1` (TR mirror) | same, mirror file | `use Claude — … Haiku 5.5 only` but `effort: medium` (golden `high`) | pass (`high`) | N (D=1 vs D=2) |
| `tg2` (TR mirror) | same | same as `tg1` run 1 | pass | N |
| `tg3` (EN) | gate must NOT fire (file about Claude) | gate quiet; Sonnet 5.5 `medium`, DeepSeek `low` + GLM-5.3-Flash `low` (golden: `high`, DeepSeek `max` + MiMo-V2.6-Pro) | same | gate quiet both runs; golden corrected (G) |
| `tg4` (EN) | gate must NOT fire (SDK script elsewhere) | gate quiet; Haiku 5.5 `medium`, DeepSeek + GLM-5.3-Flash `low` | gate quiet; Sonnet 5.5 `medium`, same pair | gate quiet both runs; golden corrected (G) |

**False positives:** none. No output of any pass or re-run contains `use Claude` where its golden has none; every golden with
`use Claude` (`i1 k1 k2 l1 tg1 tg2`) got it. **Caveat:** the English `tg1`/`tg2` outputs are word-for-word the worked example's
OpenCode line in SKILL.md (the agent copied it), so they test the example more than the rule; the Turkish agents wrote their own
reason line in both runs and fired the gate.

## Every failure

| id | run 1 | run 2 | class | action |
|---|---|---|---|---|
| `o2` (EN) | Claude Sonnet 5.5 `medium`, pair Flash `low` (agent scored D=1) | pass (D=2, Sonnet 5.5 `high`, Hy4 `#1`) | N | none |
| `tg3` (EN) | Sonnet 5.5 `medium`, DeepSeek/GLM-5.3-Flash `low` (D=1) | same | **G** | golden corrected, see below |
| `tg4` (EN) | Haiku 5.5 `medium` (agentic-code tag wrongly allowed Haiku), Flash pair `low` | Sonnet 5.5 `medium`, Flash pair `low` | **G** (run 1 Haiku is N) | golden corrected, see below |
| `w3` (EN) | badge on Claude †, Argon `#1` | same | **A** | wording proposed, rule not edited |
| `c2` (TR) | badge on OpenCode, Hy4 `#1` (golden: Claude badge, MiMo `#1`, Hy4 `#2`) | same | **A** | wording proposed |
| `p1` (TR) | badge on OpenCode (A1-OC list vs badge table) | badge on Claude, but `Evidence` says `low-confidence` with no dagger | **A** | wording proposed |
| `w3` (TR) | badge on Claude † | same | **A** | same as EN `w3` |
| `tg1`, `tg2` (TR) | `effort: medium` | pass | N | none (see TG1 table) |
| `j1` (TR) | `opusplan` not printed (declared inapplicable) | not re-run | declared omission | none |
| `d1 i1 t1 sc1 v1 w2 fa1 ar1` (TR) | only the `/fast` line missing (`i1`: also the Opus 4.8 end-date) | not re-run | known omission | none |

### G: `tg3` and `tg4` goldens (derived at D=2 by the iteration-38 author)

Re-derivation from the rule text, by rule id:

- **`tg3`**: Step 3 D table, Writing/analysis column: `1` = "Simple summary/draft", `2` = "Multi-source synthesis report". A single SKILL.md
  has no sources to synthesise; the Step 3 header says "When in doubt, round down". `D = 1`. Capability `knowledge-work`, so H1 excludes
  Haiku 5.5 (H1 admits `D = 1` only for instruction-following, latency-volume or no fitting tag) → Sonnet 5.5, effort `medium`
  (precedent: golden `a3`, a D=1 knowledge-work memo). Step 4-OC row "any tag, `D ≤ 1`" → DeepSeek V4.1 Flash `low` `#1`,
  GLM-5.3-Flash `low` `#2`; DeepSeek keeps its auto-line; no dagger. TG1 does not fire either way.
- **`tg4`**: Step 3 D note: "How many independent design decisions are left to the implementer? One reasonable approach → D=1."
  A single-file script with a retry on 429 is that. `D = 1`, `agentic-code` → H1 excludes Haiku 5.5 (the tag is not one of the three
  admitted) → Sonnet 5.5 `medium`; same "any tag, `D ≤ 1`" row → Flash pair at `low`.
- Corrected in `evals/routing/evals.json` (`tests_rule` says so); both fresh agents agreed on the output in both runs. The corrected
  goldens grade the re-run files `tg3` and `tg4` as pass.

### A: `w3` (EN and TR; both runs both languages)

Same ambiguity as iteration-37, now reproduced in English too (four of four fresh runs put the badge on Claude).

- Pool row (SKILL.md Step 4-OC, `research-synthesis`): "At `D = 3` / `R = 3` Argon is `#1` (GM1, NC1 only)" with BD1 → a lean to OpenCode †.
- Badge table (Step 5, `research-synthesis`, `R = 3`): "Sonnet 5.5 … leads MiMo-V2.6-Pro … one benchmark, a lean to Claude" — it names MiMo,
  not Argon, and v1 and v1.1 are not comparable → Claude †.
- Proposed wording (≤ 40 words), appended to the badge-table cell: "When NC1 puts Gemini 4 Argon at `#1` here, the badge compares Claude with Argon on
  AA-Omniscience v1 (Sonnet 5.5 32 / 47% vs Argon 42 / 15%): a lean to OpenCode †, not to Claude."

### A: `c2` (TR, two of two runs; iteration-37 also failed once)

Both Turkish agents tagged the prompt `agentic-code` only (Hy4 `#1`, badge OpenCode †); the English agent tagged `deep-reasoning` + `terminal-tool` and passed.

- Step 2: "Pick the **one or two dominant** tags." and D3DIAG: "Diagnosis that bisects, reproduces or runs the system drives the artefact and stays on the flagship list."
- Reading 1: bisecting 180 services is tool work → one tag (`agentic-code`), badge OpenCode † (Hy4 rows are n/p). Reading 2: an adversarial `D = 3`
  diagnosis is `deep-reasoning` **and** the artefact-driving tag → two tags, the deep-reasoning cell decides the badge (Claude), `#1` from that row (MiMo), `#2` Hy4 (PO1).
- Proposed wording (≤ 40 words), added to D3DIAG: "An adversarial `D = 3` diagnosis carries `deep-reasoning` as a dominant tag, with `agentic-code` or `terminal-tool` when it bisects or runs the system; the `D = 3` deep-reasoning cell then decides the badge."

### A: `p1` (TR; EN passed)

- A1-OC: "After a shortfall at `D ≥ 2` the badge goes to Claude whenever the dominant capability has a Claude cell anywhere in the badge table — `agentic-code`, `terminal-tool`, `deep-reasoning`, `knowledge-work`".
- The badge table row for `agentic-code`, `terminal-tool` reads **OpenCode †** in all four columns — it has no Claude cell.
- Reading 1: the named list is authoritative (badge to Claude, golden). Reading 2: the condition governs, `agentic-code` has no Claude cell, so the badge stays on OpenCode.
  Run 1 took reading 2; run 2 took reading 1 but wrote `low-confidence` on a Claude-badge line (no dagger).
- Proposed wording (≤ 40 words), replacing the list: "After a shortfall at `D ≥ 2` the badge goes to Claude for `agentic-code`, `terminal-tool`, `deep-reasoning` and `knowledge-work` — even where the badge table shows OpenCode † — and `Evidence:` carries no `low-confidence`."

## Files

`eval-<id>.txt` English first pass (53) · `grading.json` (regenerated against the corrected goldens: 50/53; against the original goldens it was 49/53) · `rerun/` English re-runs (`o2 w3 tg3 tg4`) with `grading.json`
(graded against the corrected goldens; 49 other ids show "no output") · `tr-router/` Turkish raw outputs (24) and `grading.json` ·
`tr-router/fast-copies/` grading copies with the `/fast` line and `grading.json` · `tr-router/rerun/` Turkish re-runs (`c2 p1 w3 tg1 tg2`).
