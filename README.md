# model-secici — a model & effort router for Claude Code and Codex/ChatGPT

**Paste a task. Get told which model and effort level to run it on — for both Claude and Codex/ChatGPT, in two lines.** It does *not* run the task; it routes it.

```
You:    /model-secici  Move the repo's auth flow to OAuth2

model-secici:
  Claude: Sonnet 5 · effort: high
  Codex:  Terra · effort: low
```

That's the whole idea. One more:

```
You:    /model-secici  Find the race condition that flakes in prod sometimes

model-secici:
  Claude: Opus 5 · effort: max
  Codex:  Sol · effort: max
  Do not apply without human review.
```

> The skill body (`skill/SKILL.md` + `skill/reference.md`) and its output are
> English. It routes prompts in any language. 🇹🇷 A longer Turkish walkthrough of
> the decision logic is in **[README.tr.md](README.tr.md)**.

---

## Why this exists

The failure mode isn't picking a model that's too weak. It's **reflexively picking
the most expensive model** and burning your rate-limit window — Claude's 5-hour
quota *and* ChatGPT Plus's 3-hour / weekly windows. Those are the protected
resource, not dollars.

`model-secici` scores every task on four axes (risk, depth, breadth, context) and
maps that to the *cheapest model that actually clears the bar*, on **both**
ecosystems at once. When in doubt it rounds **down**.

It's a ~700-line decision procedure, not a vibe. Every rule is sourced from
`platform.claude.com` / `openai.com` docs, every uncertain claim is labelled, and
there's a deterministic regression eval suite (currently **17/17**, cold-agent
re-run after the 2 Sep 2026 English port).

---

## Install

### Claude Code

```powershell
.\install.ps1        # copies skill/ -> ~/.claude/skills/model-secici/
```

Restart Claude Code, then:

```
/model-secici  <your task>
```

### claude.ai (native custom skill)

```powershell
.\build-claude-ai-zip.ps1                 # -> dist/model-secici.zip
```

Then **claude.ai → Settings → Features → Custom Skills → Upload** →
`dist/model-secici.zip`. (Requires Pro/Max/Team/Enterprise + code execution.)
A no-code fallback for when code execution is off lives in
[`claude-ai/instructions.tr.md`](claude-ai/instructions.tr.md).

---

## How it decides

| Step | What happens |
|---|---|
| **0 · Quality gate** | Four mechanical checks (rule stated by example but not generalised? silent-wrong-result risk? concrete target? two plausible readings?). If any fires → **no model, ask a clarifying question.** |
| **1 · Hard gates** | Sub-second / high-volume → **Haiku**. Offensive security (exploit, pentest, binary scanning) → **Opus 4.8 · xhigh**. Biology R&D → **Fable 5.1**. >200k context → drops Haiku. 1000+ files → **Fable 5.1**. |
| **2 · Score** | **R**isk, **D**epth, **W**idth, **C**ontext — each 0–3, each with a diagnostic question and a worked-example library. |
| **3 · Map** | Model ← `max(D, C)` — **not** risk. Opus 5 only when `D=3`. Effort ← `D`. `ultracode` when `W=3 ∧ >30 min ∧ ¬(D=3 ∧ R=3)`. |
| **4 · Quota guards** | `R=3` adds a human-review note (never changes the model). MCP-server bloat, auto-accept, alias drift warnings. |

Key design choice: **risk raises human oversight, not model tier.** The old
approach forced risky work onto the priciest model, then walked it back with a
second rule — convoluted, and it collapsed every prompt onto the same two models.

---

## The rosters

**Claude (as of 1 Sep 2026):**

| Model | Role | $/Mtok in·out |
|---|---|---|
| Haiku 4.5 | speed / volume, no effort param | $1 / $5 |
| **Sonnet 5** | daily driver, default starting point | $3 / $15 |
| **Opus 5** | flagship — complex agentic code, enterprise | $5 / $25 |
| Opus 4.8 | legacy — kept **only** for the offensive-security gate | $5 / $25 |
| **Fable 5.1** | frontier scale, long-horizon autonomy, biology-adjacent R&D | $10 / $50 (cache reads ¼: $0.25) |
| Mythos 5.1 | = Fable 5.1 with permissive safeguards, **Project Glasswing invite only** | — |

**Codex / ChatGPT (GPT-5.6 family):**

| Model | Role | rough Claude analogue |
|---|---|---|
| Luna | speed / volume, cheapest | Haiku 4.5 |
| Terra | balanced daily driver | Sonnet 5 |
| **Sol** | flagship — code / science / security | Opus 5 |
| **Sol Ultra** | a Codex *mode* on Sol (Plus+): ~4 collaborating agents in parallel | stronger than Claude's `ultracode` |

Offensive-security and biology-R&D prompts always route to Claude — the Codex
side has no verified safety-fallback chain, so it honestly says
`unverified — use Claude` instead of guessing.

---

## Examples

| Task | Claude | Codex |
|---|---|---|
| Label 200 customer reviews positive/negative | `Haiku 4.5` | `Luna · minimal` |
| Add dark mode to this React component | `Sonnet 5 · medium` | `Terra · low` |
| Add cursor-based pagination to this API | `Sonnet 5 · medium` | `Terra · low` |
| Audit this genomics pipeline's variant-calling logic | `Fable 5.1 · high` | `unverified — use Claude` |
| Pentest this 180-service environment, build auth-bypass chains | `Opus 4.8 · ultracode` | `unverified — use Claude` |
| Split this 6000-file legacy monolith into services | `Fable 5.1 · max` + review note | `Sol · max` + review note |
| Bump `MAX_RETRIES` 3→5 in the prod config | `Sonnet 5 · low` + review note | `Terra · minimal` + review note |
| "Fix this code" | *(no model — asks: which code? broken how? done = ?)* | |

---

## Validation

`evals/routing/evals.json` is a deterministic, re-runnable regression set graded
by `evals/routing/grade_routing.py` (pure regex, no LLM). The protocol: spin up
**cold agents** that read `skill/SKILL.md` fresh and route each prompt; grade the
raw output.

Latest run (**iteration-9**, cold agents against the English `SKILL.md`):
**17/17 auto-graded pass**. Run history and the reasoning behind each rule change
is in [`evals/README.md`](evals/README.md).

---

## Data honesty

The single most important rule in this repo: **don't inherit an old model's
benchmark numbers onto a new one.** Leaderboards (LiveBench, BenchLM BenchAlign,
Artificial Analysis) only confirm the *direction* of a routing rule — the router
never selects a model from a benchmark score. Aggregate scores mislead
(BenchAlign ranks Sonnet 5 at #39 purely from thin benchmark coverage; LiveBench,
with full coverage, puts it at 76.0). See `skill/reference.md` §2 / §7 / §9 for
every disputed number and why it's flagged.

---

## Contributing

Corrections to model specs, prices, effort defaults, or safety-fallback behaviour
are very welcome — cite the primary source. Rule changes must keep the eval suite
green (`python evals/routing/grade_routing.py --results-dir <new iteration>`).
See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).
