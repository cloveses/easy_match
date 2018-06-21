from PyQt5.QtWidgets import QTableView,QMainWindow, QScrollArea, QLabel,QWidget, QApplication
from PyQt5.QtGui import QColor,QPalette,QStandardItem,QStandardItemModel
import sys


class MyUi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.show()

    def setupUi(self):
        self.wdgt = QTableView()


        self.model = QStandardItemModel(4,3)
        for r in range(4):
            for c in range(3):
                it = QStandardItem('a {},c {}'.format(r,c))
                self.model.setItem(r,c,it)
        self.wdgt.setModel(self.model)
        
        self.model.itemChanged.connect(self.pr)
        self.wdgt.setStyleSheet('QWidget{background-color:rgb(255,255,255)}')
        self.wdgt.setMinimumSize(1500,800)

        scroll = QScrollArea(self)
        scroll.setWidget(self.wdgt)
        self.setCentralWidget(scroll)

    def pr(self):
        print('jjkkk')
        print(self.wdgt.currentIndex().row(),self.wdgt.currentIndex().column(),self.wdgt.currentIndex().data())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyUi()
    ex.show()
    sys.exit(app.exec_())

        
