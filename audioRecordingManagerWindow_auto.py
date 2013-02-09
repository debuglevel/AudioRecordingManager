# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'audioRecordingManagerWindow.ui'
#
# Created: Sun Feb 10 00:36:13 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_AudioRecordingManagerWindow(object):
    def setupUi(self, AudioRecordingManagerWindow):
        AudioRecordingManagerWindow.setObjectName(_fromUtf8("AudioRecordingManagerWindow"))
        AudioRecordingManagerWindow.resize(584, 500)
        self.centralwidget = QtGui.QWidget(AudioRecordingManagerWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.projectsTableView = QtGui.QTableView(self.centralwidget)
        self.projectsTableView.setObjectName(_fromUtf8("projectsTableView"))
        self.verticalLayout_2.addWidget(self.projectsTableView)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.newProjectButton = QtGui.QPushButton(self.centralwidget)
        self.newProjectButton.setObjectName(_fromUtf8("newProjectButton"))
        self.horizontalLayout.addWidget(self.newProjectButton)
        self.openButton = QtGui.QPushButton(self.centralwidget)
        self.openButton.setObjectName(_fromUtf8("openButton"))
        self.horizontalLayout.addWidget(self.openButton)
        self.helloButton = QtGui.QPushButton(self.centralwidget)
        self.helloButton.setObjectName(_fromUtf8("helloButton"))
        self.horizontalLayout.addWidget(self.helloButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        AudioRecordingManagerWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(AudioRecordingManagerWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 584, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        AudioRecordingManagerWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(AudioRecordingManagerWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        AudioRecordingManagerWindow.setStatusBar(self.statusbar)

        self.retranslateUi(AudioRecordingManagerWindow)
        QtCore.QObject.connect(self.newProjectButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.newProjectButton.click)
        QtCore.QMetaObject.connectSlotsByName(AudioRecordingManagerWindow)

    def retranslateUi(self, AudioRecordingManagerWindow):
        AudioRecordingManagerWindow.setWindowTitle(QtGui.QApplication.translate("AudioRecordingManagerWindow", "Audio Recording Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.newProjectButton.setText(QtGui.QApplication.translate("AudioRecordingManagerWindow", "Neues Projekt", None, QtGui.QApplication.UnicodeUTF8))
        self.openButton.setText(QtGui.QApplication.translate("AudioRecordingManagerWindow", "Projekt öffnen", None, QtGui.QApplication.UnicodeUTF8))
        self.helloButton.setText(QtGui.QApplication.translate("AudioRecordingManagerWindow", "Hello", None, QtGui.QApplication.UnicodeUTF8))

