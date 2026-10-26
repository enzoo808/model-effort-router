# OpenCode Go evidence — iteration-23

**Audit data for the OpenCode arm of `SKILL.md`. Never load this to route a prompt;
every rule needed is in `SKILL.md`.** Verified **6 October 2026** (§11, Claude Haiku 5.5: **8 October 2026**). Everything below
was fetched in this pass from the sources in §8; anything not fetched is marked
`n/p` (not published / not retrieved) and was **not** filled in from memory.

## 1. The plan and what "cap" means

Source: `opencode.ai/docs/go/`.

- **Go = USD 10/month, Go Plus = USD 40/month.** The user is on Go.
- Limits are **per model**, not shared: *"5-hour — 20% of the monthly limit; weekly —
  50%; monthly — 100%"*. The Monthly limit column is the maximum dollar amount that
  can be spent on that one model per month. So a USD 15 model allows USD 3 per
  5 hours and USD 7.50 per week; a USD 60 model allows USD 12 / USD 30.
- Model ids are `opencode-go/<model-id>` (e.g. `opencode-go/kimi-k3`).
- Page lists **31 models** (30 on 6 Oct + **Claude Haiku 5.5**, added 7 Oct). The 16 rated models are in §2 and §11; the other 15 are in §7.
- **Retention (page text):** 0 days for most models; **Grok 4.7 / 4.6: 30 days**
  (ZDR limits stateful Responses API and Files); **GPT 6 Luna / 5.6 Luna: 30 days**
  (abuse-monitoring logs); **DeepSeek (V4.1 Flash, V4 Pro, V4 Flash, V4 Flash Vision
  Exp): 0 days, "ZDR agreement is renewed monthly. The current agreement is valid
  through October 31, 2026"**; **Muse Spark 1.3 / 1.2 Contributor: prompts and
  completions may be used to train future Meta models** ("heavily discounted token
  pricing"), tier geo-restricted by Meta policy.
- **Peak pricing (DeepSeek only):** Mon–Fri 01:00–04:00 and 06:00–10:00 UTC = 04–07
  and 09–13 Turkish time; double price.
- **Context-tiered pricing:** Qwen3.7 Plus > 256K, Grok > 200K, GPT 6 Luna > 272K.
- The Go page says **nothing** about effort variants, and OpenCode's docs give no per-model
  list. The authoritative list is the model catalogue OpenCode reads, **models.dev**
  (`providers/opencode-go/models/<id>.toml`, dev branch, read 6 Oct 2026) — see §4.

## 2. The 15 original main models (Claude Haiku 5.5 is the 16th — §11)

AA = Artificial Analysis Intelligence Index **v4.3.2**, "Max" unless stated. All
benchmark columns are **AA same-page comparison values** (`artificialanalysis.ai/
models/comparisons/<model>-vs-<model>`), so they share one harness and one scale.

| Model | II | TB 4.0 | GDPval-AA | Briefcase | AutoBench | SciCode | HLE | GDP.pdf | CritPt | Omniscience | AA-LCR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **MiMo-V2.6-Pro** | 46 | 35 | 1686 | 1516 | 59 | 61 | 49 | 19 | 27 | 8 | 86 |
| **GLM-5.3** (Max) | 45 | **42** | 1653 | 1510 | 62 | 59 | 42 | 11 | 19 | 14 | 80 |
| **Kimi K3** (Max) | 44 | 13 | 1537 | 1501 | 58 | 59 | 47 | 22 | 23 | 20 | **89** |
| **Grok 4.7** (xhigh) | 46 | 26 | **1715** | **1644** | 66 | 57 | 43 | 20 | 18 | **32** | 77 |
| **Muse Spark 1.3** (Max) | **48** | 33 | 1684 | 1583 | 58 | 59 | 49 | **27** | 25 | 25 | 83 |
| **GLM-5.3-Flash** | 42 | 33 | 1647 | 1454 | 60 | 52 | 40 | 15 | 15 | 7 | 80 |
| **MiMo-V2.6-Flash** | 38 | 23 | 1611 | 1495 | 64 | 51 | 35 | 9 | 12 | −13 | 74 |
| **DeepSeek V4.1 Flash** (Max) | 39 | 27 | 1600 | 1420 | **69** | 52 | 39 | 13 | 14 | −5 | 84 |
| **GPT 6 Luna** (Max) | 38 | 13 | 1437 | 1336 | 53 | 55 | 39 | 23 | 19 | 1 | 83 |
| **Qwen3.8 Flash** (-Next) | 40 | 25 | 1633 | 1583 | 56 | 51 | 38 | 16 | 11 | −10 | 80 |
| **Qwen3.8 Max** (0902) | 45 | 39 | 1671 | 1621 | 56 | 52 | 43 | 23 | 18 | 12 | 80 |
| DeepSeek V4 Pro 0813 (Max) | 36 | 14 | 1455 | 1256 | 57 | 51 | 41 | 11 | 18 | 1 | 80 |
| MiniMax M3 | 29 | 2 | 1245 | 1091 | 21 | 47 | 39 | 10 | 4 | 1 | 83 |
| Kimi K2.7 Code | 26 | 1 | 1040 | 859 | 24 | 48 | 35 | 11 | 10 | −10 | 79 |
| Qwen3.7 Plus | 25 | 1 | 770 | 915 | 17 | 46 | 36 | 12 | 9 | 1 | 73 |

**Claude, same pages (Max):** Opus 5.5 — II 58, TB 60, GDPval 1866, Briefcase 1807,
AutoBench 70, SciCode 67, HLE 61, GDP.pdf 26, CritPt 32, Omniscience 46, LCR 85.
Sonnet 5.5 — II 56, TB 64, GDPval 1839, Briefcase 1823, AutoBench 72, SciCode 61,
HLE 55, GDP.pdf 26, CritPt 31, Omniscience 32, LCR 83.

Cost, tokens, speed (same pages):

| Model | cost/task | out tok/task | reasoning tok/task | tok/s | TTFT | Go price in/out | cap | ≈5-h out tokens |
|---|---|---|---|---|---|---|---|---|
| MiMo-V2.6-Pro | $0.13 | 64k | 38k | 45 | 4.75 s | 0.435 / 0.87 | $15 | 3.4M |
| GLM-5.3 (Max) | $2.01 | 71k | 49k | 75 | 2.84 s | 1.40 / 4.40 | $15 | 0.7M |
| GLM-5.3 (Low) | $0.85 | 88M tok total (vs 210M at Max) | — | 82 | — | same | $15 | — |
| Kimi K3 (Max) | $2.00 | 48k | 32k | 52 | 4.33 s | 3.00 / 15.00 | $15 | 0.2M |
| Kimi K3 (Low) | $1.15 | 22M tok total (vs 160M) | — | 57 | 3.36 s | same | $15 | — |
| Grok 4.7 | $3.74 | 81k | 59k | 92 | 48.1 s | 2–4 / 6–12 | $15 | 0.5M |
| Muse Spark 1.3 | $1.60 (AA price 1.25/4.25) | 60k | 34k | 187 | 39.9 s | 0.10 / 0.20 | $60 | 60M |
| GLM-5.3-Flash | $0.25 | 69k | 47k | 53 | 3.33 s | 0.15 / 0.50 | $60 | 24M |
| MiMo-V2.6-Flash | $0.06 | 78k | 58k | 62 | 4.21 s | 0.14 / 0.28 | $60 | 43M |
| DeepSeek V4.1 Flash | $0.27 | 89k | 63k | **222** | **1.08 s** | 0.15–0.30 / 0.60–1.20 | $60 | 20M / 10M peak |
| GPT 6 Luna | $0.07 | 50k | 39k | 147 | 96 s | 0.10–0.20 / 0.50–0.75 | $15 | 6M |
| Qwen3.8 Flash | $0.37 | 108k | 72k | 55 | 2.48 s | 0.15 / 0.47 | $30 | 12.8M |
| Qwen3.8 Max | $5.41 | 108k | 71k | 37 | 2.68 s | 2.00 / 6.00 | $15 | 0.5M |
| DeepSeek V4 Pro | $0.67 | 55k | 38k | 99 | 1.67 s | 0.66–1.32 / 1.98–3.96 | $15 | 1.5M |
| MiniMax M3 | $0.51 | 48k | 22k | 103 | 2.05 s | 0.30 / 1.20 | $60 | 10M |
| Kimi K2.7 Code | $0.54 | 30k | 19k | 76 | 2.80 s | 0.95 / 4.00 | $60 | 3M |
| Qwen3.7 Plus | $0.22 | 36k | 25k | 56 | 2.25 s | 0.40–1.20 / 1.60–4.80 | $60 | 7.5M |
| *Opus 5.5 (max)* | *$5.98* | *119k* | — | *97* | *716 s* | — | — | — |
| *Sonnet 5.5 (max)* | *$7.67* | *197k* | *147k* | *128* | *442 s* | — | — | — |

`≈5-h out tokens` = 0.2 × cap ÷ output price, ignoring input and cached-read cost —
an **upper bound**, useful only to rank cap pressure. Real agent sessions are
input-dominated, where MiMo's USD 0.0036 cached read is the standout.

Context windows: MiMo-V2.6-Pro 1M · GLM-5.3 1M · Kimi K3 1M · **Grok 4.7 500k** ·
Muse Spark 1.3 1M · GLM-5.3-Flash 1M · DeepSeek V4.1 Flash 1M · GPT 6 Luna 1M ·
**Qwen3.8 Flash 256k** · Qwen3.8 Max 984k · DeepSeek V4 Pro 1M · MiniMax M3 1M ·
Kimi K2.7 Code `n/p` · MiMo-V2.6-Flash **1M** (AA) · Qwen3.7 Plus ≥ 256k (tier boundary).

Input modalities (AA): **text-only GLM-5.3**; text+image Kimi K3, GLM-5.3-Flash,
Grok 4.7, GPT 6 Luna, Qwen3.8 Max; text+image+video Qwen3.8 Flash, MiniMax M3, Muse
Spark 1.3; MiMo-V2.6-Pro takes text, image, speech and video. Only *DeepSeek V4 Flash
Vision Exp* is marked vision on the Go page. MiMo-V2.6-Flash takes text+image (AA).

## 3. Findings from the AA-only pass (**superseded in part by §10** — read §10 first)

1. **MiMo-V2.6-Pro dominates the pool on the index per dollar** (46 @ $0.13; the next
   cheapest 40+ model is Qwen3.8 Flash at $0.37). It also tops HLE (49, tied with Muse
   Spark), CritPt (27) and SciCode (61).
2. **GLM-5.3 is the strongest measured coder: TB 4.0 42** — ahead of Qwen3.8 Max 39,
   MiMo-V2.6-Pro 35 and everything else. The draft's claim that Grok 4.7 has "the
   strongest independent coding-agent numbers" does not hold on AA's TB 4.0
   (Grok 26, below DeepSeek V4.1 Flash 27); Grok's 56.3 is a Coding Agent Index
   figure with its own harness.
3. **Kimi K3 is not the knowledge-work model.** It is *last* of the main group on
   GDPval-AA (1537) and AA-Briefcase (1501). Its strengths are AA-LCR (89),
   AA-Omniscience (20, third after Grok and Muse) and GDP.pdf (22). Its TB 4.0 is 13.
4. **Grok 4.7 leads knowledge-work** (GDPval-AA 1715, Briefcase 1644, AutomationBench
   66, Omniscience 32) but is eliminated for confidential work by 30-day retention.
5. **DeepSeek V4.1 Flash has the pool's best AutomationBench-AA (69)** — one point under
   Opus 5.5's 70 — on a USD 60 cap at USD 0.27/task, and is by far the fastest
   (222 tok/s, TTFT 1.08 s).
6. **GLM-5.3-Flash is the best cheap coder**: TB 33 vs MiMo-V2.6-Pro's 35, II 42, on a
   USD 60 cap at $0.25/task, with image input and a 1M window.
7. **Muse Spark 1.3 is the highest index (48)** at ~USD 0.10 per task on Go prices
   with a USD 60 cap — and trains on prompts, so it is NC1-only.
8. **Four of the 15 are dominated** (DeepSeek V4 Pro, MiniMax M3, Kimi K2.7 Code,
   Qwen3.7 Plus — the last three have TB 1–2). They are rated and kept in the pool
   because the user asked for 15 main models; no routing row emits them.
9. **Low rungs are dominated by Flash models:** GLM-5.3 Low 34 @ $0.85 (cap 15) <
   GLM-5.3-Flash 42 @ $0.25 (cap 60); Kimi K3 Low 30 @ $1.15 < MiMo-V2.6-Flash 38 @
   $0.06. So the Pro-tier models are only ever emitted at `max`.
10. **Claude vs OpenCode, one scale:** Claude leads TB 4.0 by 18–29 points (Sonnet 5.5
    64, Opus 5.5 60 vs 42/39/35/…), GDPval-AA by 150–180, Briefcase by 160–290, HLE by 6–14,
    CritPt by 4–5, Omniscience by 12+ (vs Kimi/MiMo), AutomationBench by 1–3 vs DeepSeek
    V4.1 Flash; **open models lead or tie AA-LCR** (Kimi 89, MiMo 86 vs 85/83) and tie
    SciCode (MiMo 61 = Sonnet 61).

## 4. Effort evidence and the variants OpenCode actually offers

### 4a. Variants (models.dev, `providers/opencode-go/models/*.toml`, read 6 Oct 2026)

| Model | `reasoning_options` | Note |
|---|---|---|
| GLM-5.3 · GLM-5.3-Flash | effort `low` `high` `max` | Z.ai: thinking cannot be disabled; server default `max` |
| DeepSeek V4.1 Flash | effort `low` `high` `max` | DeepSeek API: default `high`; `none` (non-thinking) exists in the API but not as an OpenCode variant |
| DeepSeek V4 Pro | effort `high` `max` | |
| Kimi K3 | effort `max` **only** | Moonshot's API has `low`/`high`/`max` (default `max`) but OpenCode lists only `max` |
| MiMo-V2.6-Pro · MiMo-V2.6-Flash | **`[]` — none** | Xiaomi docs: only `thinking.type` enabled/disabled, on by default. A pull request (anomalyco/models.dev #7680) proposing `none/low/medium/high` was flagged by a review bot as unsupported by Xiaomi's docs; its probe showed `xhigh`/`max` → HTTP 400 |
| Grok 4.7 | effort `low` `medium` `high` `xhigh` | xAI default `high` |
| Qwen3.8 Flash · Qwen3.8 Max | toggle · effort `low` `medium` `xhigh` · token budget (≤ 262,144) | API default `xhigh`; `low` ≈ 4,096-token cap, `medium` ≈ 16,384 |
| GPT 6 Luna | effort `none` `low` `medium` `high` `xhigh` `max` | |
| Muse Spark 1.3 Contributor | effort `minimal` `low` `medium` `high` `xhigh` | capability metadata copied from Muse Spark 1.2 "pending public 1.3 specifications" |

Independent confirmation that OpenCode-Go rejects `medium`/`xhigh` on the `low`/`high`/`max`
models: pingdotgg/t3code #15645 (*"Variant unavailable for opencode-go/deepseek-v4.1-flash:
medium"*) and NousResearch/hermes-agent #107495. Caveat: the dev branch may be newer or older
than the OpenCode build in use — if `variant_cycle` shows a different list, trust it.

### 4b. Measured rungs (AA, v4.3.2)

| Model | Rung | II | cost/task | tokens (index run) |
|---|---|---|---|---|
| GLM-5.3 | Max | 45 | $2.01 | 210M out (verbose) |
| GLM-5.3 | Low | 34 | $0.85 | 88M |
| Kimi K3 | Max | 44 | $2.00 | 160M |
| Kimi K3 | Low | 30 (Coding Index 72.0, GPQA 84.2 vs 93.5 at max) | $1.15 | 22M |
| Grok 4.7 | xhigh | 46 | $3.74 | 240M |
| DeepSeek V4.1 Flash | Max | 39 (AutoBench 69, TB 27, HLE 39, LCR 84) | $0.27 | 250M · 89k/task |
| **DeepSeek V4.1 Flash** | **Non-reasoning** | **25** (AutoBench 48, TB 6, HLE 11, LCR 55) | **$0.15** | 45M · 34k/task |
| MiMo-V2.6-Pro | single reasoning version (AA: "a non-reasoning variant may also exist") | 46 | $0.13 | 140M |
| GLM-5.3-Flash · MiMo-V2.6-Flash | reasoning version, rung unlabelled | 42 · 38 | $0.25 · $0.06 | 180M · — |
| GPT 6 Luna | Max | 38 | $0.07 | — |

No AA `high` rung exists for any open model, and no AA `low` rung for any Flash model (the
`…-low` / `…-high` / `…-max` slugs for GLM-5.3-Flash and DeepSeek V4.1 Flash return 404).

### 4c. Vendor rung curves (own-model, tier C — they choose a rung, never a cross-ecosystem direction)

- **DeepSeek V4.1 Flash** (arXiv 2609.19969, §5.1.4 / §5.3.2 / Table 2, Fig. 9–12): API tiers
  `low` = effort 50, `high` = 75, `max` = 100. Effort 25 → 100 lifts the average Pass@1 of eight
  reasoning benchmarks **67.1 → 76.3**, DeepSWE v1.1 **66.0 → 74.2** and Terminal-Bench 2.1
  **82.4 → 90.6** for ~2.5× the output tokens. *"The gains are front-loaded: the 60–80 range already
  recovers most of the accuracy of the maximum setting at less than half of its token budget,
  whereas the final step to effort 100 lengthens agent trajectories by 1.6–1.8× for only marginal
  improvements. The maximum tier is thus best reserved for the most challenging tasks."* AIME 2026
  4.6k → 11.4k tokens, MathArena Apex 29.1k → 86.1k. Every model-card table is at effort 100.
- **GLM-5.3** (Z.ai private Code Bench, via explainx.ai and atoms.dev; not reproducible): `max`
  **34.5%** at ~75k output tokens, `high` **31.4%** at ~50k, GLM-5.2 `max` 23.4% at ~96k, Claude
  Opus 4.8 29.5% at ~120k. No `low` figure published.
- **Kimi K3 `low`:** GPQA Diamond 84.2% vs 93.5% at `max`; AA Intelligence Index 30 vs 44.
- **MiMo-V2.6-Flash:** a third-party gateway test found the three effort values spanned 17
  reasoning tokens — they do nothing, which is consistent with models.dev listing no variants.
- **Qwen3.8:** `low`/`medium`/`xhigh` are token caps (4,096 / 16,384 / unbounded); `high`,
  `xhigh` and `max` all behave as unbounded.

→ Router rule E7: **`D=2` takes `high`, `D=3` takes `max`** on the three `low`/`high`/`max`
models; every other pool model has a single rung to write. Claude's own curve (Opus 5.5:
low 42 @ $0.55 · medium 51 @ $1.34 · high 54 @ $1.82 · xhigh 56 @ $3.46 · max 58 @ $5.98;
Sonnet 5.5 max 56 @ $7.60) is from the iteration-19 pass and is unchanged.

## 5. Claude Code harness context (not admissible under BD1)

AA **Coding Agent Index** — a harness × model aggregate of **DeepSWE v1.1 (113 tasks),
Terminal-Bench 4.0 (66 tasks) and SWE-Atlas-QnA (124 tasks)**; AA's own page shows
"14 of 31 models" and the table is not public. The mirror `benchlm.ai/benchmarks/
aacodingagents` (captured 2026-10-05, tier B) lists: Claude Code · Sonnet 5.5 (max)
**68.4** · Claude Code · Opus 5.5 (max) **66.0** · Grok Build · Grok 4.7 **56.3** ·
**OpenCode · GLM-5.3 53.6** · Kimi Code CLI · Kimi K3 51.9 · Claude Code · Qwen3.8 Max
43.3 · Codex · DeepSeek V4 Pro 43.1 · Grok 4.6 47.0 · Codex · DeepSeek V4 Flash 38.7.
MiMo-V2.6-Pro has **no entry**. Because the index contains TB 4.0 it is not a second,
independent measurement. A 66-task TB 4.0 implies a binomial 95% interval of about
±16–17 points on a difference of two pass rates near 50% — Sonnet 5.5 vs GLM-5.3
(22 points) would clear it, Opus 5.5 vs GLM-5.3 (18) only just. **That inference is
not applied** (it assumes the index's TB 4.0 is the same 66-task set, unverified, and
AA publishes no interval); see SKILL.md §5b.

The mirror's separate "AA Agentic Index" (Fable 5.1 58 · Opus 5 56.2 · Muse 55.7 ·
GLM-5.3 53.4 · Grok 4.6 53.4 · Kimi K3 50.6 · DeepSeek V4 Pro 49.6 · MiMo-V2.5-Pro
22.7) is "display-only", has no stated composition, and is an aggregate → not used.

