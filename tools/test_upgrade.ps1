# Run on a GitHub-hosted Windows runner after the current installer is built.
# Exercises the real upgrade from the last browser-only updater (2.9.5) to 2.9.6.
param(
    [Parameter(Mandatory=$true)][string]$CurrentInstaller,
    [string]$FromVersion = '2.9.5',
    [string]$ToVersion = '2.9.6'
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Invoke-Setup([string]$Exe,[string]$InstallDir) {
    $args = @('/VERYSILENT','/SUPPRESSMSGBOXES','/NORESTART','/SP-',("/DIR=`"$InstallDir`""))
    $proc = Start-Process -FilePath $Exe -ArgumentList $args -Wait -PassThru
    if ($proc.ExitCode -ne 0) { throw "Installer failed with exit code $($proc.ExitCode): $Exe" }
}

$latest = (Resolve-Path $CurrentInstaller).Path
$tempDir = Join-Path $env:RUNNER_TEMP 'QPV-UpgradeRegression'
$installDir = Join-Path $tempDir 'application'
New-Item -ItemType Directory -Path $tempDir -Force | Out-Null

$releaseUrl = "https://api.github.com/repos/sacuar/quick_photo_viewer/releases/tags/v$FromVersion"
$headers = @{'Accept'='application/vnd.github+json';'User-Agent'='QPV-UpgradeRegression'}
$release = Invoke-RestMethod -Uri $releaseUrl -Headers $headers
$assetName = "QuickPhotoViewer-Setup-$FromVersion.exe"
$asset = @($release.assets | Where-Object { $_.name -eq $assetName }) | Select-Object -First 1
if (-not $asset) { throw "Previous installer asset missing: $assetName" }
if ($asset.browser_download_url -ne "https://github.com/sacuar/quick_photo_viewer/releases/download/v$FromVersion/$assetName") {
    throw 'Unrecognised previous installer URL.'
}
if ($asset.digest -notmatch '^sha256:([a-fA-F0-9]{64})$') {
    throw 'Previous installer SHA-256 digest is unavailable: refusing to execute it.'
}
$expectedHash = $Matches[1].ToLowerInvariant()
$oldSetup = Join-Path $tempDir $assetName
Invoke-WebRequest -Uri $asset.browser_download_url -OutFile $oldSetup
if ((Get-Item $oldSetup).Length -ne [int64]$asset.size) { throw 'Previous installer size mismatch.' }
$actualHash = (Get-FileHash $oldSetup -Algorithm SHA256).Hash.ToLowerInvariant()
if ($actualHash -ne $expectedHash) { throw 'Previous installer digest mismatch.' }

try {
    Invoke-Setup $oldSetup $installDir
    $registryPath = 'HKLM:\Software\BANGTools\QuickPhotoViewer'
    $before = Get-ItemProperty -Path $registryPath -ErrorAction Stop
    if ($before.Version -ne $FromVersion) { throw "Installed baseline expected $FromVersion, got $($before.Version)" }
    if (!(Test-Path (Join-Path $installDir 'QuickPhotoViewer.exe'))) { throw 'Old installed EXE missing.' }

    Invoke-Setup $latest $installDir
    $after = Get-ItemProperty -Path $registryPath -ErrorAction Stop
    if ($after.Version -ne $ToVersion) { throw "Upgrade version expected $ToVersion, got $($after.Version)" }
    $targetExe = Join-Path $installDir 'QuickPhotoViewer.exe'
    if (!(Test-Path $targetExe)) { throw 'New installed EXE missing.' }
    if ([System.IO.Path]::GetFullPath($after.Executable) -ne [System.IO.Path]::GetFullPath($targetExe)) {
        throw 'Installed executable registration is incorrect.'
    }
    $env:QT_QPA_PLATFORM = 'offscreen'
    $test = Start-Process -FilePath $targetExe -ArgumentList '--smoke-test' -PassThru
    if (-not $test.WaitForExit(30000)) { $test.Kill(); throw 'Upgraded executable startup timeout.' }
    if ($test.ExitCode -ne 0) { throw "Upgraded executable startup failed: $($test.ExitCode)" }

    Write-Host "Verified: $FromVersion -> $ToVersion upgrade and packaged startup succeeded."
    $uninstall = Get-ChildItem $installDir -Filter 'unins*.exe' | Select-Object -First 1
    if (-not $uninstall) { throw 'Uninstaller missing.' }
    $remove = Start-Process $uninstall.FullName -ArgumentList '/VERYSILENT','/SUPPRESSMSGBOXES','/NORESTART' -Wait -PassThru
    if ($remove.ExitCode -ne 0) { throw 'Uninstaller failed.' }
    if (Test-Path $targetExe) { throw 'Executable remained after uninstall.' }
    if (Test-Path $registryPath) { throw 'Registry entry remained after uninstall.' }
    Write-Host 'Verified: upgraded installation uninstalled cleanly.'
} finally {
    Remove-Item -Path $oldSetup -Force -ErrorAction SilentlyContinue
}
