---
name: model-secici
description: >-
  Routes a prompt: which model + effort on Claude (Haiku 5.5 / Sonnet 5.5 /
  Opus 5.5 / Opus 4.8 / Fable 5.1) and on OpenCode (two models out of the 20 it
  rates — the Go budget tier and Go's Gemini 4 Argon (non-confidential work only) —
  each with an effort), and which ecosystem to use — OpenCode by default, Claude
  where it makes a serious difference. Use for "which model / effort / AI should
  I use" or /model-secici.
---

# Claude & OpenCode model / effort router

<!-- routing-policy-version: iteration-25 -->

Route the user's prompt — **do not run it**. Say which model + effort to use on
**Claude** and on **OpenCode** (**two** models, `#1` / `#2`, each with its own
effort), then mark one ecosystem `✅ RECOMMENDED AI` — **OpenCode unless Claude makes a
serious difference** (Rule SM1).

**Principle.** Errand work and everything OpenCode can do well goes to OpenCode,
on the **price-performance tier** of the Go pool; Claude is recommended only where
it makes a serious difference. Inside each arm pick the lowest-quota model × effort
that stays on the task's capability frontier. Protected resources: Claude's 5-hour
window and each Go model's **own** dollar cap (plan USD 10/month; 5-hour window =
20% of a model's cap, weekly 50%) — four Go models burn theirs in a handful of tasks
and are kept out of the default pairs (Rule BUD1). Gemini 4 Argon is
reachable on Go only through a route whose cap and data policy are unread, so it serves
non-confidential hard cases only (Rule GM1). The free lane is empty since the MiniMax M3.1 Flash
Free promo ended (Rule FR1). When in doubt, round **down**.

**Run Steps 0–6 in one pass, silently.** If Step 0 is clean and no gate fires,
score once — do not re-derive. Emit only the output lines. `opencode-benchmarks.md`
and `reference.md` (its Codex §9/§18 are stale) are audit data — never load them
to route.

**Claude roster (27 Oct 2026 — no Claude model has shipped since Haiku 5.5):**

| Model | Role |
|---|---|
| **Haiku 5.5** | **Cost pick** for small, shallow work (Rule H1). USD 0.10/USD 0.50 per MTok up to 100k tokens (USD 0.50/USD 2.50 above), 1M context, effort `low`…`max`, API default `medium`. AA: High 38 @ USD 0.08, Max 43 @ USD 0.21 against Sonnet 5.5 High 47 @ USD 0.88 |
| Haiku 4.5 | Legacy — **never selected** (retires "not sooner than 15 Oct 2026") |
| Sonnet 5.5 | Daily work, **default start**. USD 2/USD 10, 1M |
| **Opus 5.5** | **Flagship** for complex agentic code. USD 4/USD 20, 1M, API default effort `medium` |
| Opus 4.8 | Legacy — only role: the offensive-security gate |
| **Fable 5.1** | Frontier scale (1000+ files), biology-adjacent R&D. USD 10/USD 50 |
| Mythos 5.1 | = Fable 5.1, permissive safeguards, **Glasswing invite only** |

**OpenCode pool — the 20 rated models** (plan: Go, USD 10/month; read 20 Oct 2026, roster changes of 22–24 Oct from the models.dev log). `II` = AA
Intelligence Index v4.3.2 (Max unless noted), `TB` = AA Terminal-Bench 4.0,
`USD/task` = AA cost per index task, `cap` = Go monthly cap per model (`—` = no Go cap),
`tasks/mo` = `cap ÷ Arena p50 cost per real agent task` (order of magnitude: how many real
tasks one month of that model's cap buys). Tier: **B** budget, **P** premium (Rule BUD1), **G** Gemini (non-confidential hard cases
only, Rule GM1), **N** non-confidential only (NC1), **U** unrouted (rated, Go cap unread), **D** dominated. Full data, contexts and
sources: `opencode-benchmarks.md`.

