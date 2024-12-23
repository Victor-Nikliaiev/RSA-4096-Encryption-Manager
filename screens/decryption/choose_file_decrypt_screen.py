from PySide6.QtWidgets import QWidget
from PySide6 import QtCore as qtc
from assets.ui import Ui_choose_file_window_ui
from components import DragDropWidget
from backend import signal_manager
from tools.toolkit import Tools as t

from screens.decryption.choose_private_key_screen import ChoosePrivateKeyScreen


class ChooseFileDecryptScreen(QWidget, Ui_choose_file_window_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        placeholder_widget = self.findChild(QWidget, "drop_and_drag_widget")
        self.drop_and_drag_widget = DragDropWidget()
        parent_layout = placeholder_widget.parentWidget().layout()
        index = parent_layout.indexOf(placeholder_widget)
        parent_layout.removeWidget(placeholder_widget)
        parent_layout.insertWidget(index, self.drop_and_drag_widget)
        placeholder_widget.hide()

        self.setWindowTitle(self.tr("Decryption | Choose a file"))

        signal_manager.update_next_button_status.connect(self.update_next_button_status)
        self.next_button.clicked.connect(self.handle_click_next)

    @qtc.Slot()
    def handle_click_next(self):
        self.decrypt_window = t.qt.center_widget(ChoosePrivateKeyScreen())
        self.decrypt_window.show()
        self.destroy()

    @qtc.Slot(bool)
    def update_next_button_status(self, status):
        self.next_button.setEnabled(status)

    def closeEvent(self, event):
        signal_manager.saved_data.get("save_main_window").show()
