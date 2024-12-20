from math import floor
import os
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from tools.toolkit import Tools as t
from assets.ui import Ui_operation_progress_window
from backend import signal_manager
from backend import FileManager
import math
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey


class ProgressWindowScreen(qtw.QWidget, Ui_operation_progress_window):
    start_encryption = qtc.Signal(str, str, RSAPublicKey)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.update_ui()

        self.exit_without_dialog = False

        signal_manager.update_processed_bytes.connect(
            self.update_processed_bytes_handler
        )
        signal_manager.operation_completed.connect(self.operation_completed_handler)

        dropped_file_path = signal_manager.saved_data.get("file_dropped")
        saved_file_path = signal_manager.saved_data.get("saved_file_path")
        public_key = signal_manager.saved_data.get("public_key_accepted")

        if dropped_file_path and saved_file_path and public_key:

            self.file_size = os.path.getsize(dropped_file_path)
            self.one_percent = self.file_size * 0.01

            ### Here starts encrypt operation
            self.file_manager = FileManager()
            self.thread = qtc.QThread()
            self.file_manager.moveToThread(self.thread)
            self.start_encryption.connect(self.file_manager.encrypt_file)
            # self.thread.started.connect(
            #     lambda: self.file_manager.encrypt_file(
            #         dropped_file_path, saved_file_path, public_key
            #     )
            # )

            self.thread.started.connect(
                lambda: self.start_encryption.emit(
                    dropped_file_path, saved_file_path, public_key
                )
            )

            # file_manager.encrypt_file(dropped_file_path, saved_file_path, public_key)
            self.thread.start()

    def update_ui(self):
        self.setWindowTitle("Encryption | Progress")
        self.setWindowFlags(qtc.Qt.Window | qtc.Qt.WindowTitleHint)
        t.qt.center_widget(self)

    def update_processed_bytes_handler(self, bytes):
        completed_percentage = math.ceil(
            signal_manager.saved_data["update_processed_bytes"] / self.one_percent
        )
        self.operation_progress.setValue(completed_percentage)

    def operation_completed_handler(self):

        qtw.QMessageBox.information(
            self, "Success", "Operation has been completed successfully"
        )

        self.exit_without_dialog = True
        self.thread.quit()
        self.thread.wait()
        self.deleteLater()
        self.thread.deleteLater()

        self.close()

    def closeEvent(self, event):

        if self.exit_without_dialog:
            print("--Exit without dialog--")
            signal_manager.saved_data["save_main_window"].show()
            signal_manager.saved_data = {}
            event.accept()
            return

        exitConfirmed = qtw.QMessageBox.question(
            self,
            "Exit",
            "Are you sure you want to exit, it will interrupt current encryption?",
            qtw.QMessageBox.Yes | qtw.QMessageBox.No,
        )

        if exitConfirmed == qtw.QMessageBox.Yes:
            signal_manager.saved_data["save_main_window"].show()
            signal_manager.saved_data = {}
            event.accept()
        else:
            event.ignore()
