# run below in cmd in the .ui folder to create a .py file
#  Classes\Version 2>C:\Users\jamie.kapilivsky\AppData\Local\Continuum\Anaconda3\Library\bin\pyuic5.bat -x pyqtdesignerV2.ui -o UI.py

# Designer folder
# C:\Users\jamie.kapilivsky\AppData\Roaming\Python\Python36\site-packages\pyqt5-tools

import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pandas as pd

# from Threads import Threaded
from UI import Ui_MainWindow

class Window(QMainWindow):
    requestPage = pyqtSignal(str, str, str, str)

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        #self.threading()
        self.btn_functionality()
        self.nav_functionality()

        self.MainWindow = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.show()


    def btn_functionality(self):
        pass


    def nav_functionality(self):
        pass


    def go_to_folder(self):
        pass


    def run(self):
        pass


    def project_FAQ(self):
        pass


    def project_about(self):
        pass



