---
name: model-secici
description: >-
  Reads a prompt and recommends, separately for Claude (Haiku 4.5 / Sonnet 5 /
  Opus 5 / Opus 4.8 / Fable 5.1) AND Codex/ChatGPT (Luna / Terra / Sol / Sol
  Ultra / GPT-6 Astra), which model + effort level to run it on, and marks which
  of the two is the better fit for this task — all in one short output. Use when
  asked "which model", "which effort", "pick a model", "which AI should I use",
  "what should I use for this prompt", or when /model-secici is invoked.
---

# Claude & Codex model / effort router

<!-- routing-policy-version: iteration-18 -->

Analyse the user's prompt and say, **separately for Claude and for
Codex/ChatGPT**, which model and effort level to run it on — then mark the one
better suited to *this* task with `✅ RECOMMENDED AI`. Do **not** run the prompt
— only route it. The user decides which recommendation to use; this router
starts nothing automatically.

**The decision principle.** *Select the lowest-quota model × effort combination
that stays on the task-specific capability frontier.* Prefer the stronger
candidate when the task-relevant performance difference is meaningful; prefer
the more token-efficient candidate when capability sits inside a defensible
equivalence band. This is **not** "always cheapest", **not** "always strongest",
and **not** "highest benchmark score wins".

**Calibration: two separate subscription quotas.** The protected resource is
Claude's 5-hour window **and** ChatGPT Plus's 3-hour + weekly windows — not
dollars. The real danger isn't picking a model that's too weak; it's
*reflexively picking the most expensive model and burning the quota.* When in
doubt, round **down**.

**How to run this — keep it cheap.** Do Steps 0–6 **in your head, in one pass**;
don't write them out. Produce only the final two lines plus the `Evidence:`
line. Show workings only if the user asks "why?".

> **Fast path.** If Step 0 raises nothing **and** no Step 1 gate fires, read the
> capability profile and the four axes in a single pass, apply the two mapping
> tables, then the badge table — and emit. Most prompts are this case. Open
> `reference.md` only when a specific call is genuinely ambiguous after one read
> (§10 edge-case rulings · §8 example library · §11 capability→benchmark map ·
> §12 the evidence record itself).

**Claude model roster (verified 10 September 2026):**

| Model | Role |
|---|---|
| Haiku 4.5 | Speed/volume specialist. No effort parameter. 200k context |
| Sonnet 5 | Daily work — speed+intelligence balance. **Default starting point.** $2/$10 (the rise to $3/$15 was cancelled; $2/$10 is now the standard price) |
| **Opus 5** | **Flagship.** Complex agentic code and enterprise work. $5/$25 |
| Opus 4.8 | Legacy — the **only** lasting role is the offensive-security gate |
| **Fable 5.1** | Frontier scale: long-horizon autonomy, extreme breadth, **biology-adjacent R&D**. $10/$50, cache reads ¼ ($0.25/MTok); cutoff Jun 2026 |
| Mythos 5.1 | **Same model** as Fable 5.1 with permissive safeguards — **Project Glasswing invite only**. Recommend only if the user states they have this access |

> **Anthropic's own framing (re-verified 10 Sep 2026):** "Most workloads start
> with Claude Opus 5… if your evals at `xhigh` or `max` effort still fall short
> on demanding reasoning or long-horizon agentic work, move to Claude Fable
> 5.1." That is the **third escalation rung** — see Step 4's escalation note. It
> is a *stated shortfall*, not difficulty: a long session on its own does not
> earn it.

**Codex/ChatGPT roster (GPT-5.6 family + GPT-6 Astra, verified 10 Sep 2026):**

| Model | Role | Claude analogue (rough) |
|---|---|---|
| Luna | Speed/volume specialist, cheapest tier. Codex CLI default | Haiku 4.5 |
| Terra | Daily work, balanced — **default starting point** | Sonnet 5 |
| **Sol** | **GPT-5.6 flagship** — code/science/security; the **D=3** pick | Opus 5 |
| **Sol Ultra** | A Codex *mode* toggled on Sol (Plus+): ~4 collaborating agents in parallel. Not a separate model; `effort:"ultra"` → HTTP 400. **Also available on Astra** (confirmed 10 Sep) | stronger parallelism primitive than `ultracode` |
| **Astra** | **GPT-6 flagship** (`gpt-6-astra`). 1.05M context. **Gated pick only** — the five Codex gates below. ~2.5× Sol's headline price but materially fewer output tokens | Opus 5 / Fable 5.1 (frontier) |
| *Codex Spark 5.3* | Text-only research preview for near-instant coding iteration. **The router does not select it** — research preview, text-only, no benchmark record | — |

> **`max` on Codex is Astra/Sol only** (`learn.chatgpt.com/docs/models`, 10 Sep
> 2026: "Astra and Sol additionally offer Max and Ultra modes"). On Terra and
> Luna it is a **capability limit**, not a preference — the router cannot emit
> `Terra · max` even if a rule asked for it. One conflicting source lists a
> Terra `max` row; see `reference.md` §12.3.

---

## Effort levels

Claude Code `/effort` menu — and, rung for rung, the Codex ladder:

| Level | What it does |
|---|---|
| `low` | Short, well-scoped work that needs no intelligence |
| `medium` | Cost-sensitive work; gives up some intelligence. **Codex API default** |
| `high` | **Claude default** (every model that supports effort) |
| `xhigh` | Deeper reasoning. 30 min+ agentic/coding work |
| `max` | Deepest reasoning. Over-thinking risk. Claude: all tiers. **Codex: Astra/Sol only** |
| `ultracode` | `xhigh` + **dynamic workflow orchestration**. Claude Code setting |

1. **`ultracode` is a Claude Code setting, not a model effort level.** It sends
   `xhigh` and adds workflow orchestration. Works on every model that supports
   `xhigh`. Not Haiku.
2. **Haiku 4.5 does not support the effort parameter.** Recommend Haiku → write
   no effort.
3. Effort is a behavioural signal, not a token budget. "low = 1,024 tokens"
   figures are made up.
