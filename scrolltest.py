from PyQt5.QtWidgets import QTableWidgetItem,QTableWidget,QMainWindow, QScrollArea, QLabel,QWidget, QApplication
from PyQt5.QtGui import QColor,QPalette
import sys


class MyUi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.show()

    def setupUi(self):
        self.wdgt = QTableWidget(15,10)

        self.wdgt.setItem(2,3,QTableWidgetItem('abc'))
        self.wdgt.setItem(2,4,QTableWidgetItem('edes'))
        self.wdgt.setItem(2,5,QTableWidgetItem('eee'))
        self.wdgt.setStyleSheet('QWidget{background-color:rgb(255,255,255)}')
        self.wdgt.setMinimumSize(1500,800)

        self.wdgt.cellChanged.connect(self.edit_cell)

        scroll = QScrollArea(self)
        scroll.setWidget(self.wdgt)
        self.setCentralWidget(scroll)

    def edit_cell(self,row,col):
        item = self.wdgt.item(row,col)
        txt = item.text()
        print(txt,self.wdgt.currentRow())

# removeRow(currentRow())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyUi()
    ex.show()
    sys.exit(app.exec_())

# self.tableWidget.item(rowindex, colindex).text()   
# row_count = self.table.rowCount()
# self.table.insertRow(row_count)

# row_count = self.table.rowCount()
# self.table.removeRow(row_count-1)