import sys
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg
from PySide6 import QtUiTools as qtu
from PySide6.QtQuickWidgets import QQuickWidget

from assets.ui import Ui_main_window
from screens import ChooseFileEncryptWindow
from tools.toolkit import Tools as t


class MainWindow(qtw.QMainWindow, Ui_main_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setupQmlLogoAnimation()

        self.actionExit.triggered.connect(qtw.QApplication.quit)
        self.encrypt_button.clicked.connect(self.handle_encrypt)
        self.actionEncrypt.triggered.connect(self.handle_encrypt)

    def setupQmlLogoAnimation(self):
        qml_widget = QQuickWidget(self)
        qml_widget.setSource(qtc.QUrl.fromLocalFile("assets/ui/animation.qml"))
        qml_widget.setResizeMode(QQuickWidget.SizeRootObjectToView)
        layout = qtw.QVBoxLayout(self.q_logo)
        layout.addWidget(qml_widget)
        self.q_logo.setLayout(layout)

    @qtc.Slot()
    def handle_encrypt(self):
        print("Encrypt button or menu clicked")
        self.encrypt_window = t.qt.center_widget(ChooseFileEncryptWindow())
        self.encrypt_window.show()


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)

    window = t.qt.center_widget(MainWindow())
    window.show()
    sys.exit(app.exec())
