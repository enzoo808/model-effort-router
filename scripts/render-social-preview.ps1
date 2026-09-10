# Renders docs/social-preview.html to docs/social-preview.png at 1280x640.
#
# The HTML and the PNG must stay in the same commit: a stale PNG is a wrong
# screenshot of the product on every GitHub link preview, and nobody notices
# because nobody opens the HTML. This makes regenerating it a one-liner instead
# of a manual screenshot.
#
#   .\scripts\render-social-preview.ps1
#
# Uses whichever Chromium-based browser is installed (Edge ships with Windows).

$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$html = Join-Path $root 'docs\social-preview.html'
$png  = Join-Path $root 'docs\social-preview.png'

if (-not (Test-Path $html)) { throw "Source not found: $html" }

$candidates = @(
    "$env:ProgramFiles(x86)\Microsoft\Edge\Application\msedge.exe",
    "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe",
    "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe",
    "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
    "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe"
)
$browser = $candidates | Where-Object { $_ -and (Test-Path $_) } | Select-Object -First 1
if (-not $browser) {
    throw "No Chromium-based browser found. Install Microsoft Edge or Google Chrome, or render docs/social-preview.html by hand at exactly 1280x640."
}

# Render to an ABSOLUTE path in a scratch directory, then copy in.
#
# Two traps, both hit while writing this: Chromium resolves a relative
# --screenshot against its CWD and can fail to write there silently (file lock,
# sync client, sandbox), leaving the STALE png in place and reporting success.
# An absolute path plus an explicit existence check after the run fixes both.
$tmp = Join-Path ([System.IO.Path]::GetTempPath()) ("social-preview-" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Force -Path $tmp | Out-Null
$rendered = Join-Path $tmp 'social-preview.png'

# Chromium reports "N bytes written" on stderr even on success, and Windows
# PowerShell 5.1 turns any native stderr line into a terminating NativeCommandError
# under $ErrorActionPreference='Stop'. Relax it just for this call and judge the
# result by whether the file exists, which is the only thing that actually matters.
$prev = $ErrorActionPreference
$ErrorActionPreference = 'Continue'
try {
    & $browser --headless=new --disable-gpu --hide-scrollbars `
        --window-size=1280,640 `
        --screenshot="$rendered" `
        ("file:///" + ($html -replace '\\', '/')) | Out-String | Write-Verbose
} finally {
    $ErrorActionPreference = $prev
}

if (-not (Test-Path $rendered)) {
    Remove-Item -Recurse -Force $tmp -ErrorAction SilentlyContinue
    throw "The browser produced no screenshot. docs/social-preview.png is unchanged and is now STALE relative to the HTML. Render it by hand at exactly 1280x640, or re-run with a writable TEMP."
}

$before = if (Test-Path $png) { (Get-Item $png).Length } else { 0 }
Copy-Item -Path $rendered -Destination $png -Force
Remove-Item -Recurse -Force $tmp -ErrorAction SilentlyContinue
$after = (Get-Item $png).Length

if ($after -eq $before) {
    Write-Warning "docs/social-preview.png is byte-identical to the previous version. Correct only if the HTML did not change."
}

Write-Output "Rendered -> $png ($before -> $after bytes)"
Write-Output "Browser  -> $browser"
Write-Output ""
Write-Output "Commit docs/social-preview.html and docs/social-preview.png together."
