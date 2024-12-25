from assets.ui.keygen import Ui_PrivateKeyPairGenerator
from backend import RsaKeyManager, signal_manager
from PySide6 import QtWidgets as qtw
from tools.toolkit import Tools as t
from PySide6 import QtCore as qtc


class PrivateKeygenScreen(
    qtw.QWidget,
    Ui_PrivateKeyPairGenerator,
):
    def __init__(self):
        """
        Initializes the PrivateKeygenScreen widget.

        This constructor sets up the user interface and connects various UI elements
        to their respective event handlers, such as buttons and input fields. It
        initializes the state of the password match label and the selected file path.
        """

        super().__init__()
        self.setupUi(self)

        self.key_browse_btn.clicked.connect(self.browse_file)
        self.password_cb.clicked.connect(self.password_cb_click_handler)
        self.password_le.textChanged.connect(self.text_changed_handler)
        self.password_repeat_le.textChanged.connect(self.text_changed_handler)
        self.generate_btn.clicked.connect(self.process_keygen)
        self.key_match_lb_text = self.tr("Passwords do not much")
        self.selected_file_path = None

    @qtc.Slot()
    def browse_file(self):
        """
        Slot connected to the "Browse" button's clicked signal.
        This slot opens a file dialog where the user can select a path
        to save their private key. If the user selects a path, it updates
        the selected_file_path attribute and sets the text of the key_path_le
        to the selected file path. It also emits a signal to the signal manager
        with the selected file path. Finally, it sets the enabled status of the
        "Generate" button based on the status of the password protection checkbox
        and the password match label.
        """
        full_file_path, _ = qtw.QFileDialog.getSaveFileName(
            self,
            self.tr("Save Private File"),
            self.tr("private_key.pem"),
            self.tr("PEM Files (*.pem);;All Files (*)"),
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

    def set_password_fields(self, flag):
        """
        Enables/disables the password and password repeat input fields based on the given flag.

        If the flag is False, the method also clears the password and password repeat input fields
        and the key match label.

        :param flag: A boolean indicating whether to enable or disable the password input fields.
        """
        self.password_le.setEnabled(flag)
        self.password_repeat_le.setEnabled(flag)

        if not flag:
            self.password_le.clear()
            self.password_repeat_le.clear()
            self.key_match_lb.clear()

    @qtc.Slot()
    def text_changed_handler(self, event):
        """
        Slot connected to the text changed signal of the password and password repeat input fields.
        This slot checks if the password match and if the password is not empty. If the password match
        or the password is empty, the method sets the text of the key match label to the key match
        label text and sets the enabled status of the "Generate" button to False. If the password match
        and the password is not empty, the method clears the key match label and sets the enabled status
        of the "Generate" button to True if a file path has been selected.
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
        Slot connected to the clicked signal of the "Generate" button.
        This slot generates a private key using the RsaKeyManager, encrypts the
        private key with the provided password (if any), and exports the private
        key to a file at the specified file path. It displays a success message
        upon successful generation and export of the key and closes the current
        window.

        :return: None
        """
        password = None

        if self.password_cb.isChecked():
            password = self.password_le.text()

        self.key_manager = RsaKeyManager()

        private_key = self.key_manager.generate_private_key()

        try:
            self.key_manager.save_private_key_to_file(
                self.selected_file_path, password, private_key
            )

            qtw.QMessageBox.information(
                self, self.tr("Success"), self.tr("Private key generated successfully.")
            )
            self.close()

        except Exception as e:
            qtw.QMessageBox.critical(self, self.tr("Error"), self.tr(f"{e}"))

    def closeEvent(self, event):
        """
        Reimplements the closeEvent method to show the main window when
        this window is closed.

        :param event: The close event that triggered this method.
        """

        main_window = t.qt.center_widget(signal_manager.saved_data["save_main_window"])
        main_window.show()
        event.accept()
