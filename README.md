# model-effort-router

**Paste a task. Get told which model and effort level to run it on — for both Claude and Codex/ChatGPT — and which of the two is actually the better fit for *that* task.** It does *not* run the task; it routes it.

Installed as a Claude Code / claude.ai skill invoked with `/model-secici`.

```
You:    /model-secici  Move the repo's auth flow to OAuth2

model-secici:
  Claude: ✅ RECOMMENDED AI · Sonnet 5 · effort: high
  Codex:  Terra · effort: xhigh
  Evidence: Agentic multi-file coding is Claude's strongest published margin
            (Terminal-Bench 4.0: Opus 5 52.3 vs Sol 37.3); Codex takes a +1
            notch to compensate.
```

The badge is **computed, not habitual** — swap the task and it moves:

```
You:    /model-secici  Label these 200 customer reviews as positive/negative

model-secici:
  Claude: Haiku 4.5
  Codex:  ✅ RECOMMENDED AI · Luna · effort: low
  Evidence: Both clear the bar for mechanical classification, and Luna runs
            ~30% faster per token at slightly lower cost per task.
```

> The skill body (`skill/SKILL.md`, plus `reference.md`, `benchmarks.json` and
> the generated `benchmark_frontiers.json`) and its output are English. It routes prompts in any language. 🇹🇷 A longer
> Turkish walkthrough of the decision logic is in **[README.tr.md](README.tr.md)**.

---

## Why this exists

The failure mode isn't picking a model that's too weak. It's **reflexively picking
the most expensive model** and burning your rate-limit window — Claude's 5-hour
quota *and* ChatGPT Plus's 3-hour / weekly windows. Those are the protected
resource, not dollars.

The decision principle, in one sentence:

> **Select the lowest-quota model × effort combination that stays on the
> task-specific capability frontier.** Prefer the stronger candidate when the
> task-relevant performance difference is meaningful; prefer the more
> token-efficient candidate when capability sits inside a defensible equivalence
> band.

Not "always cheapest". Not "always strongest". Not "highest benchmark score wins".

## What changed, and when

**iteration-17 (Phase 2)** hardened the evidence rather than the router: it went
back for the benchmark *owners*' own leaderboards, turned the path from a raw
score into a routing rule into a deterministic compiler, and measured how much of
the router's ecosystem preference rests on vendor-run numbers. One routing rule
moved — see the Astra example below. Details: **[Data honesty](#data-honesty)**.

**iteration-16 (Phase 1)** is where the benchmark-aware engine came from:

Through iteration-15 the router read a prompt's **R/D/W/C** (risk, depth, width,
context) and mapped that straight to a model and an effort level. R/D/W/C
describes *scope and stakes* very well and *nothing about what kind of ability
the work needs* — "depth 3" is equally true of a race-condition hunt, a topology
proof and a contract-conflict review, and those three want different models.

R/D/W/C is still here and still does its job. It is now one input among four:

```
prompt
  → quality gate                     (Step 0, unchanged)
  → hard gates: capability/safety/availability   (Step 1)
  → task capability profile          (Step 2, NEW)
  → R/D/W/C + scope                  (Step 3)
  → candidate model × effort, per arm (Step 4)
  → benchmark evidence · comparability · equivalence · dominance (Step 5, NEW)
  → token & quota efficiency         (Step 5c/5d, NEW)
  → cross-ecosystem comparison → ✅ RECOMMENDED AI + Evidence line (Step 6, NEW)
  → quota guards                     (Step 7)
```

The badge is **conditional on which Codex model is on the line** — a capability
can genuinely favour Claude against Sol and not against Astra:

```
You:    /model-secici  Split this 6000-file legacy Java monolith into independent services

model-secici:
  Claude: Fable 5.1 · effort: max
  Codex:  ✅ RECOMMENDED AI · Astra · effort: max
  Evidence: Capability is level against Astra (AA Terminal-Bench 4.0: Astra 59
            vs Fable 5.1 52; Coding Agent Index tied at 62), so efficiency
            decides — 27k output tokens/task vs 78k.
  Do not apply without human review.
```

Three of the new rules change real outputs, and each is asserted in the eval set:

- **`Sonnet 5 · max` is dominated.** Artificial Analysis v4.3 (one harness, all
  rungs comparable): Sonnet 5 at `max` scores **38 for $5.09/task**; Opus 5 at
  `xhigh` scores **50 for $4.88**. Stronger *and* cheaper. So escalation is now a
  **model** change, not an effort change — `Sonnet 5 → Opus 5`, at the same rung.
  The Codex mirror: `Sol · high` (42, $0.81) dominates `Terra · max` (42, $1.40),
  and `max` isn't offered on Terra at all.
