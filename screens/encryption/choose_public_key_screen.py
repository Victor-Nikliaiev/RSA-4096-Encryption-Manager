from screens.encryption.save_file_encrypt_screen import SaveFileEncryptScreen
from assets.ui import Ui_KeyInputForm
from PySide6 import QtWidgets as qtw
from tools.toolkit import Tools as t
from backend import signal_manager
from backend import RsaKeyManager
from PySide6 import QtCore as qtc

logging = t.all.logging_config_screen()
logging = logging.getLogger(__name__)


class ChoosePublicKeyScreen(qtw.QWidget, Ui_KeyInputForm):
    def __init__(self):
        """
        Initializes the ChoosePublicKeyScreen widget.

        This constructor sets up the user interface, updates the UI based on
        the settings, connects various UI elements to their respective event
        handlers, including buttons and input fields. It also initializes the
        RSA key manager and sets the selected file to None.
        """
        super().__init__()
        self.setupUi(self)
        self.update_ui()

        self.browse_button.clicked.connect(self.browse_file)
        self.next_button.clicked.connect(self.handle_click_next)
        self.file_radio.toggled.connect(self.toggle_input_mode)
        self.key_text_area.textChanged.connect(self.update_next_button_status)
        self.file_path_input.textChanged.connect(self.update_next_button_status)

        self.key_manager = RsaKeyManager()
        self.selected_file = None

    def update_ui(self):
        """
        Updates the user interface of the ChoosePublicKeyScreen widget.

        This method sets the window title, enables/disables UI elements,
        and sets the text and placeholder text of other UI elements.
        """
        self.setWindowTitle(self.tr("Encryption | Choose a public key"))
        self.browse_button.setEnabled(True)
        self.key_text_area.setEnabled(False)
        self.file_radio.setText(self.tr("Load public key from file"))
        self.text_radio.setText(self.tr("Enter public key manually"))
        self.file_path_input.setPlaceholderText(
            self.tr(
                "Browse for a public key file (the path will be generated automatically)..."
            )
        )
        self.key_text_area.setPlaceholderText(self.tr("Enter your public key here..."))
        self.disable_password_protection()

    def disable_password_protection(self):
        """
        Removes the password protection UI elements from the layout.

        This method deletes all children widgets of the password group layout
        and then deletes the layout itself, as password protection is not
        applicable for public keys.
        """

        children = self.password_group_layout.findChildren(qtw.QWidget)
        for child in children:
            child.deleteLater()

        self.password_group_layout.deleteLater()
        self.password_group_layout = None

    @qtc.Slot(bool)
    def toggle_input_mode(self, file_radio_status):
        """
        Slot connected to the "Load public key from file" radio button's toggled signal.
        This slot enables/disables the browse button and the public key text area based on
        the status of the radio button. If the radio button is toggled on (i.e., the user
        wants to load the public key from a file), the public key text area is cleared,
        and if the radio button is toggled off (i.e., the user wants to enter the public
        key manually), the file path input is cleared.
        """
        self.browse_button.setEnabled(file_radio_status)
        self.key_text_area.setEnabled(not file_radio_status)

        if file_radio_status:
            self.key_text_area.clear()
            return

        self.file_path_input.clear()

    @qtc.Slot()
    def browse_file(self):
        """
        Slot connected to the browse button's clicked signal.
        This slot opens a file dialog where the user can select a public key
        file. If the user selects a file, it updates the selected_file_path
        attribute and sets the text of the file_path_input to the selected
        file path variable.
        """
        full_file_path, _ = qtw.QFileDialog.getOpenFileName(
            self,
            self.tr("Select Public Key File"),
            "",
            self.tr("PEM Files (*.pem);;All Files (*)"),
        )

        if not full_file_path:
            return

        self.selected_file_path = full_file_path
        self.file_path_input.setText(t.all.format_input_path(full_file_path))

    @qtc.Slot()
    def update_next_button_status(self):
        """
        Slot connected to the text changed signal of the file path input and public key text area.
        This slot updates the enabled status of the "Next" button based on the following conditions:
        1.  The user has entered a file path in the file path input.
        2.  The user has entered a public key in the public key text area.
        """

        self.next_button.setEnabled(
            any([self.file_path_input.text(), self.key_text_area.toPlainText()])
        )

    @qtc.Slot()
    def handle_click_next(self):
        """
        Slot connected to the "Next" button's clicked signal.
        This slot handles the selected input mode (file or text area) and
        calls the appropriate method to validate the input. If the input is
        valid, it calls process_public_key to proceed with the encryption
        process.
        """
        handlers = {
            True: self._handle_file_input,
            False: self._handle_text_input,
        }

        handler = handlers[self.file_radio.isChecked()]

        if not handler():
            return

        self.process_public_key()

    def _handle_file_input(self):
        """
        Handles loading a public key from a file selected by the user.

        This method retrieves the file path from the selected file path attribute,
        validates its presence, and attempts to load a public key from it using
        the RSA key manager. If the file path is invalid, a warning message is
        displayed. If loading the public key fails, a critical error message is
        shown.

        :return: True if the public key was loaded successfully, False otherwise.
        """

        file_path = self.selected_file_path.strip()

        if not file_path:
            qtw.QMessageBox.warning(
                self, self.tr("Error"), self.tr("Please select a valid file.")
            )
            return False

        try:
            self.public_key = self.key_manager.load_public_key_from_file(file_path)
            return True
        except Exception as e:
            qtw.QMessageBox.critical(
                self, self.tr("Unsupported File Detected"), self.tr(f"{e}")
            )
            return False

    def _handle_text_input(self):
        """
        Handles entering a public key in the text area.

        This method retrieves the entered public key from the text area, validates
        its format, and attempts to serialize it using the RSA key manager. If the
        public key is invalid, a warning message is displayed. If serialization
        fails, a critical error message is shown.

        :return: True if the public key was serialized successfully, False otherwise.
        """

        input_public_key = self.key_text_area.toPlainText().strip()

        if self.validate_public_key(input_public_key):
            try:
                self.public_key = self.key_manager.serialize_public_key(
                    input_public_key
                )
                return True

            except Exception as e:
                qtw.QMessageBox.critical(
                    self, self.tr("Key Format Error"), self.tr(f"{e}")
                )
                return False

        qtw.QMessageBox.warning(
            self,
            self.tr("Key Format Error"),
            self.tr("Please enter a valid public key to proceed"),
        )
        return False

    def validate_public_key(self, key: str) -> bool:
        """
        Checks if the given public key string is valid.

        A public key string is considered valid if it contains both "BEGIN PUBLIC KEY" and "END PUBLIC KEY".

        :param key: The public key string to be validated.
        :return: True if the public key string is valid, False otherwise.
        """
        return "BEGIN PUBLIC KEY" in key and "END PUBLIC KEY" in key

    def process_public_key(self):
        """
        Processes the selected or entered public key for encryption.

        This method emits a signal indicating the public key has been accepted,
        logs the public key for debugging purposes, and transitions to the
        SaveFileEncryptScreen. It is called after the public key is successfully
        loaded either from a file or entered manually.

        :return: None
        """

        signal_manager.public_key_accepted.emit(self.public_key)
        logging.info(f"Public Key{self.public_key}")
        self.save_file_encrypt_screen = t.qt.center_widget(SaveFileEncryptScreen())
        self.save_file_encrypt_screen.show()
        self.destroy()

    def closeEvent(self, event):
        """
        Reimplements the closeEvent method to show the main window when
        this window is closed.

        :param event: The close event that triggered this method.
        """
        signal_manager.saved_data.get("save_main_window").show()
