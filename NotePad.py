import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QFontDialog, QColorDialog
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from PyQt6.QtCore import QFileInfo, Qt
from PyQt6.QtGui import QFont
from MainWindow.MainWindowUI import Ui_Notepad


class NotepadMain(QMainWindow, Ui_Notepad):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.actionSave.triggered.connect(self.save_file)
        self.actionNew.triggered.connect(self.new_file)
        self.actionOpen.triggered.connect(self.open_file)
        self.actionPrint.triggered.connect(self.print_file)
        self.actionPrint_Preview.triggered.connect(self.preview_dialog)
        self.actionExport_PDF.triggered.connect(self.export_pdf)
        self.actionQuit.triggered.connect(self.exit_app)

        self.actionRedo.triggered.connect(self.textEdit.redo)
        self.actionUndo.triggered.connect(self.textEdit.undo)
        self.actionCopy.triggered.connect(self.textEdit.copy)
        self.actionCut.triggered.connect(self.textEdit.cut)
        self.actionPaste.triggered.connect(self.textEdit.paste)

        self.actionBold.triggered.connect(self.set_bold)
        self.actionItalic.triggered.connect(self.set_italic)
        self.actionUnderLine.triggered.connect(self.set_underline)

        self.actionLeft.triggered.connect(self.left)
        self.actionRight.triggered.connect(self.right)
        self.actionCenter.triggered.connect(self.center)
        self.actionJustify.triggered.connect(self.justify)

        self.actionColor.triggered.connect(self.set_color)
        self.actionFont.triggered.connect(self.set_font)

        self.actionAbout_Us.triggered.connect(self.about_us)


    def save_file(self):
        filename = QFileDialog.getSaveFileName(self, 'Save File')
        if filename[0]:
            with open(filename[0], 'w') as file:
                text = self.textEdit.toPlainText()
                file.write(text)
                QMessageBox.about(self, 'Save File', 'file saved !')
    
    def maybe_save(self):
        if self.textEdit.toPlainText() == '':
            return True
        quesiton = QMessageBox.question(self, 'Warning', 'You didn\'t save the file\nAre you sure to leave?',
                                        QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
        if quesiton == QMessageBox.StandardButton.Cancel :
            return
        elif quesiton == QMessageBox.StandardButton.Save:
            self.save_file()
        else :
            return True
    
    def new_file(self):
        if self.maybe_save():
            self.textEdit.clear()


    def open_file(self):
        if not self.maybe_save():
            return False
        file_name = QFileDialog.getOpenFileName(self, 'Open File')
        if file_name[0]:
            with open(file_name[0], 'r') as file:
                self.textEdit.setText(file.read())

    def print_file(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        dialog = QPrintDialog(printer)
        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            self.textEdit.print(printer)

    def preview_dialog(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        dialog = QPrintPreviewDialog(printer, self)
        dialog.paintRequested.connect(self.preview_file)
        dialog.exec()
    
    def preview_file(self, printer):
        self.textEdit.print(printer)


    def export_pdf(self):
        filename = QFileDialog.getSaveFileName(self, 'Export PDF', 'output.pdf')
        filename = filename[0]
        if filename:
            if QFileInfo(filename).suffix() == '':
                filename += '.pdf'
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(filename)
            self.textEdit.document().print(printer)

    def set_bold(self):
        font = QFont()
        font.setBold(True)
        self.textEdit.setFont(font)

    def set_italic(self):
        font = QFont()
        font.setItalic(True)
        self.textEdit.setFont(font)
        
    def set_underline(self):
        font = QFont()
        font.setUnderline(True)
        self.textEdit.setFont(font)

    def left(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignLeft)
    
    def right(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignRight)

    def center(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def justify(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignJustify)
    
    def set_font(self):
        font, ok = QFontDialog.getFont()
        if ok and font:
            self.textEdit.setFont(font)

    def set_color(self):
        color = QColorDialog.getColor()
        if color:
            self.textEdit.setTextColor(color)


    def about_us(self):
        msgbox = QMessageBox.information(self, 'About us', 'This is an open source program, You can see it on github :\nhttps://github.com/eleguns/PyQt6-tools')
    
    def exit_app(self):
        if self.textEdit.toPlainText() == '':
            self.close()
        else :
            quesiton = QMessageBox.question(self, 'Warning', 'You didn\'t save the file\nAre you sure to leave?',
                                            QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
            if quesiton == QMessageBox.StandardButton.Cancel :
                return
            elif quesiton == QMessageBox.StandardButton.Save:
                self.save_file()
            else :
                self.close()










if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = NotepadMain()
    sys.exit(app.exec())