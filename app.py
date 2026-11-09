import os, subprocess, sys
from pathlib import Path
from functools import lru_cache
from PySide6.QtCore import (Qt, QTimer, QSize, QSettings, QRect, QPoint, QEvent,
                            QPropertyAnimation, QEasingCurve)
from PySide6.QtGui import (QAction, QActionGroup, QColor, QIcon, QImage, QImageReader,
                           QKeySequence, QPixmap, QTransform, QPainter, QPainterPath, QShortcut)
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import (QApplication, QColorDialog, QCheckBox, QDialog, QDialogButtonBox, QDockWidget, QFileDialog,
    QGraphicsOpacityEffect, QLabel, QListWidget, QListWidgetItem, QHBoxLayout, QFormLayout, QVBoxLayout, QSpinBox, QMainWindow,
    QMenu, QMessageBox, QScrollArea, QStatusBar, QStyle, QStyledItemDelegate, QToolBar,
    QToolButton, QWidget, QSizePolicy)

APP_NAME = "Quick Photo Viewer Pro"; VERSION = "2.9.0"
APP_DIR = Path(__file__).resolve().parent
ICON_DIR = APP_DIR / "icons"
SUPPORTED = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp",
             ".tif", ".tiff", ".ico", ".svg", ".psd"}
SVG_RENDER_MIN = 1024
MAX_THUMB = QSize(130, 90)
UNDO_LIMIT = 20
ICON_COLOR = "#e3e3e3"

STYLE = """
* { font-family: "Segoe UI", "Inter", "Helvetica Neue", Arial, sans-serif; }
QMainWindow { background: #14171a; } QWidget { color: #e6e8eb; }
QMenuBar { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #252a30,stop:1 #171a1e); color: #d8e0e7; padding: 2px 5px; border-bottom: 1px solid #303841; }
QMenuBar::item { background: transparent; padding: 5px 10px; margin: 0 1px; border-radius: 3px; }
QMenuBar::item:selected { background: #262b31; color: #ffffff; }
QMenu { background: #1e2227; color: #e6e8eb; border: 1px solid #36404a; border-radius: 3px; padding: 4px; }
QMenu::item { padding: 6px 28px 6px 34px; border-radius: 4px; }
QMenu::item:selected { background: #3d8bfd; color: #ffffff; }
QMenu::item:disabled { color: #6c757d; }
QMenu::icon { left: 10px; }
QMenu::separator { height: 1px; background: #2c323a; margin: 4px 8px; }
QToolBar { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #262c33,stop:0.55 #20252b,stop:1 #171b20); border: 0; border-bottom: 1px solid #323a43; padding: 3px 6px; spacing: 2px; }
QToolBar::separator { background: #2c323a; width: 1px; margin: 4px 6px; }
QToolButton { color: #adb5bd; background: transparent; border: 1px solid transparent; border-radius: 3px; padding: 4px; }
QToolButton:hover { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #424b56,stop:1 #2a3038); border-color: #48525c; color: #ffffff; }
QToolButton:pressed { background: #313842; color: #ffffff; }
QToolButton:checked { background: #3d8bfd; color: #ffffff; border-color: #3d8bfd; }
QToolButton#sideNav { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #303741,stop:1 #1d242b); border: 1px solid #39434d; border-radius: 5px; min-width: 32px; min-height: 48px; margin: 4px; color: #cbd2d9; }
QToolButton#sideNav:hover { background: #262b31; border-color: #3d8bfd; color: #ffffff; }
QScrollArea { background: #0f1114; border: 0; }
QLabel#photo { background: #0f1114; color: #6c757d; }
QListWidget { background: #171a1e; border: 0; padding: 6px; outline: 0; }
QDockWidget { color: #adb5bd; }
QDockWidget::title { background: #171a1e; padding: 6px 10px; color: #8b929a; border-top: 1px solid #262b31; }
QStatusBar { background: #1a1d21; color: #8b929a; border-top: 1px solid #262b31; }
QStatusBar::item { border: 0; }
QDialog { background: #1a1d21; color: #e6e8eb; }
QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QFontComboBox { background: #14171a; border: 1px solid #2c323a; border-radius: 5px; padding: 5px 8px; color: #e6e8eb; }
QLineEdit:focus, QSpinBox:focus, QComboBox:focus { border-color: #3d8bfd; }
QPushButton { background: #262b31; color: #e6e8eb; border: 1px solid #2c323a; border-radius: 5px; padding: 6px 14px; }
QPushButton:hover { background: #313842; }
QPushButton:default { background: #3d8bfd; color: #fff; border-color: #3d8bfd; }
QGroupBox { border: 1px solid #2c323a; border-radius: 6px; margin-top: 10px; padding-top: 8px; }
QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; color: #8b929a; }
QSlider::groove:horizontal { height: 4px; background: #2c323a; border-radius: 2px; }
QSlider::handle:horizontal { background: #3d8bfd; width: 14px; margin: -5px 0; border-radius: 7px; }
"""

# ------------------------------------------------------------------ icons
_ICON_CACHE = {}

@lru_cache(maxsize=None)
def make_icon(key):
    svg_path = ICON_DIR / f"{key}.svg"
    if not svg_path.exists():
        svg_path = ICON_DIR / "extension.svg"
        if not svg_path.exists():
            return QIcon()
    renderer = QSvgRenderer(str(svg_path))
    icon = QIcon()
    for s in (16, 22, 32, 48, 64):
        pix = QPixmap(s, s); pix.fill(Qt.GlobalColor.transparent)
        p = QPainter(pix)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        renderer.render(p)
        p.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        p.fillRect(pix.rect(), QColor(ICON_COLOR))
        p.end()
        icon.addPixmap(pix)
    return icon


# ------------------------------------------------------------------ loaders
def load_image(path: Path):
    if path.suffix.lower() == ".svg":
        return _load_svg(path)
    reader = QImageReader(str(path)); reader.setAutoTransform(True)
    img = reader.read()
    return QPixmap.fromImage(img) if not img.isNull() else None


def _load_svg(path: Path):
    renderer = QSvgRenderer(str(path))
    if not renderer.isValid():
        return None
    size = renderer.defaultSize()
    if size.isEmpty() or size.width() <= 0 or size.height() <= 0:
        size = QSize(SVG_RENDER_MIN, SVG_RENDER_MIN)
    if size.width() < SVG_RENDER_MIN and size.height() < SVG_RENDER_MIN:
        f = max(SVG_RENDER_MIN / size.width(), SVG_RENDER_MIN / size.height())
        size = QSize(int(size.width() * f), int(size.height() * f))
    img = QImage(size, QImage.Format.Format_ARGB32)
    img.fill(Qt.GlobalColor.transparent)
    p = QPainter(img); p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    renderer.render(p); p.end()
    return QPixmap.fromImage(img)


