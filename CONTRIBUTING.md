# Contributing to Quick Photo Viewer

Thanks for helping improve Quick Photo Viewer. The project targets Windows 10/11 and uses PySide6/Python.

## Priorities

- Stability: opening large images, folder scanning, navigation and safe save/print.
- Performance: reduce first-load latency and UI stalls.
- Accessibility: menus, keyboard focus, zoom/pan, high-DPI behaviour.
- Packaging: test the Windows EXE and Inno Setup installer in a clean Windows environment.
- Documentation: provide **real** Windows app screenshots, not fabricated mock-ups.

## Before sending code

1. Check [Issues](https://github.com/sacuar/quick_photo_viewer/issues) and discuss larger changes first.
2. Use a small branch and avoid changing working photo-navigation behaviour unnecessarily.
3. Run `python -m unittest discover -s tests -v` where applicable, and manually test on Windows.
4. Describe test environment, reproduction steps, any known limitations, and changes to UI.
5. Don't bundle private photographs, passwords, account information, unlicensed images, or build outputs.
6. Respect the project's current licence status. The README says that source redistribution terms still need to be selected; do not assume any open-source licence has been granted.

The 2.9 viewer is the reference version. Please keep experimental editing/OCR features separate and get a maintainer review before integrating them.
