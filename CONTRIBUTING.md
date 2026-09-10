# Contributing

Thanks for helping. This project has two kinds of change and they have different bars.

## 1. Data corrections (model specs, prices, effort defaults, safety behaviour)

Very welcome. Requirements:

- **Cite the primary source.** `platform.claude.com`, `openai.com`, or an
  official changelog — not an aggregator/SEO blog. If only a secondary source
  exists, say so and it will be labelled "unverified" in `skill/reference.md`,
  the same as the existing hedged claims.
- Update the number in **all** of `skill/benchmarks.json` (the machine-readable
  record), `skill/reference.md`, and anywhere `skill/SKILL.md` restates it, then
  **regenerate the derived layer**:
  ```
  python scripts/compile_benchmark_frontiers.py
  python scripts/validate_benchmarks.py
  ```
  The validator fails if `skill/benchmark_frontiers.json` no longer matches the
  sha256 of `skill/benchmarks.json`, so a forgotten recompile cannot be
  committed. Never hand-edit `benchmark_frontiers.json` — it is generated.
- **Every record needs an `id`, an `evidence_class` and a `comparability_group`.**
  The class decides what the row may be used for: `model_intrinsic` (same harness
  for every model — the right input for model/effort selection),
  `ecosystem_end_to_end` (each model in its own vendor's agent — the right input
  for the `✅ RECOMMENDED AI` badge), `vendor_relative` (one vendor measuring a
  competitor — direction only), `aggregate`, `efficiency_only`. A comparability
  group *asserts* that benchmark, version, harness, tool access, scaffold and
  evaluator were constant across its rows; the validator checks the assertion.
- **Before adding a number, check whether it is actually a new measurement.** If
  two vendors publish the same figure to the decimal, that is one number re-cited,
  not corroboration — say so in `notes` and do not let it count twice.
- **Benchmark records need methodology, not just a score.** A row in
  `skill/benchmarks.json` without `harness`, `effort` and `date` cannot be
  compared with anything, so it cannot inform a rule. Leave a field `null` when
  it isn't published — never guess it, and never interpolate a score between
  effort levels.
- **A benchmark that cannot separate the candidates does not belong in a rule.**
  If the frontier clusters within a point or two, add the row with a note and put
  the benchmark on `excluded_from_direction` rather than reading a ranking off
  it. SWE-bench Verified and Terminal-Bench 2.1 are both there for this reason.
- If it's a Turkish/English README-visible fact, update `README.md` and
  `README.tr.md`.

## 2. Routing-rule changes

Higher bar, because the whole point of the project is a stable, tested decision
procedure.

1. State the rule change and the real prompt(s) that motivated it.
2. Add or update the relevant eval in `evals/routing/evals.json` (dual-format:
   `expected_claude` / `expected_codex` / `expected_recommended`, plus
   `expected_low_confidence` where the rules require a hedge, or `blocked: true`).
3. Run it with **fresh/cold agents** (a subagent or a new conversation that
   reads `skill/SKILL.md` directly — *not* the `Skill` tool, which caches) and
   save the raw outputs under `evals/routing/results/iteration-<N>/`.
4. `python evals/routing/grade_routing.py --results-dir evals/routing/results/iteration-<N>`
   must be green.
5. If the rule is benchmark-derived, add or update its entry in
   `skill/benchmarks.json` → `routing_rules` with the `evidence_ids` it rests on.
   The validator fails on a dangling id, which is what stops a rule outliving the
   number behind it. Then run:
   ```
   python scripts/validate_benchmarks.py
   python scripts/test_frontier_compiler.py
   python scripts/ablate_evidence.py
   ```
   Read the ablation even when it passes: if a capability's verdict disappears
   once vendor-run rows are dropped, the rule needs a `low-confidence` marker,
   not a stronger claim.
5. Mirror the change into `claude-ai/instructions.tr.md` (the no-code-execution
   fallback), except the Claude Code-only parts (`opusplan`, the `⚡ Fast Mode`
   speed line, the `/model opus` alias rule) — that file has a footer listing its
   deliberate differences.
6. Re-run `.\build-claude-ai-zip.ps1`.
7. If `docs/social-preview.html` changed, re-render the PNG in the same commit:
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

The skill body and README are English. `README.tr.md`, `claude-ai/instructions.tr.md`,
`evals/history.tr.md` and the `tests_rule` notes in `evals/routing/evals.json` are
Turkish (the project's original working language). When you change a rule, keep
`README.tr.md` and `claude-ai/instructions.tr.md` in sync — or flag in the PR that
they lag, so a Turkish speaker can follow up.

## Style

- **Three layers, and only the first is read at runtime.** `SKILL.md` carries
  classification, the routing algorithm, the compact benchmark-derived rules and
  the recommended-AI logic. `benchmark_frontiers.json` is the generated derived
  layer, read when auditing a rule. `benchmarks.json` is the raw evidence store,
  read when changing one. Prose, sourcing, conflicts and history live in
  `reference.md`. Runtime token cost must not grow: never make the router load
  the data files to answer a routing question.
- Every effort-level or model claim needs either a citation or an explicit
  "unverified" label. No confident numbers without a source.
- When in doubt about a routing call, the project rounds **down** (quota-aware).
