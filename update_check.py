"""Verified, user-approved updates for the public installed Windows viewer."""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path
from PySide6.QtCore import QThread, Signal

RELEASES="https://github.com/sacuar/quick_photo_viewer/releases"
RELEASE_API="https://api.github.com/repos/sacuar/quick_photo_viewer/releases/latest"
MAX_BYTES=1024*1024*1024

def version_numbers(tag):
    m=re.fullmatch(r"v?(\d+)\.(\d+)\.(\d+)",str(tag))
    return tuple(map(int,m.groups())) if m else None

def request(url):
    return urllib.request.urlopen(urllib.request.Request(url,headers={
        "User-Agent":"QuickPhotoViewer-Updater",
        "Accept":"application/vnd.github+json" if url==RELEASE_API else "application/octet-stream"
    }),timeout=20)

def parse_release(release,current):
    if release.get("draft") or release.get("prerelease"):return None
    tag=release.get("tag_name","")
    latest,installed=version_numbers(tag),version_numbers(current)
    if not latest or not installed:raise ValueError("Unrecognised release or installed version.")
    if latest<=installed:return None
    version=tag.removeprefix("v")
    name=f"QuickPhotoViewer-Setup-{version}.exe"
    url=f"{RELEASES}/download/{tag}/{name}"
    asset=next((x for x in release.get("assets",[]) if x.get("name")==name),None)
    if not asset or asset.get("browser_download_url")!=url:raise ValueError("The release has no matching Windows installer.")
    digest=asset.get("digest") or ""
    if not re.fullmatch(r"sha256:[0-9a-fA-F]{64}",digest):raise ValueError("GitHub has not provided an installer SHA-256 digest.")
    size=asset.get("size")
    if type(size) is not int or not 0<size<=MAX_BYTES:raise ValueError("Invalid installer size.")
    return {"version":version,"url":url,"digest":digest[7:].lower(),"size":size,"name":name}

def release_info(current):
    with request(RELEASE_API) as response:
        body=response.read(2_000_001)
    if len(body)>2_000_000:raise ValueError("GitHub response exceeds size limit.")
    return parse_release(json.loads(body),current)

def installed_directory(current):
    """Never auto-replace portable, source, private or unregistered builds."""
    if sys.platform!="win32" or not getattr(sys,"frozen",False):return None
    import winreg
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,r"Software\BANGTools\QuickPhotoViewer",0,winreg.KEY_READ|winreg.KEY_WOW64_64KEY) as key:
            exe=Path(winreg.QueryValueEx(key,"Executable")[0]).resolve()
            version=winreg.QueryValueEx(key,"Version")[0]
        if exe==Path(sys.executable).resolve() and exe.name.lower()=="quickphotoviewer.exe" and version==current:
            return exe.parent
    except (OSError,ValueError):pass
    return None

def download_installer(info,progress=lambda percent:None,cancel=lambda:False):
    directory=Path(tempfile.mkdtemp(prefix="QPVUpdate-"))
    destination=directory/info["name"]
    h=hashlib.sha256(); count=0
    try:
        with request(info["url"]) as response,destination.open("xb") as out:
            while True:
                if cancel():raise InterruptedError("Download cancelled.")
                chunk=response.read(256*1024)
                if not chunk:break
                count+=len(chunk)
                if count>info["size"]:raise ValueError("Installer is larger than expected.")
                h.update(chunk);out.write(chunk);progress(count*100//info["size"])
        if count!=info["size"] or h.hexdigest()!=info["digest"]:
            raise ValueError("Installer failed SHA-256 verification.")
        if cancel():raise InterruptedError("Download cancelled.")
        return destination
    except Exception:
        shutil.rmtree(directory,ignore_errors=True)
        raise

def launch_installer(path,directory):
    """Ask Windows for elevation rather than trying CreateProcess on an admin installer."""
    import ctypes
    from ctypes import wintypes
    fn=ctypes.windll.shell32.ShellExecuteW
    fn.argtypes=[wintypes.HWND,wintypes.LPCWSTR,wintypes.LPCWSTR,wintypes.LPCWSTR,wintypes.LPCWSTR,ctypes.c_int]
    fn.restype=ctypes.c_void_p
    params=subprocess.list2cmdline(["/DIR="+str(directory),"/NORESTART"])
    result=fn(None,"runas",str(path),params,str(path.parent),1)
    if result is None or result<=32:raise RuntimeError("Windows did not start Setup (elevation cancelled or launch failed).")

class UpdateChecker(QThread):
    def __init__(self,current,parent=None):
        super().__init__(parent);self.current=current;self.info=None;self.error=""
    def run(self):
        try:self.info=release_info(self.current)
        except Exception as exc:self.error=str(exc)

class InstallerDownload(QThread):
    progress=Signal(int)
    def __init__(self,info,parent=None):
        super().__init__(parent);self.info=info;self.path=None;self.error=""
    def run(self):
        try:self.path=download_installer(self.info,self.progress.emit,self.isInterruptionRequested)
        except Exception as exc:self.error=str(exc)
