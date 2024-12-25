from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from assets.ui import Ui_operation_progress_window
from PySide6 import QtWidgets as qtw
from tools.toolkit import Tools as t
from backend import signal_manager
from PySide6 import QtCore as qtc
from backend import FileManager
import math
import os


class ProgressWindowScreen(qtw.QWidget, Ui_operation_progress_window):
    start_encryption = qtc.Signal(str, str, RSAPublicKey)

    def __init__(self):
        """
        Initializes the ProgressWindowScreen widget for the encryption process.

        This constructor sets up the UI and connects the necessary signals
        for updating the encryption progress and handling operation completion.
        It retrieves required data from the signal manager, such as the file path
        to be encrypted, the destination path for the saved file, and the public key.
        If any of these data are missing, the function exits early.

        The file size is determined, and a percentage value is calculated for
        updating progress. If all required data is present, the encryption
        operation is started.

        :return: None
        """

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

        if not dropped_file_path or not saved_file_path or not public_key:
            return

        self.file_size = os.path.getsize(dropped_file_path)
        self.one_percent = self.file_size * 0.01

        self._handle_encryption(dropped_file_path, saved_file_path, public_key)

    def update_ui(self):
        """
        Updates the user interface of the ProgressWindowScreen widget for the encryption process.

        This method sets the window title to indicate an encryption process,
        applies specific window flags, and centers the widget on the screen.
        """
        self.setWindowTitle(self.tr("Encryption..."))
        self.setWindowFlags(qtc.Qt.Window | qtc.Qt.WindowTitleHint)
        t.qt.center_widget(self)

    @qtc.Slot(int)
    def update_processed_bytes_handler(self, bytes):
        """
        Handles the update of the progress bar based on the number of bytes processed.

        This function calculates the completion percentage of the encryption operation
        by dividing the total number of processed bytes by the value representing one percent
        of the file size. It then updates the progress bar with the calculated percentage.

        :param bytes: The number of bytes processed
        """
        completed_percentage = math.ceil(
            signal_manager.saved_data["update_processed_bytes"] / self.one_percent
        )
        self.operation_progress.setValue(completed_percentage)

    @qtc.Slot()
    def operation_completed_handler(self):
        """
        Handles the completion of an encryption operation.

        This method displays a success message box, sets the flag to exit without
        displaying a confirmation dialog, performs necessary cleanup, and closes
        the window.
        """
        qtw.QMessageBox.information(
            self,
            self.tr("Success"),
            self.tr("Operation has been completed successfully"),
        )

        self.exit_without_dialog = True
        self.cleanup_thread()

        self.close()

    def closeEvent(self, event):
        """
        Reimplements the closeEvent method to show a confirmation dialog when the window is
        closed. If the user confirms, the thread is stopped, the main window is shown, and
        the window is closed. If the user cancels, the event is ignored and the window is not
        closed.

        :param event: The close event that triggered this method.
        """

        if self.exit_without_dialog:
            signal_manager.saved_data["save_main_window"].show()
            signal_manager.saved_data = {}
            event.accept()
            return

        exitConfirmed = qtw.QMessageBox.question(
            self,
            self.tr("Exit"),
            self.tr(
                "Are you sure you want to exit, it will interrupt current encryption?"
            ),
            qtw.QMessageBox.Yes | qtw.QMessageBox.No,
        )
        if exitConfirmed == qtw.QMessageBox.No:
            event.ignore()
            return

        self.cleanup_thread()
        signal_manager.saved_data["save_main_window"].show()
        signal_manager.saved_data = {}

        event.accept()

    def cleanup_thread(self):
        """
        Cleans up the resources associated with the encryption thread.

        This method emits a signal to stop the ongoing process, then it quits
        and waits for the thread to finish. After the thread has stopped, it
        deletes the thread and any associated resources. This ensures that all
        resources are properly released when the encryption operation is
        complete or interrupted.
        """

        signal_manager.stop_process.emit()
        self.thread.quit()
        self.thread.wait()
        self.deleteLater()
        self.thread.deleteLater()

    def _handle_encryption(self, dropped_file_path, saved_file_path, public_key):
        """
        Initiates the encryption process in a separate thread.

        This method sets up a FileManager instance and moves it to a new thread.
        It connects the start_encryption signal to the file manager's encrypt_file
        method and starts the thread, triggering the encryption operation.

        :param dropped_file_path: The path to the file that the user dropped
        :param saved_file_path: The path to the file where the encrypted output will be saved
        :param public_key: The public key to use for encryption
        """

        self.file_manager = FileManager()
        self.thread = qtc.QThread()
        self.file_manager.moveToThread(self.thread)
        self.start_encryption.connect(self.file_manager.encrypt_file)
        self.thread.started.connect(
            lambda: self.start_encryption.emit(
                dropped_file_path, saved_file_path, public_key
            )
        )

        self.thread.start()
