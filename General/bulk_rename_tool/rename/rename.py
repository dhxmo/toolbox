# file renaming

import time
from pathlib import Path

# QObject - for custom signals and functionalities
# pyqtSignal -> emit signal on event activation
from PyQt5.QtCore import QObject, pyqtSignal


# subclass of QObject
class Renamer(QObject):
    """
    custom signals
        progressed_signal -> return int ,ie., total number of files renamed
        renamed_file_signal -> return path to renamed file
        finished_signal -> emit when renaming is done

    """
    progressed_signal = pyqtSignal(int)
    renamed_file_signal = pyqtSignal(Path)
    finished_signal = pyqtSignal()

    def __init__(self, files, prefix):
        super().__init__()
        self._files = files
        self._prefix = prefix

    def rename_files(self):
        # iterate over selected files and generate serialized numbers
        for number, file in enumerate(self._files, 1):
            # generate new file name
            new_file = file.parent.joinpath(
                f"{self._prefix}{str(number)}{file.suffix}"
            )
            # rename file
            file.rename(new_file)
            time.sleep(0.03)

            # emit signals to GUI
            self.progressed_signal.emit(number)
            self.renamed_file_signal.emit(new_file)

        # reset progress bar
        self.progressed_signal.emit(0)
        # finish
        self.finished_signal.emit()
