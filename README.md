# model-effort-router

**Paste a task. Get told which model and effort level to run it on — for both Claude and Codex/ChatGPT, in two lines.** It does *not* run the task; it routes it.

Installed as a Claude Code / claude.ai skill invoked with `/model-secici`.

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

It's a [Claude skill](https://docs.claude.com/en/docs/claude-code/skills) —
two Markdown files (`skill/SKILL.md` + `skill/reference.md`) that live in a
`model-secici/` folder. "Installing" is just putting that folder where Claude
looks for skills.

```bash
git clone https://github.com/enzoo808/model-effort-router.git
cd model-effort-router
```

### Claude Code

**macOS / Linux:**
```bash
./install.sh
```

**Windows (PowerShell):**
```powershell
.\install.ps1
```

**Or by hand (any OS)** — the scripts just do this:
```bash
mkdir -p ~/.claude/skills/model-secici
cp skill/SKILL.md skill/reference.md ~/.claude/skills/model-secici/
```

Restart Claude Code (or run `/doctor` to reload skills), then:
```
/model-secici  <your task>
```
It also triggers on its own when you ask things like "which model should I use
for this?".

Prefer it project-scoped instead of user-scoped? Put the `model-secici/` folder
under `.claude/skills/` in your repo.

### claude.ai / Claude Desktop (native custom skill)

Requires a Pro / Max / Team / Enterprise plan with **code execution** enabled.

1. Download **[`dist/model-secici.zip`](dist/model-secici.zip)** from this repo
   (open the file → *Download raw file*). Or rebuild it after edits:
   `.\build-claude-ai-zip.ps1` (Windows).
2. **claude.ai → Settings → Features → Custom Skills → Upload** → pick the zip.

It then runs in every chat, no project needed.

**No code execution?** Use the plain-text fallback in
[`claude-ai/instructions.tr.md`](claude-ai/instructions.tr.md): paste the text
below the line into a Project's *Custom instructions*. (Bound to that one
Project, and it's the Turkish variant — an English port is welcome.)

### Codex / ChatGPT

There's no skill mechanism on the Codex side — the router just produces the
`Codex:` line for you to act on. Run `model-secici` on the Claude side (or the
claude.ai fallback) and read both lines.

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

Latest run (**iteration-10**, cold agents against the current `SKILL.md`):
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
