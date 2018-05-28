import sys
import pony.orm.dbproviders.sqlite
from models.mydb import *
from ui.ui import Ui_MainWindow,QApplication

app = QApplication(sys.argv)
ex = Ui_MainWindow()
ex.show()
sys.exit(app.exec_())