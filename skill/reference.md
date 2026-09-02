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
output. Not on Opus 4.7, runs at standard speed/price on Opus 4.6.

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
| "Design a new rate-limiter algorithm, consistent in a distributed system" | 2,3,1,1 | Opus 5 · xhigh *(algorithmic depth)* |

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
