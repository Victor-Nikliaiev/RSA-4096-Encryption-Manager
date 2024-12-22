from assets.ui.keygen import Ui_SelectKeygen
import sys
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg
from PySide6 import QtUiTools as qtu
from backend import signal_manager

from screens.keygen.pair_keygen_screen import PairKeygenScreen
from screens.keygen.private_keygen_screen import PrivateKeygenScreen
from screens.keygen.public_keygen_screen import PublicKeygenScreen
from tools.toolkit import Tools as t


class SelectKeygenScreen(qtw.QWidget, Ui_SelectKeygen):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show_next_screen = False

        self.next_button.clicked.connect(self.click_next_handler)

        self.gen_priv_key_rb.clicked.connect(
            lambda: signal_manager.selected_option.emit("private")
        )
        self.gen_pub_key_rb.clicked.connect(
            lambda: signal_manager.selected_option.emit("public")
        )
        self.gen_key_pair_rb.clicked.connect(
            lambda: signal_manager.selected_option.emit("key_pair")
        )

        signal_manager.selected_option.connect(self.selected_option_handler)

    def click_next_handler(self):
        screenOptions = {
            "private": PrivateKeygenScreen,
            "public": PublicKeygenScreen,
            "key_pair": PairKeygenScreen,
        }

        selectedOption = signal_manager.saved_data.get("selected_option")
        if screenOptions.get(selectedOption):
            self.next_screen = screenOptions.get(selectedOption)()
            t.qt.center_widget(self.next_screen).show()
            self.show_next_screen = True
            self.close()
        else:
            sys.exit(1)

    def selected_option_handler(self):
        self.next_button.setEnabled(True)

    def closeEvent(self, event):
        if self.show_next_screen:
            event.accept()
            return

        signal_manager.saved_data.get("save_main_window").show()
        event.accept()