## 6. Name mapping and caveats

- **"Qwen3.8 Flash" (Go) = "Qwen3.8-Flash-Next" (AA)** — matched by price (USD 0.15 /
  0.47 on both) and August 2026 release, **not by name**; AA's page does not mention
  a plain "Qwen3.8 Flash". Treat as an inference.
- **"DeepSeek V4 Pro" (Go) = "DeepSeek V4 Pro 0813"** (AA, Aug 2026, 1.6T MoE, MIT).
- **"Qwen3.8 Max" (Go) = "Qwen3.8 Max (0902)"** (AA); the Agentic Index mirror lists a
  *Preview* — not used.
- MiMo-V2.6-Pro AA index spread by provider is not retrieved; first-party Xiaomi API.
- Muse Spark 1.3: AA prices (USD 1.25 / 4.25) are *not* Go prices (USD 0.10 / 0.20).

## 7. The 15 models outside the main pool

| Model | Why excluded |
|---|---|
| Grok 4.6, GPT 5.6 Luna, GLM-5.2, Kimi K2.6, MiMo-V2.5, MiMo-V2.5-Pro, Muse Spark 1.2, MiniMax M2.7, DeepSeek V4 Flash | superseded by a listed successor generation (no independent data gathered for the old ones) |
| DeepSeek V4 Flash Vision Exp | experimental vision variant (AA V4 Flash Vision 35) |
| Hy4 Preview, LongCat 2.5 Preview Free | preview / free-unlimited, unmeasured |
| LongCat-2.0 | AA 19 (USD 0.06/task) — dominated by every Flash model |
| Hy3 | AA 25 (USD 0.07/task), 256k, July 2026 |
| Space Bunny | no AA entry (only an alpha-era AI Benchy score of 7.0/10) |

