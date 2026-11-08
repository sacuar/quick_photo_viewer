"""Non-invasive, user-controlled GitHub release checks.

Never downloads or executes installation files. In particular, it cannot
replace the owner's private edition with the public Free edition.
"""
import json
import re
import urllib.error
import urllib.request

from PySide6.QtCore import QThread, Signal

RELEASE_API = "https://api.github.com/repos/sacuar/quick_photo_viewer/releases/latest"


def version_numbers(tag):
    match = re.search(r"(?:^|[^0-9])(\d+)\.(\d+)\.(\d+)", tag)
    return tuple(int(x) for x in match.groups()) if match else None


class UpdateChecker(QThread):
    # status, message, link
    checked = Signal(str, str, str)

    def __init__(self, current_version, parent=None):
        super().__init__(parent)
        self.current_version = current_version

    def run(self):
        request = urllib.request.Request(
            RELEASE_API,
            headers={"Accept": "application/vnd.github+json",
                     "User-Agent": "QuickPhotoViewer-UpdateCheck"},
        )
        try:
            with urllib.request.urlopen(request, timeout=5) as response:
                release = json.load(response)
            tag = release.get("tag_name", "")
            url = release.get("html_url", "")
            latest = version_numbers(tag)
            installed = version_numbers(self.current_version)
            if not latest or not url.startswith("https://github.com/sacuar/quick_photo_viewer/releases/"):
                self.checked.emit("none", "No comparable GitHub release was found.", "")
            elif installed is not None and latest > installed:
                self.checked.emit(
                    "update",
                    f"GitHub release {tag} is newer than {self.current_version}.\n"
                    "Note: the public Free release may differ from your private Pro edition.",
                    url,
                )
            else:
                self.checked.emit("current", f"No newer GitHub release than {self.current_version}.", "")
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                self.checked.emit("none", "No published GitHub releases are available yet.", "")
            else:
                self.checked.emit("error", f"GitHub returned HTTP {exc.code}.", "")
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            self.checked.emit("error", f"Could not check GitHub: {exc}", "")
