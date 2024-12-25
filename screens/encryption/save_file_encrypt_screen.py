import logging
from screens.encryption.encryption_progress_window_screen import ProgressWindowScreen
from assets.ui import Ui_SaveFileForm
from PySide6 import QtWidgets as qtw
from tools.toolkit import Tools as t
from backend import signal_manager
from PySide6 import QtCore as qtc
import os

logging = t.all.logging_config_screen()
logging = logging.getLogger(__name__)


class SaveFileEncryptScreen(qtw.QWidget, Ui_SaveFileForm):
    def __init__(self):
        """
        Initializes the SaveFileEncryptScreen widget.

        This constructor sets up the user interface and connects the necessary
        signals. It also updates the UI based on the dropped file path.

        :return: None
        """
        super().__init__()
        self.setupUi(self)
        self.update_ui()

        self.save_file_button.clicked.connect(self.save_file_dialog)
        self.start_button.clicked.connect(self.start_button_handler)

    def update_ui(self):
        """
        Updates the user interface of the SaveFileEncryptScreen widget.

        This method sets the window title, sets the text of UI elements,
        and sets the placeholder text of the input field based on the
        dropped file path.

        :return: None
        """

        self.setWindowTitle(self.tr("Encryption | Save a file"))

        dropped_file_path = signal_manager.saved_data.get("file_dropped")
        if not dropped_file_path:
            return

        self.dropped_file_path = dropped_file_path
        self.file_chooser_input.setPlaceholderText(
            t.all.format_input_path(self.dropped_file_path)
        )

    @qtc.Slot()
    def save_file_dialog(self):
        """
        Opens a file dialog for the user to choose a file path to save the
        encrypted file. The default filename is the name of the file that was
        dropped, with "_encrypted.bin" added to the end. The file extension is
        kept the same.

        If the user cancels, the method does nothing.

        :return: None
        """
        specified_file_name = os.path.split(self.dropped_file_path)[1]
        default_filename = f"{specified_file_name}_encrypted.bin"

        file_path, _ = qtw.QFileDialog.getSaveFileName(
            self,
            self.tr("Save File"),
            default_filename,
            self.tr("Binary Files (*.bin);;All Files (*)"),
        )
        if not file_path:
            return

        self.saved_name_input.setPlaceholderText(t.all.format_input_path(file_path))
        signal_manager.saved_file_path.emit(file_path)
        self.start_button.setEnabled(True)
        logging.info(f"Save file path: {signal_manager.saved_data["saved_file_path"]}")

    def closeEvent(self, event):
        """
        Reimplements the closeEvent method to show the main window when
        this window is closed.

        :param event: The close event that triggered this method.
        """
        signal_manager.saved_data.get("save_main_window").show()
        event.accept()

    @qtc.Slot()
    def start_button_handler(self):
        """
        Handles the click event of the start button to initiate the encryption process.

        This method creates an instance of ProgressWindowScreen, centers it on
        the screen, and displays it. After showing the progress window, it
        destroys the current window.

        :return: None
        """

        self.progress_window = t.qt.center_widget(ProgressWindowScreen())
        self.progress_window.show()
        self.destroy()
