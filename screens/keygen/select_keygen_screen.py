from assets.ui.keygen import Ui_SelectKeygen
import sys
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg
from PySide6 import QtUiTools as qtu
from backend import signal_manager
from tools.toolkit import Tools as t


class SelectKeygenScreen(qtw.QWidget, Ui_SelectKeygen):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

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
        print(
            "Next is clicked, selected option is: ",
            signal_manager.saved_data["selected_option"],
        )

    def selected_option_handler(self):
        self.next_button.setEnabled(True)
