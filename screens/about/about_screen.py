import sys
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg
from PySide6 import QtUiTools as qtu
from backend import signal_manager
from tools.toolkit import Tools as t
from assets.ui.about import Ui_About


class AboutScreen(qtw.QWidget, Ui_About):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.update_ui()

        self.app_name_lb.installEventFilter(self)
        self.label.installEventFilter(self)
        self.label_2.installEventFilter(self)
        self.label_3.installEventFilter(self)
        self.frame.installEventFilter(self)

    def update_ui(self):
        self.setWindowFlags(qtc.Qt.FramelessWindowHint | qtc.Qt.Window)
        self.label_3.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Preferred)
        self.scrollArea = qtw.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.label_3)
        self.verticalLayout_2.addWidget(self.scrollArea)

    def mousePressEvent(self, event):
        self.close()

    def closeEvent(self, event):
        main_window = t.qt.center_widget(signal_manager.saved_data["save_main_window"])
        main_window.show()
        event.accept()
