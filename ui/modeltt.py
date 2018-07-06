from PyQt5.QtCore import QAbstractTableModel,QModelIndex,QVariant,Qt
from models.mydb import TObj,db_session,select

ID,NAME,AGE,TEL = range(4)
HEADERS = ('id','姓名','年龄','电话')
CONVERTS_FUNS = (None,None,int,None)

class TObjModel(QAbstractTableModel):
    def __init__(self,headers=HEADERS):
        super().__init__()
        self.datas = []
        self.headers = headers
        self.load()

    def load(self):
        # 载入数据函数
        self.beginResetModel()
        with db_session:
            tobjs = select(t for t in TObj)
            for tobj in tobjs:
                self.datas.append([tobj.id,tobj.name,tobj.age,tobj.tel])
        print(self.datas)
        self.endResetModel()

    def data(self,index,role=Qt.DisplayRole):
        # 供视图调用，以获取用以显示的数据
        if (not index.isValid() or not (0 <= index.row() < len(self.datas))):
            return None

        row,col = index.row(),index.column()
        data = self.datas[row]
        if role == Qt.DisplayRole:
            item = data[col]
            if col == AGE:
                item = int(item)
            return item
        return None

    def rowCount(self,index=QModelIndex()):
        return len(self.datas)

    def columnCount(self,index=QModelIndex()):
        return len(self.headers)

    def headerData(self,section,orientation,role=Qt.DisplayRole):
        # 实现标题行的定义
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return self.headers[section]
        return int(section + 1)

    # 以下为编辑功能所必须实现的方法
    def setData(self,index,value,role=Qt.EditRole):
        # 编辑后更新模型中的数据
        if index.isValid() and 0 <= index.row() < len(self.datas) and value:
            col = index.column()
            print(col)
            if 0 < col < len(self.headers):
                self.beginResetModel()
                if CONVERTS_FUNS[col]:
                    self.datas[index.row()][col] = CONVERTS_FUNS[col](value)
                else:
                    self.datas[index.row()][col] = value
                self.dirty = True
                self.endResetModel()
                return True
        return False

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemFlags(
                QAbstractTableModel.flags(self, index)|
                Qt.ItemIsEditable | Qt.ItemIsSelectable)

    def insertRows(self,position,rows=1,index=QModelIndex()):
        # position 插入位置；rows 插入行数
        self.beginInsertRows(QModelIndex(),position,position + rows -1)
        pass #  对self.datas进行操作
        self.endInsertRows()
        self.dirty = True
        return True

    def removeRows(self,position,rows=1,index=QModelIndex):
        # position 删除位置；rows 删除行数
        self.beginRemoveRows(QModelIndex(),position,position + rows -1)
        pass  #  对self.datas进行操作
        self.endRemoveRows()
        self.dirty = True
        return True

    # 可单独定义保存数据的方法（遍历datas进行保存），供用户退出时或选择保存时，保存数据
    # 也可以在用户编辑时立即保存，即在setData方法中保存