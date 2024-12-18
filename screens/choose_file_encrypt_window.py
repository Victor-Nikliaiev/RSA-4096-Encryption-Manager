from PySide6.QtWidgets import QWidget
from assets.ui import Ui_choose_file_window_ui
from components import DragDropWidget
from backend import signal
from PySide6 import QtCore as qtc


class ChooseFileEncryptWindow(QWidget, Ui_choose_file_window_ui):
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

        self.setWindowTitle("Encryption | Choose a file")

        signal.file_dropped.connect(self.get_file_path)
        signal.update_next_button_status.connect(self.update_next_button_status)
        self.next_button.clicked.connect(self.handle_click_next)

    @qtc.Slot()
    def handle_click_next(self):
        print("Next was clicked...")
        print(f"dropped one: {self.file_path}")

    @qtc.Slot(str)
    def get_file_path(self, file_path):
        self.file_path = file_path

    @qtc.Slot(bool)
    def update_next_button_status(self, status):
        self.next_button.setEnabled(status)
