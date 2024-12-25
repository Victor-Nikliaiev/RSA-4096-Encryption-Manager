from screens.decryption.decryption_progress_window_screen import ProgressWindowScreen
from assets.ui import Ui_SaveFileForm
from PySide6 import QtWidgets as qtw
from tools.toolkit import Tools as t
from backend import signal_manager
from PySide6 import QtCore as qtc

import os

logging = t.all.logging_config_screen()
logging = logging.getLogger(__name__)


class SaveFileDecryptScreen(qtw.QWidget, Ui_SaveFileForm):
    def __init__(self):
        """
        Constructor for SaveFileDecryptScreen.

        This constructor sets up the UI, sets the window title, and connects
        the necessary signals.
        """
        super().__init__()
        self.setupUi(self)
        self.update_ui()

        self.save_file_button.clicked.connect(self.save_file_dialog)
        self.start_button.clicked.connect(self.start_button_handler)

    def update_ui(self):
        """
        Updates the user interface of the SaveFileDecryptScreen widget.

        This method sets the window title, sets the text of UI elements,
        and sets the placeholder text of the input field based on the
        dropped file path.
        """
        self.setWindowTitle(self.tr("Decryption | Save a file"))

        dropped_file_path = signal_manager.saved_data.get("file_dropped")

        if dropped_file_path:
            self.dropped_file_path = dropped_file_path
            self.file_chooser_input.setPlaceholderText(
                t.all.format_input_path(self.dropped_file_path)
            )

        self.input_file_info_btn.setText(self.tr("File to be decrypted:"))
        self.output_file_info_btn.setText(
            self.tr("Choose file name for decrypted file:")
        )
        self.start_button.setText(self.tr("Start Decryption"))

    @qtc.Slot()
    def save_file_dialog(self):
        """
        Opens a file dialog for the user to choose a file path to save the
        decrypted file. The default filename is the name of the file that was
        dropped, with "_decrypted" added to the end. The file extension is
        kept the same.

        If the user cancels, the method does nothing.

        :return: None
        """

        specified_file_name = os.path.split(self.dropped_file_path)[1]
        if "_encrypted.bin" in specified_file_name:
            specified_file_name = specified_file_name.replace("_encrypted.bin", "")

        base_name = os.path.splitext(specified_file_name)[0]
        extension = os.path.splitext(specified_file_name)[1]
        default_filename = f"{base_name}_decrypted{extension}"

        file_path, _ = qtw.QFileDialog.getSaveFileName(
            self, self.tr("Save File"), default_filename, self.tr("All Files (*)")
        )
        if not file_path:
            return

        self.saved_name_input.setPlaceholderText(t.all.format_input_path(file_path))
        signal_manager.saved_file_path.emit(file_path)
        self.start_button.setEnabled(True)
        logging.info(f"File will be saved with path: {file_path}")

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
        Starts the decryption operation.

        This method is called when the start button is clicked. It
        creates a ProgressWindowScreen, moves it to the center of the
        screen, and shows it. It then closes this window.

        :return: None
        """
        self.progress_window = t.qt.center_widget(ProgressWindowScreen())
        self.progress_window.show()
        self.destroy()