| # | Model | II | TB | USD/task | cap | tasks/mo | tier | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | **MiMo-V2.6-Pro** | **46** | 35 | **0.13** | 15 | 150 | B | Best index per dollar; leads HLE / CritPt / SciCode and AA TB 4.0 in the budget tier; no independent coding row beyond AA / Arena; takes images; **no effort variant** |
| 2 | **GLM-5.3** | 45 | **42** | 2.01 | 15 | 23 | **P** | Best open coder (TB 4.0, FrontierSWE v2), lowest hallucination — ~13% of its cap per AA task. Text-only |
| 3 | Kimi K3 | 44 | 13 | 2.00 | 15 | 21 | D | **Dominated** by Kimi K3.1 Pro (same Go cap and price, index +11, adds `low` / `high`). Best AA-LCR / MMMU-Pro of its generation; weak prompt-injection resistance; `max` only |
| 4 | **Grok 4.7** | 46 | 26 | 3.74 | 15 | 10 | **P** | Knowledge-work leader; ~25% of its cap per AA task; **30-day retention**; 500k context |
| 5 | **Muse Spark 1.3 Contributor** | **48** | 33 | ~0.10 | 60 | 140 | N | **Trains on your prompts** — NC1 only |
| 6 | **GLM-5.3-Flash** | 42 | 33 | 0.25 | 60 | 600 | B | **`D ≤ 1` #1**; text + image |
| 7 | **MiMo-V2.6-Flash** | 38 | 23 | **0.06** | 60 | 1500 | B | Cheapest; no effort variant |
| 8 | **DeepSeek V4.1 Flash** | 39 | 27 | 0.27 | 80 | 615 | B | **Best coding consensus** (DeepSWE 71.7 ±6.3, Agent Arena 4.02 at USD 0.13); AutomationBench 69; 222 tok/s; **hallucination 96.5% — never for factual recall**; peak hours 2×; cap raised to USD 80 |
| 9 | **GPT 6 Luna** | 38 | 13 | 0.07 | 15 | 214 | N | Fast bulk; **30-day retention**; never agentic |
| 10 | **Qwen3.8 Flash** | 40 | 25 | 0.37 | 30 | 200 | B | Briefcase 1583 → knowledge-work #2; 256k context; takes images |
| 11 | **Qwen3.8 Max** | 45 | 39 | 5.41 | 15 | 33 | **P** | ~36% of its cap per AA task; A1-OC only |
| 12 | DeepSeek V4 Pro | 36 | 14 | 0.67 | 15 | 47 | D | **Dominated** by V4.1 Flash |
| 13 | MiniMax M3 | 29 | 2 | 0.51 | 60 | — | D | **Dominated** |
| 14 | Kimi K2.7 Code | 26 | 1 | 0.54 | 60 | — | D | **Dominated** |
| 15 | Qwen3.7 Plus | 25 | 1 | 0.22 | 60 | — | D | **Dominated** |
| 16 | Claude Haiku 5.5 | 43 | 33 | 0.21 | 15 | — | D | **Dominated** on Go (E9): mid-pack on every independent anchor, 30-day retention. Its home is the Claude line (H1) |
| 17 | **Gemini 4 Argon** | **53** (High) | 57 | 1.99 | n/p | — | **G** | **Go route since 24 Oct** (`opencode-go/gemini-4-argon`; the Contributor route is deprecated): list USD 4/20 per MTok, promo USD 2/10 to 30 Nov, 2× from 1 Dec. **Go cap and data policy of this route unread** — kept NC1-only. Highest AutomationBench-AA (77.5); Omniscience 42, hallucination 15% (lowest rated); HLE 57; TTFT 48 s; `low`/`medium`/`high`. Rule GM1 only |
| 18 | Gemini 3.8 Flash | 41 (High) | 20 | 1.24 | — | — | D | **Dominated** (E10): 41 @ USD 1.24 vs MiMo-V2.6-Pro 46 @ 0.13; not offered on Go |
| 19 | MiniMax M3.1 Flash | 43 | 26 | 0.22 | n/p | — | U | **Unrouted.** Free promo deprecated 22 Oct; the paid `opencode-go/minimax-m3.1-flash` (USD 0.15/0.60 per MTok) arrived the same day and its Go cap is unread. Same base model, so the anchors stand: AutomationBench-AA 73, HLE 48, CritPt 22, SciCode 53; 1M; takes images. **Hallucination 92.8% — never for factual recall.** Re-enters the budget tier once a cap is read |
| 20 | **Kimi K3.1 Pro** | 55 | 67 | 2.11 | 15 | — | **P** | Live on Go since 23 Oct; supersedes Kimi K3 (44). AA TB 4.0 67 (mini-swe-agent), HLE 53, SciCode 61, GDPval-AA 1846; ~14% of its cap per AA task (150M output tokens, verbose); 1M, text + image + video; `low`/`high`/`max`. **Unverified:** the AA pages and the Go docs page were unreachable — the cap and 0-day retention come from a search summary |

<!-- rule:BUD1 -->
**BUD1 · budget-first pool.** The four premium models — GLM-5.3, Kimi K3.1 Pro, Grok 4.7 and Qwen3.8 Max, each buying at most 35 real agent tasks per month of its Go cap (Kimi K3.1 Pro has no Arena figure yet: about 14% of its cap per AA task, so roughly 7) — are never `#1` or `#2` of a routed pair. They reach the OpenCode line only through Rule A1-OC, after the user states that an earlier OpenCode run fell short. Every other pair is built from the budget tier (140 or more tasks per month) — the free lane of Rule FR1 is empty — and, under NC1, GPT 6 Luna, Muse Spark 1.3 Contributor and Gemini 4 Argon where Rule GM1 allows it.
<!-- /rule:BUD1 -->

<!-- rule:FR1 -->
**FR1 · free lane.** The free lane is empty since 22 Oct: MiniMax M3.1 Flash Free was deprecated, and its paid successor MiniMax M3.1 Flash has no Go cap read yet, so it is rated but never emitted. The rows that used it are back on their fallbacks — `deep-reasoning` and `science` take GLM-5.3-Flash as `#2`, `doc-data-understanding` is Qwen3.8 Flash · MiMo-V2.6-Pro. Zen's free twins of paid Flash models (`glm-5.3-flash-free`, `deepseek-v4.1-flash-free`: same base models, zero retention, no training; the DeepSeek twin has a 200k window) are never `#1` or `#2` — when the user says a paid Flash window is exhausted, `Evidence:` names the twin before the CAP1 chain. `mimo-v2.6-flash-free` trains on prompts (NC1 spill-over only). Every other free model, Iceman Contributor Free included, is never selected.
<!-- /rule:FR1 -->

<!-- rule:GM1 -->
**GM1 · Gemini slot.** Gemini 4 Argon is reachable on Go as `opencode-go/gemini-4-argon` (since 24 Oct; the Contributor route is deprecated), but the Go cap and the data policy of that route have not been read, so it exists only under NC1 and never takes a slot at `D ≤ 2` with `R ≤ 2`. Under NC1, in the right-hand column (`D = 3` or `R = 3`) it is `#1`, effort `high`, on `agentic-code`, `terminal-tool`, `deep-reasoning`, `research-synthesis` and `workflow-automation` — the rows where independent evidence puts it above the budget tier — and the row's former `#1` becomes `#2`. After an OpenCode shortfall at `D ≥ 2` under NC1 it is `#2` on the same rows (Rule A1-OC). Confidential work, the default, never sees it: read the rows without it. If it errors or is overloaded, run the row's other model.
<!-- /rule:GM1 -->

Rows 3, 12–16, 18 and 19 are rated but never emitted; tier **P** only through A1-OC — if a task already runs on one,
name the budget model that replaces it. DeepSeek's zero-retention agreement is **renewed monthly (valid
through 31 Oct 2026)**. **Never selected** (legacy, preview, unmeasured or free-and-unmeasured): Grok 4.6,
GPT 5.6 Luna, GLM-5.2, Kimi K2.6, MiMo-V2.5 (+ Pro, Free), Muse Spark 1.2, MiniMax M2.7, Hy4 Preview,
LongCat-2.0, Hy3, Step 5 Preview, Beam Free, LongCat 2.5 Preview Free, Big Pickle, LL Alpha Free, Exo Free, Iceman Contributor Free,
Jev 1.13, Nemotron 3 Ultra / 3.5 Lightning / 3.5 Super VL Free. Model ids: `opencode-go/<id>` (Zen free
twins `opencode/<id>`).

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

1. **`ultracode` is a Claude Code setting, not a model effort level**: it sends `xhigh` and adds
   workflow orchestration, on every `xhigh` model except Haiku 5.5.
