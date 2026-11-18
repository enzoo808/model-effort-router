# iteration-35 cold-agent run (17 Nov 2026)

The full regression set, 49 prompts, graded by `evals/routing/grade_routing.py` (regex, no LLM): **49/49 on the first
pass** (`grading.json`). No re-runs were needed.

- **Agents:** seven fresh Claude Sonnet 5.5 agents (the subagent model reports `claude-sonnet-5-5`), seven prompts each,
  `evals.json` order. Each read only `skill/SKILL.md` and a batch file holding ids and prompts (goldens never shown) and
  wrote the raw output to `eval-<id>.txt`.
- **Caveat:** all seven ended on an API 5-hour rate-limit error after writing their files, so none returned a final
  report; the 49 files are complete and gradeable, but no agent's own account of the run exists.

## The `c2` pair slot (work item 1 and 2)

Three fresh agents answered `c2` alone before the fix (`374d794` files) and three after; they saw the skill file and the
prompt, never the golden, and stated which rule produced each OpenCode slot.

| | tags | Claude line | badge | OpenCode `#1` · `#2` | `#2` reason |
|---|---|---|---|---|---|
| before 1 | deep-reasoning + terminal-tool/agentic-code | Opus 5.5 `xhigh` · ultracode | Claude | Argon · Hy4 | two-tag line, deep-reasoning decided the badge |
| before 2 | agentic-code + deep-reasoning | same | Claude | Argon · Hy4 | GM1 on the agentic-code row + the `d1` worked example |
| before 3 | agentic-code + deep-reasoning | same | Claude | Argon · Hy4 | said the two-tag line read literally gives MiMo-V2.6-Pro; followed GM1 + `d1` |
| after 1 | agentic-code + deep-reasoning | same | Claude | Argon · Hy4 | new PO1 sentence (109 vs 94 tasks/mo) |
| after 2 | terminal-tool + deep-reasoning | same | Claude | Argon · Hy4 | new PO1 sentence |
| after 3 | terminal-tool + deep-reasoning | same | Claude | Argon · Hy4 | new PO1 sentence |

Result: 3/3 before, 3/3 after. The iteration-34 split (MiMo-V2.6-Pro in 5 of 6 agents) did not reproduce, so counts do
not show an improvement. What the runs do show: all three "before" agents named the same collision (the two-tag line
against GM1, with no rule for which row decided the badge when both cells are Claude); all three "after" agents
resolved it by citing the new sentence. The orchestration tag, the prompt's wording and PO1's old two-tag clause (which
covers only badge cells that both fall to efficiency) were not involved: nobody chose `orchestration`, and every agent
read the prompt the same way.
