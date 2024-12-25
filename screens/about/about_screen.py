from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from backend import signal_manager
from tools.toolkit import Tools as t
from assets.ui.about import Ui_About


class AboutScreen(qtw.QWidget, Ui_About):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.update_ui()
        self.install_event_listeners()

    def update_ui(self):
        """
        Set up the UI for the AboutScreen.

        This method sets up the window flags, size policies, and scroll area for the
        AboutScreen.
        """
        self.setWindowFlags(qtc.Qt.FramelessWindowHint | qtc.Qt.Window)
        self.label_3.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Preferred)
        self.scrollArea = qtw.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.label_3)
        self.verticalLayout_2.addWidget(self.scrollArea)

    def install_event_listeners(self):
        """
        Install event listeners for the AboutScreen's widgets.

        This method installs event listeners for the following widgets: app_name_lb,
        label, label_2, label_3, and frame. The event listeners are used to detect
        mouse clicks and close the window when a mouse click is detected.
        """
        self.app_name_lb.installEventFilter(self)
        self.label.installEventFilter(self)
        self.label_2.installEventFilter(self)
        self.label_3.installEventFilter(self)
        self.frame.installEventFilter(self)

    def mousePressEvent(self, event):
        """
        Close the AboutScreen when a mouse button is clicked.

        This method is an event handler for the mousePressEvent signal. It is called
        when a mouse button is clicked anywhere on the AboutScreen. It closes the
        AboutScreen when called.

        Parameters
        ----------
        event : QMouseEvent
            The mouse press event that triggered the method.

        """
        self.close()

    def closeEvent(self, event):
        """
        Handle the close event for the AboutScreen.

        This method is triggered when the AboutScreen is closed. It retrieves the main
        window from the saved data using the signal manager, centers it using the toolkit,
        shows the main window, and accepts the close event to proceed with closing the
        AboutScreen.

        Parameters
        ----------
        event : QCloseEvent
            The close event that triggered this method.
        """

        main_window = t.qt.center_widget(signal_manager.saved_data["save_main_window"])
        main_window.show()
        event.accept()
