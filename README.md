# model-effort-router

**Paste a task. Get told which model and effort level to run it on — for Claude and for your OpenCode Go subscription (the two best of its 15 main models, in order, each with its own effort) — and which of the two is actually the better fit for *that* task.** It does *not* run the task; it routes it.

Installed as a Claude Code / claude.ai skill invoked with `/model-secici`.

```
You:    /model-secici  Refactor the payment module across these 40 files to use the new idempotency-key API, update every caller, and make the test suite pass.

model-secici:
  Claude:   Sonnet 5.5 · effort: high
  OpenCode: ✅ RECOMMENDED AI · #1 MiMo-V2.6-Pro · effort: max · #2 GLM-5.3 · effort: max
  Evidence: AA's Terminal-Bench 4.0 has Sonnet 5.5 at 64 against GLM-5.3 at 42 and
            MiMo-V2.6-Pro at 35 with no interval, and one row is not a direction,
            so cap pressure decides — USD 0.13 and 64k output tokens per task
            against USD 7.67 and 193k; low-confidence.
```

The badge is **computed, not habitual** — swap the task and it moves:

```
You:    /model-secici  Write the Q3 supplier-risk memo for the board from our internal spend data

model-secici:
  Claude:   ✅ RECOMMENDED AI · Sonnet 5.5 · effort: high
  OpenCode: #1 MiMo-V2.6-Pro · effort: max · #2 Qwen3.8 Flash · effort: max
  Evidence: The finished memo is knowledge-work, where two AA rows agree for Claude
            (GDPval-AA 1839 vs 1686, AA-Briefcase 1823 vs 1516), and internal spend
            data is confidential so the 30-day-retention and training models are
            out of the pool.
```

```
You:    /model-secici  Label these 200 customer reviews as positive/negative

model-secici:
  Claude:   Haiku 4.5
  OpenCode: ✅ RECOMMENDED AI · #1 DeepSeek V4.1 Flash · effort: low · #2 MiMo-V2.6-Flash · effort: low
  Evidence: Both arms clear the bar for mechanical classification, and DeepSeek V4.1
            Flash streams 222 tok/s at USD 0.27 per index task on a USD 60 cap
            against Haiku 4.5's USD 1/USD 5 pricing.
  DeepSeek V4.1 Flash: peak hours cost 2× (04–07 and 09–13 TR time, Mon–Fri); …
```

> The skill body (`skill/SKILL.md`, plus `opencode-benchmarks.md` and `reference.md`) and its output are English. It routes prompts in any language. 🇹🇷 A longer
> Turkish walkthrough is in **[README.tr.md](README.tr.md)** (its iteration-21 section is at the top; the rest is the Codex-era history).

---

## What changed in iteration-21 (6 Oct 2026): the Codex arm is gone, OpenCode Go is in

The second arm used to be Codex/ChatGPT (Luna / Sol / Sol Ultra / Astra). The Codex
subscription ended, so the arm was **re-derived from scratch for OpenCode Go (USD 10/month)**.
Claude's arm is untouched. The last Codex-era policy is the git tag `iteration-20-codex`
and `archive/iteration-20-codex/`.

- **Two models, in order, each with its own effort.** The router first *selects* the two
  best of the pool for the task (`#1`, `#2`), then picks each one's effort.
