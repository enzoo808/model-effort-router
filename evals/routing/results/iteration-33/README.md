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

## Two-tag fix and its re-run (`two-tag/`)

The `e1` finding led to a PO1 clause: with two dominant tags whose badge cells both fall to efficiency, the more
cap-efficient of the two rows' `#1`s goes first (DeepSeek 714 vs GLM-5.3-Flash 429 tasks/mo). One fresh Claude Sonnet 5.5
agent then routed `e1`, the other two-tag evals (`c2`, `d1`) and the reordered rows (`m1`, `x1`, `r1`) once
(`two-tag/grading.json`): **5/6**.

- `e1`, `d1`, `m1`, `x1` and `r1` pass.
- `c2` **failed** on the badge: Claude line Opus 5.5 `xhigh` · ultracode and the Argon · Hy4 pair are correct, but the
  badge sits on OpenCode, although its own Evidence says Opus 5.5 leads Argon (TB 4.0 59.6 vs 57.1, HLE-Diamond 64.0
  vs 56.7). The new clause orders the pair only and never moves the badge. Not re-run (no third agent). `c2` is now an
  open finding: it missed in iteration-32's first pass (Claude model), in this first pass (D=2) and here (badge), each
  time on a different limb, and passed once in between.

The prompts and goldens were **not** changed during the runs.
