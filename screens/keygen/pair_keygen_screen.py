from assets.ui.keygen import Ui_PrivateKeyPairGenerator
from backend import RsaKeyManager, signal_manager
from PySide6 import QtWidgets as qtw
from tools.toolkit import Tools as t
from PySide6 import QtCore as qtc


class PairKeygenScreen(qtw.QWidget, Ui_PrivateKeyPairGenerator):
    def __init__(self):
        """
        Initializes the PairKeygenScreen widget.

        This constructor sets up the user interface, updates the UI based on the
        settings, and connects various UI elements to their respective event handlers,
        including buttons and input fields. It also initializes the state of the
        password match label and the selected file path.
        """

        super().__init__()
        self.setupUi(self)
        self.update_ui()

        self.key_browse_btn.clicked.connect(self.browse_file)
        self.password_cb.clicked.connect(self.password_cb_click_handler)
        self.password_le.textChanged.connect(self.text_changed_handler)
        self.password_repeat_le.textChanged.connect(self.text_changed_handler)
        self.generate_btn.clicked.connect(self.process_keygen)

        self.key_match_lb_text = self.tr("Passwords do not much")
        self.selected_file_path = None

    def update_ui(self):
        """
        Updates the user interface of the PairKeygenScreen widget.

        This method sets the window title, sets the text of UI elements,
        and sets the placeholder text of the input field based on the
        translation context.
        """
        self.setWindowTitle(
            self.tr("Key Generation | Select location to generate your keys")
        )
        self.top_lb.setText(
            self.tr("Select location to generate your private and public keys:")
        )
        self.location_info_btn.setText(self.tr("  Select location to save your keys:"))
        self.key_path_le.setPlaceholderText(
            self.tr('Click "Select" to choose location to save your keys')
        )

    @qtc.Slot()
    def browse_file(self):
        """
        Slot connected to the "Browse" button's clicked signal.
        This slot opens a file dialog where the user can select a path
        to save their private and public keys. If the user selects a
        path, it updates the selected_file_path attribute and sets the
        text of the key_path_le to the selected file path. It also
        emits a signal to the signal manager with the selected file
        path. Finally, it sets the enabled status of the "Generate" button
        based on the status of the password protection checkbox and the
        password match label.
        """
        full_file_path, _ = qtw.QFileDialog.getSaveFileName(
            self,
            self.tr("Save Your Keys"),
            self.tr("my_keys.zip"),
            self.tr("ZIP Files (*.zip);;All Files (*)"),
        )

        if not full_file_path:
            return

        self.selected_file_path = full_file_path
        self.key_path_le.setText(t.all.format_input_path(full_file_path))
        signal_manager.saved_file_path.emit(full_file_path)

        self.generate_btn.setEnabled(
            any([not self.password_cb.isChecked(), not self.key_match_lb.text()])
        )

    @qtc.Slot(bool)
    def password_cb_click_handler(self, checkbox_state):
        """
        Slot connected to the "Password protect the private key" checkbox's
        state changed signal.
        This slot sets the enabled status of the password and password repeat
        input fields based on the checkbox state. If the checkbox is checked,
        it sets the text of the key match label to the key match label text
        and sets the enabled status of the "Generate" button to False. If the
        checkbox is unchecked and a file path has been selected, it sets the
        enabled status of the "Generate" button to True.
        """
        self.set_password_fields(checkbox_state)

        if checkbox_state:
            self.key_match_lb.setText(self.key_match_lb_text)
            self.generate_btn.setEnabled(False)
            return

        if self.selected_file_path:
            self.generate_btn.setEnabled(True)

    def set_password_fields(self, checkbox_state):
        """
        Updates the enabled status of the password input fields based on the checkbox state.

        If the checkbox is checked, both the password and repeat password line edits are enabled.
        If the checkbox is unchecked, the fields are disabled and cleared, and the key match label
        is also cleared.

        :param checkbox_state: A boolean indicating whether the password fields should be enabled or not.
        """

        self.password_le.setEnabled(checkbox_state)
        self.password_repeat_le.setEnabled(checkbox_state)

        if not checkbox_state:
            self.password_le.clear()
            self.password_repeat_le.clear()
            self.key_match_lb.clear()

    @qtc.Slot()
    def text_changed_handler(self, event):
        """
        Slot connected to the text changed signal of the password and repeat password
        input fields. This slot checks if the password match and if the password is
        not empty. If the password match or the password is empty, the method sets
        the text of the key match label to the key match label text and sets the
        enabled status of the "Generate" button to False. If the password match and
        the password is not empty, the method clears the key match label and sets
        the enabled status of the "Generate" button to True if a file path has been
        selected.
        """

        password_match = self.password_le.text() == self.password_repeat_le.text()
        if not password_match or not self.password_le.text():
            self.key_match_lb.setText(self.key_match_lb_text)
            self.generate_btn.setEnabled(False)
            return

        self.key_match_lb.clear()
        self.generate_btn.setEnabled(bool(self.selected_file_path))

    @qtc.Slot()
    def process_keygen(self):
        """
        Slot connected to the "Generate" button's clicked signal.
        This slot generates a pair of RSA keys (private and public),
        encrypts them using the provided password if the password protection
        checkbox is checked, and exports the keys as a ZIP file to the selected
        file path. A success message is displayed upon successful generation
        and export of the keys, and the current window is closed.

        :return: None
        """

        password = None

        if self.password_cb.isChecked():
            password = self.password_le.text()

        self.key_manager = RsaKeyManager()

        private_key = self.key_manager.generate_private_key()
        public_key = self.key_manager.generate_public_key(private_key)
        private_pem = self.key_manager.encrypt_private_key(private_key, password)
        public_key_pem = self.key_manager.encrypt_public_key(public_key)

        self.key_manager.export_keys_to_zip(
            private_pem, public_key_pem, self.selected_file_path
        )

        qtw.QMessageBox.information(
            self, self.tr("Success"), self.tr("Your keys were generated successfully.")
        )
        self.close()

    def closeEvent(self, event):
        """
        Overrides the default close event handler to show the main window
        that started the keygen process before closing the current window.
        This is necessary to ensure that the main window is shown again
        after the user closes the PairKeygenScreen.

        :param event: The close event that triggered this method.
        """
        main_window = t.qt.center_widget(signal_manager.saved_data["save_main_window"])
        main_window.show()
        event.accept()