- **The 15 main models** — chosen from the 30 on `opencode.ai/docs/go` (the other 15 are
  superseded, preview, free, vision-experimental or have no independent measurement):

  | Role | Models |
  |---|---|
  | Default / reasoning | **MiMo-V2.6-Pro** (AA 46 at USD 0.13/task — best index per dollar) |
  | Coding | **GLM-5.3** (Terminal-Bench 4.0 **42**, the pool's best) · GLM-5.3-Flash (TB 33, USD 60 cap) |
  | Factual / long context / images | **Kimi K3** (AA-LCR 89, Omniscience 20, GDP.pdf 22) |
  | Workflow / latency / bulk | **DeepSeek V4.1 Flash** (AutomationBench-AA **69**, 222 tok/s) · MiMo-V2.6-Flash |
  | Knowledge-work | **Grok 4.7** (non-confidential only) · Qwen3.8 Flash |
  | Escalation | Qwen3.8 Max |
  | Opt-in, non-confidential | Muse Spark 1.3 Contributor (AA 48, but **trains on your prompts**) · GPT 6 Luna (30-day retention) |
  | Rated, **dominated**, never emitted | DeepSeek V4 Pro · MiniMax M3 · Kimi K2.7 Code · Qwen3.7 Plus |

- **Caps are per model.** Go gives each model its own monthly dollar cap (USD 15 for the
  expensive ones, 30 or 60 for the cheap ones); the 5-hour window is 20% of it and the weekly
  50%. So the router reserves the USD 15 models for `D ≥ 2`, sends `D ≤ 1` to the USD 60
  Flash tier, and names the next model of a tier chain when a window runs out.
- **Effort is data-driven, and coarse on purpose.** Only `low` and `max` have published
  open-model data (GLM-5.3 34 → 45, Kimi K3 30 → 44). `GLM-5.3 · low` is *dominated* by
  GLM-5.3-Flash (42 at a quarter of the cost), so the Pro tier is only ever emitted at
  `max`; lower depth means a different (Flash) *model*, not a lower rung. No interpolation.
- **Confidential by default.** Grok 4.7 and GPT 6 Luna keep prompts 30 days and Muse Spark
  Contributor trains on them, so all three are out of the pool unless you say the work is
  non-confidential (Rule NC1). DeepSeek's zero-retention agreement is valid through
  31 Oct 2026 and renewed monthly — the router prints that caveat.
- **The evidence is fresh and several earlier assumptions did not survive it:** Kimi K3 is
  *last* (not first) on knowledge-work benchmarks; Grok 4.7's AA Terminal-Bench is 26
  (below DeepSeek V4.1 Flash's 27); GLM-5.3 — not Grok — is the strongest measured coder;
  four of the 15 are dominated outright. Everything is in
  **[`skill/opencode-benchmarks.md`](skill/opencode-benchmarks.md)** with sources.

### The honest consequence

AA publishes no confidence interval for any row, and this router's rule is that *no
interval ⇒ `UNRESOLVED`, however large the gap looks*. So even Sonnet 5.5's 22-point
Terminal-Bench lead over GLM-5.3 is a **lean, not a certified direction**: at `R ≤ 2`
coding falls to efficiency and reads **OpenCode (low-confidence)**; at `R = 3` the single
measurement decides and reads **Claude**. Claude keeps a clean badge only where two
independent AA rows agree — **knowledge-work** and **deep-reasoning** — and on the product
mechanisms OpenCode lacks (`ultracode`, `opusplan`), plus every gate OpenCode declines
(offensive security, biology, computer-use). If you would rather certify the coding lead
with a binomial interval from AA's published 66-task count, that is one rule (see
`skill/opencode-benchmarks.md` §5) and it would flip the coding rows to Claude.

---

## Why this exists

The failure mode isn't picking a model that's too weak. It's **reflexively picking
the most expensive model** and burning your quota — Claude's 5-hour window *and* a
Go model's per-model dollar cap. Those are the protected resources.

The decision principle, in one sentence:

> **Select the lowest-quota model × effort combination that stays on the
> task-specific capability frontier.** Prefer the stronger candidate when the
> task-relevant performance difference is meaningful; prefer the more
> quota-efficient candidate when capability sits inside a defensible equivalence
> band.

Not "always cheapest". Not "always strongest". Not "highest benchmark score wins".

```
prompt
  → quality gate                     (Step 0)
  → hard gates: capability/safety/availability/retention   (Step 1)
  → task capability profile          (Step 2)
  → R/D/W/C + scope                  (Step 3)
  → candidate model × effort         (Step 4: Claude; Step 4-OC: two OpenCode models, then efforts)
  → benchmark evidence · comparability · equivalence · dominance (Step 5)
  → cross-ecosystem comparison → ✅ RECOMMENDED AI + Evidence line (Step 6)
  → quota guards + data-policy lines (Step 7)
```

## Data honesty

> **Evidence sets the direction and the equivalence band; the capability profile
> decides which evidence applies; efficiency breaks the ties capability leaves
> open. A leaderboard position on its own decides nothing.**

- **Benchmarks are bound to capabilities.** A pure maths prompt gives Terminal-Bench a weight of zero.
- **Comparability is checked first.** Benchmark, version, harness, tool access, scaffold *and* effort must match.
  Traps in the record: Z.ai's launch table (vendor-reported, Terminal-Bench 2.1 88.2 — saturated); AA's Coding Agent
  Index is a harness × model aggregate that *contains* Terminal-Bench 4.0, so it is not a second measurement;
  AA prices differ from Go prices (Muse Spark, DeepSeek peak/off-peak).
- **No interpolation between effort rungs**, and `n/p` (not published) is an answer.
- **A direction needs two independent measurements that agree (BD1);** a single one decides only at `R=3`.
- **The aggregate index never sets a capability direction** — it only licenses the efficiency tie-break.

Raw evidence for the Claude side lives in `skill/benchmarks.json` / `skill/benchmark_frontiers.json`
(Codex-era snapshot; the Claude rows are unchanged), and for OpenCode in
`skill/opencode-benchmarks.md`. Only `SKILL.md` is read when routing.

---

## Install

It's a [Claude skill](https://docs.claude.com/en/docs/claude-code/skills) — a
`model-secici/` folder. Only `SKILL.md` is read when routing; the rest are there
for auditing a rule.

```bash
git clone https://github.com/enzoo808/model-effort-router.git
cd model-effort-router
```

### Claude Code

**macOS / Linux:** `./install.sh` · **Windows (PowerShell):** `.\install.ps1`

**Or by hand:**
```bash
mkdir -p ~/.claude/skills/model-secici
cp skill/*.md skill/*.json ~/.claude/skills/model-secici/
```

Start a new Claude Code session, then `/model-secici  <your task>`. It also triggers on
"which model should I use for this?".

### claude.ai / Claude Desktop (native custom skill)

Requires a Pro / Max / Team / Enterprise plan with **code execution** enabled. Download
**[`dist/model-secici.zip`](dist/model-secici.zip)** (rebuild with `.\build-claude-ai-zip.ps1`),
then **claude.ai → Settings → Features → Custom Skills → Upload**. No code execution? Use the
plain-text fallback in [`claude-ai/instructions.tr.md`](claude-ai/instructions.tr.md) (Turkish).

### OpenCode Go

There is no skill mechanism on the OpenCode side — the router just produces the `OpenCode:`
line (two models, each with an effort) for you to act on. In OpenCode, pick the model by its
id `opencode-go/<model-id>` and cycle the effort with `variant_cycle`.

---

## How it decides

| Step | What happens |
|---|---|
| **0 · Quality gate** | Four mechanical checks. If any fires → **no model, no badge, one `Clarify:` line.** |
| **1 · Hard gates** | Claude: sub-second/bulk → Haiku; offensive security → Opus 4.8; biology → Fable 5.1; 1000+ files → Fable 5.1. **OpenCode: offensive security / biology / computer-use → `use Claude` (no models); confidential work removes Muse Spark, Grok 4.7 and GPT 6 Luna; context > 500k removes Grok, > 256k Qwen3.8 Flash, > 200k MiMo-V2.6-Flash; image input removes GLM-5.3; bulk/latency → DeepSeek V4.1 Flash.** |
| **2 · Capability profile** | One or two tags (`agentic-code`, `deep-reasoning`, `knowledge-work`, `long-context`, `workflow-automation`, …) — what makes benchmark evidence applicable or not. |
| **3 · Score scope & stakes** | **R**isk, **D**epth, **W**idth, **C**ontext — each 0–3. |
| **4 · Candidate model × effort** | Claude: model ← `max(D,C)` + profile; effort ← D (`low/medium/high/xhigh`), `ultracode` on 3+ phases, `opusplan`. **OpenCode (4-OC): `D ≤ 1` → GLM-5.3-Flash · MiMo-V2.6-Flash; otherwise a per-capability pair from the table, flipped at `R=3` where a single measurement leans; effort `low` at `D ≤ 1`, `max` at `D ≥ 2` (Grok `xhigh`).** |
| **5 · Evidence, equivalence, efficiency** | Comparability → published dispersion only → dominance (Go cap pressure first for OpenCode). |
| **6 · `✅ RECOMMENDED AI`** | Hard gate → applicable capability → benchmark confidence → BD1 → near-parity → efficiency. MECH1 lets `ultracode` / `opusplan` win. One badge, one `Evidence:` sentence. |
| **7 · Quota guards** | `R=3` → human-review note. Escalation is a model change. Data-policy and DeepSeek lines are auto-added. |

Two design choices carried over: **risk raises human oversight, not model tier**, and
**when in doubt, round down**.

---

## Examples

| Task | Claude | OpenCode `#1` · `#2` | Recommended |
|---|---|---|---|
| Label 200 reviews positive/negative | `Haiku 4.5` | DeepSeek V4.1 Flash `low` · MiMo-V2.6-Flash `low` | **OpenCode** — latency row, a USD 60 cap |
| Bump `MAX_RETRIES` 3→5 in the prod config | `Sonnet 5.5 · low` + review note | GLM-5.3-Flash `low` · MiMo-V2.6-Flash `low` | **OpenCode**, low-confidence — `D=0`; Flash `low` is unmeasured |
| Refactor the payment module across 40 files | `Sonnet 5.5 · high` | MiMo-V2.6-Pro `max` · GLM-5.3 `max` | **OpenCode**, low-confidence — one Terminal-Bench row is not a direction |
| Stand up staging from scratch (Terraform, 12 services, seed, smoke) | `Sonnet 5.5 · ultracode` | MiMo-V2.6-Pro `max` · GLM-5.3 `max` | **Claude** — three phases; `ultracode` has no OpenCode equivalent (MECH1) |
| Find the race condition that flakes in prod | `Opus 5.5 · xhigh` | MiMo-V2.6-Pro `max` · GLM-5.3 `max` | **Claude** — two agreeing AA rows on the reasoning half |
| Design and implement the irreversible transaction boundary | `Opus 5.5 · max` + review note | MiMo-V2.6-Pro `max` · GLM-5.3 `max` | **Claude** — `R=3` and a reasoning direction |
| Redesign auth for 200 services from scratch | `opusplan · plan: max · execute: medium` | MiMo-V2.6-Pro `max` · Kimi K3 `max` | **Claude** — `opusplan` mechanism |
| Wire a Jira → Slack → on-call n8n flow | `Sonnet 5.5 · high` | DeepSeek V4.1 Flash `max` · GLM-5.3 `max` | **OpenCode**, low-confidence — AutomationBench 69 vs 72 |
| Summarise 400 pages of filings into one memo | `Sonnet 5.5 · high` | MiMo-V2.6-Pro `max` · Kimi K3 `max` | **Claude** — knowledge-work has a direction, long-context does not |
| Read 30 scanned receipts into a reconciliation table | `Sonnet 5.5 · high` | MiMo-V2.6-Pro `max` · Kimi K3 `max` | **OpenCode**, low-confidence — GLM-5.3 is text-only so it is out |
| Non-confidential conference pricing deck | `Sonnet 5.5 · high` | **Grok 4.7 `xhigh`** · MiMo-V2.6-Pro `max` + data line | **Claude** — NC1 re-admits Grok |
| An earlier OpenCode attempt at a 30-file migration fell short | `Sonnet 5.5 · high` | MiMo-V2.6-Pro `max` · **Qwen3.8 Max** `max` | **OpenCode**, low-confidence — Rule A1-OC |
| Exploit PoC for a CVE | `Opus 4.8 · xhigh` | `use Claude` | **Claude** — the other arm declines |
| Call somatic variants from tumour/normal exomes | `Fable 5.1 · high` | `unverified — use Claude` | **Claude** — availability gate |
| "Fix this code" | *(no model, no badge — asks: which code? broken how? done = ?)* | | |

---

## Validation

`evals/routing/evals.json` is a deterministic regression set (22 prompts) graded by
`evals/routing/grade_routing.py` (pure regex, no LLM): Claude model + effort, **both OpenCode
picks (model, effort, order)**, which side carries the badge, a non-trivial `Evidence:` line
(whose `low-confidence` flag must match the row's dagger), plus required / forbidden text
for the auto-added lines and the confidentiality default.

```bash
python evals/routing/grade_routing.py --selftest --results-dir /tmp/x   # goldens vs grader
python scripts/check_policy_sync.py        # SKILL.md rule blocks == evals/policy/routing_policy.json
python scripts/check_opencode_pool.py      # the 15-model pool, Step 4-OC rows, badge table, examples
python scripts/check_examples.py           # every worked example agrees with its golden
```

> **Honest status.** The goldens are derived from the rules; **a cold-agent run (fresh
> agents routing each prompt from `SKILL.md`) has not been done for iteration-21**, and
> neither has the trigger eval. Both need live agents — run them before trusting the
> goldens, as every earlier iteration did.

Run history and the reasoning behind every rule change is in
[`evals/README.md`](evals/README.md).

## Contributing

Corrections to model specs, prices, caps, retention terms, effort defaults or **benchmark
records** are very welcome — cite the primary source and add the harness/effort/date next to
the number. Rule changes must keep the checks above green. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).
