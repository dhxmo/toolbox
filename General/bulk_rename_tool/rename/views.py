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
        "Excel Files (*.xlsx)",
        "Legacy Word Files (*.doc)",
        "Word Files (*.docx)",
        "Log Files (*.log)",
        "OpenDocument Text Files (*.odt)",
        "Rich Text Format Files (*.rtf)",
        "Comma-Separated Values Files (*.csv)",
        "XML Files (*.xml)",
        "MP3 Files (*.mp3)",
        "WAVE Files (*.wav)",
        "MPEG-4 Files (*.mp4)",
        "Apple QuickTime Files (*.mov)",
        "Audio Video Interleave Files (*.avi)",
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
        # access setupUi method of Ui_Window class
        self.setupUi(self)
        # call from within UI
        self._no_file_stateupdate()

    # when there's no files to be renamed
    def _no_file_stateupdate(self):
        # updates files count to 0
        self._filesCount = len(self._files)
        # enable load files button
        self.loadFilesBtn.setEnabled(True)
        # disable rename files button
        self.renameFilesBtn.setEnabled(False)
        # disable prefix input if no files to be renamed
        self.prefixEdit.clear()
        self.prefixEdit.setEnabled(False)

    def _connect_signals_slots(self):
        # connect button's click event to load files method
        self.loadFilesBtn.clicked.connect(self.load_files)
        # connect rename files btn to rename files method
        self.renameFilesBtn.clicked.connect(self.rename_files)
        # connect user input in prefixEdit to ready state update
        # textChanged -> QLineEdit signal emitted whenever the text changes
        self.prefixEdit.textChanged.connect(self._ready_stateupdate)

    # enable rename files button once required prefix input has been provided
    def _read_stateupdate(self):
        if self.prefixEdit.text():
            self.renameFilesBtn.setEnabled(True)
        else:
            self.renameFilesBtn.setEnabled(False)

    def rename_files(self):
        self._run_renamer_thread()
        self._busy_stateupdate()

    # disable buttons if app is busy
    def _busy_stateupdate(self):
        self.loadFilesBtn.setEnabled(False)
        self.renameFilesBtn.setEnabled(False)

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

        # connect renaming signal with popping files off the stack
        self._renamer.renamed_file_signal.connect(self._update_state_on_rename)
        # connect progress signal with progress bar update function
        # progressed_signal provides the file number being processed to _update_progress_bar
        self._renamer.progressed_signal.connect(self._update_progressbar)

        # connect finished signal with no file update method to update GUI on process finish
        self._renamer.finished_signal.connect(self._no_file_stateupdate)

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
        # pop file off the deque
        self._files.popleft()
        # takeItem - Removes and returns the item from the given row in the list widget
        self.srcFiles.takeItem(0)

    # calculate percentage and update GUI
    def _update_progressbar(self, file_number):
        progress_percent = int(file_number / self._filesCount * 100)
        self.progressBar.setValue(progress_percent)

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
            # enable prefix input once files have been loaded
            self._files_loaded_stateupdate()

    def _files_loaded_stateupdate(self):
        self.prefixEdit.setEnabled(True)
