# Security Policy

## What this project is

`model-secici` is a prompt-only routing skill plus small local scripts (`install.sh`, `install.ps1`, `scripts/*.py`). It has no server, no network service and stores no user data.

## Supported versions

Only the latest release and the `main` branch are supported.

## Reporting a vulnerability

Please do **not** open a public issue for a security problem.

Report it privately through GitHub: [Report a vulnerability](https://github.com/enzoo808/model-effort-router/security/advisories/new).

Examples that count: an installer or script that runs unexpected commands or overwrites files outside the skill folder; a skill instruction that could make an agent leak data or run something unsafe.

You can expect a first reply within about 7 days. Fixes land on `main` and are noted in [CHANGELOG.md](CHANGELOG.md).

A wrong model recommendation or an outdated price is not a security issue; open a normal issue (see [CONTRIBUTING.md](CONTRIBUTING.md)).