- **`max` over `xhigh` buys almost nothing.** Fable 5.1 scores 53 at both rungs
  ($7.63 → $5.98); Astra 53 at both ($3.26 → $2.31); Opus 5 51 vs 50. `max` now
  requires `D=3 ∧ R=3` **and** a single indivisible novel-design or formal
  decision — not merely "hard and irreversible".
- **A computer-use gate on the Codex arm.** Astra's one clear published lead over
  Sol. It was named in the roster notes but the gate table never had the row.

## Data honesty

The rule this repo used to lead with was *"the router never selects a model from
a benchmark number."* That was the right instinct and the wrong mechanism: it
kept bad numbers out by keeping all numbers out. The replacement:

> **Evidence sets the direction and the equivalence band; the capability profile
> decides which evidence applies; efficiency breaks the ties capability leaves
> open. A leaderboard position on its own decides nothing.**

What that buys in practice:

- **Benchmarks are bound to capabilities.** A pure maths prompt gives
  Terminal-Bench, CursorBench and SWE-bench a weight of **zero**. An aggregate
  intelligence index is admitted for exactly three jobs (effort-rung comparisons
  within one model, token-load comparisons, and a last-resort tie-break marked
  `low-confidence`) and never overrides a task-specific benchmark.
- **Comparability is checked before comparing.** Two numbers count as comparable
  only when benchmark, version, harness, tool access, scaffold *and* effort
  match. Real traps already in the record: OSWorld 2.0's partial and strict
  scoring differ by ~36 points on the same model; AA index versions aren't
  comparable across versions; "agentic coding" puts Sol 15 points behind Opus 5
  on Terminal-Bench 4.0, 2.8 on CursorBench and 1 on DeepSWE.
- **No interpolation between effort rungs, ever.** Sonnet 5 at `high` and Sol at
  `xhigh` simply aren't published. They're recorded as unknown, not estimated.
- **Vendor benchmarks are used but discounted.** Anthropic's launch note measures
  GPT-5.6 Sol in Anthropic's own harness. That's direction, not a settled
  ranking, and it's labelled `vendor_run: true` in the data.
- **Conflicts are recorded, not averaged away.** The open conflicts and the
  explicit non-findings are written down in `skill/reference.md` §12.3–§12.5 —
  including that the two vendors publish Opus 5 on the same OSWorld version and
  scoring mode 5.2 points apart, and that OpenAI's and Anthropic's Terminal-Bench
  figures for the Claude models are digit-for-digit identical, which makes them
  one number re-cited rather than two runs.

Every record — benchmark, version, model, effort, harness, tool access, scaffold,
trials, dispersion, cost/task, date, source, source tier, comparability group —
is in **[`skill/benchmarks.json`](skill/benchmarks.json)**, 123 rows, `null`
wherever a figure isn't published.

### The evidence is compiled, not asserted

Three layers, and **only the first is read at runtime**:

| Layer | File | Written by | Read when |
|---|---|---|---|
| Runtime rule | `skill/SKILL.md` | a human | every route |
| Derived frontier | `skill/benchmark_frontiers.json` | the compiler — **generated** | auditing a rule |
| Raw evidence | `skill/benchmarks.json` | a human, one record per measurement | changing a rule |

```bash
python scripts/validate_benchmarks.py            # schema, groups, rule provenance, staleness
python scripts/compile_benchmark_frontiers.py    # regenerate the derived frontier
python scripts/test_frontier_compiler.py         # comparison-semantics assertions
python scripts/ablate_evidence.py                # vendor-bias measurement
python scripts/check_policy_sync.py              # SKILL.md and the policy mirror agree
python scripts/check_routing_reachability.py --check --report
python scripts/test_reachability_tool.py         # the auditor's own regression suite
```

> **What "meaningfully better" may rest on.** A published confidence interval, a
> published standard error, repeated-trial dispersion, or a practical-significance
> threshold the benchmark's owner publishes. Nothing else. Until iteration-18 the
> compiler fell back to *a fraction of the roster's observed score spread* — which
> reads as statistics and is not: spread is how far apart the models happen to
> sit, not how precisely either score was measured, and on a two-row comparison
> the spread *is* the gap. Removing it leaves `science` as the only capability
> with a certified direction; everything else is `UNRESOLVED` and falls through to
> efficiency. The directions the record points are unchanged — what is gone is the
> pretence that they were measured.