## 8. Sources (all fetched 6 Oct 2026)

- `opencode.ai/docs/go/` — plan, caps, model table, retention, peak hours, ids.
- `opencode.ai/docs/models/` — variants and `variant_cycle`.
- AA same-page comparisons: `/models/comparisons/mimo-v2-6-pro-vs-{glm-5-3,
  kimi-k3, grok-4-7, deepseek-v4-1-flash, gpt-6-luna, qwen3-8-max, muse-spark-1-3,
  glm-5-3-flash, mimo-v2-6-flash, minimax-m3, kimi-k2-7-code, qwen3-7-plus,
  deepseek-v4-pro, qwen3-8-flash-next}` and
  `/models/comparisons/claude-{opus,sonnet}-5-5-vs-mimo-v2-6-pro`.
- AA model pages: `kimi-k3`, `kimi-k3-low`, `glm-5-3-flash`, `qwen3-8-flash-next`, `hy3`,
  `mimo-v2-6-pro`, earlier `glm-5-3`, `glm-5-3-low`, `deepseek-v4-1-flash`, `longcat-2-0`,
  `muse-spark-1-3`.
- AA Coding Agent Index description (`/agents/coding-agents`) and the
  `benchlm.ai/benchmarks/aacodingagents` + `/aaagenticindex` mirrors (tier B).
