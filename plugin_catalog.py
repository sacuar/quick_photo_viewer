BASE = "https://raw.githubusercontent.com/sacuar/folder/b7af0f4ac2aa6a8894364d152d1c7a9b6276f770/optional_plugins/"
ROOT = ".quick_photo_viewer/github_plugins"
CATALOG = {"image_tools":["Image conversion and resize","6fe24803c2cded416b34676fc57e2b47d9305de2"]}
"""Explicit opt-in plugin installs from an immutable GitHub revision."""
import hashlib,importlib.util,os
from pathlib import Path
from PySide6.QtCore import QObject,Signal,QUrl
from PySide6.QtNetwork import QNetworkAccessManager,QNetworkRequest
from PySide6.QtWidgets import QDialog,QVBoxLayout,QLabel,QListWidget,QListWidgetItem,QPushButton,QMessageBox
PREVIEWS={};THUMBS={}
class API:
    def __init__(self,host,menu):self.host=host;self.menu=menu
    def action(self,label,fn):self.menu.addAction(label,lambda:fn(self.host))
    def preview(self,ext,widget,thumb):PREVIEWS[ext]=widget;THUMBS[ext]=thumb
class Manager(QObject):
    def __init__(self,host):
        super().__init__(host);self.host=host;self.root=Path.home()/ROOT;self.net=QNetworkAccessManager(self)
        self.menu=host.menuBar().addMenu('Plugins');self.menu.addAction('Install available plugins…',self.show_catalog)
        self.menu.addAction('Manage installed plugins…',self.show_catalog);self.menu.addSeparator()
        self.actions=self.menu.addMenu('Installed tools');self.load()
    def valid(self,key,data):
        return hashlib.sha1(('blob '+str(len(data))+'\0').encode()+data).hexdigest()==CATALOG[key][1]
    def load(self):
        for key in CATALOG:
            p=self.root/(key+'.py')
            if not p.is_file():continue
            try:
                data=p.read_bytes()
                if not self.valid(key,data):continue
                spec=importlib.util.spec_from_file_location('optional_'+key,p);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);mod.register(API(self.host,self.actions))
            except Exception as e:self.host.statusBar().showMessage('Plugin '+key+': '+str(e),10000)
    def show_catalog(self):
        if getattr(self,'dialog',None) is not None and self.dialog.isVisible():self.dialog.raise_();return
        d=QDialog(self.host);self.dialog=d;d.setWindowTitle('Available plugins');d.resize(650,420);l=QVBoxLayout(d)
        l.addWidget(QLabel('Optional GitHub plugins. Install only what you need. Restart after changes.'))
        self.list=QListWidget();l.addWidget(self.list)
        self.refresh()
        for label,fn in [('Install selected',self.install),('Uninstall selected',self.remove),('Close',d.close)]:
            b=QPushButton(label);b.clicked.connect(fn);l.addWidget(b)
        d.show()
    def refresh(self):
        self.list.clear()
        for key,(label,sha) in CATALOG.items():
            p=self.root/(key+'.py');installed=p.is_file()
            item=QListWidgetItem(label+' — '+('Installed' if installed else 'Available'));item.setData(256,key);self.list.addItem(item)
    def key(self):
        item=self.list.currentItem();return item.data(256) if item else None
    def install(self):
        key=self.key()
        if not key:return
        if QMessageBox.question(self.dialog,'Install plugin','Download and install this repository-pinned Python plugin? It runs with your permissions after restart.')!=QMessageBox.Yes:return
        req=QNetworkRequest(QUrl(BASE+key+'.py'));req.setTransferTimeout(15000);reply=self.net.get(req)
        def done():
            try:
                data=bytes(reply.readAll())
                if reply.error() or len(data)>200000 or not self.valid(key,data):raise ValueError('Download or integrity validation failed')
                self.root.mkdir(parents=True,exist_ok=True);p=self.root/(key+'.py');tmp=p.with_suffix('.tmp');tmp.write_bytes(data);os.replace(tmp,p)
                self.refresh();QMessageBox.information(self.host,'Plugins','Installed. Restart the application to activate.')
            except Exception as e:QMessageBox.warning(self.host,'Plugins',str(e))
            finally:reply.deleteLater()
        reply.downloadProgress.connect(lambda n,t:reply.abort() if n>200000 or t>200000 else None);reply.finished.connect(done)
    def remove(self):
        key=self.key()
        if not key:return
        if QMessageBox.question(self.dialog,'Uninstall plugin','Remove the selected plugin? Restart to deactivate.')!=QMessageBox.Yes:return
        try:(self.root/(key+'.py')).unlink(missing_ok=True);self.refresh()
        except OSError as e:QMessageBox.warning(self.host,'Plugins',str(e))
