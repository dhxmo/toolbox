# GUI - main window

from PyQt5.QtWidgets import QWidget
from .ui.window import Ui_Window


# Qwidget - enables base GUI functionalities
# Ui_Window - provides the specific GUI arrangement for app
class Window(QWidget, Ui_Window):
    def __init__(self):
        # initialize base class
        super().__init__()
        # generate and collect data for the GUI
        self._setupUI()

    # _ for non-public methods -> not to be used outside the class
    def _setupUI(self):
        self.setupUi(self)