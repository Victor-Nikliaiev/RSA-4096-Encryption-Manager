import sys
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg
from PySide6 import QtUiTools as qtu
from assets.ui.keygen import Ui_PrivateKeyPairGenerator
from backend import RsaKeyManager, signal_manager
from tools.toolkit import Tools as t


class PrivateKeygenScreen(qtw.QWidget, Ui_PrivateKeyPairGenerator):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.key_browse_btn.clicked.connect(self.browse_file)
        self.password_cb.clicked.connect(self.password_cb_click_handler)
        self.password_le.textChanged.connect(self.text_changed_handler)
        self.password_repeat_le.textChanged.connect(self.text_changed_handler)
        self.generate_btn.clicked.connect(self.process_keygen)
        self.key_match_lb_text = self.tr("Passwords do not much")
        self.selected_file_path = None

    def browse_file(self):
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

        if not self.password_cb.isChecked():
            self.generate_btn.setEnabled(True)
            return

        if not self.key_match_lb.text():
            self.generate_btn.setEnabled(True)

    def password_cb_click_handler(self):
        if self.password_cb.isChecked():
            self.set_password_fields(True)
            self.key_match_lb.setText(self.key_match_lb_text)
            self.generate_btn.setEnabled(False)
            return

        self.set_password_fields(False)

        if self.selected_file_path:
            self.generate_btn.setEnabled(True)

    def set_password_fields(self, flag):
        self.password_le.setEnabled(flag)
        self.password_repeat_le.setEnabled(flag)

        if not flag:
            print("Clearing passwords...")
            self.password_le.clear()
            self.password_repeat_le.clear()

    def text_changed_handler(self, event):

        if (
            self.password_le.text() != self.password_repeat_le.text()
            or not self.password_le.text()
        ):
            self.key_match_lb.setText(self.key_match_lb_text)
            self.generate_btn.setEnabled(False)
            return

        self.key_match_lb.clear()

        if self.selected_file_path:
            self.generate_btn.setEnabled(True)

    def process_keygen(self):
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
        main_window = t.qt.center_widget(signal_manager.saved_data["save_main_window"])
        main_window.show()
        event.accept()


# Create public and private key for user
# encrypt with public key a file
# put it on server
# then on every enter of user check if his encrypted file match server file
