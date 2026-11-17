# iteration-32 cold-agent run (17 Nov 2026)

Full regression set, 46 prompts, graded by `evals/routing/grade_routing.py` (regex, no LLM).

- **Agents:** six fresh agents (subagent sessions, session default model class). Each read only
  `skill/SKILL.md` directly (the `Skill` tool was not used, per evals/README.md) and routed a batch of
  6–8 prompts, writing the raw output lines to `eval-<id>.txt`.
- **Model-class deviation.** The earlier iterations ran fresh **sonnet** agents. This environment offers
  no Claude Sonnet to subagents (`opencode.models` lists only `opencode-go/claude-haiku-5-5` for Claude);
  every batch ran on the session's default model class. Flagged in evals/README.md and the PR.
- **First pass: 42/46.** Failures (all cold-agent reading misses; `--selftest` confirms the goldens are
  self-consistent): `c2` (Claude line `Sonnet 5.5` instead of Opus 5.5 `xhigh`), `j1` (opusplan plan
  effort `xhigh` instead of `max`), `u1` (badge on Claude instead of OpenCode), `sc1` (spurious
  `ultracode` flag).
- **Re-runs (once each, fresh agent):** `c2`, `u1`, `sc1` passed immediately. `j1`'s re-run failed on the
  other limb (OpenCode `#2` Hy4 — the agent read the dominant capability as agentic-code; the eval's
  `tests_rule` pins the deep-reasoning row, `#2` MiMo-V2.6-Pro); a further single re-run passed.
- **Final: 46/46** (`grading.json` summary: passed 46, failed 0, skipped 0).

## Run history for the moved evals

| id | first pass | re-run(s) | final |
|---|---|---|---|
| c2 | FAIL (wrong Claude model) | PASS | PASS |
| j1 | FAIL (plan effort) | FAIL (#2 capability read) | PASS (3rd agent) |
| u1 | FAIL (badge side) | PASS | PASS |
| sc1 | FAIL (spurious ultracode) | PASS | PASS |

The prompts and goldens were **not** changed during the run.
