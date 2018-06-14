from PyQt5.QtWidgets import QStandardItem,QStandardItemModel,QTableView,QTableWidgetItem,QTableWidget,QMainWindow, QScrollArea, QLabel,QWidget, QApplication
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

        # super(myDialog, self).__init__(arg)
        # self.setWindowTitle("first window")
        # self.setWindowFlags(Qt.WindowMaximizeButtonHint|Qt.WindowMinimizeButtonHint|Qt.WindowCloseButtonHint)
        # self.resize(500,300);
        # self.model=QStandardItemModel(4,4);
        # self.model.setHorizontalHeaderLabels(['标题1','标题2','标题3','标题4'])
        # for row in range(4):
        #     for column in range(4):
        #         item = QStandardItem("row %s, column %s"%(row,column))
        #         self.model.setItem(row, column, item)
        # self.tableView=QTableView();
        # self.tableView.setModel(self.model)
        # #下面代码让表格100填满窗口
        # #self.tableView.horizontalHeader().setStretchLastSection(True)
        # #self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # dlgLayout=QVBoxLayout();
        # dlgLayout.addWidget(self.tableView)
        # self.setLayout(dlgLayout)