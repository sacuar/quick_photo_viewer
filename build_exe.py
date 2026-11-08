from pathlib import Path
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parent
out = Path.home() / "Documents" / "QuickPhotoViewerBuild"
work = Path(tempfile.gettempdir()) / "QuickPhotoViewerPyInstaller"
out.mkdir(parents=True, exist_ok=True)
work.mkdir(parents=True, exist_ok=True)

cmd = [
    sys.executable, "-m", "PyInstaller",
    "--noconfirm", "--clean", "--windowed", "--onedir",
    "--contents-directory", ".", "--name", "QuickPhotoViewer",
    "--icon", str(root / "icons" / "quick_photo_viewer.ico"),
    "--add-data", f"{root / 'icons'};icons",
    "--specpath", str(work),
    "--workpath", str(work / "build"),
    "--distpath", str(out),
    str(root / "app.py")
]
subprocess.check_call(cmd, cwd=root)
print("EXE:", out / "QuickPhotoViewer" / "QuickPhotoViewer.exe")