- `kingy.ai` GLM-5.3 / Kimi K3 / DeepSeek V4 Pro comparison — **vendor tables, not used**.

## 9. Not found / not done

- AA's own TB 4.0 evaluation page (404) → no published interval, no task count for the
  Intelligence Index's TB 4.0 run, no trial count.
- No OSWorld row for any pool model → computer-use is gated.
- No independent offensive-security row for any open model → gated.
- MiMo-V2.6-Pro on the Coding Agent Index; an AA `high` rung for any open model; an AA `low`
  rung for GLM-5.3-Flash / DeepSeek V4.1 Flash / MiMo-V2.6 (no page exists); the zentor.ai
  GLM-5.3 effort article (a TLS-intercepting proxy blocked the fetch — its Code Bench numbers
  were confirmed on two other sites instead).
- The cold-agent routing eval and the trigger eval have **not** been run for
  iteration-21 (they need live agents).

## 10. Multi-source re-analysis (6 Oct 2026) — supersedes the AA-only conclusions

§1–§9 used one independent evaluator (Artificial Analysis). That under-weighted several
models, so every routable model was re-checked against every independent source that
publishes it. **Machine-readable evidence: `opencode-evidence.json`; consensus:
`python scripts/derive_opencode_rows.py`** (mean percentile rank over ≥ 2 independent anchors
per capability; `scripts/check_opencode_pool.py` fails if a routing row emits a model outside
the top 4 of that consensus).

### 10a. Sources added
- **DeepSWE v1.1 (Mercor/Datacurve)** via `benchlm.ai/benchmarks/mercordeepswe11` — 47
  configurations, **published error margins ±6.3 to ±8.8**: Opus 5.5 72.3 ±7.3 · DeepSeek
  V4.1 Flash 71.7 ±6.3 · Sonnet 5.5 70.5 ±7.7 · GLM-5.3 70.5 ±6.3 · GPT 6 Luna 67.0 · Kimi
  K3 66.4 ±8.8 · DeepSeek V4 Pro 56.3 · Qwen3.8 Max 53.1 · Kimi K2.7 Code 30.1 · MiniMax M3
  9.1. **MiMo-V2.6-Pro, Muse Spark 1.3, GLM-5.3-Flash and Qwen3.8 Flash are not on it**
  (vendor-reported only: MiMo 71.9, Muse 75.4). Every pair within ~±7 is a *tie* — the first
  published interval this router has been able to use.
- **Arena** (`arena.ai/leaderboard/{agent,code,text}`, Oct 1–2): Agent Arena (millions of real
  long-horizon agent tasks; net outcome vs the average model), Code Arena WebDev, Text Arena.
- **Vals AI** rows via benchlm (Terminal-Bench 2.1, SWE-bench, LiveCodeBench, MMLU-Pro, GPQA) and
  further AA components not used before (MLCR-AA, ITBench, EnterpriseOps-Gym, Tau3 Banking,
  AnalystAgent, Harvey LAB, MMMU-Pro), ARC-AGI, FrontierSWE v2, CursorBench 4.0, Gray Swan IPI.
- **OpenCode usage** (`opencode.ai/data`): 7-day tokens — Muse Spark 1.3 #2 (32T), **DeepSeek V4.1
  Flash #3 (32T)**, MiMo-V2.6-Flash #4 (9.4T), GLM-5.3-Flash #8, GPT 6 Luna #13, DeepSeek V4 Pro
  #14, MiMo-V2.6-Pro #15 (439B), MiniMax M3 #18; Kimi K3, Grok 4.7, Qwen3.8 outside the top 18.
  Two-month retention: MiMo-V2.6-Pro 59.3% (60K users), GLM-5.3 52.3% (341K). Usage follows
  price and caps as much as quality — a popularity signal, not a capability one.
- `benchlm.ai` per-model pages carry **Independent / Self-reported provenance** per row; only
  independent rows enter the evidence file.

### 10b. What changed
1. **DeepSeek V4.1 Flash is the best coding consensus of the pool**, not a weak model: DeepSWE
   71.7 ±6.3 (a tie with Opus 5.5 / Sonnet 5.5 / GLM-5.3), Agent Arena 4.02 at USD 0.12 per task
   (MiMo-V2.6-Pro 3.28 at 0.10), Vals Terminal-Bench 2.1 74.5. Its AA Terminal-Bench 4.0 (27) is
   the one anchor where it lags GLM-5.3 (42) and MiMo (35). It also costs the same as
   MiMo-V2.6-Pro per task on a **USD 60 cap instead of USD 15**, and leads AutomationBench-AA (69).
   **Its flaw is factual:** AA-Omniscience hallucination rate **96.5%**, index −5.3 → gated out
   of `research-synthesis` and of the `D ≤ 1` pair for factual recall.
2. **MiMo-V2.6-Pro is not the coding default.** Independent coding rows: AA TB 4.0 (35) and Agent
   Arena (3.28); nothing else (no DeepSWE or Vals row; its 71.9 DeepSWE is vendor-reported).
   Its strength is reasoning/science (HLE 49.4, CritPt 26.6, SciCode 60.9).
3. **Kimi K3 is a contested coder, not a weak one.** AA TB 4.0 12.6 but Vals TB 2.1 **80.9
   (top)**, Agent Arena **4.18 (top open)**, AA Coding Index 76.2 (top), DeepSWE 66.4 ±8.8. The
   evaluators disagree and the router no longer treats TB 4.0 as the whole story. Kimi also leads
   AA-LCR (88.7), MMMU-Pro (80.5), Harvey LAB (94.6) and AnalystAgent (38.8) — and has the worst
   prompt-injection resistance measured (Gray Swan IPI 52.7% attack success vs Opus 5.5 1.0%,
   Muse 15.9, GLM-5.3 31.5).
4. **GLM-5.3 leads the hardest coding anchors** (TB 4.0 41.9, FrontierSWE v2 30.2) and the
   factual rows (Omniscience index 14.3 with hallucination 29.6%), but is weak in Agent Arena
   (2.36).
5. **Claude's coding lead is now corroborated:** AA TB 4.0 (59.6 / 63.6 vs best open 41.9),
   **FrontierSWE v2 (62.3 / 61.9 vs 30.2)**, **Agent Arena (13.82 / 12.52 vs 4.18)**. DeepSWE is
   a certified tie (not opposition). → BD1 now licenses a Claude direction for `agentic-code` /
   `terminal-tool`; the earlier "OpenCode †" badge there rested on a single AA row.
6. **Rows that went the other way:** `workflow-automation` (ITBench has open models ahead of Opus
   5.5: GLM-5.3-Flash 51.2 vs 38.2; AutomationBench is a tie) and `long-context` (AA-LCR open
   ahead, MLCR-AA Claude 67 / 75 vs best open 51) are *contested* → efficiency, OpenCode †.
7. **Knowledge-work:** Claude's direction stands on GDPval-AA, Briefcase and AnalystAgent;
   Harvey LAB (legal) is a tie (Kimi 94.6 vs Sonnet 93.1 / Opus 91.2).

