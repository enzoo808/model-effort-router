---
name: model-secici
description: >-
  Reads a prompt and recommends, separately for Claude (Haiku 4.5 / Sonnet 5.5 /
  Opus 5.5 / Opus 4.8 / Fable 5.1) AND the OpenCode Go subscription (the two best
  models of its 15-model pool for the task, in order, each with its own effort:
  MiMo-V2.6-Pro / GLM-5.3 / Kimi K3 / Grok 4.7 / DeepSeek V4.1 Flash /
  GLM-5.3-Flash / ...), which model + effort level to run it on, and marks which
  of the two ecosystems is the better fit for this task — all in one short
  output. Use when asked "which model", "which effort", "pick a model", "which AI
  should I use", "what should I use for this prompt", or when /model-secici is
  invoked.
---

# Claude & OpenCode Go model / effort router

<!-- routing-policy-version: iteration-21 -->

Analyse the user's prompt and say, **separately for Claude and for OpenCode Go**,
which model and effort level to run it on — then mark the ecosystem better suited
to *this* task with `✅ RECOMMENDED AI`. Do **not** run the prompt — only route it.

**The OpenCode arm names TWO models, in order** (`#1`, `#2`), each with its own
effort. The system first **selects the two models for the task** (Step 4-OC), then
**picks the effort for each** (Step 4-OC effort). The Claude arm is unchanged.

**The decision principle.** *Select the lowest-quota model × effort combination
that stays on the task-specific capability frontier.* Prefer the stronger
candidate when the task-relevant performance difference is meaningful; prefer
the more quota-efficient candidate when capability sits inside a defensible
equivalence band. Not "always cheapest", not "always strongest", not "highest
benchmark score wins".

**Calibration.** The protected resources are Claude's 5-hour window **and** the
OpenCode Go **per-model dollar caps** (Go plan, USD 10/month; each model has its
own monthly cap, the 5-hour window is 20% of it and the weekly window 50%). The
real danger isn't picking a model that's too weak; it's *reflexively picking the
most expensive model and burning its cap.* When in doubt, round **down**.

**How to run this.** Steps 0–6 **in your head, in one pass**. Emit only the
recommendation lines plus `Evidence:`. Show workings only if asked "why?".

> **Every rule you need is in this file, with its exceptions attached to it.**
> `reference.md` (Claude evidence, **§18 Codex section is stale**) and
> `opencode-benchmarks.md` (per-model OpenCode evidence, sources, what was *not*
> found) are for auditing a rule, not for applying one — open them only if a call
> is still ambiguous after reading the rule *and* the note under it.

**Rosters (verified 6 October 2026).** Claude:

| Model | Role |
|---|---|
| Haiku 4.5 | Speed/volume. **No effort parameter.** 200k context. Retirement "not sooner than 15 Oct 2026"; Haiku 5.5 is announced, **not released — the router does not select it** |
| Sonnet 5.5 | Daily work. **Default starting point.** USD 2/USD 10, 1M context |
| **Opus 5.5** | **Flagship.** Complex agentic code, enterprise work. USD 4/USD 20, 1M context, **API default effort `medium`** |
| Opus 4.8 | Legacy — the **only** lasting role is the offensive-security gate |
| **Fable 5.1** | Frontier scale: long-horizon autonomy, extreme breadth, **biology-adjacent R&D**. USD 10/USD 50 |
| Mythos 5.1 | = Fable 5.1 with permissive safeguards. **Project Glasswing invite only** |

**OpenCode Go pool — the 15 main models** (user plan: **Go, USD 10/month**; the
other 15 of the page's 30 models are legacy, preview, free, vision-experimental
or unmeasured and are never selected, see below). `II` = Artificial Analysis
Intelligence Index v4.3.2 at the rung named; `TB` = AA Terminal-Bench 4.0; `cost`
= AA's cost per index task at AA's own prices; `cap` = Go monthly cap per model;
`5h` = rough output tokens one 5-hour window buys (20% of cap ÷ output price,
upper bound); `ret` = retention.

