import sys
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg
from PySide6 import QtUiTools as qtu
from PySide6.QtQuickWidgets import QQuickWidget

from assets.ui import Ui_main_window
from assets.ui import GlowingLogo
from screens.encryption import ChooseFileEncryptScreen
from screens.decryption import ChooseFileDecryptScreen
from tools.toolkit import Tools as t
from backend import signal_manager


class MainWindow(qtw.QMainWindow, Ui_main_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setupWebLogoAnimation()

        self.actionExit.triggered.connect(qtw.QApplication.quit)
        self.encrypt_button.clicked.connect(self.handle_encrypt)
        self.actionEncrypt.triggered.connect(self.handle_encrypt)
        self.decrypt_button.clicked.connect(self.handle_decrypt)
        self.actionDecrypt.triggered.connect(self.handle_decrypt)

    def setupWebLogoAnimation(self):
        # qml_widget = QQuickWidget(self)
        # qml_widget.setSource(qtc.QUrl.fromLocalFile("assets/ui/animation.qml"))
        # qml_widget.setResizeMode(QQuickWidget.SizeRootObjectToView)

        glowing_log = GlowingLogo()

        layout = qtw.QVBoxLayout(self.q_logo)
        layout.addWidget(glowing_log)
        self.q_logo.setLayout(layout)

    @qtc.Slot()
    def handle_encrypt(self):
        print("Encrypt button or menu clicked")
        self.encrypt_window = t.qt.center_widget(ChooseFileEncryptScreen())
        signal_manager.save_main_window.emit(self)
        self.close()
        self.encrypt_window.show()

    @qtc.Slot()
    def handle_decrypt(self):
        print("Decrypt button or menu clicked")
        self.decrypt_window = t.qt.center_widget(ChooseFileDecryptScreen())
        signal_manager.save_main_window.emit(self)
        self.close()
        self.decrypt_window.show()


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)

    window = t.qt.center_widget(MainWindow())
    window.show()
    sys.exit(app.exec())
