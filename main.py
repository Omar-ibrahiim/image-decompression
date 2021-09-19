import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets, QtCore
from pyqtgraph.Qt import QtGui, QtCore
import UI as UI
import sys
import tst



class ApplicationWindow(UI.Ui_MainWindow):
    def __init__(self, mainwindow):
        super(ApplicationWindow,self).setupUi(mainwindow)
        self.pushButton.clicked.connect(lambda : self.openFile())
        self.labels=[
            self.label,
            self.label_2,
            self.label_3,
            self.label_4,
            self.label_5,
            self.label_6,
            self.label_7,
            self.label_8
        ]
        
        
    def openFile(self):
        data=None
        data,filename = tst.getData() 
        if data is None:# if there is no data (canceled)#
            pass
        
        else:
            Chunks,numberOfChunks = tst.getChunkesFromImage(data)
            pictures=tst.getPicturesFromChunks(Chunks)
            pixmaps =tst.getPixmapsFromPictures(pictures)
            for label in self.labels:
                labelIndex=self.labels.index(label)
                if  labelIndex>=len(pixmaps) or pixmaps[labelIndex] is None:
                    pass
                else:
                    label.setPixmap(pixmaps[labelIndex])
                    label.setScaledContents(True)
            
            
                
            
def main():
    app=QtWidgets.QApplication(sys.argv)
    mainwindow = QtWidgets.QMainWindow()
    ApplicationWindow(mainwindow)
    mainwindow.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()