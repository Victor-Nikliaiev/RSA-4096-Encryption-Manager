import os
import sys
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg
from PySide6 import QtUiTools as qtu
from assets.ui import Ui_KeyInputForm


# from backend.key_manager import load_public_key_from_file, serialize_public_key
from backend import signal_manager
from screens.save_file_encrypt_screen import SaveFileEncryptScreen
from tools.toolkit import Tools as t
from backend import RsaKeyManager


class ChoosePublicKeyScreen(qtw.QWidget, Ui_KeyInputForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Encryption | Choose a public key")
        self.update_ui()

        self.key_manager = RsaKeyManager()

        self.browse_button.clicked.connect(self.browse_file)
        self.next_button.clicked.connect(self.handle_click_next)
        self.file_radio.toggled.connect(self.toggle_input_mode)
        self.selected_file = None

        self.key_text_area.textChanged.connect(self.update_next_button_status)
        self.file_path_input.textChanged.connect(self.update_next_button_status)

    def update_ui(self):
        self.browse_button.setEnabled(True)
        self.key_text_area.setEnabled(False)
        self.file_radio.setText("Load public key from file")
        self.text_radio.setText("Enter public key manually")
        self.file_path_input.setPlaceholderText(
            "Browse for a public key file (the path will be generated automatically)..."
        )
        self.key_text_area.setPlaceholderText("Enter your public key here...")

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
            self, "Select Public Key File", "", "PEM Files (*.pem);;All Files (*)"
        )
        if full_file_path:
            self.selected_file_path = full_file_path
            self.file_path_input.setText(t.all.format_input_path(full_file_path))

    def update_next_button_status(self):
        if self.file_path_input.text() or self.key_text_area.toPlainText():
            self.next_button.setEnabled(True)
        else:
            self.next_button.setEnabled(False)

    def handle_click_next(self):
        if self.file_radio.isChecked():
            file_path = self.selected_file_path.strip()
            if not file_path:
                qtw.QMessageBox.warning(self, "Error", "Please select a valid file.")
                return
            try:
                self.public_key = self.key_manager.load_public_key_from_file(file_path)
            except Exception as e:
                qtw.QMessageBox.critical(self, "Unsupported File Detected", f"{e}")
                return
        else:
            input_public_key = self.key_text_area.toPlainText().strip()
            if self.validate_public_key(input_public_key):
                try:
                    self.public_key = self.key_manager.serialize_public_key(
                        input_public_key
                    )
                except Exception as e:
                    qtw.QMessageBox.critical(self, "Key Format Error", f"{e}")
                    return
            else:
                qtw.QMessageBox.warning(
                    self,
                    "Key Format Error",
                    "Please enter a valid public key to proceed",
                )
                return

        self.process_public_key()

    def validate_public_key(self, key: str) -> bool:
        # Replace this placeholder logic with actual key validation
        return "BEGIN PUBLIC KEY" in key and "END PUBLIC KEY" in key

    def process_public_key(self):
        signal_manager.public_key_accepted.emit(self.public_key)
        print("Public Key:", self.public_key)
        self.save_file_encrypt_screen = t.qt.center_widget(SaveFileEncryptScreen())
        self.save_file_encrypt_screen.show()
        self.destroy()

    def closeEvent(self, event):
        signal_manager.saved_data.get("save_main_window").show()
