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
> **Latest research pass: 10 September 2026 — Phase 2 (iteration-17).** Phase 2
> closed the benchmark-owner gaps Phase 1 could not reach (WebSearch was down for
> that pass), and made the path from a raw score to a routing rule mechanical:
> `benchmarks.json` is now a validated evidence store with stable record ids,
> `scripts/compile_benchmark_frontiers.py` derives `benchmark_frontiers.json`
> from it deterministically, and every benchmark-derived rule carries
> machine-readable provenance. **§15** is the architecture; **§12.5** is the
> Phase 2 research record; **§14.3** carries the vendor-bias ablation. The single
> routing consequence: the agentic-code / terminal-tool badge is now conditional
> on which Codex model is on the line.
>
> **Phase 1 research pass: 10 September 2026 (iteration-16).** The
> benchmark-aware routing engine landed in that pass. Its verified facts,
> corrections, open conflicts and explicit non-findings are in **§12**; the
> capability→benchmark map is **§11**; the efficiency data and the three
> dominance rules are **§13**; the `✅ RECOMMENDED AI` rationale and the
> ablation checks are **§14**. The raw evidence records — one row per
> benchmark×model×effort, with harness, tool access, dispersion, date, source
> and source tier — live in **`benchmarks.json`** next to this file.
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
| Price (input/output $/MTok) | $10/$50 | $5/$25 | **$2/$10*** | $1/$5 |
| Cache read ($/MTok) | **$0.25** (0.025x) | $0.50 | $0.30 | $0.10 |
| Effort support | low–max | low–max | low–max | **none** |
| Effort default | `high` (CC) / `medium` (chat) | `high` | `high` | — |
| Adaptive thinking | yes (always on) | yes | yes | no |
| Knowledge cutoff | **Jun 2026** | May 2026 | Jan 2026 | Feb 2025 |

*⚠️ **Corrected 10 Sep 2026.** Sonnet 5 is **$2/$10** and stays there. The
$2/$10 launch price was announced as introductory through 31 Aug 2026, but the
scheduled rise to $3/$15 on 1 Sep **was cancelled** and $2/$10 is now the
standard price (`platform.claude.com/docs/en/about-claude/pricing`, read
10 Sep 2026). Earlier iterations of this file said $3/$15 — that was wrong, and
it understated how quota-efficient Sonnet 5 is relative to Opus 5.
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

## 2.1. Independent leaderboards (2 Sep 2026) — ⚠️ STALE, superseded by §12

