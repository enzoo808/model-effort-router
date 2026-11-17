# iteration-33 cold-agent run (17 Nov 2026)

This is the full regression set, 48 prompts, graded by `evals/routing/grade_routing.py` (regex, no LLM).

- **Agents:** six fresh agents of the Claude Sonnet 5.5 class (the class used up to iteration-31). Each one read
  only `skill/SKILL.md` directly; the `Skill` tool was not used. Each got a batch file holding only ids and prompts
  (eight prompts, in `evals.json` order) and wrote the raw output lines to `eval-<id>.txt`.
- **First pass: 46/48** (`grading.json`). The two failures:
  - `c2`: the Claude line was `Sonnet 5.5 · effort: high · ultracode` (the task was scored D=2, not D=3). It is the
    same eval that missed iteration-32's first pass on the Claude model.
  - `e1`: the OpenCode `#1` was GLM-5.3-Flash, not DeepSeek V4.1 Flash. The two-tag pick put the `long-context`
    row's `#1` ahead of the `knowledge-work` row's.
- **Re-runs** (`rerun/`, one fresh agent per failing eval, once each; the other 46 show as skipped in
  `rerun/grading.json`): `c2` **passed** (Opus 5.5 `xhigh` · ultracode; Argon · Hy4). `e1` **failed again** with the
  same reading (GLM-5.3-Flash · DeepSeek).
- **Finding (not re-run a third time):** for `e1`, Step 4-OC's two-tag rule ("`#1` from the row whose tag decided
  the badge, else the first named") does not settle the order when both dominant tags' badge cells fall to
  efficiency. That is the case here: knowledge-work and long-context are both OpenCode † at D=2. Neither row
  changed in iteration-33.
- Every eval that iteration-33 added or moved passed on the first pass: `al1`, `ar1`, `m1`, `x1`, `r1`, `w4`, `j1`.

The prompts and goldens were **not** changed during the run.
