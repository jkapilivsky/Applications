from PyQt5.QtCore import *

from Scripts import Get_Basic_Info, Localization_Info, V2_Migration

class Threaded(QObject):
    result=pyqtSignal(object)

    def __init__(self, update_textedit, update_progress, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.update_textedit = update_textedit
        self.update_progressbar = update_progress

    @pyqtSlot()
    def start(self): print("Thread started")

    @pyqtSlot(str, str, str, str)
    def get_info(self, file_path, script_select, country, modheader):
        results = None

        if script_select == 'New Page':
            results = Get_Basic_Info(file_path, 'Sheet1').url_loop(
                                                        self.update_textedit, self.update_progressbar)
        elif script_select == 'Localization':
            results = Localization_Info(file_path, 'Sheet1', country).url_loop(
                                                        self.update_textedit, self.update_progressbar)
        elif script_select == 'V2 migration':
            results = V2_Migration(file_path, 'Sheet1', modheader).url_loop(
                                                        self.update_textedit, self.update_progressbar)
        else:
            print('how did they select something that did not exist...')
        self.result.emit(results)

