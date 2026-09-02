# Reference tables

> **Primary source:** `platform.claude.com/docs/en/about-claude/models/overview`,
> `platform.claude.com/docs/en/build-with-claude/effort`,
> `platform.claude.com/docs/en/about-claude/pricing`,
> `code.claude.com/docs/en/model-config` — verified directly (after the 24 July
> 2026 Opus 5 launch).
>
> **Secondary source:** "Source-disciplined technical analysis of Claude models"
> (10 July 2026, pre-Opus 5). `[K1]` = Anthropic official doc/system card, `[K2]`
> = independent evaluator, `[K3]` = content site/forum. **The Opus 4.8 data in
> that report is not inherited by Opus 5** — a separate model, a separate
> benchmark profile.
>
> This file is read only when needed — `SKILL.md` is sufficient on its own.

---

## 0. Opus 5 — 24 July 2026 launch

Opus 5 (`claude-opus-5`) is the flagship that replaced Opus 4.8. Anthropic's own
advice: *"If you're not sure, start with Opus 5."* Opus 4.8 is now in the
"legacy" category — still working but Anthropic is actively recommending the move
to Opus 5.

**Price unchanged:** $5/$25 (input/output MTok) — same as Opus 4.8.

**Published benchmark claims** (Anthropic's own launch note):
- Frontier-Bench v0.1: **more than 2x** Opus 4.8, at lower cost
- CursorBench 3.2: within **0.5%** of Fable 5's peak score at `max` effort, at half the price
- ARC-AGI-3: **3x** the nearest competitor
- Zapier AutomationBench: **~1.5x** the nearest competitor at equal cost
- OSWorld 2.0: best at every cost point; beats Fable 5's best result at **less than a third** of the cost
- Life sciences (internal benchmark): **+10.2 points** over Opus 4.8 on organic chemistry, **+7.7 points** on protein tasks

⚠️ **What was NOT published:** SWE-bench Pro, Terminal-Bench 2.1, HLE
(tooled/tool-less), USAMO — the actual benchmarks Rules 2/3 rest on. So how far
ahead of Sonnet 5 Opus 5 is **on those specific tests** is unknown. The overall
jump above is a strong direction indicator but **not a number**.

### Safety classifier / fallback chain (updated with Fable 5.1)

| Model | If offensive-security flagged | If biology-R&D flagged |
|---|---|---|
| Fable 5.1 | → **Opus 4.8 or Opus 5** (permitted fallback targets) | → **Opus models** |
| Opus 5 | → **Opus 4.8** | → **Refuse** (no fallback) |
| Fable 5 (legacy) | → **Opus 4.8** | → **Opus 5** |

This table is the source of the two separate gates in `SKILL.md` Step 1.

**What changed with Fable 5.1 (1 Sep 2026 announcement + `platform.claude.com`
verification):**
- **Defensive vulnerability discovery is now permitted** — Fable 5.1 "can
  discover software vulnerabilities, but cannot develop exploits for them". Only
  **penetration testing, exploit generation, binary-based vulnerability
  scanning** redirect to Opus models.
- On benign requests, cyber interventions dropped **~60%**, and on basic
  biology-medical questions **~85%**.
- **Mythos 5.1** (`claude-mythos-5-1`): same model as Fable 5.1 with permissive
  safeguards. **Project Glasswing invite only** (Cyber Verification Program /
  Life Sciences Verification Program; US-first). Normal API / Claude Code access
  does not route to it automatically — a separate, invite-only model.
- Fable 5.1's permitted fallback targets are listed in the official docs as
  **"Opus 4.8 and Opus 5"**; the router continues to pick Opus 4.8 at the
  offensive gate (most permissive general model on cyber posture).

### Claude Code version requirement

`Opus 5: v2.1.219+ · Sonnet 5: v2.1.197+ · Opus 4.8: v2.1.154+`

The `/model opus` alias resolved to Opus 4.8 (or Opus 4.7 on even older versions)
before v2.1.219. If the user is on an old version, `claude update` is needed.

---

## 0.1. Fable 5.1 / Mythos 5.1 — 1 September 2026 launch

Fable 5.1 (`claude-fable-5-1`) is the frontier model that replaced Fable 5.
Anthropic's framing: *"Most work starts with Opus 5; after trying Opus 5 at
`xhigh`/`max` effort, if it still falls short on demanding reasoning or
long-horizon agentic work, move to Fable 5.1."* In the model-selection matrix
Fable 5.1 = "the highest available capability" (agent sessions that run for
hours, multi-step deep research).

**Specs (Fable 5.1 = Mythos 5.1):**
- Context 1M (default and max) · Max output 128k
- Price: $10 / $50 MTok (**same** as Fable 5) — but **cache reads $0.25/MTok**
  (0.025x of base input; 0.1x on every other model). Long agentic sessions that
  re-read a cached prefix pay **¼** of the Fable 5 rate.
- Cache writes: 5m $12.50 · 1h $20 · minimum cacheable prompt **512 tokens**
- Effort: `low`–`max`, default **`high`** (Claude Code); **`medium`** (claude.ai
  and Cowork). The gain over Fable 5 is widest at high effort.
- Adaptive thinking always on. Knowledge cutoff **Jun 2026** (Fable 5: Jan 2026).
- Same tokenizer as Fable 5 (the Opus 4.7 tokenizer).

**Published benchmark claims (Anthropic launch note, Fable 5.1 vs Fable 5):**
- Terminal-Bench-Science: 52.6% vs 24.7% (more than 2x)
- Terminal-Bench 4.0: 55.8% vs 42.0%
- CursorBench 3.2.0: 73.4% vs 70.5%
- Vs Opus 5: "generally superior across most benchmarks tested", "far more
  efficient per token than Opus 5" — the router takes this as a direction
  indicator because the granular numbers are thin, not as a firm superiority
  claim.

**Behaviour differences (visible without a code change — quota-relevant):**
- **Parallel tool calling is more variable** — in long agent loops it may issue
  one tool call per turn (Fable 5 batched). Extra turns = extra tokens + latency,
  answer quality unchanged. Add a one-line batching instruction to the prompt.
- **Answers from memory at `low` effort** — calls search/retrieval tools less
  often.
- **Whole-file rewrites for small edits** — more output tokens.
- Less formatting in chat, denser prose.

**Breaking changes (for those building the API by hand — Claude Code/claude.ai
handle it):** forced tool use (`tool_choice: any`/`tool`) not supported; thinking
blocks are model-bound; editing history invalidates thinking blocks.

**Mythos 5.1** (`claude-mythos-5-1`): invite only (Project Glasswing). Same
specs/price as Fable 5.1, permissive safeguards. Retirement not before 1 Sep
2027. The router recommends it only if the user explicitly states Glasswing
access.

---

## 1. Model capability table (Anthropic official)

| Feature | Fable 5.1 | Opus 5 | Sonnet 5 | Haiku 4.5 |
|---|---|---|---|---|
| Context | 1M | 1M | 1M | 200k |
| Max output | 128k | 128k | 128k | 64k |
| Price (input/output $/MTok) | $10/$50 | $5/$25 | $3/$15* | $1/$5 |
| Cache read ($/MTok) | **$0.25** (0.025x) | $0.50 | $0.30 | $0.10 |
| Effort support | low–max | low–max | low–max | **none** |
| Effort default | `high` (CC) / `medium` (chat) | `high` | `high` | — |
| Adaptive thinking | yes (always on) | yes | yes | no |
| Knowledge cutoff | **Jun 2026** | May 2026 | Jan 2026 | Feb 2025 |

*Sonnet 5's intro price ($2/$10) ended 31 August 2026, standard is $3/$15.
**Mythos 5.1** = exactly the same specs/price as Fable 5.1 (invite only).
**Fable 5** (legacy) is still available: $10/$50, cache read $1.00, knowledge
cutoff Jan 2026 — but Fable 5.1 is "the go-to wherever Fable 5 was the choice".

**Opus 4.8** (legacy, recommended only for the security gate): $5/$25, 1M
context, 128k output — spec-identical to Opus 5, but Anthropic itself recommends
migrating for general work.

---

## 2. Opus 4.8-era benchmark data — ⚠️ not inherited by Opus 5

The table below is from the **Opus 4.8** era. It shows the *direction* of Rules
2 and 3 (which areas Opus is strong in, which areas Sonnet reaches parity) but
**don't use the numbers for Opus 5** — Opus 5 is probably better on all of them,
the exact gap is unknown.

| Benchmark | Opus 4.8 | Sonnet 5 | Gap |
|---|---|---|---|
| **SWE-bench Pro** (agentic, multi-step) | **69.2%** | 63.2% | Opus +6.0 |
| **Terminal-Bench 2.1** (Terminus-2, raw) | 74.6% | **80.4%** | Sonnet +5.8 |
| **HLE (tooled)** | 57.9% | 57.4% | Parity (±2.65% CI) |
| **HLE (tool-less)** | **49.8%** | 43.2% | Opus +6.6 |
| **USAMO 2026** (math) | **96.7%** | 79.5% | Opus +17.2 |

⚠️ **Terminal-Bench: two numbers, two harnesses.** 74.6% = isolated `Terminus-2`
`[K1]` (raw ability); 82.7% = with CLI scaffolding `[K2]`. In a raw comparison
74.6% applies.

⚠️ **GDPval-AA v2 is not used.** Anthropic's own `[K1]` table says 1890 for Opus
4.8; the 1603/1615 figures in circulation are `[K2/K3]` and unconfirmed. A 3-Elo
gap is inside the confidence interval anyway. This row is not the basis of any
rule.

### The direction from this table (not the numbers)

1. Sonnet 5 was ahead of Opus 4.8 on raw terminal/CLI work.
2. Opus 4.8 was ahead on agentic multi-file code + math + tool-less reasoning.
3. Tool access closes Sonnet's gap (tool-less +6.6 gap → tooled parity).

Given Opus 5's overall jump, (1) may have weakened or reversed — unclear. (2) and
(3) probably strengthened — Opus 5's chemistry/protein/Frontier-Bench jump
supports that direction.

---

## 2.1. Independent leaderboards (2 Sep 2026) — LiveBench / BenchAlign / AA Index

> **Why this section exists:** §7's "no published equal-effort Opus 5 vs Sonnet 5
> comparison" gap is now **partly** closed — LiveBench (contamination-free,
> refreshed every six months, independent) measures Opus 5, Sonnet 5, Fable 5.1
> in the same release. **These are still cross-model, different-effort
> comparisons** — a 0.4-point aggregate gap does not change routing. This table
> firms up the *direction* of Rules 2/3, it does not create a new hard gate.

