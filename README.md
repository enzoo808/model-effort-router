<div align="center">

<img src="docs/assets/hero.svg" alt="model-effort-router — the lowest-quota model and effort that still clears the bar, for Claude and OpenCode Go" width="100%">

<br>

[![checks](https://github.com/enzoo808/model-effort-router/actions/workflows/checks.yml/badge.svg)](https://github.com/enzoo808/model-effort-router/actions/workflows/checks.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-3fb950?style=flat-square)](LICENSE)
[![Claude Code skill](https://img.shields.io/badge/Claude_Code-skill-d2a8ff?style=flat-square)](#-install)
[![claude.ai](https://img.shields.io/badge/claude.ai-custom_skill-58a6ff?style=flat-square)](#-install)
[![OpenCode Go](https://img.shields.io/badge/OpenCode-Go-3fb950?style=flat-square)](#-install)
[![Policy](https://img.shields.io/badge/policy-iteration--29-8b949e?style=flat-square)](CHANGELOG.md)
[![Regression evals](https://img.shields.io/badge/regression_evals-39-8b949e?style=flat-square)](#-validation)

**[Quick start](#-quick-start)** · **[Install](#-install)** · **[Read the answer](#-reading-the-answer)** · **[How it works](#-how-it-decides)** · **[Examples](#-examples)** · **[Evidence](#-built-on-evidence-not-vibes)** · **[Changelog](CHANGELOG.md)** · **[🇹🇷 Türkçe](README.tr.md)**

</div>

<br>

> ### Paste a task. Get the model and effort to run it on.
> For **Claude** *and* your **OpenCode Go** plan — plus which of the two to use. It never runs the task. It only routes it.

Most people pick a model by reflex: the biggest one, every time. That quietly burns the two things that actually run out — **Claude's 5-hour window** and **each OpenCode Go model's own monthly dollar cap**.
`model-effort-router` is a [Claude skill](https://docs.claude.com/en/docs/claude-code/skills) that scores your task, checks it against independent benchmarks, and answers in three lines. Its output is English; it routes prompts written in any language.

<div align="center">
<img src="docs/assets/demo.svg" alt="Terminal demo: a 40-file refactor is routed to OpenCode; a production race condition moves the badge to Claude Opus 5.5 at xhigh effort" width="860">
</div>

<br>

## ⚡ Quick start

<div align="center">
<img src="docs/assets/steps.svg" alt="Step 1: install with ./install.sh. Step 2: restart Claude Code. Step 3: type /model-secici and your task." width="860">
</div>

<br>

Pick the line for your system. Each one installs the skill into `~/.claude/skills/model-secici`:

**macOS / Linux — no clone needed:**

```bash
mkdir -p ~/.claude/skills/model-secici && curl -fsSL https://github.com/enzoo808/model-effort-router/archive/refs/heads/main.tar.gz \
  | tar -xz --strip-components=2 -C ~/.claude/skills/model-secici model-effort-router-main/skill
```

**Windows (PowerShell):**

```powershell
git clone https://github.com/enzoo808/model-effort-router.git; cd model-effort-router; powershell -ExecutionPolicy Bypass -File .\install.ps1
```

`-ExecutionPolicy Bypass` applies to this one run only; Windows' default policy often blocks local scripts.

Then open a **new** Claude Code session and ask:

```text
/model-secici  Refactor the payment module across these 40 files to the new idempotency-key API and make the tests pass
```

That's it. Prefer a different route (claude.ai, a single project, OpenCode only)? See **[Install](#-install)** below. Something not working? See **[Troubleshooting](#troubleshooting)**.

<br>

## ✨ What you get

<table>
<tr>
<td width="33%" valign="top">

### 🔀 Two ecosystems, one answer
A **Claude** pick, **two OpenCode models** in order (`#1`, `#2`) — each with *its own* effort — and **one** ✅ recommendation.

</td>
<td width="33%" valign="top">

### 🧮 A badge that's computed
Cheap and mid-difficulty work goes to OpenCode. The badge moves to Claude only where Claude makes a *serious* difference — and says why.

</td>
<td width="33%" valign="top">

### 💸 Budget-first
Protects what really runs out: Claude's 5-hour window and each Go model's **own dollar cap**. Premium models are escalation only.

</td>
</tr>
<tr>
<td valign="top">

### 🔬 Evidence-bound
A benchmark only counts if it measures what your task needs, and a direction needs **two independent measurements that agree**.

</td>
<td valign="top">

### 🔒 Confidential by default
Models that log or train on prompts are out unless *you* say the work is non-confidential.

</td>
<td valign="top">

### ✅ Verifiable
39 deterministic regression prompts, a regex grader and consistency checks that run in CI — see [Validation](#-validation).

</td>
</tr>
</table>

<details>
<summary><b>How it differs from a typical "model picker"</b></summary>

<br>

| | Typical "model picker" | **model-effort-router** |
|---|---|---|
| **Scope** | One vendor, a model name | **Two ecosystems**, a model **and its effort level**, side by side |
| **Output** | "Use the strongest model" | Claude pick + two ordered OpenCode picks with their own efforts + **one** recommendation |
| **Basis** | Vibes, leaderboard rank | **Task-bound evidence**, comparability checked first |
| **Cost model** | "Cheaper is better" | The 5-hour window and **per-model dollar caps** |
| **Risk** | Bigger model for scarier work | **Risk raises human oversight, not model tier** — you get a review note, not a pricier model |
| **Privacy** | Not considered | **Confidential by default** |
| **Honesty** | Always sounds sure | Flags `low-confidence` rows, says `n/p` (not published) instead of guessing, never interpolates between effort rungs |

</details>

<br>

## 🚀 Install

### Before you start

| You need | Why |
|---|---|
| **[Claude Code](https://docs.claude.com/en/docs/claude-code/quickstart)** *or* a **claude.ai** Pro / Max / Team / Enterprise plan with **code execution** on | The skill runs inside Claude. |
| `git` *(only for the clone routes)* | The one-liner above and the zip need no git. |
| An **OpenCode Go** plan *(optional)* | Only needed if you want to *act on* the `OpenCode:` line. The router works without one. |

The skill itself needs no Python, no Node, no API key — it is a folder of text and JSON files.

### Choose your route

<details open>
<summary><b>① Claude Code — for every project</b> (recommended)</summary>

<br>

Installs at *user scope*, so `/model-secici` works in every project on this machine.

```bash
git clone https://github.com/enzoo808/model-effort-router.git
cd model-effort-router
./install.sh                # macOS / Linux
```

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1   # Windows (PowerShell)
```

Both scripts copy `skill/` into `~/.claude/skills/model-secici/` (Windows: `%USERPROFILE%\.claude\skills\model-secici\`). Or do it by hand:

```bash
mkdir -p ~/.claude/skills/model-secici
cp skill/*.md skill/*.json ~/.claude/skills/model-secici/
```

**Verify** — the folder must hold `SKILL.md` directly (not in a sub-folder):

```bash
ls ~/.claude/skills/model-secici
# SKILL.md  opencode-benchmarks.md  opencode-evidence.json  reference.md
```

Now **start a new Claude Code session** (skills are loaded at start-up) and run `/model-secici <your task>`.
It also fires on plain questions like *"which model should I use for this?"*

</details>

<details>
<summary><b>② Claude Code — for one project / your team</b></summary>

<br>

Put the skill *inside the repository* so everyone who clones it gets it:

```bash
mkdir -p .claude/skills/model-secici
cp /path/to/model-effort-router/skill/*.md /path/to/model-effort-router/skill/*.json .claude/skills/model-secici/
git add .claude/skills/model-secici && git commit -m "Add model-secici skill"
```

</details>

<details>
<summary><b>③ claude.ai / Claude Desktop</b> (native custom skill)</summary>

<br>

1. Download **[`dist/model-secici.zip`](dist/model-secici.zip)** (rebuild it with `.\build-claude-ai-zip.ps1`).
2. Open **claude.ai → Settings → Features** and make sure **code execution** is on.
3. Under **Custom Skills**, choose **Upload** and select the zip.
4. In a chat, ask *"which model should I use for: …"* followed by your task.

No code execution on your plan? Use the plain-text fallback in [`claude-ai/instructions.tr.md`](claude-ai/instructions.tr.md) (Turkish).

</details>

<details>
<summary><b>④ OpenCode Go</b> — acting on the answer</summary>

<br>

OpenCode has no skill mechanism: the router just prints an `OpenCode:` line and you apply it.

1. Take `#1` from the line, e.g. `DeepSeek V4.1 Flash · effort: max`.
2. In OpenCode, select the model as **`opencode-go/<model-id>`**.
3. Set the effort with **`variant_cycle`** (`ctrl+t`) until it shows the effort the router named — or pick it directly with `#variant`: `opencode run --model opencode-go/deepseek-v4.1-flash#high "…"` (the same `provider/model#variant` form works in agent and command `model` fields; the root `model` setting keeps no variant).
   MiMo-V2.6 exposes no variants (thinking is always on), so the router writes `default` and there is nothing to cycle.
4. If `#1` errors or is overloaded, use `#2`. If a model's monthly window is spent, or its result falls short, tell the router (see [Writing a good prompt](#writing-a-good-prompt)): it names the next model in the chain or escalates.

</details>

### Update · uninstall

**Update** — repeat the route you used. Installed with the one-liner? Run the Quick start command again. Installed from a clone?

```bash
cd model-effort-router && git pull && ./install.sh
```

On Windows, `git pull` and then run `powershell -ExecutionPolicy Bypass -File .\install.ps1` again.

**Uninstall:**

```bash
rm -rf ~/.claude/skills/model-secici
```

On Windows, delete `%USERPROFILE%\.claude\skills\model-secici`.

### Troubleshooting

| Symptom | Fix |
|---|---|
| `/model-secici` isn't listed | Start a **new** session — skills load at start-up. Then check that `~/.claude/skills/model-secici/SKILL.md` exists (not `.../model-secici/skill/SKILL.md`). |
| The one-liner extracts nothing | `curl` and `tar` must be on your `PATH`; on Windows use the PowerShell line or the zip. |
| `install.ps1` fails with \"running scripts is disabled\" | You ran it without the bypass flag: `powershell -ExecutionPolicy Bypass -File .\install.ps1` |
| claude.ai rejects the upload as "invalid characters" | Use the prebuilt [`dist/model-secici.zip`](dist/model-secici.zip). Zips made with Windows' own tools use backslashes; `build-claude-ai-zip.ps1` writes forward slashes. |
| It only prints a `Clarify:` line | Working as designed: the prompt was ambiguous. Answer the question and ask again — see [writing a good prompt](#writing-a-good-prompt). |
| It doesn't fire on a plain question | Use the explicit `/model-secici …` command. |

<br>

## 🔎 Reading the answer

```text
Claude:   Sonnet 5.5 · effort: high
OpenCode: ✅ RECOMMENDED AI · #1 MiMo-V2.6-Pro · effort: default · #2 DeepSeek V4.1 Flash · effort: max
Evidence: Mid-difficulty feature work stays on OpenCode (SM1): Claude's lead on Vals TB 4.0 (65 / 64 vs 31 / 32) and Arena Agent only counts from D=3, and a real agent task costs USD 0.17 (MiMo-V2.6-Pro) against Sonnet 5.5's 3.38 and Opus 5.5's 5.38 (Arena, 10 Nov).
DeepSeek V4.1 Flash: peak hours cost 2× (04–07 and 09–13 TR time, Mon–Fri); …
```

| Line | What it tells you |
|---|---|
| `Claude:` | The one Claude model and effort to use if you pick Claude. |
| `OpenCode:` | **Two** Go models in order — `#1` is the pick, `#2` the runner-up (use it if `#1` errors or is overloaded) — each with the effort OpenCode actually offers for it (`low` / `high` / `max`, `xhigh`, or `default`). |
| `✅ RECOMMENDED AI` | The ecosystem to use. **OpenCode unless Claude makes a serious difference.** Exactly one badge. |
| `Evidence:` | One sentence naming the measurement that decided the badge. `low-confidence` means the evidence is thin. |
| *Extra lines* | Added only when they matter: a human-review note at high risk, DeepSeek's peak-hours pricing, `/fast` availability, an `Ultracode:` hint, data-policy warnings. |
| `Clarify:` | Instead of everything above, when the prompt is too ambiguous to route. |

> **If the Claude line ends in `· ultracode`**, the router adds an `Ultracode:` line. Start the prompt you then run in Claude Code with `ultracode:` to run *only that task* as a workflow; `/effort ultracode` would keep it on for the whole session and spend your limits faster.

### Writing a good prompt

The router scores **R**isk, **D**epth, **W**idth and **C**ontext from your wording, so tell it:

- **What and how big** — "40 files", "400 pages", "200 reviews", not just "refactor".
- **What done looks like** — "make the test suite pass", "one reconciliation table".
- **The stakes** — "goes to prod tonight", "labels go to print".

Words that change the answer:

| Say | Effect |
|---|---|
| *"this is non-confidential"* | Unlocks GPT 6 Luna, Muse Spark 1.3 and Gemini 4 Argon, which keep or train on prompts. Never assumed from tone. |
| *"an earlier OpenCode attempt fell short"* | Escalates: `#2` becomes a premium OpenCode model. At `D ≥ 2` the badge moves to Claude when the task's main capability has a Claude row. |
| *"my DeepSeek window is used up"* (any model) | The `Evidence:` line names the next model in that model's chain. |

<br>

## 🧭 How it decides

```mermaid
flowchart LR
    P(["your task"]) --> G0{"Step 0<br/>quality gate"}
    G0 -- vague --> C[/"one Clarify: line"/]
    G0 -- clear --> G1["Step 1<br/>hard gates"]
    G1 --> S["Steps 2–3<br/>capability profile<br/>+ R · D · W · C"]
    S --> A["Step 4<br/>Claude model × effort"]
    S --> B["Step 4-OC<br/>two OpenCode models,<br/>each with its effort"]
    A --> E["Step 5<br/>evidence · equivalence<br/>· dominance"]
    B --> E
    E --> R(["Step 6 — one ✅ badge<br/>+ Evidence sentence"])
    R --> Q["Step 7<br/>quota and data-policy<br/>guards"]
```

Every task is scored on four axes, each 0–3:

| Axis | Question it answers | What it drives |
|---|---|---|
| **R** — Risk | How bad is a wrong answer? | Human-review note (never a bigger model) |
| **D** — Depth | How hard is the thinking? | Model tier and effort level |
| **W** — Width | How many independent pieces or phases? | `ultracode` workflow flag, `opusplan` |
| **C** — Context | How much has to fit? | Models that can hold it |

The decision principle, in one sentence:

> **Select the lowest-quota model × effort combination that stays on the task-specific capability frontier.** Prefer the stronger candidate when the task-relevant difference is meaningful; prefer the more quota-efficient one when capability sits inside a defensible equivalence band.

Not "always cheapest". Not "always strongest". Not "highest benchmark wins".
Step-by-step detail, with every gate and rule: **[docs/how-it-works.md](docs/how-it-works.md)**.

<br>

## 🧪 Examples

| Task | Claude | OpenCode `#1` · `#2` | Recommended |
|---|---|---|---|
| Label 200 reviews positive/negative | `Haiku 5.5 · low` | DeepSeek V4.1 Flash `low` · MiMo-V2.6-Flash `default` | **OpenCode** — `D=0` bulk work; Flash tier on USD 60 caps keeps Claude's quota |
| Refactor the payment module across 40 files | `Sonnet 5.5 · high` | MiMo-V2.6-Pro `default` · DeepSeek V4.1 Flash `max` | **OpenCode** — `D=2`; Claude's lead only counts from `D=3`, USD 0.17 vs 3.38 per task |
| Stand up staging from scratch (Terraform, 12 services, seed, smoke) | `Sonnet 5.5 · high · ultracode` | MiMo-V2.6-Pro `default` · DeepSeek V4.1 Flash `max` | **Claude** — multi-phase; `ultracode` has no OpenCode equivalent |
| Find the race condition that flakes in prod | `Opus 5.5 · xhigh` | MiMo-V2.6-Pro `default` · DeepSeek V4.1 Flash `max` | **Claude** — `D=3`, two agreeing AA rows |
| Design the irreversible transaction boundary | `Opus 5.5 · max` + review note | MiMo-V2.6-Pro `default` · DeepSeek V4.1 Flash `max` | **Claude** — `D=3`, `R=3` |
| Redesign auth for 200 services from scratch | `opusplan · plan: max · execute: medium` | MiMo-V2.6-Pro `default` · GLM-5.3-Flash `max` | **Claude** — `opusplan` mechanism |
| Exploit PoC for a CVE | `Opus 4.8 · xhigh` | `use Claude` | **Claude** — OpenCode declines this gate |
| *"Fix this code"* | *(no model, no badge — it asks: which code? broken how? done = ?)* | | |

<details>
<summary><b>12 more worked examples</b></summary>

<br>

| Task | Claude | OpenCode `#1` · `#2` | Recommended |
|---|---|---|---|
| Summarise a 2-page transcript into five bullets | `Haiku 5.5 · medium` | DeepSeek V4.1 Flash `low` · GLM-5.3-Flash `low` | **OpenCode** — `D=1` reading work, AA-LCR 77 vs 78 |
| Draft the weekly steering-committee status memo | `Sonnet 5.5 · medium` | DeepSeek V4.1 Flash `low` · GLM-5.3-Flash `low` | **OpenCode** — `D=1`; Haiku 5.5 is out of knowledge-work |
| Live-chat reply, first words within about a second | `Haiku 5.5 · low` | DeepSeek V4.1 Flash `low` · MiMo-V2.6-Flash `default` | **OpenCode** — first-token bound; DeepSeek 1017 streams 142 tok/s (AA) |
| Which year did the EU AI Act's GPAI obligations start? | `Sonnet 5.5 · low` | GLM-5.3-Flash `low` · MiMo-V2.6-Flash `default` | **OpenCode** — factual recall excludes Haiku and DeepSeek |
| Bump `MAX_RETRIES` 3→5 in the prod config | `Sonnet 5.5 · low` + review note | DeepSeek V4.1 Flash `low` · GLM-5.3-Flash `low` | **OpenCode** — `D=0`, both clear the bar |
| Wire a Jira → Slack → on-call n8n flow | `Sonnet 5.5 · high` | GLM-5.3-Flash `max` · DeepSeek V4.1 Flash `max` | **OpenCode**, low-confidence — AutomationBench has no interval, ITBench favours open models |
| Summarise 400 pages of filings into one memo | `Sonnet 5.5 · high` | DeepSeek V4.1 Flash `max` · GLM-5.3-Flash `max` | **Claude** — knowledge-work from `D=2` |
| Read 30 scanned receipts into a reconciliation table | `Sonnet 5.5 · high` | MiMo-V2.6-Pro `default` · DeepSeek V4.1 Flash `max` | **OpenCode**, low-confidence — both take images |
| Non-confidential conference pricing deck | `Sonnet 5.5 · high` | MiMo-V2.6-Pro `default` · GLM-5.3-Flash `max` | **Claude** — knowledge-work; Grok 4.7 stays premium |
| Read 3 regulator pages before labels go to print tonight | `Sonnet 5.5 · high` + review note | MiMo-V2.6-Pro `default` · GLM-5.3-Flash `max` | **Claude**, low-confidence — `R=3` and a single Omniscience lean |
| An earlier OpenCode attempt at a 30-file migration fell short | `Sonnet 5.5 · high` | MiMo-V2.6-Pro `default` · **Gemini 4 Argon** `high` | **Claude** — Rule A1-OC adds the `#2` (Argon on a GM1 row) and hands over the badge |
| Call somatic variants from tumour/normal exomes | `Fable 5.2 · high` | `unverified — use Claude` | **Claude** — availability gate; its biology classifiers can block research tasks |

</details>

<br>

## 🧱 The model pool

**Claude arm** — one model and one effort, picked by depth and context:

| Model | Role |
|---|---|
| **Haiku 5.5** | The cost pick for small, shallow work (`D ≤ 1` reading and transform tasks) |
| **Sonnet 5.5** | Daily work, the default start |
| **Opus 5.5** | Flagship for hard agentic code (`D = 3`) |
| **Opus 4.8** | Legacy — kept only for the offensive-security gate (`/fast` ends 30 Nov 2026) |
| **Fable 5.2** | Frontier scale (1000+ files) and biology-adjacent R&D (USD 8/40; `/fast` available) |
| **Mythos 5.2** | Fable 5.2 with permissive safeguards — Life Sciences Verification Program only |

**OpenCode Go arm** — the **19 rated models**, in tiers. Each Go model has its *own* monthly dollar cap, so what matters is how many *real* agent tasks a month of that cap buys. Tier membership is **by name** (Rule BUD1); the task counts below are one informational Arena snapshot (10 Nov 2026, every row from the same page):

| Tier | Models | Role |
|---|---|---|
| **Budget** — the default pairs | MiMo-V2.6-Flash 857 · DeepSeek V4.1 Flash 714 · GLM-5.3-Flash 375 · MiMo-V2.6-Pro 88 | 88–857 tasks per month of cap |
| **Non-confidential only** | GPT 6 Luna 188 · Muse Spark 1.3 130 | Offered only if you say the work isn't confidential — some of them train on prompts |
| **Premium** — escalation only | Kimi K3 18 · GLM-5.3 13 · Qwen3.8 Max 12 · Kimi K3.1 Pro 12 · Grok 4.7 5 | 5–18 tasks per month of cap; never in a routed pair, only as `#2` after a stated shortfall |
| **Gemini (GM1)** — overlay | Gemini 4 Argon | Go's plain `gemini-4-argon` (Not used / 0 days), open to confidential work; `#1` only at `D = 3` / `R = 3` on five rows, USD 30 cap — not a default pair |
| **Unrated** — never selected | Qwen3.8 Flash | Every row under that name is "Qwen3.8-Flash-Next", a different open-weights model; `n/p` |
| **Dominated** | DeepSeek V4 Pro · MiniMax M3 · Kimi K2.7 Code · Qwen3.7 Plus · Claude Haiku 5.5 · Gemini 3.8 Flash | Rated and tracked; no row ever emits them |

> Effort is the variant OpenCode *actually offers for that model* (`low` / `high` / `max`, `xhigh`, or `default`), never a value it would reject. DeepSeek V4.1 Flash writes `D ≤ 1` `low` and `D ≥ 2` `max` (`high` is offered but never emitted: AA-Briefcase and the Vals Terminal-Bench 4.0 effort chart separate it from `max`; this reverts the iteration-26 three-rung rule). DeepSeek's cap is USD 100 and its zero-retention agreement is valid through 30 Nov 2026. Go serves the **1017** build of DeepSeek V4.1 Flash, so every DeepSeek figure the router cites is a 1017 figure (older-revision numbers back no row or badge).

<br>

## 🔬 Built on evidence, not vibes

> **Evidence sets the direction and the equivalence band; the capability profile decides which evidence applies; efficiency breaks the ties capability leaves open. A leaderboard position on its own decides nothing.**

- **Benchmarks are bound to capabilities.** A pure-maths prompt gives Terminal-Bench a weight of zero.
- **Comparability first.** Benchmark, version, harness, tool access, scaffold *and* effort must match before two numbers are compared.
- **AA Intelligence Index v5 lives in its own column.** Every v4.3.2 II / TB / USD-per-task figure stays **frozen**; the v5 column holds only what was re-read on 10 Nov 2026, and the two versions are never compared.
- **AA Elo intervals decide ties.** AA publishes an Elo interval per row; a gap that sits inside that interval is not a direction, however large it looks.
- **Independent sources set the direction.** Artificial Analysis, DeepSWE v1.1 (with error margins), Agent Arena, Vals, FrontierSWE v2, ARC-AGI, Gray Swan — compiled into [`skill/opencode-evidence.json`](skill/opencode-evidence.json). One vendor re-citing the same figure is one number, not two. Vendor-reported effort curves are used only to pick an effort rung, never a direction.
- **A direction needs two independent measurements that agree.** A single one decides only at `R = 3`.
- **No interpolation** between effort rungs, and `n/p` (not published) is an answer.
- **The aggregate index never sets a direction** — it only licenses the efficiency tie-break.

Raw numbers live in [`skill/opencode-benchmarks.md`](skill/opencode-benchmarks.md) and [`skill/reference.md`](skill/reference.md). They are audit data and are **never loaded to route**, which keeps the token cost of a routing call low.

<br>

## ✅ Validation

`evals/routing/evals.json` is a deterministic regression set — **39 prompts** — graded by a pure-regex grader (no LLM in the loop). It checks the Claude model and effort, **both OpenCode picks** (model, effort, order), which side holds the badge, a non-trivial `Evidence:` line, and required / forbidden text for the confidentiality default.

```bash
python evals/routing/grade_routing.py --selftest --results-dir /tmp/x   # goldens vs grader
python scripts/check_policy_sync.py      # SKILL.md rule blocks == evals/policy/routing_policy.json
python scripts/check_opencode_pool.py    # pool, Step 4-OC rows, badge table, per-model variants, consensus top-4
python scripts/check_examples.py         # every worked example agrees with its golden
python scripts/check_readme_facts.py     # counts, pool size, iteration and tier tables in the docs match the data
```

These are exactly what [`checks.yml`](.github/workflows/checks.yml) runs on every push and pull request. To print the independent-evidence consensus per capability: `python scripts/derive_opencode_rows.py`.

**Where it stands (12 Nov 2026, iteration-29):** all of the checks above pass, including `check_readme_facts.py`; `--selftest` is **39/39**. A cold run of the **18 prompts whose OpenCode line carries DeepSeek** (one fresh agent per prompt, reading only `skill/SKILL.md`) scored **17/18**; the one miss (`w4`, an omitted Zen twin) passed **3/3** on re-run. `i1` was skipped and the trigger eval is still a proxy. Details in [`evals/README.md`](evals/README.md).

### Known limits, stated plainly

- **The trigger eval is a proxy.** Nested `claude -p` can't authenticate in the build environment; run `evals/trigger/run_trigger.py` from a logged-in terminal for the real number.
- **The biology gate is fixed at `high` effort.** Its biology classifiers may block research tasks: on the first flagged request Claude Code moves the session to Opus 5, and later biology-flagged requests are refused. The gate does not take the D table's `xhigh`: Anthropic's vendor-reported table has Fable 5.2 at `high` matching Opus 5.5 at `max` on FrontierCode 2.0, and Fable draws on a separate weekly limit.
- **The 1000+ files gate uses the normal D rung.** It fixes Fable 5.2, not the effort: `xhigh` at D=3, `max` only under M1, `ultracode` over 30 minutes. It is a scale gate, not a classifier carve-out, so a mechanical 1000-file rename stays lower.
- **Prices, caps and retention terms are dated.** They are a snapshot (see each row's date) and OpenCode Go can change them — corrections with a primary source are the most valuable contribution.
- **OpenCode-by-default is a trade-off.** At `D = 2` the router sends coding to OpenCode although Claude still leads some hardest-task anchors, because the mid-difficulty DeepSWE comparison is a tie at a fraction of the cost. If you'd rather pay Claude there, it's one row of the badge table in [`skill/SKILL.md`](skill/SKILL.md).
- **Only `SKILL.md` is the source of truth** for routing; the `claude-ai/` fallback is a hand-synced derivative.

<br>

## 🗂 Repository map

```text
skill/                       The skill itself — only SKILL.md is read when routing
  SKILL.md                   Routing rules (the single source of truth)
  opencode-benchmarks.md     OpenCode evidence, per model, with sources
  opencode-evidence.json     Machine-readable evidence the checks derive from
  reference.md               Claude prices, limits, benchmark notes (audit data)
evals/                       Regression set, grader, policy mirror, recent run history
scripts/                     Consistency checks and evidence tooling
docs/                        How it works, assets, launch notes
dist/model-secici.zip        Ready-to-upload claude.ai skill
claude-ai/                   Plain-text fallback when code execution is off
install.sh · install.ps1     One-command installs for Claude Code
.github/workflows/          CI: the checks above on every push and pull request
CHANGELOG.md                 Every policy iteration, newest first
```

## 🤝 Contributing

Corrections to model specs, prices, caps, retention terms, effort defaults or **benchmark records** are very welcome — cite the primary source and put the harness, effort and date next to the number. Rule changes must keep the checks above green. See **[CONTRIBUTING.md](CONTRIBUTING.md)**.

## 📄 License

MIT — see [LICENSE](LICENSE).

<div align="center">
<br>

*Protects your rate-limit windows — not your wallet.*

</div>
