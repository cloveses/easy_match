import time
import functools
from models.mydb import Player,PlayGround,Games,Team,Group
from models.gather import add_team2group_db,add_groupdb,get_group_datas,get_team_datas,new_team,get_games,del_rowdb,save_cell,has_data,clear_data,load_data,get_games,get_games_sex,get_players,get_playgrounds
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QScrollArea, QAction,QPushButton,QCheckBox,QComboBox,
                            QVBoxLayout,QHBoxLayout,QScrollArea,QWidget,QLabel,
                            QMainWindow, QTextEdit, QAction, QApplication,QFileDialog,
                            QMessageBox,QGridLayout,QFormLayout,QTableView,QDialog,
                            QLineEdit,QDialogButtonBox)

from PyQt5.QtGui import QStandardItem,QStandardItemModel

class MyQVBoxLayout(QVBoxLayout):
    def maximumSize(self):
        return QtCore.QSize(100,-1)

class Ui_MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.select_checkbox_num = 0
        self.all_widgets = []
        self.game_sub_menus = []
        self.setupUi(self)
        self.updateMenu(self)
        self.retranslateUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(775, 532)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 775, 23))
        self.menubar.setObjectName("menubar")

        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")

        self.menu_team = QtWidgets.QMenu(self.menubar)
        self.menu_team.setObjectName("menu_team")

        MainWindow.setMenuBar(self.menubar)

        mgr_player = QAction(QIcon(),'运动员管理',self)
        mgr_player.triggered.connect(functools.partial(self.edit_player,*self.get_player_parmas()))

        mgr_playground = QAction(QIcon(),'场地管理',self)
        mgr_playground.triggered.connect(functools.partial(self.edit_player,*self.get_playground_parmas()))

        mgr_game = QAction(QIcon(),'竞赛项目',self)
        mgr_game.triggered.connect(functools.partial(self.edit_player,*self.get_game_parmas()))

        mgr_team = QAction(QIcon(),'参赛团队',self)
        mgr_team.triggered.connect(self.edit_team)

        mgr_group = QAction(QIcon(),'分组管理',self)
        mgr_group.triggered.connect(self.edit_group)

        self.toolbar = self.addToolBar('Mytool')
        self.toolbar.addAction(mgr_player)
        self.toolbar.addAction(mgr_playground)
        self.toolbar.addAction(mgr_game)
        self.toolbar.addAction(mgr_team)
        self.toolbar.addAction(mgr_group)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.action_init = QtWidgets.QAction(MainWindow)
        self.action_init.setObjectName("action_init")

        self.action_import_data = QtWidgets.QAction(MainWindow)
        self.action_import_data.setObjectName("action_import_data")

        self.action_gamemgr = QtWidgets.QAction(MainWindow)
        self.action_gamemgr.setObjectName("action_gamemgr")

        self.menu.addAction(self.action_init)
        self.menu.addAction(self.action_import_data)
        self.menu.addSeparator()

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_team.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.action_init.triggered.connect(self.clear_data_firm)
        self.action_import_data.triggered.connect(self.get_data_file)

        self.add_first_ui()

        # if has_data():
        #     self.add_team_ui()
            # time.sleep(2)
            # self.centralwidget.hide()

    # def pr(self):
    #     print('prrrrr')

    def updateMenu(self,MainWindow):
        """添加或更新为每个竞赛项目组队的‘参赛队组建’菜单"""
        self.games = get_games()
        for game_sub_menu in self.game_sub_menus:
            self.menu_team.removeAction(game_sub_menu)
        for game in self.games:
            self.game_sub_menus.append(QtWidgets.QAction(MainWindow))
        for game_sub_menu,game in zip(self.game_sub_menus,self.games):
            game_sub_menu.setObjectName(game.name)
            game_sub_menu.triggered.connect(functools.partial(self.select_player,game.id,game.name,game.team_num,game.sex))
            game_sub_menu.setText(QtCore.QCoreApplication.translate("MainWindow", "&{}".format(game.name)))
        for game_sub_menu in self.game_sub_menus:
            self.menu_team.addAction(game_sub_menu)

    def add_first_ui(self,info="Welcome!"):
        self.takeCentralWidget()
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
        MainWindow.setWindowTitle(_translate("MainWindow", "易用竞赛管理系统"))
        self.menu.setTitle(_translate("MainWindow", "&管理数据"))
        self.action_init.setText(_translate("MainWindow", "&清理数据"))
        self.action_import_data.setText(_translate("MainWindow", "&导入数据"))

        self.menu_team.setTitle(_translate("MainWindow", "&参赛队组建"))

    def get_data_file(self):
        fname = QFileDialog.getOpenFileName(self, '打开文件', '.\\')
        if fname[0]:
            info = load_data(fname[0])
            if info:
                QMessageBox.information(self,"数据错误,请修改后重新导入！",info)
            else:
                QMessageBox.information(self,"提示：",'数据导入成功！')
                self.add_first_ui('数据已导入！')
                # self.add_team_ui()
                self.updateMenu(self)

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

    def get_game_parmas(self):
        head_lst = ['索引号','竞赛项目','队员人数','队员性别','备注']
        keys = ['id','name','team_num','sex','memo']
        return get_games,keys,head_lst,Games

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
        if obj == Games and 'name' in param:
            self.updateMenu(self)

    def del_row(self,obj):
        reply = QMessageBox.question(self, '确认', '确定删除数据?',QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            r = self.player_tabview.currentIndex().row()
            item = self.player_model.index(r,0)
            # print(int(item.data()))
            del_rowdb(obj,int(item.data()))
            self.player_model.removeRow(r)
            if obj == Games:
                self.updateMenu(self)

    def edit_team(self):
        datas = get_team_datas()
        head_lst = ['索引号','队名','项目','分组']
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
            # edit_cell = functools.partial(self.edit_cell,obj,keys)
            # self.player_model.itemChanged.connect(edit_cell)

            self.player_tabview.setModel(self.player_model)


            boxlayout = QVBoxLayout()
            # boxlayout.addStretch(1)
            boxlayout.addWidget(self.player_tabview,18)
            # boxlayout.addStretch(1)

            del_btn = QPushButton('删除')
            del_btn.clicked.connect(self.del_team)
            boxlayout.addWidget(del_btn)

            main_frame.setLayout(boxlayout)
            self.setCentralWidget(main_frame)

    def del_team(self):
        # v = MyDialog()
        # if v.exec_():
        #     name,game = v.get_data()
        #     print(name,game)
        reply = QMessageBox.question(self, '确认', '确定删除数据?',QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            r = self.player_tabview.currentIndex().row()
            item = self.player_model.index(r,0)
            # print(int(item.data()))
            del_rowdb(Team,int(item.data()))
            self.player_model.removeRow(r)

    def select_player(self,gid,gname,gteam_num,gsex):
        # 新建团队UI
        players = get_players(gsex)
        head_lst = ['索引号','姓名','身份证号','性别','年龄','工作单位','电话']
        keys = ['id','name','idcode','sex','age','work_place','tel']
        datas =  []
        for player in players:
            data = [getattr(player,key) for key in keys]
            data = ['' if d is None else d for d in data]
            datas.append(data)
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
            self.player_tabview.setModel(self.player_model)

            boxlayout = QVBoxLayout()
            # boxlayout.addStretch(1)
            boxlayout.addWidget(self.player_tabview,18)
            # boxlayout.addStretch(1)

            new_btn = QPushButton('新建团队({})'.format(gname))
            new_btn.clicked.connect(functools.partial(self.add_team,gid,gteam_num,gsex))
            boxlayout.addWidget(new_btn)

            main_frame.setLayout(boxlayout)
            self.setCentralWidget(main_frame)

    def add_team(self,gid,gteam_num,gsex):
        # 新建团队方法
        rows = set()
        pids = []
        for selected_model_index in self.player_tabview.selectedIndexes():
            rows.add(selected_model_index.row())
        for r in rows:
            item = self.player_model.index(r,0)
            pids.append(item.data())
        if gteam_num == 1:
            info = new_team(gid,pids,flag=1)
            if info:
                QMessageBox.warning(self,'完成',info,QMessageBox.Ok)
            else:
                QMessageBox.information(self,'完成','成功建立！',QMessageBox.Ok)
        if gteam_num > 1:
            if len(rows) == gteam_num:
                info = new_team(gid,pids)
                if info:
                    QMessageBox.warning(self,'完成',info,QMessageBox.Ok)
                else:
                    QMessageBox.information(self,'完成','成功建立！',QMessageBox.Ok)
            else:
                QMessageBox.warning(self,'错误','请选中指定的运动员数：{}'.format(gteam_num),QMessageBox.Ok)
        self.player_tabview.clearSelection()

    def edit_group(self):
        datas = get_group_datas()
        head_lst = ['索引号','组名','项目','所含队名','gameid']
        self.takeCentralWidget()
        main_frame = QScrollArea(self)
        main_frame.setStyleSheet('QWidget{background-color:rgb(255,255,255)}')

        self.player_tabview = QTableView()
        self.player_model = QStandardItemModel()
        self.player_model.setHorizontalHeaderLabels(head_lst)
        if datas:
            r,c = len(datas),len(datas[0])
            # self.player_model = QStandardItemModel(r,c)
            self.player_model.setHorizontalHeaderLabels(head_lst)
            for r,rdata in enumerate(datas):
                for c,cell in enumerate(rdata):
                    it = QStandardItem(str(cell))
                    # if c == 0:
                    it.setEditable(False)
                    self.player_model.setItem(r,c,it)
        # keys = ['id','name','idcode','sex','age','work_place','tel']
        # edit_cell = functools.partial(self.edit_cell,obj,keys)
        # self.player_model.itemChanged.connect(edit_cell)

        self.player_tabview.setModel(self.player_model)


        boxlayout = QVBoxLayout()
        # boxlayout.addStretch(1)
        boxlayout.addWidget(self.player_tabview,18)
        # boxlayout.addStretch(1)
        self.player_tabview.hideColumn(4)

        add_btn = QPushButton('添加分组')
        add_btn.clicked.connect(self.add_group)
        boxlayout.addWidget(add_btn)

        del_btn = QPushButton('删除分组')
        del_btn.clicked.connect(functools.partial(self.del_row,Group))
        boxlayout.addWidget(del_btn)

        add_team_btn = QPushButton('分配参赛团队')
        add_team_btn.clicked.connect(self.add_team2group)
        boxlayout.addWidget(add_team_btn)

        main_frame.setLayout(boxlayout)
        self.setCentralWidget(main_frame)

    def add_group(self):
        v = MyDialog()
        if v.exec_():
            name,game = v.get_data()
            if name and game:
                info = add_groupdb(name,int(game))
                if info:
                    QMessageBox.warning(self,'错误',info,QMessageBox.Ok)
                else:
                    QMessageBox.information(self,'完成','成功建立！',QMessageBox.Ok)
                    self.edit_group()

    def add_team2group(self):
        rows = set()

        for selected_model_index in self.player_tabview.selectedIndexes():
            rows.add(selected_model_index.row())
        if len(rows) != 1:
            QMessageBox.warning(self,'错误','请仅选择其中一个小组',QMessageBox.Ok)
            return
        row = rows.pop()
        groupid = self.player_model.index(row,0).data()
        gameid = self.player_model.index(row,4).data()

        print(groupid,gameid)

        v = GroupDialog(gameid)
        if v.exec_():
            tids = v.get_data()
            print(tids)
            if tids:
                add_team2group_db(groupid,tids)

# # QApplication.processEvents()

class MyDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
        # self.exec()

    def initUI(self):
        self.setWindowTitle("新建小组")
        self.setGeometry(400,400,200,200)

        self.lab_a = QLabel('小组名称:')
        self.lab_b = QLabel('竞赛项目:')

        self.name_edit = QLineEdit()
        self.game_item = QComboBox()

        for g in get_games():
            self.game_item.addItem(g.name,g.id)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.glayout = QGridLayout()

        self.glayout.addWidget(self.lab_a,0,0)
        self.glayout.addWidget(self.lab_b,1,0)
        self.glayout.addWidget(self.name_edit,0,1)
        self.glayout.addWidget(self.game_item,1,1)

        self.glayout.addWidget(self.buttons,2,1)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.setLayout(self.glayout)

    def get_data(self):
        return self.name_edit.text(),self.game_item.itemData(self.game_item.currentIndex())

class GroupDialog(QDialog):
    def __init__(self,gameid):
        super().__init__()
        self.gameid = gameid
        self.initUI()
        # self.exec()

    def initUI(self):
        self.setWindowTitle("添加团队到小组")
        self.setGeometry(400,400,500,300)

        self.tv = QTableView()
        head_lst = ['索引号','队名','项目','分组']
        datas = get_team_datas(self.gameid)
        self.mdl = QStandardItemModel()
        if datas:
            r,c = len(datas),len(datas[0])
            self.mdl = QStandardItemModel(r,c)
            self.mdl.setHorizontalHeaderLabels(head_lst)
            for r,rdata in enumerate(datas):
                for c,cell in enumerate(rdata):
                    it = QStandardItem(str(cell))
                    it.setEditable(False)
                    self.mdl.setItem(r,c,it)
            self.tv.setModel(self.mdl)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.glayout = QVBoxLayout()
        self.glayout.addWidget(self.tv)
        self.glayout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.setLayout(self.glayout)

    def get_data(self):
        rows = set()
        tids = []
        for selected_model_index in self.tv.selectedIndexes():
            rows.add(selected_model_index.row())
        for r in rows:
            item = self.mdl.index(r,0)
            tids.append(item.data())
        return tids
