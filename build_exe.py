"""Clean Windows onedir build outside Program Files; no plugins included."""
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
output = Path.home() / "Documents" / "QuickPhotoViewerBuild"
for name in ("spec", "build", "dist"):
    (output / name).mkdir(parents=True, exist_ok=True)

subprocess.check_call([sys.executable, str(root / 'build_brand.py')], cwd=root)
command = [
    sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean",
    "--windowed", "--onedir", "--contents-directory", ".",
    "--name", "QuickPhotoViewer", "--icon", str(root / "icons" / "quick_photo_viewer.ico"),
    "--add-data", f"{root / 'icons'};icons",
    "--specpath", str(output / "spec"),
    "--workpath", str(output / "build"),
    "--distpath", str(output / "dist"),
    str(root / "app.py"),
]
subprocess.check_call(command, cwd=root)
folder = output / "dist" / "QuickPhotoViewer"
if not (folder / "QuickPhotoViewer.exe").is_file():
    raise RuntimeError("The compiled executable is missing.")
if not (folder / f"python{sys.version_info.major}{sys.version_info.minor}.dll").is_file():
    raise RuntimeError("Python runtime DLL missing; installer build is blocked.")
print("Build folder:", folder)
