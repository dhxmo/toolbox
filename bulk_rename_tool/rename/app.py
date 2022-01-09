# pyOt skeleton

import sys
from PyQt5.QtWidgets import QApplication

from .views import Window

def main():
    # initialize app and instantiate the window class
    app = QApplication(sys.argv)
    win = Window()
    # show main window using QtWidget method show
    win.show()
    # run event loop using QApplication exec method
    sys.exit(app.exec())
