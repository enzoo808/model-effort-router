# iteration-37 cold run (20 Nov 2026)

Full 49-eval regression set after the iteration-37 changes (GLM free-twin fix, the GLM-5.3 limits window kept out of the
rules, Gemini 4 Argon's 55-day retention: eliminated on confidential work, returned only by Rule NC1; 17 goldens touched).
Graded by `evals/routing/grade_routing.py` (regex, no LLM). Branch `iteration-37-glm` at `3c76f6b`.

**English: 48/49 on the first pass; 49/49 after one re-run (`l1`, noise).**
**Turkish mirror (18 Argon-touching evals): 8/18 raw, 15/18 with the declared `/fast` line appended to the grading copies,
16/18 after one re-run (`c2`); the remaining two are `j1` (a declared omission of the mirror) and `w3` (a finding, class A).**

## Method

- **Agents:** 7 fresh Claude Sonnet 5.5 agents (Agent tool `model: sonnet`; a preflight agent returned "ready" first), seven
  evals each in `evals.json` order (49 = 7×7). The todo's suggested id layout contained ids that are not in `evals.json`
  (`s1`) and omitted others (`s0a`, `s0b`, `i1`, `k2`, `l1`, `kw1`), so the batches follow `evals.json` order instead.
- **Isolation:** a temp dir outside the repo held the 4-file install set (`SKILL.md`, `opencode-benchmarks.md`,
  `opencode-evidence.json`, `reference.md`) copied from the branch and one `batches/batchN.txt` per agent (ids and prompts
  only). Agents were told never to open the repo, `evals/`, `results/`, notes or CHANGELOG; goldens were never visible.
  Each agent wrote `eval-<id>.txt` first, then reported only the three output lines.
- **Turkish pass:** three fresh Sonnet 5.5 agents (6 evals each) read only `claude-ai/instructions.tr.md` and a prompts file
  (the iteration-36 `tr-router` method). Ids: `c2 c3 d1 g1 j1 p1 | t1 dr1 da1 dg1 v1 z1 | w1 w2 w3 fa1 ar1 sc1`.
- **Re-runs:** each failing eval once in a new fresh agent (`l1` English; `c2` and `w3` Turkish).

## English batches

| batch | ids | first pass |
|---|---|---|
| 1 | a1 s0a a2 a3 a4 a5 s0b | 7/7 |
| 2 | b1 b2 c1 c2 c3 o2 o3 | 7/7 |
| 3 | d1 e1 f1 g1 h1 i1 j1 | 7/7 |
| 4 | k1 k2 l1 m1 n1 o1 p1 | 6/7 (`l1`) |
| 5 | q1 r1 t1 u1 sc1 dr1 da1 | 7/7 |
| 6 | dg1 kw1 v1 x1 y1 z1 w1 | 7/7 |
| 7 | w2 w3 w4 fa1 ter1 al1 ar1 | 7/7 |

Several agents copied a worked example for the matching prompt (`a1`, `s0a`, `b1`, `d1`, `f1`, `h1`, `i1`, `z1`), so
those evals test the example more than the rules; `u1` was adapted from the deck example.

## Turkish pass

| batch | raw | with `/fast` line appended | after re-run |
|---|---|---|---|
| 1 (`c2 c3 d1 g1 j1 p1`) | 3/6 | 4/6 (`c2`, `j1`) | 5/6 (`j1`) |
| 2 (`t1 dr1 da1 dg1 v1 z1`) | 4/6 | 6/6 | 6/6 |
| 3 (`w1 w2 w3 fa1 ar1 sc1`) | 1/6 | 5/6 (`w3`) | 5/6 (`w3`) |

The `/fast` speed line is a declared omission of the mirror (Claude.ai has no `/fast`). Eight raw failures were that one
line (`c2 d1 t1 v1 w2 fa1 ar1 sc1`); the four known ones are `fa1 c2 sc1 ar1`, and `d1 t1 v1 w2` fail for the same reason
(they were not in the iteration-36 Turkish run). Grading copies with the line appended are in `tr-router/grading-with-fast-line.json`;
the raw files are untouched. `j1` expects `opusplan`, which the mirror declares not applicable to Claude.ai
(`instructions.tr.md`, "`opusplan` — BU BAĞLAMDA GEÇERLİ DEĞİL"); the agent printed Opus 5.5 `max`, as the mirror says.

## Every failure

| id | run 1 | run 2 | class | action |
|---|---|---|---|---|
| `l1` (EN) | Claude line Haiku 5.5 `low`, expected Sonnet 5.5 `medium` (agent scored D=0 / H1; the prompt's "same documented click-through I run every month" pins D=1) | pass (Sonnet 5.5 `medium`, OpenCode declines on the computer-use gate) | N | none |
| `c2` (TR) | badge on the OpenCode line (agent weighed the agentic-code † cell above the deep-reasoning direction) | pass once the `/fast` line is appended (Claude badge, Opus 5.5 `xhigh` · ultracode) | N | none |
| `d1 t1 v1 w2` (TR) | only the `/fast` line missing | not re-run | known omission | none (see above) |
| `fa1 sc1 ar1` (TR) | only the `/fast` line missing | not re-run | known omission | none |
| `j1` (TR) | `opusplan` not printed (mirror declares it inapplicable) | not re-run | declared omission | none |
| `w3` (TR) | badge on Claude (worked example copied for Claude and Evidence lines; OpenCode line re-derived with Argon `#1`) | same: badge on Claude, no copy, via the badge-table cell | **A** | proposed wording below; rules not edited |

### `w3`, rule ambiguity (A)

English `w3` passed in this run (OpenCode †, Argon leading Sonnet 5.5 on Omniscience v1) and the golden follows that reading,
so the golden is not wrong; the same two sentences give two readings.

- Pool row (SKILL.md Step 4-OC, `research-synthesis`): "At `D = 3` / `R = 3` Argon is `#1` (GM1, NC1 only): AA-Omniscience v1
  index 42, hallucination 15% (Sonnet 5.5 32 / 47%)". With BD1 ("at R = 3, a single admissible measurement still decides it")
  this reads as a lean to Argon, so the badge goes to OpenCode †.
- Badge table (Step 5, `research-synthesis`, `R = 3`): "Sonnet 5.5 19 / 21 leads MiMo-V2.6-Pro −4.5 / 60.2% on both measures —
  one benchmark, a lean to Claude". It names MiMo as the comparator, says nothing about an Argon `#1`, and v1 and v1.1 are not
  comparable, so a fresh agent (twice, in Turkish) keeps **Claude †** and ignores the Argon figures.

The mirror carries both sentences verbatim (`instructions.tr.md` lines 139 and 620), so this is not a translation gap.
Proposed wording (≤ 40 words), appended to the badge-table cell: "When NC1 puts Gemini 4 Argon at `#1` here, the badge compares
Claude with Argon on AA-Omniscience v1 (Sonnet 5.5 32 / 47% vs Argon 42 / 15%): a lean to OpenCode †, not to Claude."

## Files

`eval-<id>.txt` and `grading.json`: English first pass. `rerun-en/eval-l1.txt`: English re-run (graded PASS).
`tr-router/`: Turkish raw outputs, `grading.json` (raw) and `grading-with-fast-line.json`; `tr-router/rerun/`: `c2` and `w3` re-runs.

## Checks (all green on this branch)

`grade_routing.py --selftest` 49/49 · `check_policy_sync.py` · `check_opencode_pool.py` · `check_examples.py` ·
`check_readme_facts.py` · `check_mirror_rules.py`. No golden or rule file was changed in this step.
