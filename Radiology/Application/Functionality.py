# run below in cmd in the .ui folder to create a .py file
#  Classes\Version 2>C:\Users\jamie.kapilivsky\AppData\Local\Continuum\Anaconda3\Library\bin\pyuic5.bat -x pyqtdesignerV2.ui -o UI.py

# Designer folder
# C:\Users\jamie.kapilivsky\AppData\Roaming\Python\Python36\site-packages\pyqt5-tools

import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pandas as pd
import datetime
import subprocess

from Threads import Threaded
from UI import Ui_MainWindow


class Window(QMainWindow):
    requestDoc = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.threading()
        self.btn_functionality()
        self.nav_functionality()

        self.MainWindow.show()

    def update_progressbar(self, percentage):
        self.ui.progressBar.setValue(percentage * 100)

    def threading(self):
        self._thread=QThread()
        self._threaded=Threaded(self.update_progressbar, result=self.display_page)

        self.requestDoc.connect(self._threaded.create_reports)

        self._thread.started.connect(self._threaded.start)
        self._threaded.moveToThread(self._thread)
        qApp.aboutToQuit.connect(self._thread.quit)
        self._thread.start()


    def btn_functionality(self):
        self.MainWindow = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

        self.ui.pushButton_Run.clicked.connect(self.get_comboBox_info)
        self.ui.pushButton_GoToFolder.clicked.connect(self.go_to_folder)


    def nav_functionality(self):
        pass


    def go_to_folder(self):
        folder = 'Reports/' + str(datetime.date.today()) + '/'
        if not os.path.exists(folder):
            os.makedirs(folder)

        dir_path = os.path.dirname(os.path.realpath(__file__))
        folder = folder.replace('/', '\\')
        subprocess.Popen(r"explorer /select," + dir_path + '\\' + folder)


    def project_FAQ(self):
        pass


    def project_about(self):
        pass

    def file_path(self):
        path = QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'),
                                           'Excel(*.xlsx);;csv(*.csv);;All Files(*.*)')
        csv = False
        excel = False

        if path[0][-5:] == '.xlsx':
            excel = True
        elif path[0][-4:] == '.csv':
            csv = True

        if path[0] == " ":  # Needs a space... -.-
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

    @pyqtSlot()
    def get_comboBox_info(self):
        if self.ui.label_excel_name.text() == "Excel file":
            file_path = self.file_path()
            if file_path == 'Missing':
                # TODO - need a way to warn things
                #self.ui.textEdit.setText('WARNING: Must use a CSV or Excel file.')
                return
        else:
            # Makes sure to use the temp excel file if the user selected a CSV
            if self.ui.label_excel_name.text()[-4:] == '.csv':
                file_path = 'temp.xlsx'
            else:
                # Used if a file location has already been selected!
                file_path = self.ui.label_excel_name.text()

        self.template_select = self.ui.comboBox_report.currentText()

        self.requestDoc.emit(file_path, self.template_select)

        # Todo - disable buttons! *Turn them back on in "Display page function"


    @pyqtSlot(object)
    def display_page(self):
        # TODO - make sure all of these labels are correct
        # self.ui.pushButton_Run.setEnabled(True)
        # self.ui.pushButton_Clear.setEnabled(True)
        # self.ui.pushButton_Save.setEnabled(True)
        #
        # self.ui.actionAbout.setEnabled(True)
        # self.ui.actionFAQ.setEnabled(True)
        # self.ui.actionNew.setEnabled(True)
        # self.ui.actionOpen.setEnabled(True)
        # self.ui.actionQuit.setEnabled(True)
        # self.ui.actionSave.setEnabled(True)
        pass
