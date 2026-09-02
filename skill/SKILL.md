---
name: model-secici
description: >-
  Reads a prompt and recommends, separately for Claude (Haiku 4.5 / Sonnet 5 /
  Opus 5 / Opus 4.8 / Fable 5.1) AND Codex/ChatGPT (Luna / Terra / Sol / Sol
  Ultra), which model + effort level to run it on — both in one short output.
  Use when asked "which model", "which effort", "pick a model", "what should I
  use for this prompt", or when /model-secici is invoked.
---

# Claude & Codex model / effort router

Analyse the user's prompt and say, **separately for Claude and for
Codex/ChatGPT**, which model and which effort level to run it on — both
together, in one output. Do **not** run the prompt — only route it. The user
decides which recommendation to use; this router starts nothing automatically.

**Calibration: two separate subscription quotas.** The protected resource is not
dollars — it's Claude's 5-hour window **and** ChatGPT Plus's 3-hour ("Instant")
+ weekly ("Thinking") windows. The real danger isn't picking a model that's too
weak; it's *reflexively picking the most expensive model and burning the quota*.
When in doubt, round **down**.

**Token efficiency — read this.** This skill produces two recommendations, which
is naturally a bit more work — but **not double**. Compute R/D/W/C **once**, then
read two short tables. Run Steps 0–3 silently in your head — don't write each
step out, just produce the final two lines. Show no intermediate step unless the
user asks "why?".

**Claude model roster (as of 1 September 2026):**

| Model | Role |
|---|---|
| Haiku 4.5 | Speed/volume specialist. No effort parameter |
| Sonnet 5 | Daily work — speed+intelligence balance. **Default starting point** |
| **Opus 5** | **Flagship.** Complex agentic code and enterprise work. Replaced Opus 4.8 |
| Opus 4.8 | Legacy — the **only** lasting role is the offensive-security gate |
| **Fable 5.1** | Frontier scale: long-horizon autonomy, extreme breadth, **biology-adjacent R&D**. Replaced Fable 5 (1 Sep 2026) — same **$10/$50** price, but cache reads are **¼** ($0.25/MTok); knowledge cutoff Jun 2026 |
| Mythos 5.1 | **Same model** as Fable 5.1 with permissive safeguards — **Project Glasswing invite only** (verified cyber-defender / life scientist; US-first). The router recommends it only if the user explicitly states they have this access |

> Opus 4.8 is still "legacy" — Anthropic recommends moving to Opus 5 for general
> work. Its one lasting job: when an **offensive** security request is flagged,
> it is one of Fable 5.1's permitted fallback targets (the other is Opus 5). The
> router skips that redirect and recommends Opus 4.8 directly.
>
> **Fable 5.1 vs Opus 5 — Anthropic's framing:** "Start with Opus 5 for most
> work; if you've tried Opus 5 at `xhigh`/`max` effort and it still falls short
> on demanding reasoning or long-horizon agentic work, move to Fable 5.1." This
> router already recommends Fable 5.1 only at the frontier-scale and biology
> gates — consistent with that framing, no extra rule needed.

**Codex/ChatGPT model roster (GPT-5.6 family, as of 9 July 2026):**

| Model | Role | Claude analogue (rough, not an equal-performance claim) |
|---|---|---|
| Luna | Speed/volume specialist, cheapest tier | Haiku 4.5 |
| Terra | Daily work, balanced — **default starting point** | Sonnet 5 |
| **Sol** | **Flagship** — code/science/security | Opus 5 |
| **Sol Ultra** | A Codex *mode* toggled on Sol (Plus plans+): ~4 collaborating agents in parallel (more in "multiagent v2"). Not a separate model | No clean analogue — a stronger parallelism primitive than Claude's `ultracode` |

> Fable 5.1 (frontier scale + biology-adjacent) has **no** verified analogue on
> the Codex side. For offensive-security and biology-R&D prompts the Codex line
> says "unverified", recommends no model (see Codex arm hard gates).

