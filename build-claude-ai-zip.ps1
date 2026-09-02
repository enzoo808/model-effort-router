# Packages the model-secici skill into a zip you can upload to claude.ai.
# Uses the same skill/SKILL.md + skill/reference.md as Claude Code -- not a
# hand-synced second copy.

$ErrorActionPreference = 'Stop'

$src       = Join-Path $PSScriptRoot 'skill'
$staging   = Join-Path $env:TEMP 'model-secici-package-staging'
$pkgName   = 'model-secici'
$distDir   = Join-Path $PSScriptRoot 'dist'
$zipPath   = Join-Path $distDir "$pkgName.zip"

if (-not (Test-Path $src)) {
    throw "Source not found: $src"
}

if (Test-Path $staging) { Remove-Item -Recurse -Force $staging }
$stageDir = Join-Path $staging $pkgName
New-Item -ItemType Directory -Force -Path $stageDir | Out-Null
Copy-Item -Path (Join-Path $src 'SKILL.md') -Destination $stageDir
Copy-Item -Path (Join-Path $src 'reference.md') -Destination $stageDir

New-Item -ItemType Directory -Force -Path $distDir | Out-Null
if (Test-Path $zipPath) { Remove-Item $zipPath }

# Both Compress-Archive and ZipFile.CreateFromDirectory produce backslash (\)
# separators in zip entry names on Windows. The zip spec requires forward
# slashes (/), and claude.ai rejects backslashes as "invalid characters".
# We build the entries by hand with explicit forward-slash names.
Add-Type -AssemblyName System.IO.Compression.FileSystem
Add-Type -AssemblyName System.IO.Compression
$zip = [System.IO.Compression.ZipFile]::Open($zipPath, [System.IO.Compression.ZipArchiveMode]::Create)
try {
    Get-ChildItem -Path $stageDir -File | ForEach-Object {
        $entryName = "$pkgName/$($_.Name)"
        $entry = $zip.CreateEntry($entryName, [System.IO.Compression.CompressionLevel]::Optimal)
        $entryStream = $entry.Open()
        try {
            $bytes = [System.IO.File]::ReadAllBytes($_.FullName)
            $entryStream.Write($bytes, 0, $bytes.Length)
        } finally {
            $entryStream.Dispose()
        }
    }
} finally {
    $zip.Dispose()
}

Remove-Item -Recurse -Force $staging

Write-Output "Packaged -> $zipPath"
Write-Output ""
Write-Output "To upload: claude.ai > Settings > Features > Custom Skills > Upload"
Write-Output "(requires Pro/Max/Team/Enterprise + code execution enabled)"
