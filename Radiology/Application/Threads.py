from PyQt5.QtCore import *
from Scripts import MRI_Writer

class Threaded(QObject):
    result=pyqtSignal(object)

    def __init__(self, update_progress, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.update_progressbar = update_progress

    @pyqtSlot()
    def start(self): print("Thread started")

    @pyqtSlot(str, str)
    def create_reports(self, excel_path, template_selected):
        results = None

        if template_selected == 'McAllen MRI':
            results = MRI_Writer(excel_path).create_reports(self.update_progressbar)

        # TODO - Can emit it being complete?
        # Emits None
        self.result.emit(results)