> **Source note:** this table was verified directly against
> `openai.com/index/gpt-5-6/`,
> `developers.openai.com/api/docs/guides/reasoning`,
> `learn.chatgpt.com/docs/config-file/config-reference` (5 August 2026). The
> price figures in the secondary report the user provided were **stale/wrong**
> (they didn't reflect the 30 July price cut) — see `reference.md` §9 "Data
> status".

---

## Effort levels (Claude Code `/effort` menu)

| Level | What it does |
|---|---|
| `low` | Short, well-scoped work that needs no intelligence |
| `medium` | Cost-sensitive work; gives up some intelligence |
| `high` | **Default** (every model that supports effort) |
| `xhigh` | Deeper reasoning. 30 min+ agentic/coding work |
| `max` | Deepest reasoning. Diminishing-returns risk, over-thinking tendency. Per-session |
| `ultracode` | `xhigh` + **dynamic workflow orchestration** for every substantive task. Per-session |

Know four things:

1. **`ultracode` is not a model effort level, it's a Claude Code setting.** It
   sends `xhigh` to the model and adds dynamic workflow orchestration on top.
   `/effort ultracode` or `claude --effort ultracode`. Can't be written to a
   config file. **No model restriction** — it works on every model that supports
   `xhigh`: Fable 5.1, Sonnet 5, **Opus 5**, Opus 4.8, Opus 4.7.
2. **Haiku 4.5 does not support the effort parameter.** When recommending Haiku,
   write no effort.
3. **Opus 5 specific (general knowledge, see Step 4 Rule 4):** Anthropic
   recommends low/medium effort "as a normal cost control wherever your eval
   holds up" — on earlier Opus generations (4.7/4.8) low effort was a shadowed
   option. Because this router recommends Opus 5 only when `D=3`, its own output
   always means `xhigh`/`max`; but the user should not hesitate to run Opus 5 at
   low/medium manually.
4. The effort scale is **calibrated per model**. The same name means a different
   value on a different model.

Effort is not a token budget, it's a behavioural signal. Figures like
"low = 1,024 tokens" are made up; don't use them.

---

## Step 0 — Prompt quality gate

**Do not skip this step.** Before scoring, run these four checks in order.
Asking a single "is there a success criterion/scope?" question is not enough —
most real prompts contain scope but carry an unnoticed ambiguity inside them.
If any of these is "yes", **recommend no model**, clarify first.

1. **Is there a rule stated by example but not generalised?** The prompt says
   "for instance, if X then Y" but doesn't state the general formula/percentage/
   threshold?
   > "500 of 1000 units land on the same day" — is that 50%, a fixed 500, or a
   > cutoff by production hour? **An example does not stand in for the general
   > rule.**
2. **Would a wrong assumption silently produce a wrong result?** The code runs
   without error but systematically miscalculates on real data? (Not a crash,
   a silent wrongness — the kind that takes longest to notice and is most
   dangerous.)
3. **Is the target concrete?** "We'll do it like this in the system" doesn't say
   *which query/service/table/file*. It looks like it has scope but doesn't.
4. **Do two plausible but different implementations come out of the same
   prompt?** If so it's unclear which was wanted — you (the router) may be
   making an assumption without noticing which one you chose.

When clarifying, **don't just say "it's unclear"** — ask concretely what exactly
is missing:

> "Fix this code" → *Which code? Broken how? How do we know it's fixed?*
> "500 of 1000 units should land on the same day" → *Is that always a fixed 500,
> or a percentage of production (e.g. 50%)? Or is it determined by production
> hour (e.g. same day if before 14:00)? This completely changes the calculation
> logic — and the R/D score.*

Sending an unclear prompt to the most expensive model is pure quota waste — the
model guesses the context, guesses wrong, the work is redone. Worse: if it
produces silently-wrong code as in (2), the error can take weeks to surface.

---

## Step 1 — Hard gates (Claude side)

Check in order. There are two kinds of gate — don't confuse them:

- **Deciding gate** (rows 1–3, 5): decides **which model** on its own, **bypasses**
  Step 2/3's model-selection logic. But it does not bypass evaluating
  effort-modifier signals like W/duration (e.g. `ultracode` eligibility) — those
  are separate from model selection and are still checked after the gate (see
  the note under "Why offensive security").
- **Eliminating gate** (row 4, context >200k): only **removes one candidate**
  from the list (Haiku), does not decide which model — Step 2/3 scoring runs
  normally among the remaining candidates (Sonnet 5 / Opus 5 / Fable 5.1).

| Condition | Kind | Result |
|---|---|---|
| Sub-second latency **or** high-volume classification/parsing | Deciding | **Haiku 4.5.** No effort. Stop, done |
| **Offensive security:** exploit generation, penetration testing, binary-based vulnerability scanning | Deciding | **Opus 4.8**, **effort floor `xhigh`** (W/duration signals are still evaluated → can rise to `ultracode`, see the note below) — with Glasswing access, **Mythos 5.1** |
| **Biology-adjacent R&D:** genomics, protein/chemistry-heavy pipeline, bio-CTF | Deciding | **Fable 5.1** (see the note below) |
| Context exceeds 200k tokens | **Eliminating** | **Haiku 4.5 removed**, Step 2/3 runs normally with the rest |
| **1000+ files / whole-codebase scale** (frontier scale) | Deciding | **Fable 5.1** |

> **Defensive security work does not trigger this gate.** "Audit this code/infra
> for vulnerabilities", "find open ports", "review the security-group rules" —
> that's defensive work that doesn't generate exploits. Fable 5.1 can **do this
> itself** as of 1 Sep 2026 (it was blocked on Fable 5); it goes to normal
> scoring (usually Sonnet 5 · `xhigh` or Opus 5). Only the three offensive
> categories above trigger the gate.

> **Frontier-scale gate — one signal is enough.** This gate does not look for
> three separate conditions like "thousands of files **AND** filling 1M context
> at once **AND** persistent memory" — **just the file/scope count** (1000+) is a
> sufficient trigger. Understanding work at that scale **already requires**
> filling 1M context at once and multi-session persistent memory; the prompt
> doesn't state that separately and isn't expected to.
> ✅ "Break up this 4000-file legacy monolith into modules" — only the file count
> (4000) is written, "concurrent context" or "persistent memory" never appears,
> the gate still fires → **Fable 5.1**.
> **Don't confuse it with Step 2's `W=3` threshold (100+ files):** 100–999 files
> does not trigger this gate, it goes to normal scoring (`W=3`, model per Step 3
> — usually Opus 5 or `opusplan`). This gate fires only at genuinely thousands
> (1000+).

### Why offensive security → straight to Opus 4.8

Fable 5.1, Opus 5, and Sonnet 5 each have **their own** safety classifiers. When
an offensive request (exploit generation, penetration testing, binary-based
vulnerability scanning) is flagged, Fable 5.1's permitted fallback targets are
**Opus 4.8 and Opus 5**. The router skips that redirect and recommends **Opus
4.8** directly (the most permissive general model on cyber posture; Opus 5 is
also a valid target). Do not recommend Sonnet 5 — it is deliberately isolated
from exploit generation (0% working-exploit rate on the Firefox 147 evaluation).

What changed with Fable 5.1 vs Fable 5: (a) defensive vulnerability discovery is
no longer **blocked** — Fable 5.1 does it itself (the gate note above), (b) on
benign requests, cyber interventions dropped **~60%** per session.

> **Mythos 5.1 for verified defenders.** Defensive security teams admitted to
> the Cyber Verification Program / Project Glasswing can use **Mythos 5.1**
> (`claude-mythos-5-1`) with permissive safeguards — but it's **invite only**,
> US-first. If the user doesn't state this access, the router's recommendation
> stays **Opus 4.8**; if they do, recommend `Claude: Mythos 5.1 · effort: xhigh`.

**`ultracode` can still rise above the `xhigh` effort floor.** Even though this
gate is "deciding", it only fixes the **model** — it doesn't bypass Step 2/3
evaluating the W/duration signals. **After** the gate fires, check
`W=3 ∧ duration>30min ∧ ¬(D=3 ∧ R=3)` normally; if it holds, effort is not
`xhigh` but **`ultracode`** (see the "180-service penetration test" example in
Output format).

### Why biology-adjacent → Fable 5.1 (not Opus 5)

On benign/educational biology-medical questions, safeguards now fire **~85%
less** — those are not a gate, they go to normal scoring. The gate is only for
**R&D-heavy** biology-adjacent work:
- **Fable 5.1** → R&D-flagged parts are automatically redirected to **Opus
  models** (expected behaviour, not an error)
- **Opus 5** → biology R&D has **no fallback at all, it refuses directly**

So if you recommend Opus 5 directly the user may hit a flat refusal message.
Recommend Fable 5.1. Researchers admitted to the Life Sciences Verification
Program use **Mythos 5.1** for professional R&D (invite only, US-first) — if the
user states that access, recommend Mythos 5.1.

**Do not put an effort floor on Fable 5.1.** Its default is `high`; the gain
over Fable 5 is widest at high effort but it's strong at low effort too. Note:
Fable 5.1 calls search/retrieval tools less often at `low` effort — for work
that needs fresh information, raise the effort.

---

## Step 2 — Score on four axes, 0–3

A one-word adjective ("complex", "multi-step") stays wobbly. For each axis
**ask the diagnostic question first**, then look at the level. If unsure, find
the closest analogue in the example library in `reference.md` §8.

### R — Risk / irreversibility

*Diagnostic: if the output is wrong, does fixing it take minutes or days? Is
there automatic rollback (git revert, feature flag, rollback)? How many
users/systems are affected? Is there money/health/legal/reputation risk?*

`0` Throwaway draft — no loss even if never used (idea, alternative, exploration)
`1` Will be used but a human reviews and approves it (PR, draft email)
`2` Goes straight to a real system but is reversible (isolated one-line config, feature-flagged deploy, reversible migration) — **being architectural/multi-service does not on its own make it R=3**, but **a one-line change that governs system-wide behaviour is not automatically R=2 either**, see the notes
`3` No way back / very costly — data-loss risk, irreversible migration, outbound message/payment, an irreversible or disproportionately costly architectural decision, medical/legal/financial advice, touching live user data

> **The "architectural decision" label does not on its own make it R=3.** The
> real question is reversibility: if the new component can be rolled out
> service-by-service / feature-flagged / gradually and stopped and rewound when
> something breaks, then **even if it's architectural it's R=2**. R=3 applies in
> two cases: (a) there is no real rollback mechanism (live data-schema
> migration, irreversible data transformation), **or** (b) what's being designed
> is a **central/shared** core the whole system depends on (identity/auth
> infrastructure, data model, trust boundary) — here rolling back is not "which
> component do I switch off?" but unpicking a shared decision dozens of services
> have already become dependent on.
> ✅ R=2: "Migrate 40 microservices to a shared auth middleware" — each service
> uses its own middleware **independently**, service-by-service phased migration
> and rollback are possible; architectural but reversible.
> ❌ R=3: "Redesign the auth architecture of 200 prod services from scratch" —
> what's designed here is a single, central identity/authorization core (token
> schema, trust boundary) that all 200 services **jointly depend on**;
> service-by-service phased rollout doesn't make it reversible, because the
> design decision itself is shared and gets disproportionately expensive to
> unpick as services become dependent on it — genuine R=3.