The compiler never interprets a number on its own: every threshold, grouping and
precedence weight is declared in `benchmarks.json`, and where the declared
metadata doesn't settle a comparison the answer is `UNRESOLVED` — which tells the
router to fall through to efficiency. It never averages two conflicting sources.
Two runs produce byte-identical output, and the frontier stores the sha256 of the
evidence it came from, so editing the evidence without recompiling fails the
build.

**The vendor-bias measurement is the uncomfortable one.** Re-derive the frontier
using only independent (tier B) evidence, or with vendor-measures-competitor rows
removed, and only `agentic-code` and `terminal-tool` survive. Every other
capability — Claude's lead on knowledge work and science, Codex's lead on
computer use — collapses to `UNRESOLVED`. Both sides' advantages outside terminal
work rest on one vendor's account of the other. The router doesn't paper over
that or force a balanced badge: those capabilities are marked in the rule table
and their Evidence line has to say `low-confidence`.

---

## Install

It's a [Claude skill](https://docs.claude.com/en/docs/claude-code/skills) —
four files (`skill/SKILL.md`, `skill/reference.md`, `skill/benchmarks.json`,
`skill/benchmark_frontiers.json`) in a `model-secici/` folder. Only `SKILL.md` is
read when routing; the rest are there for auditing a rule. "Installing" is just putting that folder
where Claude looks for skills.

```bash
git clone https://github.com/enzoo808/model-effort-router.git
cd model-effort-router
```

### Claude Code

**macOS / Linux:**
```bash
./install.sh
```

**Windows (PowerShell):**
```powershell
.\install.ps1
```

**Or by hand (any OS)** — the scripts just do this:
```bash
mkdir -p ~/.claude/skills/model-secici
cp skill/*.md skill/*.json ~/.claude/skills/model-secici/
```

Start a new Claude Code session, then:
```
/model-secici  <your task>
```
It also triggers on its own when you ask things like "which model should I use
for this?" or "which AI is better for this?".

Prefer it project-scoped instead of user-scoped? Put the `model-secici/` folder
under `.claude/skills/` in your repo.

### claude.ai / Claude Desktop (native custom skill)

Requires a Pro / Max / Team / Enterprise plan with **code execution** enabled.

1. Download **[`dist/model-secici.zip`](dist/model-secici.zip)** from this repo
   (open the file → *Download raw file*). Or rebuild it after edits:
   `.\build-claude-ai-zip.ps1` (Windows).
2. **claude.ai → Settings → Features → Custom Skills → Upload** → pick the zip.

It then runs in every chat, no project needed.

**No code execution?** Use the plain-text fallback in
[`claude-ai/instructions.tr.md`](claude-ai/instructions.tr.md): paste the text
below the line into a Project's *Custom instructions*. (Bound to that one
Project, and it's the Turkish variant — an English port is welcome.)

### Codex / ChatGPT

There's no skill mechanism on the Codex side — the router just produces the
`Codex:` line for you to act on. Run `model-secici` on the Claude side (or the
claude.ai fallback) and read both lines plus the badge.

---

## How it decides

