from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from assets.ui import Ui_operation_progress_window
from PySide6 import QtWidgets as qtw
from tools.toolkit import Tools as t
from backend import signal_manager
from PySide6 import QtCore as qtc
from backend import FileManager
import math
import os


class ProgressWindowScreen(qtw.QWidget, Ui_operation_progress_window):
    start_decryption = qtc.Signal(str, str, RSAPrivateKey)

    def __init__(self):
        """
        Initializes ProgressWindowScreen widget.

        This constructor sets up the UI, sets the window title, and connects
        the necessary signals. It also manages the state of the window and
        starts the decryption operation if the necessary data is present.

        :return: None
        """

        super().__init__()
        self.setupUi(self)
        self.update_ui()

        self.exit_without_dialog = False

        signal_manager.current_window.emit(self)
        signal_manager.update_processed_bytes.connect(
            self.update_processed_bytes_handler
        )
        signal_manager.operation_completed.connect(self.operation_completed_handler)

        dropped_file_path = signal_manager.saved_data.get("file_dropped")
        saved_file_path = signal_manager.saved_data.get("saved_file_path")
        private_key = signal_manager.saved_data.get("private_key_accepted")

        if not dropped_file_path or not saved_file_path or not private_key:
            return

        self.file_size = os.path.getsize(dropped_file_path)
        self.one_percent = self.file_size * 0.01

        self._handle_decryption(dropped_file_path, saved_file_path, private_key)

    def update_ui(self):
        """
        Updates the user interface of the ProgressWindowScreen widget.

        This method sets the window title to indicate a decryption process,
        applies specific window flags, and centers the widget on the screen.
        """

        self.setWindowTitle(self.tr("Decryption..."))
        self.setWindowFlags(qtc.Qt.Window | qtc.Qt.WindowTitleHint)
        t.qt.center_widget(self)

    @qtc.Slot(int)
    def update_processed_bytes_handler(self, bytes):
        """
        Updates the progress bar based on the processed bytes.

        This method calculates the percentage of the operation completed by
        dividing the total number of processed bytes by the value representing
        one percent of the file size. It then updates the progress bar with
        this calculated percentage.

        :param bytes: The number of bytes processed
        """

        completed_percentage = math.ceil(
            signal_manager.saved_data["update_processed_bytes"] / self.one_percent
        )
        self.operation_progress.setValue(completed_percentage)

    @qtc.Slot()
    def operation_completed_handler(self):
        """
        Handles the completion of a decryption operation.

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
        closed. If the user confirms, the thread is stopped and the main window is shown.
        If the user cancels, the event is ignored and the window is not closed.

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
                "Are you sure you want to exit, it will interrupt current decryption?"
            ),
            qtw.QMessageBox.Yes | qtw.QMessageBox.No,
        )

        if exitConfirmed == qtw.QMessageBox.No:
            event.ignore()
            return

        signal_manager.stop_process.emit()
        self.cleanup_thread()
        signal_manager.saved_data["save_main_window"].show()
        signal_manager.saved_data = {}
        event.accept()

    def cleanup_thread(self):
        """
        Stops the thread and cleans up resources.

        This method is called when the window is closed. It stops the thread,
        waits for the thread to finish, and then deletes both the thread and
        the window.
        """

        self.thread.quit()
        self.thread.wait()
        self.deleteLater()
        self.thread.deleteLater()

    def _handle_decryption(self, dropped_file_path, saved_file_path, private_key):
        """
        Starts the decryption operation.

        This method is called when the window is created. It creates a
        FileManager, moves it to a new thread, and connects the necessary
        signals. It then starts the thread and tells it to start the
        decryption operation.

        :param dropped_file_path: The path to the file that the user dropped
        :param saved_file_path: The path to the file that the user selected
            as the destination for the decrypted file
        :param private_key: The private key to use for decryption
        """
        self.file_manager = FileManager()
        self.thread = qtc.QThread()
        self.file_manager.moveToThread(self.thread)
        self.start_decryption.connect(self.file_manager.decrypt_file)

        self.thread.started.connect(
            lambda: self.start_decryption.emit(
                dropped_file_path, saved_file_path, private_key
            )
        )

        self.thread.start()