> **Large decomposition — module or service?** "Break the monolith into
> **modules**" = internal refactor, reversible via a gradual/strangler-fig
> approach → **R=2** (see validation id 8, `Fable 5.1 · ultracode`). "Split into
> separate **services / processes**" = introduces network + data-ownership +
> deploy-topology boundaries; once the services become interdependent,
> re-merging them is disproportionately expensive → **R=3** (criterion b: shared
> core). The frontier gate fixes the model (Fable 5.1) in both cases, but the
> effort changes: R=2 → `ultracode`, R=3∧D=3 → `max`.

> **First separate this: is it a change in the codebase, or a live/operational
> value?** A normal codebase change (component colour, text, CSS, any source-code
> line) is **R=1 by default** — the normal engineering flow is to review it via
> PR and deploy it that way (that's the definition of R=1 itself). **R=2/R=3
> only kick in if the prompt explicitly points at a value that goes straight to
> a live system without code review** — a prod config file, a live admin panel,
> a feature-flag toggle, a setting stored in the database. A vague phrasing like
> "change the settings page's default theme" is **assumed to be a codebase
> change** → R=1, absent a signal to the contrary.
>
> For a directly-operational value too, **"one-line config" does not on its own
> make it R=2.** The real question is not the **line's length but its blast
> radius**: even if rolling it back is technically instant, in the **window
> between deploy and being noticed** how many systems/users are affected? If
> you're changing an isolated operational value (one feature-flag default), R=2.
> But if the line governs **system-wide behaviour** (retry count, timeout, rate
> limit, connection-pool size) and a wrong value can cause a **gradual outage**
> (retry storm, connection exhaustion) before a human notices, it's R=3 even as
> one line.
> ✅ R=3 example: "Bump `MAX_RETRIES` from 3 to 5 in the prod config" — "in the
> prod config" explicitly points at a live/operational value, it doesn't go
> through code review; retry count governs system-wide load/resilience
> behaviour → genuine R=3.
> ❌ R=1 comparison: "Change the settings page's default theme colour (in the
> component code)" — a normal code change, goes through a PR; no signal it goes
> straight to live → R=1, no barrier for Haiku/Luna.

### D — Depth

*Diagnostic: is there a known/standard solution pattern, or does it have to be
thought out from scratch? How many different approaches is a choice being made
between? Is it solved by trial-and-error or by getting the design right in one
pass?*

The field means different things — look at it **by the kind of work**, not just
by coding:

| Level | Coding | Writing/analysis | Research | Data |
|---|---|---|---|---|
| `0` | Pattern matching, recalling a known constant; **a fully-specified additive schema change** (column name + type + nullable all given — no design decision) | One-sentence answer **or** pure form/tone change with no content change (length irrelevant — even 3 paragraphs, if there's no choice/trimming/synthesis it's D=0) | Single-source lookup | Reading a single number |
| `1` | Standard pattern (CRUD, known bug shape); a schema change but there's a choice (index type, backfill strategy, constraint) | Simple summary/draft | Single-source summary | Simple filter/aggregation |
| `2` | Multi-step but well-documented feature | Report based on multi-source synthesis | Multi-source synthesis | Statistical inference |
| `3` | Design from scratch, concurrency, algorithmic complexity, balancing conflicting constraints; **adversarial security-vulnerability hunting** (finding subtle logic errors) | Building an original argument, reconciling conflicting sources | Producing a new hypothesis/framework | Modelling, causal inference |