### LiveBench 2026-06-25 (overall / reasoning / coding / **agentic coding** / math / data / language / IF · cost per successful task)

| Model (effort) | Overall | Rsn | Cod | **Agt** | Mth | Dat | Lng | IF | $/task |
|---|---|---|---|---|---|---|---|---|---|
| **Fable 5.1** (max) | 83.4 | 91.7 | 86.4 | **66.1** | 97.0 | 80.3 | 89.5 | 73.0 | $1.21 |
| Fable 5 (max) | 83.0 | 89.7 | 86.0 | 62.2 | 96.0 | 80.5 | 90.7 | 75.8 | $1.44 |
| GPT-5.6 Sol (max) | 81.0 | 91.7 | 83.9 | 56.2 | 96.2 | 79.8 | 87.7 | 71.8 | $0.52 |
| **Opus 5** (max) | 80.1 | 91.2 | 81.4 | **65.2** | 95.7 | 74.6 | 88.7 | 63.8 | $0.70 |
| GPT-5.6 Terra (max) | 77.9 | 90.6 | 78.2 | 54.9 | 94.9 | 79.3 | 82.9 | 64.6 | $0.35 |
| Opus 4.8 (max) | 76.2 | 89.2 | 81.8 | 50.5 | 94.3 | 66.0 | 79.7 | 72.0 | $0.98 |
| **Sonnet 5** (xhigh) | 76.0 | 88.7 | 80.7 | **59.4** | 92.9 | 71.7 | 75.0 | 63.9 | $0.51 |
| GPT-5.6 Luna (max) | 73.6 | 85.6 | 82.9 | 48.4 | 87.2 | 78.0 | 72.6 | 60.1 | $0.17 |

### Aggregate indices (Sep 2026)
- **AA Intelligence Index:** Fable 5.1 (max) **66** · Fable 5.1 (xhigh) 65 · Opus
  5 (max/xhigh) **63** · Fable 5.1 (high) 62. Kimi K3 (max) 60 = best open-weight.
