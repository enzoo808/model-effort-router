# model-effort-router

**Paste a task. Get told which model and effort level to run it on — for both Claude and Codex/ChatGPT — and which of the two is actually the better fit for *that* task.** It does *not* run the task; it routes it.

Installed as a Claude Code / claude.ai skill invoked with `/model-secici`.

```
You:    /model-secici  Move the repo's auth flow to OAuth2

model-secici:
  Claude: Sonnet 5.5 · effort: high
  Codex:  ✅ RECOMMENDED AI · Sol · effort: high
  Evidence: AA's Terminal-Bench 4.0 has Sol 56 against Sonnet 5.5's 64 with no
            interval, and one row is not a direction — so token load decides:
            ~38k output tokens and $0.72 per task against ~193k and $7.60
            (low-confidence).
```

The badge is **computed, not habitual** — swap the task and it moves (the second
example below is the *Luna* case; the third is the one capability where Claude
still earns a direction):

```
You:    /model-secici  Label these 200 customer reviews as positive/negative

model-secici:
  Claude: Haiku 4.5
  Codex:  ✅ RECOMMENDED AI · Luna · effort: low
  Evidence: Both clear the bar for mechanical classification, and Luna
            (GPT-6) costs $0.10/$0.50 per MTok against Haiku 4.5's $1/$5.
```

```
You:    /model-secici  Draft the Q3 board memo from these notes and the finance pack.

model-secici:
  Claude: ✅ RECOMMENDED AI · Sonnet 5.5 · effort: high
  Codex:  Sol · effort: high
  Evidence: Two independent AA rows agree and none disagrees — GDPval-AA v2.1
            (1844 vs 1575) and AA-Briefcase (1811 vs 1564) — so knowledge work
            keeps a Claude direction, low-confidence because no interval is published.
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

## What changed for GPT-6.1 Sol (iteration-20, 30 Sep 2026)

OpenAI released GPT-6 Sol and Luna on 22 Sep — and replaced Sol with **GPT-6.1 Sol
seven days later** ($2/$10, 1.05M context, now the Codex default, "near-Astra").
The previous iteration had only *recorded* the first pair; this one re-derived the
Codex arm from the evidence. Full record: `skill/reference.md` §18.

- **The Codex arm is three tiers now: Luna / Sol / Astra.** Terra has no successor
  and is absent from OpenAI's current-recommended list. GPT-6.1 Sol dominates every
  GPT-6 Sol rung (48 @ $1.05 vs 50 @ $0.32) and scores **52 @ $0.72 at ~38k output
  tokens** against Astra's 53 @ $3.26 at ~27k (AA v4.3.2, same page).
- **Three rules retired because their basis went:** the **+1 Codex effort notch**
  (Terminal-Bench 4.0's Claude lead over Sol fell from ~29 points to 4–8, and Sol's
  own curve is flat above `high`), **Rule E4** (`Sol · max` → `Astra · xhigh`), and two
  Astra gates (**≥1M-token corpus** — Sol has the same window — and **computer use** —
  2.1 OSWorld points at one seventh of the cost, on a tier C relay). The 1000+-file
  and Daybreak gates stay.
- **The badge is now computed, not judged.** Rule **BD1**: a badge direction needs two
  independent measurements that agree (an independent evaluator's run, or a vendor's
  table that favours its *rival*), none opposing; otherwise efficiency decides — and
  at `R=3` a single measurement's lean still decides, which is what keeps
  high-risk architecture work on the stronger arm. The hint is emitted by the
  compiler and asserted by tests; the badge table in the reachability mirror fails the
  build if it drifts from it.
- **A Pareto frontier of model × effort configurations**, compiled from the evidence:
  Sol `xhigh` (51 @ $0.39) dominates Opus 5.5 `medium` (51 @ $1.34); Astra `max` is
  dominated by Opus 5.5 `high`; and **Opus 5.5 `high` / `xhigh` / `max` are the only
  undominated configurations above Sol's 52.** The flagship buys the last points — it
  is not the cheap way to reach the bar.
- **The lean is large, and stated plainly.** 91 of 154 corpus prompts change;
  the badge moves from **Claude 122 / Codex 28** to **Claude 43 / Codex 107**. Against
  GPT-6.1 Sol almost no capability has a Claude *direction* under BD1, so at `R ≤ 2` it
  falls to efficiency and efficiency favours a model that uses about a third of the
  tokens at the same list price. Only knowledge work keeps a clean Claude
  direction; science and workflow automation keep one only on OpenAI's own
  against-interest table (the ablation says so).

## What changed, and when

**iteration-17 (Phase 2, historical)** hardened the evidence rather than the router: it went
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

The badge is **conditional on which Codex model is on the line** (Astra only appears
behind a gate):

```
You:    /model-secici  Split this 6000-file legacy Java monolith into independent services