### 10c. Consensus (output of `derive_opencode_rows.py`, routable models only, best first)
| Capability | Ranking (mean percentile, n anchors) |
|---|---|
| agentic-code / terminal-tool | DeepSeek V4.1 Flash 0.82 (4) · GLM-5.3 0.76 (5) · MiMo-V2.6-Pro 0.73 (2) · Kimi K3 0.63 (5) · Qwen3.8 Max 0.40 · Qwen3.8 Flash 0.30 · GLM-5.3-Flash 0.29 · MiMo-V2.6-Flash 0.21 (NC1: Grok 0.73, Muse 0.70) |
| deep-reasoning | MiMo-V2.6-Pro 1.00 · Kimi K3 0.71 · GLM-5.3 0.64 (NC1: Muse 0.91) |
| knowledge-work | Qwen3.8 Max 0.82 · MiMo-V2.6-Pro 0.77 · Qwen3.8 Flash 0.68 · Kimi K3 0.66 · GLM-5.3 0.59 (NC1: Grok 1.00) |
| workflow-automation | DeepSeek V4.1 Flash 0.80 · GLM-5.3-Flash 0.60 · GLM-5.3 0.59 · Kimi K3 0.56 |
| long-context | Kimi K3 0.81 · GLM-5.3-Flash 0.68 · DeepSeek V4.1 Flash 0.66 · MiMo-V2.6-Pro 0.64 · GLM-5.3 0.57 |
| research-synthesis | GLM-5.3 0.76 · MiMo-V2.6-Pro 0.62 · Kimi K3 0.61 · … · DeepSeek V4.1 Flash 0.09 (NC1: Grok 0.95) |
| science | MiMo-V2.6-Pro 1.00 · Kimi K3 0.86 · GLM-5.3 0.73 |
| doc-data-understanding | Kimi K3 0.88 (2) · Qwen3.8 Flash 0.80 (1) · MiMo-V2.6-Pro 0.50 (1) |

### 10d. Data quirks and gaps (not resolved)
- **Kimi K3: TB 4.0 12.6 (AA) vs TB 2.1 80.9 (Vals)** — different versions/harnesses; both independent.
- **Agent Arena** lists MiniMax M3 at rank 43 with 6.87% — inconsistent with its neighbours, excluded.
  Scores are *relative to the average model*, not absolute pass rates.
- **MiMo-V2.6-Pro OSWorld-Verified 82%, Qwen3.8 Max 86.1%** are vendor-reported; the only independent
  open-model OSWorld 2.0 row is MiniMax M3 at 4.6% — the computer-use gate stays.
- Scale's SWE-bench Pro page (TLS-intercepted), Vals' own site and the Arena per-model pages were not
  fetchable; Vals/Arena values come through benchlm or the leaderboard pages. SWE-bench Pro numbers
  found are vendor-reported and 30% of its public tasks are reportedly broken — unused.
- Gray Swan IPI exists for only four models; prompt-injection resistance is unknown for DeepSeek, MiMo, Qwen.
- Qwen3.8 Flash = AA/Arena "Qwen3.8-Flash-Next" by price and date, not by name.

## 11. Claude Haiku 5.5 — the first Claude model on Go (8 October 2026)

Released 7 Oct 2026 (`claude-haiku-5-5`), the same day it appeared on `opencode.ai/docs/go/`
as **`opencode-go/claude-haiku-5-5`**: cap **USD 15** (Go Plus USD 60), **30-day retention**
(abuse monitoring, like Grok / Luna), two token-price brackets at 100K. models.dev lists
effort `low · medium · high · xhigh · max` and an adaptive/disabled toggle. Machine-readable
copy: `opencode-evidence.json` → `haiku_5_5`.

**Specs (Anthropic docs, primary).** USD 0.10 / USD 0.50 per MTok up to 100k tokens,
USD 0.50 / USD 2.50 above; cache read USD 0.01; batch −50%. 1M context, 128K output, Jun 2026
cutoff, text+image in. Default effort `medium`. Tokenizer counts ~30% more than Haiku 4.5, so
the headline "−90%" is about −75% in practice (and the 100k step is a 5× jump). Thinking cannot be
disabled in Claude Code. Retirement not sooner than 7 Oct 2027; **Haiku 4.5 not sooner than 15 Oct 2026**.
Claude Code: alias `haiku` → Haiku 5.5 on the Anthropic API from **v2.1.293**; `ultracode` supported.
New safeguard classifiers (`cyber`, `bio`, `frontier_llm`, `general_harms`) can refuse — consistent with
the bio and offensive-security gates, neither of which Haiku carries.

**AA v4.3.2, same-page comparisons.** AA measured two rungs only:

| | Haiku 5.5 High | Haiku 5.5 Max | Sonnet 5.5 High | Sonnet 5.5 Max |
|---|---|---|---|---|
| Intelligence Index | 38 | 43 | 47 | 56 |
| cost / task | USD 0.08 | USD 0.21 | USD 0.88 | USD 5.46 |
| output tokens / task | 55k | 162k | 37k | 197k |
| Terminal-Bench 4.0 | 22 | 33 | 44 | 64 |
| GDPval-AA / Briefcase | 1420 / 1443 | 1620 / 1578 | 1551 / 1639 | 1839 / 1823 |
| AutomationBench | 34 | 35 | 59 | 72 |
| SciCode / HLE / CritPt | 49 / 37 / 19 | 55 / 44 / 19 | 54 / 46 / 25 | 61 / 55 / 31 |
| Omniscience / AA-LCR / GDP.pdf | 6 / 77 / 17 | 11 / 83 / 21 | 21 / 78 / 25 | 32 / 83 / 26 |

Anthropic launch table (vendor, tier A, Terminal-Bench at max): Haiku 5.5 vs Sonnet 5.5 — GDPval-AA 1620 vs 1840,
Briefcase 1578 vs 1824, OSWorld 2.1 72.4 vs 83.9 (partial credit; 37.1 for full tasks), HLE 45.9 vs 56.9,
TB 4.0 39.2 vs 70.6, Chartography 46.4 vs 61.6. Haiku 4.5 was 735 / 614 / 15.7 / 10.2 / 0.0 / 6.4.

**Against the Flash tier (AA Max vs Max).** Haiku 5.5 43 @ USD 0.21 vs GLM-5.3-Flash 42 @ 0.25,
DeepSeek V4.1 Flash 39 @ 0.27, Qwen3.8 Flash 40 @ 0.37, GPT 6 Luna 38 @ 0.07, MiMo-V2.6-Flash 38 @ 0.06. It
leads the tier on HLE (44), CritPt (19), SciCode (55), GDP.pdf (21), Briefcase (1578) and
AA-Omniscience (11), ties TB 4.0 with GLM-5.3-Flash (33) and **is last on AutomationBench (35 vs 53–69)**.
It also streams the fastest (243 tok/s). On output volume it is the heaviest: 162k tokens vs DeepSeek 89k.

**Findings.**
1. **On the Claude line Haiku 5.5 is a real cost pick.** List USD 0.10 / USD 0.50 sits at or below the Go
   Flash tier (DeepSeek USD 0.15–0.30 / 0.60–1.20, GLM-5.3-Flash 0.15 / 0.50, MiMo-V2.6-Flash 0.14 / 0.28)
   with no dollar cap to burn, and at High it is **11× cheaper than Sonnet 5.5 High for −9 index points**.
   Reading comprehension is a tie (AA-LCR 77 vs 78 High, 83 = 83 Max). → Rule H1.
2. **Its gaps are exactly the agentic and knowledge-work anchors** (TB −22, AutomationBench −25,
   GDPval −131, Omniscience −15, GDP.pdf −8 at High) → H1's exclusion list. Anthropic itself recommends
   Sonnet 5.5 / Opus 5.5 for "demanding coding assignments".