> **The D=1 / D=2 boundary — "well-documented" does not on its own make it D=2.**
> The real question: how many **independent design decisions** are left to you
> (the implementer)? If a recipe/library/tutorial is being followed and there's
> a single reasonable approach → D=1; the pattern being "standard" doesn't move
> it to D=2. If you have to choose between more than one reasonable approach
> (and the choice affects the outcome) → D=2.
> ✅ D=1: "Add cursor-based pagination to this API" — a common, well-documented
>    single pattern; a library/tutorial is followed, no design decision.
> ❌ D=2: "Add both cursor and offset pagination to this API in a
>    backward-compatible way, decide when each is used" — there's a real choice
>    (two approaches + a backward-compatibility constraint).
>
> **When in doubt stay at D=1, don't force D=2** — a "this is more than a
> one-liner" feeling is not sufficient grounds for D=2; the quota-aware default
> is to round down (see the calibration note).

### W — Width

*Diagnostic: how many files/documents get read or changed? Are the pieces of the
work independent (parallelisable) or sequential?*

`0` Single file/document
`1` 2–5 files, within one module
`2` **6–99 files/units** (across a subsystem, including the same small change repeated across many services) **or** 2–3 different verification angles (e.g. correctness + performance)
`3` **100+ files** / whole codebase **or** 3+ independent, parallelisable verification angles (e.g. security + performance + style + test-coverage together)

> **The W=2 / W=3 threshold is numeric — 100.** "Add the same endpoint to 60
> microservices" sounds big but 60 < 100 → **W=2**, not W=3. `ultracode`
> requires W=3, so repetitive mechanical work over 20–99 units **does not** rise
> to `ultracode` (effort follows D). If there are genuinely 100+ files or 3+
> independent verification angles, W=3.

### C — Context synthesis

*Diagnostic: is the model fine with its own knowledge, or how much does it have
to read from outside (files, docs, chat history)?*

`0` Self-sufficient, no extra reference needed
`1` A few small files/documents
`2` A medium-sized codebase/documentation (a few thousand lines, one README + a few modules)
`3` Synthesis of a large corpus (hundreds of pages of docs, a huge codebase, a long chat history)

---

## Step 3 — Mapping

Model selection is based on the **intelligence need** (D, C) — risk (R) does not
raise the model, it raises human oversight. This distinction matters: in the old
design R forced the model straight to Opus, then a separate rule walked it back.
Now R does not affect the model, only the "human review" note and the effort
floor.

**Model** ← `max(D, C)`. Important: **Opus 5 is a candidate only when `D=3`** —
`C=3` on its own (large context synthesis while D is low) does not trigger Opus
5, it stays on Sonnet 5. Reason: Opus 5's justification is a deep-reasoning need;
a large but shallow synthesis job is already handled by Sonnet 5's 1M context
window.

| Condition | Model |
|---|---|
| `D = 0` **∧** `W=0` **∧** `C≤1` **∧** `R≤1` | **Haiku 4.5** |
| Above not met and `max(D,C) ≤ 1` | Sonnet 5 |
| `max(D,C) = 2` | Sonnet 5 |
| `max(D,C) = 3`, but `D<3` (i.e. `C=3` triggered it) | **Sonnet 5** — large context, shallow reasoning |
| `max(D,C) = 3`, `D=3` | **Opus 5** — if the task is agentic multi-step code / math-proof / tool-less deep reasoning (Rule 2). **Otherwise Sonnet 5** (quota-aware default — see Rule 3) |

**Why Haiku only at D=0:** D=1 means "known pattern" — an N+1 query fix, standard
input validation, a known bug shape. Those aren't pattern matching, they need
real judgement. When `max(D,C)≤1` and D=1, the floor is Sonnet 5, not Haiku.
Haiku fits only at D=0 (genuinely trivial — typo, one-line expression change,
recalling a known constant).

**Why the R threshold is 1, not 3:** `R=2` means "goes to prod but reversible" —
that's still a real prod change, not trivial enough to leave to Haiku's
speed/volume profile. Reserve Haiku for throwaway drafts / to-be-reviewed work
(`R≤1`); `R=2` wants at least Sonnet 5.

**R floor (general):** if `R = 3`, Haiku is never selected, the floor is Sonnet
5 — don't leave simple-but-irreversible work to the weakest model. `R=3` also
always adds a human-review note to the output (Step 4, Rule 1).

**Effort** ← `D` — **independent of the model, always by this table.** Whatever
model is selected (including Opus 5), effort follows D. Phrasings like "xhigh" in
the model table do **not** conflict with the D=3 row of the effort table, they
just remind you what happens at D=3.

| D | Effort |
|---|---|
| 0 | `low` |
| 1 | `medium` |
| 2 | `high` |
| 3 | `xhigh` |
| 3 ∧ R=3 | `max` |

If Haiku 4.5 is selected, leave the effort field blank — the model doesn't
support the parameter.

**Consequence:** in this router Opus 5 **always appears together with D=3**
(`xhigh` or `max`) — it is never recommended with `low`/`medium`, because Opus 5
is only selected at D=3 in the first place. This doesn't contradict Step 0's
"don't shadow low/medium on Opus 5" note: that note is not about the router's
**own recommendation**, it's general knowledge the user needs when running Opus
5 **manually** (via `/effort`). The router simply never recommends Opus 5 for
any non-D=3 work.

**`ultracode`** ⇔ all three true:
`W = 3` **∧** estimated duration > 30 min **∧** `¬(D=3 ∧ R=3)`

