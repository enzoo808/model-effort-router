# Contributing

Thanks for helping. This project has two kinds of change and they have different bars.

## 1. Data corrections (model specs, prices, effort defaults, safety behaviour)

Very welcome. Requirements:

- **Cite the primary source.** `platform.claude.com`, `openai.com`, or an
  official changelog — not an aggregator/SEO blog. If only a secondary source
  exists, say so and it will be labelled "unverified" in `skill/reference.md`,
  the same as the existing hedged claims.
- Update the number in **both** `skill/reference.md` and anywhere `skill/SKILL.md`
  restates it.
- If it's a Turkish/English README-visible fact, update `README.md` and
  `README.tr.md`.

## 2. Routing-rule changes

Higher bar, because the whole point of the project is a stable, tested decision
procedure.

1. State the rule change and the real prompt(s) that motivated it.
2. Add or update the relevant eval in `evals/routing/evals.json` (dual-format:
   `expected_claude` / `expected_codex`, or `blocked: true`).
3. Run it with **fresh/cold agents** (a subagent or a new conversation that
   reads `skill/SKILL.md` directly — *not* the `Skill` tool, which caches) and
   save the raw outputs under `evals/routing/results/iteration-<N>/`.
4. `python evals/routing/grade_routing.py --results-dir evals/routing/results/iteration-<N>`
   must be green.
5. Mirror the change into `claude-ai/instructions.tr.md` (the no-code-execution
   fallback), except the Claude Code-only parts (`opusplan`, the `⚡ Fast Mode`
   speed line, the `/model opus` alias rule) — that file has a footer listing its
   deliberate differences.
6. Re-run `.\build-claude-ai-zip.ps1`.

`evals/README.md` has the full run history and the reasoning behind past rule
changes — read it before proposing one.

**Trigger eval** (`evals/trigger/`) is separate: it only tests whether the
`description:` frontmatter fires at the right times, so re-run it *only* when
that line changes — `python evals/trigger/run_trigger.py --skill-path skill
--out evals/trigger/results/<label>.json` (a quota cost: one `claude -p` per
query).

## 3. Turkish parity

The skill body and README are English. `README.tr.md`, `claude-ai/instructions.tr.md`,
`evals/history.tr.md` and the `tests_rule` notes in `evals/routing/evals.json` are
Turkish (the project's original working language). When you change a rule, keep
`README.tr.md` and `claude-ai/instructions.tr.md` in sync — or flag in the PR that
they lag, so a Turkish speaker can follow up.

## Style

- `SKILL.md` stays short; tables and sourcing live in `reference.md`.
- Every effort-level or model claim needs either a citation or an explicit
  "unverified" label. No confident numbers without a source.
- When in doubt about a routing call, the project rounds **down** (quota-aware).