| Step | What happens |
|---|---|
| **0 · Quality gate** | Four mechanical checks (rule stated by example but not generalised? silent-wrong-result risk? concrete target? two plausible readings?). If any fires → **no model, no badge, ask a clarifying question.** |
| **1 · Hard gates** | Capability / safety / availability, never traded against efficiency. Sub-second or high-volume → **Haiku** / **Luna**. Offensive security → **Opus 4.8 · xhigh** / Codex `use Claude` (or `Astra` w/ Daybreak). Biology R&D → **Fable 5.1** / Codex `unverified`. >200k context → drops Haiku. 1000+ files → **Fable 5.1** / **Astra**. ≥1M-token Codex context → **Astra**. GUI-driving is the task → **Astra**. |
| **2 · Capability profile** | Name the one or two capabilities the task actually needs — `agentic-code`, `terminal-tool`, `deep-reasoning`, `knowledge-work`, `research-synthesis`, `long-context`, `computer-use`, `science`, `workflow-automation`, `doc-data-understanding`, `parallel-independent`, `latency-volume`. This is what makes benchmark evidence applicable *or not*. |
| **3 · Score scope & stakes** | **R**isk, **D**epth, **W**idth, **C**ontext — each 0–3, each with a diagnostic question and a worked-example library. |
| **4 · Candidate model × effort** | Model ← `max(D, C)` and the capability profile — **not** risk. Flagship only at `D=3` *and* a capability on the flagship list. Effort ← `D` (`0→low · 1→medium · 2→high · 3→xhigh`). Claude modifier: **`ultracode`** — >30 min **and** 3+ different *kinds* of step feeding each other (or `W=3` ∧ `D≥2`), **and** not one indivisible chain; plus `opusplan`. Codex modifiers: **Sol Ultra** for 3+ genuinely parallel strands, and a `+1` notch for agentic multi-step coding (Terra/Sol only, never Astra, caps at `xhigh`). Third escalation rung — Opus 5 → Fable 5.1, Sol → Astra — only on a *stated* flagship-tier shortfall. |
| **5 · Evidence, equivalence, efficiency** | Check comparability. Decide "meaningfully better" from **published dispersion only** — a confidence interval, a standard error, repeated-trial variance, or a threshold the benchmark's own owner publishes. With none of those the comparison is **`UNRESOLVED`**, however large the gap looks: observed score spread is not uncertainty. Widen the bar when `R=3`. Then apply dominance: reasoning tokens → output tokens → total tokens → tokens per *successful* task → quota pressure → cost → latency. |
| **6 · `✅ RECOMMENDED AI`** | Compare the two arms in order: hard gate → task-relevant capability → benchmark confidence → near-parity → token/quota efficiency → cost → latency. Emit one badge and one `Evidence:` sentence naming at most 1–2 signals. |
| **7 · Quota guards** | `R=3` adds a human-review note (never changes the model). Escalation is a model change, not an effort change. MCP-server bloat, auto-accept, alias drift warnings. |

Two design choices carried over unchanged, because they still hold: **risk raises
human oversight, not model tier**, and **when in doubt, round down**.

---

## The rosters

**Claude (verified 10 Sep 2026):**

| Model | Role | $/Mtok in·out |
|---|---|---|
| Haiku 4.5 | speed / volume, no effort param, 200k context | $1 / $5 |
| **Sonnet 5** | daily driver, default starting point | **$2 / $10** |
| **Opus 5** | flagship — complex agentic code, enterprise | $5 / $25 |
| Opus 4.8 | legacy — kept **only** for the offensive-security gate | $5 / $25 |
| **Fable 5.1** | frontier scale, long-horizon autonomy, biology-adjacent R&D | $10 / $50 (cache reads ¼: $0.25) |
| Mythos 5.1 | = Fable 5.1 with permissive safeguards, **Project Glasswing invite only** | — |

> ⚠️ **Correction, 10 Sep 2026.** Earlier versions of this repo recorded Sonnet 5
> at **$3/$15** from 1 September, on the basis that its $2/$10 launch price was
> introductory. Anthropic **cancelled** that increase — $2/$10 is now the standard
> price. The Opus 5 : Sonnet 5 quota ratio is therefore **2.5×**, not 1.67×,
> which widens the case for staying on Sonnet 5 wherever it clears the bar.

**Codex / ChatGPT (GPT-5.6 family + GPT-6 Astra):**

| Model | Role | rough Claude analogue |
|---|---|---|
| Luna | speed / volume, cheapest. Codex CLI default | Haiku 4.5 |
| Terra | balanced daily driver | Sonnet 5 |
| **Sol** | GPT-5.6 flagship — code / science / security; the D=3 pick | Opus 5 |
| **Sol Ultra** | a Codex *mode* on Sol (Plus+): ~4 collaborating agents in parallel. Also available on Astra | stronger than Claude's `ultracode` |
| **Astra** | GPT-6 flagship (`gpt-6-astra`), 1.05M context. **Rare pick.** Gates: offensive-sec *with Daybreak*, 1000+ files, ≥1M-token context, GUI-driving — plus two narrow non-gate routes, Rule E4 (where `Sol · max` would be emitted on agentic-code / terminal-tool) and a stated flagship-tier shortfall | Opus 5 / Fable 5.1 (frontier) |
| *Codex Spark 5.3* | text-only research preview for near-instant coding iteration — **the router does not select it** (no benchmark record, text-only) | — |

> **`max` is Astra/Sol only** on Codex — a capability limit, not a preference.
> Biology-R&D prompts still route to Claude (`unverified — use Claude`). For
> **offensive security**, standard Codex access hard-stops the task, so the
> router says `use Claude`; with **Daybreak Blue** access it routes to
> `Astra · xhigh`.

---

## Examples

