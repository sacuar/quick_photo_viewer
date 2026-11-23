<div align="center">

![Quick Photo Viewer banner](assets/brand-cover.svg)

# Quick Photo Viewer

**A focused Windows photo viewer for browsing local images without distractions.**

[![Windows](https://img.shields.io/badge/platform-Windows%2010%2F11-2563eb)](https://github.com/sacuar/quick_photo_viewer#install--try) [![Latest release](https://img.shields.io/github/v/release/sacuar/quick_photo_viewer?label=latest%20release)](https://github.com/sacuar/quick_photo_viewer/releases/latest) [![Issues](https://img.shields.io/github/issues/sacuar/quick_photo_viewer)](https://github.com/sacuar/quick_photo_viewer/issues)

**[DOWNLOAD / RELEASES](https://github.com/sacuar/quick_photo_viewer/releases)** · **[VIEW SOURCE](https://github.com/sacuar/quick_photo_viewer)** · [More SACUAR apps](https://github.com/sacuar)

</div>

<div align="center">

[![GitHub stars](https://img.shields.io/github/stars/sacuar/quick_photo_viewer?style=flat&label=Stars)](https://github.com/sacuar/quick_photo_viewer/stargazers) [![Windows installer downloads](https://img.shields.io/github/downloads/sacuar/quick_photo_viewer/v2.9.6/QuickPhotoViewer-Setup-2.9.6.exe?style=flat&label=Windows%20downloads)](https://github.com/sacuar/quick_photo_viewer/releases/tag/v2.9.6) [![Ubuntu package downloads](https://img.shields.io/github/downloads/sacuar/quick_photo_viewer/v2.9.6/QuickPhotoViewer-2.9.6-ubuntu24.04-amd64.deb?style=flat&label=Ubuntu%20downloads)](https://github.com/sacuar/quick_photo_viewer/releases/tag/v2.9.6)

[View visitors and referral sources](https://github.com/sacuar/quick_photo_viewer/graphs/traffic) · [All releases](https://github.com/sacuar/quick_photo_viewer/releases)

</div>

## Why use Quick Photo Viewer?

- Navigate photo folders with thumbnails, keyboard shortcuts and mouse controls.
- Zoom, rotate, print, or switch to a distraction-free fullscreen view.
- Photos stay on your computer; no account or cloud upload is required.

## Ubuntu build

**Ubuntu 24.04 x64 (preview):** A native Qt/PySide6 build and installable `.deb` are available through the Ubuntu CI pipeline. Windows updates do not run on Linux. Linux file deletion uses the desktop Trash. [Ubuntu setup and limitations](packaging/linux/README.md) · [Ubuntu workflow](https://github.com/sacuar/quick_photo_viewer/actions/workflows/ubuntu-build.yml).

## Install / try

Open **[GitHub Releases](https://github.com/sacuar/quick_photo_viewer/releases)**, choose the latest suitable Windows asset, review its release notes and known limitations, and follow the installer instructions. If no verified installer is available, use the documented source-build instructions below. Download only from the official project release page.

**Release note:** The 2.9-series documentation includes maintenance updates, but you should verify the installed version and Windows update flow against the latest release before relying on automatic upgrades.

**Licence:** Source is publicly viewable, but no redistributable open-source licence has been selected. Please check the repository's licence status before reusing source.

## Screenshots and first look

### See your photos, not the clutter

![Actual Quick Photo Viewer application showing a local image and photo-browsing controls](https://github.com/sacuar/quick_photo_viewer/releases/download/v2.9.6/workspace.png)

*Real application screen capture with synthetic demo imagery, created during the Windows build. No marketing concept rendering is substituted for the application interface.*

**Open local photos instantly, navigate with the arrow keys, zoom in, and switch to a distraction-free fullscreen or photo-only view.** The Ubuntu build preserves the main viewing workflow.

## Get involved

[Installation guide](WINDOWS_INSTALL.md) · [Contribute](CONTRIBUTING.md) · [Report a bug](https://github.com/sacuar/quick_photo_viewer/issues/new). Please report your Windows version, application version and steps to reproduce. Screenshots of reproducible issues help.

---

## Detailed documentation

### Photo viewing without distractions

**Quick Photo Viewer 2.9.6** keeps the stable original black interface and removes the experimental editing/OCR plugins. It opens local images directly; there is no cloud upload or user account.

| Browsing | Focused view | Windows integration |
|---|---|---|
| Folder navigation and thumbnail previews | Photo-only mode after **5 seconds** | Optional Start Menu and desktop shortcuts |
| Left/right arrow keys, scroll navigation | **Esc** reveals controls | Install to Program Files with Inno Setup |
| Fit-to-window, zoom, rotate and fullscreen | Compact dark toolbar and square icons | Optional **Open with** registration |
| Image information, print, save a copy | Slideshow and frame/display options | User-approved selection in Windows Default Apps |

### Screen captures

![Application workspace](https://github.com/sacuar/quick_photo_viewer/releases/latest/download/workspace.png)

Actual application capture with synthetic demo images, generated during the Windows build.

### Keyboard shortcuts

| Action | Key |
|---|---|
| Previous / next photo | ← / → |
| Show controls in Photo-only | Esc |
| Toggle Photo-only | F10 |
| Clean fullscreen | F9 / F11 |
| Zoom with mouse wheel | Ctrl + wheel |
| Open image | Ctrl + O |
| Rotate left / right | Ctrl + L / Ctrl + R |

### Install or build

**Windows installer:** Unsigned preview installers appear on [Releases](https://github.com/sacuar/quick_photo_viewer/releases).

**Source on Windows:**

```powershell
py -3 -m pip install -r requirements.txt
py app.py
```

**Build the standalone EXE + installer:** Install [Inno Setup 6](https://jrsoftware.org/isdl.php) on the **build machine**, then run `build_installer.bat`. This builds a bundled Python/Qt app and generates `installer/output/QuickPhotoViewer-Setup-2.9.6.exe`. Users of that Setup EXE do **not** need Python.

[Windows installation, upgrades and default-app registration](WINDOWS_INSTALL.md)

### Free viewer and future editors

The main viewer has **no editing or OCR plugins**, and does not import external editing code at startup. Future editors may be distributed separately, after they have been tested. The 2.9 viewer is the reference implementation; experimental 3.0–3.2 packages are not the baseline.

### Updates and privacy

**Check GitHub for updates** downloads the matching published Windows installer after your approval and verifies its size and GitHub SHA-256 digest before launching Setup with Windows elevation. New installations check at startup by default; disable this in Settings. Existing preferences are respected. Portable or unregistered copies use the official releases page. Your photos remain local.

### Contribute to Quick Photo Viewer

**Developers, testers and UI designers are welcome.** Useful contributions include reproducible Windows bug reports, faster image loading, keyboard accessibility, installation testing, and genuine screenshots after manual verification.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. Keep changes isolated and preserve the stable 2.9 photo-viewing workflow. Editing and OCR experiments should remain separate from the viewer.

### Feedback

Report bugs under [Issues](https://github.com/sacuar/quick_photo_viewer/issues). Please include your Windows version, steps to reproduce and any error message; do not upload private photos.

> **Release status:** Source and build scripts can be reviewed, but the Windows build and installer have not been run end-to-end in this environment. GitHub Actions artifacts are unsigned test builds, not approved public releases.

Copyright © 2026 BANG Tools. All rights reserved until a source distribution licence is selected.

### Installation reliability (2.9.5 and 2.9.6)
Setup only installs and registers files; it no longer launches the viewer, maintenance tool or Windows Settings. After Setup closes, open Quick Photo Viewer or QuickPhotoViewer maintenance from Start. Choose file defaults through Windows Settings manually. The release workflow tests installed JPEG opening and uninstall cleanup.

### Current release and updater verification

The published Windows release is **2.9.6**. It has a consent-based SHA-256-verified installer download for registered Windows installations. The previous 2.9.5 build only opened the official release page: install 2.9.6 once manually to acquire the new update mechanism. [Release 2.9.6](https://github.com/sacuar/quick_photo_viewer/releases/tag/v2.9.6). CI now includes a regression workflow for an actual 2.9.5 → 2.9.6 Windows installer upgrade; check [Actions](https://github.com/sacuar/quick_photo_viewer/actions/workflows/windows-build.yml) for its result before relying on it as verified.