`ultracode` sends `xhigh` to the model. In the effort field write **`ultracode`**,
not `xhigh`. No model restriction — it works on every model except Haiku
(including Sonnet 5, Opus 5, Opus 4.8, Fable 5.1); it runs on whichever model
was chosen (**by Step 3 scoring or by a Step 1 deciding gate** — e.g. offensive
security → Opus 4.8). `ultracode` is not part of model selection, it's an
independent effort-modifier that rides on top of the chosen model — which is why
even when a Step 1 gate "overrides scoring", the W/duration check still runs.

> **Conflict resolution.** If `D=3 ∧ R=3`, effort is `max`, `ultracode` **no**.
> `ultracode` only sends `xhigh`; you'd lose `max`'s depth. Also, spreading
> irreversible work across parallel workflows makes oversight harder. Depth →
> `max`. Width → `ultracode`.

### `opusplan` — plan/execute model split

**Only in Claude Code, not on Claude.ai.** `/model opusplan`: in plan mode it
uses `opus` (→ Opus 5), in execution mode it automatically switches to `sonnet`
(→ Sonnet 5). Purpose: make the architectural decision with the expensive model,
do the bulky mechanical implementation with the cheap one — fewer tokens than
running one model start to finish.

**`opusplan`** ⇔ all three true (**overrides** the `Opus 5` branch of Step 3):

1. `max(D,C)=3 ∧ D=3` **∧** the task is in Rule 2(a) territory (structured
   design/architecture)
2. **Difficulty is front-loaded into the plan.** Diagnostic: *once the plan is
   done, do most of the execution steps follow a similar/repeating pattern?* If
   yes, it's front-loaded. The opposite case — difficulty persists throughout
   execution: debugging (the real cause isn't known without looking at the
   code), formal proof (the proof itself is both plan and execution,
   inseparable), new algorithm design (design = execution). In that case do
   **not** recommend `opusplan`, plain Opus 5 stays.

   > **The execution verb may not be written — the target-scope count is enough
   > of a signal.** Even if the prompt contains no execution verb like
   > "apply/migrate/roll out", if the design's **target scope is made concrete
   > with a number** ("design X for 200 services", "define Y for 40
   > microservices"), that number implies the execution phase already exists —
   > if a design specifies "how many systems it will be applied to", it would be
   > meaningless for it not to be applied. The word "design" alone does not
   > override the front-loading signal.
   > ✅ "Redesign the auth architecture of 200 prod services from scratch" — the
   > verb is only "design", but the target is concrete as "200 services";
   > execution (applying to 200 services) is implied → front-loaded, `opusplan`
   > candidate.
3. `W ≥ 2` — there's enough implementation volume to make the mode switch pay
   off. For a small `W≤1` decision the mode switch is just overhead, plain Opus 5
   is enough.

> ✅ "Migrate 40 microservices to a new auth middleware; define the design once,
>    apply the same pattern to each service" — the middleware design is
>    front-loaded, the pattern repeated across 40 services = mechanical
>    execution, W=3.
> ❌ "Find the race condition that flakes in prod sometimes" — difficulty
>    persists throughout execution (the cause isn't known without reading the
>    code), plain Opus 5 · max stays.
> ❌ "Decouple this router's model selection from risk" — W=1, insufficient
>    volume; and execution needed judgement too (tested live in this session,
>    the plan didn't become mechanical in one pass), plain Opus 5 stays.

**Output format (added under the `Claude:` label, the warning as its own line —
the Codex line is unaffected, it comes from its own normal mapping):**
```
Claude: opusplan · plan: <effort> · execute: <effort>
```
Plan effort = Rule 2(a)'s normal result (`xhigh`, or `max` if `R=3`).
Execute effort = per the post-plan estimated D (usually `medium`, rarely `high`).

> ⚠️ **Effort does not carry over.** Opus 5 and Sonnet 5 are both "hold"-free —
> the effort you set in plan mode **stays as is** when you switch to execution,
> it does not drop automatically. When you switch to execution mode you have to
> set it manually with `/effort <execute effort>`; if you skip that, Sonnet 5
> runs at a needlessly expensive effort and `opusplan`'s quota-saving purpose is
> defeated.

This warning is added **to every `opusplan` output** as a second line — it is one
of the two mandatory exceptions in the Output format section, outside the
"explain only when asked" rule.

**Advanced combination (unverified, optional suggestion — NOT added to output).**
If `W=3`, `ultracode` on Sonnet 5 during the execution phase can also be
considered (apply the huge migration in parallel). This combination is untested
in the official docs; it is not on the mandatory-exception list, so it doesn't
go in the default output — if the user asks "what else can I do / why?", suggest
it with a "try it, fall back to plain `high` if it doesn't help" note, don't
present it as firm advice.

---

## Step 4 — Quota-protection and accuracy rules

**1. R=3 → human-review note.**
If the work is irreversible (prod migration, architectural decision,
medical/legal/financial), the model/effort stay as they came from Step 3 but a
"do not apply without human review" note is added to the output. For
simple-but-risky work (D≤1) this is sufficient warning on its own; no need to
raise the model.

**2. Prefer Opus 5 in these three areas (Rule 2 areas).**
These three are a partly-verified pattern carried over from the Opus 4.8 era —
Opus 5's own granular numbers (SWE-bench Pro / Terminal-Bench / HLE) weren't
published separately, but Opus 5's overall jump over Opus 4.8 (more than 2x on
Frontier-Bench, leading on GDPval-AA/OSWorld) strongly indicates at least the
same-direction advantage in these three areas:
**a) Agentic multi-step structured work** — multiple files, architecture design
from scratch, large refactor/migration; there's a real design decision requiring
D=3. **Not limited to a programming language** — rule-engine/decision-tree
design, system/prompt architecture, any structured system balancing conflicting
constraints also counts (e.g. designing a skill's own decision logic from
scratch).
> ✅ "Move this service to an event-driven architecture, including message
> ordering and idempotency"
> ✅ "Decouple this router's model selection from risk, design the conflict rules"
> ❌ "Fix the bug in this one file" — file count doesn't matter, D is usually 1–2

**b) Mathematics / formal proof** — algorithmic-complexity analysis, correctness
proof, numerical optimisation.
> ✅ "Prove this algorithm's worst-case complexity and find a better one"
> ❌ "Compute this average/percentage" — arithmetic is D=0–1, math is not D=3

