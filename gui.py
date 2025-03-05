from PyQt5 import QtWidgets, QtGui, uic
import sys
import os
import kb_gen

input_path = ''
output_path = ''

class MainWindow(QtWidgets.QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("screen1.ui", self)
        self.button.clicked.connect(self.gotoscreen2)

    def gotoscreen2(self):
        widget.setCurrentIndex(widget.currentIndex()+1)

class Screen2(QtWidgets.QDialog):
    def __init__(self):
        super(Screen2, self).__init__()
        uic.loadUi("screen2.ui", self)

        self.x = LoadingScreen()

        self.inputBrowse.clicked.connect(self.browseInputFile)
        self.outputBrowse.clicked.connect(self.browseOutputFile)
        self.button.clicked.connect(self.gotoloading)

    def browseInputFile(self):
        desktop_path = os.path.expanduser('~') + '/Desktop/'
        input_file = QtWidgets.QFileDialog.getOpenFileName(self, 'Open input file', desktop_path, 'Text files (*.txt)')
        self.x.input_path = input_file[0]
        self.inputFilePath.setText(input_file[0])
        

    def browseOutputFile(self):
        desktop_path = os.path.expanduser('~') + '/Desktop/'
        output_file = QtWidgets.QFileDialog.getSaveFileName(self, 'Choose output location', desktop_path, 'Text files (*.txt)')
        self.x.output_path = output_file[0]
        self.outputFilePath.setText(output_file[0])

    def gotoloading(self):
        widget.setCurrentIndex(widget.currentIndex()+1)
        self.x.kbGenerate()

class LoadingScreen(QtWidgets.QDialog):
    def __init__(self):
        super(LoadingScreen, self).__init__()
        uic.loadUi('loading.ui', self)
        self.input_path = ""
        self.output_path = ""
    
    def kbGenerate(self):
        if kb_gen.kbArticleGenerator(self.input_path, self.output_path):
            widget.setCurrentIndex(widget.currentIndex()+1)

class Finished(QtWidgets.QDialog):
    def __init__(self):
        super(Finished, self).__init__()
        uic.loadUi('finished.ui', self)
        self.exit_button.clicked.connect(self.close)
        


app = QtWidgets.QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()

mainwindow = MainWindow()
screen2 = Screen2()
#loading_screen = LoadingScreen()
finished = Finished()

widget.addWidget(mainwindow)
widget.addWidget(screen2)
#widget.addWidget(loading_screen)
widget.addWidget(finished)

widget.setFixedHeight(500)
widget.setFixedWidth(500)

widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")