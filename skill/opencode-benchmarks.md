# OpenCode Go evidence — iteration-21

**Audit data for the OpenCode arm of `SKILL.md`. Never load this to route a prompt;
every rule needed is in `SKILL.md`.** Verified **6 October 2026**. Everything below
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
- Page lists **30 models**. The 15 "main" models are in §2; the other 15 are in §7.
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
- The page says **nothing** about reasoning-effort variants. OpenCode's own docs
  (`opencode.ai/docs/models/`) describe `variant_cycle` and per-provider variants
  (Anthropic high/max; OpenAI none…xhigh; Google low/high) — no per-model list for
  the Go models. Hence the router's two-rung vocabulary (§4).

## 2. The 15 main models

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
MiMo-V2.6-Flash, Kimi K2.7 Code `n/p` · Qwen3.7 Plus ≥ 256k (tier boundary).

Input modalities (AA): **text-only GLM-5.3**; text+image Kimi K3, GLM-5.3-Flash,
Grok 4.7, GPT 6 Luna, Qwen3.8 Max; text+image+video Qwen3.8 Flash, MiniMax M3, Muse
Spark 1.3; MiMo-V2.6-Pro takes text, image, speech and video. Only *DeepSeek V4 Flash
Vision Exp* is marked vision on the Go page. MiMo-V2.6-Flash `n/p`.

## 3. Findings the numbers force (several contradict the earlier draft)

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

## 4. Effort evidence

| Model | Rung | II | cost/task | tokens (index run) |
|---|---|---|---|---|
| GLM-5.3 | Max | 45 | $2.01 | 210M out (verbose) |
| GLM-5.3 | Low | 34 | $0.85 | 88M |
| Kimi K3 | Max | 44 | $2.00 | 160M |
| Kimi K3 | Low | 30 | $1.15 | 22M |
| Grok 4.7 | xhigh | 46 | $3.74 | 240M |
| DeepSeek V4.1 Flash | Max | 39 | $0.27 | 250M |
| MiMo-V2.6-Pro | (single reasoning version; AA notes a non-reasoning variant "may exist") | 46 | $0.13 | 140M |
| GPT 6 Luna | Max | 38 | $0.07 | — |

No `medium` / `high` rung is published for any open model. → **never interpolate.**
Claude's own curve (Opus 5.5: low 42 @ $0.55 · medium 51 @ $1.34 · high 54 @ $1.82 ·
xhigh 56 @ $3.46 · max 58 @ $5.98; Sonnet 5.5 max 56 @ $7.60) is from the
iteration-19 pass and is unchanged.

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
- MiMo-V2.6-Pro on the Coding Agent Index; MiMo-V2.6-Flash context window and
  modalities; effort rungs between `low` and `max`.
- The cold-agent routing eval and the trigger eval have **not** been run for
  iteration-21 (they need live agents).
