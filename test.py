from PyQt5 import QtCore, QtGui
#app = QtGui.QApplication([])

class Delegate(QtGui.QItemDelegate):
       def __init__(self):
           QtGui.QItemDelegate.__init__(self)

       def createEditor(self, parent, option, index):
           if index.column()==0:
               lineedit=QtGui.QLineEdit(parent)
               return lineedit

           elif index.column()==1:
               combo=QtGui.QComboBox(parent)
               return combo

       def setEditorData(self, editor, index):
           row = index.row()
           column = index.column()
           value = index.model().items[row][column]
           if isinstance(editor, QtGui.QComboBox):
               editor.addItems(['Somewhere','Over','The Rainbow'])
               editor.setCurrentIndex(index.row())
           if isinstance(editor, QtGui.QLineEdit):
               editor.setText('Somewhere over the rainbow')

class Model(QtCore.QAbstractTableModel):
       def __init__(self):
           QtCore.QAbstractTableModel.__init__(self)
           self.items = [[1, 'one', 'ONE'], [2, 'two', 'TWO'], [3, 'three', 'THREE']]

       def flags(self, index):
           return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
       def rowCount(self, parent=QtCore.QModelIndex()):
           return 3 
       def columnCount(self, parent=QtCore.QModelIndex()):
           return 3

       def data(self, index, role):
           if not index.isValid(): return 
           