from PyQt5 import QtWidgets, uic, QtCore, QtGui
import sys
import os
import time
from kb_gen import kbArticleGenerator

#Pages
class welcomeScreen(QtWidgets.QDialog):
    def __init__(self):
        super(welcomeScreen, self).__init__()
        self.setWindowIcon(QtGui.QIcon('NXTKB.png'))
        uic.loadUi("welcomeScreen.ui", self)
        self.button.clicked.connect(self.gotoscreen2)

    def gotoscreen2(self):
        widget.setCurrentIndex(widget.currentIndex()+1)

class fileSelectionScreen(QtWidgets.QDialog):
    def __init__(self):
        super(fileSelectionScreen, self).__init__()
        uic.loadUi("fileSelectionScreen.ui", self)

        self.waiting.hide()
        self.emptyOutputError.hide()
        self.emptyInputError.hide()
        self.button.setEnabled(True)


        self.inputBrowse.clicked.connect(self.browseInputFile)
        self.outputBrowse.clicked.connect(self.browseOutputFile)
        self.button.clicked.connect(self.input_validation)
        #self.button.clicked.connect(self.goToFinished)

    def browseInputFile(self):
        desktop_path = os.path.expanduser('~') + '/Desktop/'
        input_file = QtWidgets.QFileDialog.getOpenFileName(self, 'Open input file', desktop_path, 'XML files (*.xml)')
        #self.input_path = input_file[0]
        self.inputFilePath.setText(input_file[0])
        

    def browseOutputFile(self):
        desktop_path = os.path.expanduser('~') + '/Desktop/'
        output_file = QtWidgets.QFileDialog.getSaveFileName(self, 'Choose output location', desktop_path, 'JSON files (*.json)')
        #self.output_path = output_file[0]
        self.outputFilePath.setText(output_file[0])

    def input_validation(self):
        if not self.outputFilePath.text():
            self.emptyOutputError.show()
        else:
            self.emptyOutputError.hide()
        
        if not self.inputFilePath.text():
            self.emptyInputError.show()
        else:
            self.emptyInputError.hide()
        
        if self.inputFilePath.text() and self.outputFilePath.text():
            self.kbGenerate(self.inputFilePath.text(), self.outputFilePath.text())
            #self.goToFinished()

    def kbGenerate(self, input, output):
        self.waiting.show()
        self.button.setEnabled(False)
        
        self.thread = QtCore.QThread()
        self.worker = Worker(input, output)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()
        
        self.thread.finished.connect(self.goToFinished)
        

    def goToFinished(self):
        self.button.setEnabled(True)
        self.waiting.hide()
        self.inputFilePath.clear()
        self.outputFilePath.clear()
        widget.setCurrentIndex(widget.currentIndex()+1)

class Finished(QtWidgets.QDialog):
    def __init__(self):
        super(Finished, self).__init__()
        uic.loadUi('finished.ui', self)
        
        self.exit_button.clicked.connect(self.close_window)
        self.back_button.clicked.connect(self.backToFileSelection)

    def close_window(self):
        for i in range(widget.count()):
            widget.close()

    def backToFileSelection(self):
        widget.setCurrentIndex(widget.currentIndex()-1)

#Worker class to run the KB article generation logic
class Worker(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    
    def __init__(self, input_file, output_file):
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file
    
    def run(self):
        kbArticleGenerator(self.input_file, self.output_file)
        time.sleep(5)
        self.finished.emit()

#Starting the program
app = QtWidgets.QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()

welcome_screen = welcomeScreen()
file_selection_screen = fileSelectionScreen()
finished = Finished()

widget.addWidget(welcome_screen)
widget.addWidget(file_selection_screen)
widget.addWidget(finished)

widget.setFixedHeight(500)
widget.setFixedWidth(500)

widget.setWindowIcon(QtGui.QIcon('NXTKB.ico'))
widget.setWindowTitle('NXTKB')

widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")