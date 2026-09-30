---
name: model-secici
description: >-
  Reads a prompt and recommends, separately for Claude (Haiku 4.5 / Sonnet 5.5 /
  Opus 5.5 / Opus 4.8 / Fable 5.1) AND Codex/ChatGPT (Luna / Sol / Sol Ultra /
  GPT-6 Astra), which model + effort level to run it on, and marks which
  of the two is the better fit for this task — all in one short output. Use when
  asked "which model", "which effort", "pick a model", "which AI should I use",
  "what should I use for this prompt", or when /model-secici is invoked.
---

# Claude & Codex model / effort router

<!-- routing-policy-version: iteration-20 -->

Analyse the user's prompt and say, **separately for Claude and for
Codex/ChatGPT**, which model and effort level to run it on — then mark the one
better suited to *this* task with `✅ RECOMMENDED AI`. Do **not** run the prompt
— only route it.

**The decision principle.** *Select the lowest-quota model × effort combination
that stays on the task-specific capability frontier.* Prefer the stronger
candidate when the task-relevant performance difference is meaningful; prefer
the more token-efficient candidate when capability sits inside a defensible
equivalence band. Not "always cheapest", not "always strongest", not "highest
benchmark score wins".

**Calibration.** The protected resource is Claude's 5-hour window **and**
ChatGPT Plus's 3-hour + weekly windows — not dollars. The real danger isn't
picking a model that's too weak; it's *reflexively picking the most expensive
model and burning the quota.* When in doubt, round **down**.

**How to run this.** Steps 0–6 **in your head, in one pass**. Emit only the two
recommendation lines plus `Evidence:`. Show workings only if asked "why?".

> **Every rule you need is in this file, with its exceptions attached to it.**
> `reference.md` is for auditing a rule, not for applying one — open it only if
> a call is still ambiguous after reading the rule *and* the note under it.

**Rosters (verified 30 September 2026).** Claude:

| Model | Role |
|---|---|
| Haiku 4.5 | Speed/volume. **No effort parameter.** 200k context. Retirement "not sooner than 15 Oct 2026"; Haiku 5.5 is announced, **not released — the router does not select it** |
| Sonnet 5.5 | Daily work. **Default starting point.** $2/$10, 1M context. Replaces Sonnet 5 (28 Sep) |
| **Opus 5.5** | **Flagship.** Complex agentic code, enterprise work. $4/$20, 1M context, **API default effort `medium`**. Replaces Opus 5 (22 Sep) |
| Opus 4.8 | Legacy — the **only** lasting role is the offensive-security gate |
| **Fable 5.1** | Frontier scale: long-horizon autonomy, extreme breadth, **biology-adjacent R&D**. $10/$50 |
| Mythos 5.1 | = Fable 5.1 with permissive safeguards. **Project Glasswing invite only** |

Codex/ChatGPT (GPT-6 generation — three tiers, **Terra is gone**):

