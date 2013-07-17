#! /usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore, QtWebKit
from utils import get_default_locale
from xdg import get_icon
from globalkey import GlobalKey
from google_engine import LANGUAGES, google_translate

class BingGroupBox(QtGui.QGroupBox):
    
    def __init__(self, parent=None):
        super(BingGroupBox, self).__init__(parent)
        
        
        self.webview = QtWebKit.QWebView(self)  
        self.webview.load(QtCore.QUrl("http://cn.bing.com/dict"))      
        self.webview.setGeometry(QtCore.QRect(-110, -35, 700, 330))        
        self.webview.loadFinished.connect(self.on_webview_finished)
        self.webframe = None
        
    def translate_word(self, word):    
        if self.webframe is None:
            self.webframe = self.webview.page().mainFrame()        
            
        document = self.webframe.documentElement()
        input_element = document.findFirst('input#sb_form_q')
        input_element.setAttribute("value", word)        
        submit_element = document.findFirst('input#sb_form_go')
        submit_element.evaluateJavaScript("this.click()")
        
    def on_webview_finished(self, arg):    
        self.webframe = self.webview.page().mainFrame()        
        
class GoogleBox(QtGui.QGroupBox):        
    
    def __init__(self, parent=None):
        super(GoogleBox, self).__init__(parent)
        
        self.source_text_view = QtGui.QTextEdit()
        self.result_text_view = QtGui.QTextEdit()
        self.create_control_layout()
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.source_text_view)
        layout.addLayout(self.control_layout)        
        layout.addWidget(self.result_text_view)
        self.setLayout(layout)        
        
    def create_control_layout(self):    
        self.source_combox = self.create_language_combox()
        self.source_combox.setCurrentIndex(self.source_combox.findData("auto"))
        
        self.target_combox = self.create_language_combox()
        self.target_combox.setCurrentIndex(self.target_combox.findData(get_default_locale()[0]))
        self.translate_button = QtGui.QPushButton(u"翻译")
        self.translate_button.clicked.connect(self.on_translate_clicked)
        
        self.control_layout = QtGui.QHBoxLayout()
        self.control_layout.addWidget(self.source_combox)
        self.control_layout.addWidget(self.target_combox)
        self.control_layout.addStretch()
        self.control_layout.addWidget(self.translate_button)
        
    def create_language_combox(self):    
        combox = QtGui.QComboBox()
        for data in LANGUAGES:
            combox.addItem(data[1], data[0])
        return combox    
    
    def on_translate_clicked(self):
        source_text =  self.source_text_view.toPlainText()
        if not source_text:
            return 
        source_language = self.source_combox.itemData(self.source_combox.currentIndex()).toPyObject()
        target_language = self.target_combox.itemData(self.target_combox.currentIndex()).toPyObject()
        _, encoding = get_default_locale()
        
        source_text = source_text.toUtf8()
        result_text = google_translate(source_text, source_language, target_language, encoding)
        self.result_text_view.setPlainText(result_text)
        
    def translate_word(self, text):    
        self.source_text_view.setPlainText(text)
        self.on_translate_clicked()
                
class QDictWidget(QtGui.QWidget):        
    global_hotkey  = QtCore.pyqtSignal(object)
    
    def __init__(self):
        super(QDictWidget, self).__init__()
        
        websetting = QtWebKit.QWebSettings.globalSettings()
        websetting.setAttribute(QtWebKit.QWebSettings.JavascriptEnabled,  True)
        websetting.setAttribute(QtWebKit.QWebSettings.PluginsEnabled,  True)        
        
        self.bing_box = BingGroupBox()
        self.google_box = GoogleBox()
        self.tab_widget = QtGui.QTabWidget(self)
        self.tab_widget.addTab(self.bing_box, QtGui.QIcon(get_icon("bing.png")), "Bing")
        self.tab_widget.addTab(self.google_box, QtGui.QIcon(get_icon("google.png")), "Google")
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.tab_widget)
        
        self.system_clipboard = QtGui.QApplication.clipboard()
        self.system_clipboard.dataChanged.connect(self.on_clipboard_data_changed)
        # self.system_clipboard.selectionChanged.connect(self.on_clipboard_selection_changed)
        # self.system_clipboard.findBufferChanged.connect(self.on_clipboard_findbuffer_changed)
        QtGui.qApp.lastWindowClosed.connect(self.on_window_closed)
        self.global_hotkey.connect(self.on_global_hotkey)
                
        self.bind_global_key()
        
        self.setMinimumSize(620, 400)
        self.setLayout(layout)
        self.create_actions()
        self.create_trayicon()
        self.set_sheet_style("Cleanlooks")
        
    def closeEvent(self, event):
        self.hide()
        event.ignore()
        
    def create_trayicon(self):    
        self.trayicon_menu = QtGui.QMenu(self)
        self.trayicon_menu.addAction(self.hide_action)        
        self.trayicon_menu.addAction(self.restore_action)        
        self.trayicon_menu.addSeparator()
        self.trayicon_menu.addAction(self.quit_action)
                
        self.trayicon = QtGui.QSystemTrayIcon(self)
        icon = QtGui.QIcon(get_icon("dict.ico"))
        self.setWindowIcon(icon)
        self.trayicon.setIcon(icon)
        self.trayicon.setContextMenu(self.trayicon_menu)
        self.trayicon.activated.connect(self.on_trayicon_activated)
        self.trayicon.show()
        
    def toggle_visible(self):    
        if self.isVisible():
            if not self.isActiveWindow():
                self.activateWindow()
            else:    
                self.hide()
        else:        
            self.showNormal()
        
    def emit_global_hotkey(self, string):        
        self.global_hotkey.emit("toggle_visible")
        
    def on_global_hotkey(self, string):    
        func = getattr(self, string, None)
        if func: 
            func()
        
    def on_trayicon_activated(self, reason):    
        if reason in (QtGui.QSystemTrayIcon.Trigger, QtGui.QSystemTrayIcon.DoubleClick):
            self.toggle_visible()
            
    def create_actions(self):    
        self.quit_action = QtGui.QAction("&Quit", self, triggered=self.clean_quit)
        self.hide_action = QtGui.QAction("&Hide", self, triggered=self.hide)
        self.restore_action = QtGui.QAction("&Restore", self, triggered=self.showNormal)
        
        
    def on_clipboard_selection_changed(self):    
        mimedata = self.system_clipboard.mimeData(QtGui.QClipboard.Selection)
        if mimedata.hasText():
            print unicode(mimedata.text())
        # print "ddd"
        
    def on_clipboard_findbuffer_changed(self):    
        print "findddd"
        
    def on_clipboard_data_changed(self):    
        text = self.system_clipboard.text("plain") # or html
        self.bing_box.translate_word(text)
        self.google_box.translate_word(text)
        
    def bind_global_key(self):    
        self.global_key = GlobalKey()
        self.global_key.bind("Ctrl + Alt + Z", lambda :self.emit_global_hotkey("toggle_visible"))
        self.global_key.start()
            
    def unbind_global_key(self):        
        self.global_key.exit()
    
    def clean_quit(self):        
        self.unbind_global_key()
        QtGui.qApp.quit()
        
    def on_window_closed(self):    
        self.clean_quit()
        
    def set_sheet_style(self, style_name):    
        QtGui.QApplication.setPalette(QtGui.QApplication.style().standardPalette())        
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(style_name))
        
if __name__ == "__main__":        
    import sys
    app = QtGui.QApplication(sys.argv)
    win = QDictWidget()
    win.show()
    sys.exit(app.exec_())
    
