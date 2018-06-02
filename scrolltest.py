from PyQt5.QtWidgets import QMainWindow, QScrollArea, QLabel,QWidget, QApplication
from PyQt5.QtGui import QColor,QPalette
import sys


class MyUi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.show()

    def setupUi(self):
        wdgt = QWidget()
        wdgt.setStyleSheet('QWidget{background-color:rgb(255,255,255)}')
        wdgt.setMinimumSize(1500,800)

        scroll = QScrollArea(self)
        scroll.setWidget(wdgt)
        self.setCentralWidget(scroll)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyUi()
    ex.show()
    sys.exit(app.exec_())

        
