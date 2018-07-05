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
        self.beginResetModel()
        with db_session:
            tobjs = select(t for t in TObj)
            for tobj in tobjs:
                self.datas.append([tobj.id,tobj.name,tobj.age,tobj.tel])
        print(self.datas)
        self.endResetModel()

    def data(self,index,role=Qt.DisplayRole):
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
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return self.headers[section]
        return int(section + 1)


    def setData(self,index,value,role=Qt.EditRole):

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
                self.dataChanged[QModelIndex,].emit(index,)
                self.endResetModel()
                return True
        return False

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemFlags(
                QAbstractTableModel.flags(self, index)|
                Qt.ItemIsEditable | Qt.ItemIsSelectable)