---
name: model-secici
description: >-
  Reads a prompt and recommends, separately for Claude (Haiku 4.5 / Sonnet 5.5 /
  Opus 5.5 / Opus 4.8 / Fable 5.1) AND Codex/ChatGPT (Luna / Terra / Sol / Sol
  Ultra / GPT-6 Astra), which model + effort level to run it on, and marks which
  of the two is the better fit for this task — all in one short output. Use when
  asked "which model", "which effort", "pick a model", "which AI should I use",
  "what should I use for this prompt", or when /model-secici is invoked.
---

# Claude & Codex model / effort router

<!-- routing-policy-version: iteration-19 -->

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

**Rosters (verified 29 September 2026).** Claude:

| Model | Role |
|---|---|
| Haiku 4.5 | Speed/volume. **No effort parameter.** 200k context. Retirement "not sooner than 15 Oct 2026"; Haiku 5.5 is announced, **not released — the router does not select it** |
| Sonnet 5.5 | Daily work. **Default starting point.** $2/$10, 1M context. Replaces Sonnet 5 (28 Sep) |
| **Opus 5.5** | **Flagship.** Complex agentic code, enterprise work. $4/$20, 1M context, **API default effort `medium`**. Replaces Opus 5 (22 Sep) |
| Opus 4.8 | Legacy — the **only** lasting role is the offensive-security gate |
| **Fable 5.1** | Frontier scale: long-horizon autonomy, extreme breadth, **biology-adjacent R&D**. $10/$50 |
| Mythos 5.1 | = Fable 5.1 with permissive safeguards. **Project Glasswing invite only** |

Codex/ChatGPT (GPT-5.6 family + GPT-6 Astra):

| Model | Role | Claude analogue |
|---|---|---|
| Luna | Speed/volume, cheapest. Codex CLI default | Haiku 4.5 |
| Terra | Balanced daily driver. **Default starting point** | Sonnet 5.5 |
| **Sol** | **GPT-5.6 flagship** — code/science/security; the `D=3` pick | Opus 5.5 |
| **Sol Ultra** | A Codex *mode* on Sol (Plus+): ~4 collaborating agents. Not a model; `effort:"ultra"` → HTTP 400. Also runs on Astra | — |
| **Astra** | **GPT-6 flagship** (`gpt-6-astra`), 1.05M context. Rare: four gates, plus Rule E4 and the frontier rung. ~2.5× Sol's price, far fewer output tokens | Opus 5.5 / Fable 5.1 |
| *Codex Spark 5.3* | Text-only research preview. **The router does not select it** | — |
| *GPT-6 Sol / GPT-6 Luna* | OpenAI, 22 Sep 2026 ($2/$10 for Sol). **Recorded, not routed** — a different model from the GPT-5.6 Sol above; never call either just "Sol" in evidence | — |

> **`max` on Codex is Astra/Sol only** — a capability limit, not a preference.
> The router cannot emit `Terra · max` even if a rule asked for it.
> **`ultracode` is Claude-only; Ultra is Codex-only.**

---

## Effort levels

