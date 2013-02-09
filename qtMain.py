import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from audioRecordingManagerWindow_auto import Ui_AudioRecordingManagerWindow


my_array = [['00','01','02'],
            ['10','11','12'],
            ['20','21','22']]

class MyTableModel(QAbstractTableModel):
    def __init__(self, datain, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain

    def rowCount(self, parent):
        return len(self.arraydata)
#return len(getProjects())

    def columnCount(self, parent):
        return len(self.arraydata[0])
#return len(getMetadata())

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.arraydata[index.row()][index.column()])
#project = getProjectByNum(index.row())
#metadatakey = getMetadataKeyByNum(index.column())
#return QVariant(getMetadata(project)[metadatakey])

class StartQT4(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_AudioRecordingManagerWindow()
        self.ui.setupUi(self)

        QtCore.QObject.connect(self.ui.helloButton,QtCore.SIGNAL("clicked()"), self.hello)

        tablemodel = MyTableModel(my_array, self)
        self.ui.tableView.setModel(tablemodel)

    def hello(self):
	self.ui.helloButton.setText('aaaaaaaaaa')

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()
    sys.exit(app.exec_())
