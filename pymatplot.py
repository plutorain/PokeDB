import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class QHistoGram(QDialog):
    def __init__(self, data = None):
        super(QDialog, self).__init__()
        self.canvas = None
        self.IsDataSet = False
        self.value = None
        self.width = 0.35
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowMinMaxButtonsHint)
        if(data == None or isinstance(data, list) or isinstance(data, dict)):
            if(data != None):
                self.N = len(data)
                self.fig = plt.Figure()
                self.ax = self.fig.add_subplot(111)
                if(isinstance(data, dict)):
                    self.SetXtickLabels(list(data.keys()))
                    self.value = data.values()
                else:
                    self.value = data
                ind = np.arange(self.N)
                self.ax.bar(ind, self.value, self.width)
                self.ax.set_xticks(ind + self.width / 20)
                self.IsDataSet = True
        else:
            raise TypeError


    def SetXtickLabels(self, x_labels):
        if(isinstance(x_labels, list) or isinstance(x_labels, tuple)):
            pass
        else:
            raise TypeError
        self.ax.set_xticklabels(x_labels)


    def DrawGraph(self):
        if(self.IsDataSet == False):
            print("value is not setted")
            raise EnvironmentError
            
        self.canvas = FigureCanvas(self.fig)
        self.canvas.draw()
        lay = QHBoxLayout()
        self.setLayout(lay)
        lay.addWidget(self.canvas)
        self.canvas.show()
    
    def SetLabels(self, label_x=None , label_y=None , title = None):
        if(label_x):
            self.ax.set_xlabel(label_x)
        if(label_y):
            self.ax.set_ylabel(label_y)
        if(title):
            self.ax.set_title(label_y)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    data_list = [10,20,30,40]
    data_dic = {'a' : 10 , 'b' : 20, 'c': 30, 'd':40}

    d = QHistoGram(data_dic)
    d.show()
    d.SetLabels('Group', 'Score')
    d.DrawGraph()
    app.exec_()