import tempfile
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from PySide6.QtGui import QImage,QColor,QPainter
from app import PhotoViewer, STYLE
app=QApplication([]);app.setStyle('Fusion');app.setStyleSheet(STYLE)
with tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp)
    for i,c in enumerate(['#207e9c','#527b67','#ba8a58']):
        im=QImage(1000,650,QImage.Format_RGB32);im.fill(QColor(c));p=QPainter(im);p.setPen(QColor('white'));p.drawText(60,80,'Sample photo '+str(i+1));p.end();im.save(str(root/f'Sample-{i+1}.png'))
    w=PhotoViewer();w.auto_photo_only=False;w.resize(1280,800);w.show();w.load_directory(root)
    def capture():
        if not w.grab().save('workspace.png'):app.exit(1)
        else:app.quit()
    QTimer.singleShot(1800,capture)
    raise SystemExit(app.exec())