# ------------------------------------------------------------------ thumbnails
class ThumbDelegate(QStyledItemDelegate):
    PIX_ROLE = Qt.ItemDataRole.UserRole + 1
    TEXT_H = 16
    def paint(self, painter, option, index):
        painter.save(); painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        rect = option.rect
        selected = bool(option.state & QStyle.StateFlag.State_Selected)
        hovered = bool(option.state & QStyle.StateFlag.State_MouseOver)
        if selected or hovered:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor("#3d8bfd") if selected else QColor("#262b31"))
            painter.drawRoundedRect(rect.adjusted(2, 2, -2, -2), 6, 6)
        pix = index.data(self.PIX_ROLE); text = index.data(Qt.ItemDataRole.DisplayRole) or ""
        fm = painter.fontMetrics(); text_h = self.TEXT_H if text else 0
        if isinstance(pix, QPixmap) and not pix.isNull():
            inner = rect.adjusted(5, 5, -5, -5 - text_h)
            x = inner.left() + (inner.width() - pix.width()) // 2
            y = inner.top() + (inner.height() - pix.height()) // 2
            path = QPainterPath()
            path.addRoundedRect(float(x), float(y), float(pix.width()), float(pix.height()), 5.0, 5.0)
            painter.setClipPath(path); painter.drawPixmap(x, y, pix)
        if text:
            painter.setPen(QColor("#ffffff") if selected else QColor("#cbd2d9"))
            tr = QRect(rect.left()+4, rect.bottom()-self.TEXT_H-3, rect.width()-8, self.TEXT_H)
            painter.drawText(tr, Qt.AlignmentFlag.AlignCenter,
                             fm.elidedText(text, Qt.TextElideMode.ElideMiddle, tr.width()))
        painter.restore()
    def sizeHint(self, option, index):
        s = index.data(Qt.ItemDataRole.SizeHintRole)
        return s if isinstance(s, QSize) else QSize(120, 100)


