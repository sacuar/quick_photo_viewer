# Quick Photo Viewer on Ubuntu 24.04 (x86-64)

The Ubuntu branch builds a PySide6 app packaged as a .deb. Windows installers and the Windows update mechanism are unchanged.

## Install a tested GitHub Actions artifact
Download `QuickPhotoViewer-Ubuntu-24.04-amd64` from the Ubuntu Actions build, unzip, inspect `*.sha256` and verify the package before installing:

```bash
sha256sum -c QuickPhotoViewer-2.9.6-ubuntu24.04-amd64.deb.sha256
sudo apt install ./QuickPhotoViewer-2.9.6-ubuntu24.04-amd64.deb
```

Open **Quick Photo Viewer** from the Applications menu, or use `/opt/quick-photo-viewer/QuickPhotoViewer /path/to/image.jpg`.

A Linux update opens the official releases page; it does not attempt to run a Windows installer. The delete action uses the user's desktop Trash through `send2trash`. No file association is made the default without the user's choice.

## Source checkout

```bash
sudo apt install python3-venv libgl1 libegl1 libxcb-cursor0 libxkbcommon-x11-0
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python app.py
```

Ubuntu 24.04 x64 is the CI target. Other Ubuntu releases, Wayland desktop integrations, file type handlers and default applications may differ. A green headless smoke test does not establish every GUI control or desktop integration is correct. The distribution uses the repository's current source and does not grant additional licence rights.
