# iteration-34 cold-agent run (17 Nov 2026)

The full regression set, 48 prompts, graded by `evals/routing/grade_routing.py` (regex, no LLM). No eval was added,
removed or changed; the prompts and goldens were not touched during the runs.

- **Agents:** six fresh agents of the Claude Sonnet 5.5 class (the subagent model reports `claude-sonnet-5-5`). Each read
  only `skill/SKILL.md` directly (no `Skill` tool, no other repo file). Each got a batch file holding only ids and
  prompts (eight, in `evals.json` order) and wrote the raw output to `eval-<id>.txt`.
- **First pass: 47/48** (`grading.json`). `c2` **passed**. The one failure:
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
