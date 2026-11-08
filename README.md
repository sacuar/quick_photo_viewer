<div align="center">
  <img src="icons/quick_photo_viewer.png" alt="Quick Photo Viewer red-orange landscape icon" width="104" height="104">
  <h1>Quick Photo Viewer</h1>
  <p><strong>A clean, fast photo viewer for Windows 10 and 11.</strong></p>
  <p>Browse folders, use thumbnails, zoom, rotate, enter distraction-free viewing and print — without an editing suite getting in the way.</p>
  <p>
    <img alt="Platform Windows 10/11" src="https://img.shields.io/badge/Windows-10%20%7C%2011-1570c7">
    <img alt="Version 2.9" src="https://img.shields.io/badge/version-2.9.0-e45737">
    <img alt="Status pre-release" src="https://img.shields.io/badge/status-pre--release-777777">
    <img alt="Standalone" src="https://img.shields.io/badge/installer-Inno%20Setup-c74432">
  </p>
</div>

---

### Photo viewing without distractions

**Quick Photo Viewer 2.9** keeps the stable original black interface and removes the experimental editing/OCR plugins. It opens local images directly; there is no cloud upload or user account.

| Browsing | Focused view | Windows integration |
|---|---|---|
| Folder navigation and thumbnail previews | Photo-only mode after **5 seconds** | Optional Start Menu and desktop shortcuts |
| Left/right arrow keys, scroll navigation | **Esc** reveals controls | Install to Program Files with Inno Setup |
| Fit-to-window, zoom, rotate and fullscreen | Compact dark toolbar and square icons | Optional **Open with** registration |
| Image information, print, save a copy | Slideshow and frame/display options | User-approved selection in Windows Default Apps |

### Screen captures

Real Windows 11 screenshots will be added after the installer and UI pass the manual smoke test. **No mock screenshots are presented as tested application captures.**

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

**Windows installer:** A signed, verified release is **not published yet**. Once Windows testing passes, the installer will appear on [Releases](https://github.com/sacuar/quick_photo_viewer/releases).

**Source on Windows:**

```powershell
py -3 -m pip install -r requirements.txt
py app.py
```

**Build the standalone EXE + installer:** Install [Inno Setup 6](https://jrsoftware.org/isdl.php) on the **build machine**, then run `build_installer.bat`. This builds a bundled Python/Qt app and generates `installer/output/QuickPhotoViewer-Setup-2.9.0.exe`. Users of that Setup EXE do **not** need Python.

[Windows installation, upgrades and default-app registration](WINDOWS_INSTALL.md)

### Free viewer and future editors

The main viewer has **no editing or OCR plugins**, and does not import external editing code at startup. Future editors may be distributed separately, after they have been tested. The 2.9 viewer is the reference implementation; experimental 3.0–3.2 packages are not the baseline.

### Updates and privacy

The **Check GitHub for updates** option compares published release versions; checking on startup is opt-in. Nothing is downloaded or installed automatically. Your photos remain local.

### Feedback

Report bugs under [Issues](https://github.com/sacuar/quick_photo_viewer/issues). Please include your Windows version, steps to reproduce and any error message; do not upload private photos.

> **Release status:** Source and build scripts can be reviewed, but the Windows build and installer have not been run end-to-end in this environment. GitHub Actions artifacts are unsigned test builds, not approved public releases.

Copyright © 2026 BANG Tools. All rights reserved until a source distribution licence is selected.
