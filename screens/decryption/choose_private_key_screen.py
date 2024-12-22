from PySide6 import QtWidgets as qtw
from assets.ui import Ui_KeyInputForm
from backend import signal_manager
from screens.decryption.save_file_decrypt_screen import SaveFileDecryptScreen
from tools.toolkit import Tools as t
from backend import RsaKeyManager


class ChoosePrivateKeyScreen(qtw.QWidget, Ui_KeyInputForm):
    def __init__(self):
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
        self.setWindowTitle("Decryption | Choose a private key")
        self.browse_button.setEnabled(True)
        self.key_text_area.setEnabled(False)
        self.file_radio.setText("Load private key from file")
        self.text_radio.setText("Enter private key manually")
        self.file_path_input.setPlaceholderText(
            "Browse for a private key file (the path will be generated automatically)..."
        )
        self.key_text_area.setPlaceholderText("Enter your private key here...")

    def toggle_input_mode(self):
        if self.file_radio.isChecked():
            self.browse_button.setEnabled(True)
            self.key_text_area.setEnabled(False)
            self.key_text_area.clear()
        else:
            self.browse_button.setEnabled(False)
            self.key_text_area.setEnabled(True)
            self.file_path_input.clear()
            self.selected_file_path = None

    def browse_file(self):
        full_file_path, _ = qtw.QFileDialog.getOpenFileName(
            self, "Select Private Key File", "", "PEM Files (*.pem);;All Files (*)"
        )
        if full_file_path:
            self.selected_file_path = full_file_path
            self.file_path_input.setText(t.all.format_input_path(full_file_path))

    def update_next_button_status(self):
        self.next_button.setEnabled(
            all(
                [
                    self.file_path_input.text() or self.key_text_area.toPlainText(),
                    not self.is_password_protected_cb.isChecked()
                    or self.password_lineEdit.text(),
                ]
            )
        )

    def handle_click_next(self):
        password = None
        if self.is_password_protected_cb.isChecked():
            password = self.password_lineEdit.text()

        if self.file_radio.isChecked():
            file_path = self.selected_file_path.strip()
            if not file_path:
                qtw.QMessageBox.warning(self, "Error", "Please select a valid file.")
                return
            try:
                self.private_key = self.key_manager.load_private_key_from_file(
                    file_path, password
                )
            except Exception as e:
                qtw.QMessageBox.critical(self, "Unsupported File Detected", f"{e}")
                return
        else:
            input_private_key = self.key_text_area.toPlainText().strip()
            if self.validate_private_key(input_private_key):
                try:
                    self.private_key = self.key_manager.serialize_private_key(
                        input_private_key, password
                    )
                except Exception as e:
                    qtw.QMessageBox.critical(self, "Key Format Error", f"{e}")
                    return
            else:
                qtw.QMessageBox.warning(
                    self,
                    "Private Key Format Error",
                    "Please enter a valid private key to proceed",
                )
                return

        self.process_private_key()

    def validate_private_key(self, key: str) -> bool:
        return "BEGIN PRIVATE KEY" in key and "END PRIVATE KEY" in key

    def process_private_key(self):
        signal_manager.private_key_accepted.emit(self.private_key)
        print("Private Key:", self.private_key)

        self.save_file_decrypt_screen = t.qt.center_widget(SaveFileDecryptScreen())
        self.save_file_decrypt_screen.show()
        self.destroy()

    def handle_password_input_accessability(self):
        self.password_lineEdit.setEnabled(self.is_password_protected_cb.isChecked())
        if not self.is_password_protected_cb.isChecked():
            self.password_lineEdit.clear()

    def closeEvent(self, event):
        signal_manager.saved_data.get("save_main_window").show()
