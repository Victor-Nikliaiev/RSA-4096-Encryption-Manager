import sys
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg
from PySide6 import QtUiTools as qtu
from assets.ui.keygen import Ui_PublicKeygen
from backend import RsaKeyManager, signal_manager
from tools.toolkit import Tools as t


class PublicKeygenScreen(qtw.QWidget, Ui_PublicKeygen):
    def __init__(self):
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
        self.password: str
        self.operation_completed = False

    def private_key_sel_btn_handler(self):
        private_key_full_path, _ = qtw.QFileDialog.getOpenFileName(
            self, "Select Private Key File", "", "PEM Files (*.pem);;All Files (*)"
        )

        if not private_key_full_path:
            return

        self.private_key_full_path = private_key_full_path
        self.private_key_path_le.setText(t.all.format_input_path(private_key_full_path))

    def password_cb_handler(self, status):
        self.password_le.setEnabled(status)

        if not status:
            self.password_le.clear()

    def pub_key_select_btn_handler(self):
        public_key_save_path, _ = qtw.QFileDialog.getSaveFileName(
            self,
            "Save Your Public Key",
            "public_key.pem",
            "PEM Files (*.pem);;All Files (*)",
        )
        if not public_key_save_path:
            return

        self.public_key_save_path = public_key_save_path
        self.pub_key_path_le.setText(t.all.format_input_path(self.public_key_save_path))
        print(_)

    @qtc.Slot()
    def generate_button_status_checker(self):
        if self.private_key_path_le.text() and self.pub_key_path_le.text():
            if self.password_cb.isChecked():
                if len(self.password_le.text()) > 0:
                    self.generate_btn.setEnabled(True)
                    return
                self.generate_btn.setEnabled(False)
                return
            self.generate_btn.setEnabled(True)
            return
        self.generate_btn.setEnabled(False)

    @qtc.Slot()
    def process_keygen(self):
        if self.password_cb.isChecked():
            self.password = self.password_le.text()

        self.key_manager = RsaKeyManager()
        try:
            private_key = self.key_manager.load_private_key_from_file(
                self.private_key_full_path, self.password
            )
            public_key = self.key_manager.generate_public_key(private_key)

            print("Private Key:", private_key)

            print("Public Key:", public_key)

            self.key_manager.save_public_key_to_file(
                public_key, self.public_key_save_path
            )

            qtw.QMessageBox.information(
                self, "Success", "Your public key was successfully generated and saved."
            )

            self.close()

        except Exception as e:
            qtw.QMessageBox.critical(self, "Error", f"{e}")
            return

    def closeEvent(self, event):
        window = t.qt.center_widget(signal_manager.saved_data["save_main_window"])
        window.show()
        event.accept()
