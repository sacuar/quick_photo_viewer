# Changes from stable 2.8.1

- Only these view methods changed: `__init__`, `build_menus`, `build_toolbar`, `toggle_immersive`, `_apply_normal_visibility`, `eventFilter`, `begin_thumbnails`, `load_thumbnail_batch`, `load_current`, `resizeEvent`, `toggle_fullscreen`, `toggle_photo_only`, `closeEvent`, `keyPressEvent`.
- Added isolated update-check logic and a small preferences dialog; the rest of the viewer functions remain intact.
- Replaced duplicate hidden-menu shortcuts with application event routing for Left / Right / Esc / F9 / F10 / F11 and visibility shortcuts.
- Photo-only begins automatically after five seconds of no mouse/keyboard activity while a photo is open.
- Fixed duplicate Ctrl+L conflict: Rotate Left stays Ctrl+L; Thumbnails Left is Ctrl+Alt+L.
- Reduced toolbar and side navigation sizing; retained black theme and original landscape icon.
- Thumbnail decoding is spread over shorter batches to reduce blocking of the photo viewer.
- No editing or OCR plugin code is loaded or bundled. External tools are a separate template, not part of this viewer.
- Windows installer script registers the application without overriding Windows default-file associations. Setup reuses earlier installer AppId for upgrades and includes targeted removal of old per-user QuickPhotoViewer.Image registry entries when enabled.
- GitHub release checks are opt-in and manual-install only. No update runs automatically or silently.

## Unchanged

Navigation methods, image decoder, supported formats, thumbnail rendering delegate, undo/redo, frame color, picture save, recycle/delete and info dialogs, and the core photo rendering method remain unchanged.