- **BenchLM BenchAlign:** Fable 5.1 **82.74** (estimated, 90% interval
  71.2–94.3) · Fable 5 82.49 · Opus 5 **82.34** · GPT-5.6 Sol 81.69 · Opus 4.8
  75.96.
  ⚠️ BenchAlign shows Sonnet 5 at **64.7 / #39** — this is a **coverage artefact**
  (only 16 of Sonnet 5's benchmark rows are sourced; reasoning/math "not
  eligible"). LiveBench's full coverage keeps Sonnet 5 at 76.0. **Do not route
  from an aggregate score** — Sonnet 5 is a strong daily driver.

### Effect on routing (direction, not a rule change)
1. **Fable 5.1 ≈ Opus 5, within noise** (BenchAlign 82.74 vs 82.34; AA 66 vs 63).
   LiveBench $/successful-task Fable 5.1 $1.21 vs Opus 5 $0.70 (~1.7x). → Keeping
   Fable 5.1 **gated** is correct; do not make it a general default. Rule
   unchanged.
2. **On agentic coding, Opus 5 (65.2) ≈ Fable 5.1 (66.1), both ~6 points above
   Sonnet 5 (59.4)** — contamination-free source. → **Rule 2(a)** (agentic
   structured work → Opus 5) is now independently evidenced.
3. **On language, Opus 5 (88.7) vs Sonnet 5 (75.0) = +13.7; reasoning +2.5;
   math +2.8.** → **Rule 3's "escalate" note** now stands on firmer ground: for
   D=3 work outside Rule 2, Sonnet 5 stays the quota default, but if the result
   is critical there's a concrete reason to move to Opus 5 (not just "unproven").
4. **GPT-5.6 Sol:** neck-and-neck with Opus 5 on reasoning/math but **weak on
   agentic coding** (56.2 < Sonnet 5). The Codex arm's D=3→Sol mapping is
   correct; but note (if the user asks) that Sol is comparatively weaker than
   the Claude side on long agentic coding work.

> **Sources:** `livebench.ai` (2026-06-25 release), `artificialanalysis.ai/models`,
> `benchlm.ai` — all read directly on 2 Sep 2026. All three agree on the top
> order: Fable 5.1 ≈ Fable 5 ≈ Opus 5 > Sol > the rest, and Fable 5.1's gap over
> Opus 5 is within noise on all three.

---

## 3. Effort levels

**Effort is not a token budget.** It's a behavioural signal: it affects the
model's **entire** token spend — text, tool calls, thinking.

### Support per model

| Model | Levels | Default |
|---|---|---|
| **Fable 5.1** / Mythos 5.1 | low, medium, high, xhigh, max | high (Claude Code) · medium (claude.ai / Cowork) |
| Fable 5 (legacy) | low, medium, high, xhigh, max | high |
| **Opus 5** | low, medium, high, xhigh, max | high |
| Sonnet 5 | low, medium, high, xhigh, max | high |
| Opus 4.8 | low, medium, high, xhigh, max | high |
| Opus 4.7 | low, medium, high, xhigh, max | **xhigh** (exception) |
| Opus 4.6, Sonnet 4.6 | low, medium, high, max (**no xhigh**) | high |
| Haiku 4.5 | **none** | — |

If `xhigh` is requested but unsupported, it falls to the nearest supported level
below (e.g. `xhigh` → `high` on Opus 4.6).

### Advice per model (Anthropic's own text)

- **Opus 5:** start from `high` (default). Go to `xhigh` for coding/agentic work,
  to `max` for a genuine frontier problem. **"Use low and medium freely as a
  cost/speed control wherever your eval holds up."** — a deliberate tone shift
  from earlier Opus generations; low/medium is no longer a "restricted mode",
  it's a normal dial.
- **Sonnet 5:** `high` default. `xhigh` for the hardest coding/agentic work.
  `medium` ≈ "Sonnet 4.6's `high`".
- **Opus 4.8/4.7:** start from `xhigh` for coding/agentic work; drop to
  `low`/`medium` only after measuring with an eval (more conservative advice than
  Opus 5).
- **Fable 5.1:** start from `high` (Claude Code default) or `medium` (chat
  default), tune with an eval. The gain over Fable 5 is widest at high effort. It
  calls search/retrieval tools less often at `low` effort — raise effort for a
  turn that needs fresh information (Fable 5.1 supports mid-conversation effort
  changes without busting the cache).

### `ultracode` — a Claude Code level

There **is** an `ultracode` in the `/effort` menu. It's not a *model* effort
level:

> "Ultracode is a Claude Code setting rather than a model effort level: it sends
> `xhigh` to the model and additionally has Claude orchestrate dynamic workflows
> for substantive tasks. It applies to the current session only."

- **No model restriction** — it works on every model that supports `xhigh`: Fable
  5.1, Sonnet 5, **Opus 5**, Opus 4.8, Opus 4.7. Doesn't work on Haiku 4.5. Opus
  4.6/Sonnet 4.6 have no `xhigh` → `ultracode` falls to `high` if requested.
- Ways to enable: `/effort ultracode` · `claude --effort ultracode` · `"ultracode":
  true` via `--settings` · Agent SDK `effortLevel: "ultracode"`
- **Per-session.** Can't be written to a config file or `CLAUDE_CODE_EFFORT_LEVEL`.
- If workflows are off, `--effort ultracode` applies `xhigh` only.

### `ultrathink` — one-off depth

Write `ultrathink` into the prompt → deeper reasoning for that turn, **the effort
level doesn't change**. Phrasings like "think", "think hard" are not recognised.

### When `ultracode` is used

- **Yes:** 100+ file audit, huge migration, cross-verification needing 3+
  independent verification angles, competitive analysis, PRD review.
- **No:** single-file edit, quick question, everyday work.
- **Conflict:** `ultracode` only sends `xhigh` to the model; if you need `max`,
  don't pick `ultracode`.

### `opusplan` — plan/execute model split

**Only in Claude Code** (`/model opusplan`), no equivalent on Claude.ai. Official
definition:

> "The `opusplan` model alias provides an automated hybrid approach:
> In plan mode: uses `opus` for complex reasoning and architecture decisions.
> In execution mode: automatically switches to `sonnet` for code generation
> and implementation. This pairs Opus's reasoning for planning with Sonnet's
> efficiency for execution."

Verified behaviour details:
- **Context window:** the Opus in the plan phase uses the same context window as
  the `opus` setting. For plans with an automatic 1M upgrade the plan phase is
  upgraded too. If there's no upgrade, use `opusplan[1m]` to force both phases to
  1M.
- **If there's an allowlist restriction:** the newest permitted Opus version is
  used for planning; if no Opus is permitted, the plan phase stays on Sonnet too.
- **⚠️ Effort does not carry over.** Opus 5 and Sonnet 5 are both "hold"-free
  models (see §3 "Defaults") — so the effort set in plan mode **carries over as
  is** to execution, it does not drop automatically. If the user doesn't lower
  the effort manually when switching to the execution phase, Sonnet 5 runs at a
  needlessly high effort and `opusplan`'s quota-saving purpose is lost. **This is
  a mandatory warning the router must add to every opusplan output.**
- **A related but different feature — "advisor tool":** the official docs
  reference: *"For a hybrid approach where Claude decides mid-task when to
  consult a second model rather than switching at the plan boundary, see the
  advisor tool."* This is a mechanism for consulting a second model mid-task,
  unlike opusplan's fixed plan/execute boundary — the router **has not examined
  this yet**, it's not in the rule set. Could be researched later.

### When `opusplan` is used — the distinguishing diagnostic

For the router to recommend `opusplan`, all three conditions must hold (see
`SKILL.md` Step 3): D=3 ∧ Rule 2(a) territory, difficulty front-loaded into the
plan, W≥2.

**The most critical distinction — where the difficulty concentrates:**

| Kind of difficulty | Example | opusplan suitable? |
|---|---|---|
| Front-loaded: once the plan is done, execution is a repeating pattern | "Migrate 40 services to a shared middleware, define the design once" | ✅ |
| Persistent: each execution step needs its own discovery/judgement | Race-condition hunt — the cause isn't known without reading the code | ❌ |
| Persistent: plan and execution are inseparable, the proof itself is the work | Formal correctness proof | ❌ |
| Insufficient volume (W≤1) | A small architectural decision, single-file impact | ❌ — plain Opus 5 is enough, mode switch is overhead |

**Live-test finding (from this session):** the task of redesigning this router's
own architecture (in Rule 2a territory, D=3) **did not** hit `opusplan` — both
W=1 (few files) and the difficulty was persistent throughout execution (constant
test/fix while writing the rules), the plan didn't become mechanical in one
pass. This is evidence the criterion makes the right distinction on a real case.

---

## 4. Pricing (per MTok) — 1 September 2026

| Model | Input | Output | Cache write (5m) | Cache read |
|---|---|---|---|---|
| **Fable 5.1** / Mythos 5.1 | $10.00 | $50.00 | $12.50 | **$0.25** |
| Fable 5 (legacy) | $10.00 | $50.00 | $12.50 | $1.00 |
| **Opus 5** | $5.00 | $25.00 | $6.25 | $0.50 |
| Opus 4.8 (legacy) | $5.00 | $25.00 | $6.25 | $0.50 |
| Opus 4.8 (Fast Mode) | $10.00 | $50.00 | $12.50 | $1.00 |
| Sonnet 5 (promo ended 31 Aug 2026) | $3.00 | $15.00 | $3.75 | $0.30 |
| Haiku 4.5 | $1.00 | $5.00 | $1.25 | $0.10 |

**Fable 5.1 cache read:** **0.025x** of base input (every other model is 0.1x).
Long agentic sessions that re-read a cached prefix pay **¼** of the Fable 5 rate
— recommending Fable 5.1 at the frontier gate is markedly cheaper on quota than
the Fable 5 era. Batch: $5 / $25.

**Opus 5 / Sonnet 5 ratio:** 1.67x (promo ended). For a subscription user this
is a rough proxy for how fast quota burns.

**Fast Mode now covers Opus 5 too** (research preview): $10/$50, 2.5x faster
output. Toggled with `/fast` in Claude Code. Not on Opus 4.7, runs at standard
speed/price on Opus 4.6. The Codex-side analogue is **Codex CLI Fast Mode (1.5x)**
— see §9.7. The router appends a speed line to every CLI Codex output
(`SKILL.md` → Codex arm → "Fast Mode (1.5x)"); the Claude `/fast` half is added
only when the Claude line is Opus 5 / Opus 4.8.

**Tokenizer inflation:** the Opus 4.7+ tokenizer produces ~30% more tokens for
the same text (1.4x for English). Opus 5, Fable 5.1, Fable 5, Sonnet 5 all use
this tokenizer.

**Batch API:** 50% discount on all models.

---

## 5. Subscription plans and default model

| Plan | Price | Claude Code | Default model |
|---|---|---|---|
| Pro | $20/mo | ✅ | **Sonnet 5** |
| Max 5x / Max 20x | $100 / $200/mo | ✅ | **Opus 5** |
| Team Standard | $25/seat | ❌ **NO** | — |
| Team Premium | $125/seat | ✅ | **Opus 5** |
| Enterprise (subscription seat) | — | ✅ | **Sonnet 5** |
| Enterprise (pay-as-you-go) / API | — | ✅ | **Opus 5** |

Defaults changed with the Opus 5 launch: Max/Team Premium/Enterprise-PAYG/API now
auto-default to **Opus 5** (previously Opus 4.8). Pro and Team Standard are still
**Sonnet 5**.

❌ **Debunked: there is no fixed "10–40 prompts per 5-hour window" quota.** Quotas
reset every 5 hours but erode by **token + context length**, not a count.

**Agent SDK credits:** Pro $20, Max 5x $100, Max 20x $200 — SDK-only, per
individual.

---

## 6. Hidden quota burners

1. **MCP servers.** Each server injects tool schemas into every message. The load
   is not fixed per server, it's **proportional to the tool count** (GitHub MCP:
   27 tools ≈ 18k tokens; Playwright: 21 tools ≈ 13.6k).