**c) Tool-less deep reasoning** — the model has to produce a deep analysis/
decision from the prompt content alone, **calling no tools** (no file reading,
code execution, search).
> ✅ "Without running code, discuss the trade-offs of these two architectural
> approaches"
> ❌ Any task running inside Claude Code — file reading / running tests already
>    counts as "tooled", it doesn't hit this exception (the note below explains)

> **Tool access flips the decision.** Sonnet 5's raw-intelligence gap tends to
> close with tool orchestration (Opus 4.8-era data: on tool-less HLE Opus is
> +6.6 ahead, with tools it's parity). If the task involves Claude Code / web
> search / code execution, Sonnet 5 is usually enough. If pure-context
> proof/analysis is asked, go up to Opus 5. **Practical upshot:** the vast
> majority of work running in a Claude Code session is already "tooled" — which
> is why sub-rule (c) rarely triggers; the frequently-triggered ones are (a) and
> (b).

**3. D=3 but not in Rule 2 → default Sonnet 5 · xhigh (quota reason).**
Anthropic's own equal-effort comparison still doesn't exist, but **LiveBench
2026-06-25** (independent, contamination-free) shows Opus 5 above Sonnet 5:
agentic coding +5.8, language +13.7, reasoning +2.5, math +2.8 (see
`reference.md` §2.1). The router still keeps the cheap side (Sonnet 5) as the
default for quota reasons — Opus 5's cost-per-successful-task on LiveBench is
~1.4x Sonnet 5's, and the difference doesn't justify every job. But:

> ⚠️ Escalate: if the result is insufficient or the work is critical → Opus 5 ·
>   xhigh. No longer unproven — on LiveBench Opus 5 is clearly ahead of Sonnet 5
>   on this axis, especially on language/reasoning-heavy D=3 work.

**4. User knowledge (does not change the router's output): low/medium on Opus 5
is not "waste".** Anthropic's Opus 5-specific advice: start from `high`
(default), go to `xhigh` for coding/agentic work, **and use low/medium freely as
a cost control wherever your eval holds up.** This is a deliberate departure from
the Opus 4.7/4.8 "waste at low effort" framing.

This router already recommends Opus 5 only at `D=3` (→ effort `xhigh`/`max`), so
it will never recommend Opus 5 with `low`/`medium` in its own output — that
combination logically doesn't arise. This note exists to tell the user "it's not
waste" if they choose, **on top of** the router's recommendation, to run Opus 5
at low effort — not for the router's own decision.

**5. Do not recommend `ultracode` for work under 30 minutes.**
It plans a workflow for every substantive task; on everyday work it adds latency
and quota, not quality. If you want one-off deep thinking, **write `ultrathink`
into the prompt** — it adds depth for that turn without changing the effort
level.

**6. Long-session warning.** If MCP servers are connected, remind: each server
injects tool schemas into every message. The load is not fixed per server, it's
**proportional to the tool count** (GitHub MCP: 27 tools ≈ 18k tokens;
Playwright: 21 tools ≈ 13.6k). Turn off the ones you're not using.

**7. Auto-accept warning.** If R≥2, suggest turning auto-accept off — chained
edits both burn quota geometrically and make rollback harder.

**8. Alias safety.** When the user types `/model opus`, on Claude Code v2.1.219+
it resolves to **Opus 5**; on an older version it may fall to Opus 4.8. When the
router recommends "Opus 5" and the user still sees Opus 4.8, suggest they run
`claude update` or pin it explicitly with `/model claude-opus-5`.

---

## Codex arm

Compute this **in parallel, at the same time** as the Claude arm — there is no
ecosystem selection, both are always produced. The R/D/W/C scoring is **exactly
the same as the definitions in Step 2**, compute it once, read two tables (Step 3
and the one here). Only the mapping table and model roster change.

### Codex hard gates

| Condition | Result |
|---|---|
| Sub-second latency / high-volume classification | **Luna**, effort `minimal` |
| **Offensive security / biology-adjacent R&D** (same definitions as Step 1) | Codex line: **"unverified — use Claude"**, no model recommended. Whether Codex has a safety-classifier/fallback behaviour like Claude's for these categories **was not researched** — rather than make up something I don't know, I honestly leave it blank. |
| Very large context | ⚠️ Per-model context windows **could not be verified** (only a single-source ~1.5M claim for Sol Ultra). I set no threshold — leave it to normal mapping by C score. |

### Codex mapping (R/D/W/C → Model, parallel logic to Step 3)

| Condition | Model |
|---|---|
| `D=0 ∧ W=0 ∧ C≤1 ∧ R≤1` | **Luna** |
| Otherwise `max(D,C)≤1` | Terra (`D=1` → `effort: low`) |
| `max(D,C)=2` | Terra (`effort: medium`) |
| `max(D,C)=3`, `D<3` (C triggered it) | Terra — the large-context/shallow-reasoning logic carried over from Claude, not separately verified on Codex but the same principle applies |
| `max(D,C)=3`, `D=3` | **Sol** — *if the condition below holds*, **Sol Ultra** |

> **Luna and `Terra · low` are real results that should come up often — if
> you're always getting "Sol high or Terra medium" that's a bug.** A problem
> found in live use: D=1 work (common pattern) rounds up to D=2 under
> uncertainty, D=0 work (genuinely mechanical) rounds up to D=1 — see the D=1/D=2
> boundary note above, the quota-aware default is to round **down**.
> ✅ Luna: "Rename this variable from `usr` to `user`" (D=0, mechanical) ·
>    "Rewrite these three paragraphs in a more formal tone" (D=0, content
>    unchanged)
> ✅ `Terra · low`: "Add email validation to this form" (D=1, standard pattern) ·
>    "Add cursor-based pagination to this API" (D=1, well-documented single
>    pattern)

**Sol → Sol Ultra diagnostic** (the Codex analogue of `ultracode`, but slightly
different from Step 3's `ultracode` condition — here "independence" is the key
criterion):
*Does the work split into 3+ separate pieces (different module/service/
verification angle) that can run unaware of each other and be merged at the end
— or are the pieces interdependent, requiring a single coherent design
decision?* If genuinely independent (and it already got to `D=3→Sol`) → **Sol
Ultra**.

> **What "Sol Ultra" actually is.** Ultra is a **product mode**, not an effort
> value — sending `reasoning: {effort: "ultra"}` returns HTTP 400. It's toggled
> in Codex settings (Plus plans and up) and runs ~4 collaborating agents in
> parallel. "Sol Ultra" = `gpt-5.6-sol` with that mode on, not a separate model
> slug. It rides on top of a normal effort level — so `Sol Ultra · effort: high`
> in the output means "Sol, ultra mode, high effort". Ultra is only meaningful
> on Sol; there is no Terra/Luna Ultra.
> ✅ "Run the security scan of 40 different microservices, each one independently,
>    at the same time" — genuinely independent 40 pieces → Sol Ultra.
> ❌ "Break this monolithic codebase into modules" — the pieces are
>    interdependent, a single coherent design decision is needed → plain **Sol**
>    (on the Claude side this example also goes to `opusplan`, see Step 3 — the
>    Codex analogue being "Sol, plain" is consistent: parallelisation is
>    misleading on both sides).

**R floor (same principle as the Claude arm's "R floor (general)"):** if `R=3`,
**Luna is never selected**, the floor is Terra — don't leave simple-but-
irreversible work to the weakest model. `R=3` also adds the human-review note to
the output (below, the single/shared note in Output format).

**Effort ← D**, same logic as the Claude arm: `0→minimal · 1→low · 2→medium ·
3→high`. If `D=3 ∧ R=3` → **`max`** (matches Claude's `max`).

> **`max` is real on Codex.** `openai.com/index/gpt-5-6/` and the GA note
> confirm the GPT-5.6 effort ladder is `none, low, medium, high, xhigh, max`, and
> that `max` "is available to all users with access to GPT-5.6 in ChatGPT Work
> and Codex and can be toggled on in settings". The
> `learn.chatgpt.com/docs/config-file/config-reference` page is stale (still
> lists only up to `xhigh`) — a doc lag, not a real limit. Caveat: some
> third-party gateways / CLI wrappers still block `max` and 400 on it (open
> GitHub issues) — if the user reports a 400, tell them to check their tooling
> or fall back to `xhigh`.
>
> **`mode: pro` — Responses-API only, still not in the Codex CLI.** `reasoning.mode:
> "pro"` (a separate axis from effort, defaults to `medium` effort) is confirmed
> for the Responses API. The Codex CLI config reference has no `model_reasoning_mode`
> key. Mention it only if the user asks, as "API-only, not in the CLI config".

### Fast Mode (1.5x) — the speed line

**Codex CLI has a Fast Mode toggle** (user-reported 2 Sep 2026, see `reference.md`
§9.7 — not independently verified): output streams ~**1.5x** faster and the
subscription quota / API bill burns at that same 1.5x rate. Model, reasoning
depth and answer quality are **unchanged** — it buys latency with quota, nothing
else. Independent of the model and of `reasoning.effort`. The Claude-side
analogue is Claude Code's `/fast` — 2.5x faster output, but it **doubles the
price** and is **Opus 5 / Opus 4.8 only** (`reference.md` §4). Both are
CLI/desktop toggles; neither exists on the web UI.

**The router appends one speed line to every CLI Codex output** whose Codex line
names a real model. It comes in **two forms — the first word says which**, so the
reader can tell a nudge from an FYI:

**1. `recommended`** — when `R ≤ 1` **and** any of: `D ≤ 1` · the Step-1
volume/latency gate fired · the user explicitly asked for speed / said they're in
a hurry. (Short, mechanical or low-stakes work — the 1.5x quota cost is tiny in
absolute terms and you're not going to be poring over the output anyway.)
```
⚡ Fast Mode recommended: Codex Fast Mode (1.5x faster, 1.5x quota) — low-risk / mechanical work.
```

**2. `available`** — every other case (`D ≥ 2`, `R ≥ 2`, deep reasoning you'll
want to read carefully, or big token counts where 1.5x is a real quota hit).
```
⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota).
```
If the Claude line is `Opus 5` or `Opus 4.8`, append the Claude half — **only to
the `available` form**, never `recommended` (`/fast` doubles the price, so it's
never a nudge):
```
⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota) · Claude /fast (2.5x faster, 2× price).
```
(The `recommended` form never needs a Claude half: it requires `D ≤ 1`, and the
Claude line is only Opus at `D = 3`.)

- **No speed line** when the Codex line is "unverified — use Claude" (the feature
  is Codex-anchored), or when the user is explicitly on a web surface.
- Ordering: the `opusplan` warning stays directly under the Claude line; the
  speed line sits just **above** the `R=3` human-review note.

This is the **third** always-added Output-format exception (below). Even the
`recommended` form is a suggestion the user can ignore — the router never toggles
anything itself.

### Human-review note on Codex

`R=3` → exactly the same logic as Step 4 Rule 1: model/effort unchanged, a
human-review note is added to the output (mandatory exception, see Output
format). The MCP/auto-accept warnings (Step 4 Rule 6/7) may also apply to the
Codex CLI, but Codex's own tool-schema/session-cost mechanics **were not
verified** — I don't carry those two rules into the Codex arm, they apply only
in the Claude arm.

### `mode: pro` — Responses-API only, optional suggestion (NOT added to output)

If `max(D,C)=3` stayed on Terra (D<3 but the result is critical),
`reasoning.mode: "pro"` (Responses API) can be tried — it's a separate axis from
effort and defaults to `medium` effort. It's not in the Codex CLI config
reference, so it doesn't go in the default output; if the user asks "what else
can I do?", suggest it as "API-only, try it, fall back to standard mode if it
doesn't work" (same caution level as the Claude arm's `opusplan`+`ultracode`
advanced-combination note).

---

## Output format

**Two lines, always both — Claude and Codex.** Rationale, score, escalation note
— none are written. Compute R/D/W/C once (in your head, without writing it out),
read two tables, write the results:

```
Claude: <Model> · effort: <level>
Codex: <Model> · effort: <level>
```

Write no effort for Haiku 4.5; on the Codex side **every model takes an effort**
(including Luna — there's no verified info excluding Luna's effort support):

```
Claude: Haiku 4.5
Codex: Luna · effort: minimal
```

**On offensive-security / biology-adjacent prompts the Codex line recommends no
model:**

```
Claude: Opus 4.8 · effort: ultracode
Codex: unverified — use Claude
```

**Exceptions to this rule — only these three, always added to the output (BELOW
the two lines, as their own separate line(s); nothing else that appears as a
"note/warning/suggestion" in the rest of this text is added automatically):**
1. `R=3` → human-review note — **one line, covers both sides** (task risk
   doesn't change by ecosystem, don't repeat it). Goes **last**.
2. `opusplan` (can only be on the Claude line) → the effort-does-not-carry-over
   warning, directly under the Claude line.
3. **Speed line** (see Codex arm → "Fast Mode (1.5x)") — one of:
   - `⚡ Fast Mode recommended: Codex Fast Mode (1.5x faster, 1.5x quota) — low-risk / mechanical work.`
     when `R≤1` ∧ (`D≤1` ∨ Step-1 volume gate ∨ explicit hurry).
   - `⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota)[ · Claude /fast (2.5x faster, 2× price)].`
     otherwise; the Claude half only when the Claude line is `Opus 5`/`Opus 4.8`.

   Added to every CLI Codex output whose Codex line names a real model. Omitted on
   a web surface and on a "unverified — use Claude" Codex line. Sits just above the
   `R=3` note.

Everything else — the notes in Step 4 Rules 2–8, `opusplan`'s "advanced
combination" paragraph, Codex's `mode: pro` note, escalation conditions — is
explained **only when the user asks**, not added to the default output.

If the user asks for the rationale (*"why?"*, *"why this?"*) then explain — but
don't add it unprompted, and even then keep it short.

### Examples

Input: *"Label these 200 customer reviews as positive/negative"*
```
Claude: Haiku 4.5
Codex: Luna · effort: minimal
⚡ Fast Mode recommended: Codex Fast Mode (1.5x faster, 1.5x quota) — low-risk / mechanical work.
```
(Volume gate fired ∧ R≤1 → `recommended`.)

Input: *"Understand the repo's auth flow and move it to OAuth2"*
```
Claude: Sonnet 5 · effort: high
Codex: Terra · effort: low
⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota).
```
(D=2 → `available`, not a nudge — you'll want to read this output.)
(Same D=1 input, two different numeric effort words — the Claude scale `low→max`
looks like it starts at `medium` for D=1 but here D=2 gives `high`; the Codex
scale `minimal→max` starts from a lower rung. The two scales don't convert to
each other, don't mix them.)

Input: *"Find the race condition that flakes in prod sometimes"*
```
Claude: Opus 5 · effort: max
Codex: Sol · effort: max
⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota) · Claude /fast (2.5x faster, 2× price).
Do not apply without human review.
```
(R=3 → `available`, not `recommended`. Claude line is Opus 5 → the Claude half is
included; speed line sits above the human-review note.)

Input: *"Run a penetration test against this 180-service environment, build auth-bypass chains"*
```
Claude: Opus 4.8 · effort: ultracode
Codex: unverified — use Claude
```
(A penetration test = offensive hard gate. But **"audit these 180 services'
code for auth-bypass vulnerabilities"** is defensive work — the gate does not
fire, it goes to normal scoring: adversarial vuln hunting = D=3, 180 services
= W=3 and independent, R=1 → `Claude: Sonnet 5 · effort: ultracode` /
`Codex: Sol Ultra · effort: high`. Shrink the scope to one service and it's
`Claude: Sonnet 5 · effort: xhigh` / `Codex: Sol · effort: high`.)

Input: *"Audit this genomics pipeline's variant-calling logic"*
```
Claude: Fable 5.1 · effort: high
Codex: unverified — use Claude
```

Input: *"Bump `MAX_RETRIES` from 3 to 5 in the prod config"*
```
Claude: Sonnet 5 · effort: low
Codex: Terra · effort: minimal
⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota).
Do not apply without human review.
```
(D=0 but R=3 → `available`, not `recommended` — don't nudge speed on an
irreversible prod change.)
(R=3 but D=0 — on the Claude side the model doesn't drop to Haiku, it finds the
floor at Sonnet; on the Codex side there's no such floor rule because Luna
already takes an effort, D=0 drops straight to Luna... but because of R=3 the
Codex side also stays on Terra instead of Luna, the same "R=3 is not left to the
weakest model" principle.)

Input: *"Redesign the auth architecture of 200 prod services from scratch"*
```
Claude: opusplan · plan: max · execute: medium
⚠️ Effort does not carry over — after switching to execution mode set it manually with /effort medium.
Codex: Sol · effort: max
⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota).
Do not apply without human review.
```
(`opusplan` is Claude-only; the Codex side comes out plain Sol from its own
normal mapping — D=3 ∧ R=3 → `max`. `available` (R=3); no Claude half — `opusplan`
is not a plain Opus line. The two sides can use different mechanisms, that's
normal.)

Input: *"Run the security scan of 40 completely independent microservices at once, each on its own"*
```
Claude: Sonnet 5 · effort: ultracode
Codex: Sol Ultra · effort: high
⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota).
```
(Genuinely independent-parallel work — `ultracode` fires on the Claude side, Sol
Ultra on the Codex side; each uses its own parallelism mechanism. D=3 → `available`,
not `recommended`; and on Sol Ultra the "1.5x quota" is 1.5x of ~4 parallel
agents — expensive, so definitely the user's call.)

---

## If detail is needed

For benchmark tables, pricing, subscription plans and source-data-quality notes,
read `reference.md`. If the user asks "why this model?", "what are the numbers?",
look there — especially **§2.1** (LiveBench / BenchAlign / AA Index, 2 Sep 2026),
**§0.1** (Fable 5.1 / Mythos 5.1) and **§9.7** (Codex Fast Mode / the speed line).

**The router does not select a model from a benchmark number.** Leaderboards
confirm the *direction* of Rules 2/3; scoring runs on R/D/W/C, not on an
aggregate score (BenchAlign shows Sonnet 5 low as a coverage artefact — see §2.1).
