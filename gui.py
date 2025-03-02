from PyQt5 import QtWidgets
import sys

def window():
    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QMainWindow()
    win.show()
    sys.exit(app.exec_())

window()