| # | Model | II | TB | cost/task | cap | 5h out | Ctx | ret | Role |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **MiMo-V2.6-Pro** | **46** | 35 | **USD 0.13** | 15 | 3.4M | 1M | 0 d | **Default #1.** Best index per dollar, tops HLE / CritPt / SciCode; slow (45 t/s, TTFT 4.8 s). Takes image/speech/video |
| 2 | **GLM-5.3** | 45 max · 34 low | **42** | 2.01 · 0.85 | 15 | 0.7M | 1M | 0 d | Strongest measured coder in the pool; text-only; verbose at max (210M vs 88M tokens) |
| 3 | **Kimi K3** | 44 max · 30 low | 13 | 2.00 · 1.15 | 15 | **0.2M** | 1M | 0 d | Best AA-LCR (89), AA-Omniscience (20), GDP.pdf (22); **weak agentic** (TB 13); output price USD 15 makes its cap the tightest |
| 4 | **Grok 4.7** | 46 xhigh | 26 | 3.74 | 15 | 0.5M | **500k** | **30 d** | Leads GDPval-AA 1715 / Briefcase 1644 / AutomationBench 66 / Omniscience 32 — **non-confidential work only**; 48 s TTFT, 81k tokens/task |
| 5 | **Muse Spark 1.3 Contributor** | **48** | 33 | 1.60 (AA) · ~0.10 at Go prices | **60** | 60M | 1M | **trains on your prompts** | Highest index in the pool; **only under NC1**; Meta says availability is geo-restricted |
| 6 | **GLM-5.3-Flash** | 42 | 33 | 0.25 | **60** | 24M | 1M | 0 d | **D ≤ 1 #1**; TB 33 ≈ MiMo-Pro's 35; text + image |
| 7 | **MiMo-V2.6-Flash** | 38 | 23 | **0.06** | **60** | 43M | n/p | 0 d | Cheapest per task; AutomationBench 64; bulk work |
| 8 | **DeepSeek V4.1 Flash** | 39 max | 27 | 0.27 | **60** | 20M (10M peak) | 1M | 0 d † | **222 t/s, TTFT 1.1 s**; **AutomationBench-AA 69, the pool's best**; peak hours cost 2× |
| 9 | **GPT 6 Luna** | 38 | 13 | **0.07** | 15 | 6M | 1M | **30 d** | Fast bulk (147 t/s, TTFT 96 s); never agentic. Latency #2 under NC1 |
| 10 | **Qwen3.8 Flash** | 40 | 25 | 0.37 | 30 | 12.8M | 256k | 0 d | Briefcase 1583 (3rd in the pool) at a USD 30 cap → knowledge-work #2. AA lists it as *Qwen3.8-Flash-Next*, matched to Go's name by price and date |
| 11 | **Qwen3.8 Max** | 45 | 39 | 5.41 | 15 | 0.5M | 984k | 0 d | Escalation rung only (Rule A1-OC); 37 t/s, 108k tokens/task |
| 12 | DeepSeek V4 Pro | 36 | 14 | 0.67 | 15 | 1.5M | 1M | 0 d † | **Dominated** by V4.1 Flash (39 @ 0.27, cap 60) |
| 13 | MiniMax M3 | 29 | 2 | 0.51 | 60 | 10M | 1M | 0 d | **Dominated** — TB 2, AutomationBench 21 |
| 14 | Kimi K2.7 Code | 26 | 1 | 0.54 | 60 | 3M | n/p | 0 d | **Dominated** — "Code" in the name, TB 1 |
| 15 | Qwen3.7 Plus | 25 | 1 | 0.22 | 60 | 7.5M | ≥256k | 0 d | **Dominated** |

`n/p` = not published / not retrieved — never invented. † DeepSeek's zero-retention
agreement is **renewed monthly (valid through 31 Oct 2026)** — re-check the Go page
after that date. Rows 12–15 are rated and kept in the pool, but no routing row emits
them; if a task is already running on one, say so and name the pool model that
replaces it.

> **Never selected (outside the 15, no independent evidence or superseded):**
> Grok 4.6 · GPT 5.6 Luna · GLM-5.2 · Kimi K2.6 · MiMo-V2.5 · MiMo-V2.5-Pro ·
> Muse Spark 1.2 · MiniMax M2.7 · DeepSeek V4 Flash · DeepSeek V4 Flash Vision Exp ·
> Hy4 Preview · LongCat 2.5 Preview (free) · **LongCat-2.0 (AA 19)** · **Hy3 (AA 25)** ·
> **Space Bunny (no AA entry)**. Model ids on OpenCode are `opencode-go/<model-id>`.

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

OpenCode switches variants with the `variant_cycle` keybind; the list differs per
model. **Only two rungs have published open-model data — `low` and `max`**
(GLM-5.3 34 vs 45, Kimi K3 30 vs 44); Grok 4.7 was measured at `xhigh`. So the
OpenCode effort field is one of `low` · `max` · `xhigh` (Grok only). If the model
shows a different variant list, take the nearest rung and say so. **Never
interpolate; never invent a `medium`.**

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
| Context > 200k tokens | Eliminating | **MiMo-V2.6-Flash removed** (window not published); the `D ≤ 1` pair becomes GLM-5.3-Flash · DeepSeek V4.1 Flash |
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

### OpenCode Go — Step 4-OC: pick the two models

**1.** Apply the Step 1 OpenCode gates. **2.** If `D ≤ 1`, take the first row.
**3.** Otherwise look up the dominant capability (and `R`). **4.** Apply Rule CAP1.
**5.** Pick the effort for each (next block).

