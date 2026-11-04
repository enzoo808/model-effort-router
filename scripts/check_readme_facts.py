#!/usr/bin/env python3
"""Fail when a number or a model list copied into the docs no longer matches the data.

The eval count, the pool size and the policy iteration are written by hand into the
READMEs, the badges, hero.svg and the social preview. Nothing else compares them
with the files they describe, so they drift: the social preview once said "30
regression evals" while evals/routing/evals.json held 36.

What is checked (stdlib only, no network):
  * eval count         evals/routing/evals.json  vs README badges and prose, hero.svg,
                       docs/social-preview.html
  * pool size          evals/policy/routing_policy.json  vs "19 rated models" wording
  * policy iteration   routing_policy.json, skill/SKILL.md, CHANGELOG.md and both
                       README badges / status lines must name the same iteration
  * tier tables        every pool model must appear in the README row of its tier

Every pattern must match at least once in its file, so rewording a sentence cannot
silently switch a check off - it fails with "pattern not found" until the guard is
updated.

    python scripts/check_readme_facts.py [--root PATH]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    root = Path(ap.parse_args().root)

    def read(rel: str) -> str:
        return (root / rel).read_text(encoding="utf-8")

    evals = json.loads(read("evals/routing/evals.json"))["evals"]
    policy = json.loads(read("evals/policy/routing_policy.json"))
    models: dict = policy["pool"]["models"]
    n_evals, n_models = len(evals), len(models)
    iteration = re.fullmatch(r"iteration-(\d+)", policy["policy_version"])
    if not iteration:
        print(f"unexpected policy_version {policy['policy_version']!r}")
        return 1
    it = int(iteration.group(1))

    errors: list[str] = []
    checks = 0

    def expect(rel: str, pattern: str, want: int, what: str) -> None:
        nonlocal checks
        found = [int(m) for m in re.findall(pattern, read(rel))]
        if not found:
            errors.append(f"{rel}: pattern not found for {what}: /{pattern}/ (update this guard if the wording changed)")
            return
        for value in found:
            checks += 1
            if value != want:
                errors.append(f"{rel}: {what} says {value}, data says {want}")

    # eval count
    expect("README.md", r"regression_evals-(\d+)", n_evals, "eval badge")
    expect("README.md", r"(\d+) deterministic regression prompts", n_evals, "eval count (features)")
    expect("README.md", r"\*\*(\d+) prompts\*\*", n_evals, "eval count (validation)")
    expect("README.tr.md", r"regresyon_eval-(\d+)", n_evals, "eval badge")
    expect("README.tr.md", r"(\d+) deterministik regresyon", n_evals, "eval count (features)")
    expect("README.tr.md", r"\*\*(\d+) prompt\*\*", n_evals, "eval count (validation)")
    expect("docs/assets/hero.svg", r"(\d+) regression evals", n_evals, "hero chip")
    expect("docs/social-preview.html", r"(\d+) regression evals", n_evals, "social preview")

    # pool size
    expect("README.md", r"\*\*(\d+) rated models\*\*", n_models, "pool size")
    expect("README.tr.md", r"puanlanan (\d+) model", n_models, "pool size")
    expect("docs/assets/hero.svg", r"(\d+) rated models", n_models, "hero chip")

    # policy iteration
    expect("README.md", r"policy-iteration--(\d+)", it, "policy badge")
    expect("README.tr.md", r"politika-iteration--(\d+)", it, "policy badge")
    expect("README.md", r"Where it stands \([^)]*iteration-(\d+)\)", it, "status line")
    expect("README.tr.md", r"Durum \([^)]*iteration-(\d+)\)", it, "status line")
    expect("skill/SKILL.md", r"routing-policy-version: iteration-(\d+)", it, "SKILL.md version")
    first = re.search(r"^## iteration-(\d+)", read("CHANGELOG.md"), re.M)
    if not first:
        errors.append("CHANGELOG.md: no '## iteration-N' heading")
    elif int(first.group(1)) != it:
        errors.append(f"CHANGELOG.md: newest entry is iteration-{first.group(1)}, policy is iteration-{it}")
    else:
        checks += 1

    # tier tables: every pool model sits in the row of its tier
    rows = {
        "README.md": {
            "B": "**Budget**", "F": "**Free**", "N": "**Non-confidential only**",
            "G": "**Non-confidential only**", "P": "**Premium**", "D": "**Dominated**",
        },
        "README.tr.md": {
            "B": "**Bütçe**", "F": "**Ücretsiz**", "N": "**Yalnızca gizli olmayan iş**",
            "G": "**Yalnızca gizli olmayan iş**", "P": "**Premium**", "D": "**Baskın olunan**",
        },
    }
    for rel, labels in rows.items():
        lines = read(rel).splitlines()
        for name, info in models.items():
            label = labels[info["tier"]]
            row = next((ln for ln in lines if ln.startswith("| ") and label in ln.split("|")[1]), None)
            short = name.removesuffix(" Contributor")
            checks += 1
            if row is None:
                errors.append(f"{rel}: no table row labelled {label} for {name}")
            elif short not in row:
                errors.append(f"{rel}: {name} (tier {info['tier']}) is missing from the {label} row")

    if errors:
        print("readme facts FAILED:")
        for e in errors:
            print("  -", e)
        return 1
    print(f"readme facts OK: {checks} figures and tier entries agree with {n_evals} evals, "
          f"{n_models} pool models, iteration-{it}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