3. **`xhigh` / `max` do not pay.** Max buys +5 index for 2.6× the cost and 2.9× the tokens, and still sits 4
   points under Sonnet 5.5 High, which uses 37k tokens → E8, Haiku stops at `medium`.
4. **On Go it is dominated** (E9): High 38 @ 0.08 (cap 15, 30-day retention) vs MiMo-V2.6-Flash 38 @ 0.06
   (cap 60, 0-day); Max 43 @ 0.21 vs GLM-5.3-Flash 42 @ 0.25 — cap pressure 0.014 vs 0.0042 of the cap per
   task. `derive_opencode_rows.py` puts it mid-pack (0.53–0.67) on every capability it has ≥ 2 anchors for.
5. **No independent coding evidence beyond AA TB 4.0.** Not on Arena's Agent leaderboard; no DeepSWE,
   Vals, FrontierSWE, MLCR or MMMU-Pro row. benchlm's overall rank (#28 of 887) is a different field size
   from the pool's 784-model ranks and was not mixed in.

**Not resolved.**
- The **`low` and `medium` rungs — the only ones Rule H1 emits — are unmeasured by AA.** The cost claims
  use High (the lowest measured rung) as an upper bound by monotonicity, not as a measurement.
- **First-token time:** AA shows 26 s (High) and 415 s (Max) because hidden thinking counts; DeepSeek V4.1
  Flash streams its reasoning and shows 1.1 s. The two are not comparable, no sub-second Haiku figure exists,
  and Anthropic positions Haiku 5.5 at `low` for chat and voice agents. The `latency-volume` badge row therefore
  stays OpenCode on a measured fact and says so.
- AA's "Non-Hallucination 83%" for Haiku 5.5 (vs 84% for DeepSeek, whose hallucination rate AA elsewhere
  gives as 96.5%) is a different quantity and was not used.
- Cold-agent routing evals for the new rules have not been run (goldens are rule-derived; `--selftest` only
  proves grader ≈ goldens).

**Price drift found on the same pass.** Sonnet 5.5's cache reads were halved on 7 Oct (USD 0.20 → 0.10), so AA's
Sonnet 5.5 Max cost/task fell from USD 7.60–7.67 to **5.46**; Opus 5.5 (USD 5.98 at Max) did not move.
E1 (`Sonnet 5.5 · max` dominated by `Opus 5.5 · xhigh`, 56 @ 3.46) still holds at 1.6× instead of 2.2×.
Agent Arena cost/task refreshed: Opus 5.5 1.67, Sonnet 5.5 3.04, DeepSeek V4.1 Flash 0.13, Luna 0.07.

**Sources (fetched 8 Oct 2026).** `platform.claude.com/docs/en/models/haiku-5-5/overview`, `.../models/overview`,
`.../model-deprecations`, `.../prompting-claude-haiku-5-5`; `code.claude.com/docs/en/model-config`;
`anthropic.com/claude-haiku-5-5`; `artificialanalysis.ai/models/comparisons/claude-haiku-5-5{,-high}-vs-{claude-sonnet-5-5,deepseek-v4-1-flash,gpt-6-luna}`;
`opencode.ai/docs/go/`; models.dev `providers/opencode-go/models/claude-haiku-5-5.toml`; `arena.ai/leaderboard/agent`;
`benchlm.ai/models/claude-haiku-5-5`; kingy.ai, venturebeat.com, datacamp.com (secondary, for the Luna cross-rows).

## 12. Budget-first tiering and the OpenCode-default badge (14 October 2026, iteration-23)

**Why.** The user reported that some Go models burn their quota in a handful of tasks and asked for price-performance pairs
with as much performance as that allows; and that OpenCode should take everything up to where it stops being good enough, with
Claude recommended only where it makes a serious difference.

**Measuring burn.** Go caps are per model (§1). Two independent per-task cost figures exist for the pool:

| Model | cap | AA USD/task (Max) | % of cap per AA task | Arena p50 USD/real agent task | agent tasks per month of cap | tier |
|---|---|---|---|---|---|---|
| MiMo-V2.6-Flash | 60 | 0.06 | 0.1% | 0.04 | 1500 | B |
| GLM-5.3-Flash | 60 | 0.25 | 0.4% | 0.10 | 600 | B |
| DeepSeek V4.1 Flash | 60 | 0.27 | 0.5% | 0.13 | 462 | B |
| GPT 6 Luna | 15 | 0.07 | 0.5% | 0.07 | 214 | N |
| Qwen3.8 Flash | 30 | 0.37 | 1.2% | 0.15 | 200 | B |
| MiMo-V2.6-Pro | 15 | 0.13 | 0.9% | 0.10 | 150 | B |
| Muse Spark 1.3 | 60 | ~0.10 | 0.2% | 0.43 | 140 | N |
| DeepSeek V4 Pro | 15 | 0.67 | 4.5% | 0.32 | 47 | D |
| Qwen3.8 Max | 15 | 5.41 | 36% | 0.45 | 33 | **P** |
| GLM-5.3 | 15 | 2.01 (Low 0.85) | 13% (6%) | 0.66 | 23 | **P** |
| Kimi K3 | 15 | 2.00 (Low 1.15) | 13% (8%) | 0.72 | 21 | **P** |
| Grok 4.7 | 15 | 3.74 | 25% | 1.54 | 10 | **P** |

Both columns split the pool the same way, with a wide gap (35 → 140 tasks per month; 1.2% → 5.7% of the cap per task), so the tier boundary
is not sensitive to which cost figure is used. The 5-hour window is 20% of the cap: one GLM-5.3 AA task at Max uses ~67% of it, one DeepSeek V4.1 Flash
task ~2%. Arena p50 costs are list-price token costs on real agent traces; they are an order of magnitude, not a quote.

**What the tiering changes.** Premium models leave every routed pair (Rule BUD1) and return only as `#2` through A1-OC. Pairs are the
consensus *inside* the budget tier (`scripts/derive_opencode_rows.py`, percentiles taken among budget + NC1 models; the premium consensus is
printed beside it for reference). Where the budget tier is weak, it is weak: the deep-reasoning `#2` is GLM-5.3-Flash (HLE 40, CritPt 15) because the
rest of the tier is lower still (HLE 35–39), and the knowledge-work pair is a three-way tie at 0.83 (MiMo-V2.6-Pro, Qwen3.8 Flash, and Muse Spark under NC1).
Only one budget model (MiMo-V2.6-Pro) has strong reasoning evidence, which is why it leads four rows.

**The badge threshold (Rule SM1).** The earlier badge asked "does Claude lead on independent evidence?" — and for coding and knowledge-work the answer was
yes at every depth. The new question is "is the lead serious *at this depth*?":

- Claude's lead on coding sits on the hardest anchors — AA Terminal-Bench 4.0 (Sonnet 5.5 64, Opus 5.5 60 vs best budget 35), FrontierSWE v2 (62 vs 18),
  Agent Arena (13.8 / 12.5 vs 4.0). On DeepSWE v1.1, which publishes ±6–9 per row, DeepSeek V4.1 Flash 71.7 ties Opus 5.5 72.3 and Sonnet 5.5 70.5.
  Reading DeepSWE as mid-difficulty work and TB 4.0 / FrontierSWE as the hardest work gives the `D = 2` → OpenCode, `D = 3` → Claude split.
  This is an interpretation of which task depth each benchmark represents, not a measured crossover, and it is the single softest step in the rule.
- Deep reasoning (HLE 61 / 55 vs 49, CritPt 32 / 31 vs 27, ARC-AGI-2 92 vs 61) bites at `D = 3`.
- Finished deliverables (GDPval-AA 1866 / 1839 vs 1686, Briefcase 1807 / 1823 vs 1583, AnalystAgent 56 / 58 vs 39) are wide and consistent across
  three AA rows, so `knowledge-work` stays Claude from `D = 2`.