| Level | What it does |
|---|---|
| `low` | Short, well-scoped work that needs no intelligence |
| `medium` | Cost-sensitive work. **Codex API default** |
| `high` | **API default** on every effort model **except Opus 5.5** (`medium`) |
| `xhigh` | Deeper reasoning. 30 min+ agentic/coding work |
| `max` | Deepest reasoning. Over-thinking risk. **Codex: Astra/Sol only** |
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
   Rules E1–E4.

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
| **Offensive security** (same definitions) | Deciding | **"use Claude"** — standard access **hard-stops** these tasks (Astra sits at OpenAI's **Critical** cyber level). **Exception:** user states **Daybreak Blue** access → **Astra**, floor `xhigh` |
| **Biology-adjacent R&D** (same definitions) | Deciding | **"unverified — use Claude"**, no model |
| **1000+ files / whole-codebase scale** | Deciding | **Astra** — only Codex model with a verified ≥1M window |
| **≥ ~1M-token corpus / "load the whole repo at once"** | Deciding | **Astra**. Mind the **2× price** above 272k input |
| **Computer use / GUI is the task itself** | Deciding | **Astra** — its one clear published lead. Not for "code that happens to touch a browser" |

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
| **agentic-code** | multi-file implementation, refactor, migration, feature build, debug-and-fix across files | Terminal-Bench 4.0 · CursorBench 3.2.0 |
| **terminal-tool** | terminal/CLI work, build & test loops, tool orchestration, long-horizon execution | Terminal-Bench 4.0 |
| **deep-reasoning** | **architecture from scratch**, algorithm design, mathematics/formal proof, tool-less analysis, adversarial correctness hunting | HLE (tool-less vs tooled) |
| **knowledge-work** | produce a finished document / spreadsheet / deck / memo / filing | GDPval-AA v2 |
| **research-synthesis** | multi-source research, web search, reconciling conflicting sources | AA-Omniscience (via AA Index) |
| **long-context** | read a large corpus, map/summarise across hundreds of pages or a whole repo | AA-LCR v1.1 + the context-window spec |
| **computer-use** | drive a browser or desktop GUI, click through an app, screenshots | OSWorld (⚠️ version + scoring mode) |
| **science** | genomics, chemistry, physics, research engineering, lab pipelines | Terminal-Bench-Science 0.1 |
| **workflow-automation** | wire up business workflows, integrations, multi-tool orchestration | AutomationBench |
| **doc-data-understanding** | scanned documents, PDFs, charts, tables, multimodal extraction | *evidence-poor* |
| **parallel-independent** | 3+ targets or strands that proceed unaware of each other and merge at the end | *product mechanism:* `ultracode` vs Ultra |
| **latency-volume** | sub-second, high-throughput, bulk classification/parsing | output speed + cost/task |
| **instruction-following** | rigid format/schema compliance | never dominant on its own |

> Cybersecurity: **offensive** is a Step 1 gate. **Defensive** hunting is
> `deep-reasoning` (adversarial correctness) plus whichever of `agentic-code` /
> `terminal-tool` the scale demands.
>
> `parallel-independent` is inert below `D=3` — Codex path (a) requires `D=3`
> and the badge table is skipped at `D ≤ 1`.

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
| Otherwise `max(D,C) ≤ 2` | Terra |
| `max(D,C)=3`, `D<3` (C triggered it) | Terra |
| `max(D,C)=3`, `D=3` | In order: **(a)** `P = high` (Rule P1) → **Sol Ultra** — *parallelism, not depth, so it fires for analysis work too and is checked first*. **(b)** same flagship capability list as Claude → **Sol**. **(c)** otherwise (D=3 analytical / research / single-artefact review) → **Terra** |

<!-- rule:P1 -->
**P1 · parallelisable strands.** `P = high` when the work splits into three or more strands that proceed without waiting on each other and merge at the end. A strand may be an already-independent target (service, repo, vendor) or an independent work-kind (three candidate designs investigated or prototyped side by side). Two strands is not enough, and one coherent decision sliced up after the fact is never strands.
<!-- /rule:P1 -->

> Splitting a monolith is plain **Sol** (path b) — one boundary decision; the
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

- **Rung 2.** The user says the work is critical, must not be under-resourced,
  or that an earlier run fell short → **Sonnet 5.5 → Opus 5.5**, **Terra → Sol**,
  same rung. Do *not* crank the mid tier instead: Rules E1/E2 show its top rung
  is dominated by the next tier's ordinary rung on quality *and* quota.

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

<!-- rule:N1 -->
**N1 · Codex +1 notch.** When the task is writing or restructuring code across multiple dependent steps and the model is Terra or Sol, raise the Codex effort one rung, capped at `xhigh` on both models, and never lower a rung that another rule already set higher. Never on Astra. Claude is untouched.
<!-- /rule:N1 -->

> Basis: Terminal-Bench 4.0 (Sol 37.3 vs Opus 5.5 66.4 ±2.6) — the largest
> published Claude-vs-Codex gap in the evidence set. The cap is at
> `xhigh` because the notch compensates for a *model-tier* gap and Rule E3 says
> the top rung is not where you buy that.
>
> **Does NOT apply to:** a **single local addition** — one endpoint, one flag,
> one column, one pattern in one place; code *review* / vulnerability *analysis*
> / reading code to answer; non-code design; mechanical repetition of the same
> edit across files.
>
> **The notch keys on the *fix*, not the diagnosis.** If the hard part is working
> out what is wrong and the resulting change is local, there is no notch.
>
> `Sol Ultra` rides on top of the bumped level.

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
- **"Agentic coding" is not one number.** Terminal-Bench 4.0 puts Sol ~29 points
  behind Opus 5.5; CursorBench 4.0 ~16; FrontierCode 1.1 ~7. Name the benchmark,
  never the label.
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

1. **Published confidence interval** (Terminal-Bench 4.0's owner leaderboard).
2. **Published standard error** → the 95% interval is 2 × SE (TB-Science 0.1:
   SE ±3.5–4.5). An SE published for one benchmark does **not** carry to another.
3. **Repeated-trial variance under one harness.**
4. **A practical-significance threshold the benchmark's own owner publishes.**
5. **None of those → `UNRESOLVED`.** Say so, fall through to efficiency.
   **However large the gap looks.**

> **Score spread is not uncertainty.** "These four span 40–59, so a 7-point gap
> must be real" is a claim about how far apart the models sit, not how precisely
> either was measured — and on a two-model row the spread *is* the gap. After
> this rule `science` is the only capability with a certified direction; the rest
> are `UNRESOLVED`, which makes `low-confidence` the honest word. Detail:
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

Four settled results (AA Index, one harness per version, all rungs comparable):

- **E1 — `Sonnet 5.5 · max` is dominated.** AA v4.3.2: 56 @ $7.60 (~193k output
  tokens/task, the most AA has measured) vs Opus 5.5 `xhigh` 56 @ $3.46 — the
  same score for 2.2× the cost. Anthropic's own footnote adds that Sonnet 5.5
  scores *lower* at `max` than at `xhigh` on FrontierCode. → the router **never**
  emits `Sonnet 5.5 · max`; the escalation target is `Opus 5.5 · xhigh`. *(The
  Sonnet 5 / Opus 5 generation showed the identical shape: 38 @ $5.09 vs 50 @
  $4.88.)* Sonnet 5.5's lower rungs are unpublished — E1 says nothing about them.
- **E2 — `Terra · max` is dominated** (and unavailable). 42 @ $1.40 vs
  `Sol · high` 42 @ $0.81 → the Codex escalation target is **`Sol`**.
- **E3 — `max` over `xhigh` buys little.** Fable 5.1 53 at both rungs; Astra 53
  at both; Opus 5.5 58 vs 56 (+2 for +73% cost/task). → `max` needs M1 in full.
  > The *dominance* holds only where `max` ties `xhigh` — a gain of zero at
  > higher cost, which needs no interval. Opus 5.5's two points are
  > **unresolved**, so holding `max` back there is quota policy, not a free lunch.

<!-- rule:E4 -->
**E4 · Astra swap.** When the dominant capability is agentic-code or terminal-tool and the rules would emit `Sol · max`, emit `Astra · xhigh` instead.
<!-- /rule:E4 -->

  AA Index v4.3: Astra `xhigh` 53 @ $2.31 vs Sol `max` 47 @ $1.99; AA
  Terminal-Bench 4.0 (the only independent source covering both ecosystems)
  Astra 59 vs Sol 40, at ~27k output tokens/task against ~78k.
  > **Capability-scoped on purpose.** Tooled HLE puts Astra **behind** on
  > `deep-reasoning` and GDPval shows a regression on `knowledge-work`, so a
  > `D=3 ∧ R=3` architecture decision stays `Sol · max`. **And it stops at
  > `max`:** widening it downward would compare `Astra · xhigh` with
  > `Sol · xhigh`, a rung AA does not publish. That, not a frequency target, is
  > what keeps Astra rare.

### 5d. Choosing the effort rung

**What is the lowest rung that reaches the capability level this task needs?**
The D table is the starting point; E1–E4 and 5b are the corrections. Round
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
   lacks the required context window, the other arm gets the badge. Stop.
2. **Applicable** task-relevant capability (B1), from the dominant tag's anchor.
3. **Benchmark confidence** — tier, date, harness, and *who ran it*. An
   independent evaluator outranks a vendor's own table. A vendor result favouring
   the **competitor** is against-interest and is the most credible vendor
   evidence there is.
4. **Near-parity check** (5b). Inside the band → go to 5.
5. **Token / quota efficiency** (5c order). 6. **Cost per task.** 7. **Latency.**

"Claude has the better general intelligence index" is **not** on its own a
reason to pick Claude, and the mirror-image claim is not a reason to pick Codex.

### Badge table — dominant capability → default side

**Conditional on which Codex model is on the line.** A capability can favour
Claude against Sol and not against Astra.

| Dominant capability | vs **Terra / Sol** | vs **Astra** | Evidence to name |
|---|---|---|---|
| `agentic-code` | **Claude** | **Codex** † | TB 4.0: Opus 5.5 66.4 (SE ±2.6) vs Sol 37.3. Against Astra it is a tie — AA TB 4.0 Astra 60 vs Opus 5.5 59.6, Coding Agent Index 62 = 62 — so tokens decide: Astra ~27k output tokens/task vs Opus 5.5 ~119k |
| `terminal-tool` | **Claude** | **Codex** † | same TB 4.0 row (the vendor's Opus-`xhigh`-vs-Astra-`high` gap is unmatched, so it sets nothing) |
| `science` | **Claude** | **Codex** † | TB-Science 0.1: 58.7 vs Sol 22.4; vs Astra 64.6 is inside the ±5 band → parity, tokens decide |
| `knowledge-work` † | **Claude** | **Claude** † | GDPval-AA v2.1: Opus 5.5 1846 vs Astra 1542 / Sol 1588 (no interval published) |
| `workflow-automation` † | **Claude** | **Codex** † | AutomationBench: Opus 5.5 40.0 vs Sol 28.8; vs Astra 41.4 is a tie |
| `computer-use` † | **Claude** | **Codex** | OSWorld 2.0 offline partial: Astra 72.6 vs Sol 65.7 |
| `latency-volume` | **Codex** | **Codex** | Luna 112 tok/s @ $0.18 vs Haiku 4.5 85 @ $0.21 |
| `parallel-independent` | **Codex** | **Codex** | Ultra runs ~4 collaborating agents; `ultracode` is one chain |
| `long-context` (shallow) | **Claude** | **Claude** | Sonnet 5.5's 1M window at $2/$10 vs Astra $10/$50 |
| `deep-reasoning` † | **Claude** | **Claude** | Tooled HLE, published by OpenAI and favouring the competitor: Opus 5.5 67.7 · Fable 5.1 65.0–65.6 · **Astra 57.2** |
| `research-synthesis` †, `doc-data-understanding` † | **Claude** | **Claude** | no cross-ecosystem row at all |
| anything else / no evidence | the **lighter** chosen model × effort | same | say `low-confidence` |

> **† — the Evidence line must say `low-confidence`.** A † after the capability
> name binds the whole row; a † inside a cell binds that cell only
> (`agentic-code` vs Sol carries none, vs Astra it does). So must the "anything
> else" row. Check this against the cell you actually used before emitting.

**Tie-breaks**

- **`D ≤ 1` → skip the capability rows entirely; efficiency decides.** Both arms
  clear the bar by construction. **Haiku 4.5 vs Luna → Codex**; **Sonnet 5.5 vs
  Terra → Claude** ($2/$10 vs $2/$12). `R` doesn't change this.
- **Two *dominant* capability rows conflict** → the one backed by a
  task-specific benchmark beats one backed only by a product mechanism. Both
  rows must be dominant tags for this prompt (B1) — a benchmark for a capability
  this task does not need has already been excluded and cannot break the tie.
  *(A 180-service defensive audit is `terminal-tool` + `parallel-independent`:
  TB 4.0 outranks Ultra mode → Claude. A 120-vendor contract triage is
  `parallel-independent` + `research-synthesis`: no code, no repo, so TB 4.0 is
  not applicable at all → Ultra's mechanism decides → Codex.)*
- Both arms gated to the same conclusion → no badge. Step 0 blocked → no badge.
- **Genuinely insufficient evidence:** give the more sensible default, with
  `low-confidence` in the Evidence line. Never manufacture certainty.

---

## Step 7 — Quota-protection and accuracy rules

Rationale in `reference.md` §10.5. **Only Rule 1's note is auto-added.**

1. **R=3 → human-review note** ("Do not apply without human review."). Model and
   effort unchanged. One shared note, not one per arm.
2. **Escalation is a model change, not an effort change** — Step 4.
3. **`D=3` outside the flagship capability list → mid-tier default** (Sonnet 5.5 /
   Terra) at `xhigh`.
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
Evidence: Both clear the bar for mechanical classification, and Luna runs ~30% faster per token at slightly lower cost per task.
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
Claude: ✅ RECOMMENDED AI · Sonnet 5.5 · effort: high
Codex: Terra · effort: xhigh
Evidence: Agentic multi-file coding is Claude's strongest published margin (Terminal-Bench 4.0: Opus 5.5 66.4 and Sonnet 5.5 70.6 vs Sol 37.3), and a D=2 job does not need the flagship; Codex takes the +1 notch to xhigh.
⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota).
```
> **One phase, not four.** Locate the callers, edit, run the existing suite, fix
> what it catches — that is the implementation loop (O1), so **no `ultracode`**
> however many files or minutes it takes.

*"Stand up the new staging environment from scratch: Terraform it, deploy the 12 services, seed the data, run the smoke suite, and fix whatever does not come up."*
```
Claude: ✅ RECOMMENDED AI · Sonnet 5.5 · effort: ultracode
Codex: Terra · effort: xhigh
Evidence: Implementation, a data-seeding phase and a smoke run against a deployed environment are three distinct phases feeding each other, which is what ultracode's orchestration buys; Codex takes the +1 notch.
⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota).
```
> Three phases at `W=2` — orchestration is not a width question.

*"Find the race condition that flakes in prod sometimes"*
```
Claude: ✅ RECOMMENDED AI · Opus 5.5 · effort: xhigh
Codex: Sol · effort: xhigh
Evidence: Adversarial debugging inside a repo leans on the terminal/agentic profile where Claude leads against Sol; max needs one indivisible design decision at R=3, and a bug hunt is neither.
⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota) · Claude /fast (2.5x faster, 2× price).
```
> `D=3` by D3DIAG — intermittent *and* timing-dependent. **`xhigh`, not
> `ultracode`:** the session is long and loops through tools, but it is one
> implementation phase. No notch either — the fix is local.

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
Claude: Opus 5.5 · effort: max
Codex: ✅ RECOMMENDED AI · Astra · effort: xhigh
Evidence: One indivisible boundary decision at R=3 is the case max exists for, but on agentic code Astra xhigh outscores Sol max (AA Index v4.3: 53 @ $2.31 vs 47 @ $1.99) at roughly a third of the output tokens; against Opus 5.5 the coding rows are a tie, so the badge is low-confidence.
⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota) · Claude /fast (2.5x faster, 2× price).
Do not apply without human review.
```
> The **only** non-gate route to Astra (E4). Change the capability to
> architecture or a written deliverable and it stays `Sol · max`.

*"Bump `MAX_RETRIES` from 3 to 5 in the prod config"*
```
Claude: ✅ RECOMMENDED AI · Sonnet 5.5 · effort: low
Codex: Terra · effort: low
Evidence: D=0 work — both are far past the bar, and Sonnet 5.5 is the cheaper of the two daily drivers on output tokens.
⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota).
Do not apply without human review.
```
> `R=3` by blast radius, not line length — which is also why Haiku/Luna are out.

*"Split this 6000-file legacy Java monolith into independent services"*
```
Claude: Fable 5.1 · effort: max
Codex: ✅ RECOMMENDED AI · Astra · effort: max
Evidence: The boundary design is one indivisible decision at D=3∧R=3, which is what max buys; the 6000-file scale gates both arms to frontier, and Astra ties Opus 5.5 on the coding rows, so the badge is low-confidence.
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
Evidence: Front-loaded architecture design (deep-reasoning) at D=3∧R=3 is opusplan on Claude with a max plan phase; Codex has no plan/execute split, so the same indivisible design decision is Sol · max (low-confidence).
⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota).
Do not apply without human review.
```
> **Codex is `Sol · max`, not `xhigh`.** opusplan separates the *plan* from the
> mechanical execution on the Claude arm; the design decision itself is still one
> indivisible novel-design call (M1). Codex has no opusplan, so it takes that
> decision whole at `max`. `deep-reasoning`, so E4 does not fire.

---

## If detail is needed

`reference.md`: **§8** example library · **§10** edge-case rulings · **§11**
capability→benchmark map · **§12** comparability record and conflicts · **§13**
efficiency/quota data · **§14** recommended-AI rationale and the ablation ·
**§15** the three-layer evidence architecture · **§16** the reachability audit · **§17** the Claude 5.5 generation (iteration-19).

**Three layers; only this file is read at runtime.** `benchmark_frontiers.json`
is generated from `benchmarks.json` for auditing a rule, not for answering one.
**Never load either to route a prompt** — the rules above are their compiled
form.
