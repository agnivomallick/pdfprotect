from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import sys
from PyQt5.QtCore import QUrl
from pypdf import PdfReader, PdfWriter


class MainWin(QMainWindow):
    def __init__(self):
        super(MainWin, self).__init__()
        loadUi("protector.ui", self)
        self.chooseFile.clicked.connect(self.fileChooser)
        self.protectpdf.clicked.connect(self.pdfProtect)
        self.saveto.clicked.connect(self.saveToFile)

    def fileChooser(self):
        global path_chooseFile
        path_chooseFile, _ = QFileDialog.getOpenFileName(self, "Choose File", "C:", "PDF Files (*.pdf)")
        if path_chooseFile == '':
            return
        
        url = QUrl.fromLocalFile(path_chooseFile)

        fileurl = url.url()
        
        strip_url = fileurl.replace("file:///", '')

        global slash_change
        slash_change = strip_url.replace("/", "\\")

        self.chosenFile.setText(slash_change)
        self.chosenFile.adjustSize()

        print(fileurl)
        print(strip_url)

    def saveToFile(self):
        global path_savefile
        path_savefile, _ = QFileDialog.getSaveFileName(self, "Save Encrypted File", "C:", "PDF Files (*.pdf)")
        if path_savefile == '':
            return
        
        url = QUrl.fromLocalFile(path_savefile)

        fileurl = url.url()
        
        strip_url = fileurl.replace("file:///", '')

        global slash_change_savefile
        slash_change_savefile = strip_url.replace("/", "\\")

        self.savingFile.setText(slash_change_savefile)
        self.savingFile.adjustSize()

    def pdfProtect(self):
        if path_savefile == '':
            errorbox = QMessageBox(self)
            errorbox.setIcon(QMessageBox.Critical)
            errorbox.setWindowTitle("Error")
            errorbox.setText("This error was found:")
            errorbox.setDetailedText("There is no file chosen in \'Save To File\' field.")
            show = errorbox.exec_()

        elif path_chooseFile == '':
            errorbox = QMessageBox(self)
            errorbox.setIcon(QMessageBox.Critical)
            errorbox.setWindowTitle("Error")
            errorbox.setText("This error was found:")
            errorbox.setDetailedText("There is no file chosen in \'Choose File\' field.")
            show = errorbox.exec_()

        elif self.password.text() == '':
            errorbox = QMessageBox(self)
            errorbox.setIcon(QMessageBox.Critical)
            errorbox.setWindowTitle("Error")
            errorbox.setText("This error was found:")
            errorbox.setDetailedText("There is no password specified.")
            show = errorbox.exec_()
            
        else:
           reader = PdfReader(slash_change)
           writer = PdfWriter()
   
           for page in reader.pages:
               writer.add_page(page)
           
           writer.encrypt(self.password.text(), algorithm="AES-256")
   
           with open(slash_change_savefile, "wb") as f:
               writer.write(f)

           msgbox = QMessageBox(self)
           msgbox.setIcon(QMessageBox.Information)
           msgbox.setWindowTitle("Encrypted File")
           msgbox.setText("The new file %s has been password protected." % slash_change_savefile)
           show = msgbox.exec_()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    win = MainWin()
    win.show()

    app.exec_()