- Every `D ≤ 1` task is OpenCode, including the ones Haiku 5.5 handles (the Claude line still names Haiku). This reverses iteration-22's
  Haiku tie-break on purpose: the user's priority is Claude quota, and DeepSeek V4.1 Flash costs about the same per task as Haiku 5.5 at Max (USD 0.27 vs 0.21 per AA task).
- After a stated OpenCode shortfall at `D ≥ 2` the badge goes to Claude whenever the dominant capability has a BD1 direction (A1-OC).

**Not changed.** Efforts (the `max` that was expensive was GLM-5.3 / Kimi K3; on the Flash tier it is USD 0.25–0.27 per AA task), gates, retention rules,
the Claude arm and all Claude-side evidence. `benchmarks.json` / frontiers are untouched.

**Open.** (1) No cold-agent run of the 30 goldens yet. (2) The D=2 / D=3 split above is policy on top of the evidence; if it should move, change one row
of the badge table in `SKILL.md` and its mirror in `evals/policy/routing_policy.json`. (3) MiMo-V2.6-Pro now appears in the `agentic-code` pair on two AA/Arena
anchors only (it has no DeepSWE or Vals row) — the weakest-evidenced pick in the new coding pairs.

## 13. Free models and the Gemini line (20 October 2026, iteration-24)

Trigger: the user wanted (a) the free OpenCode models benchmarked and used where they fit, and (b) the Gemini entitlement from their Google membership
used where Gemini stands out. Everything below was read from the cited page on 2026-10-20; `skill/opencode-evidence.json` → `iteration_24` holds the numbers.

### 13.1 What the Go page looks like now (opencode.ai/docs/go, 29 models)

New against the 8 Oct list: **Gemini 4 Argon Contributor** (USD 60 / 240, *Not ZDR — prompts may be used to train Google models*, 2× promo), **MiniMax M3.1 Flash Free**
(Unlimited / Unlimited, 0 days, limited time), **Beam Free** (Unlimited, 30 days, limited regions), **LongCat 2.5 Preview Free**, **Step 5 Preview** (USD 60, 4× promo).
**DeepSeek V4.1 Flash's cap rose USD 60 → 80** (tasks/month 462 → 615, still budget). No longer listed: DeepSeek V4 Flash, its Vision Exp, Space Bunny.

### 13.2 The Zen free list, model by model

The page gives no rate limits and no end dates ("limited time"). A third-party probe of the free tier (12 Oct, one run per cell, harness bugs documented by its author — low weight)
saw no 429 at 12 concurrent calls, found `exo-free` returning HTTP 410, and scored `longcat-2.5-preview-free` 3/4 (it mis-summed a structured-output task).

| Free model | What it is | Data | Independent evidence | Verdict |
|---|---|---|---|---|
| **MiniMax M3.1 Flash Free** | `minimax/MiniMax-M3.1-Flash` (models.dev base), Go + Zen | zero retention, no training | **AA II 43**, AutomationBench-AA 73, TB 4.0 26, HLE 48, CritPt 22, SciCode 53, AA-LCR 80, GDP.pdf 21, MMMU-Pro 79.1, USD 0.22/task, 116 tok/s, TTFT 1.2 s; **hallucination rate 92.8%** (index 15.6) | **Routed (tier F)** — FR1 |
| GLM-5.3-Flash Free | twin of paid `zhipuai/glm-5.3-flash` | zero retention | = the paid model (II 42) | Twin: named as spill-over, never a pick |
| DeepSeek V4.1 Flash Free | twin of paid `deepseek/deepseek-v4.1-flash`, **200k context / 32k output** | zero retention | = the paid model (II 39) | Twin (same) |
| MiMo-V2.6-Flash Free | twin of `xiaomi/mimo-v2.6-flash` | **may be used to improve the model** | = the paid model (II 38) | Twin, NC1 only |
| LongCat 2.5 Preview Free | Meituan preview, 1M context | zero retention | none (AA page 404; vendor figures only) | Unmeasured — never selected |
| Beam Free | unknown | 30 days, **region-restricted** | none found | Unmeasured |
| Big Pickle / LL Alpha Free / Exo Free | stealth models (identity undisclosed) | **trains** (LL Alpha: 30 days) | Big Pickle's SWE Atlas 50.8 is self-reported, single trial | Unmeasured; Exo is HTTP 410 |
| MiMo-V2.5 Free | older MiMo generation | trains | none at v4.3.2 | Never selected |
| Nemotron 3 Ultra Free | NVIDIA 550B-A55B | **logged; "do not submit confidential data"** | **AA II 23 at v4.3.2** (TB 4.0 1, AutomationBench 3) | Dominated by every budget model |
| Nemotron 3.5 Lightning / Super VL Free | NVIDIA | same | Lightning II 24 at *v4.1.1* — not comparable | Never selected |
| Jev 1.13 Free | TypeSafe AI, `/v1/systemone` | — | not a text generator ("structured-decision model") | Not applicable |

**Why only M3.1 Flash joined the pool.** It is the only free model that has both a v4.3.2 row and a data policy compatible with the user's confidential default. On the
Flash tier it leads AutomationBench-AA (73 vs DeepSeek 69), HLE (48 vs 39–40), CritPt (22 vs 14–15) and SciCode (53 vs 51–52) and ties MMMU-Pro, with no cap pressure.
It has **no** DeepSWE / Agent Arena / Vals row, so it cannot lead `agentic-code` (the consensus needs ≥ 2 anchors) — its place is `deep-reasoning` / `science` as `#2` and
`doc-data-understanding` as `#1`. Its hallucination rate (92.8%) is the same failure as DeepSeek V4.1 Flash (96.5%), so the factual-recall gate removes both. It is limited-time:
FR1 records the rows it replaced (GLM-5.3-Flash as `#2`; Qwen3.8 Flash · MiMo-V2.6-Pro for doc-data) so delisting is a one-line revert.

### 13.3 Gemini 4 Argon

Model card 13 Oct 2026 (announced 30 Sep); natively multimodal (text, image, audio, video in; text out); 1,048,576 tokens combined; knowledge cutoff March 2026; **API is paid-tier only
(Tier 1 = billing linked); a free-tier key gets `429 "limit: 0"`**; `thinking_level` `low`/`medium`/`high`, default `medium`, `max` → HTTP 400; USD 2 / 10 per MTok through 30 Nov, **4 / 20 from 1 Dec**.

| Measure (AA v4.3.2 unless noted) | Gemini 4 Argon (High) | MiMo-V2.6-Pro | Sonnet 5.5 | Opus 5.5 |
|---|---|---|---|---|
| Intelligence Index / USD per task | **53** / 1.99 | 46 / 0.13 | 56 (Max) / 5.46 | 58 (Max) / 5.98 |
| Terminal-Bench 4.0 | 57.1 (Vals 57.6) | 35 | 63.6 | 59.6 |
| FrontierSWE v2 (Proximal) | 55.0 | — (GLM-5.3: 30) | 61.9 | 62.3 |
| HLE / CritPt / ARC-AGI-2 | 57.1 / 27.1 / 91.3 | 49 / 27 / — | 55.0 / 31.4 / — | 61.4 / 31.7 / 91.7 |
| **AutomationBench-AA** | **77.5** | 59 | 71.8 | 69.5 |
| **AA-Omniscience index / hallucination rate** | **42.4 / 15.1%** | 8.4 / 40.6% | 32.3 / 47.0% | 46.4 / 58.6% |
| GDPval-AA / Briefcase / AnalystAgent | 1623 / 1486 / 48.8 | 1686 / 1516 / — | 1839 / 1823 / 57.5 | 1866 / 1807 / 56.3 |
| AA-LCR / GDP.pdf / SciCode | 79.7 / 21.8 / 61.8 | 86.3 / 19.2 / 60.9 | 82.7 / 25.8 / 61.0 | 84.7 / 26.2 / 66.9 |
| Speed / TTFT | 84 tok/s / **48.6 s** | 49 / 3.2 s | — | — |