2. **Haiku 5.5 has effort** (`low`…`max`; thinking always on in Claude Code). The router writes only
   `low` or `medium` (Rule E8).
3. Effort is a behavioural signal, not a token budget. Opus 5.5 defaults to `medium` and Sonnet 5.5's
   rungs are recalibrated, so the written effort is always explicit. Anthropic's Sonnet 5.5 start
   points: `medium` for well-specified agentic coding, `high` for harder or longer work.
4. **Effort is not the primary quality dial.** A stronger model at a lower rung often beats a weaker
   model at a higher one on quality *and* quota — Rules E1–E3.

### OpenCode Go

OpenCode shows only the effort **variants its model catalogue (models.dev, `opencode-go`
provider, read 6 Oct 2026; Claude Haiku 5.5 added 8 Oct, Gemini 4 Argon 20 and 24 Oct, MiniMax M3.1 Flash 22 Oct, Kimi K3.1 Pro 23 Oct) lists for each model** — and they differ:

| Model | Variants OpenCode offers | Emit |
|---|---|---|
| GLM-5.3 · GLM-5.3-Flash · DeepSeek V4.1 Flash | `low` · `high` · `max` | `D ≤ 1` `low` · `D ≥ 2` `max` |
| MiMo-V2.6-Pro · MiMo-V2.6-Flash | **none** — thinking is always on | `default` |
| Kimi K3 | `max` only | never emitted (dominated) |
| Kimi K3.1 Pro | `low` · `high` · `max` (default `max`) | `max` (A1-OC only, `D ≥ 2`) |
| Grok 4.7 | `low` · `medium` · `high` · `xhigh` | `xhigh` (the rung AA measured) |
| Qwen3.8 Flash · Qwen3.8 Max | `low` · `medium` · `xhigh` (+ toggle, token budget) | `xhigh` (the API default) |
| GPT 6 Luna | `none` … `max` | `low` (latency row only) |
| Muse Spark 1.3 Contributor | `minimal` … `xhigh` | `xhigh` (NC1 only) |
| Claude Haiku 5.5 | `low` … `max` | never emitted (Rule E9) |
| MiniMax M3.1 Flash | `low` … `max` | never emitted (unrouted) |
| Gemini 4 Argon | `low` · `medium` · `high` (`max` → HTTP 400) | `high` (the rung AA measured) |
| Gemini 3.8 Flash | — | never emitted (Rule E10) |

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
| Sub-second latency **or** high-volume classification/parsing (at `D ≤ 1`) | Deciding | **Haiku 5.5**, effort `low`. Stop (Rule H2 overrides it after a Haiku shortfall) |
| **Offensive security:** exploit generation, penetration testing, binary-based vulnerability scanning | Deciding | **Opus 4.8**, effort floor `xhigh` (W/duration can still raise it to `ultracode`) — with Glasswing access, **Mythos 5.1** |
| **Biology-adjacent R&D:** genomics, protein/chemistry-heavy pipeline, bio-CTF | Deciding | **Fable 5.1** (default effort `high`, no floor) |
| **1000+ files / whole-codebase scale** | Deciding | **Fable 5.1** |

### OpenCode arm