# ------------------------------------------------------------------ main window
class PhotoViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1280,820); self.setMinimumSize(720,480)
        self.setWindowTitle(f"{APP_NAME} {VERSION}")
        self.setWindowIcon(QIcon(str(ICON_DIR / "quick_photo_viewer.ico")))
        self.setAcceptDrops(True); self.setMouseTracking(True)
        self.files=[]; self.index=-1; self.current_pixmap=None
        self.rotation=0; self.zoom_factor=1.0; self.fit_mode=True; self.photo_only=False
        self.thumb_index=0; self.image_cache={}
        self.undo_stack=[]; self.redo_stack=[]
        self.settings=QSettings("BANG Tools",APP_NAME)
        self.frame_color = self._load_frame_color()

        # ---- view-state flags ----
        self.immersive_mode     = False
        self.thumbnails_visible = True
        self.thumbnails_bottom  = True
        self.file_menu_visible  = True
        self.toolbar_visible    = True

        self.slideshow_timer=QTimer(self); self.slideshow_timer.setInterval(3000)
        self.slideshow_timer.timeout.connect(self.next_image)
        self.thumb_timer=QTimer(self); self.thumb_timer.timeout.connect(self.load_thumbnail_batch)

        # ---- auto photo-only: five seconds after last UI activity ----
        self.idle_seconds = max(2, min(60, int(self.settings.value("photo_idle_seconds", 5))))
        self.auto_photo_only = self.settings.value("auto_photo_only", True, type=bool)
        self.check_updates_on_start = self.settings.value("check_updates_on_start", False, type=bool)
        self.idle_timer = QTimer(self)
        self.idle_timer.setSingleShot(True)
        self.idle_timer.timeout.connect(self._enter_photo_only_if_idle)
        self._before_photo_geometry = None
        self._before_photo_maximized = False
        self._update_worker = None
        QApplication.instance().installEventFilter(self)

        # ---- nav auto-hide (normal mode) ----
        self._nav_opacity=[None,None]; self._nav_anim=[None,None]
        self.nav_hide_timer=QTimer(self); self.nav_hide_timer.setSingleShot(True)
        self.nav_hide_timer.setInterval(2200); self.nav_hide_timer.timeout.connect(self._fade_nav_out)
        self.resize_timer = QTimer(self); self.resize_timer.setSingleShot(True)
        self.resize_timer.setInterval(65); self.resize_timer.timeout.connect(self.refresh_image)

        # ---- photo stage ----
        self.label=QLabel("Drop an image here\n\nor use Open / Folder")
        self.label.setObjectName("photo"); self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size:16px;color:#6c757d;letter-spacing:0.5px")
        self.label.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.label.customContextMenuRequested.connect(self._photo_context_menu)
        self.scroll=QScrollArea(); self.scroll.setWidget(self.label)
        self.scroll.setWidgetResizable(True); self.scroll.setAlignment(Qt.AlignmentFlag.AlignCenter)

        stage=QWidget(); stage_layout=QHBoxLayout(stage)
        stage_layout.setContentsMargins(4,0,4,0); stage_layout.setSpacing(0)
        self.left_button=QToolButton(); self.left_button.setObjectName("sideNav")
        self.left_button.setIcon(make_icon("chevron_left")); self.left_button.setIconSize(QSize(20,20))
        self.left_button.setToolTip("Previous photo — Left arrow")
        self.left_button.clicked.connect(self.prev_image)
        self.right_button=QToolButton(); self.right_button.setObjectName("sideNav")
        self.right_button.setIcon(make_icon("chevron_right")); self.right_button.setIconSize(QSize(20,20))
        self.right_button.setToolTip("Next photo — Right arrow")
        self.right_button.clicked.connect(self.next_image)
        stage_layout.addWidget(self.left_button); stage_layout.addWidget(self.scroll,1)
        stage_layout.addWidget(self.right_button); self.setCentralWidget(stage)

        for i, btn in enumerate((self.left_button, self.right_button)):
            eff=QGraphicsOpacityEffect(btn); btn.setGraphicsEffect(eff); self._nav_opacity[i]=eff
            anim=QPropertyAnimation(eff, b"opacity", self); anim.setDuration(280)
            anim.setEasingCurve(QEasingCurve.Type.InOutQuad); self._nav_anim[i]=anim

        self.setStatusBar(QStatusBar())
        self.build_menus(); self.build_toolbar(); self.build_thumbnails()
        self.restoreGeometry(self.settings.value("geometry",b""))
        self.update_status()
        self.nav_hide_timer.start()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        if self.check_updates_on_start:
            QTimer.singleShot(2500, lambda: self.check_for_updates(silent=True))

    # ================================================== frame color
    def _load_frame_color(self):
        v = self.settings.value("frame_color", None)
        if v in (None, "", "None"): return None
        c = QColor(v) if not isinstance(v, QColor) else v
        return c if c.isValid() else None
    def _save_frame_color(self):
        self.settings.setValue("frame_color",
                               self.frame_color.name() if self.frame_color else "None")
    def _compose_frame(self, pix):
        if self.frame_color is None or pix is None or not pix.hasAlphaChannel():
            return pix
        out = QPixmap(pix.size()); out.fill(self.frame_color)
        p = QPainter(out); p.drawPixmap(0, 0, pix); p.end()
        return out

    # ================================================== helpers
    def action(self,text,shortcut,callback,icon=None,check=False):
        item=QAction(make_icon(icon) if icon else QIcon(), text, self); item.setToolTip(text)
        if shortcut:
            item.setShortcut(QKeySequence(shortcut))
            item.setShortcutContext(Qt.ShortcutContext.ApplicationShortcut)
        item.setCheckable(check); item.triggered.connect(callback); return item

    # ================================================== menus
    def build_menus(self):
        mb=self.menuBar()

        self.file_menu=mb.addMenu("File"); self.file_menu.setIcon(make_icon("folder"))
        self.file_menu.addAction(self.action("Open image…","Ctrl+O",self.open_file,"image"))
        self.file_menu.addAction(self.action("Open folder…","Ctrl+Shift+O",self.open_folder,"folder"))
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.action("Save a copy…","Ctrl+S",self.save_copy,"save"))
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.action("Exit","Ctrl+Q",self.close,"logout"))

        self.edit_menu=mb.addMenu("Edit"); self.edit_menu.setIcon(make_icon("edit"))
        self.undo_action=self.action("Undo","Ctrl+Z",self.undo,"undo")
        self.redo_action=self.action("Redo","Ctrl+Shift+Z",self.redo,"redo")
        self.undo_action.setEnabled(False); self.redo_action.setEnabled(False)
        self.edit_menu.addAction(self.undo_action); self.edit_menu.addAction(self.redo_action)
        self.edit_menu.addSeparator()
        self.reset_action=self.action("Reset to original","Ctrl+Shift+R",
                                      self.reset_to_original,"restart_alt")
        self.edit_menu.addAction(self.reset_action)
        self.edit_menu.addSeparator()

        view=mb.addMenu("View"); view.setIcon(make_icon("image"))
        # Key navigation is managed by eventFilter even while menus are hidden.
        view.addAction(self.action("Previous  (Left)",None,self.prev_image,"chevron_left"))
        view.addAction(self.action("Next  (Right)",None,self.next_image,"chevron_right"))
        view.addSeparator()
        view.addAction(self.action("First photo","Home",self.first_image,"first_page"))
        view.addAction(self.action("Last photo","End",self.last_image,"last_page"))
        view.addSeparator()
        # ---- immersive ----
        self.immersive_action=self.action("Clean fullscreen (F9 or F11)",None,
                                          self.toggle_immersive,"fullscreen",True)
        view.addAction(self.immersive_action)
        view.addSeparator()
        # ---- quick toggles ----
        self.thumb_toggle=self.action("Show thumbnails  (Ctrl+H)",None,
                                      self.toggle_thumbnails,"apps",True)
        self.thumb_toggle.setChecked(True); view.addAction(self.thumb_toggle)

        thumb_pos_menu=view.addMenu(make_icon("first_page"),"Thumbnail position")
        self.thumb_pos_group=QActionGroup(self); self.thumb_pos_group.setExclusive(True)
        self.thumb_at_bottom_action=self.action("Bottom","Ctrl+B",
            lambda: self.set_thumbnails_position(bottom=True),"fit_screen",True)
        self.thumb_at_left_action=self.action("Left","Ctrl+Alt+L",
            lambda: self.set_thumbnails_position(bottom=False),"crop",True)
        self.thumb_at_bottom_action.setChecked(True)
        for a in (self.thumb_at_bottom_action, self.thumb_at_left_action):
            self.thumb_pos_group.addAction(a); thumb_pos_menu.addAction(a)

        self.file_toggle=self.action("Show File menu  (Ctrl+Shift+F)",None,
                                     self.toggle_file_menu,"folder",True)
        self.file_toggle.setChecked(True); view.addAction(self.file_toggle)

        self.toolbar_toggle=self.action("Show toolbar (icons)  (Ctrl+Shift+T)",None,
                                        self.toggle_toolbar,"apps",True)
        self.toolbar_toggle.setChecked(True); view.addAction(self.toolbar_toggle)

        self.menu_toggle=self.action("Show menu bar  (Ctrl+Shift+M)",None,
                                     self.toggle_menu_bar,"visibility_off",True)
        self.menu_toggle.setChecked(True); view.addAction(self.menu_toggle)

        self.photo_only_action=self.action("Photo only (F10) — Esc to reveal controls",None,
                                           self.toggle_photo_only,"crop_free",True)
        view.addAction(self.photo_only_action)
        view.addAction(self.action("Fullscreen (F11)",None,self.toggle_fullscreen,"fullscreen"))

        settings=mb.addMenu("Settings"); settings.setIcon(make_icon("apps"))
        settings.addAction(self.action("Frame color for transparent images…",
                                       None, self.choose_frame_color, "palette"))
        settings.addAction(self.action("Clear frame color",
                                       None, self.clear_frame_color, "crop_free"))
        settings.addSeparator()
        settings.addAction(self.action("Viewer preferences…", None,
                                       self.show_preferences, "apps"))
        settings.addAction(self.action("Check for updates on GitHub…", None,
                                       self.check_for_updates, "refresh"))

        help_menu=mb.addMenu("Help"); help_menu.setIcon(make_icon("help"))
        help_menu.addAction(self.action("About",None,
            lambda: QMessageBox.information(self,"About",
                f"{APP_NAME} {VERSION}\nA fast local photo viewer."),
            "info"))

        # Shortcuts for F9/F10/F11/Esc/Left/Right are handled centrally below.
        # No duplicated QShortcut instances: avoids Qt ambiguous-shortcut failures.

    # ================================================== toggles
    def toggle_menu_bar(self, checked=None):
        visible = self.menuBar().isVisible()
        hidden  = visible if checked is None else (not bool(checked))
        self.menuBar().setVisible(not hidden)
        self.menu_toggle.setChecked(not hidden)
        self.statusBar().showMessage(
            "  Menu bar hidden — press Ctrl+Shift+M to show" if hidden
            else "  Menu bar shown", 3000)

    def toggle_file_menu(self, checked=None):
        self.file_menu_visible = (not self.file_menu_visible) if checked is None else bool(checked)
        self.file_menu.menuAction().setVisible(self.file_menu_visible)
        self.file_toggle.setChecked(self.file_menu_visible)
        self.statusBar().showMessage(
            f"  File menu {'shown' if self.file_menu_visible else 'hidden'} "
            f"(Ctrl+Shift+F to toggle)", 2500)

    def toggle_toolbar(self, checked=None):
        self.toolbar_visible = (not self.toolbar_visible) if checked is None else bool(checked)
        self.main_toolbar.setVisible(self.toolbar_visible and not self.immersive_mode)
        self.toolbar_toggle.setChecked(self.toolbar_visible)
        self.statusBar().showMessage(
            f"  Toolbar {'shown' if self.toolbar_visible else 'hidden'} "
            f"(Ctrl+Shift+T to toggle)", 2500)

    def toggle_thumbnails(self, checked=None):
        self.thumbnails_visible = (not self.thumbnails_visible) if checked is None else bool(checked)
        self.thumbnail_dock.setVisible(self.thumbnails_visible and not self.immersive_mode)
        self.thumb_toggle.setChecked(self.thumbnails_visible)
        self.statusBar().showMessage(
            f"  Thumbnails {'shown' if self.thumbnails_visible else 'hidden'} "
            f"(Ctrl+H to toggle)", 2500)

    def set_thumbnails_position(self, bottom: bool):
        self.thumbnails_bottom = bottom
        self.removeDockWidget(self.thumbnail_dock)
        area = (Qt.DockWidgetArea.BottomDockWidgetArea if bottom
                else Qt.DockWidgetArea.LeftDockWidgetArea)
        self.thumbnail_dock.setAllowedAreas(area)
        self.addDockWidget(area, self.thumbnail_dock)
        if bottom:
            self.thumb_list.setFlow(QListWidget.Flow.LeftToRight)
            self.thumb_list.setWrapping(False)
            self.thumb_list.setMinimumHeight(MAX_THUMB.height() + 40)
            self.thumb_list.setMaximumHeight(16777215)
            self.thumbnail_dock.setMinimumWidth(0)
            self.thumbnail_dock.setMaximumWidth(16777215)
        else:
            self.thumb_list.setFlow(QListWidget.Flow.TopToBottom)
            self.thumb_list.setWrapping(False)
            self.thumb_list.setMinimumHeight(0)
            self.thumb_list.setMaximumHeight(16777215)
            self.thumbnail_dock.setMinimumWidth(MAX_THUMB.width() + 50)
            self.thumbnail_dock.setMaximumWidth(MAX_THUMB.width() + 50)
        self.thumbnail_dock.setVisible(self.thumbnails_visible and not self.immersive_mode)
        self.thumb_at_bottom_action.setChecked(bottom)
        self.thumb_at_left_action.setChecked(not bottom)
        self.statusBar().showMessage(
            f"  Thumbnails moved to {'bottom' if bottom else 'left'}", 2500)

    # ================================================== immersive mode
    def toggle_immersive(self, checked=None):
        enabled = (not self.immersive_mode) if checked is None else bool(checked)
        if enabled and self.photo_only:
            self.toggle_photo_only(False)
        self.immersive_mode = enabled
        self.immersive_action.setChecked(enabled)
        self.idle_timer.stop()
        if enabled:
            if not self.isFullScreen(): self.showFullScreen()
            self._immersive_hide_now()
        else:
            if self.isFullScreen(): self.showNormal()
            self._apply_normal_visibility()
            self._restart_photo_idle()

    def _immersive_hide_now(self):
        if not self.immersive_mode: return
        self.menuBar().setVisible(False)
        self.main_toolbar.setVisible(False)
        self.thumbnail_dock.setVisible(False)
        self.statusBar().setVisible(False)
        self.left_button.setVisible(False)
        self.right_button.setVisible(False)
        for a in self._nav_anim: a.stop()
        self._nav_opacity[0].setOpacity(0.0); self._nav_opacity[1].setOpacity(0.0)

    def _apply_normal_visibility(self):
        self.menuBar().setVisible(True)
        self.file_menu.menuAction().setVisible(self.file_menu_visible)
        self.main_toolbar.setVisible(self.toolbar_visible)
        self.thumbnail_dock.setVisible(self.thumbnails_visible)
        self.statusBar().setVisible(True)
        self.left_button.setVisible(True)
        self.right_button.setVisible(True)
        self._nav_opacity[0].setOpacity(1.0)
        self._nav_opacity[1].setOpacity(1.0)
        self.nav_hide_timer.start()

    def _restart_photo_idle(self):
        if (self.auto_photo_only and self.files and not self.photo_only
                and not self.immersive_mode and not QApplication.activeModalWidget()):
            self.idle_timer.start(self.idle_seconds * 1000)
        else:
            self.idle_timer.stop()

    def _enter_photo_only_if_idle(self):
        if (self.auto_photo_only and self.files and not self.photo_only
                and not self.immersive_mode and self.isActiveWindow()
                and not QApplication.activeModalWidget() and not QApplication.activePopupWidget()):
            self.toggle_photo_only(True)

    def eventFilter(self, obj, event):
        # Capture navigation BEFORE Qt scroll areas or invisible menu actions can
        # consume it.  Only act on events belonging to this viewer's widgets.
        if not isinstance(obj, QWidget) or not (obj is self or self.isAncestorOf(obj)):
            return super().eventFilter(obj, event)
        if QApplication.activeModalWidget():
            return super().eventFilter(obj, event)
        if QApplication.activePopupWidget():
            return super().eventFilter(obj, event)
        kind = event.type()
        if kind == QEvent.Type.KeyPress:
            key = event.key()
            mod = event.modifiers()
            if key == Qt.Key.Key_Escape:
                if self.immersive_mode:
                    self.toggle_immersive(False); return True
                if self.photo_only:
                    self.toggle_photo_only(False); return True
            if mod == Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.ShiftModifier:
                if key == Qt.Key.Key_M:
                    if not self.photo_only and not self.immersive_mode:
                        self.toggle_menu_bar(); return True
                if key == Qt.Key.Key_T:
                    if not self.photo_only and not self.immersive_mode:
                        self.toggle_toolbar(); return True
                if key == Qt.Key.Key_F:
                    if not self.photo_only and not self.immersive_mode:
                        self.toggle_file_menu(); return True
            if mod == Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_H:
                if not self.photo_only and not self.immersive_mode:
                    self.toggle_thumbnails(); return True
            if mod == Qt.KeyboardModifier.NoModifier:
                if key == Qt.Key.Key_Left:
                    self.prev_image(); return True
                if key == Qt.Key.Key_Right:
                    self.next_image(); return True
                if key in (Qt.Key.Key_F9, Qt.Key.Key_F11) and not event.isAutoRepeat():
                    self.toggle_immersive(); return True
                if key == Qt.Key.Key_F10 and not event.isAutoRepeat():
                    self.toggle_photo_only(); return True
        if kind == QEvent.Type.Wheel and (self.photo_only or self.immersive_mode):
            if (obj is self or obj is self.scroll or obj is self.label
                    or self.scroll.isAncestorOf(obj)):
                delta = event.angleDelta().y()
                if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                    if delta: self.zoom_in() if delta > 0 else self.zoom_out()
                elif delta:
                    self.prev_image() if delta > 0 else self.next_image()
                event.accept(); return True
        if kind in (QEvent.Type.MouseMove, QEvent.Type.MouseButtonPress,
                    QEvent.Type.Wheel, QEvent.Type.KeyPress):
            if not self.photo_only and not self.immersive_mode:
                self._restart_photo_idle()
                if kind == QEvent.Type.MouseMove:
                    self._fade_nav_in()
        return super().eventFilter(obj, event)

    # ================================================== frame color actions
    def choose_frame_color(self):
        c = QColorDialog.getColor(self.frame_color or QColor("#000000"),
                                  self, "Frame color for transparent images")
        if not c.isValid(): return
        self.frame_color = c; self._save_frame_color(); self.refresh_image()
        self.statusBar().showMessage(f"  Frame color → {c.name()}", 3000)

    def clear_frame_color(self):
        self.frame_color = None; self._save_frame_color(); self.refresh_image()
        self.statusBar().showMessage("  Frame color cleared (transparent)", 3000)

    def _photo_context_menu(self,pos):
        m=QMenu(self)
        m.addAction(make_icon("fullscreen"),"Immersive mode  (F9)",
                    self.toggle_immersive)
        m.addAction(make_icon("visibility_off"),
                    "Hide menu bar (Ctrl+Shift+M)" if self.menuBar().isVisible()
                    else "Show menu bar (Ctrl+Shift+M)",
                    self.toggle_menu_bar)
        m.addSeparator()
        m.addAction(make_icon("apps"),"Show thumbnails  (Ctrl+H)", self.toggle_thumbnails)
        m.addAction(make_icon("first_page"),"Thumbnails: bottom / left",
                    lambda: self.set_thumbnails_position(not self.thumbnails_bottom))
        m.addAction(make_icon("apps"),"Show toolbar  (Ctrl+Shift+T)", self.toggle_toolbar)
        m.addAction(make_icon("folder"),"Show File menu  (Ctrl+Shift+F)", self.toggle_file_menu)
        m.addSeparator()
        m.addAction(make_icon("image"),"Open image…  (Ctrl+O)",self.open_file)
        m.addAction(make_icon("folder"),"Open folder…  (Ctrl+Shift+O)",self.open_folder)
        m.addSeparator()
        m.addAction(make_icon("palette"),"Frame color…", self.choose_frame_color)
        m.addAction(make_icon("crop_free"),"Clear frame color", self.clear_frame_color)
        m.addSeparator()
        m.addAction(make_icon("fullscreen"),"Fullscreen  (F11)",self.toggle_fullscreen)
        m.exec(self.label.mapToGlobal(pos))

    # ================================================== toolbar
    def _toolbar_spacer(self,tb):
        w=QWidget(tb); w.setSizePolicy(QSizePolicy.Policy.Expanding,
                                        QSizePolicy.Policy.Preferred); return w

    def build_toolbar(self):
        tb=QToolBar("Photo controls"); self.main_toolbar=tb; tb.setObjectName("MainToolbar")
        tb.setMovable(False); tb.setIconSize(QSize(18,18))
        tb.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly); self.addToolBar(tb)
        tb.addWidget(self._toolbar_spacer(tb))
        for spec in (("Open",None,self.open_file,"image"),("Folder",None,self.open_folder,"folder"),None,
                     ("Previous",None,self.prev_image,"chevron_left"),
                     ("Next",None,self.next_image,"chevron_right"),None,
                     ("Zoom in","+",self.zoom_in,"zoom_in"),
                     ("Zoom out","-",self.zoom_out,"zoom_out"),
                     ("Actual size","0",self.actual_size,"actual")):
            if spec is None: tb.addSeparator()
            else: tb.addAction(self.action(*spec))
        self.fit_action=self.action("Fit to window","F",self.toggle_fit,"fit_screen",True)
        self.fit_action.setChecked(True); tb.addAction(self.fit_action); tb.addSeparator()
        tb.addAction(self.action("Rotate left","Ctrl+L",self.rotate_left,"rotate_left"))
        tb.addAction(self.action("Rotate right","Ctrl+R",self.rotate_right,"rotate_right"))
        tb.addSeparator()
        tb.addAction(self.undo_action); tb.addAction(self.redo_action); tb.addSeparator()
        self.slide_action=self.action("Slideshow","Space",self.toggle_slideshow,"slideshow",True)
        tb.addAction(self.slide_action)
        tb.addAction(self.action("Fullscreen",None,self.toggle_fullscreen,"fullscreen"))
        tb.addSeparator()
        tb.addAction(self.action("Recycle image","Delete",self.delete_current,"delete"))
        tb.addAction(self.action("Image information","I",self.show_info,"info"))
        tb.addWidget(self._toolbar_spacer(tb))

    # ================================================== thumbnails
    def build_thumbnails(self):
        self.thumb_list=QListWidget()
        self.thumb_list.setViewMode(QListWidget.ViewMode.IconMode)
        self.thumb_list.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.thumb_list.setMovement(QListWidget.Movement.Static)
        self.thumb_list.setWrapping(False)
        self.thumb_list.setFlow(QListWidget.Flow.LeftToRight)
        self.thumb_list.setSpacing(4)
        self.thumb_list.setMinimumHeight(MAX_THUMB.height()+40)
        self.thumb_list.setItemDelegate(ThumbDelegate(self.thumb_list))
        self.thumb_list.itemClicked.connect(self.thumbnail_clicked)
        dock=QDockWidget("",self); dock.setObjectName("ThumbnailDock")
        dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        dock.setTitleBarWidget(QLabel())
        dock.setAllowedAreas(Qt.DockWidgetArea.BottomDockWidgetArea)
        dock.setWidget(self.thumb_list)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea,dock)
        self.thumbnail_dock=dock

    # ================================================== undo / redo
    def _push_undo(self):
        if self.current_pixmap is None: return
        self.undo_stack.append(QPixmap(self.current_pixmap))
        if len(self.undo_stack)>UNDO_LIMIT: self.undo_stack.pop(0)
        self.redo_stack.clear(); self._refresh_undo_actions()
    def _refresh_undo_actions(self):
        self.undo_action.setEnabled(bool(self.undo_stack))
        self.redo_action.setEnabled(bool(self.redo_stack))
    def undo(self):
        if not self.undo_stack: return
        self.redo_stack.append(QPixmap(self.current_pixmap))
        self.current_pixmap=self.undo_stack.pop()
        self.rotation=0; self.refresh_image(); self._refresh_undo_actions()
        self.statusBar().showMessage("  Undo",1500)
    def redo(self):
        if not self.redo_stack: return
        self.undo_stack.append(QPixmap(self.current_pixmap))
        self.current_pixmap=self.redo_stack.pop()
        self.rotation=0; self.refresh_image(); self._refresh_undo_actions()
        self.statusBar().showMessage("  Redo",1500)
    def reset_to_original(self):
        if self.index<0 or not self.files: return
        pix=load_image(self.files[self.index])
        if pix is None: return
        self._push_undo(); self.current_pixmap=pix; self.rotation=0
        self.image_cache[self.files[self.index]]=QPixmap(self.current_pixmap)
        self.refresh_image()
        self.statusBar().showMessage("  Reverted to original file",1500)

    # ================================================== file operations
    def open_file(self):
        path,_=QFileDialog.getOpenFileName(self,"Open image","",
            "Images (*.jpg *.jpeg *.png *.bmp *.gif *.webp *.tif *.tiff *.ico *.svg *.psd);;"
            "All files (*.*)")
        if path: self.load_directory(Path(path).parent,Path(path))
    def open_folder(self):
        folder=QFileDialog.getExistingDirectory(self,"Open image folder")
        if folder: self.load_directory(Path(folder))
    def save_copy(self):
        if self.current_pixmap is None:
            QMessageBox.information(self,"Save a copy","No image loaded."); return
        path,_=QFileDialog.getSaveFileName(self,"Save a copy","",
            "PNG (*.png);;JPEG (*.jpg);;WEBP (*.webp);;BMP (*.bmp)")
        if not path: return
        # Save the displayed rotation, but preserve the image's original
        # transparency rather than baking the viewer-only frame colour in.
        pix = self.transformed_pixmap()
        if pix is not None and pix.save(path):
            self.statusBar().showMessage(f"  Saved → {path}",3000)
        else:
            QMessageBox.warning(self, "Save a copy", f"Could not save the image:\n{path}")

    def load_directory(self,folder,selected=None):
        try:
            new_files=sorted((p for p in folder.iterdir()
                              if p.is_file() and p.suffix.lower() in SUPPORTED),
                             key=lambda p:p.name.lower())
        except OSError as exc: QMessageBox.warning(self,APP_NAME,str(exc)); return
        if not new_files:
            QMessageBox.information(self,APP_NAME,"No supported images found.")
            return  # Keep the previously opened folder and image intact.
        self.files=new_files
        self.image_cache.clear()
        self.index=self.files.index(selected) if selected in self.files else 0
        self.undo_stack.clear(); self.redo_stack.clear(); self._refresh_undo_actions()
        self.begin_thumbnails(); self.load_current()

    def begin_thumbnails(self):
        self.thumb_timer.stop(); self.thumb_list.clear(); self.thumb_index=0
        for i,path in enumerate(self.files):
            item=QListWidgetItem(path.name); item.setData(Qt.ItemDataRole.UserRole,i)
            item.setToolTip(str(path))
            item.setSizeHint(QSize(MAX_THUMB.width()+10,MAX_THUMB.height()+24))
            self.thumb_list.addItem(item)
        self.thumb_list.setCurrentRow(self.index)
        self.thumb_timer.start(12)

    def load_thumbnail_batch(self):
        for _ in range(3):
            if self.thumb_index>=len(self.files):
                self.thumb_timer.stop(); return
            i=self.thumb_index; path=self.files[i]
            suffix = path.suffix.lower()
            pix = None
            if suffix == ".svg":
                r = QSvgRenderer(str(path))
                if r.isValid():
                    size = r.defaultSize() or MAX_THUMB
                    size.scale(MAX_THUMB, Qt.AspectRatioMode.KeepAspectRatio)
                    size.setWidth(max(size.width(), 28)); size.setHeight(max(size.height(), 22))
                    img = QImage(size, QImage.Format.Format_ARGB32)
                    img.fill(Qt.GlobalColor.transparent)
                    pp = QPainter(img); r.render(pp); pp.end()
                    pix = QPixmap.fromImage(img)
            else:
                reader=QImageReader(str(path)); reader.setAutoTransform(True)
                orig=reader.size()
                if orig.isValid() and orig.width()>0 and orig.height()>0:
                    target=QSize(orig); target.scale(MAX_THUMB,Qt.AspectRatioMode.KeepAspectRatio)
                    target.setWidth(max(target.width(),28)); target.setHeight(max(target.height(),22))
                else: target=QSize(MAX_THUMB)
                reader.setScaledSize(target)
                image=reader.read()
                if not image.isNull(): pix = QPixmap.fromImage(image)
            if pix is not None:
                if self.frame_color is not None: pix = self._compose_frame(pix)
                item=self.thumb_list.item(i)
                item.setData(ThumbDelegate.PIX_ROLE,pix)
                item.setSizeHint(QSize(max(pix.width(),50)+10,pix.height()+24))
            self.thumb_index+=1
        self.thumb_list.viewport().update()

    def thumbnail_clicked(self,item):
        self.index=item.data(Qt.ItemDataRole.UserRole); self.load_current()

    def load_current(self):
        if not self.files or self.index<0: return
        path=self.files[self.index]
        if path in self.image_cache:
            # A recent hit remains cached while older photos are evicted first.
            self.current_pixmap=QPixmap(self.image_cache.pop(path))
            self.image_cache[path]=self.current_pixmap
        else:
            pix = load_image(path)
            if pix is None:
                QMessageBox.warning(self,APP_NAME,
                    f"Could not open:\n{path}\n\n"
                    "If this is a PSD, the Qt qpsd plugin may be missing.")
                return
            self.current_pixmap=pix
            self.image_cache[path]=QPixmap(self.current_pixmap)
            self._trim_image_cache()
        self.rotation=0; self.zoom_factor=1.0
        self.undo_stack.clear(); self.redo_stack.clear(); self._refresh_undo_actions()
        self.setWindowTitle(f"{path.name} — {APP_NAME}")
        self.refresh_image(); self.thumb_list.setCurrentRow(self.index)
        self.thumb_list.scrollToItem(self.thumb_list.item(self.index)); self.update_status()
        self._restart_photo_idle()

    def _trim_image_cache(self):
        # QPixmap copies share pixel data, but keeping five 24–50 MP photos
        # alive can still consume hundreds of MB on ordinary Windows PCs.
        budget = 128 * 1024 * 1024
        def estimated_bytes(pix):
            return pix.width() * pix.height() * max(pix.depth(), 8) // 8
        total = sum(estimated_bytes(pix) for pix in self.image_cache.values())
        while len(self.image_cache) > 5 or (total > budget and len(self.image_cache) > 1):
            oldest = next(iter(self.image_cache))
            total -= estimated_bytes(self.image_cache.pop(oldest))

    def replace_current_pixmap(self,pixmap,record_undo=True):
        if record_undo: self._push_undo()
        self.current_pixmap=QPixmap(pixmap); self.rotation=0; self.refresh_image()

    # ================================================== view
    def transformed_pixmap(self):
        if not self.current_pixmap: return None
        # Do not run a costly full-image transform for the common 0° case.
        if self.rotation % 360 == 0: return self.current_pixmap
        t=QTransform(); t.rotate(self.rotation)
        return self.current_pixmap.transformed(t,Qt.TransformationMode.SmoothTransformation)
    def refresh_image(self):
        pix=self.transformed_pixmap()
        if pix is None: return
        pix=self._compose_frame(pix)
        if self.fit_mode:
            size=self.scroll.viewport().size()
            target=pix.scaled(max(1,size.width()-20),max(1,size.height()-20),
                              Qt.AspectRatioMode.KeepAspectRatio,
                              Qt.TransformationMode.SmoothTransformation)
        else:
            target=(pix if abs(self.zoom_factor-1.0)<1e-9 else
                    pix.scaled(pix.size()*self.zoom_factor,
                               Qt.AspectRatioMode.KeepAspectRatio,
                               Qt.TransformationMode.SmoothTransformation))
        self.label.setPixmap(target); self.label.resize(target.size()); self.update_status()
    def resizeEvent(self,event):
        super().resizeEvent(event)
        if self.fit_mode and self.current_pixmap: self.resize_timer.start()
    def next_image(self):
        if self.files: self.index=(self.index+1)%len(self.files); self.load_current()
    def prev_image(self):
        if self.files: self.index=(self.index-1)%len(self.files); self.load_current()
    def first_image(self):
        if self.files: self.index=0; self.load_current()
    def last_image(self):
        if self.files: self.index=len(self.files)-1; self.load_current()
    def zoom_in(self): self.set_zoom(self.zoom_factor*1.2)
    def zoom_out(self): self.set_zoom(self.zoom_factor/1.2)
    def set_zoom(self,value):
        if self.current_pixmap:
            self.fit_mode=False; self.fit_action.setChecked(False)
            self.zoom_factor=max(.05,min(10,value)); self.refresh_image()
    def actual_size(self): self.set_zoom(1.0)
    def toggle_fit(self): self.fit_mode=self.fit_action.isChecked(); self.refresh_image()
    def rotate_left(self):
        self._push_undo(); self.rotation=(self.rotation-90)%360; self.refresh_image()
    def rotate_right(self):
        self._push_undo(); self.rotation=(self.rotation+90)%360; self.refresh_image()
    def toggle_fullscreen(self):
        self.toggle_immersive()

    # ================================================== photo-only (separate from immersive)
    def toggle_photo_only(self, checked=None):
        enabled = (not self.photo_only) if checked is None else bool(checked)
        if enabled == self.photo_only:
            return
        if enabled and self.immersive_mode:
            self.toggle_immersive(False)
        self.idle_timer.stop()
        if enabled:
            self._before_photo_geometry = self.saveGeometry()
            self._before_photo_maximized = self.isMaximized()
        self.photo_only = enabled
        self.photo_only_action.setChecked(enabled)
        if enabled:
            self.nav_hide_timer.stop()
            for a in self._nav_anim: a.stop()
            self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
            self.showMaximized()
            for w in (self.menuBar(), self.main_toolbar, self.thumbnail_dock,
                      self.statusBar(), self.left_button, self.right_button):
                w.hide()
            self.label.setStyleSheet("background:#0f1114;color:#6c757d")
        else:
            self.setWindowFlag(Qt.WindowType.FramelessWindowHint, False)
            self.showNormal()
            if self._before_photo_geometry:
                self.restoreGeometry(self._before_photo_geometry)
            if self._before_photo_maximized:
                self.showMaximized()
            self.label.setStyleSheet("font-size:16px;color:#6c757d;background:#0f1114")
            self._apply_normal_visibility()
            self._restart_photo_idle()
        self.setFocus()
        self.refresh_image()

    # ================================================== nav auto-hide (normal mode)
    def _fade_nav_out(self):
        if self.photo_only or self.immersive_mode: return
        for i,anim in enumerate(self._nav_anim):
            anim.stop(); anim.setStartValue(self._nav_opacity[i].opacity())
            anim.setEndValue(0.0); anim.start()
    def _fade_nav_in(self):
        if self.photo_only or self.immersive_mode: return
        for i,anim in enumerate(self._nav_anim):
            if self._nav_opacity[i].opacity()<0.99:
                anim.stop(); anim.setStartValue(self._nav_opacity[i].opacity())
                anim.setEndValue(1.0); anim.start()
        self.nav_hide_timer.start()
    def mouseMoveEvent(self,event):
        super().mouseMoveEvent(event)
        if not self.photo_only and not self.immersive_mode: self._fade_nav_in()

    # ================================================== preferences / updates
    def show_preferences(self):
        self.idle_timer.stop()
        dialog = QDialog(self)
        dialog.setWindowTitle("Viewer preferences")
        dialog.setMinimumWidth(365)
        form = QFormLayout()
        auto_box = QCheckBox("Switch to photo-only after inactivity")
        auto_box.setChecked(self.auto_photo_only)
        seconds = QSpinBox(); seconds.setRange(2, 60)
        seconds.setValue(self.idle_seconds); seconds.setSuffix(" seconds")
        github_box = QCheckBox("Check GitHub for updates on startup")
        github_box.setChecked(self.check_updates_on_start)
        form.addRow("Viewing", auto_box)
        form.addRow("Idle delay", seconds)
        form.addRow("Updates", github_box)
        hint = QLabel("Left/Right: next photo · Esc: show controls\n"
                      "F10: photo only · F9/F11: clean fullscreen · Ctrl+O: open")
        hint.setWordWrap(True)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok |
                                   QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout = QVBoxLayout(dialog)
        layout.addLayout(form); layout.addWidget(hint); layout.addWidget(buttons)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.auto_photo_only = auto_box.isChecked()
            self.idle_seconds = seconds.value()
            self.check_updates_on_start = github_box.isChecked()
            self.settings.setValue("auto_photo_only", self.auto_photo_only)
            self.settings.setValue("photo_idle_seconds", self.idle_seconds)
            self.settings.setValue("check_updates_on_start", self.check_updates_on_start)
        self._restart_photo_idle()

    def check_for_updates(self, silent=False):
        from update_check import UpdateChecker
        if self._update_worker is not None and self._update_worker.isRunning():
            if not silent:
                self.statusBar().showMessage("  Already checking GitHub…", 2000)
            return
        worker = UpdateChecker(VERSION, self)
        self._update_worker = worker
        worker.checked.connect(lambda kind, message, url: self._on_update_result(
            kind, message, url, silent))
        worker.finished.connect(lambda: setattr(self, "_update_worker", None))
        worker.finished.connect(worker.deleteLater)
        worker.start()

    def _on_update_result(self, kind, message, url, silent):
        if kind == "update":
            question = QMessageBox.question(self, "New release on GitHub",
                message + "\n\nOpen the release page?\n"
                "Updates are never installed without your approval.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if question == QMessageBox.StandardButton.Yes:
                from PySide6.QtGui import QDesktopServices
                from PySide6.QtCore import QUrl
                QDesktopServices.openUrl(QUrl(url))
        elif not silent:
            QMessageBox.information(self, "GitHub update check", message)

    # ================================================== misc
    def toggle_slideshow(self):
        self.slideshow_timer.start() if self.slide_action.isChecked() else self.slideshow_timer.stop()
    def delete_current(self):
        if not self.files: return
        path=self.files[self.index]
        if QMessageBox.question(self,"Recycle image",
            f"Move this image to the Recycle Bin?\n\n{path.name}",
            QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)!=QMessageBox.StandardButton.Yes:
            return
        try:
            escaped=str(path).replace("'","''")
            cmd=("Add-Type -AssemblyName Microsoft.VisualBasic; "
                 "[Microsoft.VisualBasic.FileIO.FileSystem]::DeleteFile("
                 f"'{escaped}','OnlyErrorDialogs','SendToRecycleBin')")
            result=subprocess.run(["powershell","-NoProfile","-Command",cmd],
                                  capture_output=True,text=True)
            if result.returncode: raise RuntimeError(result.stderr.strip())
            self.files.pop(self.index); self.index=min(self.index,len(self.files)-1)
            self.begin_thumbnails()
            self.load_current() if self.files else self.clear_view()
        except Exception as exc:
            QMessageBox.warning(self,APP_NAME,f"Could not recycle image:\n{exc}")
    def clear_view(self):
        self.current_pixmap=None; self.index=-1
        self.image_cache.clear(); self.idle_timer.stop()
        self.label.clear(); self.label.setText("No images remain in this folder")
        self.setWindowTitle(f"{APP_NAME} {VERSION}")
        self.update_status()
    def show_info(self):
        if self.current_pixmap and self.files:
            p=self.files[self.index]
            QMessageBox.information(self,"Image information",
                f"File: {p.name}\nFolder: {p.parent}\n"
                f"Format: {p.suffix.upper()[1:]}\n"
                f"Dimensions: {self.current_pixmap.width()} × {self.current_pixmap.height()} px\n"
                f"Size: {p.stat().st_size/1024:.1f} KB\n"
                f"Position: {self.index+1}/{len(self.files)}")
    def update_status(self):
        if self.files and self.index>=0 and self.current_pixmap:
            self.statusBar().showMessage(
                f"  {self.index+1} / {len(self.files)}    {self.files[self.index].name}    "
                f"{'Fit' if self.fit_mode else f'{self.zoom_factor:.0%}'}    {self.rotation}°")
        else: self.statusBar().showMessage("  Ready — drop an image or open a folder")
    def wheelEvent(self,event):
        if event.modifiers()&Qt.KeyboardModifier.ControlModifier:
            self.zoom_in() if event.angleDelta().y()>0 else self.zoom_out(); event.accept()
        elif self.photo_only or self.immersive_mode:
            self.prev_image() if event.angleDelta().y()>0 else self.next_image(); event.accept()
        else: super().wheelEvent(event)
    def dragEnterEvent(self,event):
        if event.mimeData().hasUrls() and any(
            Path(u.toLocalFile()).suffix.lower() in SUPPORTED for u in event.mimeData().urls()):
            event.acceptProposedAction()
    def dropEvent(self,event):
        paths=[Path(u.toLocalFile()) for u in event.mimeData().urls()]
        image=next((p for p in paths if p.is_file() and p.suffix.lower() in SUPPORTED),None)
        if image: self.load_directory(image.parent,image)
    def closeEvent(self,event):
        self.idle_timer.stop()
        if self._update_worker is not None and self._update_worker.isRunning():
            self._update_worker.wait(6000)
        if self.photo_only and self._before_photo_geometry is not None:
            self.settings.setValue("geometry", self._before_photo_geometry)
        else:
            self.settings.setValue("geometry",self.saveGeometry())
        super().closeEvent(event)
    def keyPressEvent(self, event):
        super().keyPressEvent(event)


def main():
    app=QApplication(sys.argv); app.setApplicationName(APP_NAME); app.setOrganizationName("BANG Tools")
    app.setStyle("Fusion"); app.setStyleSheet(STYLE)
    window=PhotoViewer(); window.show()
    if len(sys.argv)>1:
        path=Path(sys.argv[1])
        if path.is_file() and path.suffix.lower() in SUPPORTED:
            window.load_directory(path.parent,path)
    sys.exit(app.exec())
if __name__=="__main__": main()