model-secici:
  Claude: Fable 5.1 · effort: max
  Codex:  ✅ RECOMMENDED AI · Astra · effort: max
  Evidence: The 6000-file scale gates both arms to frontier, and against Astra
            the coding rows are contested, so tokens decide — ~27k output
            tokens/task vs ~119k (low-confidence).
  Do not apply without human review.
```

Three of the new rules change real outputs, and each is asserted in the eval set:

- **`Sonnet 5.5 · max` is dominated.** Artificial Analysis v4.3.2 (one harness,
  all rungs comparable): Sonnet 5.5 at `max` scores **56 for $7.60/task** (the
  most output tokens AA has measured); Opus 5.5 at `xhigh` scores **56 for
  $3.46** — the same score at under half the cost. So escalation is a **model**
  change, not an effort change — `Sonnet 5.5 → Opus 5.5`, at the same rung.
  (The previous generation had the identical shape: 38 @ $5.09 vs 50 @ $4.88.)
  *(The Codex mirror this bullet used to carry — GPT-5.6 `Sol · high` over `Terra · max` —
  is moot: Terra is gone. E2 is now GPT-6.1 Sol over every older Sol; see the top.)*
- **`max` over `xhigh` buys little.** Fable 5.1 scores 53 at both rungs
  ($7.63 → $5.98); Astra 53 at both ($3.26 → $2.31); Opus 5.5 58 vs 56 (+2 for
  +73% cost). `max` requires `D=3 ∧ R=3` **and** a single indivisible
  novel-design or formal decision — not merely "hard and irreversible".
- ~~**A computer-use gate on the Codex arm.**~~ *Retired in iteration-20: GPT-6.1 Sol
  is 2.1 OSWorld points behind Astra at one seventh of the cost.*

## What changed for the Claude 5.5 models (iteration-19, 29 Sep 2026)

Claude Opus 5.5 (22 Sep) and Sonnet 5.5 (28 Sep) replaced Opus 5 and Sonnet 5.
Rather than rename and move on, the pass re-asked which rules the new evidence
touches — full record in `skill/reference.md` §17:

- **Roster:** Opus 5.5 ($4/$20, default effort `medium`) and Sonnet 5.5 ($2/$10).
  Haiku 5.5 is announced, not released — the router does not select it.
- **The frontier rung is narrower.** Anthropic's own same-harness table has Opus
  5.5 at or above Fable 5.1 on all eight benchmarks it lists (Terminal-Bench 4.0
  66.4 vs 55.8) at less than half the price. So *"it runs for hours"* no longer
  reaches Fable 5.1 — only a stated `xhigh`/`max` shortfall does.
- **Against Astra, the coding rows are now a tie**, so four badge cells say
  `low-confidence` instead of quietly picking a side: on the independent rows Astra
  ties Opus 5.5 (Terminal-Bench 4.0 60 vs 59.6; Coding Agent Index 62 = 62), and the
  vendor's 66.4-vs-57.9 gap compared Opus at `xhigh` with Astra at `high`.
- **The compiler got stricter.** It used to compare unmatched efforts as if they
  matched, and to pool every benchmark of a launch note into one "effort curve".
  Both fixed and unit-tested.
- **Deliberately not changed:** the D=3 → Opus 5.5 rule (Sonnet 5.5 leads
  Terminal-Bench 4.0 but trails on FrontierCode and CursorBench, and burns more
  tokens at `max`), and the biology / 1000+-file gates → Fable 5.1 (no evidence
  either way; flagged as the least-supported decision in the router).
- **Done in iteration-20:** OpenAI's GPT-6 Sol / Luna — see the top of this section.

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
  comparable across versions; "agentic coding" is not one number (AA's Terminal-Bench
  4.0 has GPT-6.1 Sol 4–8 points behind Opus / Sonnet 5.5; the same benchmark had
  GPT-5.6 Sol ~29 behind; OpenAI's DeepSWE has Sol *ahead* of Sonnet 5.5) — a vendor
  table can pair *unmatched* efforts (Opus 5.5 at `xhigh` against Astra at `high`),
  which the compiler refuses to compare, and a vendor scores its rival differently
  (Opus 5.5 on TB-Science: 63.3 in OpenAI's table, 58.7 in Anthropic's).
- **No interpolation between effort rungs, ever.** Sonnet 5.5 below `max` and Sol at
  `xhigh` simply aren't published. They're recorded as unknown, not estimated.
- **Vendor benchmarks are used but discounted.** A vendor table that favours its own
  model counts for nothing in a badge decision; one that favours its *rival* is the
  most credible vendor evidence there is. Each group declares who ran it
  (`run_by`), never inferred.
- **Conflicts are recorded, not averaged away.** The open conflicts and the
  explicit non-findings are written down in `skill/reference.md` §12.3–§12.5 —
  including that the two vendors publish Opus 5 on the same OSWorld version and
  scoring mode 5.2 points apart, and that OpenAI's and Anthropic's Terminal-Bench
  figures for the Claude models are digit-for-digit identical, which makes them
  one number re-cited rather than two runs.

Every record — benchmark, version, model, effort, harness, tool access, scaffold,
trials, dispersion, cost/task, date, source, source tier, comparability group —
is in **[`skill/benchmarks.json`](skill/benchmarks.json)**, 311 rows, `null`
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
python scripts/compile_benchmark_frontiers.py    # regenerate: frontiers, effort curves, Pareto, badge_hint
python scripts/test_frontier_compiler.py         # comparison, Pareto and badge-hint assertions
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
> the spread *is* the gap. Removing it leaves no cross-ecosystem direction against
> a current Codex model certified at all — the only certified results are two
> *equivalences* (Astra sits inside the Claude frontier's band on TB-Science and on the
> Terminal-Bench 4.0 leaderboard). Everything else is `UNRESOLVED` and falls through to
> the badge rule BD1 above. What is gone is the pretence that the gaps were measured.

The compiler never interprets a number on its own: every threshold, grouping and
precedence weight is declared in `benchmarks.json`, and where the declared
metadata doesn't settle a comparison the answer is `UNRESOLVED` — which tells the
router to fall through to efficiency. It never averages two conflicting sources.
Two runs produce byte-identical output, and the frontier stores the sha256 of the
evidence it came from, so editing the evidence without recompiling fails the
build.

**The vendor-bias measurement is the uncomfortable one.** Re-derive the badge hints
using only independent (tier B) evidence, or with vendor-measures-competitor rows
removed. Against GPT-6.1 Sol only `knowledge-work` keeps its Claude direction
(two AA rows). `science` and `workflow-automation` fall to `efficiency` — their
direction rested on OpenAI's *own* table having Opus 5.5 ahead of its own model, which is
excellent evidence but is still one vendor's account. Against Astra,
`deep-reasoning` needs OpenAI's tooled-HLE row. The router doesn't paper over that or
force a balanced badge: those cells are marked † and their Evidence line has to say
`low-confidence`.

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
| **1 · Hard gates** | Capability / safety / availability, never traded against efficiency. Sub-second or high-volume → **Haiku** / **Luna**. Offensive security → **Opus 4.8 · xhigh** / Codex `use Claude` (or `Astra` w/ Daybreak). Biology R&D → **Fable 5.1** / Codex `unverified`. >200k context → drops Haiku. 1000+ files → **Fable 5.1** / **Astra** (Astra on OpenAI's positioning only — Sol has the same window). |
| **2 · Capability profile** | Name the one or two capabilities the task actually needs — `agentic-code`, `terminal-tool`, `deep-reasoning`, `knowledge-work`, `research-synthesis`, `long-context`, `computer-use`, `science`, `workflow-automation`, `doc-data-understanding`, `parallel-independent`, `orchestration`, `latency-volume`. This is what makes benchmark evidence applicable *or not*. |
| **3 · Score scope & stakes** | **R**isk, **D**epth, **W**idth, **C**ontext — each 0–3, each with a diagnostic question and a worked-example library. |
| **4 · Candidate model × effort** | Model ← `max(D, C)` and the capability profile — **not** risk. Flagship only at `D=3` *and* a capability on the flagship list. Effort ← `D` (`0→low · 1→medium · 2→high · 3→xhigh`). Claude modifier: **`ultracode`** — >30 min **and** either `O=high` (3+ distinct *phases* — research / implementation / verification / packaging / migration / docs / triage — feeding each other; the edit-run-repair loop is **one** phase) or `W=3` ∧ `D≥2`, **and** not one indivisible chain; plus `opusplan`. Codex modifier: **Sol Ultra** for 3+ genuinely parallel strands — **both arms take the same effort from the same table**. Third escalation rung — Opus 5.5 → Fable 5.1, Sol → Astra — only on a *stated* flagship-tier shortfall. |
| **5 · Evidence, equivalence, efficiency** | Check comparability. Decide "meaningfully better" from **published dispersion only** — a confidence interval, a standard error, repeated-trial variance, or a threshold the benchmark's own owner publishes. With none of those the comparison is **`UNRESOLVED`**, however large the gap looks: observed score spread is not uncertainty. Widen the bar when `R=3`. Then apply dominance: reasoning tokens → output tokens → total tokens → tokens per *successful* task → quota pressure → cost → latency. |
| **6 · `✅ RECOMMENDED AI`** | Compare the two arms in order: hard gate → task-relevant capability → benchmark confidence → near-parity → token/quota efficiency → cost → latency. **BD1** decides whether a benchmark may set a direction (two independent measurements that agree, none opposing) — else efficiency, except that at `R=3` a single lean decides; **MECH1** lets a mechanism only one arm has (Ultra, `ultracode` on 3+ phases, `opusplan`) win when nothing benchmark-backed disagrees. Emit one badge and one `Evidence:` sentence naming at most 1–2 signals. |
| **7 · Quota guards** | `R=3` adds a human-review note (never changes the model). Escalation is a model change, not an effort change. MCP-server bloat, auto-accept, alias drift warnings. |

Two design choices carried over unchanged, because they still hold: **risk raises
human oversight, not model tier**, and **when in doubt, round down**.

---

## The rosters

**Claude (verified 30 Sep 2026):**

| Model | Role | $/Mtok in·out |
|---|---|---|
| Haiku 4.5 | speed / volume, no effort param, 200k context. Retirement floor **15 Oct 2026**; Haiku 5.5 announced, not released | $1 / $5 |
| **Sonnet 5.5** | daily driver, default starting point (replaces Sonnet 5) | **$2 / $10** |
| **Opus 5.5** | flagship — complex agentic code, enterprise; API default effort `medium` (replaces Opus 5) | **$4 / $20** |
| Opus 4.8 | legacy — kept **only** for the offensive-security gate | $5 / $25 |
| **Fable 5.1** | frontier scale, long-horizon autonomy, biology-adjacent R&D | $10 / $50 (cache reads ¼: $0.25) |
| Mythos 5.1 | = Fable 5.1 with permissive safeguards, **Project Glasswing invite only** | — |

> The Opus 5.5 : Sonnet 5.5 list-price ratio is **2×** — but per *task* it can
> invert: at `max` Sonnet 5.5 costs more than Opus 5.5 ($7.60 vs $5.98). List price
> is a proxy for quota only at comparable effort.
>
> *(Correction of 10 Sep 2026, about the previous generation: Sonnet 5's rise to
> $3/$15 was cancelled and $2/$10 stayed.)*

**Codex / ChatGPT (GPT-6 generation, verified 30 Sep 2026):**

| Model | Role | rough Claude analogue |
|---|---|---|
| Luna | **GPT-6 Luna**, $0.10 / $0.50 — volume, cheapest, and the weakest agentic model in the record (Terminal-Bench 4.0: 13 vs Sol's 56); never for `D ≥ 1` | Haiku 4.5 |
| **Sol** | **GPT-6.1 Sol** (29 Sep), $2 / $10, 1.05M context, **Codex default**, near-Astra. The daily driver *and* the D=3 pick — there is no Terra between | Sonnet 5.5 / Opus 5.5 |
| **Sol Ultra** | a Codex *mode* on Sol (Plus+): ~4 collaborating agents in parallel. Also available on Astra | stronger than Claude's `ultracode` |
| **Astra** | GPT-6 flagship, $10 / $50. **Rare pick:** the Daybreak gate (it leads Sol on every published offensive eval), the 1000+ file gate, and a stated flagship-tier shortfall | Opus 5.5 / Fable 5.1 (frontier) |
| *Legacy — never selected* | Terra, GPT-5.6 Sol / Luna, GPT-6 Sol (superseded after seven days), Codex Spark 5.3 | — |

> **`max` only through Rule M1** (D=3 ∧ R=3 ∧ one indivisible decision, on a
> flagship). Biology-R&D prompts still route to Claude (`unverified — use Claude`).
> For **offensive security**, standard Codex access hard-stops the task — Astra
> **and GPT-6.1 Sol** are both at OpenAI's *Critical* cyber level — so the router says
> `use Claude`; with **Daybreak Blue** access it routes to `Astra · xhigh`.

---

## Examples

| Task | Claude | Codex | Recommended |
|---|---|---|---|
| Split this 6000-file monolith into services | `Fable 5.1 · max` | `Astra · max` | **Codex**, low-confidence — the coding rows are contested against Astra, so token load decides |
| Label 200 customer reviews positive/negative | `Haiku 4.5` | `Luna · low` | **Codex** — both clear the bar; Luna is $0.10/$0.50 vs $1/$5 |
| Add a `--dry-run` flag to this CLI command | `Sonnet 5.5 · medium` | `Sol · medium` | **Codex**, low-confidence — D=1, the same $2/$10, Sol's lower token load |
| Refactor the payment module across 40 files, make the tests pass | `Sonnet 5.5 · high` | `Sol · high` | **Codex**, low-confidence — one Terminal-Bench row is not a direction, so tokens decide; one implementation phase, so no `ultracode` |
| Stand up staging from scratch: Terraform, deploy 12 services, seed data, run the smoke suite, fix | `Sonnet 5.5 · ultracode` | `Sol · high` | **Claude** — three phases feeding each other; `ultracode` sequences them and Codex has no equivalent (MECH1) |
| Rename `userId` to `accountId` across 150 files | `Sonnet 5.5 · medium` | `Sol · medium` | **Codex**, low-confidence — `W=3` but `D=1`; one step repeated is width, so no orchestration mode |
| Investigate three candidate event-bus designs independently, then compare | `Sonnet 5.5 · xhigh` | `Sol Ultra · xhigh` | **Codex** — three strands that never wait on each other; `ultracode` is one chain |
| Design and implement the cross-service transaction boundary — ships tonight, no rollback | `Opus 5.5 · max` | `Sol · max` | **Claude**, low-confidence — `R=3`, so a single-row lean is not parity (the same task at `R≤2` reads Codex) |
| Prove this scheduling bound, no code | `Opus 5.5 · xhigh` | `Sol · xhigh` | **Codex**, low-confidence — one HLE row and a CritPt tie are not a direction |
| Drive the desktop ERP client through month-end close | `Sonnet 5.5 · high` | `Sol · high` | **Codex**, low-confidence — the computer-use gate is retired; no comparable row |
| Check 120 unrelated vendors' DPA compliance | `Sonnet 5.5 · ultracode` | `Sol Ultra · xhigh` | **Codex** — genuine parallel-agent mechanism |
| Draft the Q3 board memo from these notes | `Sonnet 5.5 · high` | `Sol · high` | **Claude**, low-confidence — the one capability with a BD1 direction |
| Audit this genomics pipeline's variant-calling logic | `Fable 5.1 · high` | `unverified — use Claude` | **Claude** — availability gate |
| Bump `MAX_RETRIES` 3→5 in the prod config | `Sonnet 5.5 · low` + review note | `Sol · low` + review note | **Codex**, low-confidence — `D=0`, efficiency decides |
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

Latest live cold-agent run: **iteration-20, 38/38** (cold agents that had never seen the skill; a first pass caught one ambiguous prompt, `x1`, fixed at the prompt rather than the rule). The evidence layer has its own,
faster checks that run without an LLM — schema validation, rule-provenance
resolution, frontier staleness, the compiler assertions and the bias ablation.

**Correctness is not coverage.** A regression suite answers "does this prompt get
the right answer?"; it cannot answer "is there any prompt at all that reaches
`Sonnet 5.5 · ultracode`?" `evals/reachability/` answers the second one: a
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