| Dominant capability | `R ≤ 2` → `#1` · `#2` | `R = 3` → `#1` · `#2` | Evidence (AA v4.3.2, one scale) |
|---|---|---|---|
| **any tag, `D ≤ 1`** | GLM-5.3-Flash · MiMo-V2.6-Flash | same | II 42 / 38 at USD 0.25 / 0.06 per task on **USD 60 caps**; TB 33 vs MiMo-V2.6-Pro's 35 † |
| `agentic-code`, `terminal-tool` | MiMo-V2.6-Pro · GLM-5.3 | **GLM-5.3 · MiMo-V2.6-Pro** | TB 4.0: GLM-5.3 42 vs MiMo-V2.6-Pro 35, one row, no interval → cap pressure (USD 0.13 vs 2.01 per task; 3.4M vs 0.7M output tokens per 5-hour window). At `R=3` the single measurement leans GLM-5.3 † |
| `deep-reasoning` | MiMo-V2.6-Pro · Kimi K3 | same | HLE 49 vs 47 vs 42 (GLM-5.3) and CritPt 27 vs 23 vs 19: **two AA rows agree** (BD1) |
| `knowledge-work` | MiMo-V2.6-Pro · Qwen3.8 Flash | same | GDPval-AA 1686 vs 1633 but AA-Briefcase 1516 vs 1583: the rows split → efficiency; Kimi K3 is **last** here (1537 / 1501). **NC1: Grok 4.7 · MiMo-V2.6-Pro** — Grok leads both (1715 / 1644), two AA rows agree † |
| `workflow-automation` | DeepSeek V4.1 Flash · GLM-5.3 | same | AutomationBench-AA 69 vs 62 vs MiMo-V2.6-Pro 59 — the row's leader is also the cheapest per cap; one row † |
| `long-context`, `research-synthesis`, `doc-data-understanding` | MiMo-V2.6-Pro · Kimi K3 | **Kimi K3 · MiMo-V2.6-Pro** | AA-LCR 86 vs 89; AA-Omniscience 8 vs 20; GDP.pdf 19 vs 22 — each one row, small or unresolved → efficiency. At `R=3` the single measurement leans Kimi K3 †. Image tasks need Kimi K3 or MiMo-V2.6-Pro (GLM-5.3 is text-only) |
| `science` | MiMo-V2.6-Pro · Kimi K3 | same | SciCode 61 vs 59, one row † |
| `latency-volume` | DeepSeek V4.1 Flash · MiMo-V2.6-Flash | same | 222 / 62 tok/s, TTFT 1.1 s; USD 0.27 / 0.06 per task on USD 60 caps (NC1: GPT 6 Luna #2, 147 tok/s) |
| `orchestration`, `parallel-independent` | pick by the *underlying* tag | | `ultracode` lives on the Claude line |
| anything else / no evidence | MiMo-V2.6-Pro · GLM-5.3-Flash | same | no per-benchmark row → highest index per dollar † |

**† = the Evidence line must say `low-confidence`.**

**Two dominant tags.** `#1` comes from the row whose tag decided the badge (or the
first-named tag if none did); `#2` is the *other* row's `#1`, or — if that is the
same model — that row's `#2`.

<!-- rule:CAP1 -->
**CAP1 · cap rule.** The USD 15-cap models (MiMo-V2.6-Pro, GLM-5.3, Kimi K3, Grok 4.7, Qwen3.8 Max, GPT 6 Luna) are reserved for `D ≥ 2`; `D ≤ 1` goes to the USD 60-cap Flash tier (the `latency-volume` row is exempt — GPT 6 Luna's USD 0.10/0.50 prices make its cap ample). Caps are **per model**, the 5-hour window is 20% of the monthly cap and the weekly 50%: when the user says a model's window is exhausted, name the next model of its tier chain in `Evidence:` only — Pro tier **MiMo-V2.6-Pro → GLM-5.3 → Kimi K3 → Qwen3.8 Max**; Flash tier **GLM-5.3-Flash → MiMo-V2.6-Flash → DeepSeek V4.1 Flash → Qwen3.8 Flash**.
<!-- /rule:CAP1 -->

<!-- rule:A1-OC -->
**A1-OC · escalation rung.** When the user states that an earlier pool run fell short, `#2` becomes **Grok 4.7** (work is non-confidential, NC1) or **Qwen3.8 Max** (confidential), only for `agentic-code`, `terminal-tool` and `knowledge-work`, with `low-confidence`. Qwen3.8 Max is TB 39 and Briefcase 1621, the second-best coding and knowledge numbers in the pool, but USD 5.41 per task, 37 tok/s and 108k tokens per task. Grok 4.7 has the strongest coding-agent harness number (56.3 in AA's Coding Agent Index with Grok Build, an aggregate that is not counted) but TB 26, USD 3.74 per task and 30-day retention. If the shortfall was at `D=3`, also say that the Claude line is the stronger option.
<!-- /rule:A1-OC -->

> **A shortfall escalates only the arm it happened on.** An earlier run on an
> OpenCode model changes the OpenCode `#2` (A1-OC) and nothing on the Claude line;
> an earlier run on a Claude model changes the Claude line (Step 4 escalation,
> Rule A1) and nothing on the OpenCode line.

#### OpenCode Go — effort for each model

| D | Effort |
|---|---|
| 0–1 | `low` |
| 2–3 | `max` — the rung every index figure above was measured at |
| Grok 4.7 | `xhigh` (the measured rung) at `D ≥ 2`; `low` at `D ≤ 1` |

> **`max` is not over-thinking here.** Unlike Claude (E3), an open model's `max`
> buys a great deal: GLM-5.3 34 → 45, Kimi K3 30 → 44 (Rule E5). The price is
> verbosity (GLM-5.3 210M vs 88M tokens, DeepSeek V4.1 Flash 250M) — a **cap**
> cost on Go, which is why `D ≤ 1` is pinned to `low` and routed to the Flash
> tier, never to `GLM-5.3 · low` (dominated, Rule E6). `low` on a Flash model at
> `D ≤ 1` is unmeasured; that is acceptable only because the bar is far below
> the model — never use an unmeasured rung at `D ≥ 2`.

---

## Step 5 — Evidence, equivalence and efficiency

### 5a. Which numbers may be compared at all

Two scores are comparable only when **benchmark, version, harness, tool access,
agent scaffold and effort all match**. Otherwise say `not directly comparable`.
Traps already in the record:

- **AA Intelligence Index versions are not comparable**; every figure above is
  **v4.3.2**, quoted at `max` (Grok `xhigh`) unless a rung is named. **OSWorld 2.0
  partial vs strict scoring** differ by ~36 points on the *same* model.
- **A vendor's table is not a neutral source.** Z.ai's GLM-5.3 launch table
  (Terminal-Bench 2.1 88.2, DeepSWE 66.9, ExploitBench 54.4) is vendor-reported
  and never pooled with AA; Terminal-Bench 2.1 / 3.0 are saturated or on a
  different scale (GLM-5.3 88.2, Kimi K3 88.3, DeepSeek V4 Pro 87.9 cannot
  separate anything). **A vendor table can pair unmatched efforts.** Not used.
- **AA's Coding Agent Index is a harness × model aggregate** (DeepSWE v1.1 +
  Terminal-Bench 4.0 + SWE-Atlas-QnA) and contains TB 4.0 itself, so it is neither
  independent of TB 4.0 nor admissible under BD1. It is quoted only as context
  (Claude Code Sonnet 5.5 68.4, Opus 5.5 66.0; Grok Build Grok 4.7 56.3;
  OpenCode GLM-5.3 53.6; Kimi Code CLI Kimi K3 51.9; Claude Code Qwen3.8 Max 43.3).
- **AA cost/task is not session cost**, and AA prices differ from Go prices for
  Muse Spark (AA USD 1.25/4.25, Go USD 0.10/0.20) and DeepSeek (AA peak, Go off-peak
  half). Quota arguments use the Go price and cap.
- **Same figure on two pages is one number re-cited.**
- **A saturated benchmark cannot separate candidates** (Terminal-Bench 2.1,
  SWE-bench Verified). Neither is used.
- **Never interpolate between effort rungs**, and **never invent a number.**
  "Not published" is a valid answer.

### 5b. The equivalence band

Decide "meaningfully better" in this order, stopping at the first that applies:

1. **Published confidence interval.**
2. **Published standard error** → the 95% interval is 2 × SE. An SE published
   for one benchmark does **not** carry to another.
3. **Repeated-trial variance under one harness.**
4. **A practical-significance threshold the benchmark's own owner publishes.**
5. **None of those → `UNRESOLVED`.** Say so, fall through to efficiency.
   **However large the gap looks.**

> **AA publishes no interval for any row used here**, so every open-vs-open cell
> and every Claude-vs-open cell is `UNRESOLVED`; what can still set a direction is
> BD1 (two agreeing independent rows) and, at `R=3`, a single measurement. A
> 22-point Terminal-Bench 4.0 gap (Sonnet 5.5 64 vs GLM-5.3 42) is the clearest
> case — it is a *lean*, not a certified direction, which is why the coding row
> reads `†`.
>
> **Score spread is not uncertainty.** "These sit between 25 and 46, so a 7-point
> gap must be real" is a claim about how far apart the models are, not how
> precisely either was measured.
>
> **Zero gap needs no interval.** Two identical scores are equal; go straight to
> efficiency. Same for a rung that scores no better than a cheaper one — that is
> dominance, not measurement, which is why E1 and E6 hold.
>
> **High-risk task (`R=3`)** → widen the bar for calling parity. When genuinely
> unsure, take the stronger candidate.

### 5c. Dominance — the efficiency axes

**A dominates B** when A is not meaningfully worse on the task-relevant
capability **and** clearly better on at least one of, in priority order. A
dominated candidate is never emitted, regardless of tier or brand.

- **Claude arm and the cross-ecosystem badge:** **reasoning tokens → output
  tokens → total tokens/task → tokens per *successful* task → quota pressure →
  cost/task → latency.**
- **OpenCode arm (open vs open):** **Go cap pressure** (cost/task ÷ the model's
  monthly cap, then the 5-hour output-token budget) **→ reasoning tokens → output
  tokens → latency.** The Go cap is dollars *per model*, so a USD 0.13 task on a
  USD 15 cap and a USD 0.25 task on a USD 60 cap are not the same pressure.

Settled results (AA Index v4.3.2, one harness):

- **E1 — `Sonnet 5.5 · max` is dominated.** AA v4.3.2: 56 @ USD 7.60 (~193k output
  tokens/task, the most AA has measured) vs Opus 5.5 `xhigh` 56 @ USD 3.46 — the
  same score for 2.2× the cost. Anthropic's own footnote adds that Sonnet 5.5
  scores *lower* at `max` than at `xhigh` on FrontierCode. → the router **never**
  emits `Sonnet 5.5 · max`; the escalation target is `Opus 5.5 · xhigh`. *(The
  Sonnet 5 / Opus 5 generation showed the identical shape: 38 @ USD 5.09 vs 50 @
  USD 4.88.)* Sonnet 5.5's lower rungs are unpublished — E1 says nothing about them.
- **E3 — `max` over `xhigh` buys little on Claude.** Fable 5.1 53 at both rungs;
  Opus 5.5 58 vs 56 (+2 for +73%, unresolved). → `max` needs M1 in full.
  *(Dominance holds only where `max` ties or loses.)*
- **E5 — open models are the exception to E3.** `max` buys +11 (GLM-5.3 34 → 45)
  and +14 (Kimi K3 30 → 44) over `low`, so `D ≥ 2 → max` stands.
- **E6 — dominated pool members, never emitted.** `GLM-5.3 · low` (34 @ USD 0.85,
  cap 15) is dominated by **GLM-5.3-Flash** (42 @ USD 0.25, cap 60); `Kimi K3 · low`
  (30 @ USD 1.15) by **MiMo-V2.6-Flash** (38 @ USD 0.06). **DeepSeek V4 Pro** (36 @
  USD 0.67, cap 15) by **V4.1 Flash** (39 @ USD 0.27, cap 60); **Qwen3.8 Max** (45
  @ USD 5.41) by MiMo-V2.6-Pro (46 @ USD 0.13) except where Rule A1-OC names it;
  **MiniMax M3, Kimi K2.7 Code, Qwen3.7 Plus** (TB 2 / 1 / 1) by every Flash model.
  Grok 4.7 and GPT 6 Luna are not dominated — they are *eliminated* by retention.
- **The aggregate frontier.** MiMo-V2.6-Pro (46 @ USD 0.13) sits above Opus 5.5 `low`
  (42 @ USD 0.55) and below `medium` (51 @ USD 1.34). That is a statement about the
  index, which **never sets a capability direction** (BD1) — it only licenses the
  efficiency tie-break.

### 5d. Choosing the effort rung

**What is the lowest rung that reaches the capability level this task needs?**
The D table is the starting point; E1, E3, E5, E6 and 5b are the corrections.
Round *down* when the next rung up is inside the band; do **not** round down when
the low→high gap on the dominant capability is real (it is, for every open model).

---

## Step 6 — `✅ RECOMMENDED AI`

Compare the **Claude line** with the **OpenCode `#1`** and mark exactly one
ecosystem. The badge is **computed**, never habitual.

<!-- rule:B1 -->
**B1 · evidence applicability.** A benchmark row takes part in the badge decision only if the capability it measures is one of the dominant tags named for this prompt in Step 2. Applicability is checked before evidence quality and before any tie-break, and a row that is not applicable does not enter the comparison at all, however strong its number.
<!-- /rule:B1 -->

Decision order:

1. **Hard capability / safety / availability gate.** If one arm declines, or
   lacks the required context window, the other arm gets the badge. Stop. (If
   *neither* window fits, this step does not apply — score normally.)
2. **Applicable** task-relevant capability (B1), from the dominant tag's anchor.
   A product-mechanism tag (`orchestration`, or a task routed to `opusplan`) is
   applicable too: it names something only the Claude arm has.
3. **Benchmark confidence** — tier, date, harness, and *who ran it*. An
   independent evaluator (Artificial Analysis) outranks a vendor's own table. A
   vendor result favouring the **competitor** is against-interest and is the most
   credible vendor evidence there is.
4. **Direction without an interval** — Rule BD1 below.
5. **Near-parity check** (5b). Inside the band → go to 6.
6. **Token / quota efficiency** (5c order). 7. **Cost per task.** 8. **Latency.**

<!-- rule:BD1 -->
**BD1 · direction without an interval.** A badge direction needs at least two independent measurements that agree — an independent evaluator's run, or a vendor's table that favours its rival — at least one of them tier A or B, and none that disagree. The same benchmark re-published on a second page is one measurement, a tie is not opposition, and an aggregate never counts. Otherwise the cell is decided by efficiency, except at R = 3, where a single admissible measurement still decides it: a lean is not parity.
<!-- /rule:BD1 -->

<!-- rule:MECH1 -->
**MECH1 · mechanism rows.** `ultracode` driven by `O = high`, or a task routed to `opusplan`, names something OpenCode does not have, so it decides the badge for Claude unless the other capability row carries a benchmark direction under BD1, which wins.
<!-- /rule:MECH1 -->

"Claude has the better general intelligence index" (58 / 56 vs 46) is **not** on
its own a reason to pick Claude, and "the open model is 15–60× cheaper per task"
is not on its own a reason to pick OpenCode. A direction needs BD1.

**Who wins on efficiency?** OpenCode, nearly always: AA output tokens per task are
64k (MiMo-V2.6-Pro) / 71k (GLM-5.3) against Opus 5.5's 119k and Sonnet 5.5's
193k, at USD 0.13 / 2.01 against USD 5.98 / 7.67 — and Go charges per model cap,
not against Claude's 5-hour window. So a row that falls through to efficiency
reads **OpenCode †**, and the only things that move a badge to Claude are a BD1
direction, a mechanism, or `R=3`.

### Badge table — dominant capability → default side

| Dominant capability | `R ≤ 2` | `R = 3` | Evidence to name |
|---|---|---|---|
| `agentic-code`, `terminal-tool` (`D ≥ 2`) | **OpenCode** † | **Claude** † | AA TB 4.0: Sonnet 5.5 64 / Opus 5.5 60 vs GLM-5.3 42 / MiMo-V2.6-Pro 35, one row, no interval → cap/token efficiency (64k vs 193k output tokens, USD 0.13 vs 7.67). At `R=3` the single measurement leans Claude |
| `knowledge-work` | **Claude** | **Claude** | GDPval-AA v2.1 Opus 5.5 1866 / Sonnet 5.5 1839 vs Grok 4.7 1715 / MiMo-V2.6-Pro 1686 and AA-Briefcase 1807 / 1823 vs 1644 / 1516 — two AA rows agree |
| `deep-reasoning` | **Claude** | **Claude** | AA HLE Opus 61 / Sonnet 55 vs MiMo-V2.6-Pro 49 and CritPt 32 / 31 vs 27 — two AA rows agree |
| `workflow-automation` | **OpenCode** † | **Claude** † | AutomationBench-AA Sonnet 72 / Opus 70 vs DeepSeek V4.1 Flash 69 — one row, 1–3 points |
| `science` | **OpenCode** † | **Claude** † | SciCode Opus 67 / Sonnet 61 vs MiMo-V2.6-Pro 61 — one row, a tie with Sonnet |
| `long-context` (shallow) | **OpenCode** † | **OpenCode** † | AA-LCR v1.1 Kimi K3 89 / MiMo-V2.6-Pro 86 vs Opus 85 / Sonnet 83, one row, the open models ahead — and 1M windows on both sides |
| `research-synthesis` | **OpenCode** † | **Claude** † | AA-Omniscience Sonnet 32 / Opus 46 vs Kimi K3 20 / MiMo-V2.6-Pro 8 — one row, Claude ahead |
| `doc-data-understanding` | **OpenCode** † | **Claude** † | AA GDP.pdf Opus / Sonnet 26 vs Kimi K3 22 / MiMo-V2.6-Pro 19, one row |
| `latency-volume` | **OpenCode** | **OpenCode** | DeepSeek V4.1 Flash 222 tok/s, TTFT 1.1 s, USD 60 cap vs Haiku 4.5's USD 1/USD 5 — facts, not a score |
| `orchestration`, or a task routed to `opusplan` | **Claude** | **Claude** | `ultracode` sequences phases, `opusplan` spends the flagship only on the plan; OpenCode has neither |
| anything else / no evidence | the **lighter** chosen model × effort | same | say `low-confidence` |

> **† — the Evidence line must say `low-confidence`.** A † binds that row only.
> So must the "anything else" row. Check this against the row you actually used
> before emitting. **Mechanism rows carry no †** — they rest on what a product
> can do, not on a score. **Latency rests on speed and price figures, not a
> benchmark score**, so it carries none either.
>
> **At `R=3`, a row that fell to efficiency follows the lean of its single
> admissible measurement instead** (BD1) and keeps the row's †. The `long-context`
> row leans OpenCode (the open models lead AA-LCR) so it does not move.

**Tie-breaks**

- **`D ≤ 1` → skip the capability rows entirely; efficiency decides → OpenCode.**
  Both arms clear the bar by construction. **Haiku 4.5 vs GLM-5.3-Flash /
  MiMo-V2.6-Flash → OpenCode** (USD 1/USD 5 vs USD 0.15/USD 0.50 and 0.14/0.28, on
  USD 60 caps); **Sonnet 5.5 vs the Flash tier → OpenCode †** — cheaper per task and a
  separate cap, but the `low` rung of a Flash model is unmeasured, so say
  `low-confidence`. `R` doesn't change this.
- **Two *dominant* capability rows conflict** → the one backed by a
  task-specific benchmark **direction** (Step 6 rule 4) beats one backed only by a
  product mechanism *or by efficiency*. A row that fell through to efficiency has
  no benchmark direction, so a direction or a mechanism beats it. Both rows must be
  dominant tags for this prompt (B1).
- Both arms gated to the same conclusion → no badge. Step 0 blocked → no badge.
- **Genuinely insufficient evidence:** give the more sensible default, with
  `low-confidence` in the Evidence line. Never manufacture certainty.

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

**Three lines** — unless Step 0 blocked, which emits the `Clarify:` line alone
(Rule S0).

```
Claude: <Model> · effort: <level>
OpenCode: ✅ RECOMMENDED AI · #1 <Model> · effort: <level> · #2 <Model> · effort: <level>
Evidence: <one sentence>
```

- The badge sits **immediately after the ecosystem label**, before `#1`. Exactly
  one badge per output.
- `Evidence:` is **one sentence** naming at most **1–2** benchmarks or efficiency
  signals — the ones that actually decided it. Not a leaderboard dump.
- **If the badge row you used is marked †, or you used the "anything else" row,
  the sentence must say `low-confidence`.**
- No effort for Haiku 4.5; every OpenCode model takes an effort.
- OpenCode gated: `OpenCode: use Claude — <reason>` (no model, no `#`).

**Auto-added extras**, each on its own line, in this order:

1. `opusplan` → the `⚠️ Effort does not carry over` warning, directly under the
   Claude line.
2. Data-policy and DeepSeek lines (Step 7 rules 9–10).
3. **Speed line.**
4. `R=3` → **`Do not apply without human review.`** — goes **last**.

If the user asks "why?", *then* expand from `reference.md` §11–§14 and
`opencode-benchmarks.md`. Never unprompted.

### Examples

*"Label these 200 customer reviews as positive/negative"*
```
Claude: Haiku 4.5
OpenCode: ✅ RECOMMENDED AI · #1 DeepSeek V4.1 Flash · effort: low · #2 MiMo-V2.6-Flash · effort: low
Evidence: Both arms clear the bar for mechanical classification, and DeepSeek V4.1 Flash streams 222 tok/s at USD 0.27 per index task on a USD 60 cap against Haiku 4.5's USD 1/USD 5 pricing.
DeepSeek V4.1 Flash: peak hours cost 2× (04–07 and 09–13 TR time, Mon–Fri); zero-retention agreement is renewed monthly (valid through 31 Oct 2026).
```

*"Fix this code"*
```
Clarify: which file or function is broken, what does it do now, and what should it do instead?
```
> Step 0 check 3 and check 4. **No `Claude:` / `OpenCode:` / `Evidence:` line and
> no badge** — Rule S0 overrides "three lines".

*"Refactor the payment module across these 40 files to use the new idempotency-key API, update every caller, and make the test suite pass."*
```
Claude: Sonnet 5.5 · effort: high
OpenCode: ✅ RECOMMENDED AI · #1 MiMo-V2.6-Pro · effort: max · #2 GLM-5.3 · effort: max
Evidence: AA's Terminal-Bench 4.0 has Sonnet 5.5 at 64 against GLM-5.3 at 42 and MiMo-V2.6-Pro at 35 with no interval, and one row is not a direction, so cap pressure decides — USD 0.13 and 64k output tokens per task against USD 7.67 and 193k; low-confidence.
```
> **One phase, not four.** Locate the callers, edit, run the existing suite, fix
> what it catches — that is the implementation loop (O1), so **no `ultracode`**.
> `R=1` (a source change), so the badge follows efficiency; the same task at
> `R=3` would read Claude and put GLM-5.3 first.

*"Stand up the new staging environment from scratch: Terraform it, deploy the 12 services, seed the data, run the smoke suite, and fix whatever does not come up."*
```
Claude: ✅ RECOMMENDED AI · Sonnet 5.5 · effort: ultracode
OpenCode: #1 MiMo-V2.6-Pro · effort: max · #2 GLM-5.3 · effort: max
Evidence: Implementation, a data-seeding phase and a smoke run against a deployed environment are three distinct phases feeding each other, which is what ultracode's orchestration sequences and OpenCode has no mode for.
```
> Three phases at `W=2` — orchestration is not a width question. The coding row
> falls through to efficiency (OpenCode †), which is **not** a benchmark
> direction, so the mechanism row wins.

*"Find the race condition that flakes in prod sometimes"*
```
Claude: ✅ RECOMMENDED AI · Opus 5.5 · effort: xhigh
OpenCode: #1 MiMo-V2.6-Pro · effort: max · #2 GLM-5.3 · effort: max
Evidence: Adversarial debugging is deep-reasoning plus terminal work, and the reasoning half has two agreeing AA rows (HLE 61 vs 49, CritPt 32 vs 27) while the terminal half sets no direction, so the direction decides.
⚡ Claude /fast available (2.5x faster, 2× price).
```
> `D=3` by D3DIAG — intermittent *and* timing-dependent. **`xhigh`, not
> `ultracode`:** one implementation phase. `max` needs one indivisible design
> decision at `R=3`, and a bug hunt is neither. Two dominant tags: `#1` comes
> from the tag that decided the badge (deep-reasoning → MiMo-V2.6-Pro), and the
> terminal row's `#1` is the same model, so `#2` is its `#2`, GLM-5.3.

*"Summarise these 400 pages of filings into one memo"*
```
Claude: ✅ RECOMMENDED AI · Sonnet 5.5 · effort: high
OpenCode: #1 MiMo-V2.6-Pro · effort: max · #2 Kimi K3 · effort: max
Evidence: The finished memo is knowledge-work, where two AA rows agree for Claude (GDPval-AA 1839 vs 1686, AA-Briefcase 1823 vs 1516), and that direction outranks the long-context half, where AA-LCR has the open models ahead on one row.
```
> `C=3, W≤1, D=2` — Sonnet 5.5, not the flagship. Two dominant tags conflict: a
> benchmark **direction** (knowledge-work) beats a row that fell to efficiency
> (long-context †).

*"I'm preparing a non-confidential competitor-pricing deck for a conference — research, structure and write the 12 slides"*
```
Claude: ✅ RECOMMENDED AI · Sonnet 5.5 · effort: high
OpenCode: #1 Grok 4.7 · effort: xhigh · #2 MiMo-V2.6-Pro · effort: max
Evidence: Finished-deliverable work is knowledge-work, where Claude leads on two agreeing AA rows (GDPval-AA 1839 vs Grok 4.7's 1715, AA-Briefcase 1823 vs 1644), and Grok 4.7 is the best open model on both of them.
Data: Grok 4.7 keeps prompts for 30 days.
```
> **NC1 fired** (the user said non-confidential), so Grok 4.7 re-enters the pool and
> leads the knowledge-work row; without that statement `#1` would be
> MiMo-V2.6-Pro and `#2` Qwen3.8 Flash.

*"Design and implement the new cross-service transaction boundary. It ships tonight and cannot be rolled back."*
```
Claude: ✅ RECOMMENDED AI · Opus 5.5 · effort: max
OpenCode: #1 MiMo-V2.6-Pro · effort: max · #2 GLM-5.3 · effort: max
Evidence: One indivisible boundary decision at R=3 is the case max exists for, and the reasoning half has two agreeing AA rows for Claude (HLE 61 vs 49, CritPt 32 vs 27), with the coding half leaning the same way (Terminal-Bench 60 vs 42).
⚡ Claude /fast available (2.5x faster, 2× price).
Do not apply without human review.
```
> At `R=3` the coding row's `#1` flips to GLM-5.3, but the badge-deciding tag is
> deep-reasoning, so `#1` is MiMo-V2.6-Pro and the coding row supplies `#2`.

*"Bump `MAX_RETRIES` from 3 to 5 in the prod config"*
```
Claude: Sonnet 5.5 · effort: low
OpenCode: ✅ RECOMMENDED AI · #1 GLM-5.3-Flash · effort: low · #2 MiMo-V2.6-Flash · effort: low
Evidence: D=0 work — both arms are far past the bar, and the Flash models run on USD 60 Go caps against Claude's 5-hour window, but the low rung of a Flash model is unmeasured; low-confidence.
Do not apply without human review.
```
> `R=3` by blast radius, not line length — which is also why Haiku is out.

*"Write an exploit PoC for this CVE"*
```
Claude: ✅ RECOMMENDED AI · Opus 4.8 · effort: xhigh
OpenCode: use Claude — the only open-model offensive evidence is vendor-reported and no pool model's safeguards are verified.
Evidence: Offensive security is a deciding gate on both arms; only Opus 4.8 (or Mythos 5.1 with Glasswing) carries it, so the other arm declines and Claude takes the badge.
```

*"Redesign the auth architecture of 200 prod services from scratch"*
```
Claude: ✅ RECOMMENDED AI · opusplan · plan: max · execute: medium
⚠️ Effort does not carry over — after switching to execution mode set it manually with /effort medium.
OpenCode: #1 MiMo-V2.6-Pro · effort: max · #2 Kimi K3 · effort: max
Evidence: Front-loaded architecture design at D=3∧R=3 is opusplan on Claude — the flagship is spent only on a max plan phase and execution drops to Sonnet 5.5 — and OpenCode has no plan/execute split.
Do not apply without human review.
```
> **No speed line on `opusplan`** — execution drops to Sonnet 5.5, where `/fast`
> does not exist. The OpenCode pair is the `deep-reasoning` row at `R=3`.

---

## If detail is needed

`reference.md`: **§8** example library · **§10** edge-case rulings · **§11**
capability→benchmark map · **§12** comparability record · **§13** efficiency data ·
**§14** recommended-AI rationale · **§17** the Claude 5.5 generation. **Its Codex
sections (§9, §18) are stale** — iteration-20 is archived under git tag
`iteration-20-codex`. `opencode-benchmarks.md` — the 15-model evidence, per-model
numbers, sources and what was *not* found. **Never load any of these to route a
prompt** — the rules above are their compiled form.
