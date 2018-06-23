import time
import functools
from models.mydb import Player,PlayGround
from models.gather import del_rowdb,save_cell,has_data,clear_data,load_data,get_games,get_games_sex,get_players,get_playgrounds
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QScrollArea, QAction,QPushButton,QCheckBox,QComboBox,
                            QVBoxLayout,QHBoxLayout,QScrollArea,QWidget,QLabel,
                            QMainWindow, QTextEdit, QAction, QApplication,QFileDialog,
                            QMessageBox,QGridLayout,QFormLayout,QTableView)

from PyQt5.QtGui import QStandardItem,QStandardItemModel

class MyQVBoxLayout(QVBoxLayout):
    def maximumSize(self):
        return QtCore.QSize(100,-1)

class Ui_MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.select_checkbox_num = 0
        self.all_widgets = []
        self.setupUi(self)
        self.retranslateUi(self)


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(775, 532)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 775, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)

        mgr_player = QAction(QIcon(),'运动员管理',self)
        mgr_player.triggered.connect(functools.partial(self.edit_player,*self.get_player_parmas()))

        mgr_playground = QAction(QIcon(),'场地管理',self)
        mgr_playground.triggered.connect(functools.partial(self.edit_player,*self.get_playground_parmas()))

        self.toolbar = self.addToolBar('Mytool')
        self.toolbar.addAction(mgr_player)
        self.toolbar.addAction(mgr_playground)

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

        self.add_first_ui()

        # if has_data():
        #     self.add_team_ui()
            # time.sleep(2)
            # self.centralwidget.hide()

    def add_first_ui(self,info="Welcome!"):
        self.main_frame = QScrollArea(self)
        self.main_frame.setStyleSheet('QWidget{background-color:rgb(255,255,255)}')
        self.wel = QLabel(info)

        boxlayout = QHBoxLayout()
        boxlayout.addStretch()
        boxlayout.addWidget(self.wel)
        boxlayout.addStretch()

        self.main_frame.setLayout(boxlayout)
        self.setCentralWidget(self.main_frame)

    def add_team_ui(self):
        self.centralwidget = QWidget()
        self.form_layout = QHBoxLayout(self.centralwidget)

        self.left_layout = MyQVBoxLayout()
        self.right_layout = QVBoxLayout()

        # qbtn = QPushButton('1')
        # qbtn.resize(qbtn.minimumSize())
        self.left_widgts = self.get_left_widgts()
        # self.left_layout.addWidget(qbtn)
        # self.left_layout.addWidget(QLabel('def'))
        for widgt in self.left_widgts:
            self.left_layout.addWidget(widgt)
        self.left_layout.addStretch()
        # self.right_layout.addWidget(QLabel('aaaa'),0,0)
        # self.right_layout.addWidget(QLabel('bbbb'),1,0)
        self.right_widgts = self.get_right_widgets()
        for widgt in self.right_widgts:
            self.right_layout.addWidget(widgt)
        self.right_layout.addStretch()
        self.form_layout.addLayout(self.left_layout)
        self.form_layout.addLayout(self.right_layout)

        self.setCentralWidget(self.centralwidget)


    #     qbtn.clicked.connect(self.test)

    def test(self):
        centralwidget = QWidget()
        test_layout = QHBoxLayout(centralwidget)
        test_layout.addWidget(QLabel('kkkkkkkkkkkkkkkkkkk'))
        # self.removeWidget(self.centralwidget)
        self.takeCentralWidget()
        self.setCentralWidget(centralwidget)
        # self.show()
        # self.update()
        # self.repaint()

    def test_tool(self):
        print('abccc')
        self.wel.setText('akkkkkkkkkkkk!')
        self.takeCentralWidget()
        self.setCentralWidget(QLabel('kkkdkddaaaaaaaaaaaaaa'))


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

    def show_players(self,game):
        self.test()

        game_sex = get_games_sex()
        sex = game_sex[game]
        self.players = get_players(sex)
        self.p_checkboxes = [QCheckBox(' '.join((p.name,p.idcode))) for p in self.players]
        for w in self.right_widgts:
            w.hide()
        for cb in self.p_checkboxes:
            cb.toggle()
            print('abc')
            self.right_layout.addWidget(cb)
        self.right_layout.addStretch()


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
                # self.add_team_ui()

    def clear_data_firm(self):
        reply = QMessageBox.question(self, '确认', '确定删除数据?',QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        self.takeCentralWidget()
        if reply == QMessageBox.Yes:
            clear_data()
            self.add_first_ui('数据已全部清空！')

    def get_player_parmas(self):
        head_lst = ['索引号','姓名','身份证号','性别','年龄','工作单位','电话']
        keys = ['id','name','idcode','sex','age','work_place','tel']
        return get_players,keys,head_lst,Player

    def get_playground_parmas(self):
        head_lst = ['索引号','场地名','使用状态','备注']
        keys = ['id','name','using','memo']
        return get_playgrounds,keys,head_lst,PlayGround

    def edit_player(self,getfunc,keys,head_lst,obj):
        model_objs = getfunc()
        datas = []
        for model_obj in model_objs:
            # data = [p.id,p.name,p.idcode,p.sex,p.age,p.work_place,p.tel]
            data = [getattr(model_obj,key) for key in keys]
            data = ['' if d is None else d for d in data]
            datas.append(data)
        # head_lst = ['索引号','姓名','身份证号','性别','年龄','工作单位','电话']
        if datas:
            self.takeCentralWidget()
            main_frame = QScrollArea(self)
            main_frame.setStyleSheet('QWidget{background-color:rgb(255,255,255)}')

            self.player_tabview = QTableView()
            r,c = len(datas),len(datas[0])
            self.player_model = QStandardItemModel(r,c)
            self.player_model.setHorizontalHeaderLabels(head_lst)
            for r,rdata in enumerate(datas):
                for c,cell in enumerate(rdata):
                    it = QStandardItem(str(cell))
                    if c == 0:
                        it.setEditable(False)
                    self.player_model.setItem(r,c,it)
            # keys = ['id','name','idcode','sex','age','work_place','tel']
            edit_cell = functools.partial(self.edit_cell,obj,keys)
            self.player_model.itemChanged.connect(edit_cell)

            self.player_tabview.setModel(self.player_model)


            boxlayout = QVBoxLayout()
            # boxlayout.addStretch(1)
            boxlayout.addWidget(self.player_tabview,18)
            # boxlayout.addStretch(1)

            del_btn = QPushButton('删除')
            del_btn.clicked.connect(functools.partial(self.del_row,obj))
            boxlayout.addWidget(del_btn)

            main_frame.setLayout(boxlayout)
            self.setCentralWidget(main_frame)

    def edit_cell(self,obj,keys):
        r = self.player_tabview.currentIndex().row()
        c = self.player_tabview.currentIndex().column()
        curr_data = self.player_tabview.currentIndex().data()
        item = self.player_model.index(r,0)
        param = dict()
        param[keys[c]] = curr_data
        save_cell(obj,int(item.data()),param)

    def del_row(self,obj):
        reply = QMessageBox.question(self, '确认', '确定删除数据?',QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            r = self.player_tabview.currentIndex().row()
            item = self.player_model.index(r,0)
            print(int(item.data()))
            del_rowdb(obj,int(item.data()))
            self.player_model.removeRow(r)

# # QApplication.processEvents()