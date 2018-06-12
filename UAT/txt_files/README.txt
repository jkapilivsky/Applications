Use PyInstaller
- needs to be run in the folder location of the file

For one file executable
pyinstaller ".py file location" -F
example: pyinstaller Main.py -F

.exe file is in dist folder
in dist run ./(.py file) to launch app in CMD

Py file required in Python\Lib\site-packages\PyInstaller\hooks
Create file below
hook-pandas.py
hiddenimports = ['pandas._libs.tslibs.nattype',
                 'pandas._libs.tslibs.timedeltas',
                 'pandas._libs.tslibs.np_datetime',
                 'pandas._libs.skiplist']




Qt Designer
run below in cmd in the .ui folder to create a .py file
Classes\Version 2>C:\Users\jamie.kapilivsky\AppData\Local\Continuum\Anaconda3\Library\bin\pyuic5.bat -x pyqtdesignerV2.ui -o UI.py

- Designer folder
C:\Users\jamie.kapilivsky\AppData\Roaming\Python\Python36\site-packages\pyqt5-tools