| Task | Claude | Codex | Recommended |
|---|---|---|---|
| Split this 6000-file monolith into services | `Fable 5.1 · max` | `Astra · max` | **Codex** — against Astra the coding lead is level, so token load decides |
| Label 200 customer reviews positive/negative | `Haiku 4.5` | `Luna · low` | **Codex** — both clear the bar; Luna is faster and cheaper |
| Add a `--dry-run` flag to this CLI command | `Sonnet 5 · medium` | `Terra · medium` | **Claude** — D=1, so efficiency decides; $2/$10 vs $2/$12 |
| Refactor the payment module across 40 files, make the tests pass | `Sonnet 5 · high` | `Terra · xhigh` | **Claude** — Terminal-Bench 4.0 agentic-code margin |
| Implement the RFC across ~25 files: add tests, run lint and the build, fix what breaks | `Sonnet 5 · ultracode` | `Terra · xhigh` | **Claude** — five kinds of step is orchestration, and it is not a width question |
| Rename `userId` to `accountId` across 150 files | `Sonnet 5 · medium` | `Terra · medium` | **Claude** — `W=3` but `D=1`; one step repeated is width, so no orchestration mode |
| Investigate three candidate event-bus designs independently, then compare | `Sonnet 5 · xhigh` | `Sol Ultra · xhigh` | **Codex** — three strands that never wait on each other; `ultracode` is one chain |
| Design and implement the cross-service transaction boundary — ships tonight, no rollback | `Opus 5 · max` | `Astra · xhigh` | **Codex** — Rule E4: Astra `xhigh` outscores Sol `max` at a third of the output tokens |
| Prove this scheduling bound, no code | `Opus 5 · xhigh` | `Sol · xhigh` | **Claude**, low-confidence — coding benchmarks weigh zero here |
| Drive the desktop ERP client through month-end close | `Sonnet 5 · high` | `Astra · high` | **Codex**, low-confidence — OSWorld computer-use lead |
| Check 120 unrelated vendors' DPA compliance | `Sonnet 5 · ultracode` | `Sol Ultra · xhigh` | **Codex** — genuine parallel-agent mechanism, no Claude capability edge |
| Audit this genomics pipeline's variant-calling logic | `Fable 5.1 · high` | `unverified — use Claude` | **Claude** — availability gate |
| Bump `MAX_RETRIES` 3→5 in the prod config | `Sonnet 5 · low` + review note | `Terra · low` + review note | **Claude** |
| "Fix this code" | *(no model, no badge — asks: which code? broken how? done = ?)* | | |

---

## Validation

`evals/routing/evals.json` is a deterministic, re-runnable regression set graded
by `evals/routing/grade_routing.py` (pure regex, no LLM). The protocol: spin up
**cold agents** that read `skill/SKILL.md` fresh and route each prompt; grade the
raw output.

The grader checks the Claude model, the Claude effort, the Codex model, the Codex
effort, **which side carries the badge** (`expected_recommended`), and that an
`Evidence:` line is present and non-trivial. It deliberately does **not** compare
the Evidence wording — that line is free-form by design — but it can require it
to flag `low-confidence` where the rules say it must.

Latest run: **32/32** (iteration-17). The evidence layer has its own,
faster checks that run without an LLM — schema validation, rule-provenance
resolution, frontier staleness, the compiler assertions and the bias ablation.

**Correctness is not coverage.** A regression suite answers "does this prompt get
the right answer?"; it cannot answer "is there any prompt at all that reaches
`Sonnet 5 · ultracode`?" `evals/reachability/` answers the second one: a
154-prompt labelled corpus, a machine-readable mirror of the rules, and a
generated matrix with one row per supported model × effort/mode cell. **A zero
with no written rationale fails the run.** The counts are a diagnostic, never a
target — no frequency goal was used and no prompt exists to make a cell non-zero.
It found three bugs the routing evals could not see: an effort emitted on a model
that has no effort parameter, orchestration bought for 150 files of one
mechanical rename, and a dead zone where `ultracode` and `max` refused the same
task for opposite reasons. Details in `skill/reference.md` §16.

Run history and the reasoning behind every rule change is in
[`evals/README.md`](evals/README.md).

---

## Contributing

Corrections to model specs, prices, effort defaults, safety-fallback behaviour or
**benchmark records** are very welcome — cite the primary source, and add the
harness/effort/date alongside the number so the comparability check can use it.
Rule changes must keep the eval suite green
(`python evals/routing/grade_routing.py --results-dir <new iteration>`).
See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).
