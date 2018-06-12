from PyQt5.QtWidgets import QApplication
import sys
from Functionality import Window

if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())
