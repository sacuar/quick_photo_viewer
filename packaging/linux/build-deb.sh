#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
# Keep this fixed version aligned with app.py; CI verifies before packaging.
grep -q 'VERSION = "2.9.6"' app.py || { echo 'Application version changed: update packaging version' >&2; exit 1; }
VERSION=2.9.6
PKG="quick-photo-viewer"
STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT
APP="$STAGE/opt/quick-photo-viewer"
mkdir -p "$APP" "$STAGE/DEBIAN" "$STAGE/usr/share/applications" "$STAGE/usr/share/icons/hicolor/256x256/apps" installer/linux
cp -a dist/QuickPhotoViewer/. "$APP/"
cp icons/quick_photo_viewer.png "$STAGE/usr/share/icons/hicolor/256x256/apps/quick-photo-viewer.png"
cat > "$STAGE/usr/share/applications/quick-photo-viewer.desktop" <<'EOF'
[Desktop Entry]
Type=Application
Name=Quick Photo Viewer
Comment=View local images and photo folders
Exec=/opt/quick-photo-viewer/QuickPhotoViewer %f
Icon=quick-photo-viewer
Terminal=false
Categories=Graphics;Viewer;
MimeType=image/jpeg;image/png;image/gif;image/webp;image/bmp;image/tiff;image/svg+xml;
StartupNotify=true
EOF
cat > "$STAGE/DEBIAN/control" <<EOF
Package: $PKG
Version: $VERSION
Section: graphics
Priority: optional
Architecture: amd64
Maintainer: SACUAR Tools <noreply@github.com>
Depends: libgl1, libegl1, libxkbcommon0, libxcb-cursor0, libdbus-1-3
Description: Local, distraction-free photo viewer for Ubuntu
 Native Qt/PySide6 app for local image browsing and keyboard navigation.
EOF
chmod 755 "$STAGE/DEBIAN"
OUTPUT="installer/linux/QuickPhotoViewer-${VERSION}-ubuntu24.04-amd64.deb"
dpkg-deb --build --root-owner-group "$STAGE" "$OUTPUT"
sha256sum "$OUTPUT" > "$OUTPUT.sha256"
dpkg-deb --info "$OUTPUT"
