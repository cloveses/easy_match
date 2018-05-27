import sys
from models.mydb import *
from ui.ui import Ui_MainWindow,QApplication

app = QApplication(sys.argv)
ex = Ui_MainWindow()
sys.exit(app.exec_())