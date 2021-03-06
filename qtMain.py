import sys
import os
import pprint
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from audioRecordingManagerWindow_auto import Ui_AudioRecordingManagerWindow

from logic.metadata import Metadata
from logger import Logger
from logic.compression import Compression
from logic.file import File
from logic.open import Open

class ProjectsTableModel(QAbstractTableModel):
    def __init__(self, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)

    def rowCount(self, parent):
        return len(File.allProjects(os.getcwd()))

    def columnCount(self, parent):
        return len(Metadata.listUsedAnnotations(os.getcwd()))

    def headerData(self, section, orientation, role = QtCore.Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                listUsedAnnotations = Metadata.listUsedAnnotations(os.getcwd())
                key = listUsedAnnotations[section]
            
                return QString(key)
            
            elif orientation == Qt.Vertical:
                project = File.allProjects(os.getcwd())[section]

                return QVariant(project)
            
        else:
            return QVariant()

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole and role != Qt.EditRole:
            return QVariant()
        
        project = File.allProjects(os.getcwd())[index.row()]
        metadatakey = Metadata.listUsedAnnotations(os.getcwd())[index.column()]
        annotations = Metadata.getAnnotations(project)
        if annotations.has_key(metadatakey):
            metadatavalue = annotations[metadatakey]
        else:
            metadatavalue = "<NOT SET>"
            
        return QVariant(metadatavalue)
    
    def setData(self, index, value, role=Qt.EditRole):
        row = index.row()
        col = index.column()
        
        project = File.allProjects(os.getcwd())[row]
        metadatakey = Metadata.listUsedAnnotations(os.getcwd())[col]
        value = str(value.toPyObject())
        
        Metadata.setMetadata(project, metadatakey, value)
        
        return True
    
    def flags(self, index):
        flags = super(self.__class__,self).flags(index)

        flags |= Qt.ItemIsEditable
        flags |= Qt.ItemIsSelectable
        flags |= Qt.ItemIsEnabled
        flags |= Qt.ItemIsDragEnabled
        flags |= Qt.ItemIsDropEnabled

        return flags

class StartQT4(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_AudioRecordingManagerWindow()
        self.ui.setupUi(self)

        QtCore.QObject.connect(self.ui.helloButton,QtCore.SIGNAL("clicked()"), self.hello)

        tablemodel = ProjectsTableModel(self)
        self.ui.projectsTableView.setModel(tablemodel)

    def hello(self):
        self.ui.helloButton.setText('aaaaaaaaaa')

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()
    sys.exit(app.exec_())
