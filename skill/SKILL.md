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
Codex/ChatGPT**, which model and effort level to run it on — both together, in
one output. Do **not** run the prompt — only route it. The user decides which
recommendation to use; this router starts nothing automatically.

**Calibration: two separate subscription quotas.** The protected resource is
Claude's 5-hour window **and** ChatGPT Plus's 3-hour + weekly windows — not
dollars. The real danger isn't picking a model that's too weak; it's
*reflexively picking the most expensive model and burning the quota.* When in
doubt, round **down**.

**How to run this — keep it cheap.** Compute R/D/W/C **once**, in your head
(don't write the steps out), then read two short tables. Produce only the final
two lines. Show intermediate reasoning only if the user asks "why?".

> **Fast path.** If Step 0 raises nothing **and** no Step 1 gate fires, score the
> four axes in one pass and emit — do not re-derive or second-guess. Most prompts
> are this case. Open `reference.md` only when a specific score is genuinely
> ambiguous after one read (§10 has the edge-case rulings; §8 the example
> library).

**Claude model roster (as of 1 September 2026):**

| Model | Role |
|---|---|
| Haiku 4.5 | Speed/volume specialist. No effort parameter |
| Sonnet 5 | Daily work — speed+intelligence balance. **Default starting point** |
| **Opus 5** | **Flagship.** Complex agentic code and enterprise work. Replaced Opus 4.8 |
| Opus 4.8 | Legacy — the **only** lasting role is the offensive-security gate |
| **Fable 5.1** | Frontier scale: long-horizon autonomy, extreme breadth, **biology-adjacent R&D**. $10/$50, cache reads ¼ ($0.25/MTok); cutoff Jun 2026 |
| Mythos 5.1 | **Same model** as Fable 5.1 with permissive safeguards — **Project Glasswing invite only**. Recommend only if the user states they have this access |

> **Fable 5.1 vs Opus 5 — Anthropic's framing:** "Start with Opus 5 for most
> work; if Opus 5 at `xhigh`/`max` still falls short on demanding reasoning or
> long-horizon agentic work, move to Fable 5.1." This router already recommends
> Fable 5.1 only at the frontier-scale and biology gates — consistent, no extra
> rule needed.

**Codex/ChatGPT roster (GPT-5.6 family, as of 9 July 2026):**

| Model | Role | Claude analogue (rough) |
|---|---|---|
| Luna | Speed/volume specialist, cheapest tier | Haiku 4.5 |
| Terra | Daily work, balanced — **default starting point** | Sonnet 5 |
| **Sol** | **Flagship** — code/science/security | Opus 5 |
| **Sol Ultra** | A Codex *mode* toggled on Sol (Plus+): ~4 collaborating agents in parallel. Not a separate model; `effort:"ultra"` → HTTP 400 | stronger parallelism primitive than `ultracode` |

> Fable 5.1 (frontier scale + biology-adjacent) has **no** verified Codex
> analogue. For offensive-security and biology-R&D prompts the Codex line says
> "unverified — use Claude" and recommends no model.
>
> Source note: roster + effort ladder re-verified against
> `developers.openai.com/api/docs/guides/latest-model` + `learn.chatgpt.com/docs/models`
> (3 Sep 2026): ladder is `none, low, medium, high, xhigh, max`; `medium` is the
> coding default, `low` is for quick/well-scoped/latency-sensitive work only.
> Full notes + benchmark direction in `reference.md` §9.

---

## Effort levels (Claude Code `/effort` menu)

| Level | What it does |
|---|---|
| `low` | Short, well-scoped work that needs no intelligence |
| `medium` | Cost-sensitive work; gives up some intelligence |
| `high` | **Default** (every model that supports effort) |
| `xhigh` | Deeper reasoning. 30 min+ agentic/coding work |
| `max` | Deepest reasoning. Over-thinking risk. Per-session |
| `ultracode` | `xhigh` + **dynamic workflow orchestration**. Per-session, Claude Code setting |

1. **`ultracode` is a Claude Code setting, not a model effort level.** It sends
   `xhigh` to the model and adds workflow orchestration. No model restriction —
   works on every model that supports `xhigh` (Fable 5.1, Sonnet 5, Opus 5, Opus
   4.8). Not Haiku.
2. **Haiku 4.5 does not support the effort parameter.** Recommend Haiku → write
   no effort.
3. Effort is a behavioural signal, not a token budget. "low = 1,024 tokens"
   figures are made up.
4. **Both arms use the same `D → effort` table** (Step 3). Codex's ladder is
   `none, low, medium, high, xhigh, max` (no `minimal` any more); OpenAI's own
   guidance puts `medium` as the coding default and `low` as "quick,
   well-scoped, latency-sensitive" only — which lines up rung-for-rung with the
   Claude scale. The only arm-specific effort-field values are `ultracode`
   (Claude) and `Sol Ultra` (Codex).

---

## Step 0 — Prompt quality gate

**Do not skip.** Before scoring, run these four checks. "Is there a success
criterion / scope?" as a single question is not enough — most real prompts
contain scope but carry an unnoticed ambiguity. If any check is "yes",
**recommend no model** — clarify first, concretely (name what's missing, don't
just say "it's unclear").

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
guesses the context, guesses wrong, the work is redone. Worse if it produces
silently-wrong code as in (2). Counter-example (do **not** block): "Add a
`deleted_at` column and implement soft-delete instead of `DELETE`" — rule
complete, one interpretation, concrete scope → go straight to scoring.

---

## Step 1 — Hard gates (Claude side)

Two kinds of gate:

- **Deciding gate** (rows 1–3, 5): fixes **which model**, bypasses Step 2/3
  model selection. Does **not** bypass the W/duration check — `ultracode`
  eligibility is still evaluated after the gate fires.
- **Eliminating gate** (row 4): removes one candidate (Haiku), Step 2/3 scoring
  runs normally among the rest.

| Condition | Kind | Result |
|---|---|---|
| Sub-second latency **or** high-volume classification/parsing | Deciding | **Haiku 4.5.** No effort. Stop |
| **Offensive security:** exploit generation, penetration testing, binary-based vulnerability scanning | Deciding | **Opus 4.8**, effort floor `xhigh` (W/duration can still raise it to `ultracode`) — with Glasswing access, **Mythos 5.1** |
| **Biology-adjacent R&D:** genomics, protein/chemistry-heavy pipeline, bio-CTF | Deciding | **Fable 5.1** (default effort `high`, no floor) |
| Context exceeds 200k tokens | **Eliminating** | **Haiku 4.5 removed**, Step 2/3 runs with the rest |
| **1000+ files / whole-codebase scale** | Deciding | **Fable 5.1** |

> **Defensive security work does not trigger the offensive gate — at any scale.**
> "Audit this code/infra for vulnerabilities", "find open ports", "review the
> security-group rules", "audit 180 services for auth-bypass bugs (no exploits)"
> — defensive, goes to normal scoring. Only the three offensive categories above
> gate. (Fable 5.1 does defensive vuln discovery itself as of 1 Sep 2026.)
>
> **Frontier-scale gate — one signal is enough:** just the file/scope count
> (1000+). "Concurrent 1M context" / "persistent memory" need not be stated
> separately. 100–999 files does **not** gate — normal scoring (`W=3`).
>
> Why offensive → Opus 4.8, why biology → Fable 5.1 (not Opus 5), and the
> `ultracode`-above-floor mechanics: `reference.md` §10.1.

---

## Step 2 — Score on four axes, 0–3

For each axis **ask the diagnostic first**, then place the level. If unsure,
find the closest analogue in `reference.md` §8. **When in doubt, round down**
(quota-aware default — a "more than a one-liner" feeling is not grounds to go up
a level).

### R — Risk / irreversibility

*Diagnostic: if the output is wrong, minutes or days to fix? Automatic rollback
(git revert, feature flag)? How many users/systems affected? Money/health/legal?*

`0` Throwaway draft — no loss even if unused
`1` Used but a human reviews and approves (PR, draft email)
`2` Goes to a real system but reversible (feature-flagged deploy, reversible migration, isolated operational value)
`3` No way back / disproportionately costly — data-loss risk, irreversible migration, outbound message/payment, central shared-core architectural decision, medical/legal/financial advice, live user data

> **First separate: a codebase change, or a live/operational value?** A normal
> source-code change (colour, text, any source line) is **R=1 by default** — the
> normal flow is PR review + deploy. R=2/R=3 only kick in if the prompt
> explicitly points at a value that goes live **without** code review — prod
> config file, live admin panel, feature-flag toggle, DB setting. Vague
> phrasings ("change the settings page default theme") are assumed to be
> codebase changes → R=1.
> - **"Architectural decision" alone ≠ R=3.** If it can roll out
>   service-by-service / feature-flagged and be rewound → **R=2** even if
>   architectural (e.g. "migrate 40 services to a shared auth middleware" — each
>   uses its own middleware independently). R=3 only when (a) no real rollback
>   (live schema migration), or (b) a **central/shared** core the whole system
>   depends on (identity/auth infra, data model, trust boundary).
> - **Decompose → module or service?** "Break the monolith into **modules**" =
>   internal refactor, reversible (strangler-fig) → **R=2**. "Split into separate
>   **services/processes**" = network + data-ownership + deploy boundaries,
>   re-merging is disproportionately expensive → **R=3**.
> - **"One-line config" alone ≠ R=2.** The question is blast radius, not line
>   length. Isolated operational value (one feature-flag default) → R=2. A line
>   governing **system-wide** behaviour (retry count, timeout, rate limit,
>   pool size) where a wrong value causes a gradual outage before anyone notices
>   → **R=3** even as one line (e.g. "bump `MAX_RETRIES` 3→5 in the prod config").
>
> Worked ✅/❌ pairs: `reference.md` §10.2.

### D — Depth

*Diagnostic: known/standard pattern, or thought out from scratch? How many
approaches is a choice being made between? Solved by trial-and-error, or by
getting the design right in one pass?*

| Level | Coding | Writing/analysis | Research | Data |
|---|---|---|---|---|
| `0` | Pattern match, known constant; **fully-specified additive schema change** (name + type + nullable all given, no design decision) | One-sentence answer **or** pure form/tone change with no content change (length irrelevant) | Single-source lookup | Reading a single number |
| `1` | Standard pattern (CRUD, known bug shape); schema change with a choice (index type, backfill) | Simple summary/draft | Single-source summary | Simple filter/aggregation |
| `2` | Multi-step but well-documented feature | Multi-source synthesis report | Multi-source synthesis | Statistical inference |
| `3` | Design from scratch, concurrency, algorithmic complexity, conflicting constraints; **adversarial security-vulnerability hunting** (subtle logic errors) | Original argument, reconciling conflicting sources | New hypothesis/framework | Modelling, causal inference |

> - **D=1 / D=2 boundary — "well-documented" alone ≠ D=2.** The question is how
>   many **independent design decisions** are left to the implementer. One
>   reasonable approach, following a recipe/library → **D=1** (e.g. "add
>   cursor-based pagination to this API"). A real choice between >1 approach that
>   affects the outcome → D=2.
> - **Mechanical enumeration = D=1**, not D=3 — "list which security-group rules
>   allow 0.0.0.0/0 on ports other than 80/443" is a fixed-condition scan. An
>   open-ended "review this for security holes" is the D=3 adversarial case.
> - **Adversarial vuln hunting = D=3** (subtle logic errors — same as a race
>   condition hunt or reconciling conflicting contract clauses). A large
>   defensive audit is still D=3 on depth even though it doesn't gate.
>
> Worked pairs: `reference.md` §10.3.

### W — Width

*Diagnostic: how many files/documents read or changed? Independent
(parallelisable) or sequential?*

`0` Single file/document
`1` 2–5 files, one module
`2` **6–99 files/units** (incl. the same small change repeated across many services) **or** 2–3 verification angles
`3` **100+ files** / whole codebase **or** 3+ independent, parallelisable verification angles

> **The W=2 / W=3 threshold is numeric — 100.** "Add the same endpoint to 60
> microservices" → **W=2** (60 < 100), not W=3. `ultracode` requires W=3, so
> repetitive mechanical work over 20–99 units does **not** rise to `ultracode`
> (effort follows D). "Unaware of each other" phrasing doesn't change the count.

### C — Context synthesis

*Diagnostic: fine with its own knowledge, or how much to read from outside?*

`0` Self-sufficient
`1` A few small files/documents
`2` A medium codebase/documentation (one README + a few modules)
`3` A large corpus (hundreds of pages, a huge codebase, a long chat history)

---

## Step 3 — Mapping

Model selection is by **intelligence need** (D, C) — risk (R) does not raise the
model, it raises human oversight (a review note + the effort floor).

**Model** ← `max(D, C)`. **Opus 5 is a candidate only when `D=3`** — `C=3` alone
(large but shallow synthesis) stays on Sonnet 5 (its 1M window handles it).

| Condition | Model |
|---|---|
| `D = 0` **∧** `W=0` **∧** `C≤1` **∧** `R≤1` | **Haiku 4.5** |
| Above not met, `max(D,C) ≤ 1` | Sonnet 5 |
| `max(D,C) = 2` | Sonnet 5 |
| `max(D,C) = 3`, `D<3` (C triggered it) | **Sonnet 5** — large context, shallow reasoning |
| `max(D,C) = 3`, `D=3` | **Opus 5** if the task is Rule 2 territory (agentic multi-step code / math-proof / tool-less deep reasoning). **Otherwise Sonnet 5** (quota-aware default) |

- **Haiku only at D=0.** D=1 = "known pattern" (N+1 fix, standard validation) —
  needs real judgement, floor is Sonnet 5.
- **R floor:** `R=3` → Haiku never selected, floor Sonnet 5; also adds a
  human-review note (Step 4 Rule 1).

**Effort** ← `D`, **independent of the model** — always by this table:

| D | Effort |
|---|---|
| 0 | `low` |
| 1 | `medium` |
| 2 | `high` |
| 3 | `xhigh` |
| 3 ∧ R=3 | `max` |

Haiku 4.5 selected → leave the effort field blank.

**`ultracode`** ⇔ all three: `W = 3` **∧** estimated duration > 30 min **∧**
`¬(D=3 ∧ R=3)`. Write `ultracode` in the effort field (not `xhigh`). No model
restriction except Haiku; rides on whichever model was chosen (by Step 3 scoring
**or** a Step 1 deciding gate).

> **Conflict:** `D=3 ∧ R=3` → effort `max`, `ultracode` **no** (`ultracode` only
> sends `xhigh`; you'd lose `max`'s depth, and spreading irreversible work across
> parallel workflows hurts oversight). Depth wins → `max`.

### `opusplan` — plan/execute model split

**Claude Code only** (`/model opusplan`): Opus 5 in plan mode, auto-switches to
Sonnet 5 for execution. **Overrides the Opus 5 branch** when all three hold:

1. `max(D,C)=3 ∧ D=3` **∧** Rule 2(a) territory (structured design/architecture).
2. **Difficulty front-loaded into the plan** — once the plan is done, execution
   steps follow a repeating pattern. Opposite (do **not** use opusplan):
   debugging, formal proof, new-algorithm design — difficulty persists through
   execution.
   > The execution verb may be unstated — a **concrete target-scope number**
   > ("design the auth architecture for 200 services") implies the execution
   > phase exists. "Design" alone doesn't override front-loading.
3. `W ≥ 2` — enough implementation volume to pay off the mode switch.

Output (under the `Claude:` label; Codex line unaffected — its own mapping):
```
Claude: opusplan · plan: <effort> · execute: <effort>
⚠️ Effort does not carry over — after switching to execution mode set it manually with /effort <execute effort>.
```
Plan effort = Rule 2(a)'s result (`xhigh`, or `max` if `R=3`). Execute effort =
the post-plan estimated D (usually `medium`). **The ⚠️ warning is mandatory on
every `opusplan` output** (one of the three always-added exceptions).

> opusplan diagnostic table + the "advanced combination" (ultracode on the
> execution phase, on-ask only): `reference.md` §10.4.

---

## Step 4 — Quota-protection and accuracy rules

Terse list; rationale in `reference.md` §10.5. Only Rule 1's note is auto-added
to output — the rest is explained **only if the user asks**.

1. **R=3 → human-review note** ("Do not apply without human review."). Model/
   effort unchanged. For simple-but-risky work (D≤1) this note alone is enough.
2. **Prefer Opus 5 in three areas (Rule 2):** (a) agentic multi-step
   **structured** work — architecture from scratch, large refactor/migration,
   also non-code (rule-engine / decision-tree / prompt architecture) with a real
   D=3 design decision; (b) mathematics / formal proof; (c) tool-less deep
   reasoning (deep analysis from prompt content alone, **no** tool calls). Tool
   access flips (c) toward Sonnet 5 — most Claude Code work is "tooled", so (c)
   rarely fires; (a) and (b) are the frequent ones.
3. **D=3 outside Rule 2 → default Sonnet 5 · xhigh** (quota). LiveBench
   2026-06-25 has Opus 5 ahead (agentic +5.8, language +13.7, reasoning +2.5) —
   so **escalate to Opus 5 · xhigh if the result is insufficient or the work is
   critical**, especially language/reasoning-heavy D=3.
4. **User knowledge (not a router output change):** low/medium on Opus 5 is not
   "waste" — Anthropic's Opus 5 advice treats it as a normal cost dial. The
   router still never emits Opus 5 below `xhigh` (it only picks Opus 5 at D=3).
5. **No `ultracode` for work under 30 min.** For one-off depth, write
   `ultrathink` into the prompt instead (doesn't change the effort level).
6. **Long-session / MCP warning:** each MCP server injects tool schemas into
   every message, proportional to tool count (GitHub MCP 27 tools ≈ 18k tokens).
   Turn off unused ones.
7. **Auto-accept warning:** if R≥2, suggest turning auto-accept off — chained
   edits burn quota geometrically and make rollback harder.
8. **Alias safety:** `/model opus` → Opus 5 on Claude Code v2.1.219+; older
   versions may fall to Opus 4.8. Suggest `claude update` or `/model claude-opus-5`.

---

## Codex arm

Compute **in parallel** with the Claude arm — both are always produced. R/D/W/C
scoring is **exactly** Step 2; compute once, read this table.

### Codex hard gates

| Condition | Result |
|---|---|
| Sub-second latency / high-volume classification | **Luna**, effort `low` |
| **Offensive security / biology-adjacent R&D** (same definitions as Step 1) | **"unverified — use Claude"**, no model. (Codex's safety-classifier/fallback behaviour here was not researched — left blank rather than guessed.) |
| Very large context | No threshold — per-model context windows unverified. Normal mapping by C. |

### Codex mapping (R/D/W/C → Model)

| Condition | Model |
|---|---|
| `D=0 ∧ W=0 ∧ C≤1 ∧ R≤1` | **Luna** |
| Otherwise `max(D,C)≤1` | Terra |
| `max(D,C)=2` | Terra |
| `max(D,C)=3`, `D<3` (C triggered it) | Terra |
| `max(D,C)=3`, `D=3` | **Sol** — or **Sol Ultra** if the work splits into **3+ genuinely independent** pieces (module/service/verification angle) that run unaware of each other and merge at the end |

- **Effort ← D — the same table as Step 3:** `0→low · 1→medium · 2→high ·
  3→xhigh`; `D=3 ∧ R=3 → max`. This is OpenAI's own guidance (`medium` = coding
  default, `low` = quick/well-scoped/latency-sensitive only), not a parallel to
  the Claude scale — but it now matches it rung-for-rung. `Terra · low` is a
  **D=0** answer only (rename, tone-only rewrite, fully-specified schema change).
  Real D=1 dev work ("add email validation", "add cursor-based pagination") is
  `Terra · medium`.
- **Don't round D up.** If you're always landing on `Sol · xhigh` / `Terra ·
  high`, that's the D=1→D=2 / D=0→D=1 bug — the quota-aware default is to round
  **down** a level, not up.
- **R floor:** `R=3` → Luna never selected, floor Terra. Adds the human-review note.
- `max` is a real Codex setting toggle on every GPT-5.6 tier (re-verified 3 Sep
  2026).

> "What Sol Ultra actually is", `mode: pro` (Responses-API-only, on-ask), and the
> Codex-side notes: `reference.md` §10.6.

### Fast Mode (1.5x) — the speed line

Codex CLI has a Fast Mode toggle (user-reported 2 Sep 2026, not independently
verified — `reference.md` §9.7): output ~**1.5x** faster, quota/bill burns 1.5x,
model + reasoning + quality unchanged. Claude analogue: `/fast` — 2.5x faster,
**2× price**, **Opus 5 / Opus 4.8 only**. Both CLI/desktop toggles, not web.

**Append one speed line to every CLI Codex output whose Codex line names a real
model.** Two forms — the first word says which:

- **`recommended`** — when `R ≤ 1` **and** any of: `D ≤ 1` · the Step-1
  volume/latency gate fired · the user explicitly asked for speed.
  ```
  ⚡ Fast Mode recommended: Codex Fast Mode (1.5x faster, 1.5x quota) — low-risk / mechanical work.
  ```
- **`available`** — every other case.
  ```
  ⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota).
  ```
  If the Claude line is `Opus 5` / `Opus 4.8`, append the Claude half **to the
  `available` form only** (never `recommended` — `/fast` doubles the price):
  ```
  ⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota) · Claude /fast (2.5x faster, 2× price).
  ```

**No speed line** when the Codex line is "unverified — use Claude", or on a web
surface. Ordering: `opusplan` warning directly under the Claude line; speed line
just **above** the `R=3` human-review note.

### Human-review note on Codex

`R=3` → same as Step 4 Rule 1: model/effort unchanged, one shared human-review
note (task risk doesn't change by ecosystem — don't repeat it per side). The
MCP/auto-accept warnings (Rules 6/7) are **not** carried into the Codex arm —
Codex's tool-schema/session-cost mechanics were not verified.

---

## Output format

**Two lines, always both.** No rationale, score, or escalation note.

```
Claude: <Model> · effort: <level>
Codex: <Model> · effort: <level>
```

No effort for Haiku 4.5; on the Codex side every model takes an effort (Luna
included):

```
Claude: Haiku 4.5
Codex: Luna · effort: low
```

Offensive-security / biology-adjacent → Codex recommends no model:

```
Claude: Opus 4.8 · effort: ultracode
Codex: unverified — use Claude
```

**The only three things auto-added to output** (below the two lines, each on its
own line; nothing else from this document is added unprompted):

1. `R=3` → **`Do not apply without human review.`** — one line, covers both
   sides. Goes **last**.
2. `opusplan` (Claude line only) → the `⚠️ Effort does not carry over` warning,
   directly under the Claude line.
3. **Speed line** (see Codex arm → Fast Mode) — `recommended` or `available`
   form. Every CLI Codex output with a real Codex model; omitted on web and on
   "unverified". Sits just above the `R=3` note.

If the user asks "why?", explain briefly — but never add it unprompted.

### Examples

*"Label these 200 customer reviews as positive/negative"*
```
Claude: Haiku 4.5
Codex: Luna · effort: low
⚡ Fast Mode recommended: Codex Fast Mode (1.5x faster, 1.5x quota) — low-risk / mechanical work.
```

*"Understand the repo's auth flow and move it to OAuth2"*  (D=2)
```
Claude: Sonnet 5 · effort: high
Codex: Terra · effort: high
⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota).
```

*"Find the race condition that flakes in prod sometimes"*  (D=3, R=3, difficulty persists → plain Opus 5)
```
Claude: Opus 5 · effort: max
Codex: Sol · effort: max
⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota) · Claude /fast (2.5x faster, 2× price).
Do not apply without human review.
```

*"Run a penetration test against this 180-service environment, build auth-bypass chains"*  (offensive gate; W=3 → ultracode)
```
Claude: Opus 4.8 · effort: ultracode
Codex: unverified — use Claude
```
> But *"audit these 180 services' code for auth-bypass vulnerabilities (no
> exploits)"* is **defensive** — no gate, normal scoring: D=3 (adversarial),
> W=3 + independent, R=1 → `Claude: Sonnet 5 · effort: ultracode` /
> `Codex: Sol Ultra · effort: xhigh`. One service → `Sonnet 5 · xhigh` /
> `Sol · xhigh`.

*"Redesign the auth architecture of 200 prod services from scratch"*  (opusplan)
```
Claude: opusplan · plan: max · execute: medium
⚠️ Effort does not carry over — after switching to execution mode set it manually with /effort medium.
Codex: Sol · effort: max
⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota).
Do not apply without human review.
```

*"Bump `MAX_RETRIES` from 3 to 5 in the prod config"*  (D=0 but R=3 → not `recommended`)
```
Claude: Sonnet 5 · effort: low
Codex: Terra · effort: low
⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota).
Do not apply without human review.
```

---

## If detail is needed

`reference.md`: **§10** routing rubric edge-cases & rationale (the material moved
out of this file) · **§8** example library (score by analogy) · **§2.1**
LiveBench / BenchAlign / AA Index · **§0.1** Fable 5.1 / Mythos 5.1 · **§9.7**
Codex Fast Mode.

**The router never selects a model from a benchmark number.** Leaderboards
confirm the *direction* of Rules 2/3; scoring runs on R/D/W/C.
