#!/usr/bin/env python
from PyQt4 import QtGui, QtCore
from gclip_ui import Ui_GClipDialog
from PyKDE4 import kdecore
from PyKDE4 import kdeui

#we need access to the clip_client package (currently a sibling of gclip)
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
from clip_client.clip_client import *

class GClip(kdeui.KMainWindow, Ui_GClipDialog):
    gclip_client = None
    def __init__ (self, *args):
        kdeui.KMainWindow.__init__ (self)
        rootWidget = QtGui.QWidget(self)
        self.setupUi(rootWidget)
        self.setCentralWidget(rootWidget)

        self.btnStart.clicked.connect(self.handle_start)
        self.btnSendRecieve.clicked.connect(self.handle_sendreceive)
        self.btnSendOnly.clicked.connect(self.handle_sendonly)
        self.btnReceiveOnly.clicked.connect(self.handle_recieveonly)
        self.btnPause.clicked.connect(self.handle_pause)

        self.gclip_client = GClipClient()

    def handle_start(self):
        if self.gclip_client:
            self.gclip_client.start()

    def handle_sendreceive(self):
        if self.gclip_client:
            self.gclip_client.toggle_send_recieve()

    def handle_sendonly(self):
        if self.gclip_client:
            self.gclip_client.toggle_send_only()

    def handle_recieveonly(self):
        if self.gclip_client:
            self.gclip_client.toggle_recieve_only()

    def handle_pause(self):
        if self.gclip_client:
            self.gclip_client.toggle_stop_client()

    def handle_exit(self):
        if self.gclip_client:
            self.gclip_client.exit()

if __name__ == '__main__':
    import sys
    global app
    appName     = "GClip"
    catalog     = "" #the translation catalog name -- defaults to appName
    programName = kdecore.ki18n(appName)
    version     = "1.0"
    desc = """
GClip v.1 : A simple front-end for the powerful Python GlobalClipboard Client, ClipClient (v.1.1)
Nemesis Fixx (joewillrich@gmail.com) 2012
GClip and GlobalClipboard Client are both GPL Licensed. 
"""
    description = kdecore.ki18n(desc)
    license     = kdecore.KAboutData.License_GPL
    copyright   = kdecore.ki18n("GPL")
    text        = kdecore.ki18n("none")
    homePage    = "https://plus.google.com/u/0/113417329814714254684"
    bugEmail    = "joewillrich@gmail.com"

    aboutData   = kdecore.KAboutData(appName, catalog, programName, version, description,
                              license, copyright, text, homePage, bugEmail)
    kdecore.KCmdLineArgs.init(sys.argv, aboutData)

    app = kdeui.KApplication()
    mainWindow = GClip(None, appName)
    mainWindow.show()

    def finishem():
        mainWindow.handle_exit()
        app.quit()
        
    app.lastWindowClosed.connect(finishem)
    sys.exit(app.exec_())