2. **Auto-accept always on.** Chained edits create a "geometric cost machine".
3. **Not using prompt caching.** Cache read is up to 90% off (**97.5%** on Fable
   5.1 — cache read is 0.025x of base input). Minimum cacheable text: 4096 tokens
   on Opus models, **512 on Fable 5.1**.

---

## 7. Data status

### ✅ Resolved / verified

- **Opus 5 is real**, launched 24 July 2026, replaced Opus 4.8.
- **Fable 5.1 / Mythos 5.1 are real**, launched 1 September 2026
  (`claude-fable-5-1` / `claude-mythos-5-1`). Fable 5.1 is available to all
  customers; Mythos 5.1 is Project Glasswing invite only. Same specs/price; cache
  read $0.25/MTok; knowledge cutoff Jun 2026. Verified against
  `platform.claude.com/docs/en/models/fable-5-1/*` (2 Sep 2026).
- Fable 5.1 offensive-cyber fallback targets: **Opus 4.8 and Opus 5** (official
  docs). Defensive vulnerability discovery is now permitted on Fable 5.1.
  Biology R&D → Opus models; Opus 5 itself refuses biology R&D.
- Fable 5 (legacy) fallback chain: cyber→Opus 4.8, biology→Opus 5.
- `task_budget` minimum = 20,000 tokens. The "2,000" claim came from confusion
  with `max_tokens`, it's wrong.
- The two Terminal-Bench numbers (74.6%/82.7%) are a harness difference, not a
  contradiction.
- `ultracode` is not in the API; it's the Claude Code CLI's `xhigh`+workflow
  macro.

### ❌ Debunked — must not enter the router

| Claim | Reality |
|---|---|
| Token budgets for effort levels (~1,024/~4,000/~8,000) | No such budget exists |
| `task_budget` minimum 2,000 | 20,000 |
| "10–40 prompts per 5-hour window" | Quota erodes by token+context |
| Every MCP server = a fixed 18k tokens | Proportional to tool count |
| "Sonnet 5 beat Opus on GDPval" | 3 Elo is not meaningful, Opus's K1 score is 1890 |
| Opus 4.8's benchmark profile applies to Opus 5 too | **Separate model**, no granular comparison published |

### ⚠️ Still unresolved

- **Opus 5 vs Sonnet 5**: Anthropic's own equal-effort SWE-bench Pro /
  Terminal-Bench / HLE comparison is still unpublished — but **LiveBench
  2026-06-25** (independent, contamination-free) now measures both in the same
  release (see §2.1): agentic coding Opus +5.8, language Opus +13.7, reasoning
  Opus +2.5. Rule 3 still keeps Sonnet 5 the default for quota reasons but the
  "escalate" note is no longer unproven.
- **GPQA Diamond / Fable 5.** 87.8% `[K3]` — below Opus 4.8's 93.6%, contradicts
  older reports. Fable's GPQA superiority is unconfirmed.
- Which Opus (4.8 or 5) Fable 5.1 routes a biology-R&D-flagged request to is
  unclear — the official text just says "Opus models". The router doesn't
  over-specify: biology-adjacent work → recommend Fable 5.1, the redirect is
  expected.
- Whether Codex/ChatGPT has a permissive-safeguard behaviour like Claude's for
  defensive vulnerability discovery **was not researched** — the Codex arm still
  goes through normal scoring in this category (it only says "unverified" for
  offensive + biology R&D).

---

## 8. Example library — use for analogy when scoring

Each row: prompt → R,D,W,C → model·effort. Non-coding areas are included too,
because SKILL.md's default reading drifts toward coding. If your own prompt
resembles one on this list, use that example's score as a starting point.

### Coding

