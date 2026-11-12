# Contributing

Thanks for helping. This project has two kinds of change and they have different bars.

## 1. Data corrections (model specs, prices, effort defaults, safety behaviour)

Very welcome. Requirements:

- **Cite the primary source.** `platform.claude.com`, `openai.com`, or an
  official changelog — not an aggregator/SEO blog. If only a secondary source
  exists, say so and it will be labelled "unverified" in `skill/reference.md`,
  the same as the existing hedged claims.
- Update the number everywhere it is stated: `skill/opencode-evidence.json` (the
  machine-readable record the checks read), `skill/opencode-benchmarks.md` (the
  per-model write-up), `skill/reference.md` (Claude prices and limits) and anywhere
  `skill/SKILL.md` restates it. Then run `python scripts/check_opencode_pool.py`: it
  recomputes tasks per month from the Arena costs and fails if a routing row leaves
  the top 4 of the independent-evidence consensus.
- **Before adding a number, check whether it is actually a new measurement.** If
  two vendors publish the same figure to the decimal, that is one number re-cited,
  not corroboration — say so in the write-up and do not let it count twice.
- **Evidence needs methodology, not just a score.** Name the benchmark, its
  version, the harness, the effort and the date next to the number. Write `n/p`
  when it isn't published — never guess it, and never interpolate a score between
  effort levels.
- **Only published dispersion may set a direction.** A confidence interval, a
  standard error, repeated-trial variance, or a practical-significance threshold
  the benchmark's *owner* publishes. Nothing else — and specifically **not a
  fraction of the roster's observed score spread**, which reads as statistics and
  is not one. A comparison with no published dispersion sets no direction however
  large its gap looks; the router falls through to efficiency (Rule BD1).
- **A benchmark that cannot separate the candidates does not belong in a rule.**
  If the frontier clusters within a point or two (Terminal-Bench 2.1 is saturated
  for this reason), record the row with a note instead of reading a ranking off it.
- If it's a Turkish/English README-visible fact, update `README.md` and
  `README.tr.md`. `scripts/check_readme_facts.py` fails CI when a count, the pool
  size, the iteration or a tier table in the docs disagrees with the data.

## 2. Routing-rule changes

Higher bar, because the whole point of the project is a stable, tested decision
procedure.

1. State the rule change and the real prompt(s) that motivated it.
2. Add or update the relevant eval in `evals/routing/evals.json`
   (`expected_claude` / `expected_opencode` — `#1 <model> · effort: <e> · #2 <model> · effort: <e>`,
   or a decline — / `expected_recommended` (`claude` | `opencode`), plus
   `expected_low_confidence` where the row carries a dagger, `expected_notes` /
   `forbidden` for the auto-added lines, a `golden_output`, or `blocked: true`).
3. Run it with **fresh/cold agents** (a subagent or a new conversation that
   reads `skill/SKILL.md` directly — *not* the `Skill` tool, which caches) and
   save the raw outputs under `evals/routing/results/iteration-<N>/`. Keep only
   the latest iterations in the tree; older runs stay in git history.
4. `python evals/routing/grade_routing.py --results-dir evals/routing/results/iteration-<N>`
   must be green (`--selftest` first, to prove the grader and goldens agree).
5. **Mirror the rule into `evals/policy/routing_policy.json` in the same commit** —
   the rule block text (verbatim), the pool, the Step 4-OC rows, the badge table —
   and bump `policy_version` + the `<!-- routing-policy-version: ... -->` marker in
   `skill/SKILL.md` if the rule set is a new iteration. Then run:
   ```
   python scripts/check_policy_sync.py
   python scripts/check_opencode_pool.py
   python scripts/check_examples.py
   ```
   `check_examples.py` fails if a worked example in `SKILL.md` contradicts the
   golden it matches (a shipped example missing a required `low-confidence`
   marker, wrong badge side, wrong effort). `check_policy_sync.py` verifies each
   `<!-- rule:ID -->` block in `SKILL.md` matches the canonical text in
   `routing_policy.json` `rule_blocks` **verbatim** — edit the block and the
   mirror together — and rejects any `$<digit>` / `$ARGUMENTS` in `SKILL.md`
   (Claude Code substitutes them: write `USD 2`, never `$2`).
   `check_opencode_pool.py` fails if the roster, a Step 4-OC row, a badge row or an
   example OpenCode line stops matching the mirror, if a dominated model is
   emitted, or if a USD 15-cap model is emitted at `low` (Rule CAP1).
   The mirror and the shipped skill once drifted a whole iteration apart, which
   meant an audit was certifying a policy nobody could run — these guards fail if
   either file moves without the other.

   *(The Codex-era reachability audit — corpus, matrix, flip review — simulated the
   retired Codex arm and was removed from the tree; the last commit that has it is
   `7c24c81`. An OpenCode reachability audit is open work.)*
6. If the rule is benchmark-derived, add or update the anchor in
   `skill/opencode-evidence.json` and its write-up in `skill/opencode-benchmarks.md`,
   then run:
   ```
   python scripts/check_opencode_pool.py
   python scripts/derive_opencode_rows.py
   ```
   Read the consensus output even when the check passes: if a capability's lead
   rests on one anchor, or on vendor-reported rows, the rule needs a
   `low-confidence` marker, not a stronger claim.
7. Mirror the change into `claude-ai/instructions.tr.md` (the no-code-execution
   fallback), except the Claude Code-only parts (`opusplan`, the `⚡ Claude /fast`
   speed line, the `/model opus` alias rule) — that file has a footer listing its
   deliberate differences.
8. Re-run `.\build-claude-ai-zip.ps1` at release time — `dist/` is git-ignored; the zip is never committed.
9. If `docs/social-preview.html` changed, re-render the PNG in the same commit:
   `.\scripts\render-social-preview.ps1`. A stale PNG is a wrong screenshot of the
   product on every link preview, and nobody notices because nobody opens the HTML.

`evals/README.md` has the full run history and the reasoning behind past rule
changes — read it before proposing one.

**Trigger eval** (`evals/trigger/`) is separate: it only tests whether the
`description:` frontmatter fires at the right times, so re-run it *only* when
that line changes — `python evals/trigger/run_trigger.py --skill-path skill
--out evals/trigger/results/<label>.json` (a quota cost: one `claude -p` per
query).

## 3. Turkish parity

The skill body and README are English. `README.tr.md`, `claude-ai/instructions.tr.md`
and the `tests_rule` notes in `evals/routing/evals.json` are
Turkish (the project's original working language). When you change a rule, keep
`README.tr.md` and `claude-ai/instructions.tr.md` in sync — or flag in the PR that
they lag, so a Turkish speaker can follow up.

## Style

- **Two layers, and only the first is read at runtime.** `SKILL.md` carries
  classification, the routing algorithm, the compact benchmark-derived rules and
  the recommended-AI logic. The audit data (`opencode-evidence.json`,
  `opencode-benchmarks.md`, and `reference.md` with its prose, sourcing, conflicts
  and history) is read when changing a rule. Runtime token cost must not grow:
  never make the router load the data files to answer a routing question.
- Every effort-level or model claim needs either a citation or an explicit
  "unverified" label. No confident numbers without a source.
- When in doubt about a routing call, the project rounds **down** (quota-aware).
