# Launch plan

Honest framing first: stars come from a real, widespread pain solved cleanly plus
being seen at the right moment plus luck. You can control the first two. "Tens of
thousands" is top-0.1% territory for an individual dev tool; a good outcome for a
well-executed launch is hundreds to low thousands. Don't buy stars or run
mutual-star rings — it gets the repo flagged and kills its credibility.

The biggest lever you haven't pulled: **the skill body is still Turkish.** An
English README on a Turkish skill caps reach hard. If you can port
`SKILL.md` + `reference.md` to English (same rules, re-run the eval iteration),
do that *before* launch — it roughly changes the addressable audience by 20x.

---

## Pre-launch checklist

- [ ] Repo is public, description set (see below), topics added
- [ ] `LICENSE` copyright line has your real name/handle
- [ ] `git config user.name` / `user.email` are the identity you want on commits
- [ ] README renders correctly on GitHub (tables, the code blocks)
- [ ] Social preview image set (Settings → General → Social preview) — even a
      plain card with the two-line output example converts well
- [ ] A 10-second asciinema/GIF of `/model-secici <task>` → two-line output,
      embedded near the top of the README
- [ ] `evals` run is green and the iteration folder is committed
- [ ] One "good first issue" open (e.g. "English port of SKILL.md §X")
- [ ] You're available for ~4 hours after posting to answer comments fast

## GitHub repo settings

**Description:**
> Routes a task to the cheapest Claude *and* Codex/ChatGPT model + effort level that clears the bar — protects your rate-limit windows, not your wallet.

**Topics:** `claude` `claude-code` `anthropic` `chatgpt` `codex` `llm` `ai-agents`
`prompt-engineering` `developer-tools` `model-routing` `skill`

## Timing

Tuesday–Thursday, ~8–10am US Eastern (that's afternoon in TR). Avoid Fridays,
weekends, and major AI-news days (model launches, big keynotes) — you'll be
buried.

---

## Show HN

**Title:**
`Show HN: A router that picks the cheapest Claude/GPT model + effort for a task`

**Body:**
> I kept reflexively running everything on the most expensive model and burning
> my Claude 5-hour window (and ChatGPT Plus's), so I wrote a decision procedure
> that scores a task on four axes — risk, depth, breadth, context — and outputs
> which model and effort level to use, for both ecosystems, in two lines. It
> doesn't run the task, it just routes it.
>
> The interesting design choice: risk *doesn't* raise the model tier, only the
> human-oversight note. Forcing risky work onto the flagship model, then walking
> it back with a second rule, is what made my earlier version collapse every
> prompt onto the same two models.
>
> It's sourced from the official docs, every uncertain claim is labelled, and
> there's a deterministic regression eval (cold agents read the rules fresh and
> route a fixed prompt set; a regex grader checks the output). Currently 17/17.
>
> Caveat: the rule file is currently written in Turkish (my working language);
> the README is English and an English port is the top open issue.
>
> Repo: <link>

Then a first comment from you with the concrete "here's what it does" example and
the honest limitations (Turkish skill body, model-name/price data has a shelf
life, Codex safety-fallback behaviour is unverified so it punts to Claude).

## r/ClaudeAI (and cross-post to r/LocalLLaMA, r/OpenAI)

**Title:**
`I built a skill that tells you which model + effort to use for a task (Claude + GPT-5.6)`

**Body:**
> Short version: paste a task, it replies with two lines —
> `Claude: Sonnet 5 · effort: high` / `Codex: Terra · effort: low` — and doesn't
> run anything.
>
> It's built around one idea: the thing you're actually running out of is your
> rate-limit window, not money, and the common mistake is reaching for Opus/the
> biggest model by reflex. So it scores risk/depth/breadth/context and maps to
> the cheapest model that clears the bar, rounding down on ties.
>
> Install is one PowerShell line for Claude Code, or a zip upload for claude.ai.
> MIT, sourced from the official docs, has a regression eval suite.
>
> The rule file is Turkish right now (working on an English port). README is
> English. Feedback and data corrections very welcome.
>
> <link>

## X / Bluesky thread

1. You don't run out of money on Claude/ChatGPT. You run out of your 5-hour
   window. And you burn it by reaching for the biggest model by reflex.
   I built a router for that. 🧵
2. Paste a task → it tells you the cheapest model + effort that clears the bar,
   for Claude *and* Codex/ChatGPT, in two lines. It doesn't run the task.
   [GIF of the two-line output]
3. Design choice I'm happiest with: risk raises the *human-review note*, not the
   model tier. Forcing risky work onto the flagship and walking it back is what
   made v1 collapse every prompt onto the same 2 models.
4. Everything's sourced from the official docs, uncertain claims are labelled,
   and there's a deterministic eval suite — cold agents route a fixed prompt set,
   a regex grader checks it. 17/17 right now.
5. MIT. One-line install for Claude Code. English port of the rules is the top
   open issue if anyone wants a first PR. <link>

---

## After posting

- Reply to every comment in the first few hours, especially corrections — "good
  catch, fixed in <commit>" builds more goodwill than the feature itself.
- If someone reports a wrong price / spec / effort default, fix it fast and
  thank them in the changelog. Model data ages; visible maintenance is the
  signal that keeps a repo alive.
- Add a `CHANGELOG.md` after the first few fixes land.
- Don't relaunch the same post if it flops. Improve, wait a month, try a
  different angle (e.g. after the English port).
