## What changed

<!-- One or two lines. -->

## Type

- [ ] Data correction (spec, price, effort default, safety behaviour)
- [ ] Routing-rule change
- [ ] Docs / tooling only

## Checklist

- [ ] Primary source cited for every new number (or marked unverified)
- [ ] `skill/opencode-evidence.json`, `skill/opencode-benchmarks.md`, `skill/reference.md` and `skill/SKILL.md` agree
- [ ] Rule change: eval added/updated and mirrored in `evals/policy/routing_policy.json`
- [ ] `README.md` and `README.tr.md` (and `claude-ai/instructions.tr.md`) in sync, or the lag is flagged below
- [ ] CI commands pass locally:
  `python evals/routing/grade_routing.py --selftest`, `python scripts/check_policy_sync.py`, `python scripts/check_opencode_pool.py`, `python scripts/check_examples.py`, `python scripts/check_readme_facts.py`

## Notes

<!-- Anything reviewers should know. -->
