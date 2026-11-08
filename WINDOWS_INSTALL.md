# Windows installation & upgrade (Quick Photo Viewer 2.9)

**Stable viewer:** `app.py` is unchanged from the focused 2.9 baseline. No editing plugins are included.

## Build

1. Unzip to Documents (do not build inside Program Files).
2. Install Python 3.11–3.14 and [Inno Setup 6](https://jrsoftware.org/isdl.php) on the **build PC only**.
3. Run `build_installer.bat`. The batch file installs PySide6 and PyInstaller as needed, builds a complete `--onedir` Windows bundle, checks for `python3*.dll`, and compiles `installer/output/QuickPhotoViewer-Setup-2.9.0.exe`.
4. Copy the resulting **Setup EXE** to the target Windows 10/11 (x64) computer. That computer does not need Python.

## Installer behaviour

- Installs the entire application into Program Files with Start Menu, uninstall entry and optional desktop shortcut.
- Uses **the same Inno Setup AppId** as the earlier 3.1/3.2 installers, so a detected Inno-installed version can be updated in place.
- Does not remove arbitrary older portable folders; those can contain user data.
- Optional **Open with / Default Apps registration**; optional post-install link to Windows Default Apps.
- **Never overwrites `UserChoice` or silently changes defaults.** Windows controls the final selection.
- On uninstall, removes only its app-specific machine registration; never resets other applications' file associations. Legacy per-user registrations are left unchanged to avoid breaking existing defaults.

## When older versions remain

If another version was copied into `C:\Program Files` manually rather than installed through Inno Setup, that folder is not automatically removed. First check your old files for private content, then uninstall any conflicting old version through Windows Installed Apps. Do not run the former registration BAT.

## Verify before sharing

1. Confirm installer builds without warnings and EXE launches on a clean Windows 11 PC.
2. Open a JPG, PNG and WebP via **Open with**.
3. Select Default Apps manually if desired; verify no other photo app was displaced without permission.
4. Confirm arrows, 5-second photo-only, Esc, thumbnails, Ctrl+wheel zoom, and fullscreen.
5. Install the same version again and check that the previous install is detected.
6. Uninstall and check that shortcuts and registration disappear, but personal files and Windows image defaults are preserved.

**Release safety:** These build scripts are prepared but an actual Windows installer has not been compiled or tested here. Do not publish a GitHub Release until the Windows verification is done.
