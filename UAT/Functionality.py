# run below in cmd in the .ui folder to create a .py file
#  Classes\Version 2>C:\Users\jamie.kapilivsky\AppData\Local\Continuum\Anaconda3\Library\bin\pyuic5.bat -x pyqtdesignerV2.ui -o UI.py

# Designer folder
# C:\Users\jamie.kapilivsky\AppData\Roaming\Python\Python36\site-packages\pyqt5-tools

import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pandas as pd

from Threads import Threaded
from UI import Ui_MainWindow

class Window(QMainWindow):
    requestPage = pyqtSignal(str, str, str, str)

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.threading()
        self.btn_functionality()
        self.nav_functionality()
        self.MainWindow.show()


    def update_textedit(self, html):
        self.ui.textEdit.textCursor().insertHtml(html)

    def update_progressbar(self, percentage):
        self.ui.progressBar.setValue(percentage * 100)

    def threading(self):
        self._thread=QThread()
        self._threaded=Threaded(self.update_textedit, self.update_progressbar, result=self.display_page)

        self.requestPage.connect(self._threaded.get_info)

        self._thread.started.connect(self._threaded.start)
        self._threaded.moveToThread(self._thread)
        qApp.aboutToQuit.connect(self._thread.quit)
        self._thread.start()


    def nav_functionality(self):
        # TODO - Where to save this file?
        self.ui.actionNew.triggered.connect(self.new_project)
        self.ui.actionOpen.triggered.connect(self.file_path)
        self.ui.actionSave.triggered.connect(self.file_save)
        self.ui.actionQuit.triggered.connect(lambda: QApplication.quit())

        self.ui.actionFAQ.triggered.connect(self.project_FAQ)
        self.ui.actionAbout.triggered.connect(self.project_about)

    def new_project(self):
        self.ui.textEdit.setText('')
        self.ui.progressBar.setValue(0)
        self.ui.label_excel_name.setText('Excel file')
        self.ui.label_tab_name.setText('Tab name')
        self.file_path()

    def project_FAQ(self):
        faq_file = open('txt_files/FAQ.txt', 'r')
        faq = faq_file.read()
        self.ui.textEdit.setText(faq)

    def project_about(self):
        about_file = open('txt_files/About.txt', 'r')
        about = about_file.read()
        self.ui.textEdit.setText(about)

    def btn_functionality(self):
        self.MainWindow = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

        self.ui.pushButton_Run.clicked.connect(self.get_comboBox_info)
        self.ui.pushButton_Clear.clicked.connect(self.clear_texteditbox)
        self.ui.pushButton_Save.clicked.connect(self.file_save)


    def file_path(self):
        path = QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'),
                                           'Excel(*.xlsx);;csv(*.csv);;All Files(*.*)')
        # TODO - need ability to return a CSV as well, need to accept it in the script as well!

        csv = False
        excel = False

        if path[0][-5:] == '.xlsx':
            excel = True
        elif path[0][-4:] == '.csv':
            csv = True

        if path[0] == "":  # Needs a space... -.-
            return "Missing"
        if csv:
            df_new = pd.read_csv(path[0])
            writer = pd.ExcelWriter('temp.xlsx')
            df_new.to_excel(writer, 'Sheet1', index=False)
            writer.save()
            self.ui.label_excel_name.setText(path[0])
            return 'temp.xlsx'
        elif excel:
            self.ui.label_excel_name.setText(path[0])
            return path[0]

    def file_save(self):
        name = QFileDialog.getSaveFileName(self, 'Save File', os.getenv('HOME'),
                                           'Text file(*.txt)')
        file = open(name[0], 'w')
        text = self.ui.textEdit.toPlainText()
        file.write(text)
        file.close()


    @pyqtSlot()
    def get_comboBox_info(self):
        if self.ui.label_excel_name.text() == "Excel file":
            file_path = self.file_path()
            if file_path == 'Missing':
                self.ui.textEdit.setText('WARNING: Must use a CSV or Excel file.')
                return
        else:
            # Makes sure to use the temp excel file if the user selected a CSV
            if self.ui.label_excel_name.text()[-4:] == '.csv':
                file_path = 'temp.xlsx'
            else:
                # Used if a file location has already been selected!
                file_path = self.ui.label_excel_name.text()

        # Get combobox values
        self.script_select = self.ui.comboBox_program.currentText()
        self.country_select = self.ui.comboBox_country.currentText()
        self.modheader_select = self.ui.comboBox_modheader.currentText()

        # Emit all values to slot
        self.requestPage.emit(file_path, self.script_select, self.country_select, self.modheader_select)

        # Disable button functions
        self.ui.pushButton_Run.setEnabled(False)
        self.ui.pushButton_Clear.setEnabled(False)
        self.ui.pushButton_Save.setEnabled(False)

        # Disable nav bar during Run
        self.ui.actionAbout.setEnabled(False)
        self.ui.actionFAQ.setEnabled(False)
        self.ui.actionNew.setEnabled(False)
        self.ui.actionOpen.setEnabled(False)
        self.ui.actionQuit.setEnabled(False)
        self.ui.actionSave.setEnabled(False)

        self.ui.progressBar.setValue(0)


    @pyqtSlot(object)
    def display_page(self, df):
        global final_df
        self.ui.pushButton_Run.setEnabled(True)
        self.ui.pushButton_Clear.setEnabled(True)
        self.ui.pushButton_Save.setEnabled(True)

        self.ui.actionAbout.setEnabled(True)
        self.ui.actionFAQ.setEnabled(True)
        self.ui.actionNew.setEnabled(True)
        self.ui.actionOpen.setEnabled(True)
        self.ui.actionQuit.setEnabled(True)
        self.ui.actionSave.setEnabled(True)

        final_df = df


    def clear_texteditbox(self):
        self.ui.textEdit.setText('')
        self.ui.progressBar.setValue(0)


# try:
#     os.remove(filename)
# except OSError:
#     pass
