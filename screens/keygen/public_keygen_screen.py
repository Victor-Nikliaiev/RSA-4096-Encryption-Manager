from backend import RsaKeyManager, signal_manager
from assets.ui.keygen import Ui_PublicKeygen
from PySide6 import QtWidgets as qtw
from tools.toolkit import Tools as t
from PySide6 import QtCore as qtc

logging = t.all.logging_config_screen()
logging = logging.getLogger(__name__)


class PublicKeygenScreen(qtw.QWidget, Ui_PublicKeygen):
    def __init__(self):
        """
        Initializes the PublicKeygenScreen widget.

        This constructor sets up the user interface by connecting various UI
        elements such as buttons and input fields to their respective event
        handlers. It initializes the state of the public and private key paths,
        password, and operation status, and ensures the generate button's
        availability is checked based on input changes.
        """

        super().__init__()
        self.setupUi(self)

        self.private_key_sel_btn.clicked.connect(self.private_key_sel_btn_handler)
        self.password_cb.clicked.connect(self.password_cb_handler)
        self.pub_key_select_btn.clicked.connect(self.pub_key_select_btn_handler)

        self.private_key_path_le.textChanged.connect(
            self.generate_button_status_checker
        )
        self.password_cb.clicked.connect(self.generate_button_status_checker)
        self.pub_key_path_le.textChanged.connect(self.generate_button_status_checker)
        self.password_le.textChanged.connect(self.generate_button_status_checker)

        self.generate_btn.clicked.connect(self.process_keygen)

        self.public_key_save_path: str
        self.private_key_full_path: str
        self.password = None
        self.operation_completed = False

    @qtc.Slot()
    def private_key_sel_btn_handler(self):
        """
        Slot connected to the private key selection button's clicked signal.
        This slot opens a file dialog where the user can select a private key
        file. If the user selects a file, it updates the private_key_full_path
        attribute and sets the text of the private_key_path_le to the selected
        file path. It also checks if the generate button should be enabled based
        on the input fields' state.
        """
        private_key_full_path, _ = qtw.QFileDialog.getOpenFileName(
            self,
            self.tr("Select Private Key File"),
            "",
            self.tr("PEM Files (*.pem);;All Files (*)"),
        )

        if not private_key_full_path:
            return

        self.private_key_full_path = private_key_full_path
        self.private_key_path_le.setText(t.all.format_input_path(private_key_full_path))

    @qtc.Slot()
    def password_cb_handler(self, status):
        """
        Slot connected to the password checkbox's state changed signal.
        This slot sets the enabled status of the password input field based on the
        checkbox state. If the checkbox is unchecked, it clears the password input
        field.
        """
        self.password_le.setEnabled(status)

        if not status:
            self.password_le.clear()

    @qtc.Slot()
    def pub_key_select_btn_handler(self):
        """
        Slot connected to the public key selection button's clicked signal.
        This slot opens a file dialog where the user can select a path to save the public key.
        If the user selects a path, it updates the public_key_save_path attribute and sets
        the text of the pub_key_path_le to the selected file path.
        """

        public_key_save_path, _ = qtw.QFileDialog.getSaveFileName(
            self,
            self.tr("Save Your Public Key"),
            self.tr("public_key.pem"),
            self.tr("PEM Files (*.pem);;All Files (*)"),
        )
        if not public_key_save_path:
            return

        self.public_key_save_path = public_key_save_path
        self.pub_key_path_le.setText(t.all.format_input_path(self.public_key_save_path))

    @qtc.Slot()
    def generate_button_status_checker(self):
        """
        Slot connected to the text changed signal of the private key path input and public key path input
        and the state changed signal of the password checkbox.
        This slot sets the enabled status of the "Generate" button based on the following conditions:
        1.  The user has entered a private key path in the private key path input.
        2.  The user has entered a public key path in the public key path input.
        3.  If the user has checked the "Password protect the private key" checkbox,
            the user must have entered a password in the password input field.
        """
        self.generate_btn.setEnabled(
            all(
                [
                    self.private_key_path_le.text(),
                    self.pub_key_path_le.text(),
                    not self.password_cb.isChecked() or self.password_le.text(),
                ]
            )
        )

    @qtc.Slot()
    def process_keygen(self):
        """
        Slot connected to the "Generate" button's clicked signal.
        This slot will load the private key from the file path entered in the
        private key path input field, encrypt the private key with the provided
        password (if any), generate the public key from the private key, and
        save the public key to the file path entered in the public key path input
        field. It displays a success message upon successful generation and
        saving of the public key and closes the current window.

        :return: None
        """
        if self.password_cb.isChecked():
            self.password = self.password_le.text()

        self.key_manager = RsaKeyManager()
        try:
            private_key = self.key_manager.load_private_key_from_file(
                self.private_key_full_path, self.password
            )
            public_key = self.key_manager.generate_public_key(private_key)

            logging.info(f"Private Key: { private_key}")

            logging.info(f"Public Key: {public_key}")

            self.key_manager.save_public_key_to_file(
                public_key, self.public_key_save_path
            )

            qtw.QMessageBox.information(
                self,
                self.tr("Success"),
                self.tr("Your public key was successfully generated and saved."),
            )

            self.close()

        except Exception as e:
            qtw.QMessageBox.critical(self, self.tr("Error"), self.tr(f"{e}"))
            self.password_le.clear()
            self.password = None
            return

    def closeEvent(self, event):
        """
        Reimplements the closeEvent method to show the main window when this
        window is closed. It retrieves the main window from the saved data using
        the signal manager, centers it using the toolkit, shows the main window,
        and accepts the close event to proceed with closing the current window.

        :param event: The close event that triggered this method.
        """

        window = t.qt.center_widget(signal_manager.saved_data["save_main_window"])
        window.show()
        event.accept()