| Condition | Kind | Result |
|---|---|---|
| **Offensive security** (same definitions) | Deciding | **"use Claude"** — the only open-model offensive evidence is vendor-reported (Z.ai's GLM-5.3 ExploitBench 54.4 vs Kimi K3 32.2, no independent row) and no pool model's safeguards are verified. No OpenCode models on the line |
| **Biology-adjacent R&D** | Deciding | **"unverified — use Claude"**, no model |
| **Computer-use (GUI driving)** | Deciding | **"unverified — use Claude"** — no independent OSWorld row exists for any pool model (Haiku 5.5's 72.4 is Anthropic's own, on Claude's harness) |
| Context > 500k tokens | Eliminating | **Grok 4.7 removed** |
| Context > 256k tokens | Eliminating | **Qwen3.8 Flash removed** |
| Task needs **image input** | Eliminating | **GLM-5.3 removed** (text-only; only reachable through A1-OC) |
| Task is **factual recall / research-synthesis** | Eliminating | **DeepSeek V4.1 Flash removed** (AA-Omniscience hallucination rate 96.5%, index −5.3; MiniMax M3.1 Flash, 92.8%, is unrouted anyway) |
| Work is **confidential** — the default for this user (company code, data, plans) | Eliminating | **Muse Spark 1.3 Contributor removed** (trains on prompts); **Grok 4.7 and GPT 6 Luna removed** (30-day retention, as is Claude Haiku 5.5's; every other Go model is 0-day); **Gemini 4 Argon removed** (the cap and data policy of its Go route are unread; the deprecated Contributor route trained on prompts). Lifted only by Rule NC1 (Grok 4.7 stays premium — BUD1) |
| Sub-second latency / high-volume bulk (one labelling or parsing job applied to hundreds of items — redoing such a batch included) | Deciding | **DeepSeek V4.1 Flash #1 · MiMo-V2.6-Flash #2** (NC1: **GPT 6 Luna** #2), effort `low` |

<!-- rule:NC1 -->
**NC1 · non-confidential unlock.** Only when the user says the work is non-confidential or personal: GPT 6 Luna stays in the pool (30-day retention is accepted; Grok 4.7 stays premium under BUD1 and does not return), and Muse Spark 1.3 Contributor takes `#2` on `research-synthesis` rows only (AA-Omniscience 25 vs MiMo-V2.6-Pro 8, USD 60 cap against USD 15; `deep-reasoning` and `science` already carry the free model, or Argon, so it adds nothing there), and Gemini 4 Argon becomes available (Rule GM1). Never infer non-confidentiality from the prompt's tone.
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
| **agentic-code** | multi-file implementation, refactor, migration, feature build, debug-and-fix across files | AA Terminal-Bench 4.0 · DeepSWE v1.1 · FrontierSWE v2 · Agent Arena |
| **terminal-tool** | terminal/CLI work, build & test loops, tool orchestration, long-horizon execution | AA Terminal-Bench 4.0 |
| **deep-reasoning** | **architecture from scratch**, algorithm design, mathematics/formal proof, tool-less analysis, adversarial correctness hunting | AA HLE · CritPt · ARC-AGI-2 |
| **knowledge-work** | produce a finished document / spreadsheet / deck / memo / filing | GDPval-AA v2.1 · AA-Briefcase · AA-AnalystAgent · Harvey LAB |
| **research-synthesis** | multi-source research, web search, reconciling conflicting sources | AA-Omniscience index |
| **long-context** | read a large corpus, map/summarise across hundreds of pages or a whole repo | AA-LCR v1.1 · MLCR-AA + the context-window spec |
| **computer-use** | drive a browser or desktop GUI, click through an app, screenshots | OSWorld (⚠️ version + scoring mode) — gated on the OpenCode arm |
| **science** | genomics, chemistry, physics, research engineering, lab pipelines | SciCode · Terminal-Bench-Science |
| **workflow-automation** | wire up business workflows, integrations, multi-tool orchestration | AutomationBench-AA · ITBench · EnterpriseOps-Gym |
| **doc-data-understanding** | scanned documents, PDFs, charts, tables, multimodal extraction | AA GDP.pdf (one independent row) |
| **parallel-independent** | 3+ targets or strands that proceed unaware of each other and merge at the end | *no product mechanism on either arm now* |
| **orchestration** | three or more distinct phases in one session (Rule O1) | *product mechanism:* `ultracode` (Claude) |
| **latency-volume** | an explicit **first-token requirement**: sub-second, real-time, autocomplete, voice, "while the user waits". Bulk labelling or parsing that nobody waits on is **not** this tag — it has no dominant tag and falls to the `D ≤ 1` price tie-break | first-token time (DeepSeek V4.1 Flash 1.1 s measured; none for Haiku 5.5) |
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

<!-- rule:H1 -->
**H1 · Haiku 5.5.** Haiku 5.5 is the Claude pick when `R ≤ 1` and `C ≤ 1` and the dominant capability is not `research-synthesis` and one of these holds: `D = 0` and `W = 0`; or `D = 1` and `W ≤ 1` and the dominant capability is `instruction-following`, `latency-volume`, or none of the tags fits (a summary, a reformat, a translation, a label, a rewrite or an answer from text the user provides). Effort is `low` at `D = 0` and `medium` at `D = 1`, never higher.
<!-- /rule:H1 -->

> The exclusions are where Haiku 5.5 trails Sonnet 5.5 (High) widely — Terminal-Bench 22 vs 44, AutomationBench 34 vs 59, GDPval-AA 1420 vs 1551, AA-Omniscience 6 vs 21. Reading comprehension is a tie (AA-LCR 77 vs 78), so summaries, labels and rewrites stay on Haiku.

| Condition | Model |
|---|---|
| Rule H1 holds | **Haiku 5.5** |
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

**Escalation — a model change, never an effort change.** The user says the work
is critical, must not be under-resourced, or that an earlier run fell short →
**Sonnet 5.5 → Opus 5.5**, same rung. Do *not* crank the mid tier instead: Rule E1
shows its top rung is dominated by the next tier's ordinary rung on quality *and*
quota.

<!-- rule:H2 -->
**H2 · Haiku escalation.** When the user says an earlier Haiku 5.5 run fell short, or asks for more care on work H1 would give Haiku, the Claude line becomes Sonnet 5.5 at its own `D` rung. Haiku's effort is never raised instead.
<!-- /rule:H2 -->
<!-- rule:A1 -->
**A1 · frontier rung.** Opus 5.5 becomes Fable 5.1 only when the dominant capability is on the flagship list and `A = high`, where `A = high` means the user states that an earlier flagship-tier run at `xhigh` or `max` already fell short. A long or unattended session is not that statement.
<!-- /rule:A1 -->

> Difficulty and duration never reach the frontier rung: Anthropic's same-harness table has Opus 5.5 at or above Fable 5.1 on all eight benchmarks it lists (Terminal-Bench 4.0 66.4 vs 55.8) at under half the price. Only a stated `xhigh`/`max` shortfall does. *(The 1000+-file gate is unchanged — `reference.md` §17.)*

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
**UC1 · `ultracode`.** Emit `ultracode` when the estimated duration is over 30 minutes and either `O = high` or (`W = 3` and `D >= 2`) and the difficulty is not one indivisible chain. Write `ultracode` in the effort field. Never on Haiku 5.5.
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
`R = 3` (Rule PO1). **4.** Rules CAP1, FR1, GM1. **5.** Effort for each (below). Every pair comes
from the **budget tier** (Rule BUD1) — the free lane of FR1 is empty; under NC1 Rule GM1 puts Gemini 4 Argon
on top of the right-hand column — the premium four are not in this table.

Each row is the **consensus of the independent anchors in `opencode-evidence.json`
among the budget tier** (mean rank across ≥ 2 evaluators;
`scripts/derive_opencode_rows.py` reproduces it) — not one benchmark.

| Dominant capability | `R ≤ 2` → `#1` · `#2` | `D = 3` or `R = 3` → `#1` · `#2` | Evidence (independent anchors, budget tier) |
|---|---|---|---|
| **any tag, `D ≤ 1`** | DeepSeek V4.1 Flash · GLM-5.3-Flash | same | DeepSeek is the all-rounder of the USD 60–80 tier (Agent Arena 4.02 at USD 0.13 vs 0.44 / 0.57); research-synthesis drops DeepSeek (gate) → GLM-5.3-Flash · MiMo-V2.6-Flash |
| `agentic-code`, `terminal-tool` | DeepSeek V4.1 Flash · MiMo-V2.6-Pro | **MiMo-V2.6-Pro · DeepSeek V4.1 Flash** | DeepSeek leads DeepSWE (71.7 ±6.3, tied with Claude), Agent Arena and Vals TB 2.1; MiMo-V2.6-Pro leads AA TB 4.0 in the budget tier (35), so it goes first at depth. Under NC1 Argon is `#1` at `D = 3` / `R = 3` (GM1): AA TB 4.0 57, Vals 58, FrontierSWE v2 55 (vs 35 / 18), still behind Claude (60–64). GLM-5.3 is premium — A1-OC |
| `deep-reasoning` | MiMo-V2.6-Pro · GLM-5.3-Flash | same | HLE 49 vs 40, CritPt 27 vs 15 (FR1: the free model that was `#2` is gone). Under NC1 at `D = 3` / `R = 3` Argon is `#1` (GM1): HLE 57, ARC-AGI-2 91.3 (vs 49 / 61); Opus 5.5 still leads HLE and CritPt |
| `knowledge-work` | MiMo-V2.6-Pro · Qwen3.8 Flash | same | GDPval 1686 vs 1648, Briefcase 1516 vs 1583 — the rows split, so the two lead together |
| `workflow-automation` | DeepSeek V4.1 Flash · GLM-5.3-Flash | same | AutomationBench-AA 69 vs 60; ITBench 47 vs 51. Under NC1 at `D = 3` / `R = 3` Argon is `#1` — 77.5 (Sonnet 5.5 72) |
| `long-context` | DeepSeek V4.1 Flash · GLM-5.3-Flash | same | AA-LCR 84 vs 80; MLCR-AA 23 vs 51 — each leads one row, both 1M. Kimi K3.1 Pro is premium |
| `research-synthesis` | MiMo-V2.6-Pro · GLM-5.3-Flash | same | Omniscience 8.4 vs 7.5, hallucination 41% (MiMo-V2.6-Pro); **DeepSeek is gated out**. Under NC1 at `D = 3` / `R = 3` Argon is `#1`: index 42, hallucination 15% (Sonnet 5.5 32 / 47%) |
| `science` | MiMo-V2.6-Pro · GLM-5.3-Flash | same | SciCode 61 vs 52, CritPt 27 vs 15 (DeepSeek ties GLM-5.3-Flash and has peak pricing); Argon only ties MiMo-V2.6-Pro (62 / 27), so GM1 skips the row |
| `doc-data-understanding` | Qwen3.8 Flash · MiMo-V2.6-Pro | same | MMMU-Pro 80 (Qwen3.8 Flash) and GDP.pdf 19 (MiMo-V2.6-Pro) are one row each, so the two lead together; both take images. Kimi K3.1 Pro is premium |
| `latency-volume` | DeepSeek V4.1 Flash · MiMo-V2.6-Flash | same | 222 / 62 tok/s; NC1: GPT 6 Luna as #2 (147 tok/s) |
| `orchestration`, `parallel-independent` | by the *underlying* tag | | `ultracode` lives on the Claude line |
| anything else | MiMo-V2.6-Pro · GLM-5.3-Flash | same | no row → best index per dollar |

**Two dominant tags:** `#1` from the row whose tag decided the badge (else the first
named); `#2` = the other row's `#1`, or its `#2` if that is the same model.

<!-- rule:PO1 -->
**PO1 · pair order.** At `D ≤ 2` and `R ≤ 2` the most cap-efficient model inside the leading consensus band goes first; at `D = 3` or `R = 3` the leader on the hardest anchors goes first (the right-hand column). This orders the pair only — the badge still follows SM1.
<!-- /rule:PO1 -->

<!-- rule:CAP1 -->
**CAP1 · cap rule.** The USD 15-cap budget models (MiMo-V2.6-Pro, GPT 6 Luna) are reserved for `D ≥ 2`; `D ≤ 1` goes to the USD 60–80-cap Flash tier (the `latency-volume` row is exempt). Caps are per model: when the user says a model's window is exhausted, name the next model of its chain in `Evidence:` only — Pro **MiMo-V2.6-Pro → DeepSeek V4.1 Flash → GLM-5.3-Flash → Qwen3.8 Flash**; Flash **DeepSeek V4.1 Flash → GLM-5.3-Flash → MiMo-V2.6-Flash → Qwen3.8 Flash**.
<!-- /rule:CAP1 -->

<!-- rule:A1-OC -->
**A1-OC · escalation rung.** When the user states that an earlier OpenCode run fell short, `#2` becomes the premium model with the best consensus for the dominant capability — **GLM-5.3** for `agentic-code`, `terminal-tool`, `workflow-automation` and `research-synthesis`; **Kimi K3.1 Pro** for `deep-reasoning`, `science`, `long-context` and `doc-data-understanding`; **Qwen3.8 Max** for `knowledge-work` — or, when the work is non-confidential (NC1), **Gemini 4 Argon** on the GM1 rows at `D ≥ 2` and **Grok 4.7** elsewhere, and `Evidence:` names its cost (about 3–5% of its monthly cap per real agent task, Grok 10%, Kimi K3.1 Pro about 14% per AA index task, Argon's cap unread). After a shortfall at `D ≥ 2` the badge goes to Claude whenever the dominant capability has a Claude cell anywhere in the badge table — `agentic-code`, `terminal-tool`, `deep-reasoning`, `knowledge-work`, whatever the task's own depth — because the earlier run already showed the task is harder than the OpenCode pair handles; at `D = 3` also say the Claude line is stronger.
<!-- /rule:A1-OC -->

> A shortfall escalates only the arm it happened on.

#### OpenCode Go — effort for each model

Use the variants table under *Effort levels*. On the three `low`/`high`/`max`
models and Kimi K3.1 Pro: `D ≤ 1` `low` · `D ≥ 2` `max`. Every
other model has one rung to write (Gemini 4 Argon: `high`).

> **E7.** `D ≥ 2 → max` on the Flash tier. AA measured DeepSeek V4.1 Flash only at `max` (non-reasoning 25 → 39 at
> `max`), GLM-5.3 `low` 34 → `max` 45 and Kimi K3 30 → 44 (E5; Kimi K3.1 Pro's own curve is unpublished): the independent evidence sits at `max`, `high` has no
> independent figure. `max` costs USD 0.25–0.27 per AA task on this tier — about 0.3% of a USD 80 cap — so there is no
> quota reason to hold back. (DeepSeek's V4.1-Flash paper has effort 60–80 recovering most of `max` at under half the
> tokens, and Z.ai's Code Bench has GLM-5.3 `high` 31.4% vs `max` 34.5% — vendor, own-model curves that pick a rung, never a direction.) `GLM-5.3 · low` is dominated (E6);
> `low` on a Flash model has no number and is used only at `D ≤ 1`. Kimi K3.1 Pro has no
> published rung curve and borrows the same convention (A1-OC only, so `D ≥ 2`).

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
variance or an owner-published threshold. AA publishes none, so its cells are
`UNRESOLVED` however large the gap looks** — only BD1, or at `R=3` a single
measurement, sets a direction. **DeepSWE v1.1 (Mercor/Datacurve) does publish ±6–9 per
row**, so it certifies a tie: DeepSeek V4.1 Flash 71.7, GLM-5.3 70.5, Opus 5.5 72.3
and Sonnet 5.5 70.5 are one band. Score spread is not uncertainty. At `R=3` widen the
bar; if unsure take the stronger candidate.

**Dominance** — A dominates B if A is not meaningfully worse on the task capability
and clearly better on one axis, in order; a dominated candidate is never emitted.
Claude arm and badge: reasoning tokens → output tokens → total tokens → tokens per
successful task → quota pressure → cost → latency. OpenCode (open vs open): **Go cap
pressure** (cost/task ÷ cap, then the 5-hour output-token budget) → reasoning tokens
→ output tokens → latency.

- **E1** `Sonnet 5.5 · max` (56 @ USD 5.46, ~197k tokens) is dominated by `Opus 5.5 · xhigh` (56 @ USD 3.46); Anthropic's footnote: Sonnet scores *lower* at `max` on FrontierCode. Never emit it; escalate to `Opus 5.5 · xhigh`.
- **E3** `max` over `xhigh` buys little on Claude (Fable 5.1 53 = 53; Opus 5.5 58 vs 56, +73% cost) → `max` needs M1.
- **E5** open models are the exception: `max` buys +11 (GLM-5.3 34 → 45) and +14 (Kimi K3 30 → 44) — the premium pair, reached only through A1-OC — and DeepSeek V4.1 Flash non-reasoning 25 → 39 at `max`, so `D ≥ 2 → max` on the Flash tier (E7).
- **E6** dominated, never emitted: `GLM-5.3 · low` (→ GLM-5.3-Flash 42 @ 0.25), Kimi K3 (→ Kimi K3.1 Pro through A1-OC: same cap and price, index 44 → 55), DeepSeek V4 Pro (→ V4.1 Flash), MiniMax M3 / Kimi K2.7 Code / Qwen3.7 Plus (TB 2/1/1), Qwen3.8 Max (→ MiMo-V2.6-Pro) except via A1-OC. Grok 4.7 and GPT 6 Luna are not dominated — retention *eliminates* them; Grok 4.7 is premium (BUD1).
- **E8** `Haiku 5.5 · xhigh` / `max` is never emitted: AA Max is 43 @ USD 0.21 but 162k output tokens per task against Sonnet 5.5 High 47 @ USD 0.88 and 37k. Haiku stops at `medium` (H1); needing more makes it a Sonnet 5.5 task.
- **E9** Claude Haiku 5.5 is rated on Go but never emitted there: High 38 @ USD 0.08 on a USD 15 cap with 30-day retention is dominated by MiMo-V2.6-Flash (38 @ 0.06, USD 60 cap, 0-day), Max 43 @ 0.21 by GLM-5.3-Flash (42 @ 0.25, USD 60 cap). Use it on the Claude line, where no dollar cap applies.
- **E10** Gemini 3.8 Flash is never emitted: 41 @ USD 1.24 per AA task against MiMo-V2.6-Pro 46 @ USD 0.13; its one edge (AA-Omniscience 30) is covered by Argon. It is not offered on Go (Google API / Zen only).
- **E11** Gemini 4 Argon is written at `high` only: AA measured `high`, `medium` (Google's default) has no independent figure, `max` is rejected (HTTP 400). Its Go cap is a promo (USD 60, 30 after; about 3% per heavy AA task), so a GM1 row is a deliberate spend.

**Effort rung:** the lowest rung that reaches the capability the task needs; round
down when the next rung is inside the band, never when the low→high gap is real.

---

## Step 6 — `✅ RECOMMENDED AI`

Compare the **Claude line** with **OpenCode `#1`**; mark exactly one ecosystem. **OpenCode
is the default** — the budget tier clears the bar for errand work and for everything up to
mid-depth, and Claude's quota is the scarcer one. Claude is recommended only where it makes
a serious difference (Rule SM1).

<!-- rule:B1 -->
**B1 · evidence applicability.** A benchmark row takes part in the badge decision only if the capability it measures is one of the dominant tags named for this prompt in Step 2. Applicability is checked before evidence quality and before any tie-break, and a row that is not applicable does not enter the comparison at all, however strong its number.
<!-- /rule:B1 -->

<!-- rule:BD1 -->
**BD1 · direction without an interval.** A badge direction needs at least two independent measurements that agree — an independent evaluator's run, or a vendor's table that favours its rival — at least one of them tier A or B, and none that disagree. The same benchmark re-published on a second page is one measurement, a tie is not opposition, and an aggregate never counts. Otherwise the cell is decided by efficiency, except at R = 3, where a single admissible measurement still decides it: a lean is not parity.
<!-- /rule:BD1 -->

<!-- rule:MECH1 -->
**MECH1 · mechanism rows.** `ultracode` driven by `O = high`, or a task routed to `opusplan`, names something OpenCode does not have, so it decides the badge for Claude unless the other capability row carries a benchmark direction under BD1, which wins.
<!-- /rule:MECH1 -->

<!-- rule:SM1 -->
**SM1 · OpenCode by default.** The badge goes to OpenCode unless Claude clears a serious margin. Claude takes it only when a hard gate or the context window puts OpenCode out, or MECH1 applies, or `D = 3` and the dominant capability is `agentic-code`, `terminal-tool` or `deep-reasoning` and BD1 gives Claude a direction, or the dominant capability is `knowledge-work` at `D ≥ 2` with a BD1 direction, or `R = 3` and `D ≥ 2` and the dominant row leans to Claude. Every `D ≤ 1` task and every other `D = 2` task is OpenCode: the budget pair clears the bar there, and a Claude direction that only shows on harder tasks is not a reason to spend Claude's quota.
<!-- /rule:SM1 -->

**Order:** (1) hard gate — if one arm declines or lacks the context window, the other
gets the badge, stop; (2) MECH1; (3) applicable capability (B1) and its evidence
(independent evaluator > vendor table; a vendor result favouring its *rival* is the most
credible vendor evidence) read through BD1 and SM1; (4) everything SM1 leaves over is
OpenCode, and the Evidence line says what Claude would add and why it is below the bar.

The depth split is the evidence's own: Claude's lead lives on the `D = 3` anchors (TB 4.0, FrontierSWE v2, HLE) while DeepSWE v1.1 (±7) ties at mid-difficulty; finished deliverables are the other wide gap, so `knowledge-work` stays Claude from `D = 2`.

### Badge table

| Dominant capability | `D = 2`, `R ≤ 2` | `D = 3`, `R ≤ 2` | `D ≥ 2`, `R = 3` | Evidence to name |
|---|---|---|---|---|
| `agentic-code`, `terminal-tool` | **OpenCode** | **Claude** | **Claude** | `D = 2`: DeepSWE ±7 ties (DeepSeek 71.7 vs Opus 72.3 / Sonnet 70.5) at USD 0.13 vs 1.67 per agent task. `D = 3` / `R = 3`: three independent rows agree — AA TB 4.0 64 / 60 vs 35, FrontierSWE v2 62 vs 18, Agent Arena 13.8 / 12.5 vs 4.0; against Argon (NC1 only) Claude still leads: TB 64 / 60 vs 57, FrontierSWE 62 vs 55, Google's own table 66 vs 57 |
| `deep-reasoning` | **OpenCode** | **Claude** | **Claude** | HLE 61 / 55 vs MiMo-V2.6-Pro 49; CritPt 32 / 31 vs 27; ARC-AGI-2 92 vs 61 — three rows agree, and they bite at `D = 3`; against Argon (NC1 only) Claude still leads HLE and CritPt (61 / 32 vs 57 / 27) |
| `knowledge-work` | **Claude** | **Claude** | **Claude** | GDPval-AA 1866 / 1839 vs MiMo-V2.6-Pro 1686; Briefcase 1807 / 1823 vs 1583; AnalystAgent 56 / 58 vs 39 — three AA rows agree (Harvey LAB is a tie) |
| `workflow-automation` | **OpenCode** † | **OpenCode** † | **OpenCode** † | AutomationBench-AA Sonnet 72 / Opus 70 vs DeepSeek 69 is a tie and ITBench has the open models ahead — no Claude direction; Argon (NC1 only) is 77.5 |
| `science` | **OpenCode** † | **OpenCode** † | **Claude** † | SciCode Opus 67 / Sonnet 61 vs MiMo-V2.6-Pro 61 — one row, a tie with Sonnet |
| `long-context` (shallow) | **OpenCode** † | **OpenCode** † | **OpenCode** † | The rows disagree: AA-LCR DeepSeek 84 vs Opus 85 / Sonnet 83 is a tie, but MLCR-AA Claude 67 / 75 vs best budget 51 — contested, so efficiency |
| `research-synthesis` | **OpenCode** † | **OpenCode** † | **Claude** † | AA-Omniscience Sonnet 32 / Opus 46 vs MiMo-V2.6-Pro 8 — one row. Under NC1 Argon is `#1` at `R = 3` (GM1) and beats the Claude pick on both measures — index 42 vs 32, hallucination 15% vs 47% — so the `R = 3` cell reads **OpenCode** † |
| `doc-data-understanding` | **OpenCode** † | **OpenCode** † | **Claude** † | GDP.pdf Opus / Sonnet 26 vs MiMo-V2.6-Pro 19 — one row |
| `latency-volume` (first-token bound) | **OpenCode** | **OpenCode** | **OpenCode** | DeepSeek V4.1 Flash 222 tok/s, TTFT 1.1 s; Haiku 5.5 has no measured first-token figure at `low` — facts, not a score |
| `orchestration`, or a task routed to `opusplan` | **Claude** | **Claude** | **Claude** | `ultracode` sequences phases, `opusplan` spends the flagship on the plan; OpenCode has neither |
| anything else | **OpenCode** † | **OpenCode** † | **OpenCode** † | no row → the cheaper arm; say `low-confidence` |

**† → Evidence must say `low-confidence`** (binds that row; so does "anything else").
Mechanism, `latency-volume` and the `D ≤ 1` rule carry none. A `D = 2` coding or reasoning
row that SM1 sends to OpenCode is **not** †: its evidence is strong, the Claude lead just
sits at a depth the task does not reach — name the tie and the price instead. At `R = 3` a
row that fell to efficiency follows its single measurement's lean and keeps its †.

**`D ≤ 1` → OpenCode, whatever the Claude pick** (Haiku 5.5 included): skip the capability
rows (except `latency-volume`, which keeps its own); price, cap and the Claude quota
decide, no †, and `R` doesn't change it. The Claude line still names what to run if the
user goes there. Two dominant rows conflict → a benchmark **direction** beats a mechanism
or an efficiency fall-through. Both arms gated alike or Step 0 blocked → no badge. Genuinely
thin evidence → the sensible default + `low-confidence`.

---

## Step 7 — Quota-protection and accuracy rules

Rationale in `reference.md` §10.5. **Auto-added lines:** Rules 1, 9, 10 and 11.

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
8. **Alias safety:** `/model opus` → Opus 5.5 on Claude Code v2.1.280+; `/model sonnet` → Sonnet 5.5 on v2.1.284+; `/model haiku` → Haiku 5.5 on v2.1.293+ (older builds: use `/model claude-haiku-5-5`).
9. **Data-policy line (auto).** If **Grok 4.7** (A1-OC only) or **GPT 6 Luna** is on the OpenCode
   line: `Data: <model> keeps prompts for 30 days.` If **Muse Spark 1.3 Contributor**
   is on it (NC1 only): `Data: Muse Spark 1.3 Contributor trains on your prompts.`
   Never name Muse Spark when the work is confidential.
10. **DeepSeek line (auto).** If **DeepSeek V4.1 Flash** is on the OpenCode line:
    `DeepSeek V4.1 Flash: peak hours cost 2× (04–07 and 09–13 TR time, Mon–Fri); zero-retention agreement is renewed monthly (valid through 31 Oct 2026).`
11. **Gemini line (auto).** If **Gemini 4 Argon** is on the OpenCode line:
    `Gemini 4 Argon: opencode-go/gemini-4-argon — the Go cap and data policy of this route are unread (promo USD 2/10 per MTok to 30 Nov, then 4/20). If it errors or is overloaded, run the row's other model.`

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
- Write `default` where OpenCode offers no variant (MiMo-V2.6).
  OpenCode gated: `OpenCode: use Claude — <reason>` (no `#`).
- Extras, own line each, in order: `opusplan` ⚠️ (directly under the Claude line) ·
  data / DeepSeek / Gemini lines (Step 7) · speed line · `R=3` → `Do not apply without human
  review.` last.
- "Why?" → expand from `reference.md` / `opencode-benchmarks.md`; never unprompted.

### Examples

*"Label these 200 customer reviews as positive/negative"*
```
Claude: Haiku 5.5 · effort: low
OpenCode: ✅ RECOMMENDED AI · #1 DeepSeek V4.1 Flash · effort: low · #2 MiMo-V2.6-Flash · effort: default
Evidence: Labelling is D=0 bulk work, so OpenCode runs it: the Flash tier buys hundreds of such batches a month on USD 60–80 caps (USD 0.13–0.27 per task) and keeps Claude's quota for harder work.
DeepSeek V4.1 Flash: peak hours cost 2× (04–07 and 09–13 TR time, Mon–Fri); zero-retention agreement is renewed monthly (valid through 31 Oct 2026).
```
> Errand work goes to OpenCode even when Haiku 5.5 would do it. A finished memo or deck at `D ≥ 2` is `knowledge-work` and stays on Claude.

*"Fix this code"*
```
Clarify: which file or function is broken, what does it do now, and what should it do instead?
```

*"Refactor the payment module across these 40 files to use the new idempotency-key API, update every caller, and make the test suite pass."*
```
Claude: Sonnet 5.5 · effort: high
OpenCode: ✅ RECOMMENDED AI · #1 DeepSeek V4.1 Flash · effort: max · #2 MiMo-V2.6-Pro · effort: default
Evidence: Mid-difficulty feature work is a tie on the independent DeepSWE (DeepSeek 71.7 vs Sonnet 5.5 70.5, ±7) at USD 0.13 against Opus 5.5's 1.67 per agent task; Claude's lead starts at D=3.
DeepSeek V4.1 Flash: peak hours cost 2× (04–07 and 09–13 TR time, Mon–Fri); zero-retention agreement is renewed monthly (valid through 31 Oct 2026).
```
> One implementation phase → no `ultracode`. The same task at `D=3` (or after an OpenCode shortfall) flips the badge to Claude.

*"Find the race condition that flakes in prod sometimes"*
```
Claude: ✅ RECOMMENDED AI · Opus 5.5 · effort: xhigh
OpenCode: #1 MiMo-V2.6-Pro · effort: default · #2 DeepSeek V4.1 Flash · effort: max
Evidence: D=3 reasoning half has two agreeing AA rows (HLE 61 vs 49, CritPt 32 vs 27); the terminal half sets no direction, so the direction decides.
DeepSeek V4.1 Flash: peak hours cost 2× (04–07 and 09–13 TR time, Mon–Fri); zero-retention agreement is renewed monthly (valid through 31 Oct 2026).
⚡ Claude /fast available (2.5x faster, 2× price).
```
> `D=3` (D3DIAG) but one phase → `xhigh`, not `ultracode`/`max`. `#1` from the badge-deciding tag (deep-reasoning); the terminal row's `#1` is the same model, so `#2` is its `#2`. Gemini 4 Argon is absent: the work is confidential by default (GM1).

*"Read these three public EU regulator pages and tell me what each one says about home-compostable claims on packaging labels — we send the labels to print tonight and cannot reprint them"*
```
Claude: ✅ RECOMMENDED AI · Sonnet 5.5 · effort: high
OpenCode: #1 MiMo-V2.6-Pro · effort: default · #2 GLM-5.3-Flash · effort: max
Evidence: Printing cannot be undone (R=3), and the one Omniscience row has Sonnet 5.5 at 32 against MiMo-V2.6-Pro's 8, so the single lean decides; low-confidence.
Do not apply without human review.
```
> Said non-confidential, the same prompt gets Gemini 4 Argon `#1` and the badge moves to OpenCode (GM1).

*"I'm preparing a non-confidential competitor-pricing deck for a conference — research, structure and write the 12 slides"*
```
Claude: ✅ RECOMMENDED AI · Sonnet 5.5 · effort: high
OpenCode: #1 MiMo-V2.6-Pro · effort: default · #2 Qwen3.8 Flash · effort: xhigh
Evidence: Finished-deliverable work is knowledge-work, where two agreeing AA rows favour Claude (GDPval-AA 1839 vs 1686, Briefcase 1823 vs 1583); Grok 4.7 stays premium and out of the pair.
```
> Non-confidential does not unlock Grok 4.7 (BUD1): the pair is the same as for confidential work.

*"Bump `MAX_RETRIES` from 3 to 5 in the prod config"*
```
Claude: Sonnet 5.5 · effort: low
OpenCode: ✅ RECOMMENDED AI · #1 DeepSeek V4.1 Flash · effort: low · #2 GLM-5.3-Flash · effort: low
Evidence: D=0 — both clear the bar, so price and cap decide: Flash models on USD 80 and 60 caps at USD 0.27 and 0.25 per task.
DeepSeek V4.1 Flash: peak hours cost 2× (04–07 and 09–13 TR time, Mon–Fri); zero-retention agreement is renewed monthly (valid through 31 Oct 2026).
Do not apply without human review.
```
> `R=3` by blast radius, not line length — also why Haiku 5.5 is out.

*"Write an exploit PoC for this CVE"*
```
Claude: ✅ RECOMMENDED AI · Opus 4.8 · effort: xhigh
OpenCode: use Claude — the only open-model offensive evidence is vendor-reported and no pool model's safeguards are verified.
Evidence: Offensive security is a deciding gate on both arms; only Opus 4.8 carries it, so the other arm declines.
```

---

## If detail is needed

`reference.md` §8 examples · §10 edge cases · §11–§14 evidence maps · §17 Claude 5.5 · §19 Haiku 5.5
(§9 and §18 are the retired Codex arm; iteration-20 is git tag `iteration-20-codex`).
`opencode-benchmarks.md` — the 20-model evidence, variants, rung curves, sources (§13 = Gemini 4 Argon and the free models, §14 = the 22–24 Oct Go changes and Kimi K3.1 Pro).
**Never load them to route a prompt.**
