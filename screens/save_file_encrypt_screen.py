from email.mime import base
import sys
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg
from PySide6 import QtUiTools as qtu
from assets.ui import Ui_SaveFileForm
from backend import signal_manager
from screens.progress_window_screen import ProgressWindowScreen
from tools.toolkit import Tools as t
import os


class SaveFileEncryptScreen(qtw.QWidget, Ui_SaveFileForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.update_ui()

        self.save_file_button.clicked.connect(self.save_file_dialog)
        self.start_button.clicked.connect(self.start_button_handler)

    def update_ui(self):
        self.setWindowTitle("Encryption | Save a file")

        if signal_manager.saved_data.get("file_dropped"):
            self.dropped_file_path = signal_manager.saved_data["file_dropped"]
            self.file_chooser_input.setPlaceholderText(
                t.all.format_input_path(self.dropped_file_path)
            )

    def save_file_dialog(self):
        specified_file_name = os.path.split(self.dropped_file_path)[1]
        base_name = os.path.splitext(specified_file_name)[0]
        default_filename = f"{base_name}_encrypted.bin"

        file_path, _ = qtw.QFileDialog.getSaveFileName(
            self, "Save File", default_filename, "Binary Files (*.bin);;All Files (*)"
        )

        if file_path:
            self.saved_name_input.setPlaceholderText(t.all.format_input_path(file_path))
            signal_manager.saved_file_path.emit(file_path)
            self.start_button.setEnabled(True)
            print(
                "From signal manager data: saved_file_path =",
                signal_manager.saved_data["saved_file_path"],
            )

    def closeEvent(self, event):
        signal_manager.saved_data.get("save_main_window").show()
        event.accept()

    @qtc.Slot()
    def start_button_handler(self):
        self.progress_window = t.qt.center_widget(ProgressWindowScreen())
        self.progress_window.show()
        self.destroy()
