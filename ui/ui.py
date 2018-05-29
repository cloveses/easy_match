from models.gather import clear_data,load_data,get_games
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QComboBox,QVBoxLayout,QHBoxLayout,QScrollArea,QWidget,QLabel,QMainWindow, QTextEdit, QAction, QApplication,QFileDialog,QMessageBox,QGridLayout,QFormLayout

class Ui_MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.retranslateUi(self)


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(775, 532)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 775, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.action_init = QtWidgets.QAction(MainWindow)
        self.action_init.setObjectName("action_init")

        self.action_import_data = QtWidgets.QAction(MainWindow)
        self.action_import_data.setObjectName("action_import_data")

        self.menu.addAction(self.action_init)
        self.menu.addAction(self.action_import_data)
        self.menu.addSeparator()
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.action_init.triggered.connect(self.clear_data_firm)
        self.action_import_data.triggered.connect(self.get_data_file)


        main_form = QFormLayout()
        left_widgt = QWidget(None)
        left_widgt_layout = QVBoxLayout()
        left_widgt.setLayout(left_widgt_layout)
        for i in range(5):
            left_widgt_layout.addWidget(QLabel('标签%i' % i))

        for w in self.get_left_widgts():
            left_widgt_layout.addWidget(w)

        scroll_area = QScrollArea()
        right_widgt = QWidget(None)
        self.right_widgt_layout = QHBoxLayout()
        right_widgt.setLayout(self.right_widgt_layout)
        self.right_widgt_layout.addWidget(QLabel('标签%i' % 5))
        self.right_widgt_layout.addWidget(QLabel('标签%i' % 7))
        scroll_area.setWidget(right_widgt)
        
        main_form.addRow(left_widgt,scroll_area)

        main_widgt = QWidget(None)
        main_widgt.setLayout(main_form)
        self.setCentralWidget(main_widgt)

    def get_left_widgts(self):
        widgts = []
        self.game_data = get_games()
        widgts.append(QLabel('运动项目:'))
        self.game_combo = QComboBox(None)
        for item in self.game_data.keys():
            self.game_combo.addItem(item)
        widgts.append(self.game_combo)

        self.game_combo.activated[str].connect(self.set_cur_game)
        return widgts

    def set_cur_game(self,game):
        self.game = game
        print(game,self.game_data[game])

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menu.setTitle(_translate("MainWindow", "&管理数据"))
        self.action_init.setText(_translate("MainWindow", "&清理数据"))
        self.action_import_data.setText(_translate("MainWindow", "&导入数据"))

    def get_data_file(self):
        fname = QFileDialog.getOpenFileName(self, '打开文件', '.\\')
        if fname[0]:
            info = load_data(fname[0])
            if info:
                QMessageBox.information(self,"数据错误,请修改后重新导入！",info)
            else:
                QMessageBox.information(self,"提示：",'数据导入成功！')

    def clear_data_firm(self):
        reply = QMessageBox.question(self, '确认', '确定删除数据?',QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            clear_data()

# QApplication.processEvents()