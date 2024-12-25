from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from assets.ui import Ui_choose_file_window_ui
from components import DragDropWidget
from backend import signal_manager
from tools.toolkit import Tools as t
from screens.decryption.choose_private_key_screen import ChoosePrivateKeyScreen


class ChooseFileDecryptScreen(qtw.QWidget, Ui_choose_file_window_ui):
    def __init__(self):
        """
        Constructor for ChooseFileDecryptScreen.

        This constructor sets up the UI, sets the window title, and connects
        the necessary signals.
        """
        super().__init__()
        self.setupUi(self)

        # Replacing placeholder widget with DragDropWidget
        parent_layout = self.drop_and_drag_widget.parentWidget().layout()
        parent_layout.replaceWidget(self.drop_and_drag_widget, DragDropWidget())

        self.setWindowTitle(self.tr("Decryption | Choose a file"))

        signal_manager.update_next_button_status.connect(self.update_next_button_status)
        self.next_button.clicked.connect(self.handle_click_next)

    @qtc.Slot()
    def handle_click_next(self):
        """
        Slot connected to the "Next" button's clicked signal. This slot
        destroys the current window and creates a ChoosePrivateKeyScreen
        instance, which is then centered and shown.
        """
        self.decrypt_window = t.qt.center_widget(ChoosePrivateKeyScreen())
        self.decrypt_window.show()
        self.destroy()

    @qtc.Slot(bool)
    def update_next_button_status(self, status):
        """
        Slot connected to the update_next_button_status signal. This slot
        updates the enabled status of the "Next" button based on the given
        status that comes from the DragDropWidget.
        """
        self.next_button.setEnabled(status)

    def closeEvent(self, event):
        """
        Reimplements the closeEvent method to show the main window when
        this window is closed.
        """
        signal_manager.saved_data.get("save_main_window").show()