| Prompt | R,D,W,C | → |
|---|---|---|
| "Fix the typo in this function" | 1,0,0,0 | Haiku 4.5 *(D=0, genuinely trivial)* |
| "Add input validation to this API endpoint" | 1,1,0,0 | Sonnet 5 · medium *(D=1 "known pattern" → not Haiku)* |
| "Add dark mode support to this component" | 1,1,1,1 | Sonnet 5 · medium |
| "Merge 3 services onto a shared auth middleware" | 2,2,2,2 | Sonnet 5 · high |
| "Find and fix the race condition in this cache-invalidation logic" | 2,3,1,2 | Opus 5 · xhigh *(agentic code domain)* |
| "Split the monolith into 12 microservices, including data consistency" | 3,3,3,3 | Opus 5 · max, `ultracode` **no** *(D=3∧R=3 conflict)* |
| "Migrate 500 files from the old logging library to the new one" | 1,1,3,1 | Sonnet 5 · **ultracode** *(when ultracode fires, the effort field says "ultracode", not D's value)* |
| "Get this SQL query out of N+1" | 1,1,0,0 | Sonnet 5 · medium *(D=1 "known bug shape" → not Haiku)* |
| "Add cursor-based pagination to this API" | 1,1,0,0 | Sonnet 5 · medium *(well-documented single pattern → D=1, not D=2)* |
| "Add a `last_login_at` column and make it nullable" | 2,0,0,0 | Sonnet 5 · low *(fully-specified additive schema → D=0; R=2 reversible migration → not Haiku)* |
| "Change this button's colour from blue to green" | 1,0,0,0 | Haiku 4.5 *(source-code change → R=1 by default, PR-reviewed)* |
| "Design a new rate-limiter algorithm, consistent in a distributed system" | 2,3,1,1 | Opus 5 · xhigh *(algorithmic depth)* |
| "Review this single-file JWT validation module for security vulnerabilities" | 1,3,0,1 | Sonnet 5 · xhigh *(adversarial vuln hunt → D=3; W=0 → not ultracode; outside Rule 2 → Sonnet)* |

### Structured system design (not code but hits Rule 2a)

Found in live testing: when Rule 2(a) only looked at "programming-language code",
work like rule-engine/prompt-architecture design incorrectly fell to the default
Sonnet. This category shows Rule 2(a) also covers non-code.

| Prompt | R,D,W,C | → |
|---|---|---|
| "Decouple this router's model selection from risk, design the conflict rules from scratch" | 1,3,1,2 | Opus 5 · xhigh *(structured system design — Rule 2a)* |
| "Enrich this skill's axis definitions with examples and counter-examples" | 1,2,1,1 | Sonnet 5 · high *(extending an existing framework, not design from scratch)* |
| "Build a new decision tree: choose among 3 outputs based on 5 inputs" | 1,3,0,1 | Opus 5 · xhigh *(decision-logic design, not code but D=3)* |

### Writing / analysis / legal work

| Prompt | R,D,W,C | → |
|---|---|---|
| "Rewrite this email in a more polite tone" | 1,0,0,0 | Haiku 4.5 |
| "Rewrite these three paragraphs in a more formal tone" | 1,0,0,0 | Haiku 4.5 *(tone only, no content change → D=0 regardless of length)* |
| "Summarise these meeting notes into 5 bullets" | 1,1,0,1 | Sonnet 5 · medium |
| "Write a report comparing the pricing of 3 competitors" | 1,2,1,2 | Sonnet 5 · high |
| "Find the clauses in this 40-page contract that conflict with the arbitration clause" | 2,3,1,2 | Sonnet 5 · xhigh *(outside Rule 2 → cheap default)* |
| "Build a legal defence strategy against this indictment (the facts are in the prompt, no need to read files)" | 3,3,1,1 | Opus 5 · max *(tool-less deep reasoning — Rule 2c; R=3 pulls the effort not the model to `max`)* |
| "Read this 300-page API documentation, list the deprecated endpoints" | 1,1,1,3 | Sonnet 5 · medium *(C=3 alone doesn't trigger Opus)* |

### Research / data

| Prompt | R,D,W,C | → |
|---|---|---|
| "Compute the monthly sales total in this CSV" | 1,0,0,0 | Haiku 4.5 |
| "Compare these two datasets, flag the anomalies" | 1,1,1,1 | Sonnet 5 · medium |
| "Find the factors driving user churn with a regression" | 1,3,1,2 | Sonnet 5 · xhigh *(statistical modelling, not agentic code but uses tools)* |
| "Synthesise 10 academic papers and propose a new hypothesis" | 1,3,1,3 | Sonnet 5 · xhigh *(research D=3, outside Rule 2)* |
| "Without running code, using only your literature knowledge, argue theory X's superiority over Y" | 1,3,0,1 | **Opus 5 · xhigh** *(genuine tool-less deep reasoning — Rule 2c)* |

### Ops / DevSecOps (excluding offensive security — that's at the hard gate)

| Prompt | R,D,W,C | → |
|---|---|---|
| "Find the flaky test in the CI pipeline" | 1,1,1,0 | Sonnet 5 · medium |
| "Add the same health-check endpoint to 60 independent microservices" | 1,1,2,0 | Sonnet 5 · medium *(60 < 100 → W=2, not W=3 → no ultracode; effort follows D=1)* |
| "List which security-group rules allow 0.0.0.0/0 on ports other than 80/443" | 1,1,1,1 | Sonnet 5 · medium *(mechanical enumeration → D=1, not the D=3 adversarial case; defensive → no gate)* |
| "Profile 180 services for performance regression" | 2,2,3,2 | Sonnet 5 · **ultracode** *(W=3 triggered; the effort field says "ultracode", not D's `high`)* |
| "Find the deploy that caused the prod CPU spike, don't roll back yet" | 2,2,1,2 | Sonnet 5 · high |
| "Migrate the Kubernetes cluster to multi-region HA from scratch" | 3,3,2,2 | Opus 5 · max |

### Step 0 examples (clarification should be asked, scoring does not start)

This category was validated by a live user example: Step 0's old form ("ask if
there's no success criterion/scope") was too coarse and never triggered in real
use. In all of the examples below scope **appears to be present** but a critical
parameter is stated by example, not generalised.

| Prompt | Why Step 0 triggers |
|---|---|
| "If 1000 units are produced in a day, 500 should land the same day, 500 the next day" | Fixed 500, 50%, or an hour-based cutoff — unclear; the example doesn't stand in for the general rule |
| "Apply an extra discount on large orders, like 5% over 10,000" | The word "like" shows the threshold and rate aren't firm |
| "Optimise this table for performance" | No "performance" metric — latency, throughput, which query? |
| "If a user is inactive, deactivate the account" | "Inactive" undefined — how many days, absence of which action |

**Counter-example (Step 0 does not trigger):** "Add a `deleted_at` column to this
table and implement soft-delete, update this field instead of `DELETE`" — the
rule is complete, one interpretation, concrete scope. Go straight to scoring.

### Hard-gate examples (scoring disabled)

| Prompt | Gate | → |
|---|---|---|
| "Categorise 1000 support tickets" | Volume | Haiku 4.5 |
| "Run a penetration test against this environment, build an exploit chain" | Offensive security | Opus 4.8 · xhigh |
| "Audit this API code for auth-bypass vulnerabilities" | **NO gate** (defensive) → normal scoring | Sonnet 5 · xhigh (Fable 5.1 can do it too) |
| "Optimise this protein-folding simulation code" | Biology-adjacent R&D | Fable 5.1 · high |
| "Analyse an 800k-token log history" | Context >200k | Haiku removed → Sonnet 5/Opus 5 |

---

## 9. Codex / ChatGPT ecosystem (dual-provider expansion, 5 August 2026)

> **Source status:** the user provided a "current Codex Plus models report" —
> compiled from SEO/aggregator sites (gradually.ai, felloai.com, analyticsvidhya,
> datacamp, mindstudio.ai etc.), not an official OpenAI doc. Just like the Claude
> reports at the start of this project, it was **not trusted directly** — it was
> cross-checked against `openai.com/index/gpt-5-6/`,
> `developers.openai.com/api/docs/guides/reasoning`,
> `developers.openai.com/api/docs/guides/latest-model`,
> `learn.chatgpt.com/docs/config-file/config-reference`.

### 9.1. Model family — GPT-5.6 (Sol, Terra, Luna)

Went to general availability on 9 July 2026. Sol is the flagship, Terra the
balanced mid-tier, Luna the speed/cost-focused budget model — verified directly
from the official launch page.

**Sol Ultra:** introduced 26 June 2026, GA on 9 July. A **product mode** (not a
model, not an effort value — `effort: "ultra"` returns HTTP 400), toggled in
Codex settings on **Plus plans and up** (Pro/Enterprise in ChatGPT Work).
Instead of a single reasoning chain it decomposes the task into ~4 collaborating
agents that communicate in real time (more in "multiagent v2" mode). "Sol Ultra"
= `gpt-5.6-sol` with the mode on. Context window **43% larger** than GPT-5.5
(~1.5M tokens — single-source claim, couldn't be confirmed directly from the
official page).

### 9.2. Pricing (per MTok) — after the 30 July 2026 price cut

| Model | Input | Output |
|---|---|---|
| Sol | $5.00 | $30.00 |
| Terra | $2.00 | $12.00 |
| Luna | $0.20 | $1.20 |

**The user's report was stale:** it said Terra $2.50/$15, Luna $1/$6 — those are
the pre-30-July prices. On that date OpenAI cut Luna 80%, Terra 20%, Sol
unchanged. Output price is **6x** input on all three models (fixed ratio).

### 9.3. Effort / reasoning mechanics — three separate things

The report described a single linear ladder
"Instant→Low→Medium→High→Extra High→Max→Ultra". It's actually **three separate
things**:

1. **`reasoning.effort`** — supported values `none, minimal, low, medium, high,
   xhigh, max` (varies by model; `openai.com/index/gpt-5-6/` +
   `developers.openai.com/api/docs/guides/reasoning`). Default `medium`.
   **`max` is real on Codex** (updated 2 Sep 2026): the GPT-5.6 GA note says
   `max` "is available to all users with access to GPT-5.6 in ChatGPT Work and
   Codex and can be toggled on in settings". The
   `learn.chatgpt.com/docs/config-file/config-reference` page still lists only up
   to `xhigh` — it's **stale**, a doc lag, not a real limit. Known snag: some
   third-party gateways / CLI wrappers still 400 on `effort: "max"` (open GitHub
   issues) — a tooling gap, not a product one. → **The router uses `max` as the
   Codex ceiling for `D=3 ∧ R=3`, matching Claude.**
2. **`reasoning.mode`** — `standard` (default) or `pro`, a **separate axis** from
   effort (defaults to `medium` effort). *"Mode selects standard or pro
   execution, while reasoning.effort controls how much reasoning the model
   applies within that mode."* Confirmed for the **Responses API only**; no
   `model_reasoning_mode` key in the Codex CLI config reference. → Router mentions
   it only if asked, as "API-only".
3. **`ultra` — a product mode, not an effort value.** Sending
   `reasoning: {effort: "ultra"}` returns **HTTP 400**. Ultra is toggled in Codex
   settings (Plus plans and up) and runs ~4 collaborating agents in parallel
   (more in "multiagent v2"). "Sol Ultra" = `gpt-5.6-sol` with that mode on — not
   a separate model slug; it rides on top of a normal effort level. For API
   builders the equivalent is OpenAI's "Multi-Agent orchestration" beta. The
   Codex CLI's config reference exposes the underlying knobs as an `agents` table
   (`agents.default_subagent_model`, `agents.default_subagent_reasoning_effort`,
   `agents.max_concurrent_threads_per_session`, `agents.max_threads`). This is
   symmetric with Claude's `ultracode` "a setting, not an API parameter" status
   but a **stronger** mechanism: genuine concurrent collaborative model instances.

### 9.4. ChatGPT Plus quotas

| Tier | Capacity | Note |
|---|---|---|
| Instant (fast) | ~160 messages / 3 hours | Attributed to GPT-5.5 in one source, whether it carried to GPT-5.6 not freshly verified — the mechanism probably continues |
| Thinking (reasoning) | ~3,000 messages / week | Same verification note applies |
| File upload | ~80 files / 3 hours | May drop at peak hours |

⚠️ These quota numbers **were not freshly verified against help.openai.com's own
current article** (confirmed indirectly via search results) — they enter the
router with a "probably right, not certain" note, don't use them as firm numbers.

### 9.5. Benchmark status — Terminal-Bench 2.1 numbers are CONTRADICTORY, not used as a rule basis

The user's report gave a single firm ranking (Sol Ultra 91.9%, Sol 88.8%, Terra
87.4%, Luna 84.7%, Claude Fable 5 86.0%). Scanning independent sources found
**three different methodologies, three different rankings**:

| Source/methodology | Result |
|---|---|
| "Resolution rate" methodology | Opus 5 (max) 43.5% ahead, GPT-5.6 Sol (max) 34.4%, Fable 5 (max) 33.8% |
| Artificial Analysis | GPT-5.6 Sol (xhigh) 89.5% ahead, Opus 5 (max) 89.1%, Terra (max) 88.0% |
| Another source | Opus 5 89.1% ahead, Sol 88.8% |

**This router does not use any Terminal-Bench number as the basis of a
"Claude/Codex which is better" decision** — the same discipline applied to
Claude-internal comparisons (see §2 "GDPval-AA v2 is not used") applies here too.
And since 5 August 2026 the router recommends **both** (see `SKILL.md` "Output
format") — it doesn't have to decide which is "better", so contradictory
benchmark numbers are also architecturally irrelevant now.

**LiveBench 2026-06-25 (§2.1) is the one exception:** it measures both Claude and
GPT-5.6 in the same release with the same methodology — the router uses it as a
single direction indicator for the Codex arm: **GPT-5.6 Sol is neck-and-neck with
Opus 5 on reasoning/math but weak on agentic coding** (Sol 56.2 vs Sonnet 5 59.4
vs Opus 5 65.2). So the Codex D=3→Sol mapping is kept, but note (if the user
asks) that Sol is comparatively disadvantaged versus the Claude side on long
agentic coding work.

### 9.6. Data status summary

**✅ Verified (official source):**
- GPT-5.6 Sol/Terra/Luna family, 9 July 2026 GA.
- Current prices (§9.2), the 30 July price cut.
- **LiveBench 2026-06-25 (§2.1):** GPT-5.6 Sol/Terra/Luna and Claude Fable 5.1/
  Opus 5/Sonnet 5 measured in the same release. Sol neck-and-neck on
  reasoning/math, weak on agentic coding (56.2). `livebench.ai` — read directly
  2 Sep 2026.
- **`reasoning.effort` ladder is `none, minimal, low, medium, high, xhigh, max`**
  and **`max` is a Codex setting toggle** for anyone with GPT-5.6 access
  (`openai.com/index/gpt-5-6/` + GA note, re-verified 2 Sep 2026). The router
  uses `max` as the Codex ceiling for `D=3 ∧ R=3`. The
  `learn.chatgpt.com/docs/config-file/config-reference` page is stale (lists only
  to `xhigh`).
- **`ultra` is a product mode, not an effort value** — `effort: "ultra"` → HTTP
  400. Codex Plus+ toggle, ~4 parallel agents. "Sol Ultra" = `gpt-5.6-sol` +
  ultra mode. Sub-agent config keys: `agents.default_subagent_model`,
  `agents.default_subagent_reasoning_effort`, `agents.max_concurrent_threads_per_session`,
  `agents.max_threads`.
- `reasoning.mode` (`standard`/`pro`) is a separate axis from effort — confirmed
  for the Responses API only (no `model_reasoning_mode` key in the Codex CLI).
- Codex CLI model selection: `--model`/`-m` flag, `model` key in `config.toml`.

**❌ Debunked (the report was wrong):**
- Terra/Luna's old prices ($2.50/$15, $1/$6).
- The one-dimensional "Instant→...→Ultra" ladder — actually effort (`none`…`max`)
  + a separate `mode` axis (`standard`/`pro`, API-only) + a separate product mode
  (`ultra`, not an effort value).
- (Earlier version of this file) "`max` unverified in the Codex CLI, use `xhigh`
  as the ceiling" — `max` was confirmed as a Codex toggle on 2 Sep 2026; the
  ceiling is now `max`.

**⚠️ Could not be verified / not researched — did not enter the router:**
- Whether Codex/ChatGPT has a safety-classifier/fallback chain like Claude's for
  security or biology-adjacent content. Because of this uncertainty the Codex arm
  recommends no model in these two categories, it says "unverified — use Claude".
- Per-model context window for Luna/Terra/Sol-base (only a single-source ~1.5M
  claim for Sol Ultra).
- Whether the ChatGPT Plus quota numbers carried to GPT-5.6 (§9.4).
- Whether `reasoning.mode: pro` can be set via the Codex CLI in any way (not in
  the config reference, maybe possible via a `--config` override, not tried).
- Independent benchmark numbers for **Sol Ultra specifically** — the only figure
  seen is Terminal-Bench 2.1 91.9%, which is in the contradictory pile (§9.5).
  LiveBench §2.1 has Sol/Terra/Luna at plain `max`, not Ultra.
- The firm ranking of Terminal-Bench 2.1 and similar cross-provider benchmarks
  (§9.5) — contradictory, not used as a rule basis.
- Whether "Codex CLI Fast Mode (1.5x)" exists by that name — user-reported 2 Sep
  2026, no official page found (§9.7). It is carried in the **default output** as
  a user-provided feature; a later pass should confirm or drop it.

---

## 9.7. Codex CLI Fast Mode (1.5x) — user-reported 2 Sep 2026, not independently verified

> **Source:** the skill owner reported that Codex CLI exposes a "Fast Mode"
> toggle. No `openai.com` / `developers.openai.com` page was found documenting it
> by that name — it enters the router the way the 2 Sep `max` update did:
> **"probably real, treat as user-provided"**, flagged here so a later pass can
> confirm or drop it.

**What it is:** a speed toggle **independent of the model and of
`reasoning.effort`**. With it on, output streams ~**1.5x** faster and the
subscription quota / API bill is consumed at that same 1.5x rate. Model choice,
reasoning depth and answer quality are **unchanged** — it buys latency with
quota, nothing else.

**Claude-side analogue:** Claude Code `/fast` (Fast Mode) — 2.5x faster output,
**doubles the price** ($10/$50), **Opus 5 / Opus 4.8 only** (§4). Both are
CLI/desktop toggles; neither exists on the web UI.

**How the router uses it — the speed line.** Unlike `mode: pro` (kept as an
on-ask suggestion), Fast Mode goes in the **default output**: a line appended
under the two model lines on **every CLI Codex output whose Codex line names a
real model**. It has **two forms, and the first word says which** — so the reader
can tell a nudge from an FYI:

| Form | When | Line |
|---|---|---|
| **`recommended`** | `R ≤ 1` **∧** (`D ≤ 1` ∨ Step-1 volume/latency gate ∨ user explicitly asked for speed) | `⚡ Fast Mode recommended: Codex Fast Mode (1.5x faster, 1.5x quota) — low-risk / mechanical work.` |
| **`available`** | everything else | `⚡ Fast Mode available: Codex Fast Mode (1.5x faster, 1.5x quota)[ · Claude /fast (2.5x faster, 2× price)].` |

- **Why `recommended` is gated on `R≤1 ∧ (D≤1 ∨ …)`:** on short mechanical /
  low-stakes work the 1.5x quota cost is tiny in absolute terms and the user
  isn't going to pore over the output — pure upside. On `D≥2` / `R≥2` the output
  is something you read carefully and 1.5x of a large token count is a real hit,
  so it drops to `available` (stated, not pushed).
- **Claude half** (`· Claude /fast (2.5x faster, 2× price)`): appended **only to
  the `available` form**, and only when the Claude line is `Opus 5` / `Opus 4.8`.
  Never on `recommended` (that requires `D≤1`; the Claude line is Opus only at
  `D=3`) and never a nudge (`/fast` doubles the price). Not for `opusplan`
  (execution drops to Sonnet), Haiku, Sonnet, Fable 5.1.
- **No speed line** when the Codex line is "unverified — use Claude" (the feature
  is Codex-anchored), or when the user is explicitly on a web surface.
- Ordering with the other exception lines: the `opusplan` warning stays directly
  under the Claude line; the speed line sits just **above** the `R=3`
  human-review note.

**Why default output, not on-ask:** the skill owner asked for it to be surfaced
every time — it's a cheap, always-relevant lever (every Codex CLI session can
toggle it) and the quota trade-off is exactly the kind of thing this router
exists to make visible. Even the `recommended` form is a suggestion the user can
ignore — the router never toggles anything itself.

**Combining with Sol Ultra:** technically independent toggles, so the line still
appears on `Sol Ultra` outputs. The combination (≈4 parallel agents × 1.5x quota
rate) is expensive — the "burns quota faster" wording is the whole warning; the
user weighs it.

**Eval impact:** the speed line is additive text that `grade_routing.py` ignores
(it extracts only `Claude:` / `Codex:` lines and named notes). No existing eval
breaks. If a future eval wants to assert the line, add an `expected` field for
it.

---

## 10. Routing rubric — edge cases & rationale

> **Why this section exists:** `SKILL.md` used to carry every one of these notes
> inline. It grew to ~920 lines / ~12k tokens of nested blockquotes, and a cold
> agent re-reading all of it before every route was spending ~2 min second-
> guessing each score. The decision spine stays in `SKILL.md`; the accumulated
> rulings (10 eval iterations' worth) live here and are consulted **only when a
> specific score is genuinely ambiguous**. Nothing here changes routing
> behaviour vs. the pre-trim `SKILL.md` — it is the same content, relocated.
> (Trim done 2 Sep 2026, verified by routing eval iteration-11.)

### 10.1. Step 1 hard-gate rationale

**Why offensive security → straight to Opus 4.8.** Fable 5.1, Opus 5 and Sonnet
5 each have their own safety classifiers. When an offensive request (exploit
generation, penetration testing, binary-based vulnerability scanning) is
flagged, Fable 5.1's permitted fallback targets are **Opus 4.8 and Opus 5**. The
router skips the redirect and recommends **Opus 4.8** directly (most permissive
general model on cyber posture). Do **not** recommend Sonnet 5 — it is
deliberately isolated from exploit generation (0% working-exploit rate on the
Firefox 147 evaluation). With Glasswing access → **Mythos 5.1 · xhigh**.

What changed with Fable 5.1 vs Fable 5: (a) defensive vulnerability discovery is
no longer blocked — Fable 5.1 does it itself; (b) on benign requests, cyber
interventions dropped ~60% per session.

**`ultracode` can still rise above the `xhigh` floor.** The offensive gate is
"deciding" but only fixes the **model**. After it fires, check
`W=3 ∧ duration>30min ∧ ¬(D=3 ∧ R=3)` normally — if it holds, effort is
`ultracode`, not `xhigh` (the "180-service penetration test" example).

**Why biology-adjacent → Fable 5.1, not Opus 5.** On benign/educational
biology-medical questions safeguards fire ~85% less — not a gate, normal
scoring. The gate is only for **R&D-heavy** work:
- **Fable 5.1** → R&D-flagged parts auto-redirect to **Opus models** (expected).
- **Opus 5** → biology R&D has **no fallback, it refuses directly.** So
  recommending Opus 5 here can hit the user with a flat refusal.

Life Sciences Verification Program researchers use **Mythos 5.1** (invite only).
**Do not put an effort floor on Fable 5.1** — default `high`; it calls
search/retrieval less at `low`, so raise effort for work needing fresh info.

**Frontier-scale gate — one signal is enough.** Not "thousands of files AND 1M
context AND persistent memory" — just the file/scope count (1000+). Work at that
scale already requires the rest; the prompt isn't expected to state it.
✅ "Break up this 4000-file legacy monolith into modules" — only the file count
is written, the gate still fires → Fable 5.1. Don't confuse with Step 2's `W=3`
threshold (100+ files): 100–999 files → normal scoring, not this gate.

### 10.2. R axis — worked pairs

> **Architectural decision label ≠ R=3.** The real question is reversibility.
> ✅ R=2: "Migrate 40 microservices to a shared auth middleware" — each service
>    uses its own middleware independently; service-by-service phased migration
>    and rollback are possible; architectural but reversible.
> ❌ R=3: "Redesign the auth architecture of 200 prod services from scratch" —
>    a single central identity/authorization core (token schema, trust boundary)
>    all 200 services jointly depend on; phased rollout doesn't make it
>    reversible because the design decision itself is shared.

> **Large decomposition — module or service?**
> "Break the monolith into **modules**" = internal refactor, reversible via a
> strangler-fig approach → **R=2** (validation id 8 → `Fable 5.1 · ultracode`).
> "Split into separate **services / processes**" = network + data-ownership +
> deploy-topology boundaries; once interdependent, re-merging is
> disproportionately expensive → **R=3** (id f1 → `Fable 5.1 · max`). The
> frontier gate fixes the model (Fable 5.1) either way; the effort differs
> (R=2 → `ultracode`, R=3∧D=3 → `max`).

> **Codebase change vs. operational value.** A normal source-code change
> (component colour, text, CSS, any source line) is **R=1 by default** — the
> normal flow is PR review + deploy (that's the definition of R=1). R=2/R=3 only
> when the prompt explicitly points at a value that goes live **without** code
> review — a prod config file, a live admin panel, a feature-flag toggle, a DB
> setting. "Change the settings page's default theme" is assumed to be a
> codebase change → R=1.
> ✅ R=1: "Change this button's colour from blue to green" (id s1 → Haiku 4.5).
> ✅ R=2: "Turn on the new checkout flow for all users from the feature-flag
>    panel" (id s3 → Sonnet 5 · low — live operational value, not left to Haiku).

> **"One-line config" ≠ R=2 automatically.** Blast radius, not line length.
> Isolated operational value (one feature-flag default) → R=2. A line governing
> **system-wide** behaviour (retry count, timeout, rate limit, connection-pool
> size) where a wrong value causes a gradual outage (retry storm, connection
> exhaustion) before a human notices → **R=3** even as one line.
> ✅ R=3: "Bump `MAX_RETRIES` from 3 to 5 in the prod config" (id d5 → Sonnet 5 ·
>    low + human-review note).

### 10.3. D axis — worked pairs

> **D=1 / D=2 boundary — "well-documented" ≠ D=2.** How many independent design
> decisions are left to the implementer? One reasonable approach following a
> recipe/library → D=1. A real choice between >1 approach affecting the outcome
> → D=2.
> ✅ D=1: "Add cursor-based pagination to this API" (id r1 → Sonnet 5 · medium).
> ❌ D=2: "Add both cursor and offset pagination in a backward-compatible way,
>    decide when each is used" — two approaches + a constraint.
> When in doubt stay at D=1 — a "more than a one-liner" feeling is not grounds
> for D=2.

> **D=0 in non-coding.** Pure form/tone change with no content change is D=0
> regardless of length — even 3 paragraphs, if there's no choice/trimming/
> synthesis. ✅ "Rewrite these three paragraphs in a more formal tone" (id r2 →
> Haiku 4.5).

> **Fully-specified additive schema change = D=0.** Column name + type + nullable
> all given, no design decision. ✅ "Add a `last_login_at` column and make it
> nullable" (id n3 → Sonnet 5 · low — D=0 effort, but R=2 keeps it off Haiku).
> A schema change *with a choice* (index type, backfill strategy, constraint) is
> D=1.

> **Adversarial vulnerability hunting = D=3** (finding subtle logic errors —
> same family as a race-condition hunt or reconciling conflicting contract
> clauses). Holds even for a large defensive audit (still D=3 on depth, though
> it doesn't gate).
> ✅ D=3: "Review this single-file JWT validation module for security
>    vulnerabilities" (id f2 → Sonnet 5 · xhigh — W=0 so no ultracode).
> **Mechanical enumeration = D=1**, not D=3: "list which security-group rules
> allow 0.0.0.0/0 on ports other than 80/443" is a fixed-condition scan (id n2 →
> Sonnet 5 · medium). An open-ended "review this for security holes" is the D=3
> case — the phrasing decides.

### 10.4. opusplan — diagnostic & advanced combination

| Kind of difficulty | Example | opusplan? |
|---|---|---|
| Front-loaded: once the plan is done, execution repeats a pattern | "Migrate 40 services to a shared middleware, define the design once" | ✅ |
| Persistent: each execution step needs its own discovery | Race-condition hunt — cause unknown without reading the code | ❌ plain Opus 5 · max |
| Persistent: plan and execution inseparable | Formal correctness proof | ❌ |
| Insufficient volume (W≤1) | A small architectural decision, single-file impact | ❌ — mode switch is overhead |

**Execution verb may be unstated — the target-scope count is the signal.** "Design
X for 200 services", "define Y for 40 microservices" — the number implies the
execution phase exists. "Design" alone doesn't override front-loading.
✅ "Redesign the auth architecture of 200 prod services from scratch" (id d6/10 →
`opusplan · plan: max · execute: medium`).
❌ "Decouple this router's model selection from risk" (id 16 → plain Opus 5 ·
xhigh — W=1, and execution needed judgement too; live-tested in this project).

**opusplan output** adds two lines under `Claude:`:
```
Claude: opusplan · plan: <effort> · execute: <effort>
⚠️ Effort does not carry over — after switching to execution mode set it manually with /effort <execute effort>.
```
Plan effort = Rule 2(a)'s result (`xhigh`, or `max` if `R=3`). Execute effort =
post-plan estimated D (usually `medium`, rarely `high`). Opus 5 and Sonnet 5 are
both "hold"-free — the plan-mode effort **stays** on the switch to execution, it
doesn't drop automatically, hence the mandatory warning.

**Advanced combination (unverified, on-ask only — NOT auto-added).** If `W=3`,
`ultracode` on Sonnet 5 during the execution phase can be considered (apply the
migration in parallel). Untested in the official docs; suggest only if the user
asks "what else can I do?", with a "try it, fall back to plain `high`" note.

**opusplan is Claude Code only** — no equivalent on Claude.ai (the
`instructions.tr.md` derivative drops it entirely). Context-window detail: the
plan phase uses the `opus` setting's window; `opusplan[1m]` forces both phases
to 1M.

### 10.5. Step 4 rules — rationale

**Rule 1 (R=3 → human-review note).** Model/effort stay as Step 3 produced them;
a "Do not apply without human review." line is added. For simple-but-risky work
(D≤1) this is sufficient warning on its own — no need to raise the model.

**Rule 2 (prefer Opus 5 in three areas).** A partly-verified pattern from the
Opus 4.8 era. Opus 5's granular numbers (SWE-bench Pro / Terminal-Bench / HLE)
weren't published separately, but its overall jump over Opus 4.8 (>2x
Frontier-Bench, leading GDPval-AA/OSWorld) plus LiveBench 2026-06-25 (agentic
coding Opus 5 65.2 vs Sonnet 5 59.4) indicate the same-direction advantage.
(a) covers non-code structured design too (rule-engine, decision-tree,
system/prompt architecture). (c) tool-less: Sonnet 5's raw-intelligence gap
closes with tools (Opus 4.8-era: tool-less HLE Opus +6.6, tooled parity) — most
Claude Code work is "tooled", so (c) rarely fires.

**Rule 3 (D=3 outside Rule 2 → Sonnet 5 · xhigh default).** LiveBench 2026-06-25
shows Opus 5 above Sonnet 5 (agentic +5.8, language +13.7, reasoning +2.5, math
+2.8) — but Opus 5's cost-per-successful-task is ~1.4x Sonnet 5's, and the
difference doesn't justify every job. Escalate to Opus 5 · xhigh if the result
is insufficient or the work is critical (especially language/reasoning-heavy).
Do not route from an aggregate score — BenchAlign shows Sonnet 5 at #39 via a
coverage artefact (§2.1); LiveBench's full coverage keeps it at 76.0.

**Rule 4 (user knowledge).** Anthropic's Opus 5 advice: start `high`, `xhigh`
for coding/agentic, and use low/medium freely as a cost control "wherever your
eval holds up" — a departure from the Opus 4.7/4.8 "waste at low effort"
framing. The router still never emits Opus 5 below `xhigh` (it only picks Opus 5
at D=3); this note is for the user running Opus 5 manually.

**Rule 5 (`ultracode` ≥ 30 min).** It plans a workflow for every substantive
task; on everyday work that's latency + quota, not quality. One-off depth →
`ultrathink` in the prompt.

**Rules 6–8** (MCP tool-schema load, auto-accept geometric cost, `/model opus`
alias resolution) — see the one-liners in `SKILL.md` Step 4; full figures in §6
and §0.

### 10.6. Codex arm — notes

**What "Sol Ultra" actually is.** Ultra is a **product mode**, not an effort
value — `reasoning: {effort: "ultra"}` returns HTTP 400. Toggled in Codex
settings (Plus plans and up), runs ~4 collaborating agents in parallel. "Sol
Ultra" = `gpt-5.6-sol` with that mode on — not a separate model slug. It rides
on top of a normal effort level, so `Sol Ultra · effort: high` means "Sol, ultra
mode, high effort". Ultra is only meaningful on Sol — no Terra/Luna Ultra.
✅ "Run the security scan of 40 independent microservices at once, each on its
   own" — genuinely independent → Sol Ultra.
❌ "Break this monolith into modules" — pieces interdependent, one coherent
   design decision → plain Sol (Claude side goes to `opusplan` here — consistent:
   parallelisation is misleading on both sides).

**Sol → Sol Ultra diagnostic** (Codex analogue of `ultracode`; "independence" is
the key criterion). *Does the work split into 3+ separate pieces
(module/service/verification angle) that run unaware of each other and merge at
the end — or are the pieces interdependent, requiring one coherent design
decision?* If genuinely independent (and it already reached `D=3 → Sol`) → Sol
Ultra.

**`max` on Codex is real** (verified 2 Sep 2026). `openai.com/index/gpt-5-6/` +
the GA note: the GPT-5.6 effort ladder is `none, low, medium, high, xhigh, max`,
and `max` "is available to all users with access to GPT-5.6 in ChatGPT Work and
Codex and can be toggled on in settings". The
`learn.chatgpt.com/docs/config-file/config-reference` page is stale (lists only
to `xhigh`) — a doc lag. Caveat: some third-party gateways / CLI wrappers still
400 on `max` — if the user reports a 400, tell them to check tooling or fall
back to `xhigh`.

**`mode: pro` — Responses-API only, on-ask only (NOT auto-added).** `reasoning.mode:
"pro"` is a separate axis from effort (defaults to `medium` effort), confirmed
for the Responses API; no `model_reasoning_mode` key in the Codex CLI config
reference. If `max(D,C)=3` stayed on Terra (D<3 but the result is critical),
suggest it — "API-only, try it, fall back to standard mode" — only if the user
asks "what else can I do?".

**Codex human-review note:** `R=3` → same as Step 4 Rule 1, one shared note.
The MCP/auto-accept warnings (Rules 6/7) are **not** carried into the Codex arm —
Codex's tool-schema/session-cost mechanics were not verified.