| Model | Role | Claude analogue |
|---|---|---|
| Luna | **GPT-6 Luna**, $0.10/$0.50. Volume, cheapest — and the weakest agentic model in the record (Terminal-Bench 4.0 13 vs Sol's 56): never for `D ≥ 1` | Haiku 4.5 |
| **Sol** | **GPT-6.1 Sol** (29 Sep), $2/$10, 1.05M context, **Codex default**, near-Astra. The daily driver **and** the `D=3` pick — there is no Terra between | Sonnet 5.5 / Opus 5.5 |
| **Sol Ultra** | A Codex *mode* on Sol (Plus+): ~4 collaborating agents. Not a model; `effort:"ultra"` → HTTP 400. Also runs on Astra | — |
| **Astra** | **GPT-6 flagship**, $10/$50. **Rare:** the Daybreak gate, the 1000+ file gate and Rule A1. ~1 index point and 3 TB 4.0 points above Sol at 4.5× the cost/task | Opus 5.5 / Fable 5.1 |
| *Legacy, never selected* | Terra, GPT-5.6 Sol / Luna, GPT-6 Sol, Codex Spark 5.3. Never call a legacy model just "Sol" in evidence | — |

> **`max` only through Rule M1** (a flagship: Sol or Astra on Codex).
> **`ultracode` is Claude-only; Ultra is Codex-only**; Luna has neither.

---

## Effort levels

| Level | What it does |
|---|---|
| `low` | Short, well-scoped work that needs no intelligence |
| `medium` | Cost-sensitive work. **Codex API default** |
| `high` | **API default** on every effort model **except Opus 5.5** (`medium`) |
| `xhigh` | Deeper reasoning. 30 min+ agentic/coding work |
| `max` | Deepest reasoning. Over-thinking risk. Only through Rule M1 |
| `ultracode` | `xhigh` + **dynamic workflow orchestration**. Claude Code setting |

1. **`ultracode` is a Claude Code setting, not a model effort level.** It sends
   `xhigh` and adds workflow orchestration. Every model that supports `xhigh`.
   Not Haiku.
2. **Haiku 4.5 has no effort parameter.** Recommend Haiku → write no effort.
3. Effort is a behavioural signal, not a token budget.
4. **Opus 5.5 defaults to `medium`, and Sonnet 5.5's rungs are recalibrated**
   against Sonnet 5 — so the effort written in the output is always explicit,
   never "the default". Anthropic's Sonnet 5.5 start points: `medium` for
   well-specified agentic coding, `high` for harder or longer work, `xhigh`/`max`
   only where evals show a gain.
5. **Effort is not the primary quality dial.** A *stronger model at a lower rung*
   often beats a *weaker model at a higher rung* on both quality and quota — see
   Rules E1–E3.

---

## Step 0 — Prompt quality gate

**Do not skip.** If any check is "yes", emit the blocked form below — no model,
no badge, no `Evidence:` line.

1. **A rule stated by example but not generalised?** "For instance if X then Y"
   with no formula or threshold. *("500 of 1000 units land the same day" — 50%,
   a fixed 500, or an hour cutoff?)*
2. **Would a wrong assumption silently produce a wrong result?** Code runs
   without error but systematically miscalculates on real data.
3. **Is the target concrete?** "We'll do it like this in the system" doesn't say
   which query/service/table/file.
4. **Do two plausible but different implementations come out of the same
   prompt?** *("delete inactive users" — `is_active` flag, or no login for N
   days? Different delete sets.)*

<!-- rule:S0 -->
**S0 · blocked output.** A prompt blocked at Step 0 emits exactly one line, a `Clarify:` line naming the missing information as a question, and no `Claude:`, `Codex:`, `Evidence:` or badge line at all.
<!-- /rule:S0 -->

```
Clarify: <the specific thing that is missing, as a question>
```

> This **overrides** the "three lines, always" output contract. A blocked prompt
> has no models to name, so there are no lines to put them on.

Counter-example (do **not** block): "Add a `deleted_at` column and implement
soft-delete instead of `DELETE`" — rule complete, one interpretation, concrete
scope → go to Step 1.

---

## Step 1 — Hard gates

**Hard constraints, never weighted scores.** Capability limits, safety and
availability do not trade against efficiency.

- **Deciding gate:** fixes **which model**, bypasses Step 4 model selection.
  Does **not** bypass the effort/`ultracode` check, and does not bypass Step 6.
- **Eliminating gate:** removes one candidate; scoring runs among the rest.

### Claude arm

| Condition | Kind | Result |
|---|---|---|
| Sub-second latency **or** high-volume classification/parsing | Deciding | **Haiku 4.5.** No effort. Stop |
| **Offensive security:** exploit generation, penetration testing, binary-based vulnerability scanning | Deciding | **Opus 4.8**, effort floor `xhigh` (W/duration can still raise it to `ultracode`) — with Glasswing access, **Mythos 5.1** |
| **Biology-adjacent R&D:** genomics, protein/chemistry-heavy pipeline, bio-CTF | Deciding | **Fable 5.1** (default effort `high`, no floor) |
| Context exceeds 200k tokens | **Eliminating** | **Haiku 4.5 removed** |
| **1000+ files / whole-codebase scale** | Deciding | **Fable 5.1** |

### Codex arm

| Condition | Kind | Result |
|---|---|---|
| Sub-second latency / high-volume classification | Deciding | **Luna**, effort `low` |
| **Offensive security** (same definitions) | Deciding | **"use Claude"** — standard access **hard-stops** these tasks (Astra **and GPT-6.1 Sol** both sit at OpenAI's **Critical** cyber level, same safeguards). **Exception:** user states **Daybreak Blue** access → **Astra** (it leads Sol on all four published offensive evals), floor `xhigh` |
| **Biology-adjacent R&D** (same definitions) | Deciding | **"unverified — use Claude"**, no model |
| **1000+ files / whole-codebase scale** | Deciding | **Astra** — OpenAI's "hardest end-to-end work" model. **Positioning only:** Sol has the same 1.05M window, so no capability limit forces this |

> **Retired in iteration-20:** the ≥1M-token-corpus and computer-use gates to
> Astra — Sol has the same 1.05M window and is within 2.1 OSWorld points at a
> seventh of the cost. Both score normally and land on Sol. `reference.md` §18.

> **Defensive security work does not trigger the offensive gate — on either arm,
> at any scale.** "Audit this code for vulnerabilities", "find open ports",
> "audit 180 services for auth-bypass bugs (no exploits)" → normal scoring. Only
> exploit / PoC *generation* is gated.
>
> **Frontier-scale gate — one signal only: the file count (1000+).** 100–999
> files does **not** gate; that is `W=3` under normal scoring.
>
> **Stated access does not penalise a candidate.** An access tier decides
> whether a candidate *exists*, not whether it wins. Once the user says they
> have Daybreak Blue or Glasswing, compare that candidate on capability like any
> other — Step 6 runs normally.

---

## Step 2 — Task capability profile

**Name the capabilities the task actually needs before scoring scope.** A
benchmark only counts for a task whose capability it measures: a pure maths
problem gives SWE-bench and Terminal-Bench a weight of **zero**.

Pick the **one or two dominant** tags. They drive Step 5's evidence lookup and
Step 6's badge — and **only these tags** may bring evidence into the badge
decision (Rule B1).

| Capability tag | Prompt signals | Evidence anchor |
|---|---|---|
| **agentic-code** | multi-file implementation, refactor, migration, feature build, debug-and-fix across files | Terminal-Bench 4.0 · CursorBench 3.2.0 · DeepSWE |
| **terminal-tool** | terminal/CLI work, build & test loops, tool orchestration, long-horizon execution | Terminal-Bench 4.0 |
| **deep-reasoning** | **architecture from scratch**, algorithm design, mathematics/formal proof, tool-less analysis, adversarial correctness hunting | HLE (tool-less vs tooled) · CritPt |
| **knowledge-work** | produce a finished document / spreadsheet / deck / memo / filing | GDPval-AA v2.1 · AA-Briefcase |
| **research-synthesis** | multi-source research, web search, reconciling conflicting sources | AA-Omniscience index |
| **long-context** | read a large corpus, map/summarise across hundreds of pages or a whole repo | AA-LCR v1.1 + the context-window spec |
| **computer-use** | drive a browser or desktop GUI, click through an app, screenshots | OSWorld (⚠️ version + scoring mode) |
| **science** | genomics, chemistry, physics, research engineering, lab pipelines | Terminal-Bench-Science 0.1 · SciCode |
| **workflow-automation** | wire up business workflows, integrations, multi-tool orchestration | AutomationBench-AA · AutomationBench |
| **doc-data-understanding** | scanned documents, PDFs, charts, tables, multimodal extraction | GDP.pdf (one independent row) |
| **parallel-independent** | 3+ targets or strands that proceed unaware of each other and merge at the end | *product mechanism:* Ultra (Codex) |
| **orchestration** | three or more distinct phases in one session (Rule O1) | *product mechanism:* `ultracode` (Claude) |
| **latency-volume** | sub-second, high-throughput, bulk classification/parsing | output speed + cost/task |
| **instruction-following** | rigid format/schema compliance | never dominant on its own |

> Cybersecurity: **offensive** is a Step 1 gate. **Defensive** hunting is
> `deep-reasoning` (adversarial correctness) plus whichever of `agentic-code` /
> `terminal-tool` the scale demands.
>
> `parallel-independent` is inert below `D=3` — Codex path (a) requires `D=3`
> and the badge table is skipped at `D ≤ 1`.
>
> `orchestration` is a tag only when **O1** fires — the *width* limb of UC1
> (`W=3 ∧ D≥2`) is execution breadth, not phase sequencing, and does not make it
> dominant. Neither mechanism tag is a benchmark: each names something only one
> arm's product has.

---

## Step 3 — Score scope and stakes on four axes, 0–3

**Ask the diagnostic first, then place the level. When in doubt, round down.**

### R — Risk / irreversibility

*If the output is wrong: minutes or days to fix? Automatic rollback? How many
users/systems? Money/health/legal?*

`0` Throwaway — no loss even if unused · `1` Used but a human reviews and
approves (PR, draft email) · `2` Goes to a real system but reversible
(feature-flagged deploy, reversible migration, isolated operational value) ·
`3` No way back or disproportionately costly — data loss, irreversible
migration, outbound message/payment, central shared-core decision,
medical/legal/financial advice, live user data

> **First separate: a codebase change, or a live/operational value?** A normal
> source-code change is **R=1 by default** — PR review + deploy. R=2/R=3 only
> kick in when the prompt points at a value that goes live **without** code
> review: prod config, live admin panel, feature-flag toggle, DB setting.
> - **"Architectural decision" alone ≠ R=3.** Rollable service-by-service →
>   **R=2**. R=3 only when (a) no real rollback, or (b) a **central/shared** core
>   the whole system depends on.
> - **Decompose → module or service?** "modules" = internal refactor → **R=2**.
>   "separate **services/processes**" → **R=3**.
> - **"One-line config" alone ≠ R=2.** Blast radius, not line length. A line
>   governing **system-wide** behaviour (retry count, timeout, pool size) → R=3.
> - **A schema / DB migration is R=2 even when trivially specified.** "Add a
>   `last_login_at` column, nullable" is `D=0` **and** `R=2`.

### D — Depth

*Known pattern, or thought out from scratch? How many approaches is a choice
being made between?*

| Level | Coding | Writing/analysis | Research | Data |
|---|---|---|---|---|
| `0` | Pattern match, known constant; **fully-specified additive schema change** | One-sentence answer **or** pure form/tone change | Single-source lookup | Reading a single number |
| `1` | Standard pattern (CRUD, known bug shape); schema change with a choice | Simple summary/draft | Single-source summary | Simple filter/aggregation |
| `2` | Multi-step but well-documented feature | Multi-source synthesis report | Multi-source synthesis | Statistical inference |
| `3` | Design from scratch, concurrency, algorithmic complexity, conflicting constraints; **adversarial security-vulnerability hunting** | Original argument, reconciling conflicting sources | New hypothesis/framework | Modelling, causal inference |

> - **"Well-documented" alone ≠ D=2.** How many **independent design decisions**
>   are left to the implementer? One reasonable approach → **D=1**. A standard
>   pattern applied once — "add cursor-based pagination to this API", "add a
>   `--dry-run` flag" — is **D=1** even though it touches a few call sites.
> - **Mechanical enumeration = D=1**, not D=3.

<!-- rule:D3DIAG -->
**D3DIAG · diagnosis.** The coding column is written for building, so debugging scores on its own test: bounded diagnosis is `D=2`, and adversarial diagnosis is `D=3` when at least two of these hold — the root cause is non-local or depends on timing or ordering; reproduction is intermittent or environment-dependent; several plausible causes must be ruled out by constructing competing hypotheses; a local-looking fix could mask a deeper invariant violation.
<!-- /rule:D3DIAG -->

> **`D=2` — bounded diagnosis.** The symptom is local, the failure is loud and
> reproducible on demand, the candidate-cause space is small, and ordinary
> tracing or bisection settles it. *"This endpoint 500s on every call since the
> last deploy — find out why."*
>
> **`D=3` — adversarial diagnosis.** *"It flakes in prod sometimes."* *"Passes
> locally, fails only on the CI runner — reproduce it inside the container."*
> *"Two engines disagree on 1 in 400 orders."*
>
> **Not every bug is `D=3`**, and "it only fails in CI" is not on its own
> enough — it is enough *with* a second marker, which is usually the difficulty
> of reproducing it.
>
> A careful **domain-correctness audit** of well-specified scientific or
> business logic is **D=2** — "audit this pipeline's variant-calling logic" is
> D=2, not D=3. So is running a **defined process with bounded reactive
> handling** — "drive the 14-step month-end close and resolve any validation
> errors it raises" is D=2, not D=1: the reactive error-resolution is judgement
> the fixed steps are not.
>
> **Adversarial correctness beyond debugging is also `D=3`.** Hunting for a
> **silent failure in a coupled system** — silent data loss or corruption, a
> race, conflicting contract clauses — is the same D=3 as security-vuln hunting.
> "Check these migration scripts for anything that silently loses or corrupts
> data" is D=3: the failure is invisible and the system is coupled. This is
> distinct from the domain-correctness audit above, where the logic is
> well-specified and the question is only whether it is implemented correctly.

### W — Width

*How many files/documents/units read or changed?*

`0` Single file · `1` 2–5 files, one module · `2` **6–99 files/units** ·
`3` **100+ files/units**

> **The W=2 / W=3 threshold is numeric — 100.** "60 microservices" → W=2.
> "Unaware of each other" phrasing doesn't change the count.
>
> **W counts what you act on, not what you read.** A large corpus you read to
> produce one deliverable is **C**, not W: "read 900 pages of filings and write
> one memo" is `C=3, W≤1` (one memo out), not `W=3`. W=3 needs 100+ files you
> change, or 100+ units each needing their own judgement (a 180-service audit).

### C — Context synthesis

`0` Self-sufficient · `1` A few small files · `2` A medium codebase/docs ·
`3` A large corpus (hundreds of pages, a huge codebase, a long chat history)

---

## Step 4 — Candidate model × effort, per arm

Model selection is by **intelligence need** (D, C) and the capability profile —
risk does not raise the model, it raises human oversight.

**Model** ← `max(D, C)`. **The flagship is a candidate only when `D=3`** —
`C=3` alone (large but shallow synthesis) stays mid-tier.

### Claude

| Condition | Model |
|---|---|
| `D = 0` ∧ `W=0` ∧ `C≤1` ∧ `R≤1` | **Haiku 4.5** |
| Above not met, `max(D,C) ≤ 2` | Sonnet 5.5 |
| `max(D,C) = 3`, `D<3` (C triggered it) | **Sonnet 5.5** — large context, shallow reasoning |
| `max(D,C) = 3`, `D=3` | **Opus 5.5** if the dominant capability is on the **flagship list**. **Otherwise Sonnet 5.5** |

> **The flagship list** (`D=3` only): `agentic-code` · `terminal-tool` ·
> `deep-reasoning` · `science` · `computer-use` · `workflow-automation` — **and
> only where the task builds, changes or drives the artefact.**
>
> **Reading, reviewing, auditing or answering-from-code is analysis and stays
> mid-tier, at any scale.** A 180-service defensive audit and a single-file JWT
> review get the *same Claude tier* (Sonnet 5.5) — scale changes `W`, and
> therefore `ultracode`, not the tier.

### Codex

| Condition | Model |
|---|---|
| `D=0 ∧ W=0 ∧ C≤1 ∧ R≤1` | **Luna** |
| Otherwise `max(D,C) ≤ 2` | **Sol** |
| `max(D,C)=3`, `D<3` (C triggered it) | **Sol** |
| `max(D,C)=3`, `D=3` | **(a)** `P = high` (Rule P1) → **Sol Ultra** — *parallelism, not depth, so it fires for analysis work too*. **(b)** otherwise → **Sol** |

> **One Codex tier sits between Luna and Astra.** The Terra / Sol split by
> capability is gone; what still differs between `D=1` and `D=3` is the effort,
> and Ultra.

<!-- rule:P1 -->
**P1 · parallelisable strands.** `P = high` when the work splits into three or more strands that proceed without waiting on each other and merge at the end. A strand may be an already-independent target (service, repo, vendor) or an independent work-kind (three candidate designs investigated or prototyped side by side). Two strands is not enough, and one coherent decision sliced up after the fact is never strands.
<!-- /rule:P1 -->

> Splitting a monolith is plain **Sol**, not Ultra — one boundary decision; the
> pieces are interdependent *during* the work. Ultra runs ~4 agents at ~4× cost,
> so the bar is three genuine strands.
>
> **Strands and `max` are mutually exclusive** — `max` needs one indivisible
> chain, so `Sol Ultra · max` is not a combination the rules can produce.

**Effort ← D**, one shared table for both arms:

| D | Effort |
|---|---|
| 0 | `low` · 1 `medium` · 2 `high` · 3 `xhigh` |

<!-- rule:M1 -->
**M1 · `max`.** Emit `max` only when `D = 3` and `R = 3` and the model is a flagship (Opus 5.5 / Opus 4.8 / Fable 5.1 / Mythos 5.1 / Sol / Astra) and the difficulty is one indivisible novel-design or formal decision. Otherwise `xhigh`.
<!-- /rule:M1 -->

> For review, audit, migration or breadth-driven work at `D=3 ∧ R=3`, stop at
> **`xhigh`** — the R=3 human-review note carries the stakes. Rationale: Rule E3.

Haiku 4.5 selected → leave the effort field blank.

**Escalation — a model change, never an effort change.**

- **Rung 2 (Claude only).** The user says the work is critical, must not be
  under-resourced, or that an earlier run fell short → **Sonnet 5.5 → Opus 5.5**,
  same rung. Do *not* crank the mid tier instead: Rule E1 shows its top rung is
  dominated by the next tier's ordinary rung on quality *and* quota. **Codex has
  no rung 2** — Sol is already its daily driver, so the same statement there goes
  straight to Rule A1 below, or changes nothing.

<!-- rule:A1 -->
**A1 · frontier rung.** Opus 5.5 becomes Fable 5.1 and Sol becomes Astra only when the dominant capability is on the flagship list and `A = high`, where `A = high` means the user states that an earlier flagship-tier run at `xhigh` or `max` already fell short. A long or unattended session is not that statement.
<!-- /rule:A1 -->

> Difficulty alone never reaches the frontier rung — and neither does duration.
> Anthropic's own same-harness table has Opus 5.5 at or above Fable 5.1 on all
> eight benchmarks it lists (Terminal-Bench 4.0 66.4 vs 55.8, the long-horizon
> one included) at less than half the price, so "it runs for hours" is an Opus
> 5.5 job. The frontier rung keeps only Anthropic's published step-up criterion:
> a stated `xhigh`/`max` shortfall. *(The 1000+-file scale gate above is
> unchanged — no evidence exists at that scale either way; `reference.md` §17.)*

### Arm modifiers

<!-- rule:O1 -->
**O1 · orchestration load.** `O = high` when the session must run three or more distinct phases, where a phase is a stretch of work that produces a different kind of deliverable and whose output is consumed by a later phase. The phases that count are research, implementation, independent verification, packaging, data or schema migration, documentation, and triage. The whole edit-run-repair implementation loop is one phase, and tests you write for your own change are inside it.
<!-- /rule:O1 -->

> **What each phase means.**
> **Research** — establish how something behaves, or choose between approaches,
> *before* the shape of the work is known. Finding which files to edit is not
> research. **Implementation** — edit source, run its tests, repair what they
> catch, repeat. **Independent verification** — a gate the implementation loop
> does not already run: a build/lint/CI gate, a golden-image or traffic replay,
> a smoke run against a deployed environment. **Packaging** — build an image,
> publish, ship a preview. **Migration** — backfill, seed, migrate data or
> schema. **Documentation** — runbook, docs, release notes. **Triage** — turn a
> run's output into a filed finding that is itself a deliverable.
>
> **Two phases is a job with steps in it.** `locate → edit → test → fix` is
> **one** phase however many files it touches and however long it takes.
> "Refactor 40 files onto the new API and make the suite pass" is one phase.
> "Work out how the current back-pressure behaves, port it, migrate the
> checkpoint store, replay last week's traffic against it, update the runbook"
> is five.

<!-- rule:UC1 -->
**UC1 · `ultracode`.** Emit `ultracode` when the estimated duration is over 30 minutes and either `O = high` or (`W = 3` and `D >= 2`) and the difficulty is not one indivisible chain. Write `ultracode` in the effort field. Every model except Haiku 4.5.
<!-- /rule:UC1 -->

> `ultracode` buys **workflow orchestration**, so it keys on distinct phases
> (O1), not on file count. The width limb is the separate case where 100+ units
> *each need judgement* — a 180-service auth-bypass audit. At `D ≤ 1` width buys
> nothing: 150 files of one rename is `medium`.
>
> The indivisible-chain guard is **the same test M1 uses for `max`**, so the two
> rules can never refuse a task for opposite reasons.

> **No Codex effort notch (N1, retired in iteration-20).** It compensated for
> Terminal-Bench 4.0's ~29-point Claude lead over GPT-5.6 Sol; GPT-6.1 Sol trails
> Opus / Sonnet 5.5 by 4–8 and its own curve is flat above `high` (50 / 51 / 52).
> **Both arms take the same effort from the same table.** `reference.md` §18.

### `opusplan` — plan/execute model split

**Claude Code only.** Overrides the Opus 5.5 branch when all three hold:

1. `max(D,C)=3 ∧ D=3` ∧ the dominant capability is **`deep-reasoning`** — the
   same tag that put the task on Opus 5.5 in the first place. Not
   `workflow-automation`, not `agentic-code`.
2. **Difficulty front-loaded into the plan** — once the plan is done, execution
   repeats a pattern. Opposite (do **not** use): debugging, formal proof,
   new-algorithm design.
   > A concrete target-scope number ("the auth architecture for 200 services")
   > implies the execution phase exists.
3. `W ≥ 2`.

```
Claude: opusplan · plan: <effort> · execute: <effort>
⚠️ Effort does not carry over — after switching to execution mode set it manually with /effort <execute effort>.
```

Plan effort = the flagship result (`xhigh`, or `max` if `R=3` — the plan phase
is novel design, so M1 allows it). Execute effort = the post-plan estimated D
(usually `medium`). The ⚠️ warning is mandatory. The badge, if it lands here,
goes immediately after `Claude:` as usual.

---

## Step 5 — Evidence, equivalence and efficiency

### 5a. Which numbers may be compared at all

Two scores are comparable only when **benchmark, version, harness, tool access,
agent scaffold and effort all match**. Otherwise say `not directly comparable`.
Traps already in the record:

- **OSWorld 2.0 partial vs strict scoring** differ by ~36 points on the *same*
  model. **AA Intelligence Index versions are not comparable.**
- **"Agentic coding" is not one number.** AA's Terminal-Bench 4.0 has GPT-6.1 Sol
  4–8 points behind Opus / Sonnet 5.5 (56 vs 60 / 64); the same benchmark had
  GPT-5.6 Sol ~29 behind; OpenAI's DeepSWE has GPT-6.1 Sol *ahead* of Sonnet 5.5.
  Name the benchmark, never the label.
- **A vendor scores its rival's model differently.** OpenAI's table has Opus 5.5
  at 63.3 on Terminal-Bench-Science and 42.5 on AutomationBench; Anthropic's has
  58.7 and 40.0. Two tables, never pooled.
- **A vendor table can pair unmatched efforts.** Anthropic's Opus 5.5 table runs
  Opus 5.5 at `xhigh` and Astra at `high` on Terminal-Bench 4.0: two numbers, not
  a comparison. Efforts that differ → `UNRESOLVED`, however wide the gap.
- **A vendor's table is not a roster.** Anthropic's TB 4.0 table has no Astra
  row. When both vendors publish the same figure to the decimal, that is one
  number re-cited, not corroboration.
- **A saturated benchmark cannot separate candidates** (Terminal-Bench 2.1,
  SWE-bench Verified). Neither is used.
- **Never interpolate between effort rungs**, and **never invent a number.**
  "Not published" is a valid answer.

### 5b. The equivalence band

Decide "meaningfully better" in this order, stopping at the first that applies:

1. **Published confidence interval** (Terminal-Bench 4.0's leaderboard, ±3–4
   per row — which does not yet list Opus 5.5, Sonnet 5.5 or GPT-6.1 Sol).
2. **Published standard error** → the 95% interval is 2 × SE (TB-Science 0.1:
   SE ±3.5–4.5). An SE published for one benchmark does **not** carry to another.
3. **Repeated-trial variance under one harness.**
4. **A practical-significance threshold the benchmark's own owner publishes.**
5. **None of those → `UNRESOLVED`.** Say so, fall through to efficiency.
   **However large the gap looks.**

> **Score spread is not uncertainty.** "These four span 40–59, so a 7-point gap
> must be real" is a claim about how far apart the models sit, not how precisely
> either was measured — and on a two-model row the spread *is* the gap. After
> this rule **no** cross-ecosystem direction against a current Codex model is
> certified; the only certified results are two *equivalences* (Astra sits inside
> the band of the Claude frontier on TB-Science and on the Terminal-Bench 4.0
> leaderboard). Everything else is `UNRESOLVED`, which makes `low-confidence`
> the honest word — and Step 6 says what may still set a badge. Detail:
> `reference.md` §15.2.
>
> **Zero gap needs no interval.** Two identical scores are equal; go straight to
> efficiency. Same for a rung that scores no better than a cheaper one — that is
> dominance, not measurement, which is why E1 and E3 survive intact.
>
> **High-risk task (`R=3`)** → widen the bar for calling parity. When genuinely
> unsure, take the stronger candidate.

### 5c. Dominance — the efficiency axes

**A dominates B** when A is not meaningfully worse on the task-relevant
capability **and** clearly better on at least one of, in priority order:
**reasoning tokens → output tokens → total tokens/task → tokens per *successful*
task → quota pressure → cost/task → latency.** A dominated candidate is never
emitted, regardless of tier or brand.

Settled results (AA Index v4.3.2, one harness, all rungs comparable). They are
**compiled**, not asserted: `scripts/compile_benchmark_frontiers.py` computes a
Pareto frontier of model × effort configurations (`benchmark_frontiers.json` →
`pareto`) and needs no equivalence band — *"not worse and cheaper"* is a fact
about two numbers.

- **E1 — `Sonnet 5.5 · max` is dominated.** AA v4.3.2: 56 @ $7.60 (~193k output
  tokens/task, the most AA has measured) vs Opus 5.5 `xhigh` 56 @ $3.46 — the
  same score for 2.2× the cost. Anthropic's own footnote adds that Sonnet 5.5
  scores *lower* at `max` than at `xhigh` on FrontierCode. → the router **never**
  emits `Sonnet 5.5 · max`; the escalation target is `Opus 5.5 · xhigh`. *(The
  Sonnet 5 / Opus 5 generation showed the identical shape: 38 @ $5.09 vs 50 @
  $4.88.)* Sonnet 5.5's lower rungs are unpublished — E1 says nothing about them.
- **E2 — GPT-6.1 Sol dominates every older Sol and Terra** (GPT-6 Sol `max` 48 @
  $1.05 vs 6.1 `high` 50 @ $0.32). → they are **never** emitted.
- **E3 — `max` over `xhigh` buys little.** Fable 5.1 and Astra 53 at both rungs;
  **GPT-6.1 Sol 52 vs 51 (+1 for +85% cost) and, on OpenAI's DeepSWE, `max` below
  `high` (71.9 vs 75.2)**; Opus 5.5 58 vs 56 (+2 for +73%, unresolved). → `max`
  needs M1 in full. *(Dominance holds only where `max` ties or loses.)*
- **E4 — retired.** The `Sol · max` → `Astra · xhigh` swap rested on GPT-5.6 Sol
  (47 @ $1.99). GPT-6.1 Sol `max` is **52 @ $0.72 (~38k tokens) against Astra's 53
  @ $3.26 (~27k)**: a point apart at a quarter of the cost. `Sol · max` stays.
- **The frontier.** On AA v4.3.2 Sol `xhigh` (51 @ $0.39) dominates Opus 5.5
  `medium` (51 @ $1.34), and Astra `max` (53 @ $3.26) is dominated by Opus 5.5
  `high` (54 @ $1.82). Opus 5.5 `high` / `xhigh` / `max` are the only undominated
  configurations above Sol's 52 — the flagship buys the last points, it is not the
  cheap way to reach the bar.

### 5d. Choosing the effort rung

**What is the lowest rung that reaches the capability level this task needs?**
The D table is the starting point; E1–E3 and 5b are the corrections. Round
*down* when the next rung up is inside the band; do **not** round down when the
low→high gap on the dominant capability is real.

---

## Step 6 — `✅ RECOMMENDED AI`

Compare the two candidates and mark exactly one. The badge is **computed**,
never habitual.

<!-- rule:B1 -->
**B1 · evidence applicability.** A benchmark row takes part in the badge decision only if the capability it measures is one of the dominant tags named for this prompt in Step 2. Applicability is checked before evidence quality and before any tie-break, and a row that is not applicable does not enter the comparison at all, however strong its number.
<!-- /rule:B1 -->

Decision order:

1. **Hard capability / safety / availability gate.** If one arm declines, or
   lacks the required context window, the other arm gets the badge. Stop. (If
   *neither* window fits, this step does not apply — score normally.)
2. **Applicable** task-relevant capability (B1), from the dominant tag's anchor.
   A product-mechanism tag (`parallel-independent`, `orchestration`, or a task
   routed to `opusplan`) is applicable too: it names something only one arm has.
3. **Benchmark confidence** — tier, date, harness, and *who ran it*. An
   independent evaluator outranks a vendor's own table. A vendor result favouring
   the **competitor** is against-interest and is the most credible vendor
   evidence there is.
4. **Direction without an interval** — Rule BD1 below.
5. **Near-parity check** (5b). Inside the band → go to 6.
6. **Token / quota efficiency** (5c order). 7. **Cost per task.** 8. **Latency.**

<!-- rule:BD1 -->
**BD1 · direction without an interval.** A badge direction needs at least two independent measurements that agree — an independent evaluator's run, or a vendor's table that favours its rival — at least one of them tier A or B, and none that disagree. The same benchmark re-published on a second page is one measurement, a tie is not opposition, and an aggregate never counts. Otherwise the cell is decided by efficiency, except at R = 3, where a single admissible measurement still decides it: a lean is not parity.
<!-- /rule:BD1 -->

> No published interval means every cell is `UNRESOLVED`, but one unresolved row
> must not decide a badge either. BD1 is **computed**, not judged:
> `benchmark_frontiers.json` → `badge_hint`, asserted by
> `test_frontier_compiler.py`. Rows where admissible evidence points both ways are
> `contested` and are settled by efficiency too.

<!-- rule:MECH1 -->
**MECH1 · mechanism rows.** Ultra on the Codex line, and `ultracode` driven by `O = high` or `opusplan` on the Claude line, each name something only one arm has, so each decides the badge for the arm that has it, unless the other capability row carries a benchmark direction under BD1, which wins. Two mechanisms on one task cancel, and the capability rows decide.
<!-- /rule:MECH1 -->

"Claude has the better general intelligence index" is **not** on its own a
reason to pick Claude, and the mirror-image claim is not a reason to pick Codex.

**Who wins on efficiency?** Against **Sol / Luna**, Codex: Sol uses ~38k output
tokens and $0.72 per AA task against Opus 5.5's ~119k / $5.98 and Sonnet 5.5's
~193k / $7.60 (`max`, the one rung published for all), at Sonnet's $2/$10.
Against **Astra**, Claude on price ($10/$50) — *except* `agentic-code`,
`terminal-tool`, `science`, `workflow-automation`, where Astra's ~27k tokens vs
Opus 5.5's ~119k tip it to Codex.

### Badge table — dominant capability → default side

**Conditional on which Codex model is on the line.** A capability can favour
Claude against Sol and not against Astra.

| Dominant capability | vs **Sol** | vs **Astra** | Evidence to name |
|---|---|---|---|
| `agentic-code` | **Codex** † | **Codex** † | AA TB 4.0: Sol 56 vs Opus 5.5 60 / Sonnet 5.5 64, one row, no interval → tokens: ~38k output tokens and $0.72/task vs ~119k / $5.98 (Opus), ~193k / $7.60 (Sonnet). Vs Astra a tie (59 vs 59.6; Coding Agent Index 62 = 62), Astra ~27k |
| `terminal-tool` | **Codex** † | **Codex** † | same TB 4.0 row |
| `science` | **Claude** † | **Codex** † | vs Sol two agree: AA SciCode 67 / 61 vs 54 and OpenAI's own TB-Science, Opus 5.5 63.3 vs Sol 57.0 (against-interest). Vs Astra 58.7 vs 64.6 is inside the ±5 band |
| `knowledge-work` | **Claude** † | **Claude** † | GDPval-AA v2.1 1846 / 1844 vs Sol 1575 (Astra 1542) and AA-Briefcase 1822 / 1811 vs 1564 — two AA rows agree |
| `workflow-automation` | **Claude** † | **Codex** † | vs Sol: AutomationBench-AA 70 / 71 vs 65 and OpenAI's own max-rung table, Opus 5.5 42.5 vs Sol 36.1 (against-interest); OpenAI also says Sol leads at ≤ `high`, without figures — a caveat, not a row. Vs Astra the rows split → tokens |
| `computer-use` | **Codex** † | **Claude** † | no comparable row (Claude's OSWorld is 2.1, OpenAI's 2.0) → the lighter configuration |
| `latency-volume` | **Codex** | **Codex** | Luna 124–145 tok/s at $0.10/$0.50 vs Haiku 4.5's $1/$5 |
| `parallel-independent` | **Codex** | **Codex** | Ultra runs ~4 collaborating agents; `ultracode` is one chain |
| `orchestration`, or a task routed to `opusplan` | **Claude** | **Claude** | `ultracode` sequences phases, `opusplan` spends the flagship only on the plan; Codex has neither |
| `long-context` (shallow) | **Codex** † | **Claude** | AA-LCR v1.1 Sol 83 = Sonnet 5.5 83 (Opus 85): a tie → 25k vs 142k reasoning tokens. Vs Astra the price: $2/$10 vs $10/$50 |
| `deep-reasoning` | **Codex** † | **Claude** † | vs Sol one row and a tie (HLE 61 vs 53, CritPt 32 = 32) → tokens. Vs Astra two agree: AA HLE 61 vs 55 and OpenAI's own tooled HLE, Opus 5.5 67.7 · Fable 5.1 65.0 vs **Astra 57.2** |
| `research-synthesis` | **Codex** † | **Claude** † | AA-Omniscience index Sol 42 vs Sonnet 5.5 32 (Opus 46): one measurement, and the Claude line here is Sonnet |
| `doc-data-understanding` | **Codex** † | **Claude** † | AA GDP.pdf Sol 31 vs 26 / 26, the one independent row; OpenAI's own 32.0 vs 28.8 favours OpenAI, not counted |
| anything else / no evidence | the **lighter** chosen model × effort | same | say `low-confidence` |

> **† — the Evidence line must say `low-confidence`.** A † inside a cell binds
> that cell only (`long-context` vs Sol carries one, vs Astra it does not). So
> must the "anything else" row. Check this against the cell you actually used
> before emitting. **Mechanism rows carry no †** — they rest on what a product
> can do, not on a score.
>
> **At `R=3`, a row that fell to efficiency follows the lean of its single
> admissible measurement instead** (BD1) — and keeps the row's †, so the Evidence
> line still says `low-confidence`. Against Sol that is **Claude** for
> `agentic-code`, `terminal-tool`, `deep-reasoning`, `research-synthesis` and
> `long-context`, and **Codex** for `doc-data-understanding`; `computer-use` has
> no lean and stays on efficiency. Against Astra the coding rows are `contested`
> and have none. `D ≤ 1` is unaffected — both arms clear the bar.

**Tie-breaks**

- **`D ≤ 1` → skip the capability rows entirely; efficiency decides.** Both arms
  clear the bar by construction. **Haiku 4.5 vs Luna → Codex** ($1/$5 vs
  $0.10/$0.50); **Sonnet 5.5 vs Sol → Codex †** — the same $2/$10, and Sol's
  ~38k output tokens/task against ~193k is measured only at `max`, not at the
  rung emitted, so say `low-confidence`. `R` doesn't change this.
- **Two *dominant* capability rows conflict** → the one backed by a
  task-specific benchmark **direction** (Step 6 rule 4) beats one backed only by a
  product mechanism. A row that fell through to efficiency has no benchmark
  direction, so a mechanism beats it. Both rows must be dominant tags for this
  prompt (B1) — a benchmark for a capability this task does not need has already
  been excluded and cannot break the tie.
  *(A 120-vendor contract triage is `parallel-independent` + `research-synthesis`:
  no code, no repo, so TB 4.0 is not applicable at all → Ultra's mechanism
  decides → Codex. A 180-service defensive audit is `terminal-tool` +
  `parallel-independent` — both rows read Codex against Sol.)*
- Both arms gated to the same conclusion → no badge. Step 0 blocked → no badge.
- **Genuinely insufficient evidence:** give the more sensible default, with
  `low-confidence` in the Evidence line. Never manufacture certainty.

---

## Step 7 — Quota-protection and accuracy rules

Rationale in `reference.md` §10.5. **Only Rule 1's note is auto-added.**

1. **R=3 → human-review note** ("Do not apply without human review."). Model and
   effort unchanged. One shared note, not one per arm.
2. **Escalation is a model change, not an effort change** — Step 4.
3. **`D=3` outside the flagship capability list → Sonnet 5.5 at `xhigh`** on the
   Claude arm. (The Codex arm is Sol either way — it has no mid tier to drop to.)
4. **User knowledge:** low/medium on Opus 5.5 is not "waste" — Anthropic
   recommends them "liberally as your primary control for token cost".
5. **No `ultracode` for work under 30 min.** For one-off depth, write
   `ultrathink` into the prompt instead.
6. **Long-session / MCP warning:** each MCP server injects tool schemas into
   every message (GitHub MCP 27 tools ≈ 18k tokens).
7. **Auto-accept warning:** if R≥2, suggest turning auto-accept off.
8. **Alias safety:** `/model opus` → Opus 5.5 on Claude Code v2.1.280+; `/model sonnet` → Sonnet 5.5 on v2.1.284+.

### Fast Mode (1.5x) — the speed line

Codex CLI has a Fast Mode toggle (user-reported, `reference.md` §9.7): output
~**1.5x** faster, quota burns 1.5x, quality unchanged. Claude analogue: `/fast`
— 2.5x faster, **2× price**, **Opus 5.5 / Opus 4.8 only**.

**Append one speed line to every CLI Codex output whose Codex line names a real
model.**

- **`recommended`** — when `R ≤ 1` **and** any of: `D ≤ 1` · the volume/latency
  gate fired · the user asked for speed.
  ```
  ⚡ Fast Mode recommended: Codex Fast Mode (1.5x faster, 1.5x quota) — low-risk / mechanical work.
  ```
- **`available`** — every other case.
  ```
  ⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota).
  ```
  If the Claude line is `Opus 5.5` / `Opus 4.8`, append the Claude half **to the
  `available` form only**: `· Claude /fast (2.5x faster, 2× price).` **Not on
  `opusplan`** — execution drops to Sonnet 5.5, where `/fast` doesn't exist.

**No speed line** when the Codex line names no runnable model, or on a web
surface. It **does** appear when the offensive gate resolves to Astra via stated
Daybreak access.

---

## Output format

**Three lines** — unless Step 0 blocked, which emits the `Clarify:` line alone
(Rule S0).

```
Claude: <Model> · effort: <level>
Codex: ✅ RECOMMENDED AI · <Model> · effort: <level>
Evidence: <one sentence>
```

- The badge sits **immediately after the ecosystem label**, before the model
  name. Exactly one badge per output.
- `Evidence:` is **one sentence** naming at most **1–2** benchmarks or efficiency
  signals — the ones that actually decided it. Not a leaderboard dump.
- **If the badge row you used is marked †, or you used the "anything else" row,
  the sentence must say `low-confidence`.**
- No effort for Haiku 4.5; every Codex model takes an effort.

**Auto-added extras**, each on its own line:

1. `R=3` → **`Do not apply without human review.`** — goes **last**.
2. `opusplan` → the `⚠️ Effort does not carry over` warning, directly under the
   Claude line.
3. **Speed line** — just above the `R=3` note.

If the user asks "why?", *then* expand from `reference.md` §11–§13. Never
unprompted.

### Examples

*"Label these 200 customer reviews as positive/negative"*
```
Claude: Haiku 4.5
Codex: ✅ RECOMMENDED AI · Luna · effort: low
Evidence: Both clear the bar for mechanical classification, and Luna (GPT-6) costs $0.10/$0.50 per MTok against Haiku 4.5's $1/$5 while streaming 124–145 tok/s.
⚡ Fast Mode recommended: Codex Fast Mode (1.5x faster, 1.5x quota) — low-risk / mechanical work.
```

*"Fix this code"*
```
Clarify: which file or function is broken, what does it do now, and what should it do instead?
```
> Step 0 check 3 and check 4. **No `Claude:` / `Codex:` / `Evidence:` line and
> no badge** — Rule S0 overrides "three lines".

*"Refactor the payment module across these 40 files to use the new idempotency-key API, update every caller, and make the test suite pass."*
```
Claude: Sonnet 5.5 · effort: high
Codex: ✅ RECOMMENDED AI · Sol · effort: high
Evidence: AA's Terminal-Bench 4.0 has Sol 56 against Sonnet 5.5's 64 with no interval, and one row is not a direction, so token load decides — ~38k output tokens and $0.72 per task against ~193k and $7.60; low-confidence.
⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota).
```
> **One phase, not four.** Locate the callers, edit, run the existing suite, fix
> what it catches — that is the implementation loop (O1), so **no `ultracode`**
> however many files or minutes it takes. Both arms take `high` from the same
> table: there is no Codex notch.

*"Stand up the new staging environment from scratch: Terraform it, deploy the 12 services, seed the data, run the smoke suite, and fix whatever does not come up."*
```
Claude: ✅ RECOMMENDED AI · Sonnet 5.5 · effort: ultracode
Codex: Sol · effort: high
Evidence: Implementation, a data-seeding phase and a smoke run against a deployed environment are three distinct phases feeding each other, which is what ultracode's orchestration sequences and Codex has no mode for.
⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota).
```
> Three phases at `W=2` — orchestration is not a width question. The coding rows
> fall through to efficiency (Codex †), which is **not** a benchmark direction, so
> the mechanism row wins.

*"Find the race condition that flakes in prod sometimes"*
```
Claude: Opus 5.5 · effort: xhigh
Codex: ✅ RECOMMENDED AI · Sol · effort: xhigh
Evidence: Adversarial debugging is deep-reasoning plus terminal work, and against GPT-6.1 Sol neither row sets a direction (HLE 61 vs 53 but CritPt 32 = 32; Terminal-Bench 60 vs 56), so token load decides — ~38k output tokens per task against ~119k; low-confidence.
⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota) · Claude /fast (2.5x faster, 2× price).
```
> `D=3` by D3DIAG — intermittent *and* timing-dependent. **`xhigh`, not
> `ultracode`:** the session is long and loops through tools, but it is one
> implementation phase. `max` needs one indivisible design decision at `R=3`, and
> a bug hunt is neither.

*"For each of these 120 unrelated vendors, reconcile their sub-processor terms against our DPA and decide whether there is an actual breach — counsel reviews every flag."*
```
Claude: Sonnet 5.5 · effort: ultracode
Codex: ✅ RECOMMENDED AI · Sol Ultra · effort: xhigh
Evidence: 120 vendors reconciled independently is a parallelism problem and Ultra runs ~4 collaborating agents against ultracode's single chain; no coding benchmark applies to contract triage.
⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota).
```
> Dominant tags are `parallel-independent` + `research-synthesis`. There is no
> code and no repo, so Terminal-Bench is **not applicable** (B1) and cannot
> outrank the mechanism. `ultracode` fires on the width limb (`W=3 ∧ D≥2`).

*"Design and implement the new cross-service transaction boundary. It ships tonight and cannot be rolled back."*
```
Claude: ✅ RECOMMENDED AI · Opus 5.5 · effort: max
Codex: Sol · effort: max
Evidence: One indivisible boundary decision at R=3 is the case max exists for; neither the coding nor the reasoning row sets a direction against GPT-6.1 Sol, but at R=3 a lean is not parity and AA's Terminal-Bench 4.0 leans Claude (60 vs 56), so the badge is low-confidence.
⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota) · Claude /fast (2.5x faster, 2× price).
Do not apply without human review.
```
> **`Sol · max`, not Astra.** The old E4 swap is retired: Sol `max` is within a
> point of Astra on the index at a quarter of the cost. **The badge is Claude
> only because `R=3`** — the same task at `R≤2` reads Codex, because one row is
> not a direction and efficiency then decides.

*"Bump `MAX_RETRIES` from 3 to 5 in the prod config"*
```
Claude: Sonnet 5.5 · effort: low
Codex: ✅ RECOMMENDED AI · Sol · effort: low
Evidence: D=0 work — both are far past the bar at the same $2/$10, and Sol's ~38k output tokens per task against Sonnet 5.5's ~193k is measured only at max, not at the rung emitted; low-confidence.
⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota).
Do not apply without human review.
```
> `R=3` by blast radius, not line length — which is also why Haiku/Luna are out.

*"Split this 6000-file legacy Java monolith into independent services"*
```
Claude: Fable 5.1 · effort: max
Codex: ✅ RECOMMENDED AI · Astra · effort: max
Evidence: The boundary design is one indivisible decision at D=3∧R=3, which is what max buys; the 6000-file scale gates both arms to frontier, and against Astra the coding rows are contested (Terminal-Bench 59 vs 59.6 and a tie on the Coding Agent Index, but Vals has Opus 5.5 ahead), so tokens decide (~27k vs ~119k) and the badge is low-confidence.
⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota).
Do not apply without human review.
```
> **`max`, not `ultracode`.** The difficulty is the *boundary decision* — one
> indivisible design call (M1) — even though moving 6000 files is wide. Width is
> execution, not the difficulty, so the indivisible guard blocks `ultracode`.
> "One boundary decision" is also why P1 does **not** make it Sol Ultra.

*"Redesign the auth architecture of 200 prod services from scratch"*
```
Claude: ✅ RECOMMENDED AI · opusplan · plan: max · execute: medium
⚠️ Effort does not carry over — after switching to execution mode set it manually with /effort medium.
Codex: Sol · effort: max
Evidence: Front-loaded architecture design at D=3∧R=3 is opusplan on Claude — the flagship is spent only on a max plan phase and execution drops to Sonnet 5.5 — while Codex has no plan/execute split and takes the same indivisible decision whole as Sol · max.
⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota).
Do not apply without human review.
```
> **Codex is `Sol · max`, not `xhigh`.** opusplan separates the *plan* from the
> mechanical execution on the Claude arm; the design decision itself is still one
> indivisible novel-design call (M1). Codex has no opusplan, so it takes that
> decision whole at `max`. The `deep-reasoning` row falls through to efficiency
> (no direction against Sol), so the `opusplan` mechanism row decides.

---

## If detail is needed

`reference.md`: **§8** example library · **§10** edge-case rulings · **§11**
capability→benchmark map · **§12** comparability record and conflicts · **§13**
efficiency/quota data · **§14** recommended-AI rationale and the ablation ·
**§15** the three-layer evidence architecture · **§16** the reachability audit · **§17** the Claude 5.5 generation (iteration-19) · **§18** the GPT-6.1 Sol generation (iteration-20).

**Three layers; only this file is read at runtime.** `benchmark_frontiers.json`
is generated from `benchmarks.json` for auditing a rule, not for answering one.
**Never load either to route a prompt** — the rules above are their compiled
form.
