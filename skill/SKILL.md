---
name: model-secici
description: >-
  Routes a prompt: which model + effort on Claude (Haiku 4.5 / Sonnet 5.5 /
  Opus 5.5 / Opus 4.8 / Fable 5.1) and on OpenCode Go (best two of its 15 main
  models, each with an effort), and which ecosystem fits better. Use for "which
  model / effort / AI should I use" or /model-secici.
---

# Claude & OpenCode Go model / effort router

<!-- routing-policy-version: iteration-21 -->

Route the user's prompt — **do not run it**. Say which model + effort to use on
**Claude** and on **OpenCode Go** (**two** models, `#1` / `#2`, each with its own
effort), then mark the better-fit ecosystem `✅ RECOMMENDED AI`.

**Principle.** Pick the lowest-quota model × effort that stays on the task's
capability frontier: the stronger candidate when the task-relevant gap is
meaningful, the more quota-efficient one when capability sits inside a
defensible band. Not "always cheapest", not "always strongest". Protected
resources: Claude's 5-hour window and each Go model's **own** dollar cap (plan
USD 10/month; 5-hour window = 20% of a model's cap, weekly 50%). When in doubt,
round **down**.

**Run Steps 0–6 in one pass, silently.** If Step 0 is clean and no gate fires,
score once — do not re-derive. Emit only the output lines. `opencode-benchmarks.md`
and `reference.md` (its Codex §9/§18 are stale) are audit data — never load them
to route.

**Claude roster (6 Oct 2026):**

| Model | Role |
|---|---|
| Haiku 4.5 | Speed/volume. **No effort parameter.** 200k context. Retires "not sooner than 15 Oct 2026"; Haiku 5.5 is announced, **not released — never selected** |
| Sonnet 5.5 | Daily work, **default start**. USD 2/USD 10, 1M |
| **Opus 5.5** | **Flagship** for complex agentic code. USD 4/USD 20, 1M, API default effort `medium` |
| Opus 4.8 | Legacy — only role: the offensive-security gate |
| **Fable 5.1** | Frontier scale (1000+ files), biology-adjacent R&D. USD 10/USD 50 |
| Mythos 5.1 | = Fable 5.1, permissive safeguards, **Glasswing invite only** |

**OpenCode Go pool — the 15 main models** (plan: Go, USD 10/month). `II` = AA
Intelligence Index v4.3.2 (Max unless noted), `TB` = AA Terminal-Bench 4.0,
`USD/task` = AA cost per index task, `cap` = Go monthly cap per model. Full data,
contexts and sources: `opencode-benchmarks.md`.

| # | Model | II | TB | USD/task | cap | Notes |
|---|---|---|---|---|---|---|
| 1 | **MiMo-V2.6-Pro** | **46** | 35 | **0.13** | 15 | **Default.** Best index per dollar; tops HLE/CritPt/SciCode; slow; **no effort variant** |
| 2 | **GLM-5.3** | 45 | **42** | 2.01 | 15 | Best measured coder; text-only |
| 3 | **Kimi K3** | 44 | 13 | 2.00 | 15 | Best AA-LCR 89 / Omniscience 20 / GDP.pdf 22; weak agentic; `max` only; tightest cap |
| 4 | **Grok 4.7** | 46 | 26 | 3.74 | 15 | Knowledge-work leader; **30-day retention**; 500k context |
| 5 | **Muse Spark 1.3 Contributor** | **48** | 33 | ~0.10 | 60 | **Trains on your prompts** — NC1 only |
| 6 | **GLM-5.3-Flash** | 42 | 33 | 0.25 | 60 | **`D ≤ 1` #1**; text + image |
| 7 | **MiMo-V2.6-Flash** | 38 | 23 | **0.06** | 60 | Cheapest; no effort variant |
| 8 | **DeepSeek V4.1 Flash** | 39 | 27 | 0.27 | 60 | 222 tok/s; **AutomationBench-AA 69**; peak hours 2× |
| 9 | **GPT 6 Luna** | 38 | 13 | 0.07 | 15 | Fast bulk; **30-day retention**; never agentic |
| 10 | **Qwen3.8 Flash** | 40 | 25 | 0.37 | 30 | Briefcase 1583 → knowledge-work #2; 256k context |
| 11 | **Qwen3.8 Max** | 45 | 39 | 5.41 | 15 | Escalation only (A1-OC) |
| 12 | DeepSeek V4 Pro | 36 | 14 | 0.67 | 15 | **Dominated** by V4.1 Flash |
| 13 | MiniMax M3 | 29 | 2 | 0.51 | 60 | **Dominated** |
| 14 | Kimi K2.7 Code | 26 | 1 | 0.54 | 60 | **Dominated** |
| 15 | Qwen3.7 Plus | 25 | 1 | 0.22 | 60 | **Dominated** |

Rows 12–15 are rated but no row emits them — if a task already runs on one, name
the pool model that replaces it. DeepSeek's zero-retention agreement is **renewed
monthly (valid through 31 Oct 2026)**. **Never selected** (legacy, preview, free,
vision-experimental or unmeasured): Grok 4.6, GPT 5.6 Luna, GLM-5.2, Kimi K2.6,
MiMo-V2.5, MiMo-V2.5-Pro, Muse Spark 1.2, MiniMax M2.7, DeepSeek V4 Flash,
DeepSeek V4 Flash Vision Exp, Hy4 Preview, LongCat 2.5 Preview, LongCat-2.0, Hy3,
Space Bunny. Model ids: `opencode-go/<model-id>`.

---

## Effort levels

### Claude

| Level | What it does |
|---|---|
| `low` | Short, well-scoped work that needs no intelligence |
| `medium` | Cost-sensitive work |
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

### OpenCode Go

OpenCode shows only the effort **variants its model catalogue (models.dev, `opencode-go`
provider, read 6 Oct 2026) lists for each model** — and they differ:

| Model | Variants OpenCode offers | Emit |
|---|---|---|
| GLM-5.3 · GLM-5.3-Flash · DeepSeek V4.1 Flash | `low` · `high` · `max` | `D ≤ 1` `low` · `D = 2` `high` · `D = 3` `max` |
| MiMo-V2.6-Pro · MiMo-V2.6-Flash | **none** — thinking is always on | `default` |
| Kimi K3 | `max` only | `max` |
| Grok 4.7 | `low` · `medium` · `high` · `xhigh` | `xhigh` (the rung AA measured) |
| Qwen3.8 Flash · Qwen3.8 Max | `low` · `medium` · `xhigh` (+ toggle, token budget) | `xhigh` (the API default) |
| GPT 6 Luna | `none` … `max` | `low` (latency row only) |
| Muse Spark 1.3 Contributor | `minimal` … `xhigh` | `xhigh` (NC1 only) |

`medium` and `xhigh` are **rejected** on the `low`/`high`/`max` models, and `max` does not
exist on Grok or Qwen — never write a rung the model does not list. OpenCode cycles
variants with `variant_cycle`. **Never interpolate a rung between two measured ones.**

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
**S0 · blocked output.** A prompt blocked at Step 0 emits exactly one line, a `Clarify:` line naming the missing information as a question, and no `Claude:`, `OpenCode:`, `Evidence:` or badge line at all.
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

### OpenCode arm

| Condition | Kind | Result |
|---|---|---|
| **Offensive security** (same definitions) | Deciding | **"use Claude"** — the only open-model offensive evidence is vendor-reported (Z.ai's GLM-5.3 ExploitBench 54.4 vs Kimi K3 32.2, no independent row) and no pool model's safeguards are verified. No OpenCode models on the line |
| **Biology-adjacent R&D** | Deciding | **"unverified — use Claude"**, no model |
| **Computer-use (GUI driving)** | Deciding | **"unverified — use Claude"** — no pool model has a published OSWorld row |
| Context > 500k tokens | Eliminating | **Grok 4.7 removed** |
| Context > 256k tokens | Eliminating | **Qwen3.8 Flash removed** |
| Task needs **image input** | Eliminating | **GLM-5.3 removed** (text-only) |
| Work is **confidential** — the default for this user (company code, data, plans) | Eliminating | **Muse Spark 1.3 Contributor removed** (trains on prompts); **Grok 4.7 and GPT 6 Luna removed** (30-day retention; every other pool model is 0-day). Lifted only by Rule NC1 |
| Sub-second latency / high-volume bulk | Deciding | **DeepSeek V4.1 Flash #1 · MiMo-V2.6-Flash #2** (NC1: **GPT 6 Luna** #2), effort `low` |

<!-- rule:NC1 -->
**NC1 · non-confidential unlock.** Only when the user says the work is non-confidential or personal: Grok 4.7 and GPT 6 Luna stay in the pool (30-day retention is accepted), and Muse Spark 1.3 Contributor may take `#2` on `deep-reasoning`, `science` and `research-synthesis` rows (HLE 49 = MiMo-V2.6-Pro, AA-Omniscience 25 vs Kimi K3 20, USD 60 cap against USD 15). Never infer non-confidentiality from the prompt's tone.
<!-- /rule:NC1 -->

> **Defensive security work does not trigger the offensive gate — on either arm,
> at any scale.** "Audit this code for vulnerabilities", "find open ports",
> "audit 180 services for auth-bypass bugs (no exploits)" → normal scoring. Only
> exploit / PoC *generation* is gated.
>
> **Frontier-scale gate — one signal only: the file count (1000+).** 100–999
> files does **not** gate; that is `W=3` under normal scoring. It gates the
> **Claude arm only**; the OpenCode arm scores 1000+ files normally (every pool
> window is ≤ 1M, so check the context gate above).
>
> **Stated access does not penalise a candidate.** An access tier decides
> whether a candidate *exists*, not whether it wins. Once the user says they
> have Glasswing access, compare that candidate on capability like any other —
> Step 6 runs normally.

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
| **agentic-code** | multi-file implementation, refactor, migration, feature build, debug-and-fix across files | AA Terminal-Bench 4.0 · DeepSWE |
| **terminal-tool** | terminal/CLI work, build & test loops, tool orchestration, long-horizon execution | AA Terminal-Bench 4.0 |
| **deep-reasoning** | **architecture from scratch**, algorithm design, mathematics/formal proof, tool-less analysis, adversarial correctness hunting | AA HLE · CritPt |
| **knowledge-work** | produce a finished document / spreadsheet / deck / memo / filing | GDPval-AA v2.1 · AA-Briefcase |
| **research-synthesis** | multi-source research, web search, reconciling conflicting sources | AA-Omniscience index |
| **long-context** | read a large corpus, map/summarise across hundreds of pages or a whole repo | AA-LCR v1.1 + the context-window spec |
| **computer-use** | drive a browser or desktop GUI, click through an app, screenshots | OSWorld (⚠️ version + scoring mode) — gated on the OpenCode arm |
| **science** | genomics, chemistry, physics, research engineering, lab pipelines | SciCode · Terminal-Bench-Science |
| **workflow-automation** | wire up business workflows, integrations, multi-tool orchestration | AutomationBench-AA |
| **doc-data-understanding** | scanned documents, PDFs, charts, tables, multimodal extraction | AA GDP.pdf (one independent row) |
| **parallel-independent** | 3+ targets or strands that proceed unaware of each other and merge at the end | *no product mechanism on either arm now* |
| **orchestration** | three or more distinct phases in one session (Rule O1) | *product mechanism:* `ultracode` (Claude) |
| **latency-volume** | sub-second, high-throughput, bulk classification/parsing | output speed + cost/task |
| **instruction-following** | rigid format/schema compliance | never dominant on its own |

> Cybersecurity: **offensive** is a Step 1 gate. **Defensive** hunting is
> `deep-reasoning` (adversarial correctness) plus whichever of `agentic-code` /
> `terminal-tool` the scale demands.
>
> `parallel-independent` is **inert**: Codex Ultra is gone and neither arm has a
> mechanism for it. Route by the underlying tag.
>
> `orchestration` is a tag only when **O1** fires — the *width* limb of UC1
> (`W=3 ∧ D≥2`) is execution breadth, not phase sequencing, and does not make it
> dominant. It names something only the Claude arm's product has.

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

### Claude

**Model** ← `max(D, C)`. **The flagship is a candidate only when `D=3`** —
`C=3` alone (large but shallow synthesis) stays mid-tier.

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

**Effort ← D** (Claude):

| D | Effort |
|---|---|
| 0 | `low` · 1 `medium` · 2 `high` · 3 `xhigh` |

<!-- rule:M1 -->
**M1 · `max`.** Emit `max` only when `D = 3` and `R = 3` and the model is a flagship (Opus 5.5 / Opus 4.8 / Fable 5.1 / Mythos 5.1) and the difficulty is one indivisible novel-design or formal decision. Otherwise `xhigh`.
<!-- /rule:M1 -->

> For review, audit, migration or breadth-driven work at `D=3 ∧ R=3`, stop at
> **`xhigh`** — the R=3 human-review note carries the stakes. Rationale: Rule E3.

Haiku 4.5 selected → leave the effort field blank.

**Escalation — a model change, never an effort change.** The user says the work
is critical, must not be under-resourced, or that an earlier run fell short →
**Sonnet 5.5 → Opus 5.5**, same rung. Do *not* crank the mid tier instead: Rule E1
shows its top rung is dominated by the next tier's ordinary rung on quality *and*
quota.

<!-- rule:A1 -->
**A1 · frontier rung.** Opus 5.5 becomes Fable 5.1 only when the dominant capability is on the flagship list and `A = high`, where `A = high` means the user states that an earlier flagship-tier run at `xhigh` or `max` already fell short. A long or unattended session is not that statement.
<!-- /rule:A1 -->

> Difficulty alone never reaches the frontier rung — and neither does duration.
> Anthropic's own same-harness table has Opus 5.5 at or above Fable 5.1 on all
> eight benchmarks it lists (Terminal-Bench 4.0 66.4 vs 55.8, the long-horizon
> one included) at less than half the price, so "it runs for hours" is an Opus
> 5.5 job. The frontier rung keeps only Anthropic's published step-up criterion:
> a stated `xhigh`/`max` shortfall. *(The 1000+-file scale gate above is
> unchanged — no evidence exists at that scale either way; `reference.md` §17.)*

#### Claude arm modifiers

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

#### `opusplan` — plan/execute model split

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

### OpenCode Go — Step 4-OC: pick two models, then efforts

**1.** Step 1 OpenCode gates. **2.** `D ≤ 1` → first row. **3.** Otherwise the
dominant tag's row, left column for `D ≤ 2 ∧ R ≤ 2`, right column for `D = 3` or
`R = 3` (Rule PO1). **4.** Rule CAP1. **5.** Effort for each (below).

| Dominant capability | `R ≤ 2` → `#1` · `#2` | `D = 3` or `R = 3` → `#1` · `#2` | Evidence (AA v4.3.2) |
|---|---|---|---|
| **any tag, `D ≤ 1`** | GLM-5.3-Flash · MiMo-V2.6-Flash | same | both clear the bar; price and USD 60 caps decide |
| `agentic-code`, `terminal-tool` | MiMo-V2.6-Pro · GLM-5.3 | **GLM-5.3 · MiMo-V2.6-Pro** | TB 4.0 GLM-5.3 42 vs MiMo 35, one row → cap pressure (USD 0.13 vs 2.01); leader first at depth † |
| `deep-reasoning` | MiMo-V2.6-Pro · Kimi K3 | same | HLE 49/47/42 and CritPt 27/23/19 — **two AA rows agree** |
| `knowledge-work` | MiMo-V2.6-Pro · Qwen3.8 Flash | same | GDPval MiMo, Briefcase Qwen Flash → rows split; Kimi K3 last (1537/1501). **NC1: Grok 4.7 · MiMo-V2.6-Pro** — Grok leads both (1715/1644) † |
| `workflow-automation` | DeepSeek V4.1 Flash · GLM-5.3 | same | AutomationBench-AA 69 vs 62 vs 59, one row † |
| `long-context`, `research-synthesis`, `doc-data-understanding` | MiMo-V2.6-Pro · Kimi K3 | **Kimi K3 · MiMo-V2.6-Pro** | AA-LCR 86/89, Omniscience 8/20, GDP.pdf 19/22 — one row each; leader first at depth †. Images: Kimi or MiMo (GLM-5.3 is text-only) |
| `science` | MiMo-V2.6-Pro · Kimi K3 | same | SciCode 61 vs 59, one row † |
| `latency-volume` | DeepSeek V4.1 Flash · MiMo-V2.6-Flash | same | 222 / 62 tok/s; NC1: GPT 6 Luna as #2 (147 tok/s) |
| `orchestration`, `parallel-independent` | by the *underlying* tag | | `ultracode` lives on the Claude line |
| anything else | MiMo-V2.6-Pro · GLM-5.3-Flash | same | no row → best index per dollar † |

**† = Evidence must say `low-confidence`.** **Two dominant tags:** `#1` from the row
whose tag decided the badge (else the first named); `#2` = the other row's `#1`, or
its `#2` if that is the same model.

<!-- rule:PO1 -->
**PO1 · pair order.** At `D ≤ 2` and `R ≤ 2` the efficient model goes first; at `D = 3` or `R = 3` the leader on the dominant capability's anchor benchmark goes first (the right-hand column). This orders the pair only — the badge still follows BD1.
<!-- /rule:PO1 -->

<!-- rule:CAP1 -->
**CAP1 · cap rule.** The USD 15-cap models (MiMo-V2.6-Pro, GLM-5.3, Kimi K3, Grok 4.7, Qwen3.8 Max, GPT 6 Luna) are reserved for `D ≥ 2`; `D ≤ 1` goes to the USD 60-cap Flash tier (the `latency-volume` row is exempt). Caps are per model: when the user says a model's window is exhausted, name the next model of its chain in `Evidence:` only — Pro **MiMo-V2.6-Pro → GLM-5.3 → Kimi K3 → Qwen3.8 Max**; Flash **GLM-5.3-Flash → MiMo-V2.6-Flash → DeepSeek V4.1 Flash → Qwen3.8 Flash**.
<!-- /rule:CAP1 -->

<!-- rule:A1-OC -->
**A1-OC · escalation rung.** When the user states that an earlier OpenCode run fell short, `#2` becomes **Grok 4.7** (non-confidential, NC1) or **Qwen3.8 Max** (confidential), only for `agentic-code`, `terminal-tool` and `knowledge-work`, with `low-confidence` (Qwen3.8 Max: TB 39, Briefcase 1621, USD 5.41 per task; Grok 4.7: TB 26, USD 3.74 per task, 30-day retention). If the shortfall was at `D=3`, also say the Claude line is stronger.
<!-- /rule:A1-OC -->

> A shortfall escalates only the arm it happened on.

#### OpenCode Go — effort for each model

Use the variants table under *Effort levels*. On the three `low`/`high`/`max`
models: `D ≤ 1` `low` · `D = 2` `high` · `D = 3` `max`. Every other model has one
rung to write.

> **E7.** `high` at `D=2`: DeepSeek's V4.1-Flash paper has effort 60–80 recovering
> most of `max`'s accuracy at under half its tokens (the last step adds 1.6–1.8×
> agent tokens for marginal gains); Z.ai's Code Bench has GLM-5.3 `high` 31.4% at
> ~50k tokens vs `max` 34.5% at ~75k. Vendor, own-model curves: they pick a rung,
> never a direction. `max` at `D=3`: AA GLM-5.3 `low` 34 → `max` 45, Kimi K3 30 → 44
> (E5), at a verbosity cost on a per-model cap. `GLM-5.3 · low` is dominated (E6);
> `low` on a Flash model has no number and is used only at `D ≤ 1`.

---

## Step 5 — Evidence, equivalence, efficiency

**Comparable only if** benchmark, version, harness, tools, scaffold and effort all
match — else `not directly comparable`. AA Index versions never mix (all figures
v4.3.2); vendor tables never pool with AA; AA's Coding Agent Index is a harness ×
model aggregate containing TB 4.0 → context only, never a direction; AA prices ≠ Go
prices; one figure on two pages is one number; saturated benchmarks (TB 2.1,
SWE-bench Verified) are unused. **Never interpolate between rungs, never invent a
number — `n/p` is an answer.**

**"Meaningfully better" needs a published interval, standard error, repeated-trial
variance or an owner-published threshold. AA publishes none, so every open-vs-open
and Claude-vs-open cell is `UNRESOLVED` however large the gap looks** — only BD1, or
at `R=3` a single measurement, sets a direction (Sonnet 5.5's 64 vs GLM-5.3's 42 on
TB 4.0 is a *lean*). Score spread is not uncertainty. At `R=3` widen the bar; if
unsure take the stronger candidate.

**Dominance** — A dominates B if A is not meaningfully worse on the task capability
and clearly better on one axis, in order; a dominated candidate is never emitted.
Claude arm and badge: reasoning tokens → output tokens → total tokens → tokens per
successful task → quota pressure → cost → latency. OpenCode (open vs open): **Go cap
pressure** (cost/task ÷ cap, then the 5-hour output-token budget) → reasoning tokens
→ output tokens → latency.

- **E1** `Sonnet 5.5 · max` (56 @ USD 7.60, ~193k tokens) is dominated by `Opus 5.5 · xhigh` (56 @ USD 3.46); Anthropic's footnote: Sonnet scores *lower* at `max` on FrontierCode. Never emit it; escalate to `Opus 5.5 · xhigh`.
- **E3** `max` over `xhigh` buys little on Claude (Fable 5.1 53 = 53; Opus 5.5 58 vs 56, +73% cost) → `max` needs M1.
- **E5** open models are the exception: `max` buys +11 (GLM-5.3 34 → 45) and +14 (Kimi K3 30 → 44), so `D = 3 → max`; `D = 2 → high` (E7).
- **E6** dominated, never emitted: `GLM-5.3 · low` (→ GLM-5.3-Flash 42 @ 0.25), `Kimi K3 · low` (→ MiMo-V2.6-Flash; OpenCode offers Kimi `max` only), DeepSeek V4 Pro (→ V4.1 Flash), MiniMax M3 / Kimi K2.7 Code / Qwen3.7 Plus (TB 2/1/1), Qwen3.8 Max (→ MiMo-V2.6-Pro) except via A1-OC. Grok 4.7 and GPT 6 Luna are not dominated — retention *eliminates* them.

**Effort rung:** the lowest rung that reaches the capability the task needs; round
down when the next rung is inside the band, never when the low→high gap is real.

---

## Step 6 — `✅ RECOMMENDED AI`

Compare the **Claude line** with **OpenCode `#1`**; mark exactly one ecosystem. The
badge is computed, never habitual.

<!-- rule:B1 -->
**B1 · evidence applicability.** A benchmark row takes part in the badge decision only if the capability it measures is one of the dominant tags named for this prompt in Step 2. Applicability is checked before evidence quality and before any tie-break, and a row that is not applicable does not enter the comparison at all, however strong its number.
<!-- /rule:B1 -->

**Order:** (1) hard gate — if one arm declines or lacks the context window, the
other gets the badge, stop; (2) applicable capability (B1; `orchestration` and
`opusplan` are mechanism tags and applicable); (3) source confidence — independent
evaluator (AA) > vendor table, a vendor result favouring its *rival* is the most
credible vendor evidence; (4) BD1; (5) near-parity (Step 5); (6) token/quota
efficiency; (7) cost; (8) latency.

<!-- rule:BD1 -->
**BD1 · direction without an interval.** A badge direction needs at least two independent measurements that agree — an independent evaluator's run, or a vendor's table that favours its rival — at least one of them tier A or B, and none that disagree. The same benchmark re-published on a second page is one measurement, a tie is not opposition, and an aggregate never counts. Otherwise the cell is decided by efficiency, except at R = 3, where a single admissible measurement still decides it: a lean is not parity.
<!-- /rule:BD1 -->

<!-- rule:MECH1 -->
**MECH1 · mechanism rows.** `ultracode` driven by `O = high`, or a task routed to `opusplan`, names something OpenCode does not have, so it decides the badge for Claude unless the other capability row carries a benchmark direction under BD1, which wins.
<!-- /rule:MECH1 -->

A higher general index (Claude 58/56 vs 46) or a 15–60× lower task cost (OpenCode)
is not a reason on its own. A row that falls to efficiency reads **OpenCode †**
(AA output tokens per task: MiMo 64k, GLM-5.3 71k vs Opus 5.5 119k, Sonnet 5.5
193k); only a BD1 direction, a mechanism or `R=3` moves the badge to Claude.

### Badge table

| Dominant capability | `R ≤ 2` | `R = 3` | Evidence to name |
|---|---|---|---|
| `agentic-code`, `terminal-tool` (`D ≥ 2`) | **OpenCode** † | **Claude** † | TB 4.0 Sonnet 5.5 64 / Opus 5.5 60 vs GLM-5.3 42 / MiMo 35, one row, no interval → tokens/cost (64k vs 193k; USD 0.13 vs 7.67) |
| `knowledge-work` | **Claude** | **Claude** | GDPval-AA 1866/1839 vs Grok 1715 / MiMo 1686; AA-Briefcase 1807/1823 vs 1644/1516 — two AA rows agree |
| `deep-reasoning` | **Claude** | **Claude** | HLE 61/55 vs MiMo 49; CritPt 32/31 vs 27 — two AA rows agree |
| `workflow-automation` | **OpenCode** † | **Claude** † | AutomationBench-AA Sonnet 72 / Opus 70 vs DeepSeek V4.1 Flash 69 — one row |
| `science` | **OpenCode** † | **Claude** † | SciCode Opus 67 / Sonnet 61 vs MiMo 61 — one row, a tie with Sonnet |
| `long-context` (shallow) | **OpenCode** † | **OpenCode** † | AA-LCR Kimi 89 / MiMo 86 vs Opus 85 / Sonnet 83 — one row, open models ahead |
| `research-synthesis` | **OpenCode** † | **Claude** † | AA-Omniscience Sonnet 32 / Opus 46 vs Kimi 20 / MiMo 8 — one row |
| `doc-data-understanding` | **OpenCode** † | **Claude** † | GDP.pdf Opus/Sonnet 26 vs Kimi 22 / MiMo 19 — one row |
| `latency-volume` | **OpenCode** | **OpenCode** | DeepSeek V4.1 Flash 222 tok/s, TTFT 1.1 s, USD 60 cap vs Haiku 4.5 USD 1/USD 5 (facts, not a score) |
| `orchestration`, or a task routed to `opusplan` | **Claude** | **Claude** | `ultracode` sequences phases, `opusplan` spends the flagship on the plan; OpenCode has neither |
| anything else | the **lighter** model × effort | same | say `low-confidence` |

**† → Evidence must say `low-confidence`** (binds that row; so does "anything else").
Mechanism and `latency-volume` rows carry none. At `R=3` a row that fell to efficiency
follows its single measurement's lean and keeps its †.

**Tie-breaks.** `D ≤ 1` → skip capability rows; price and cap decide → **OpenCode**
(Haiku 4.5 or Sonnet 5.5 vs the Flash tier; no †, like latency; `R` doesn't change
it). Two dominant rows conflict → a benchmark **direction** beats a mechanism or an
efficiency fall-through. Both arms gated alike or Step 0 blocked → no badge.
Genuinely thin evidence → the sensible default + `low-confidence`.

---

## Step 7 — Quota-protection and accuracy rules

Rationale in `reference.md` §10.5. **Auto-added lines:** Rules 1, 9 and 10.

1. **R=3 → human-review note** ("Do not apply without human review."). Model and
   effort unchanged. One shared note, not one per arm.
2. **Escalation is a model change, not an effort change** — Claude: Step 4;
   OpenCode: Rule A1-OC.
3. **`D=3` outside the flagship capability list → Sonnet 5.5 at `xhigh`** on the
   Claude arm.
4. **User knowledge:** low/medium on Opus 5.5 is not "waste" — Anthropic
   recommends them "liberally as your primary control for token cost".
5. **No `ultracode` for work under 30 min.** For one-off depth, write
   `ultrathink` into the prompt instead.
6. **Long-session / MCP warning:** each MCP server injects tool schemas into
   every message (GitHub MCP 27 tools ≈ 18k tokens).
7. **Auto-accept warning:** if R≥2, suggest turning auto-accept off.
8. **Alias safety:** `/model opus` → Opus 5.5 on Claude Code v2.1.280+; `/model sonnet` → Sonnet 5.5 on v2.1.284+.
9. **Data-policy line (auto).** If **Grok 4.7** or **GPT 6 Luna** is on the OpenCode
   line: `Data: <model> keeps prompts for 30 days.` If **Muse Spark 1.3 Contributor**
   is on it (NC1 only): `Data: Muse Spark 1.3 Contributor trains on your prompts.`
   Never name Muse Spark when the work is confidential.
10. **DeepSeek line (auto).** If **DeepSeek V4.1 Flash** is on the OpenCode line:
    `DeepSeek V4.1 Flash: peak hours cost 2× (04–07 and 09–13 TR time, Mon–Fri); zero-retention agreement is renewed monthly (valid through 31 Oct 2026).`

### Speed line

Only when the Claude line is `Opus 5.5` / `Opus 4.8` and **not** `opusplan`:
`⚡ Claude /fast available (2.5x faster, 2× price).` There is no OpenCode speed line
(the Codex speed line was retired with the Codex arm).

---

## Output format

Three lines — or the single `Clarify:` line when Step 0 blocks (Rule S0):

```
Claude: <Model> · effort: <level>
OpenCode: ✅ RECOMMENDED AI · #1 <Model> · effort: <level> · #2 <Model> · effort: <level>
Evidence: <one sentence, ≤ 30 words>
```

- Badge right after the ecosystem label, exactly one. `Evidence:` names ≤ 2 signals;
  if the row is † (or "anything else") it must say `low-confidence`.
- No effort for Haiku 4.5; write `default` where OpenCode offers no variant (MiMo-V2.6).
  OpenCode gated: `OpenCode: use Claude — <reason>` (no `#`).
- Extras, own line each, in order: `opusplan` ⚠️ (directly under the Claude line) ·
  data / DeepSeek lines (Step 7) · speed line · `R=3` → `Do not apply without human
  review.` last.
- "Why?" → expand from `reference.md` / `opencode-benchmarks.md`; never unprompted.

### Examples

*"Label these 200 customer reviews as positive/negative"*
```
Claude: Haiku 4.5
OpenCode: ✅ RECOMMENDED AI · #1 DeepSeek V4.1 Flash · effort: low · #2 MiMo-V2.6-Flash · effort: default
Evidence: Both clear the bar; DeepSeek V4.1 Flash streams 222 tok/s at USD 0.27 per task on a USD 60 cap against Haiku 4.5's USD 1/USD 5.
DeepSeek V4.1 Flash: peak hours cost 2× (04–07 and 09–13 TR time, Mon–Fri); zero-retention agreement is renewed monthly (valid through 31 Oct 2026).
```

*"Fix this code"*
```
Clarify: which file or function is broken, what does it do now, and what should it do instead?
```

*"Refactor the payment module across these 40 files to use the new idempotency-key API, update every caller, and make the test suite pass."*
```
Claude: Sonnet 5.5 · effort: high
OpenCode: ✅ RECOMMENDED AI · #1 MiMo-V2.6-Pro · effort: default · #2 GLM-5.3 · effort: high
Evidence: Terminal-Bench 4.0 (Sonnet 5.5 64, GLM-5.3 42) has no interval, so cap pressure decides — USD 0.13 vs 7.67 per task; low-confidence.
```
> One implementation phase → no `ultracode`; `R=1`, so efficiency decides (at `R=3` Claude, GLM-5.3 first).

*"Find the race condition that flakes in prod sometimes"*
```
Claude: ✅ RECOMMENDED AI · Opus 5.5 · effort: xhigh
OpenCode: #1 MiMo-V2.6-Pro · effort: default · #2 GLM-5.3 · effort: max
Evidence: Reasoning half has two agreeing AA rows (HLE 61 vs 49, CritPt 32 vs 27); the terminal half sets no direction, so the direction decides.
⚡ Claude /fast available (2.5x faster, 2× price).
```
> `D=3` (D3DIAG) but one phase → `xhigh`, not `ultracode`/`max`. `#1` from the badge-deciding tag (deep-reasoning), `#2` from the terminal row.

*"I'm preparing a non-confidential competitor-pricing deck for a conference — research, structure and write the 12 slides"*
```
Claude: ✅ RECOMMENDED AI · Sonnet 5.5 · effort: high
OpenCode: #1 Grok 4.7 · effort: xhigh · #2 MiMo-V2.6-Pro · effort: default
Evidence: Knowledge-work: two agreeing AA rows favour Claude (GDPval-AA 1839 vs 1715, Briefcase 1823 vs 1644); Grok 4.7 is the best open model on both.
Data: Grok 4.7 keeps prompts for 30 days.
```
> NC1 fired; without it `#1` is MiMo-V2.6-Pro and `#2` Qwen3.8 Flash.

*"Bump `MAX_RETRIES` from 3 to 5 in the prod config"*
```
Claude: Sonnet 5.5 · effort: low
OpenCode: ✅ RECOMMENDED AI · #1 GLM-5.3-Flash · effort: low · #2 MiMo-V2.6-Flash · effort: default
Evidence: D=0 — both clear the bar, so price and cap decide: Flash models on USD 60 caps at USD 0.25 and 0.06 per task.
Do not apply without human review.
```
> `R=3` by blast radius, not line length — also why Haiku is out.

*"Write an exploit PoC for this CVE"*
```
Claude: ✅ RECOMMENDED AI · Opus 4.8 · effort: xhigh
OpenCode: use Claude — the only open-model offensive evidence is vendor-reported and no pool model's safeguards are verified.
Evidence: Offensive security is a deciding gate on both arms; only Opus 4.8 carries it, so the other arm declines.
```

---

## If detail is needed

`reference.md` §8 examples · §10 edge cases · §11–§14 evidence maps · §17 Claude 5.5
(§9 and §18 are the retired Codex arm; iteration-20 is git tag `iteration-20-codex`).
`opencode-benchmarks.md` — the 15-model evidence, variants, rung curves, sources.
**Never load them to route a prompt.**
