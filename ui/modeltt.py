from PyQt5.QtCore import QAbstractTableModel,QModelIndex,QVariant
from PyQt5 import Qt
from models.mydb import TObj,db_session,select

NAME,AGE,TEL = range(3)
COL_NUM = 3

class TObjModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.datas = []

    def load(self):
        self.beginResetModel()
        with db_session:
            tobjs = select(t for t in TObj)
            for tobj in tobjs:
                self.datas.append([tobj.name,tobj.age,tobj.tel])
        self.endResetModel()

    def data(self,index,role=Qt.DisplayRole):
        if (not index.isValid() or not (0 <= index.row() < len(self.datas))):
            return QVariant()

        row,col = index.row(),index.column()
        data = self.datas[row]
        if role = Qt.DisplayRole:
            item = data[col]
            if col == AGE:
                item = int(item)
        return QVariant()

    def rowCount(self,index=QModelIndex()):
        return len(self.datas)

    def columnCount(self,index=QModelIndex()):
        return COL_NUM