> **Status as of 10 September 2026: this whole section is historical.**
> `livebench.ai` returned no leaderboard table when re-read on 10 Sep 2026, so
> none of the LiveBench rows below could be re-verified, and the AA Intelligence
> Index figures here (66 / 63 / 62 / 60) come from an **older index version**
> than the current **v4.3** — Artificial Analysis states that scores are *not*
> comparable across index versions, so these numbers must never be mixed with
> the v4.3 figures in §13.1.
>
> The two rules this section used to carry (the Codex **+1 agentic-coding
> notch** and the **D=3 mid-tier default**) survive, but they are now grounded
> on **Terminal-Bench 4.0** and **AA Index v4.3** instead — see §11 and §12.
> The section is kept because iterations 13–15 were decided on it and the
> reasoning is still legible; it is no longer cited as live evidence.

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
   agentic coding** (Sol 56.2 < Sonnet 5 59.4 < Opus 5 65.2). The Codex arm's
   D=3→Sol mapping is correct (it's the whole tier that trails, not just Sol) →
   this is the basis of the Codex **+1 effort notch for agentic multi-step
   coding** (iteration-13). It's the *only* axis where the GPT-5.6 line is behind
   Claude — overall LiveBench Terra (max) 77.9 ≈ Sonnet 5 (xhigh) 76.0, and Sol
   ties Opus on reasoning/math.
5. **Terra (max) reasoning 90.6 / math 94.9 ≈ Sol (91.7 / 96.2)** and above
   Sonnet 5 (xhigh) (88.7 / 92.9). → **Rule 3 now mirrors onto the Codex arm**
   (iteration-14): D=3 *outside* Rule 2 (analytical / research / review) →
   **Terra**, not Sol, matching Claude's "stay on Sonnet 5" — the mid tier
   handles that work on both sides. Sol / Opus 5 stay the Rule-2 (agentic-coding
   / math / tool-less) pick and the "escalate if critical" target.
6. **GPT-6 Astra (3 Sep 2026) does not change any of the above** (iteration-15).
   Astra is not on the LiveBench 2026-06-25 board; the numbers that exist put it
   ≈ Opus 5 / Sol on intelligence (AA Index ≈ Sol, ~2–5 behind Fable 5.1) and
   **at parity on agentic coding** (DeepSWE 74.1 ≈ Opus 5 73.7; Codex Coding
   Agent Index 67 = Opus 5, behind Fable 5.1's 70). It leads clearly only on
   **computer use** (OSWorld V2 72.6 vs Sol 65.7; Mind2Web 1.9× faster). → Astra
   stays a **gated pick** (offensive-sec with Daybreak, 1000+ files, ≥1M corpus,
   computer-use), never the D=3 default — same discipline that keeps Fable 5.1
   gated on the Claude side. The one concrete effect: the Codex **+1 agentic-
   coding notch is Terra/Sol only, not Astra** — the gap it compensates for
   closes at Astra's tier. Full Astra writeup: §9.8.

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

> **`max` is a supported *setting* on every Claude tier, but the router only
> *emits* it on a flagship** (Opus 5 / Opus 4.8 / Fable 5.1 / Sol / Astra), and
> since iteration-16 only when Rule E3 also allows it (§13.2). The
> `D=3 ∧ R=3 → max` rule fires there; on a mid-tier model (Sonnet 5 / Terra) it
> stays `xhigh`. Rationale: the router picks the mid tier only when the reasoning
> need is *moderate* (D=3 outside Rule 2), so pairing it with `max` is
> incoherent and risks over-thinking (Anthropic's Sonnet 5 advice tops out at
> `xhigh`; OpenAI frames `max` as "high cost of failure" but the mid tier's
> practical ceiling is still `xhigh`). The `R=3` human-review note carries the
> stakes; if maximum reasoning is genuinely needed, escalate to the flagship.

### Advice per model (Anthropic's own text)

- **Opus 5:** start from `high` (default). Go to `xhigh` for coding/agentic work,
  to `max` for a genuine frontier problem. **"Use low and medium freely as a
  cost/speed control wherever your eval holds up."** — a deliberate tone shift
  from earlier Opus generations; low/medium is no longer a "restricted mode",
  it's a normal dial.
- **Sonnet 5:** `high` default. `xhigh` for the hardest coding/agentic work
  ⚠️ **Corrected 10 Sep 2026:** an earlier version of this file said Anthropic
  publishes no `max` guidance for Sonnet 5. It does — the effort page lists
  "**Max effort:** For tasks requiring the absolute highest capability with no
  constraints on token spending" for Sonnet 5. The router still never emits
  `Sonnet 5 · max`, but the reason is now the measured dominance in §13.2
  (Rule E1), not a missing vendor recommendation.
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
- ⚠️ **Corrected 10 Sep 2026:** it *can* be persisted. `code.claude.com/docs/en/model-config`
  lists an `ultracode` settings key and `CLAUDE_CODE_EFFORT_LEVEL=<level>`
  alongside `/effort ultracode` and `--effort ultracode` (the flag needs
  v2.1.203+). The earlier "per-session only" claim was wrong. Routing behaviour
  is unaffected.
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
| **Sonnet 5** (the $3/$15 rise was cancelled) | **$2.00** | **$10.00** | $2.50 | $0.20 |
| Haiku 4.5 | $1.00 | $5.00 | $1.25 | $0.10 |

**Fable 5.1 cache read:** **0.025x** of base input (every other model is 0.1x).
Long agentic sessions that re-read a cached prefix pay **¼** of the Fable 5 rate
— recommending Fable 5.1 at the frontier gate is markedly cheaper on quota than
the Fable 5 era. Batch: $5 / $25.

**Opus 5 / Sonnet 5 ratio: 2.5x** (corrected 10 Sep 2026 — it was recorded as
1.67x on the wrong $3/$15 assumption). For a subscription user this is a rough
proxy for how fast quota burns, and the correction *widens* the case for staying
on Sonnet 5 wherever the capability bar is met. It does **not** widen the case
for `Sonnet 5 · max`, which §13.2 Rule E1 shows is dominated by `Opus 5 · high`
on both quality and cost.

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

> **Note (10 Sep 2026):** the list below is the iteration-15 status. §12.3 and
> §12.4 supersede it for anything the 10 Sep pass touched — in particular the
> LiveBench rows referenced here could not be re-verified.

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

> The `→` column gives the **Claude** model·effort (Codex per the Codex mapping).
> It predates the `✅ RECOMMENDED AI` badge and deliberately does not show it —
> these rows exist to calibrate *scoring*, and the badge is computed afterwards
> from the capability profile (§11) and Step 6. Effort values here are still
> current except where Rule E3 (§13.2) narrows `max`; the `max` rows that remain
> below are all indivisible novel-design decisions, which E3 still allows.

Each row: prompt → R,D,W,C → model·effort. Non-coding areas are included too,
because SKILL.md's default reading drifts toward coding. If your own prompt
resembles one on this list, use that example's score as a starting point.

### Coding

The `→` column is the **Claude** answer. Codex model per §Codex-mapping, Codex
effort per Step 3 + the **+1 notch for agentic multi-step coding** (§10.6):
- "Merge 3 services onto a shared auth middleware" → Codex `Terra · xhigh`
  (D=2 → `high`, +1 for the migration).
- "Find and fix the race condition", "Design a new rate-limiter algorithm" →
  Rule 2 (agentic code / algorithmic) → Codex **Sol**; `xhigh` on the table, +1
  → `Sol · max` (Sol is a flagship, so `max` is allowed).
- "Split the monolith into 12 microservices" → Rule 2a, `D=3∧R=3` → Opus 5 · max
  / Sol · max (both flagships). But **state a 1000+ file count** ("split this
  6000-file monolith…") and the frontier gate fires on **both** arms → Fable 5.1
  / **Astra**, effort still `max`.
- "Review this JWT module" → D=3 **outside Rule 2**, sequential → Codex path (c)
  → **Terra**; analysis, no +1 → `Terra · xhigh` (mirrors `Sonnet 5 · xhigh`).
- The **+1 agentic-coding notch is Terra/Sol only** — if a gate puts the Codex
  model on **Astra**, no notch (Astra ties Opus 5 on coding, §9.8).

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
| "Review this single-file JWT validation module for security vulnerabilities" | 1,3,0,1 | Sonnet 5 · xhigh *(adversarial vuln hunt → D=3; W=0 → not ultracode; outside Rule 2, sequential → Sonnet 5 / **Codex Terra**, both `xhigh`)* |
| "These prod migration scripts run tonight with no review — check for silent data loss" | 3,3,1,2 | Sonnet 5 · xhigh / **Terra · xhigh** *(D=3 ∧ R=3 outside Rule 2 → mid-tier both sides; `max` is flagship-only → stays `xhigh`; + human-review note)* |

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

| Prompt | Gate | → (Claude / Codex) |
|---|---|---|
| "Categorise 1000 support tickets" | Volume | Haiku 4.5 / Luna · low |
| "Run a penetration test against this environment, build an exploit chain" | Offensive security | Opus 4.8 · xhigh / `use Claude` (standard) — `Astra · xhigh` with Daybreak Blue |
| "Audit this API code for auth-bypass vulnerabilities" | **NO gate** (defensive) → normal scoring | Sonnet 5 · xhigh / Terra · xhigh (Fable 5.1 & Astra can do it too) |
| "Optimise this protein-folding simulation code" | Biology-adjacent R&D | Fable 5.1 · high / `unverified — use Claude` |
| "Analyse an 800k-token log history" | Context >200k (Claude, eliminates Haiku); <1M so no Codex gate | Sonnet 5 / Terra, by C |
| "Split this 6000-file monolith into services" | Frontier scale (1000+ files) — both arms | Fable 5.1 · max / **Astra · max** + review note |
| "Load this whole 1.2M-token repo and map every call site" | ≥1M corpus (Codex) | Sonnet 5 (by C) / **Astra** |

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

### 9.1. Model family — GPT-5.6 (Sol, Terra, Luna) + GPT-6 Astra

GPT-5.6 went to general availability on 9 July 2026. Sol is the GPT-5.6 flagship,
Terra the balanced mid-tier, Luna the speed/cost-focused budget model — verified
directly from the official launch page.

**GPT-6 Astra** (`gpt-6-astra`, 3 Sep 2026) sits above Sol as OpenAI's new
flagship. Sol / Terra / Luna all remain — the Codex model picker now shows four
tiers, and the Codex CLI default is **Luna** (not Astra). Astra is a **narrow
router pick** — see §9.8 for the full writeup and §2.1 item 6 for why it does not
become the D=3 default.

**Sol Ultra:** introduced 26 June 2026, GA on 9 July. A **product mode** (not a
model, not an effort value — `effort: "ultra"` returns HTTP 400), toggled in
Codex settings on **Plus plans and up** (Pro/Enterprise in ChatGPT Work).
Instead of a single reasoning chain it decomposes the task into ~4 collaborating
agents that communicate in real time (more in "multiagent v2" mode). "Sol Ultra"
= `gpt-5.6-sol` with the mode on. Context window **43% larger** than GPT-5.5
(~1.5M tokens — single-source claim, couldn't be confirmed directly from the
official page).

### 9.2. Pricing (per MTok) — after the 30 July 2026 price cut

| Model | Input | Output | Cache read |
|---|---|---|---|
| **Astra** (GPT-6, 3 Sep 2026) | $10.00 | $50.00 | $1.00 |
| Sol | $5.00 | $30.00 | — |
| Terra | $2.00 | $12.00 | — |
| Luna | $0.20 | $1.20 | — |

**Astra:** ~2.5× Sol's headline rate, cache write $12.50. **2× all rates above
272k input tokens** (whole request). Batch / Flex 50% off; Fast Mode 2×. But
Astra is **~70% more token-efficient** than Sol — roughly ⅓ of Sol's tokens at
`max` in the Codex harness, ~⅕ of Opus 5's at `xhigh` — so on a coding task
Artificial Analysis puts its cost-per-task ≈ Sol (max), and ~$2.6 vs Fable 5's
~$6. The router still treats it as the quota-heavier option (higher headline
rate, and long-context work blows past the 272k 2× line) → gated pick, not
default.

**The user's report was stale:** it said Terra $2.50/$15, Luna $1/$6 — those are
the pre-30-July prices. On that date OpenAI cut Luna 80%, Terra 20%, Sol
unchanged. Output price is **6x** input on all three models (fixed ratio).

### 9.3. Effort / reasoning mechanics — three separate things

The report described a single linear ladder
"Instant→Low→Medium→High→Extra High→Max→Ultra". It's actually **three separate
things**:

1. **`reasoning.effort`** — supported values **`none, low, medium, high, xhigh,
   max`** (re-verified 3 Sep 2026 against
   `developers.openai.com/api/docs/guides/latest-model` +
   `learn.chatgpt.com/docs/models`). **`minimal` is gone** — earlier docs / this
   file listed `none, minimal, low, …`; the current ladder has no `minimal` rung
   (the router dropped it in iteration-12; ex-`minimal` cases → `low`).
   - **Official guidance:** *"Use `medium` as a balanced starting point and `low`
     for latency-sensitive workloads."* `medium` is the **coding/development
     default**; `low` is for *"quick, well-scoped tasks"* / *"narrow tasks with
     clear requirements and limited impact"*; `none` = no reasoning. → This maps
     rung-for-rung onto the D scale, so **both arms start from one `D → effort`
     table**: `0→low · 1→medium · 2→high · 3→xhigh`, `D=3 ∧ R=3 → max`.
   - **Codex modifier — +1 notch for agentic multi-step coding** (iteration-13).
     LiveBench §2.1 puts the whole GPT-5.6 line behind Claude on agentic coding
     (Sol 56.2 < Sonnet 5 59.4 < Opus 5 65.2) and *nowhere else*. So when the
     task is writing/restructuring code across multiple dependent steps
     (multi-file feature, refactor, migration, architecture implementation,
     codebase-spanning debug-and-fix), the Codex effort is bumped one rung above
     the table (capped at `max`); Claude is unaffected. Not for code review /
     vuln analysis / reading-to-answer, non-code design, or mechanical
     cross-file repetition. In practice this bites at D=2–3 coding-build tasks
     (e.g. d2 auth→OAuth2: Claude `high` / Codex `xhigh`).
   - **UI name drift:** the Codex app / ChatGPT Work / IDE label `low` as
     **"Light"**; the CLI and API say `low`. Same rung.
   - **`max` — ⚠️ conflicting sources, re-checked 10 Sep 2026.**
     `learn.chatgpt.com/docs/models` now states plainly: *"All models support:
     Low/Light, Medium (default), High, and Extra High. **Astra and Sol
     additionally offer Max and Ultra modes**"* — i.e. `max` is **not** available
     on Terra or Luna. The earlier reading of the API model-guidance page put the
     full ladder on all three tiers, and Artificial Analysis still publishes a
     `Terra (max)` row. Unresolved; see §12.3. **Routing impact: none in
     practice** — the router already never emitted `Terra · max`, and under the
     stricter reading that restraint becomes a hard capability limit rather than
     a preference. Some third-party gateways also 400 on `effort: "max"` — a
     separate tooling gap.
   - **GPT-6 Astra effort:** same ladder **minus `none`** (`none` is rejected at
     the API layer). Codex CLI config default `model_reasoning_effort = "high"`;
     OpenAI / community guidance is "start at `medium`" for agentic coding and
     research, `high` for complex debugging, `xhigh` / `max` only for hard
     architecture or difficult debugging loops — same shape as the shared table.
     `max` is generally available across paid plans; one source reports Chat
     Completions capping at `xhigh` with `max` on the Responses API — treat as
     the same "if a surface 400s, fall back to `xhigh`" caveat as Sol. `temperature`,
     `top_p`, `logprobs` unsupported. Needs Codex CLI **v0.153.0+**.
   - **Why the ladder was shifted up one rung (iteration-12):** the skill owner
     reported from field use that `Terra · low` is materially weaker than
     `Sonnet 5 · medium` (the Claude D=1 pick) — "hatalı işlemler", not an
     equivalent. OpenAI's own guidance agrees: `low` is not for normal dev work.
     Options weighed: (A) raise Terra's effort, (B) `Luna · high` instead of
     `Terra · low`. Chose **A** — Vellum / layer3labs / official all say Luna is
     "for volume, not depth" (long-context recall collapses to ~41% vs Sol ~91%),
     so `Luna · high` is unsafe for exactly the D≥1 codebase work where
     `Terra · low` was failing.
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
- **`reasoning.effort` ladder is `none, low, medium, high, xhigh, max`** (no
  `minimal` — re-verified 3 Sep 2026, `developers.openai.com/api/docs/guides/latest-model`
  + `learn.chatgpt.com/docs/models`). `medium` = coding default, `low` =
  quick/well-scoped/latency-sensitive only, `none` = no reasoning. `max` on every
  GPT-5.6 tier. Both arms start from **one `D → effort` table**: `0→low ·
  1→medium · 2→high · 3→xhigh`, `D=3 ∧ R=3 → max`. Codex then adds **+1 notch for
  agentic multi-step coding** (iteration-13, capped at `max` — the one axis
  LiveBench §2.1 shows the GPT-5.6 line behind Claude). See §9.3 for both.
- **`ultra` is a product mode, not an effort value** — `effort: "ultra"` → HTTP
  400. Codex Plus+ toggle, ~4 parallel agents. "Sol Ultra" = `gpt-5.6-sol` +
  ultra mode. Sub-agent config keys: `agents.default_subagent_model`,
  `agents.default_subagent_reasoning_effort`, `agents.max_concurrent_threads_per_session`,
  `agents.max_threads`.
- `reasoning.mode` (`standard`/`pro`) is a separate axis from effort — confirmed
  for the Responses API only (no `model_reasoning_mode` key in the Codex CLI).
- Codex CLI model selection: `--model`/`-m` flag, `model` key in `config.toml`.
- **GPT-6 Astra** (`gpt-6-astra`, 3 Sep 2026) — §9.8. Slug, 1.05M context, Apr
  2026 cutoff, $10/$50, effort ladder minus `none`, Codex CLI v0.153.0+, four-tier
  picker with Luna as CLI default — all official (`developers.openai.com/api/docs/models/gpt-6-astra`).
- **Codex cyber behaviour is now partly known** (was fully "not researched").
  GPT-6 Astra is at OpenAI's **"Critical"** cyber Preparedness level: standard
  access does defensive vuln *discovery* but **hard-stops** exploit / PoC
  generation (the task ends, no approval prompt); the **Daybreak (Blue)**
  programme (API-key-level, application-gated) lifts that for authorised
  researchers. → the Codex offensive-security gate now says `use Claude` for
  standard access and routes to **`Astra · xhigh`** when the user states Daybreak
  access. (`deploymentsafety.openai.com/gpt-6-astra`, Codex KB integration guides.)

**❌ Debunked (the report was wrong):**
- Terra/Luna's old prices ($2.50/$15, $1/$6).
- The one-dimensional "Instant→...→Ultra" ladder — actually effort (`none`…`max`)
  + a separate `mode` axis (`standard`/`pro`, API-only) + a separate product mode
  (`ultra`, not an effort value).
- (Earlier version of this file) "`max` unverified in the Codex CLI, use `xhigh`
  as the ceiling" — `max` was confirmed as a Codex toggle on 2 Sep 2026; the
  ceiling is now `max`.
- (Earlier version) the `none, minimal, low, …` ladder and the `D → effort` map
  `0→minimal · 1→low · 2→medium · 3→high` — `minimal` does not exist in the
  current ladder, and `1→low` put real dev work below OpenAI's own `low`
  threshold. Corrected in iteration-12 to the shared table `0→low · 1→medium ·
  2→high · 3→xhigh` (see §9.3).

**⚠️ Could not be verified / not researched — did not enter the router:**
- Whether Codex/ChatGPT has a safety-classifier/fallback chain like Claude's for
  **biology-adjacent** content. Astra's system card is cyber-only (re-checked
  8 Sep 2026) — so the Codex arm still says "unverified — use Claude" for
  biology-R&D. (The cyber side is now partly known — see the ✅ list.)
- ~~Whether Ultra mode / parallel subagents run on `gpt-6-astra`~~ —
  **resolved 10 Sep 2026**: they do (`learn.chatgpt.com/docs/models`).
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

## 9.8. GPT-6 Astra — 3 September 2026 (iteration-15)

> **Source status:** researched 8 Sep 2026 via `developers.openai.com/api/docs/models/gpt-6-astra`,
> `deploymentsafety.openai.com/gpt-6-astra` (system card), `openai.com/index/gpt-6-astra/`,
> Artificial Analysis, and the Codex Knowledge Base integration guides. Same
> discipline as every other entry: benchmark numbers confirm *direction* only,
> the router never selects Astra from a score.

**Identity.** `gpt-6-astra`. OpenAI's new flagship, above GPT-5.6 Sol. Sol /
Terra / Luna all remain (four-tier Codex picker). "Our most capable model, built
for the hardest end-to-end work." One snapshot, **no mini/nano sub-tiers**.

**Specs.**
- Context **1,050,000 tokens** (≈922k input / 128k output). Knowledge cutoff
  **30 April 2026**.
- Effort `low, medium, high, xhigh, max` — **`none` rejected at the API**. Codex
  CLI default `high`; "start at `medium`" is the common guidance. `max` generally
  available on paid plans (one source: Responses-API-only, Chat Completions caps
  at `xhigh`).
- Price $10 / $50 MTok, cached-in $1, cache-write $12.50. **2× all rates above
  272k input tokens.** Batch / Flex 50% off; Fast Mode 2×.
- **~70% more token-efficient than Sol** (~⅓ of Sol's tokens at `max` in the
  Codex harness, ~⅕ of Opus 5's at `xhigh`) — so per-task cost is far closer to
  Sol than the headline suggests (AA: coding cost-per-task ≈ Sol max; ~$2.6 vs
  Fable 5 ~$6).
- Codex CLI **v0.153.0+**. Not in the in-session model picker by default (manual
  config / staged rollout). ChatGPT: **Plus, Pro, Business, Enterprise** (not
  Free); picker label "GPT-6 Pro". Also on the API, Azure, Bedrock.

**Benchmarks (direction only).**
| Axis | Astra | Comparators | Read |
|---|---|---|---|
| Computer use — OSWorld V2 | **72.6%** | Sol 65.7 | Clear Astra win; task time 75→40 min; Mind2Web 1.9× faster |
| Terminal-Bench 4.0 | 57.7% | Fable 5.1 55.8 | Marginal |
| DeepSWE v1.1 (SWE-bench-like) | 74.1% | Sol 72.7 · Opus 5 73.7 · Gemini Flash 73.8 | Inside the pack — parity |
| Codex Coding Agent Index | 67 | Opus 5 67 · **Fable 5.1 (Claude Code) 70** | Ties Opus 5, behind Fable 5.1 |
| AA Intelligence Index | ≈ Sol | ~2–5 behind Fable 5.1 | Two index versions, same direction |
| AA-Omniscience hallucination | 92% → **51%** | — | Big improvement |
| GDPval-AA v2 | **~80 Elo regression** | — | Worse — consistent with §2's "GDPval not used" |

→ Astra is a **flagship that is not clearly ahead of Claude's flagships.** It
wins on computer use and is at parity elsewhere. This is exactly the profile
that keeps a model **gated** rather than default (cf. Fable 5.1 vs Opus 5).

**Cyber — "Critical" (first model OpenAI has placed at this Preparedness level).**
- The model "can locate previously unknown vulnerabilities and develop working
  exploits across hardened systems without per-step human guidance" (found two
  zero-day V8 bugs, built browser/OS exploits during evals).
- **Default access:** defensive vulnerability *discovery* works (~66.7% task
  completion — like Fable 5.1's carve-out); exploit / PoC *generation* is
  **refused** (~2.4%), and a cyber safety check **ends the task outright** rather
  than pausing for approval. Misalignment monitoring runs across all tool-using
  inference — non-trusted users report occasional pauses/blocks, sometimes on
  unrelated work.
- **Elevated access:** the **Daybreak (Blue)** programme — "reduced cybersecurity
  refusals for authorised security researchers", granted at the **API-key
  level**, application-gated. **Trusted Access** = the staged-rollout enrolment.
- **No bio / CBRN threshold** crossed or documented — the card is cyber-only.

**Router treatment (conservative — iteration-15).**
1. **Offensive-security gate (Codex arm):** was a blanket "unverified — use
   Claude". Now: standard access **hard-stops** → `use Claude`; **Daybreak Blue
   access stated → Astra · `xhigh` floor** (mirrors Mythos 5.1 / Glasswing on the
   Claude side). Defensive work is unchanged — normal scoring, no gate.
2. **New Codex frontier gate:** 1000+ files / whole-codebase → **Astra** (mirror
   of the Claude Fable 5.1 gate; Astra has the only verified ≥1M Codex window).
   Wins over the D=3 mapping incl. path (a) — no `Sol Ultra` at that scale.
3. **≥ ~1M-token corpus on the Codex side → Astra** (only verified large window;
   mind the 272k 2× surcharge).
4. **Escalation ceiling** above Sol in the D=3 paths (b)/(c) — but only for
   genuinely long-session complex work with stated Astra access, not a reflex.
5. **`max` flagship list** gains Astra (Opus 5 / Opus 4.8 / Fable 5.1 / Sol /
   Astra).
6. **+1 agentic-coding notch does NOT apply on Astra** — parity with Opus 5 on
   DeepSWE / Coding Agent Index means the gap the notch compensates for is gone.
7. **Biology-adjacent → still "unverified — use Claude"** — Astra's card is
   cyber-only, re-checked 8 Sep 2026.

**Codex product changes shipped with Astra (context, not routing):**
context-notes architecture replaces compaction — running notes kept across
context windows, earlier windows stay searchable, long agent runs stop losing
failure detail (behind a `config.toml` flag, becoming default). Async "ask" —
Astra continues work that doesn't depend on your reply, waits only on
consequential decisions.

**Not verified / left out:** ~~whether Ultra mode / parallel subagents run on
`gpt-6-astra`~~ — **resolved 10 Sep 2026**: `learn.chatgpt.com/docs/models` says
"Astra and Sol additionally offer Max and Ultra modes", so Ultra **does** run on
Astra. The router's path (a) still names `Sol Ultra` because Sol is the D=3
parallel pick; Astra is reached by gate, and no Astra gate currently coexists
with path (a). Still open: exact LiveBench rows for Astra (not on the 2026-06-25
board); which ChatGPT-plan users hit the cyber monitor hardest.

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

**Why the Codex offensive gate is "use Claude", now with a Daybreak exception
(iteration-15).** Before GPT-6 Astra, the Codex side had no researched safety
behaviour here, so it declined ("unverified — use Claude"). Astra's system card
resolves it: standard Codex / ChatGPT access does defensive vuln *discovery* but
**hard-stops** exploit / PoC generation — the cyber safety check ends the run, it
does not pause for approval, so pointing a standard user at Astra for pen-test
work just wastes the turn. The **Daybreak (Blue)** programme (API-key-level,
application-gated, "reduced cybersecurity refusals for authorised security
researchers") is the elevated tier — structurally the same as Claude's
Glasswing / Mythos 5.1. So: **standard → `use Claude`; stated Daybreak access →
`Astra · xhigh`** (floor, W/duration can't raise it — `ultracode` is Claude
Code-only, Astra's own ceiling is `max`). Defensive work never gates on either
arm.

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

**The Codex arm now has a frontier gate too (iteration-15).** Before GPT-6 Astra
there was no Codex model with a verified large window, so the Codex side had no
analogue — a 6000-file monolith split routed to `Sol · max` with no
acknowledgement of scale. Astra has a **verified 1.05M context** and is pitched
at "the hardest end-to-end work", so 1000+ files / whole-codebase / "load the
whole repo at once" / ≥~1M-token corpus → **Astra** on the Codex side, matching
the Claude Fable 5.1 gate. It's a *deciding* gate: it wins over the D=3 mapping,
including path (a), because Ultra mode is Sol-only — at 1000+ scale you take
Astra and lose the parallel-agents primitive. Mind the **272k 2× price line** —
frontier work sails past it. 100–999 files → normal Codex scoring (W=3), same as
Claude.

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

**Rule 3 (D=3 outside Rule 2 → mid-tier · xhigh default — both arms).** LiveBench
2026-06-25 shows Opus 5 above Sonnet 5 (agentic +5.8, language +13.7, reasoning
+2.5, math +2.8) — but Opus 5's cost-per-successful-task is ~1.4x Sonnet 5's, and
the difference doesn't justify every job. **iteration-14 mirrors this onto the
Codex arm:** the old Codex mapping sent *every* D=3 to Sol; now D=3 outside Rule
2 (analytical / research / single-artefact review) → **Terra** — Terra (max)
reasoning 90.6 / math 94.9 ≈ Sol (91.7 / 96.2) and above Sonnet 5 xhigh, so the
mid tier is the right call on both sides. Sol stays the Rule-2 pick (agentic
coding — where the GPT-5.6 line *does* trail — plus math / tool-less) and the
"escalate if the result is insufficient or the work is critical" target
(· `xhigh`, or `max` at R=3 since Sol/Opus 5 are flagships). Do not route from an
aggregate score — BenchAlign shows Sonnet 5 at #39 via a coverage artefact
(§2.1); LiveBench's full coverage keeps it at 76.0.

**`max` (from `D=3 ∧ R=3`) is flagship-only (iteration-14).** The rule means
"irreversible + hard → deepest reasoning", but the router picks the *mid* tier
(Sonnet 5 / Terra) only when the reasoning need was assessed as *moderate* (D=3
outside Rule 2) — so `Sonnet 5 · max` / `Terra · max` is an incoherent pairing
and courts over-thinking without adding safety. Both vendors' mid-tier tuning
advice tops out at `xhigh` (Anthropic explicitly; OpenAI frames `max` as "high
cost of failure" but that's the escalate-to-flagship signal). So at `D=3 ∧ R=3`:
flagship model → `max`; mid-tier model → `xhigh` + the R=3 review note. The user
can still set `max` by hand. Before iteration-14 the router could emit
`Sonnet 5 · max` / `Terra · max` (rule-valid but untested and unwanted); it no
longer does. The flagship list that may carry `max` is Opus 5 / Opus 4.8 /
Fable 5.1 / Sol / **Astra** (Astra added iteration-15).

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

**Effort ladder (iteration-12).** The Codex `D → effort` map was
`0→minimal · 1→low · 2→medium · 3→high`. Field report from the skill owner:
`Terra · low` is materially worse than `Sonnet 5 · medium` on real D=1 dev work
("hatalı işlemler", not equivalent). OpenAI's own guidance
(`developers.openai.com/api/docs/guides/latest-model`,
`learn.chatgpt.com/docs/models`) backs this: `medium` is the coding default,
`low` is for *"quick, well-scoped, latency-sensitive"* work only, and `minimal`
is no longer a rung. So the ladder shifted up one: **`0→low · 1→medium ·
2→high · 3→xhigh`, `D=3 ∧ R=3 → max` (Sol only — iteration-14)** — otherwise
identical to the Claude arm's table.
`Luna · high` was rejected as the alternative fix (Vellum / layer3labs / official
all: Luna is "for volume, not depth"; its long-context recall drops to ~41% vs
Sol ~91%, unsafe for D≥1 codebase work). `Terra · low` now appears only for D=0
work (rename, tone-only rewrite, fully-specified schema change) and the volume
gate (`Luna · low`).

**+1 notch for agentic multi-step coding (iteration-13).** After iteration-12 the
two effort columns were byte-identical on every eval row, which raised the fair
question of what the dual arm is *for* if not the effort. The honest answer:
model-tier selection and the gate divergence (offensive → Opus 4.8 vs
"unverified"; biology / frontier → Fable 5.1 vs normal scoring; `opusplan` /
`ultracode` vs `Sol Ultra`) were always the substance — the effort convergence
removed a *false* distinction (the old ladder was mis-derived, not deliberately
different). But there **is** one real, cited asymmetry: LiveBench §2.1 puts the
whole GPT-5.6 line behind Claude on agentic coding (Sol 56.2 < Sonnet 5 59.4 <
Opus 5 65.2) and nowhere else. So the router adds **+1 Codex effort notch when
the task is agentic multi-step coding** — writing/restructuring code across
dependent steps (multi-file feature, refactor, migration, architecture
implementation, codebase-spanning debug-and-fix). Capped at `max`; Claude
untouched. **Excludes** code review / vuln analysis / reading-to-answer (that's
analysis — `f2`, `5b` stay level), non-code design, and mechanical cross-file
repetition (width, not depth). In the current eval set only **d2** moves
(Claude `high` / Codex `xhigh`); `§8` rows "Merge 3 services onto a shared auth
middleware", "Find and fix the race condition", "Design a new rate-limiter
algorithm" would also take the bump on the Codex side. This is a deliberate
product choice (the skill owner asked for the effort column to carry a
distinction); it is loosely — not strongly — benchmark-backed, and it is the
*only* effort difference between the arms.

**Codex model mapping at D=3 — Rule 3 mirror + `max` cap (iteration-14).** Two
inconsistencies surfaced by a real output (`Claude: Sonnet 5 · max` /
`Codex: Sol · max` for a D=3 ∧ R=3 review task):
1. The old Codex mapping sent **every** D=3 to Sol — no equivalent of the Claude
   arm's Rule 3 ("D=3 outside Rule 2 → stay on Sonnet 5, quota default"). So the
   Claude arm protected quota while the Codex arm jumped to the flagship for the
   same analytical work. Fixed: the D=3 row is now an ordered check —
   **(a)** 3+ already-independent parallel targets → Sol Ultra; **(b)** Rule 2
   territory (agentic coding / math / tool-less) → Sol; **(c)** otherwise
   (analytical / research / single-artefact review) → **Terra** (LiveBench
   reasoning 90.6 / math 94.9 ≈ Sol; escalate to Sol · `xhigh` if critical).
   Only `f2` moved in the eval set (`Sol · xhigh` → `Terra · xhigh`); a new eval
   `m1` locks in the D=3 ∧ R=3-outside-Rule-2 case.
2. `Sonnet 5 · max` / `Terra · max` were rule-valid (the `D=3 ∧ R=3 → max` rung
   applied to any model) but in neither vendor's mid-tier tuning advice. Fixed:
   `max` is flagship-only (see §10.5 and §3). `Terra · max` and `Sonnet 5 · max`
   are no longer producible by the router.

**What "Sol Ultra" actually is.** Ultra is a **product mode**, not an effort
value — `reasoning: {effort: "ultra"}` returns HTTP 400. Toggled in Codex
settings (Plus plans and up), runs ~4 collaborating agents in parallel. "Sol
Ultra" = `gpt-5.6-sol` with that mode on — not a separate model slug. It rides
on top of a normal effort level, so `Sol Ultra · effort: xhigh` means "Sol, ultra
mode, xhigh effort". Ultra is only meaningful on Sol — no Terra/Luna Ultra.
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

**`max` on Codex is real** (verified 2 Sep 2026; re-confirmed for Astra 8 Sep).
`openai.com/index/gpt-5-6/` + the GA note: the GPT-5.6 effort ladder is
`none, low, medium, high, xhigh, max`, and `max` "is available to all users with
access to GPT-5.6 in ChatGPT Work and Codex and can be toggled on in settings".
GPT-6 Astra keeps the ladder minus `none`. The
`learn.chatgpt.com/docs/config-file/config-reference` page is stale (lists only
to `xhigh`) — a doc lag. Caveat: some third-party gateways / CLI wrappers still
400 on `max`, and one source has Astra's `max` as Responses-API-only — if the
user reports a 400, tell them to check tooling or fall back to `xhigh`. The
router only *emits* `max` on a flagship (Opus 5 / Opus 4.8 / Fable 5.1 / Sol /
Astra); mid-tier caps at `xhigh`.

**`mode: pro` — Responses-API only, on-ask only (NOT auto-added).** `reasoning.mode:
"pro"` is a separate axis from effort (defaults to `medium` effort), confirmed
for the Responses API; no `model_reasoning_mode` key in the Codex CLI config
reference. If `max(D,C)=3` stayed on Terra (D<3 but the result is critical),
suggest it — "API-only, try it, fall back to standard mode" — only if the user
asks "what else can I do?".

**Codex human-review note:** `R=3` → same as Step 4 Rule 1, one shared note.
The MCP/auto-accept warnings (Rules 6/7) are **not** carried into the Codex arm —
Codex's tool-schema/session-cost mechanics were not verified.

**GPT-6 Astra — when the router picks it, and when it doesn't (iteration-15).**
Full specs / benchmarks / cyber-tier detail in §9.8. Routing summary:
- **Picked** only via a gate: (1) offensive-security *with stated Daybreak Blue
  access* → `Astra · xhigh`; (2) 1000+ files / whole-codebase → `Astra` (new
  Codex frontier gate, mirrors Fable 5.1); (3) ≥~1M-token corpus / "whole repo
  at once" → `Astra`; (4) as the escalation ceiling above Sol in D=3 paths
  (b)/(c), but only for genuinely long-session complex work with stated access.
- **Not picked** as the D=3 default (that's still Sol / Terra per the mapping),
  and never *just because the task is hard* — Astra's intelligence and coding
  indices sit ≈ Opus 5 / Sol and behind Fable 5.1 (§9.8 table); it leads only on
  computer use. Same discipline that keeps Fable 5.1 gated on the Claude side.
- **`max` list:** Astra joins Opus 5 / Opus 4.8 / Fable 5.1 / Sol as a flagship
  the router may emit `max` on. Caveat: a source reports `max` as Responses-API-
  only for Astra (Chat Completions caps at `xhigh`) — treat like the Sol `max`
  400 caveat, fall back to `xhigh` if a surface rejects it.
- **+1 agentic-coding notch: never on Astra.** DeepSWE 74.1 ≈ Opus 5 73.7 and
  Coding Agent Index 67 = Opus 5 — the GPT-5.6-line gap the notch compensates for
  (Sol 56.2 < Sonnet 5 59.4) is closed at Astra's tier. The notch stays for
  Terra / Sol.
- **Defensive vuln discovery** works on Astra by default (~67% task completion,
  like Fable 5.1's carve-out) — only exploit / PoC generation is refused without
  Daybreak. If the user picks Astra, mention that the misalignment monitor can
  pause unrelated work for non-trusted accounts.
- **Biology-adjacent → still `unverified — use Claude`** — Astra's card is
  cyber-only (re-checked 8 Sep 2026).
- **Ultra + Astra:** undocumented — no "Astra Ultra" asserted; `Sol Ultra`
  language unchanged.

---

## 11. Capability → benchmark map (iteration-16)

> **Why this section exists.** Before iteration-16 the router scored a prompt on
> R/D/W/C and stopped. R/D/W/C describes *scope and stakes* very well and
> *nothing about what kind of ability the work needs* — "depth 3" is true of a
> race-condition hunt, a topology proof and a contract-conflict review alike,
> and those three want different models. Step 2 of `SKILL.md` now names the
> capability first; this section is the full map behind that table, including
> which benchmarks are deliberately **excluded** for each tag. Raw records with
> harness/effort/date/source: `benchmarks.json`.

### 11.1. The tags, in full

| Tag | Counts | Primary evidence | Explicitly **excluded** |
|---|---|---|---|
| `agentic-code` | multi-file implementation, code generation at scale, refactor, migration, feature build, debug-and-fix across files, repository navigation | Terminal-Bench 4.0 · CursorBench 3.2.0 · DeepSWE v1.1 (tier C) | HLE, GDPval, OSWorld, AA-LCR |
| `terminal-tool` | terminal/CLI use, build-and-test loops, tool orchestration, long-horizon autonomous execution | Terminal-Bench 4.0 | CursorBench (IDE scaffold, different failure modes) |
| `deep-reasoning` | architecture from scratch, algorithm design, mathematics and formal proof, tool-less analysis, adversarial correctness hunting | HLE (tool-less **and** tooled rows, they differ) · AA Index Scientific Reasoning category | **All coding benchmarks weight ~0 here.** This is the single most important exclusion in the map |
| `knowledge-work` | produce a finished document, spreadsheet, deck, memo, filing, model | GDPval-AA v2 | Terminal-Bench, SWE-style benchmarks |
| `research-synthesis` | multi-source research, web search, following up on findings, reconciling sources | AA-Omniscience + AA-Briefcase (via AA Index) | Coding benchmarks |
| `long-context` | read/map/summarise a large corpus; reason across a full window | AA-LCR v1.1 (via AA Index) **plus the hard context-window spec**, which is a gate not a score | Aggregate index (a model can win the index and still lack the window) |
| `computer-use` | drive a browser or desktop GUI end-to-end, click through an app, screenshots | OSWorld — **always state version and scoring mode** | Everything else; see §12.3 for why this row is low-confidence |
| `science` | genomics, chemistry, physics, research engineering, lab pipelines | Terminal-Bench-Science 0.1 (publishes SE) · CritPt (via AA Index) | General coding benchmarks |
| `workflow-automation` | wire up business workflows, integrations, multi-tool orchestration | AutomationBench | — |
| `doc-data-understanding` | scanned documents, PDFs, dense charts, nested tables, multimodal extraction | *none cross-ecosystem* — vendor vision claims only | — |
| `parallel-independent` | 3+ targets genuinely unaware of each other, merging at the end | *product mechanism, not a benchmark*: `ultracode` (one orchestrated chain) vs Ultra mode (~4 collaborating agents) | Any benchmark. This tag never outranks a benchmark-backed tag — see the tie-break in `SKILL.md` Step 6 |
| `latency-volume` | sub-second response, high-throughput bulk classification/parsing | AA Index output-speed and cost/task columns | Intelligence scores — the bar is "clears it", not "wins" |
| `instruction-following` | rigid format/schema compliance | folded into the dominant tag | never dominant alone |

### 11.2. Where the requested capability list landed

The upgrade brief named 21 capability categories. They are all covered; several
collapse onto one tag because no benchmark distinguishes them:

agentic software engineering · multi-file implementation · code generation ·
debugging · repository navigation → **`agentic-code`** ·
terminal / CLI tool use · tool use / orchestration → **`terminal-tool`** (+
`workflow-automation` when the tools are business systems rather than a shell) ·
architecture / system design · deep reasoning · mathematics / formal reasoning →
**`deep-reasoning`** · instruction following → **`instruction-following`**
(folded) · knowledge work → **`knowledge-work`** · research / multi-source
synthesis → **`research-synthesis`** · long-context comprehension →
**`long-context`** · document/data understanding → **`doc-data-understanding`** ·
computer use / GUI interaction · multimodal reasoning → **`computer-use`** /
**`doc-data-understanding`** (multimodal splits by what the task *does* with the
image) · science → **`science`** · cybersecurity → Step 1 gate (offensive) or
`deep-reasoning` + scale tag (defensive) · independent parallel workstreams →
**`parallel-independent`** · latency / high-volume processing →
**`latency-volume`**.

### 11.3. Weighting, in practice

Pick the **one or two dominant** tags and ignore the rest. A tag is dominant
when removing it would change what "done" means. Worked examples:

- *"Refactor auth across 300 files, run the tests, fix what breaks"* →
  `agentic-code` (dominant) + `terminal-tool` + width. `deep-reasoning` is
  present but secondary; `knowledge-work` and `computer-use` are zero.
- *"Prove this scheduling bound or find a counterexample, from the definitions
  given here"* → `deep-reasoning` alone. **Terminal-Bench and CursorBench weigh
  zero.** This is the case the old router could not express: it scored D=3 and
  then reached for evidence about code agents.
- *"Reconcile 60 scanned invoices against the ledger"* →
  `doc-data-understanding` + `long-context`. Evidence-poor: say so.

---

## 12. Comparability record — research pass of 10 September 2026

Source hierarchy used: **Tier A** vendor primary docs / launch posts / system
cards → **Tier B** benchmark owner or serious independent evaluator → **Tier C**
blogs, aggregators, and figures this repo carried forward without
re-verification. A Tier C claim never becomes a routing rule on its own.

### 12.1. Verified this pass (Tier A unless noted)

| Fact | Source | Effect |
|---|---|---|
| Claude roster: Fable 5.1 / Opus 5 / Sonnet 5 / Haiku 4.5, with Mythos 5.1 Glasswing-only; legacy Fable 5, Opus 4.8/4.7/4.6/4.5, Sonnet 4.6/4.5 | `platform.claude.com/docs/en/models/overview` | roster unchanged |
| Effort ladder `low, medium, high, xhigh, max`; default `high` on Fable 5.1 / Opus 5 / Sonnet 5; Haiku 4.5 has no effort parameter | `.../build-with-claude/effort` | unchanged |
| **Sonnet 5 is $2/$10 permanently** — the 1 Sep rise to $3/$15 was cancelled | `.../about-claude/pricing` | §1/§4 corrected; Opus/Sonnet ratio 1.67x → **2.5x** |
| Fable 5.1 / Mythos 5.1 cache reads at 0.025x base input ($0.25/MTok); all others 0.1x | `.../about-claude/pricing` | unchanged |
| Fable 5.1's permitted refusal-fallback targets are **Opus 4.8 and Opus 5** | `.../models/fable-5-1/whats-new-fable-5-1` | offensive-security gate re-validated |
| Fable 5.1's six named capability gains: agentic coding over long sessions · knowledge work with documents/spreadsheets/slides · research and search · vision · long-context · computer use | same | this is the backbone of the §11 tag list |
| Anthropic model-selection matrix: Opus 5 for "multihour autonomous coding agents, large-scale refactoring, complex systems engineering, vision-heavy workflows, computer use" | `.../models/choosing-a-model` | supports flagship capability list in Step 4 |
| Sonnet 5 **does** have published `max` guidance | `.../build-with-claude/effort` | falsified an earlier claim in §3 |
| `ultracode` = `xhigh` + dynamic workflow orchestration; settable via `/effort`, `--effort` (v2.1.203+), settings key, `CLAUDE_CODE_EFFORT_LEVEL`; `opusplan` = Opus in plan mode → Sonnet in execution | `code.claude.com/docs/en/model-config` | both mechanisms re-validated; "per-session only" falsified |
| Astra: `gpt-6-astra`, 1,050,000-token context (922k input / 128k output), cutoff 30 Apr 2026, $10/$50 (+2× above 272k), `reasoning.effort` `low…max`, **`none` rejected** | `developers.openai.com/api/docs/models/gpt-6-astra` | roster + gates unchanged |
| Codex roster: **Astra**, **5.6 Sol** (premium); **5.6 Terra**, **5.6 Luna** (standard); **5.3 Codex Spark** (text-only research preview); legacy 5.5/5.4 | `learn.chatgpt.com/docs/models` | Codex Spark newly recorded; router does not select it |
| **`max` and Ultra are Astra/Sol only**; Ultra therefore runs on Astra too | same | resolves an open question; hardens the Terra cap |
| GPT-5.6 defaults to `medium` effort; "Treat `reasoning.effort` as a tuning knob, not the primary way to recover quality" | `developers.openai.com/api/docs/guides/reasoning` | quoted in `SKILL.md` effort notes; supports Rules E1–E3 |
| "Astra achieves stronger results while using substantially fewer output tokens — delivering a lower estimated API cost per task" | `developers.openai.com/api/docs/guides/latest-model` | token-efficiency signal; partially conflicts with AA, see §12.3 |
| Astra is at OpenAI's **Critical** cyber Preparedness level; Critical-capability deployment carries stricter isolation and universal trajectory monitoring | `deploymentsafety.openai.com/gpt-6-astra` | offensive-security gate re-validated |
| AA Intelligence Index **v4.3** composition: Agents 30% (AA-Briefcase, GDPval-AA v2, AutomationBench-AA) · General 30% (AA-Omniscience, GDP.pdf, AA-LCR v1.1) · Coding 20% (Terminal-Bench v4.0, SciCode) · Scientific Reasoning 20% (HLE, CritPt); **scores not comparable across index versions** | `artificialanalysis.ai/methodology/intelligence-benchmarking` (Tier B) | the single most useful methodological find of the pass |
| Per-model, per-effort index + cost/task + output speed + latency | `artificialanalysis.ai/leaderboards/models` (Tier B) | §13.1; basis of Rules E1–E3 |
| Terminal-Bench 4.0 / TB-Science 0.1 / HLE / CursorBench 3.2.0 / GDPval-AA v2 / OSWorld 2.0 / AutomationBench numbers incl. GPT-5.6 Sol | `anthropic.com/claude-fable-and-mythos-5-1` | §11 anchors — **vendor-run**, direction only |

### 12.2. What changed in the router because of it

1. **Sonnet 5 pricing** — corrected everywhere; the Opus/Sonnet quota ratio is
   2.5x, not 1.67x.
2. **`Sonnet 5 · max` / `Terra · max`** — were forbidden by a heuristic; now
   forbidden by measured dominance (§13.2 E1/E2) plus, on Terra, a hard
   capability limit.
3. **The escalation target changed** from "same tier, more effort" to "next tier
   up, same or lower rung" (Step 7 Rule 2).
4. **`max` narrowed** (§13.2 E3): it now requires a single indivisible
   novel-design or formal decision, not merely `D=3 ∧ R=3`.
5. **New Codex computer-use gate** — `SKILL.md` already *mentioned* computer use
   as one of Astra's gates in its roster note but the gate table never had the
   row. Fixed.
6. **`minimal`/`none` rungs** — the reasoning guide still lists `none` and
   `minimal`; `learn.chatgpt.com` lists neither. The router emits neither, so
   the conflict is recorded and left alone.
7. **The 2026-09-02 leaderboard section (§2.1) was demoted to historical** and
   the two rules it carried were re-grounded on Terminal-Bench 4.0 + AA v4.3.

### 12.3. Conflicts left open — recorded, not silently resolved

1. **Codex `max` availability.** `learn.chatgpt.com/docs/models` (10 Sep):
   Max/Ultra are Astra+Sol only. The API model-guidance reading used in
   iteration-12 put the full ladder on all GPT-5.6 tiers. Artificial Analysis
   publishes a `Terra (max)` row, which implies they could run it. Possible
   causes: product surface vs API surface; a staged rollout; AA using API access
   the ChatGPT product doesn't expose. **Not resolved.** Router behaviour is the
   same under both readings.
2. **"Agentic coding" gap for Sol.** Terminal-Bench 4.0 (Tier A, 2026-09-01):
   Sol 37.3 vs Opus 5 52.3 — a ~15-point gap. DeepSWE v1.1 (Tier C, carried):
   Sol 72.7 vs Opus 5 73.7 — a 1-point gap. CursorBench 3.2.0 (Tier A): Sol 67.2
   vs Opus 5 70.0 — 2.8 points. Three benchmarks, three magnitudes, one label.
   Most likely cause: scaffold. Terminal-Bench is a bare terminal agent loop;
   CursorBench runs inside an IDE agent; DeepSWE's scaffold is unstated. **Not
   resolved.** The router weights Terminal-Bench 4.0 highest (Tier A, dated,
   names its harness, and is an AA Index component) — but keeps the consequence
   at a **+1 effort notch** rather than a model change precisely because the
   other two benchmarks disagree about the size.
3. **Astra token efficiency.** OpenAI: Astra uses substantially fewer output
   tokens than Sol and costs less per task. AA v4.3: Astra max $3.26/task vs Sol
   max $1.99/task — i.e. *more* per task, not less. Both can be true (different
   task mixes, different effort pairings, per-token vs per-task), but they are
   not the same claim. The router uses the AA figure for Astra-vs-Claude
   comparisons, where the two sources agree in direction, and does **not** use
   the vendor claim to prefer Astra over Sol.
4. **OSWorld.** Anthropic publishes OSWorld **2.0** with *partial* and *strict*
   scoring (a ~36-point spread on the same model). The Astra 72.6 / Sol 65.7
   figures this repo carries are OSWorld **V2** with the scoring mode unstated.
   These sets are **not directly comparable**. Consequence: the computer-use
   badge is real but always marked **low-confidence**.
5. **Codex Coding Agent Index.** The 67 / 70 figures carried from iteration-15
   could not be traced to any live index — AA v4.3 has no standalone coding-agent
   index. Demoted to Tier C and removed from every rule's justification.

### 12.4. Could not be verified in Phase 1 — stated plainly

> Phase 2 closed most of this list. See §12.5 for what was actually found; the
> entries below are kept as the Phase 1 record.

- **WebSearch was unavailable for the entire pass.** All research was done by
  fetching known primary URLs directly. Anything that would have been *found*
  by search rather than *fetched* by URL is therefore missing from this pass.
- **Terminal-Bench 4.0 leaderboard rows** (`tbench.ai/leaderboard`) — page
  reachable, table not rendered. This is the highest-value gap: the owner's
  leaderboard carries per-model **cost, tokens and 95% CI whiskers**, which
  would replace vendor-run Terminal-Bench numbers *and* give the equivalence
  band a published CI.
- **LiveBench** — no table returned. The whole 2026-06-25 row set is now
  unverifiable; §2.1 is marked historical.
- **OSWorld leaderboard** (`os-world.github.io`) — connection refused.
- **SWE-bench / SWE-bench Pro leaderboards** — page truncated before the rows.
  No current SWE-bench figures entered this pass at all.
- **`openai.com/index/gpt-6-astra/`** — HTTP 403. Astra's launch benchmarks come
  only from the API docs and carried Tier C figures.
- **"Daybreak Blue" by name** — the Astra safety page describes Critical-tier
  access controls but did not name the programme in what was retrieved. The gate
  is unchanged because it is conservative either way (standard access → "use
  Claude"), and the exception only fires when the *user* states the access.
- **Astra's biology/CBRN threshold** — the page shows that bio/chem capability
  thresholds exist but not Astra's level. Biology stays `unverified — use Claude`.
- **MRCR, GraphWalks, BrowseComp, ScreenSpot-Pro, FrontierMath, ARC-AGI,
  Toolathlon** — none verified cross-ecosystem this pass. Where a tag depends on
  them (`long-context` beyond AA-LCR, `computer-use` beyond OSWorld,
  `deep-reasoning` maths), the router says `low-confidence` rather than inventing
  a ranking.
- **Sonnet 5 at `high` / `xhigh`, and Sol at `xhigh`,** are absent from the AA
  extract. Those rungs are **unknown**. They are not interpolated anywhere.

### 12.5. Phase 2 research record — benchmark-owner sources (10 September 2026)

Phase 1 ran with WebSearch unavailable and could only fetch known URLs, so every
benchmark-owner leaderboard went unread. Phase 2 had search and went back for
them. What changed is substantial.

#### Terminal-Bench — the biggest correction in the set

| Source | Class | Rows |
|---|---|---|
| **Vals.ai, TB 2.1, Terminus 2 for every model** | model_intrinsic, tier B | Astra 87.27 · Sol 85.77 · Fable 5.1 85.02 · Opus 5 84.64 |
| **tbench.ai owner leaderboard, TB 2.1** | ecosystem_end_to_end, tier B | Codex CLI + Sol **89.5** · Claude Code + Opus 5 (max) **89.1** |
| **Artificial Analysis, TB 4.0** | model_intrinsic, tier B | **Astra 59 · Fable 5.1 52 · Sol 40** |
| OpenAI launch table, TB 4.0 (relayed) | vendor_relative, tier C | Astra 57.7 · Fable 5.1 55.8 · Opus 5 52.3 · Fable 5 42.0 · Sol 37.3 |
| Anthropic launch note, TB 4.0 | vendor_relative, tier A | Mythos 5.1 60.9 · Fable 5.1 55.8 · Opus 5 52.3 · Fable 5 42.0 · Sol 37.3 |

Four things fall out of this table, and each of them matters:

1. **The two vendor tables are one table.** OpenAI's TB 4.0 figures for Fable 5.1
   (55.8), Opus 5 (52.3), Fable 5 (42.0) and Sol (37.3) are digit-for-digit
   identical to Anthropic's. That is one published number being re-cited by both
   sides, not two independent runs, so it is not corroboration and must not be
   counted twice.
2. **Anthropic's table has no Astra row.** The iteration-16 rule
   "agentic-code → Claude" was read off a table that never measured the model it
   was being used to rule against. That is a sampling error, and it is exactly
   the failure mode the Phase 2 brief asked to look for.
3. **The independent run agrees about Sol and disagrees about Astra.** AA's TB
   4.0 reproduces the Claude-over-Sol direction (52 vs 40) and puts Astra above
   both. Hence the model-conditional badge.
4. **TB 2.1 is saturated and TB 4.0 is not.** 84–88 versus 40–59. Both groups are
   flagged `saturated: true` in the evidence store, so the compiler refuses to
   read a ranking off them; the unsaturated version is the discriminating
   instrument.

**Terminal-Bench 2.1 vs 4.0 are different benchmarks and are never compared.**
2.1 is a tagged release with a public dataset repo (`harbor-framework/terminal-bench-2-1`)
and a documented submission protocol — `metadata.yaml` naming agent and model,
`config.json` per job, `result.json` per trial, minimum five trials per task. The
owner leaderboard columns are Rank / Model / Agent / Resolution rate / Cost /
Tokens with 95% CI whiskers.

**What still could not be extracted:** the owner leaderboard's actual rows.
`tbench.ai` renders client-side, the Hugging Face mirror
(`harborframework/terminal-bench-2-leaderboard`) is 2.0-only and its dataset
viewer was down, and the repo stores raw per-trial artifacts rather than an
aggregated table. The two end-to-end rows above come from a search index quoting
the leaderboard, which is why that group is tier B but the CI column is still
unavailable. **The published 95% CIs remain the single highest-value gap.**

#### LiveBench — re-verified as a mutable snapshot, then excluded

Overall figures re-verified: Fable 5.1 83.4 · Fable 5 83.0 · Sol 81.0 · Opus 5
80.1 · Sonnet 5 76.0, across 53 model variants, 23 tasks, 7 categories. No
canonical artifact could be pinned: the LiveBench GitHub repo documents releases
only to 2025-04-25 and describes `all_groups.csv` / `all_tasks.csv` as *generated*
by a local script rather than published per release. So the rows carry
`mutable_snapshot: true` with a retrieval date, and **LiveBench is on the
excluded list** — it sets no direction. The per-category rows this repo relied on
through iteration-14, including the agentic-coding figures behind the Codex +1
notch, still could not be re-verified. The notch survives because it was
re-grounded on TB 4.0 in Phase 1 and independently in Phase 2.

#### SWE-bench — deliberately null

SWE-bench Verified is saturated: Opus 5 ~96, Sol ~96.2, Fable 5 ~95, with the
top models clustered inside about one point and no aggregator stating the
scaffold. SWE-bench Pro figures (Fable 5.1 ~81.2) appear only on tier C blogs
with no harness and no Sonnet 5 or Terra rows. **No SWE-bench number entered the
router**, and no extrapolation was made from the older Claude 4.x / GPT-5.x
results. The record `swebench-verified-saturation` exists purely to document the
exclusion so the next maintainer does not re-derive it.

#### OSWorld — the computer-use gate survives, the cross-vendor badge does not

OpenAI's table, with the metadata Phase 1 was missing: **OSWorld 2.0, offline
set, partial scoring** — Astra 72.6 · Opus 5 70.2 · Sol 65.7, and ~40 min/task
against Sol's ~75 (a ~47% reduction). Anthropic's table, same version and the
same *scoring-mode label*: Fable 5.1 77.9 · Opus 5 75.4 · Fable 5 72.9 partial,
and 41.7 / 39.6 / 36.1 strict.

**Both vendors publish Opus 5 on OSWorld 2.0 partial and disagree by 5.2 points**
(70.2 vs 75.4). The likely differentiator is the offline set, which only OpenAI
names. Consequences:

- The **within-Codex** direction (Astra > Sol) is corroborated three ways —
  OSWorld, ScreenSpot-Pro (92.7 vs 76.9), Agents' Last Exam (59.3 vs 53.6) — so
  the computer-use gate that routes GUI work to Astra stands.
- The **cross-ecosystem** comparison does not: Astra 72.6 against Fable 5.1 77.9
  is two vendors' harnesses, not one measurement. The computer-use badge stays
  `low-confidence` for exactly this reason.

#### New cross-ecosystem rows that did not exist in Phase 1

- **Tooled HLE** (OpenAI's own table): Fable 5.1 65.0 · Fable 5 63.8 · Opus 5
  63.6 · **Astra 57.2**. A vendor publishing a result that favours the competitor
  is against-interest and is the most credible vendor evidence there is. It is
  why `deep-reasoning` stays with Claude.
- **FrontierMath Tier 4 (v2)**: Astra 97.6 · Fable 5.1 87.8 · Opus 5 73.2 —
  points the other way, and **excluded**: Epoch AI runs it, but the source itself
  discloses that OpenAI funded its development and holds exclusive access to part
  of it.
- **ARC-AGI-3**: Astra 99.9 · Opus 5 30.2 · Sol 7.8 — **excluded**: Anthropic's
  own Opus 5 launch note claims "three times the nearest competitor" on this
  benchmark, which cannot be reconciled with 30.2, and neither vendor publishes a
  harness spec.
- **AA Coding Agent Index (current)**: Astra+Codex 62 = Fable 5.1+Claude Code 62 ·
  Opus 5 60 · Sol 55, with Astra at $7.09/task at max. This is the index the
  iteration-15 "67/70" figures could not be traced to — they belong to an older
  version of it (Fable 5 68.1 · Fable 5.1 67.2 · Astra 67.0), which is now
  recorded separately and excluded. **A Phase 1 open item, closed.**
- **AA Intelligence Index v4.1.1**: Fable 5.1 65.7 · Opus 5 63.1 · Fable 5 62.1 ·
  Astra 61.2. This is where the 66/63/62 figures this repo carried came from.
  Under v4.1.1 Astra sat 4.5 points *below* Fable 5.1; under v4.3 they tie at 53.
  Same models, same evaluator, opposite conclusion — the concrete proof behind
  "index versions are not comparable". **A second Phase 1 open item, closed.**
- **Output tokens per task** (AA v4.3): Astra 27k at $3.26 · Fable 5.1 78k at
  $7.63. The first genuine output-token figures in the set — efficiency signal
  #2, not a cost proxy — and what decides the agentic-code badge against Astra.
- **MRCR v2 8-needle**: Astra 100 vs Sol 91.5 (256–512K), 96.3 vs 73.8
  (512K–1M). No Claude row, so long-context still has no cross-ecosystem
  comparison.
- **ExploitBench is real.** Phase 1's §7 listed it among claims that looked like
  content-farm inventions. It appears in OpenAI's launch table (Astra 100.0 ·
  Sol 78.5 · Fable 5.1 70.0, both run without production safeguards). It informs
  no routing rule — offensive security is a hard safety gate, not a capability
  comparison — but the "probably fabricated" note was wrong.

#### Still unresolved after Phase 2

- **Terminal-Bench owner leaderboard rows with their published 95% CIs.** The one
  thing that would let the equivalence band rest on real dispersion instead of
  the declared spread rule for the most important capability in the set.
- **`openai.com/index/gpt-6-astra/` still returns HTTP 403.** Every OpenAI launch
  figure in this record is a tier C relay of that page.
- **Sol pricing.** One relay states $4/$20 promotional against the $5/$30 this
  repo carries. Not re-verified against OpenAI's own pricing page; the router
  uses Sol's price only as an efficiency tie-break input, so the exposure is
  small, but it is a known soft spot.
- **"Daybreak Blue" by name** — still not seen on the safety page itself.
- **Astra's biology/CBRN threshold** — still unpublished, so the biology gate
  still declines on the Codex arm.
- **Sonnet 5 and Terra are missing from nearly every cross-ecosystem benchmark.**
  Every capability comparison in this record is between the *top* of each roster.
  The mid tier — which is what most prompts actually route to — is compared
  almost entirely on the AA aggregate. This is the largest structural weakness
  remaining in the evidence base.


---

## 13. Efficiency and quota data

### 13.1. AA Intelligence Index v4.3 — one harness, one suite, all rungs comparable

Read 10 Sep 2026 from `artificialanalysis.ai/leaderboards/models` (Tier B).
`Cost/task` is the cost of running the whole fixed evaluation suite, so within
this table it is a sound **proxy for total token load**.

| Model | Effort | Index | Cost/task | Output tok/s | Latency (s) |
|---|---|---|---|---|---|
| Fable 5.1 | max | 53 | $7.63 | 67 | 296.2 |
| Fable 5.1 | xhigh | **53** | **$5.98** | 60 | 138.4 |
| Fable 5.1 | high | 51 | $3.91 | 51 | 23.7 |
| Astra | max | 53 | $3.26 | 54 | 334.8 |
| Astra | xhigh | **53** | **$2.31** | 51 | 220.6 |
| Astra | high | 51 | $1.72 | 48 | 93.3 |
| Opus 5 | max | 51 | $5.86 | 52 | 94.9 |
| Opus 5 | xhigh | 50 | $4.88 | 52 | 30.6 |
| Opus 5 | high | 48 | $3.61 | 51 | 26.0 |
| GPT-5.6 Sol | max | 47 | $1.99 | 64 | 140.3 |
| GPT-5.6 Sol | high | 42 | $0.81 | 59 | 39.9 |
| GPT-5.6 Terra | max | 42 | $1.40 | 84 | 183.1 |
| Sonnet 5 | max | **38** | **$5.09** | 79 | 197.8 |
| GPT-5.6 Luna | max | 38 | $0.18 | 112 | 138.6 |
| Haiku 4.5 | — | 18 | $0.21 | 85 | 22.2 |

⚠️ **This is an aggregate** (Agents 30 / General 30 / Coding 20 / Science 20).
It never overrides a task-specific benchmark for a task that benchmark covers.
Its legitimate uses are: (a) effort-rung comparisons *within one model*, (b)
cost/token-load comparisons, (c) a last-resort tie-break when no task-specific
row exists — flagged `low-confidence`.

⚠️ **Not comparable with the 66/63/62/60 figures in §2.1** — different index
version.

### 13.2. The three dominance rules

**Rule E1 — `Sonnet 5 · max` is dominated.**
Sonnet 5 max = 38 @ $5.09. Opus 5 xhigh = 50 @ $4.88. Opus 5 high = 48 @ $3.61.
Twelve index points *better* and cheaper. There is no task on which paying
Sonnet 5's `max` premium is the rational move, so the router never emits it and
the escalation target is `Opus 5 · xhigh`. (Iterations 14–15 reached the same
output from a heuristic — "max on a mid-tier model risks over-thinking" — plus a
citation that turned out to be wrong. The behaviour is unchanged; the reason is
now measured.)

**Rule E2 — `Terra · max` is dominated, and also unavailable.**
Terra max = 42 @ $1.40. `Sol · high` = 42 @ $0.81. Identical index score at 42%
less quota — and `learn.chatgpt.com` says `max` isn't offered on Terra at all.
Codex escalation therefore goes **Terra → Sol**, not Terra → more effort.

**Rule E3 — `max` over `xhigh` buys almost nothing.**
Fable 5.1: 53 → 53 ($7.63 → $5.98, and 296s → 138s). Astra: 53 → 53 ($3.26 →
$2.31). Opus 5: 51 → 50 ($5.86 → $4.88, and 95s → 31s). One index point at most,
for 17–28% more quota and 2–3× the latency. So `max` is emitted only when
`D=3 ∧ R=3` **and** the difficulty is a *single indivisible novel-design or
formal decision*: architecture or boundary design from scratch, a proof, a
one-shot irreversible design call. Review, audit, migration and breadth-driven
`D=3 ∧ R=3` work stops at `xhigh`; the human-review note carries the stakes.

> **What E3 is not.** It is not "always use xhigh". Where the vendor's own
> guidance and the task class agree that the top rung matters — a frontier
> problem, an irreversible one-shot design — `max` still fires. `f1` (split a
> 6000-file monolith into services) and the `opusplan` plan phase both still
> emit `max`.

### 13.3. Efficiency signals, in priority order

1. **Reasoning tokens** — the biggest hidden quota drain. Rarely published; the
   one solid figure in the record is Opus 5 using ~1/7 of Opus 4.8's reasoning
   tokens on an internal trading benchmark (generation-over-generation only).
2. **Output tokens** — OpenAI's Astra claim and Anthropic's "26% fewer tokens at
   max" legal figure live here.
3. **Total tokens per task.**
4. **Tokens per *successful* task** — the honest metric, since a failed
   expensive run costs twice. Nobody publishes it directly; AA's cost/task on a
   fixed suite is the closest available proxy and is what §13.1 uses.
5. **Quota pressure** — which of the user's two windows is being spent. This is
   the actual objective; dollars are a proxy for it.
6. **Cost per task.**
7. **Latency / wall-clock.**

**The efficiency rule of engagement:** when the task-relevant capability
difference is meaningful, quality wins and efficiency only picks the rung. When
capability sits inside the equivalence band, efficiency picks the candidate.
Efficiency never downgrades a model whose capability edge is real — that is the
failure mode this ordering exists to prevent.

**Behaviour notes that cost tokens without changing quality** (worth mentioning
if the user asks why a session is burning quota): Fable 5.1 issues more one-call
turns in agent loops than Fable 5 did, and rewrites whole files for small edits;
both are prompt-fixable (§0.1). MCP tool schemas are re-sent every message.
Auto-accept chains edits geometrically.

---

## 14. `✅ RECOMMENDED AI` — rationale and ablation

### 14.1. Why a badge at all

Since 5 Aug 2026 the router has produced both arms and left the choice to the
user. That is still right for *which quota to spend* — only the user knows which
window is emptier. But "both are fine" was never true task-by-task: the
published evidence shows genuinely different profiles, and withholding that made
the output *less* useful, not more neutral. The badge states the router's read;
the user still decides.

### 14.2. How it is computed

The decision order lives in `SKILL.md` Step 6. The two properties that keep it
honest:

- **It is capability-conditional.** No global "Claude is better" or "Codex is
  cheaper" term exists anywhere in the rule set. Change the dominant capability
  tag and the badge moves.
- **It degrades loudly.** Where the evidence is thin the badge still appears —
  users need an answer — but the Evidence line must carry `low-confidence`.
  Four of the twelve badge rows are permanently marked that way.

### 14.3. Ablation and sanity checks (run at iteration-16)

1. **Turn the benchmark layer off — what changes?** With Step 5 and Step 6
   removed, the router falls back to iteration-15 behaviour. The outputs that
   change are: the badge on every prompt (it wouldn't exist); `Opus 5 · max` →
   `Opus 5 · xhigh` on `D=3 ∧ R=3` review work (Rule E3); the escalation target
   (`Sonnet 5 · max` → `Opus 5 · xhigh`, Rule E1); and the new computer-use
   Codex gate. Model selection on ordinary prompts is unchanged — which is the
   intended result: the evidence layer refines the edges, it doesn't re-found
   the router.
2. **Does the badge collapse onto one ecosystem?** No, and Phase 2 measured
   *why* instead of asserting it. Iteration-17: **Claude 24 · Codex 7 · no badge
   1** (`d7`, Step-0 blocked). The seven Codex wins come from four distinct
   causes — `d1`/`r2`/`s1` are `D≤1` efficiency calls (Luna over Haiku 4.5);
   `g1` is a capability lead (computer use); `i1` is a product mechanism (Ultra's
   parallel agents); `f1`/`x1` are the Phase 2 model-conditional finding (against
   Astra, Claude's agentic-code lead does not hold).

   **The vendor-bias ablation** (`python scripts/ablate_evidence.py`) reruns the
   whole frontier under three evidence views and is the real answer to "is this
   lean earned?":

   | view | records kept | claude | codex | efficiency decides |
   |---|---|---|---|---|
   | full | 123 | 14 | 7 | 10 |
   | independent only (tier B) | 31 | 11 | 6 | 14 |
   | vendor-cross-model disabled | 48 | 11 | 6 | 14 |

   Only **`agentic-code` and `terminal-tool` survive both filters.** Every other
   capability collapses to UNRESOLVED once you remove rows where one vendor
   scored the other in its own harness — `knowledge-work` (GDPval, Anthropic
   only), `science` and `workflow-automation` (both vendors' own tables),
   `computer-use` (OpenAI only), `deep-reasoning` (OpenAI's HLE row only).

   **Both sides' advantages outside terminal work are vendor-dependent.** That is
   a fact about the published record, not a reason to force a 50/50 split — a
   balanced badge would be a fabrication. The response was to make the router say
   so: those capabilities are marked † in the Step 6 table and their Evidence
   line must carry `low-confidence`. The eval set enforces it (`x2`, `q1`, `h1`,
   `p1`, `d6`, `f2`, `m1`).
3. **Are top-tier models over-selected?** No. Across the 32-eval iteration-17
   run the mid tier (Sonnet 5 / Terra) still carries roughly half of all model
   lines, the flagships appear only at `D=3` plus a flagship-list capability, and
   the frontier tier only where a gate put it there.
4. **Is `max` over-selected?** No longer. Effort spread across the run:
   `xhigh` 16 · `medium` 10 · `high` 9 · `low` 9 · `max` **5** · `ultracode` 4.
   The five `max` lines are `f1` (both arms), `h1` (both arms) and `d6`'s
   `opusplan` plan phase — all indivisible novel-design decisions at `R=3`,
   which is exactly the surviving E3 case. Before E3, `q1` would also have
   produced `max`; it now stops at `xhigh`.
5. **Does efficiency ever actually change a decision?** Yes, and it is asserted
   in the eval set, not just described: the volume gate's badge, the
   long-context badge, the parallel-work badge, and the escalation eval
   (`q1`) all turn on efficiency rather than on a capability gap.
6. **Does efficiency override quality too often?** It is structurally barred
   from doing so: 5c requires "not meaningfully worse" *before* any efficiency
   axis is consulted, and 5b widens the equivalence bar when `R=3`.
7. **Does the aggregate index steamroll task-specific benchmarks?** The AA Index
   is admitted for exactly three purposes (§13.1) and is explicitly excluded
   from `deep-reasoning`, `agentic-code` and every other tag with its own row.
8. **Are different-harness numbers being compared?** The three known cases
   (OSWorld version/scoring, the three agentic-coding scaffolds, AA index
   versions) are each recorded in §12.3 and each carry an explicit
   `not directly comparable` marker rather than a silent average.

---

## 15. Evidence architecture — raw, derived, runtime (Phase 2, 10 Sep 2026)

> **Why this section exists.** Phase 1 built the benchmark-aware engine and left
> the path from a raw score to a routing rule inside prose. That works until it
> doesn't: a number changes, a rule keeps citing it, and nothing fails. Phase 2
> made the path mechanical. The routing behaviour barely moved — the point was to
> make it *auditable*.

### 15.1. Three layers, and only one is read at runtime

| Layer | File | Written by | Read when | Size |
|---|---|---|---|---|
| **Runtime rule** | `skill/SKILL.md` | a human | every route | ~740 lines |
| **Derived frontier** | `skill/benchmark_frontiers.json` | `scripts/compile_benchmark_frontiers.py` — **generated** | auditing a rule | ~1.5k lines |
| **Raw evidence** | `skill/benchmarks.json` | a human, one record per measurement | changing a rule | 123 records |

**Runtime cost, stated honestly.** The router still reads only `SKILL.md`, and
that is the constraint that matters: loading 123 evidence records to answer
"which model for this prompt" would be precisely the quota waste this project
exists to prevent, and `SKILL.md` says so explicitly. The two data files ship in
the package so a maintainer can check a rule, not so the router can consult them.

`SKILL.md` itself grew **+5.7%** (39,415 → 41,653 bytes) in Phase 2. That is not
free and it is not zero. It buys the model-conditional badge table, which is a
fourth column rather than a longer file, plus three comparability traps in §5a
that exist because the first draft fell into two of them. A trim pass afterwards
recovered ~2.2KB by cutting the badge table's evidence column down to the
decisive figure — the full rows live in §11 and §13, which the router does not
read. Anything in `SKILL.md` that is explanation rather than decision belongs
here instead; that is the standing rule when it next grows.

### 15.2. The compiler

`scripts/compile_benchmark_frontiers.py` transforms raw records into
capability frontiers. Its one hard constraint: **it never interprets a number on
its own.** Every threshold is declared in `benchmarks.json`:

- `comparability_groups` — a group *asserts* that benchmark, version, harness,
  tool access, scaffold and evaluator were constant. The compiler never infers
  comparability; it only trusts the assertion. Groups also declare
  `saturated: true` and an `equivalence_band`.
- `evidence_precedence` — the weight of each (evidence class, source tier) pair.
- `no_dispersion_rule` — when a group publishes no CI or SE, the band is a
  declared fraction (0.15) of the group's own observed spread. That is the
  codification of §5b step 3: a gap counts only if it is large relative to how
  discriminating the benchmark actually is.
- `excluded_from_direction` — benchmarks that may never set a direction, each
  with a written reason.
- `model_ecosystem` — which model belongs to which arm. Declared, never parsed
  out of a model name.

Where the declared metadata does not settle a comparison the output is
**`UNRESOLVED`**, which is a first-class result: it tells the router to fall
through to the efficiency tie-break. The compiler never averages two conflicting
sources, never splits a difference, never prefers the newer number, and never
fills in a missing effort rung.

Two subtleties that cost a rewrite each, both now covered by unit tests:

1. **A cell is (group, benchmark, version), not (group).** One source publishing
   HLE, FrontierMath and ARC-AGI-3 under one harness yields three cells. Pooling
   them let the first draft compare an ARC-AGI-3 score against an HLE score.
2. **The equivalence band comes from the full cell, never from a subset.** With
   two rows the spread *is* the gap, so a subset-derived band would make every
   two-model comparison produce a winner.

### 15.3. Model-conditional frontiers

The compiler emits `by_codex_model` alongside the overall verdict, because
"best Claude vs best Codex" is the wrong question for a router. The Codex
candidate is usually Terra or Sol; Astra only appears behind a gate. A capability
can favour Claude against Sol and not against Astra — and on agentic coding it
does exactly that:

| capability | vs Sol | vs Astra |
|---|---|---|
| `agentic-code` | **claude** (high) | equivalent → efficiency decides |
| `terminal-tool` | **claude** (high) | **codex** (medium) |
| `science` | claude | codex |
| `workflow-automation` | claude | codex |
| `computer-use` | claude | **codex** |
| `deep-reasoning` | UNRESOLVED | claude (low) |

Phase 1 collapsed the first two rows into a single "agentic-code → Claude", which
was right against Sol and wrong against Astra. That was not a reasoning error so
much as a **sampling** error: the rule rested on Anthropic's Terminal-Bench 4.0
table, and that table has no Astra row at all.

### 15.4. Rule provenance

Every benchmark-derived rule in `SKILL.md` has a machine-readable entry in
`benchmarks.json` → `routing_rules`, carrying `rule_id`, `evidence_ids`,
`capability`, `comparison_type`, `confidence` and `last_verified`. The validator
fails if any `evidence_id` stops resolving, so a rule cannot outlive the number
it was built on. `benchmark_frontiers.json` → `rule_provenance` resolves each
rule to its evidence classes, source tiers and whether it is entirely vendor-run.

`BADGE-parallel-independent` deliberately carries an empty evidence list: it
rests on a documented product mechanism, not a benchmark. The validator permits
that only for `comparison_type` of `product_mechanism`, `spec_and_price` or
`excluded` — everything else must cite evidence.

### 15.5. Validation and staleness

```
python scripts/validate_benchmarks.py          # schema, groups, rules, staleness
python scripts/compile_benchmark_frontiers.py  # regenerate the frontier
python scripts/compile_benchmark_frontiers.py --check   # fail if stale
python scripts/test_frontier_compiler.py       # 26 comparison-semantics assertions
python scripts/ablate_evidence.py              # vendor-bias measurement
```

The validator catches: invalid or missing source tier · missing/duplicate record
id · a score with no `benchmark_version` where the benchmark is versioned · a
score with no unit · a record whose class or tier contradicts its group · **two
different harnesses inside one comparability cell** · an `ecosystem_end_to_end`
group that uses only one harness (mislabelled) · partial/strict scoring living in
one group · text that reads as an interpolated figure · a rule citing a
nonexistent evidence id · a rule with no evidence where its type requires some ·
and **a derived frontier that no longer matches the evidence it came from**.

Staleness is enforced by hash: the frontier stores `input_sha256` of the exact
bytes of `benchmarks.json`. Edit the evidence without recompiling and both the
compiler's `--check` and the validator fail. That is deliberate — a benchmark
router whose derived layer silently lags its evidence is worse than one with no
derived layer at all.

**Determinism** is a build requirement, not a nicety: the compiler sorts every
key and derives `generated_from` from the input rather than from the wall clock,
so two runs produce byte-identical output. `scripts/test_frontier_compiler.py`
asserts it, and the release checklist runs the compiler twice and diffs.

### 15.6. What Phase 2 changed in routing

Almost nothing, on purpose. One badge row became model-conditional
(`agentic-code` / `terminal-tool` against Astra), and seven capabilities gained a
mandatory `low-confidence` marker because the ablation showed they rest entirely
on vendor-run cross-model rows. Model and effort selection are untouched.
