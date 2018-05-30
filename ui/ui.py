from models.gather import has_data,clear_data,load_data,get_games,get_games_sex,get_players
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton,QCheckBox,QComboBox,QVBoxLayout,QHBoxLayout,QScrollArea,QWidget,QLabel,QMainWindow, QTextEdit, QAction, QApplication,QFileDialog,QMessageBox,QGridLayout,QFormLayout

class MyQVBoxLayout(QVBoxLayout):
    def maximumSize(self):
        return QtCore.QSize(100,-1)

class Ui_MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.select_checkbox_num = 0
        self.setupUi(self)
        self.retranslateUi(self)


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(775, 532)
        # self.centralwidget = QtWidgets.QWidget(MainWindow)
        # self.centralwidget.setObjectName("centralwidget")
        # MainWindow.setCentralWidget(self.centralwidget)

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

        if has_data():
            self.add_team_ui()

    def add_team_ui(self):
        self.centralwidget = QWidget()
        self.form_layout = QHBoxLayout(self.centralwidget)

        self.left_layout = MyQVBoxLayout()
        self.right_layout = QVBoxLayout()

        qbtn = QPushButton('1')
        qbtn.resize(qbtn.minimumSize())
        widgts = self.get_left_widgts()
        # self.left_layout.addWidget(qbtn)
        # self.left_layout.addWidget(QLabel('def'))
        for widgt in widgts:
            self.left_layout.addWidget(widgt)
        self.left_layout.addStretch()
        # self.right_layout.addWidget(QLabel('aaaa'),0,0)
        # self.right_layout.addWidget(QLabel('bbbb'),1,0)
        widgts = self.get_right_widgets()
        for widgt in widgts:
            self.right_layout.addWidget(widgt)
        self.right_layout.addStretch()
        self.form_layout.addLayout(self.left_layout)
        self.form_layout.addLayout(self.right_layout)

        self.setCentralWidget(self.centralwidget)

    #     qbtn.clicked.connect(self.test)

    # def test(self):
    #     self.right_layout.addWidget(QLabel('NEWWW'),2,0)

#         main_form = QFormLayout()
#         left_widgt = QWidget(None)
#         left_widgt_layout = QVBoxLayout()
#         left_widgt.setLayout(left_widgt_layout)
#         for i in range(5):
#             left_widgt_layout.addWidget(QLabel('标签%i' % i))

#         for w in self.get_left_widgts():
#             left_widgt_layout.addWidget(w)

#         scroll_area = QScrollArea()
#         right_widgt = QWidget(None)
#         self.right_widgt_layout = QVBoxLayout()
#         right_widgt.setLayout(self.right_widgt_layout)
#         self.right_widgt_layout.addWidget(QLabel('标签%i' % 5))
#         self.right_widgt_layout.addWidget(QLabel('标签%i' % 7))
#         scroll_area.setWidget(right_widgt)
        
#         main_form.addRow(left_widgt,scroll_area)

#         main_widgt = QWidget(None)
#         main_widgt.setLayout(main_form)
#         self.setCentralWidget(main_widgt)

    def get_left_widgts(self):
        widgts = []
        self.game_data = get_games()
        mylbl = QLabel('运动项目:')
        mylbl.setMaximumHeight(20)
        widgts.append(mylbl)
        self.game_combo = QComboBox(None)
        self.game_combo.setMaximumWidth(80)
        self.game_combo.setMaximumHeight(20)
        for item in self.game_data.keys():
            self.game_combo.addItem(item)
        widgts.append(self.game_combo)
        self.game_combo.setCurrentIndex(-1)
        self.game_combo.activated[str].connect(self.set_cur_game)
        return widgts

    def set_cur_game(self,game):
        self.game = game
        print(game,self.game_data[game])
        if self.game_data[game] == 1:
            self.show_players(game)

    def get_right_widgets(self):
        players = get_players()
        widgts = []

        for p in players:
            data = [p.name,p.idcode,p.sex,p.age,p.work_place,p.tel]
            data = ['' if d is None else d for d in data]
            info = '{: <8} {: <8} {: <2} {: <2} {: <10} {: <12}'.format(*data)
            widgts.append(QLabel(info))
        return widgts

#     def show_players(self,game):
#         game_sex = get_games_sex()
#         sex = game_sex[game]
#         self.players = get_players(sex)
#         self.p_checkboxes = [QCheckBox(' '.join((p.name,p.idcode))) for p in self.players]
#         for cb in self.p_checkboxes:
#             cb.toggle()
#             print('abc')
#             self.right_widgt_layout.addWidget(cb)
#             cb.show()
#         self.update()



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
                self.add_team_ui()

    def clear_data_firm(self):
        reply = QMessageBox.question(self, '确认', '确定删除数据?',QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            clear_data()

# # QApplication.processEvents()