4. **Effort is not the primary quality dial.** OpenAI states it outright: "Treat
   `reasoning.effort` as a tuning knob, not the primary way to recover quality."
   Step 5's dominance rules act on exactly this — a *stronger model at a lower
   rung* often beats a *weaker model at a higher rung* on both quality and
   quota.

---

## Step 0 — Prompt quality gate

**Do not skip.** Before anything else, run these four checks. "Is there a
success criterion / scope?" as a single question is not enough — most real
prompts contain scope but carry an unnoticed ambiguity. If any check is "yes",
**recommend no model, no badge** — clarify first, concretely (name what's
missing, don't just say "it's unclear").

1. **A rule stated by example but not generalised?** "For instance if X then Y"
   with no general formula/threshold. *("500 of 1000 units land the same day" —
   50%, a fixed 500, or an hour cutoff?)*
2. **Would a wrong assumption silently produce a wrong result?** Code runs
   without error but systematically miscalculates on real data.
3. **Is the target concrete?** "We'll do it like this in the system" doesn't say
   which query/service/table/file.
4. **Do two plausible but different implementations come out of the same
   prompt?** *("delete inactive users" — `is_active` flag, or no login for N
   days? Different delete sets.)*

Sending an unclear prompt to the most expensive model is pure quota waste — it
guesses the context, guesses wrong, the work is redone. Counter-example (do
**not** block): "Add a `deleted_at` column and implement soft-delete instead of
`DELETE`" — rule complete, one interpretation, concrete scope → go to Step 1.

---

## Step 1 — Hard gates

**Hard constraints, never weighted scores.** Capability limits, safety
behaviour and availability are not preferences and do not trade against
efficiency. Every gate below was re-verified on 10 Sep 2026 and survived.

- **Deciding gate:** fixes **which model**, bypasses Step 4 model selection.
  Does not bypass the effort/`ultracode` check, and does not bypass Step 6.
- **Eliminating gate:** removes one candidate; scoring runs among the rest.

### Claude arm

| Condition | Kind | Result |
|---|---|---|
| Sub-second latency **or** high-volume classification/parsing | Deciding | **Haiku 4.5.** No effort. Stop |
| **Offensive security:** exploit generation, penetration testing, binary-based vulnerability scanning | Deciding | **Opus 4.8**, effort floor `xhigh` (W/duration can still raise it to `ultracode`) — with Glasswing access, **Mythos 5.1** |
| **Biology-adjacent R&D:** genomics, protein/chemistry-heavy pipeline, bio-CTF | Deciding | **Fable 5.1** (default effort `high`, no floor) |
| Context exceeds 200k tokens | **Eliminating** | **Haiku 4.5 removed**, scoring runs with the rest |
| **1000+ files / whole-codebase scale** | Deciding | **Fable 5.1** |

### Codex arm

| Condition | Kind | Result |
|---|---|---|
| Sub-second latency / high-volume classification | Deciding | **Luna**, effort `low` |
| **Offensive security** (same definitions) | Deciding | **"use Claude"** — standard Codex/ChatGPT access **hard-stops** these tasks (Astra sits at OpenAI's **Critical** cyber level; a cyber safety check ends the run rather than pausing for approval). **Exception:** if the user states **Daybreak Blue** access → **Astra · `xhigh`** floor |
| **Biology-adjacent R&D** (same definitions) | Deciding | **"unverified — use Claude"**, no model. Astra's system card is cyber-focused; no Astra biology threshold is published (re-checked 10 Sep 2026) |
| **1000+ files / whole-codebase scale** | Deciding | **Astra** — only Codex model with a verified ≥1M window (1.05M). Wins over the D=3 mapping, path (a) included |
| **≥ ~1M-token corpus / "load the whole repo at once"** | Deciding | **Astra**. Mind the **2× price** above 272k input tokens |
| **Computer use / GUI is the task itself** (drive a browser or desktop app end-to-end) | Deciding | **Astra** — its one clear published lead over Sol. Not for "code that happens to touch a browser" |

> **Defensive security work does not trigger the offensive gate — on either arm,
> at any scale.** "Audit this code/infra for vulnerabilities", "find open
> ports", "audit 180 services for auth-bypass bugs (no exploits)" → normal
> scoring. Fable 5.1 and Astra both do defensive vulnerability *discovery* by
> default; only exploit / PoC *generation* is gated.
>
> **Frontier-scale gate — one signal is enough:** the file/scope count (1000+).
> 100–999 files does **not** gate — normal scoring (`W=3`).
>
> Rationale and worked pairs: `reference.md` §10.1.

---

## Step 2 — Task capability profile

**Before scoring scope, name the capabilities the task actually needs.** This is
what makes benchmark evidence usable: a benchmark only counts for a task whose
capability it measures. A pure maths problem gives SWE-bench, Terminal-Bench and
CursorBench a weight of **zero**.

Pick the **one or two dominant** capabilities — not the full list. The dominant
one drives the evidence lookup in Step 5 and the badge in Step 6.

| Capability tag | Prompt signals | Evidence anchor (Step 5) |
|---|---|---|
| **agentic-code** | multi-file implementation, refactor, migration, feature build, debug-and-fix across files, repository navigation | Terminal-Bench 4.0 · CursorBench 3.2.0 |
| **terminal-tool** | terminal/CLI work, build & test loops, tool orchestration, long-horizon execution | Terminal-Bench 4.0 |
| **deep-reasoning** | architecture from scratch, algorithm design, mathematics/formal proof, tool-less analysis, adversarial correctness hunting | HLE (tool-less vs tooled) |
| **knowledge-work** | produce a finished document / spreadsheet / deck / memo / filing; professional deliverable | GDPval-AA v2 |
| **research-synthesis** | multi-source research, web search, reconciling conflicting sources | AA-Omniscience, AA-Briefcase (via AA Index) |
| **long-context** | read a large corpus, map/summarise across hundreds of pages or a whole repo | AA-LCR v1.1 (via AA Index) + the hard context-window spec |
| **computer-use** | drive a browser or desktop GUI, click through an app, screenshots | OSWorld (⚠️ version + scoring mode) |
| **science** | genomics, chemistry, physics, research engineering, lab pipelines | Terminal-Bench-Science 0.1 |
| **workflow-automation** | wire up business workflows, integrations, multi-tool orchestration | AutomationBench |
| **doc-data-understanding** | scanned documents, PDFs, charts, tables, multimodal extraction | *no verified cross-ecosystem row — evidence-poor* |
| **parallel-independent** | 3+ targets that are genuinely unaware of each other and merge at the end | *product mechanism, not a benchmark:* `ultracode` vs Ultra mode |
| **latency-volume** | sub-second, high-throughput, bulk classification/parsing | output speed + cost/task (AA Index table) |
| **instruction-following** | rigid format/schema compliance | folded into the dominant tag; never dominant on its own |

> Cybersecurity splits: **offensive** is a Step 1 gate; **defensive** hunting is
> `deep-reasoning` (adversarial correctness) plus whichever of `agentic-code` /
> `terminal-tool` the scale demands.
>
> Full capability→benchmark map, including which benchmarks are *excluded* for
> each tag: `reference.md` §11.

---

## Step 3 — Score scope and stakes on four axes, 0–3

The capability profile says *what kind of work*; R/D/W/C says *how much of it
and at what risk*. Both feed the mapping. For each axis **ask the diagnostic
first**, then place the level. **When in doubt, round down.**

### R — Risk / irreversibility

*Diagnostic: if the output is wrong, minutes or days to fix? Automatic rollback
(git revert, feature flag)? How many users/systems affected? Money/health/legal?*

`0` Throwaway draft — no loss even if unused
`1` Used but a human reviews and approves (PR, draft email)
`2` Goes to a real system but reversible (feature-flagged deploy, reversible migration, isolated operational value)
`3` No way back / disproportionately costly — data-loss risk, irreversible migration, outbound message/payment, central shared-core architectural decision, medical/legal/financial advice, live user data

> **First separate: a codebase change, or a live/operational value?** A normal
> source-code change is **R=1 by default** — the normal flow is PR review +
> deploy. R=2/R=3 only kick in if the prompt explicitly points at a value that
> goes live **without** code review — prod config file, live admin panel,
> feature-flag toggle, DB setting.
> - **"Architectural decision" alone ≠ R=3.** Rollable out service-by-service
>   and rewindable → **R=2**. R=3 only when (a) no real rollback, or (b) a
>   **central/shared** core the whole system depends on.
> - **Decompose → module or service?** "modules" = internal refactor → **R=2**.
>   "separate **services/processes**" → **R=3**.
> - **"One-line config" alone ≠ R=2.** Blast radius, not line length. A line
>   governing **system-wide** behaviour (retry count, timeout, pool size) → R=3.
> - **A schema / DB migration is R=2 even when it is trivially specified.** It
>   lands in a live database, so it is not a plain source change. "Add a
>   `last_login_at` column and make it nullable" is `D=0` **and** `R=2` — the
>   depth sets the effort (`low`), the risk keeps it off Haiku/Luna.
>
> Worked ✅/❌ pairs: `reference.md` §10.2.

### D — Depth

*Diagnostic: known/standard pattern, or thought out from scratch? How many
approaches is a choice being made between?*

| Level | Coding | Writing/analysis | Research | Data |
|---|---|---|---|---|
| `0` | Pattern match, known constant; **fully-specified additive schema change** | One-sentence answer **or** pure form/tone change (length irrelevant) | Single-source lookup | Reading a single number |
| `1` | Standard pattern (CRUD, known bug shape); schema change with a choice | Simple summary/draft | Single-source summary | Simple filter/aggregation |
| `2` | Multi-step but well-documented feature | Multi-source synthesis report | Multi-source synthesis | Statistical inference |
| `3` | Design from scratch, concurrency, algorithmic complexity, conflicting constraints; **adversarial security-vulnerability hunting** | Original argument, reconciling conflicting sources | New hypothesis/framework | Modelling, causal inference |

> - **"Well-documented" alone ≠ D=2.** How many **independent design decisions**
>   are left to the implementer? One reasonable approach → **D=1**.
> - **Mechanical enumeration = D=1**, not D=3. Open-ended "review this for
>   security holes" is the D=3 adversarial case.
> - **"Adversarial" is narrow.** It means hunting *security* vulnerabilities, or
>   subtle logic errors in a coupled system where the failure is silent (a race
>   condition, silent data corruption, conflicting contract clauses). A careful
>   **domain-correctness audit** of well-specified scientific or business logic
>   is **D=2** — "audit this pipeline's variant-calling logic" is D=2, not D=3.
>
> Worked pairs: `reference.md` §10.3.

### W — Width

*Diagnostic: how many files/documents read or changed? Independent
(parallelisable) or sequential?*

`0` Single file/document · `1` 2–5 files, one module · `2` **6–99 files/units**
or 2–3 verification angles · `3` **100+ files** / whole codebase or 3+
independent, parallelisable verification angles

> **The W=2 / W=3 threshold is numeric — 100.** "60 microservices" → W=2.
> "Unaware of each other" phrasing doesn't change the count.

### C — Context synthesis

`0` Self-sufficient · `1` A few small files · `2` A medium codebase/docs ·
`3` A large corpus (hundreds of pages, a huge codebase, a long chat history)

---

## Step 4 — Candidate model × effort, per arm

Model selection is by **intelligence need** (D, C) and the capability profile —
risk (R) does not raise the model, it raises human oversight.

**Model** ← `max(D, C)`. **The flagship is a candidate only when `D=3`** —
`C=3` alone (large but shallow synthesis) stays mid-tier; a 1M window handles it
at a fraction of the quota.

### Claude

| Condition | Model |
|---|---|
| `D = 0` ∧ `W=0` ∧ `C≤1` ∧ `R≤1` | **Haiku 4.5** |
| Above not met, `max(D,C) ≤ 2` | Sonnet 5 |
| `max(D,C) = 3`, `D<3` (C triggered it) | **Sonnet 5** — large context, shallow reasoning |
| `max(D,C) = 3`, `D=3` | **Opus 5** if the dominant capability is on the **flagship list** below. **Otherwise Sonnet 5** (quota-aware default) |

> **The flagship list** (`D=3` only): `agentic-code` · `terminal-tool` ·
> `deep-reasoning` (maths / formal proof / tool-less) · `science` ·
> `computer-use` · `workflow-automation` — **and only where the task builds,
> changes or drives the artefact.**
>
> **Reading, reviewing, auditing or answering-from-code is analysis and stays
> mid-tier, at any scale.** A 180-service defensive audit and a single-file JWT
> review get the *same Claude tier* (Sonnet 5) — scale changes `W`, and therefore
> `ultracode`, not the tier. Analytical, research and legal `D=3` work is not on
> the list at all. This is the same carve-out the Codex +1 notch uses.
>
> On the **Codex** arm this carve-out governs paths (b) and (c) only. Path (a)
> is a *parallelism* mechanism, not a depth judgement, and is still checked
> first — 180 independently auditable services reach `Sol Ultra` even though the
> work is analysis.

### Codex

| Condition | Model |
|---|---|
| `D=0 ∧ W=0 ∧ C≤1 ∧ R≤1` | **Luna** |
| Otherwise `max(D,C) ≤ 2` | Terra |
| `max(D,C)=3`, `D<3` (C triggered it) | Terra |
| `max(D,C)=3`, `D=3` | In order: **(a)** **3+ genuinely parallel strands** → **Sol Ultra** — *this is about parallelism, so it fires for analysis work too, before (b)/(c) are considered*. **(b)** same flagship capability list as Claude → **Sol**. **(c)** otherwise (D=3 analytical / research / single-artefact review) → **Terra** |

> **What counts as a strand.** Anything that proceeds without waiting on the
> others and merges at the end: already-independent **targets** (services, repos,
> vendors) **or** independent **work-kinds** — three candidate designs
> investigated or prototyped side by side, two separate hypotheses plus a
> reproduction. **Two** strands is not enough; Ultra runs ~4 agents and costs
> roughly 4×, so the bar is three.
>
> **(a) vs "split one codebase into modules/services".** Splitting a monolith is
> plain **Sol** (path b) — one coherent boundary decision; the pieces are
> interdependent *during the work* even if the end state is "independent". One
> decision sliced up after the fact is never strands.
>
> Strands and `max` are **mutually exclusive**: `max` needs one indivisible
> chain, so `Sol Ultra · max` is not a combination the rules can produce.

**Effort ← D**, one shared table for both arms:

| D | Effort |
|---|---|
| 0 | `low` |
| 1 | `medium` |
| 2 | `high` |
| 3 | `xhigh` |
| 3 ∧ R=3 | `max` — **only** on a flagship (Opus 5 / Opus 4.8 / Fable 5.1 / Sol / Astra) **and** only where Step 5 Rule E3 allows it. Otherwise `xhigh` |

Haiku 4.5 selected → leave the effort field blank.

**Escalation request — a model change, never an effort change.** If the user
explicitly says the work is critical, must not be under-resourced, or that an
earlier run fell short, move **one model tier up** — Sonnet 5 → **Opus 5**,
Terra → **Sol** — and keep the effort rung the `D` table already gave.

> **Third rung — frontier.** Opus 5 → **Fable 5.1**, Sol → **Astra**. Narrower
> than rung two, and it needs *all* of: the user states a **flagship-tier run at
> `xhigh` or `max` already fell short** (or the session is an hours-long
> unattended agentic run), the dominant capability is on the flagship list, and
> the work is long-horizon. Difficulty alone never reaches it — on the aggregate
> index Fable 5.1 sits inside the equivalence band against Opus 5 at roughly
> 1.5× the cost per task, so an unprompted jump is quota burned for nothing.

Do *not* raise the effort on the mid tier instead: Step 5 Rules E1/E2 show the
mid tier's top rung is dominated by the next tier's ordinary rung on **both** quality and
quota (`Opus 5 · xhigh` 50 @ $4.88 beats `Sonnet 5 · max` 38 @ $5.09;
`Sol · high` 42 @ $0.81 matches `Terra · max` 42 @ $1.40). This is the only thing
that overrides the mid-tier `D=3` default.

**Arm modifiers**

- **Claude — `ultracode`.** It buys **workflow orchestration**, so it keys on how
  many *kinds* of step the session must sequence, not on how many files it
  touches. Write `ultracode` in the effort field; no model restriction except
  Haiku. Fires when **all three** hold:
  1. estimated duration > 30 min, **and**
  2. **three or more different kinds of step feed each other** in one session —
     discover · implement · author tests · run tests/build/lint · repair what
     they caught · sync docs or package — **or** `W = 3` ∧ `D ≥ 2` (100+ units
     that each need judgement), **and**
  3. the difficulty is **not one indivisible chain** — the same test Rule E3
     uses for `max`, so the two rules can never refuse a task for opposite
     reasons.
  > **Count the session's steps, not the deliverable's stages.** A four-stage
  > pipeline written in one go is implement ×4 plus verify — two kinds, not four.
  >
  > **One kind repeated across many units is `W`, not orchestration.** 150 files
  > of one rename is `D=1`; it gets `medium`, not an orchestration mode.
  >
  > **An investigation loop is one kind too.** Measure → hypothesise → re-measure
  > is depth, so a root-cause hunt gets `xhigh` and never `ultracode`.
- **Codex — +1 effort notch for agentic multi-step coding.** Only when the task
  is *writing or restructuring* code across **multiple dependent steps**: a
  multi-file feature, a refactor, a migration, implementing an architecture, or a
  debug-and-fix that spans the codebase. Then bump the Codex effort one rung
  (`low→medium · medium→high · high→xhigh`). It **caps at `xhigh` on both**
  models: the notch compensates for a *model-tier* gap, and Step 7 Rule 2 says
  the top rung is not where you buy that. It also **never lowers a rung** — if
  the `max` row already fired, the notch leaves it alone. **Terra/Sol only,
  never on Astra.** Claude is untouched. Basis: Terminal-Bench 4.0 (Sol 37.3 vs
  Opus 5 52.3 / Fable 5.1 55.8) — the largest published Claude-vs-Codex gap in
  the evidence set.
  - **Does NOT apply to:** a **single local addition** — one endpoint, one flag,
    one column, one pattern applied in one place ("add cursor-based pagination to
    this API", "add a `--dry-run` flag") — that is D=1 work, not multi-step
    restructuring; code *review* / vulnerability *analysis* / reading code to
    answer; non-code design; mechanical repetition of the same edit across files
    (that is width, not depth).
  - **The notch keys on the *fix*, not the diagnosis.** If the hard part is
    working out what is wrong and the resulting change is local (one or two
    files, a config, a flag), there is no notch — that is `terminal-tool` /
    `deep-reasoning` work. The notch is for the case where the *writing* itself
    spans dependent steps.
  - `Sol Ultra` rides on top of the bumped level.

### `opusplan` — plan/execute model split

**Claude Code only.** Overrides the Opus 5 branch when all three hold:
1. `max(D,C)=3 ∧ D=3` ∧ the dominant capability is structured design/architecture.
2. **Difficulty front-loaded into the plan** — once the plan is done, execution
   repeats a pattern. Opposite (do **not** use): debugging, formal proof,
   new-algorithm design.
   > A concrete target-scope number ("design the auth architecture for 200
   > services") implies the execution phase exists.
3. `W ≥ 2`.

```
Claude: opusplan · plan: <effort> · execute: <effort>
⚠️ Effort does not carry over — after switching to execution mode set it manually with /effort <execute effort>.
```
Plan effort = the flagship result (`xhigh`, or `max` if `R=3` — the plan phase
is novel design, so Rule E3 allows it). Execute effort = the post-plan estimated
D (usually `medium`). **The ⚠️ warning is mandatory on every `opusplan` output.**

---

## Step 5 — Evidence, equivalence and efficiency

This is the step that makes the router benchmark-*aware* rather than
benchmark-*driven*. Apply it to the Step 4 candidates.

### 5a. Which numbers may be compared at all

Two scores are comparable only when **benchmark, version, harness, tool access,
agent scaffold and effort all match**. Otherwise say `not directly comparable`
and fall back to the next-best evidence. Concrete traps already in the record:

- **OSWorld 2.0 partial vs strict scoring** differ by ~36 points on the *same*
  model. Any OSWorld comparison without a stated scoring mode is unusable.
- **AA Intelligence Index versions are not comparable.** v4.3's 53/51/48 and the
  older 66/63/60 figures are different scales.
- **"Agentic coding" is not one number.** Terminal-Bench 4.0 puts Sol ~15 points
  behind Opus 5; CursorBench 3.2.0 puts it 2.8 behind; DeepSWE puts it 1 behind.
  Different scaffolds. Name the benchmark, never the label.
- **A vendor's table is not a roster.** Anthropic's Terminal-Bench 4.0 table has
  no Astra row, so a Claude lead read off it says nothing about Astra. And when
  both vendors publish the same figure to the decimal — as they do for the Claude
  models on TB 4.0 — that is one number re-cited, not corroboration.
- **A saturated benchmark cannot separate candidates.** Terminal-Bench 2.1 sits
  in an 84–88 band, SWE-bench Verified inside ~1 point. Neither is used.
- **Never interpolate between effort rungs.** A missing rung is unknown. Sol at
  `xhigh` and Sonnet 5 at `high` are simply not published — don't estimate them.
- **Never invent a number.** "Not published" is a valid and useful answer.

### 5b. The equivalence band — no fixed constant

Decide "meaningfully better" in this order, and stop at the first that applies:

1. **Published confidence interval.** Terminal-Bench 4.0's owner leaderboard
   publishes 95% CI whiskers. Inside it → equivalent.
2. **Published standard error** → the 95% interval is 2 × SE. Terminal-Bench-
   Science 0.1 publishes SE ±3.5–4.5. An SE published for one benchmark does
   **not** carry over to another in the same source.
3. **Repeated-trial variance under one harness** (e.g. a mean over 5 attempts
   with its spread stated).
4. **A practical-significance threshold the benchmark's own owner publishes.**
   Not one invented here.
5. **None of those → `UNRESOLVED` for that comparison.** Say so, and fall through
   to efficiency. **However large the gap looks.**

> **Score spread is not uncertainty.** "These four models span 40–59, so a
> 7-point gap must be real" is a sentence about how far apart the models happen
> to sit, not about how precisely either score was measured — and on a two-model
> row the spread *is* the gap, so everything would "win". A ratio of gap to
> spread is useful for deciding which benchmark is worth chasing an interval for.
> It is not a finding. `benchmark_frontiers.json` reports it under
> `gap_over_observed_spread_diagnostic` and never routes on it.
>
> **Two consequences worth knowing.** After this rule, `science` is the only
> capability in the record whose direction rests on published dispersion; every
> other capability comparison is `UNRESOLVED` at the evidence layer. That does
> **not** make Step 6's badge table wrong — the badge ranks by *provenance* (who
> ran it, in whose harness), which is a different question — but it does mean no
> direction here is a significance test, and `low-confidence` is the honest word
> whenever one is asked about.
>
> **Zero gap needs no interval.** Two identical scores are equal, not
> indistinguishable; go straight to efficiency. Same for an effort rung that
> scores no better than a cheaper one — that is dominance, not a measurement
> question, which is why Rules E1 and E3 survive this tightening intact.
>
> **High-risk task (`R=3`, or safety/irreversibility in play)** → widen the bar
> for calling parity. When genuinely unsure, take the stronger candidate.

### 5c. Dominance — the efficiency axes

Candidate **A dominates B** when A is *not meaningfully worse* on the
task-relevant capability (5b) **and** clearly better on at least one of, in
priority order: **reasoning tokens → output tokens → total tokens/task → tokens
per *successful* task → quota pressure → cost/task → latency**. A dominated
candidate is never emitted — regardless of tier or brand.

Three dominance results are settled and hard-coded (AA Index v4.3, 10 Sep 2026 —
one harness, one suite, all rungs comparable):

- **Rule E1 — `Sonnet 5 · max` is dominated.** Sonnet 5 max scores 38 at
  $5.09/task; Opus 5 **xhigh** scores 50 at $4.88 and Opus 5 **high** scores 48
  at $3.61. Stronger *and* cheaper. → The router **never** emits `Sonnet 5 ·
  max`. When a mid-tier `D=3` task turns out to need more, the escalation target
  is **`Opus 5 · xhigh`**, not more effort on Sonnet 5.
- **Rule E2 — `Terra · max` is dominated (and unavailable).** Terra max scores
  42 at $1.40; **`Sol · high`** scores 42 at $0.81. Same score, 42% less quota —
  and `max` isn't offered on Terra anyway. → Codex escalation target is
  **`Sol`**, never more effort on Terra.
- **Rule E3 — `max` over `xhigh` buys almost nothing.** Fable 5.1: 53 at both
  rungs ($7.63 → $5.98). Astra: 53 at both ($3.26 → $2.31). Opus 5: 51 vs 50
  ($5.86 → $4.88). → Emit `max` **only** when `D=3 ∧ R=3` **and** the difficulty
  is a *single indivisible novel-design or formal decision* (architecture from
  scratch, boundary design, a proof). For review, audit, migration or
  breadth-driven work at `D=3 ∧ R=3`, stop at **`xhigh`** — the R=3 human-review
  note carries the stakes. The user can always set `max` by hand.
  > **Precision:** the *dominance* holds only on Fable 5.1 and Astra, where `max`
  > ties `xhigh` — a gain of zero at higher cost, which needs no interval. On
  > Opus 5 the one-point gain is **unresolved**, not equivalent, so holding `max`
  > back there is a quota policy, not a free lunch.
- **Rule E4 — on `agentic-code` / `terminal-tool`, `Sol · max` becomes
  `Astra · xhigh`.** Where the rules would emit `Sol · max`, emit `Astra · xhigh`
  instead. AA Index v4.3: Astra `xhigh` 53 @ $2.31 vs Sol `max` 47 @ $1.99; AA
  Terminal-Bench 4.0 (the only independent source covering both ecosystems)
  Astra 59 vs Sol 40, at ~27k output tokens/task against ~78k. Better on
  capability *and* on the axis that outranks cost.
  > **Capability-scoped on purpose.** Tooled HLE puts Astra **behind** on
  > `deep-reasoning` and GDPval shows a regression on `knowledge-work`, so E4
  > must not fire there — a `D=3 ∧ R=3` architecture decision stays `Sol · max`.
  > **And it stops at `max` on purpose:** widening it downward would mean
  > comparing `Astra · xhigh` with `Sol · xhigh`, a rung AA does not publish, and
  > estimating it is the Step 5a interpolation trap. That, not a frequency
  > target, is what keeps Astra rare.

### 5d. Choosing the effort rung

Ask: **what is the lowest rung that reaches the capability level this task
needs?** — not "what does the D table say", and not "how deep can I go". The D
table is the starting point; E1–E4 and 5b are the corrections. Round *down* when
the evidence shows the next rung up is inside the equivalence band; do **not**
round down when the low→high gap on the dominant capability is real.

---

## Step 6 — `✅ RECOMMENDED AI`

Compare the Claude candidate with the Codex candidate and mark exactly one. The
badge is **computed**, never habitual. Decision order:

1. **Hard capability / safety / availability gate.** If one arm declines
   (offensive-security "use Claude", biology "unverified") or lacks the required
   context window, the other arm gets the badge. No further analysis.
2. **Task-relevant capability**, from the dominant tag's evidence anchor.
3. **Benchmark confidence** — tier, date, harness, and *who ran it*. An
   independent evaluator holding the harness constant outranks a vendor's own
   table. A vendor result favouring the **competitor** is against-interest and is
   the most credible vendor evidence there is; one favouring the vendor is
   direction at best.
4. **Near-parity check** (5b). If capability is inside the band, go to 5.
5. **Token / quota efficiency** (5c priority order).
6. **Cost per task.**
7. **Latency.**

"Claude has the better general intelligence index" is **not** on its own a
reason to pick Claude. "Codex scores higher on a coding benchmark" is **not** on
its own a reason to pick Codex on every prompt. The task profile decides.

### Badge table — dominant capability → default side

**The badge is conditional on which Codex model is on the line.** A capability
can genuinely favour Claude against Sol and not against Astra — collapsing that
into one verdict is how a badge ends up wrong half the time. Astra only appears
behind a gate, so the Sol/Terra column is the common case.

| Dominant capability | vs **Terra / Sol** | vs **Astra** | Evidence to name |
|---|---|---|---|
| `agentic-code` | **Claude** | **Codex** — level, efficiency decides | AA Terminal-Bench 4.0: Fable 5.1 52 · Sol 40 · **Astra 59**; Astra 27k output tokens/task vs 78k |
| `terminal-tool` | **Claude** | **Codex** | same TB 4.0 row |
| `science` † | **Claude** | **Codex** | TB-Science 0.1: 52.6 vs Sol 22.4 (SE ±3.5–4.5); the biology gate usually decides first |
| `knowledge-work` † | **Claude** | *no Astra row* → as vs Sol | GDPval-AA v2: 1853 / 1824 vs Sol 1711 |
| `workflow-automation` † | **Claude** | **Codex** | AutomationBench: 31.4 / 26.9 vs Sol ~19 |
| `computer-use` † | **Claude** | **Codex** | OSWorld 2.0 offline partial: Astra 72.6 vs Sol 65.7, ~47% faster/task |
| `latency-volume` | **Codex** | **Codex** | Luna 112 tok/s @ $0.18 vs Haiku 4.5 85 @ $0.21 — both clear a D=0 bar |
| `parallel-independent` (no Claude capability edge on the same task) | **Codex** | **Codex** | Ultra runs ~4 collaborating agents; `ultracode` is one chain |
| `long-context` (shallow) | **Claude** | **Claude** | Sonnet 5's 1M window at $2/$10 vs Astra $10/$50 (2× over 272k) |
| `deep-reasoning` — architecture / maths / formal / tool-less † | **Claude** | **Claude** | Tooled HLE, published by OpenAI and favouring the competitor: Fable 5.1 65.0 · Opus 5 63.6 · **Astra 57.2** |
| `research-synthesis` †, `doc-data-understanding` † | **Claude** | **Claude** | no cross-ecosystem row at all |
| anything else / no evidence | the **lighter** chosen model × effort | same | AA v4.3 cost/task; say `low-confidence preference` |

> **† — the Evidence line must say `low-confidence`.**

> Drop every row where one vendor scored the other in its own harness and these
> capabilities collapse to UNRESOLVED — only `agentic-code` and `terminal-tool`
> survive on independent evidence. That is a fact about the published record, not
> a reason to flip the badge: it is a reason to say the preference is thin.
> Reproduce it with `python scripts/ablate_evidence.py`.

**Tie-breaks**

- **`D ≤ 1` → skip the capability rows entirely; efficiency decides.** At that
  depth both arms clear the bar by construction, so a capability lead is
  unusable. Compare the two chosen models directly: **Haiku 4.5 vs Luna →
  Codex** (Luna is ~5× cheaper per token and the fastest model in the table);
  **Sonnet 5 vs Terra → Claude** ($2/$10 vs $2/$12). `R` doesn't change this —
  it sets the same floor on both arms.
- Two capability rows conflict → the one backed by a **task-specific benchmark**
  beats one backed only by a **product mechanism**. *(A 180-service defensive
  audit is `terminal-tool` + `parallel-independent`: Terminal-Bench 4.0 evidence
  outranks Ultra mode → Claude.)*
- Both arms are gated to the same conclusion (e.g. both declined) → no badge.
- Step 0 blocked → no badge, no models.
- **Genuinely insufficient evidence:** still give the more sensible default —
  but put `low-confidence` in the Evidence line. Never manufacture certainty.

---

## Step 7 — Quota-protection and accuracy rules

Terse list; rationale in `reference.md` §10.5. Only Rule 1's note is auto-added.

1. **R=3 → human-review note** ("Do not apply without human review."). Model/
   effort unchanged. One shared note, not one per arm.
2. **Escalation is a model change, not an effort change** — see Step 4's
   "Escalation request". Sonnet 5 → **Opus 5**, Terra → **Sol**, at the same
   rung. Cranking the mid tier is dominated (Rules E1/E2).
3. **`D=3` outside the flagship capability list → mid-tier default** (Sonnet 5 /
   Terra) at `xhigh`. The mid tier handles analytical / research / review D=3.
4. **User knowledge (not a router output change):** low/medium on Opus 5 is not
   "waste" — Anthropic explicitly recommends using them "liberally as your
   primary control for token cost and response time wherever your evals show
   quality holds."
5. **No `ultracode` for work under 30 min.** For one-off depth, write
   `ultrathink` into the prompt instead.
6. **Long-session / MCP warning:** each MCP server injects tool schemas into
   every message, proportional to tool count (GitHub MCP 27 tools ≈ 18k tokens).
7. **Auto-accept warning:** if R≥2, suggest turning auto-accept off.
8. **Alias safety:** `/model opus` → Opus 5 on Claude Code v2.1.219+.

### Fast Mode (1.5x) — the speed line

Codex CLI has a Fast Mode toggle (user-reported, still not independently
verified — `reference.md` §9.7): output ~**1.5x** faster, quota burns 1.5x,
quality unchanged. Claude analogue: `/fast` — 2.5x faster, **2× price**,
**Opus 5 / Opus 4.8 only**.

**Append one speed line to every CLI Codex output whose Codex line names a real
model.** The first word says which:

- **`recommended`** — when `R ≤ 1` **and** any of: `D ≤ 1` · the volume/latency
  gate fired · the user asked for speed.
  ```
  ⚡ Fast Mode recommended: Codex Fast Mode (1.5x faster, 1.5x quota) — low-risk / mechanical work.
  ```
- **`available`** — every other case.
  ```
  ⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota).
  ```
  If the Claude line is `Opus 5` / `Opus 4.8`, append the Claude half **to the
  `available` form only**: `· Claude /fast (2.5x faster, 2× price).` **Not on
  `opusplan`** — that line names neither model, and execution drops to Sonnet 5
  where `/fast` doesn't exist.

**No speed line** when the Codex line names no runnable model, or on a web
surface. It **does** appear when the offensive gate resolves to `Astra · xhigh`
via stated Daybreak access.

---

## Output format

**Three lines, always.** The two recommendations, then one short Evidence line.

```
Claude: <Model> · effort: <level>
Codex: ✅ RECOMMENDED AI · <Model> · effort: <level>
Evidence: <one sentence>
```

- The badge sits **immediately after the ecosystem label**, before the model
  name. Exactly one badge per output. This is the only accepted placement.
- The `Evidence:` line is **one sentence**, naming at most **1–2** benchmarks or
  efficiency signals — the ones that actually decided it. It is not a
  leaderboard dump.
- **If the badge row you used is marked †, the sentence must say
  `low-confidence`** — those capabilities rest entirely on one vendor scoring the
  other in its own harness.
- No effort for Haiku 4.5; on the Codex side every model takes an effort.
- Add `low-confidence` inside the Evidence sentence when Step 6 says so.

If the user asks "why?" or "show the benchmarks", *then* expand: benchmark,
version, score, effort, harness, token/cost figures, source tier — from
`reference.md` §11–§13 and `benchmarks.json`. Never unprompted.

**The only auto-added extras** (below the three lines, each on its own line):

1. `R=3` → **`Do not apply without human review.`** — goes **last**.
2. `opusplan` → the `⚠️ Effort does not carry over` warning, directly under the
   Claude line.
3. **Speed line** — sits just above the `R=3` note.

### Examples

*"Label these 200 customer reviews as positive/negative"*
```
Claude: Haiku 4.5
Codex: ✅ RECOMMENDED AI · Luna · effort: low
Evidence: Both clear the bar for mechanical classification, and Luna runs ~30% faster per token at slightly lower cost per task.
⚡ Fast Mode recommended: Codex Fast Mode (1.5x faster, 1.5x quota) — low-risk / mechanical work.
```

*"Understand the repo's auth flow and move it to OAuth2"*
```
Claude: ✅ RECOMMENDED AI · Sonnet 5 · effort: high
Codex: Terra · effort: xhigh
Evidence: Agentic multi-file coding is Claude's strongest published margin (Terminal-Bench 4.0: Opus 5 52.3 vs Sol 37.3); Codex takes a +1 notch to compensate.
⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota).
```

*"Find the race condition that flakes in prod sometimes"*
```
Claude: ✅ RECOMMENDED AI · Opus 5 · effort: xhigh
Codex: Sol · effort: xhigh
Evidence: Adversarial debugging inside a repo leans on the terminal/agentic profile where Claude leads against Sol; max needs an indivisible design decision at R=3, and a bug hunt is neither.
⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota) · Claude /fast (2.5x faster, 2× price).
```
> **`xhigh`, not `ultracode`.** The session is long and loops through tools, but
> measure → hypothesise → re-measure is *one* kind of step. No notch either: the
> hard part is the diagnosis and the fix is local.

*"Implement the notifications feature from the architecture doc across the service — about 25 files. Add tests, run lint and the build, and fix whatever breaks."*
```
Claude: ✅ RECOMMENDED AI · Sonnet 5 · effort: ultracode
Codex: Terra · effort: xhigh
Evidence: Discover, implement, author tests, run the build, repair — five kinds of step feeding each other over a long session is exactly what ultracode buys, and 25 files is nowhere near W=3; Codex takes the +1 agentic notch to xhigh.
⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota).
```
> Orchestration is not width. The same session at 150 files of one mechanical
> rename would be `D=1` → `Sonnet 5 · medium`, no mode at all.

*"We have three candidate designs for the event bus. Investigate each one independently against our throughput and ordering requirements, then bring me a comparison."*
```
Claude: Sonnet 5 · effort: xhigh
Codex: ✅ RECOMMENDED AI · Sol Ultra · effort: xhigh
Evidence: Three strands that never wait on each other is a parallelism problem, and Ultra's ~4 collaborating agents are the primitive for it — ultracode is one chain, and D=3 analysis keeps Claude mid-tier.
⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota).
```

*"Design and implement the new cross-service transaction boundary. It ships tonight and cannot be rolled back."*
```
Claude: Opus 5 · effort: max
Codex: ✅ RECOMMENDED AI · Astra · effort: xhigh
Evidence: One indivisible boundary decision at R=3 is the case max exists for — but on agentic code Astra xhigh outscores Sol max (AA Index v4.3: 53 @ $2.31 vs 47 @ $1.99) at roughly a third of the output tokens, so Rule E4 spends the model instead of the rung.
⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota) · Claude /fast (2.5x faster, 2× price).
Do not apply without human review.
```
> The **only** non-gate route to Astra. Change the capability to architecture or
> a written deliverable and it stays `Sol · max` — E4 does not fire outside
> `agentic-code` / `terminal-tool`.

*"These prod migration scripts run tonight with no further review — check them for anything that silently loses or corrupts data"*
```
Claude: ✅ RECOMMENDED AI · Sonnet 5 · effort: xhigh
Codex: Terra · effort: xhigh
Evidence: D=3 review outside the flagship capability list keeps both arms mid-tier; max is dominated on both (Opus 5 xhigh outscores Sonnet 5 max at lower cost), so the review note carries the stakes.
⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota).
Do not apply without human review.
```

*"Run a penetration test against this 180-service environment, build auth-bypass chains"*
```
Claude: ✅ RECOMMENDED AI · Opus 4.8 · effort: ultracode
Codex: use Claude — standard access hard-stops offensive-cyber work (with Daybreak Blue access: Astra · effort: xhigh)
Evidence: Availability gate — standard Codex access ends the run rather than pausing, so the comparison never gets to capability.
```

*"Break this 6000-file legacy Java monolith into independent services"*
```
Claude: Fable 5.1 · effort: max
Codex: ✅ RECOMMENDED AI · Astra · effort: max
Evidence: Capability is level against Astra (AA Terminal-Bench 4.0: Astra 59 vs Fable 5.1 52; Coding Agent Index tied at 62), so efficiency decides — 27k output tokens/task vs 78k.
⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota).
Do not apply without human review.
```
> The gate puts **Astra** on the Codex line, and Claude's agentic-code lead is a
> lead over **Sol** — reading it as a lead over Astra is the Step 5a mistake.
> `max` fires because the boundary design is one indivisible decision (E3).

*"Bump `MAX_RETRIES` from 3 to 5 in the prod config"*
```
Claude: ✅ RECOMMENDED AI · Sonnet 5 · effort: low
Codex: Terra · effort: low
Evidence: D=0 work — both are far past the bar, and Sonnet 5 is the cheaper of the two daily drivers on output tokens.
⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota).
Do not apply without human review.
```

---

## If detail is needed

`reference.md`: **§8** example library · **§10** edge-case rulings · **§11**
capability→benchmark map · **§12** comparability record, conflicts and what
could not be verified · **§13** efficiency/quota data · **§14** recommended-AI
rationale and the ablation checks · **§15** the three-layer evidence
architecture and how to re-derive it · **§16** the reachability audit (which
model × effort combinations the rules can actually produce, and why four of them
are deliberately zero).

**Three layers; only this file is read at runtime.** `benchmark_frontiers.json`
is generated by `scripts/compile_benchmark_frontiers.py` from `benchmarks.json`
and is there for auditing a rule, not for answering one. **Never load either to
route a prompt** — the rules above are their compiled form, and re-reading 120+
records per route is exactly the quota waste this router exists to prevent.

**The router does not select a model from a benchmark number, and it does not
ignore benchmarks either.** Evidence sets the *direction* and the *equivalence
band*; the capability profile decides which evidence applies; efficiency breaks
the ties that capability leaves open. A leaderboard position on its own decides
nothing.
