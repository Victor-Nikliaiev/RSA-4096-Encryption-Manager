import os
import sys
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg
from PySide6 import QtUiTools as qtu
from assets.ui import Ui_KeyInputForm
from backend.key_manager import load_public_key_from_file, serialize_public_key
from backend import signal
from tools.toolkit import Tools as t


class ChoosePublicKeyWindow(qtw.QWidget, Ui_KeyInputForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Encryption | Choose a public key")
        self.update_ui()

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
            file_path, file_name = os.path.split(full_file_path)

            formatted_file_path = self.format_file_path_input(file_path)
            formatted_file_name = self.format_file_name(file_name)
            self.file_path_input.setText(
                os.path.join(formatted_file_path, formatted_file_name)
            )

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
                self.public_key = load_public_key_from_file(file_path)
            except Exception as e:
                qtw.QMessageBox.critical(self, "Unsupported File Detected", f"{e}")
                return
        else:
            input_public_key = self.key_text_area.toPlainText().strip()
            if self.validate_public_key(input_public_key):
                try:
                    self.public_key = serialize_public_key(input_public_key)
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

        qtw.QMessageBox.information(self, "Success", "Public key loaded successfully!")
        self.process_public_key()

    def validate_public_key(self, key: str) -> bool:
        # Replace this placeholder logic with actual key validation
        return "BEGIN PUBLIC KEY" in key and "END PUBLIC KEY" in key

    def process_public_key(self):
        signal.public_key_accepted.emit(self.public_key)
        print("Public Key:", self.public_key)

        # Perform encryption or further actions with the loaded key

    def format_file_path_input(self, file_path):
        if len(file_path) > 30:
            return f"{file_path[:28]}..."
        return file_path

    def format_file_name(self, file_name):
        if len(file_name) > 30:
            return f"{file_name[:14]}...{file_name[-14:]}"
        return file_name
