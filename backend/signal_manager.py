from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey, RSAPrivateKey
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw


class _SignalManager(qtc.QObject):
    file_dropped = qtc.Signal(str)
    update_next_button_status = qtc.Signal(bool)
    public_key_accepted = qtc.Signal(RSAPublicKey)
    private_key_accepted = qtc.Signal(RSAPrivateKey)
    save_main_window = qtc.Signal(qtw.QMainWindow)
    saved_file_path = qtc.Signal(str)
    update_processed_bytes = qtc.Signal(int)
    operation_completed = qtc.Signal()
    stop_process = qtc.Signal()

    current_window = qtc.Signal(qtc.QObject)
    critical_error = qtc.Signal(str, str)

    selected_option = qtc.Signal(object)

    saved_data = {}

    @qtc.Slot(qtw.QMainWindow)
    def _save_main_window_handler(self, widget):
        """
        Save the main window that the user interacted with into the saved data. This window
        is the one that started the operation. This is useful for showing a progress bar
        on the main window.
        """

        self.saved_data["save_main_window"] = widget

    @qtc.Slot(str)
    def _file_dropped_handler(self, file_path):
        """
        Save the file path that the user dropped into the saved data. This is the file
        that the user wants to encrypt/decrypt.
        """
        self.saved_data["file_dropped"] = file_path

    @qtc.Slot(RSAPublicKey)
    def _public_key_accepted_handler(self, key):
        """
        Save the public RSA key that the user selected/entered into the saved data.
        This is the key that will be used for encryption.
        """

        self.saved_data["public_key_accepted"] = key

    @qtc.Slot(RSAPrivateKey)
    def _private_key_accepted_handler(self, key):
        """
        Save the private RSA key that the user selected/entered into the saved data.
        This is the key that will be used for decryption.
        """

        self.saved_data["private_key_accepted"] = key

    @qtc.Slot(str)
    def _saved_file_path_handler(self, file_path):
        """
        Save the file path that the user selected as the destination for the saved
        encrypted/decrypted file into the saved data.
        """
        self.saved_data["saved_file_path"] = file_path

    @qtc.Slot(int)
    def _update_processed_bytes_handler(self, bytes):
        """
        Increment the total number of bytes processed by the given number of bytes.

        This function is a slot for the update_processed_bytes signal. It is used
        by the encrypt/decrypt threads to update the progress bar on the window.

        :param bytes: The number of bytes processed
        """
        if self.saved_data.get("update_processed_bytes") is None:
            self.saved_data["update_processed_bytes"] = 0
        self.saved_data["update_processed_bytes"] += bytes

    @qtc.Slot(qtc.QObject)
    def _current_window_handler(self, window):
        """
        Save the current window in the saved data. This is the window that the operation
        is currently being performed on. This is useful for showing a progress bar on the
        correct window.
        """
        self.saved_data["current_window"] = window

    @qtc.Slot(str, str)
    def _critical_error_handler(self, input_file_path: str, error_message: str):
        """
        Shows a critical error message box with the given error message,
        and closes the current window without showing the dialog to confirm
        closing the window.
        """
        qtw.QMessageBox.critical(
            None, "Error", f"Error processing file: {input_file_path}, {error_message}"
        )
        window = self.saved_data["current_window"]
        window.cleanup_thread()
        window.exit_without_dialog = True
        window.close()

    @qtc.Slot(object)
    def _selected_option_handler(self, option):
        """
        Save the selected option from the keygen screen into the saved data.
        This is the option that the user selected for how to generate a key pair.

        :param option: The selected option
        """
        self.saved_data["selected_option"] = option


signal_manager = _SignalManager()
signal_manager.save_main_window.connect(signal_manager._save_main_window_handler)
signal_manager.file_dropped.connect(signal_manager._file_dropped_handler)
signal_manager.public_key_accepted.connect(signal_manager._public_key_accepted_handler)
signal_manager.private_key_accepted.connect(
    signal_manager._private_key_accepted_handler
)
signal_manager.saved_file_path.connect(signal_manager._saved_file_path_handler)
signal_manager.update_processed_bytes.connect(
    signal_manager._update_processed_bytes_handler
)
signal_manager.current_window.connect(signal_manager._current_window_handler)
signal_manager.critical_error.connect(signal_manager._critical_error_handler)
signal_manager.selected_option.connect(signal_manager._selected_option_handler)
