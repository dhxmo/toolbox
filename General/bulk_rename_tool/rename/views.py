# GUI - main window

# QThread -> manage worker threads
from PyQt5.QtCore import QThread
from collections import deque
from pathlib import Path
from PyQt5.QtWidgets import QWidget, QFileDialog

# import renamer class
from .rename import Renamer
# import GUI class
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
        # connect rename files btn to rename files method
        self.renameFilesBtn.clicked.connect(self.rename_files)

    def rename_files(self):
        self._run_renamer_thread()

    def _run_renamer_thread(self):
        # retrieve prefix from input
        prefix = self.prefixEdit.text()

        # new QThread object to offload process
        self._thread = QThread()

        # instantiate Renamer
        # turn files into tuple to prevent thread from modifying underlying deque on main thread
        self._renamer = Renamer(files=tuple(self._files), prefix=prefix)
        # move renaming to instantiated thread
        self._renamer.moveToThread(self._thread)

        # connect thread start to function
        self._thread.started.connect(self._renamer.rename_files)

        # connect signal with popping files off the stack
        self._renamer.renamed_file_signal.connect(self._update_state_on_rename)

        # clean up
        # quit thread once renaming is done
        self._renamer.finished_signal.connect(self._thread.quit)
        # schedule objects for later deletion
        # The object will be deleted when control returns to the event loop
        self._renamer.finished_signal.connect(self._renamer.deleteLater)
        # delete thread only after renaming is done
        self._thread.finished.connect(self._renamer.deleteLater)
        # start worker thread
        self._thread.start()

    def _update_state_on_rename(self):
        self._files.popleft()
        self.srcFiles.takeItem(0)


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
