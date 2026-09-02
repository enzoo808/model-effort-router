# Installs the model-secici skill at user scope (~/.claude/skills/model-secici).
# After this it is available as /model-secici in every Claude Code project.

$ErrorActionPreference = 'Stop'

$src  = Join-Path $PSScriptRoot 'skill'
$dest = Join-Path $env:USERPROFILE '.claude\skills\model-secici'

if (-not (Test-Path $src)) {
    throw "Source not found: $src"
}

New-Item -ItemType Directory -Force -Path $dest | Out-Null
Copy-Item -Path (Join-Path $src '*') -Destination $dest -Recurse -Force

Write-Output "Installed -> $dest"
Get-ChildItem $dest | Select-Object -ExpandProperty Name | ForEach-Object { Write-Output "  $_" }
Write-Output ""
Write-Output "Restart Claude Code, then: /model-secici <your prompt>"
