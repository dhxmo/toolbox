# GUI - main window

from collections import deque
from pathlib import Path
from PyQt5.QtWidgets import QWidget, QFileDialog
from .ui.window import Ui_Window

# different file types to select from
FILTERS = ";;".join(
    (
        "PNG Files (*.png)",
        "JPEG Files (*.jpeg)",
        "JPG Files (*.jpg)",
        "GIF Files (*.gif)",
        "Text Files (*.txt)",
        "Python Files (*.py)",
    )
)


# QWidget - enables base GUI functionalities
# Ui_Window - provides the specific GUI arrangement for app
class Window(QWidget, Ui_Window):
    def __init__(self):
        # initialize base class
        super().__init__()
        # deque object to store filepaths to be renamed
        self._files = deque()
        self._filesCount = len(self._files)
        # generate and collect data for the GUI
        self._setup_ui()
        self._connect_signals_slots()

    # _ for non-public methods -> not to be used outside the class
    def _setup_ui(self):
        self.setupUi(self)

    def _connect_signals_slots(self):
        # connect btn's click event to load files method
        self.loadFilesBtn.clicked.connect(self.load_files)

    def load_files(self):
        # set initializing directory
        if self.dirEdit.text():
            init_dir = self.dirEdit.text()
        else:
            init_dir = str(Path.home())

        """
            getOpenFileNames:
                parent= self -> widget (current window) that owns the dialog
                caption -> dialog title
                dir -> path to initializing directory
                filter -> file type filters
            returns a tuple
                -> selected files are returned as a list in the first element of the tuple
        """
        files = QFileDialog.getOpenFileNames(self, "Choose Files to Rename", init_dir, filter=FILTERS)

        if len(files[0]) > 0:
            # find directory of the current file and set to dirEdit
            src_dir_name = str(Path(files[0][0]).parent)
            self.dirEdit.setText(src_dir_name)

            # iterate over selected files
            for file in files[0]:
                # append file paths to _files
                self._files.append(Path(file))
                filename = file.split("/")
                # add files to srcFiles for GUI
                self.srcFiles.addItem(".../" + filename[-1])

            # update file count
            self._filesCount = len(self._files)