**Where it stands out (and so where GM1 uses it):** factual reliability (the lowest hallucination rate and, bar Opus 5.5, the highest Omniscience index of any model rated here),
AutomationBench-AA (highest of all), deep-reasoning parity with Opus on ARC-AGI-2 (independent), and the far-best non-Claude option on terminal / agentic coding.
**Where it does not:** finished deliverables (GDPval / Briefcase / AnalystAgent are *below* MiMo-V2.6-Pro or Claude), the Claude coding lead (TB 4.0, FrontierSWE v2, and Google's
own table has Opus 5.5 66.4 vs 57.4), long-context reading (AA-LCR 79.7), TTFT (48.6 s at High), and price (USD 1.99 per AA task, 3.98 from 1 Dec).
Vendor-only rows (Google's DeepSWE 77.9, GraphWalks 84.2, OSWorld-2.0 69.2, Gray Swan 0.7) are tier A *vendor_relative* and enter no rule. Independent Kubernetes-manifest
test of one blog (n = 12): none served HTTP 200 (Opus 5.5 3/3) — noted, not weighted.

**Cost reality.** At AA's USD 1.99 per index task, one month of AI Pro's USD 10 credit buys about five such tasks (about half that after 1 Dec); a real agent task is cheaper (Arena p50
runs 0.33–0.77× AA cost for the other models; Argon has no Arena row). That is premium-tier arithmetic, which is why BUD1 keeps Argon out of `D ≤ 2 ∧ R ≤ 2` pairs and GM1 spends it
only on the five rows where it leads, at `D = 3` / `R = 3`.

### 13.4 The Google membership, and the "server load" error

*Background only since 26 Oct: the user cannot use the membership in OpenCode, so the router relies on Go's Contributor route alone.*

- **The subscription does not include an API key or API quota.** Google AI Pro (USD 19.99) carries Google Developer Program premium benefits: **USD 10/month of Google Cloud credits**
  usable on the Gemini API (AI Ultra: USD 100). They are *not automatic* — activate at developers.google.com/program/my-benefits and choose a billing account; credits expire after
  12 months; one source says a positive prepaid balance may still be required (unverified). Attaching billing moves the key to the **paid tier**.
- **Paid tier:** content is not used to improve Google products; prompts and responses are logged "for a limited period" (unspecified) for misuse detection. **Free tier:** used to improve
  products, human reviewers may read it. The user chose to treat the paid tier like Claude (confidential work allowed) — see the Step 1 confidential row.
- **Third-party login is the risky route.** Google's Antigravity FAQ calls using third-party software with an Antigravity login a Terms-of-Service violation that "can result in suspension or
  termination"; a forum report (19 Feb 2026) has an AI Pro account suspended after one day of OpenCode + Gemini CLI use (no Google reply on the page; outcome unknown). Google recommends an
  AI Studio / Enterprise API key for third-party agents. The router never recommends the OAuth route (Step 7 rule 11).
- **The overload error.** Not reproducible from here (no Gemini key). Two different failures look alike: a **503** is Google-side capacity (retry with exponential backoff, or switch Pro → Flash — Google's own
  advice), and a **429 `limit: 0`** on Argon means the key is free-tier (Argon has none). One independent 9-call test on a paid key saw no 503 and no capacity error; the model card lists
  "hallucinations, occasional slowness, and timeouts" as known limitations and Google suggests 15-minute client timeouts for hard prompts. Rule 11 therefore names both.
- **Gemini 3.8 Flash** (41 @ USD 1.24 per AA task; USD 0.75 / 3.75 through 31 Dec, 1.50 / 7.50 after; has a free tier that trains) is dominated by MiMo-V2.6-Pro on index per dollar (E10); it stays as Argon's fallback.

### 13.5 What changed in the rules

**26 Oct revision — Go's Contributor route is the only Gemini route.** The user cannot use their Google membership inside OpenCode (no OAuth route, no API key in use), so the paid-API assumptions above (confidential work allowed, USD 10/month credits, 503/429 diagnosis, Gemini 3.8 Flash fallback) no longer apply to the router. Argon is `opencode-go/gemini-4-argon-contributor`: Google trains on prompts, so it is **NC1-only**; GM1 is an overlay (right-hand column at `D = 3` / `R = 3` on five rows, `#2` after a shortfall), not a table entry; the confidential default reverts to the pre-GM1 pairs; `research-synthesis` at `R = 3` is Claude † by default and OpenCode † under NC1+Argon. The §13.4 facts stay as background.

**21 Oct follow-up (effort):** the user noticed DeepSeek V4.1 Flash `max` almost never appeared (16 golden DeepSeek picks: 9 `low`, 6 `high`, 1 `max`) — `max` only fired at `D = 3`, and GM1 had moved `D = 3` to Argon. E7 is now `D ≥ 2 → max` on DeepSeek V4.1 Flash, GLM-5.3-Flash and MiniMax M3.1 Flash Free: the only independent measurement of these models is at `max` (DeepSeek non-reasoning 25 → 39 at `max`), `high` had only vendor curves, and `max` costs USD 0.25–0.27 per AA task (about 0.3% of the USD 80 cap). `D ≤ 1` stays `low`.

FR1 (free lane) and GM1 (Gemini slot) are new; BUD1, NC1, CAP1 and A1-OC were reworded; badge row `research-synthesis` at `R = 3` flipped Claude † → OpenCode † (with Argon the OpenCode line beats the
Claude pick on both Omniscience measures); the DeepSeek cap is USD 80; the pool is 19. Mirror: `evals/policy/routing_policy.json` (`gm1_rows`, `free_lane`, `pool.models`). Goldens: 34 evals
(d1/g1/j1/t1/v1/z1/p1/n1/r1 moved; w1–w4 new). `grade_routing.py` rejects a Gemini model on the OpenCode line unless the eval sets `allow_gemini`, and rejects any free model other than M3.1 Flash Free.

**Cold-agent run.** 6 fresh agents read only `SKILL.md`: 33/33 routed evals pass after two corrections (`w2`: NC1 ambiguity → Muse Spark `#2` on `research-synthesis` only; `r1`: prompt sharpened). `i1` was refused by its agent and not re-run; `k1`/`l1` were routed by an agent that had seen other result files (gates are deterministic).

**Open.** (1) `i1` not cold-tested this iteration. (2) Argon's `medium` rung (the default) has no independent figure. (3) M3.1 Flash Free has no
independent coding row and its free status is time-limited. (4) The Antigravity ban report is one forum post. (5) Whether the AI Pro credit needs a prepaid balance is one blog's claim.

**Sources (read 2026-10-20).** opencode.ai/docs/go · opencode.ai/docs/zen · opencode.ai/v2/docs/console/models · opencode.ai/docs/providers · models.dev (`providers/opencode-go/models/gemini-4-argon-contributor.toml`,
`minimax-m3.1-flash-free.toml`; `providers/google/models/gemini-4-argon.toml`; `providers/opencode/models/{glm-5.3,deepseek-v4.1,mimo-v2.6}-flash-free.toml`) · deepmind.google/models/model-cards/gemini-4-argon ·
artificialanalysis.ai (Argon page; comparisons vs MiMo-V2.6-Pro for Argon, Gemini 3.8 Flash, Nemotron 3 Ultra, MiniMax M3.1 Flash) · benchlm.ai/models/{gemini-4-argon,minimax-m3-1-flash} ·
ai.google.dev/gemini-api/{pricing,terms} · blog.google …/gdp-premium-ai-pro-ultra · developersdigest.tech and smartscope.blog (credits) · discuss.ai.google.dev (suspension thread; 429/503 handling) ·
computingforgeeks.com and eesel.ai (Argon API hands-on) · github.com/digithings-ai/digithings PR 5494 (free-tier probe).
