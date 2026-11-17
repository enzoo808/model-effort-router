# iteration-34 cold-agent run (17 Nov 2026)

The full regression set, 49 prompts (the 48 of iteration-33 plus `dg1`), graded by `evals/routing/grade_routing.py`
(regex, no LLM). `dg1`, the counter-eval to `c2` (a read-only D=3 diagnosis stays Sonnet 5.5 `xhigh`, OpenCode †), has
an expectation derived from the rules, not from a cold-agent golden; it was run once on its own fresh agent and passed.
The prompts and goldens were not touched during the runs.

- **Agents:** six fresh agents of the Claude Sonnet 5.5 class (the subagent model reports `claude-sonnet-5-5`). Each read
  only `skill/SKILL.md` directly (no `Skill` tool, no other repo file). Each got a batch file holding only ids and
  prompts (eight, in `evals.json` order) and wrote the raw output to `eval-<id>.txt`.
- **First pass: 47/48 on the 48 original prompts, 48/49 with `dg1`** (`grading.json`). `c2` **passed**. The one failure:
  - `a5`: the Claude line was `Sonnet 5.5 · effort: high` (expected `medium`); the 200-review tone batch was scored D=2,
    not D=1. `a5` passed in iteration-33 and the iteration-34 edit does not touch its rules.
- **Re-run** (`rerun/`, one fresh agent, once): `a5` **failed again** (`Sonnet 5.5 · effort: high`; OpenCode `#1`
  MiMo-V2.6-Pro, a different pair from the first run, so the badge reasoning moved as well). Not re-run a third time:
  an open finding, see the CHANGELOG.

## The `c2` baseline and its after-fix run (work item 1 and 2)

Three independent fresh agents answered `c2` alone before and after the D3DIAG clarification (they saw the skill file
and the prompt, never the golden, and also stated their badge reason):

| | Claude line | badge | OpenCode `#1` · `#2` |
|---|---|---|---|
| before, agent 1 | Sonnet 5.5 `xhigh` · ultracode | OpenCode | Argon · MiMo-V2.6-Pro |
| before, agent 2 | Sonnet 5.5 `xhigh` · ultracode | OpenCode | Argon · MiMo-V2.6-Pro |
| before, agent 3 | Opus 5.5 `xhigh` · ultracode | **Claude** | Argon · MiMo-V2.6-Pro |
| after, agent 1 | Opus 5.5 `xhigh` · ultracode | **Claude** | Argon · MiMo-V2.6-Pro |
| after, agent 2 | Opus 5.5 `xhigh` · ultracode | **Claude** | Argon · MiMo-V2.6-Pro |
| after, agent 3 | Opus 5.5 `xhigh` · ultracode | **Claude** | Argon · Hy4 |

Badge: Claude 1/3 before, 3/3 after. All six agents said MECH1 does not apply (the ultracode here comes from UC1's
width limb, not from `O = high`). The two "before" misses read the task as analysis (so the line stays Sonnet 5.5 and
the "`D = 3` analysis on a flagship tag" paragraph sends the badge to OpenCode); the third read it as driving the
artefact. The rules did not say which a bisect-and-judge diagnosis is. **Still splitting after the fix:** the OpenCode
`#2` (Hy4 in one agent, MiMo-V2.6-Pro in five of six; the golden says Hy4). That limb is the two-tag pair rule and it
split in the baseline too; it is left open (no fourth agent).

## `a5` A/B (follow-up check)

`a5` missed twice (`high` for `medium`; the re-run also picked a different OpenCode pair, MiMo-V2.6-Pro · GLM-5.3-Flash,
the D=2 reading). To tell a regression from an old flutter, the `cbfe614` skill files and this iteration's were
exported to a scratch folder and three fresh agents each routed `a5` alone (goldens never shown; each also stated its D
score, which the original runs did not, so the A/B is not identical to them). Result: **all six** gave
`Sonnet 5.5 · effort: medium` with DeepSeek V4.1 Flash `low` · MiMo-V2.6-Flash `default`, D=1 (one noted that D=2 would
make it `high` / `max`). Neither version fell, so no regression is shown and the prompt was not changed; the two
earlier misses stay unexplained and `a5` is carried as an open, intermittent finding.
