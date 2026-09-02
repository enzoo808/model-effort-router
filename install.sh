#!/usr/bin/env bash
# Installs the model-secici skill at user scope (~/.claude/skills/model-secici).
# After this it is available as /model-secici in every Claude Code project.
set -euo pipefail

src="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/skill"
dest="$HOME/.claude/skills/model-secici"

[ -d "$src" ] || { echo "Source not found: $src" >&2; exit 1; }

mkdir -p "$dest"
cp -R "$src/." "$dest/"

echo "Installed -> $dest"
ls -1 "$dest" | sed 's/^/  /'
echo
echo "Restart Claude Code, then: /model-secici <your task>"
