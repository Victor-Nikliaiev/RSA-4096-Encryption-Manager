import logging
from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from assets.ui import Ui_KeyInputForm
from backend import signal_manager
from screens.decryption.save_file_decrypt_screen import SaveFileDecryptScreen
from tools.toolkit import Tools as t
from backend import RsaKeyManager

logging = t.all.logging_config_screen()
logging = logging.getLogger(__name__)


class ChoosePrivateKeyScreen(qtw.QWidget, Ui_KeyInputForm):
    def __init__(self):
        """
        Initializes the ChoosePrivateKeyScreen widget.

        This constructor sets up the user interface, initializes the RSA key manager,
        and connects various UI elements to their respective event handlers,
        including buttons and input fields. It also manages the state of the
        password protection checkbox and its corresponding input accessibility.
        """

        super().__init__()
        self.setupUi(self)
        self.update_ui()

        self.key_manager = RsaKeyManager()

        self.browse_button.clicked.connect(self.browse_file)
        self.next_button.clicked.connect(self.handle_click_next)
        self.file_radio.toggled.connect(self.toggle_input_mode)
        self.selected_file = None

        self.key_text_area.textChanged.connect(self.update_next_button_status)
        self.file_path_input.textChanged.connect(self.update_next_button_status)
        self.is_password_protected_cb.stateChanged.connect(
            self.update_next_button_status
        )
        self.password_lineEdit.textChanged.connect(self.update_next_button_status)

        self.is_password_protected_cb.stateChanged.connect(
            self.handle_password_input_accessability
        )

    def update_ui(self):
        """
        Updates the user interface of the ChoosePrivateKeyScreen widget.

        This method sets the window title, enables/disables UI elements,
        and sets the text and placeholder text of other UI elements.
        """

        self.setWindowTitle(self.tr("Decryption | Choose a private key"))
        self.browse_button.setEnabled(True)
        self.key_text_area.setEnabled(False)
        self.file_radio.setText(self.tr("Load private key from file"))
        self.text_radio.setText(self.tr("Enter private key manually"))
        self.file_path_input.setPlaceholderText(
            self.tr(
                "Browse for a private key file (the path will be generated automatically)..."
            )
        )
        self.key_text_area.setPlaceholderText(self.tr("Enter your private key here..."))

    @qtc.Slot(bool)
    def toggle_input_mode(self, file_radio_status):
        """
        Slot connected to the "Load private key from file" radio button's toggled signal.
        This slot enables/disables the browse button and the private key text area based on
        the status of the radio button. If the radio button is toggled on (i.e., the user
        wants to load the private key from a file), the private key text area is cleared,
        and if the radio button is toggled off (i.e., the user wants to enter the private
        key manually), the file path input is cleared.
        """

        self.browse_button.setEnabled(file_radio_status)
        self.key_text_area.setEnabled(not file_radio_status)

        if file_radio_status:
            self.key_text_area.clear()
            return

        self.file_path_input.clear()
        self.selected_file_path = None

    @qtc.Slot()
    def browse_file(self):
        """
        Slot connected to the browse button's clicked signal.
        This slot opens a file dialog where the user can select a private key
        file. If the user selects a file, it updates the selected_file_path
        attribute and sets the text of the file_path_input to the selected
        file path.
        """

        full_file_path, _ = qtw.QFileDialog.getOpenFileName(
            self,
            self.tr("Select Private Key File"),
            "",
            "PEM Files (*.pem);;All Files (*)",
        )
        if full_file_path:
            self.selected_file_path = full_file_path
            self.file_path_input.setText(t.all.format_input_path(full_file_path))

    @qtc.Slot()
    def update_next_button_status(self):
        """
        Slot connected to the text changed signal of the file path input and the key text area.
        This slot updates the enabled status of the "Next" button based on the following conditions:
        1.  The user has entered a file path in the file path input or has entered a private key
            in the key text area.
        2.  If the user has checked the "Password protect the private key" checkbox, the user
            must have entered a password in the password line edit.
        """
        self.next_button.setEnabled(
            all(
                [
                    self.file_path_input.text() or self.key_text_area.toPlainText(),
                    not self.is_password_protected_cb.isChecked()
                    or self.password_lineEdit.text(),
                ]
            )
        )

    @qtc.Slot()
    def handle_click_next(self):
        """
        Slot connected to the clicked signal of the "Next" button.
        This slot will call one of the two private methods based on the state of the
        "Load private key from file" radio button. If the user has checked the
        "Password protect the private key" checkbox, the user must have entered a
        valid password. If the user's input is valid, the slot will call the
        process_private_key method.

        :return: None
        """
        password = (
            self.password_lineEdit.text()
            if self.is_password_protected_cb.isChecked()
            else None
        )

        handlers = {True: self._handle_file_input, False: self._handle_text_input}
        handler = handlers[self.file_radio.isChecked()]

        if not handler(password):
            return

        self.process_private_key()

    def _handle_file_input(self, password):
        """
        Handles loading a private key from a file selected by the user.

        :param password: The password to decrypt the private key.
        :return: True if the private key was loaded successfully, False otherwise.
        """
        file_path = self.selected_file_path.strip()
        if not file_path:
            qtw.QMessageBox.warning(
                self, self.tr("Error"), self.tr("Please select a valid file.")
            )
            return False
        try:
            self.private_key = self.key_manager.load_private_key_from_file(
                file_path, password
            )
        except Exception as e:
            qtw.QMessageBox.critical(
                self, self.tr("Unsupported File Detected"), self.tr(f"{e}")
            )
            return False
        return True

    def _handle_text_input(self, password):
        """
        Handles entering a private key in the text area.

        :param password: The password to encrypt the private key.
        :return: True if the private key was entered successfully, False otherwise.
        """
        private_key = self.key_text_area.toPlainText().strip()

        if not self.validate_private_key(private_key):
            qtw.QMessageBox.warning(
                self,
                self.tr("Private Key Format Error"),
                self.tr("Please enter a valid private key to proceed"),
            )
            return False

        try:
            self.private_key = self.key_manager.serialize_private_key(
                private_key, password
            )
        except Exception as e:
            qtw.QMessageBox.critical(self, self.tr("Key Format Error"), self.tr(f"{e}"))
            return False

        return True

    def validate_private_key(self, key: str) -> bool:
        """
        Checks if the given private key string is valid.

        A private key string is considered valid if it contains both "BEGIN PRIVATE KEY" and "END PRIVATE KEY".

        :param key: The private key string to be validated.
        :return: True if the private key string is valid, False otherwise.
        """
        return "BEGIN PRIVATE KEY" in key and "END PRIVATE KEY" in key

    def process_private_key(self):
        """
        Processes the selected or entered private key for decryption.

        This method emits a signal indicating the private key has been accepted,
        logs the private key for debugging purposes, and transitions to the
        SaveFileDecryptScreen. It is called after the private key is successfully
        loaded either from a file or entered manually.

        :return: None
        """

        signal_manager.private_key_accepted.emit(self.private_key)
        logging.info(f"Saved Private Key {self.private_key}")

        self.save_file_decrypt_screen = t.qt.center_widget(SaveFileDecryptScreen())
        self.save_file_decrypt_screen.show()
        self.destroy()

    @qtc.Slot(bool)
    def handle_password_input_accessability(self, state):
        """
        Slot connected to the state changed signal of the "Password protect the private key" checkbox.
        This slot sets the enabled status of the password input field based on the checkbox state.
        If the checkbox is unchecked, the method also clears the password input field.

        :param state: A boolean indicating whether the password input field should be enabled or not.
        """
        self.password_lineEdit.setEnabled(state)

        if not state:
            self.password_lineEdit.clear()

    def closeEvent(self, event):
        """
        Handle the close event for the ChoosePrivateKeyScreen.

        This method is triggered when the ChoosePrivateKeyScreen is closed.
        It retrieves the main window from the saved data using the signal manager
        and shows it. The event is then accepted to proceed with closing the
        ChoosePrivateKeyScreen.

        Parameters
        ----------
        event : QCloseEvent
            The close event that triggered this method.
        """

        signal_manager.saved_data.get("save_main_window").show()
