# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'choose_file_window.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)
import icons_rc

class Ui_choose_file_window_ui(object):
    def setupUi(self, choose_file_window_ui):
        if not choose_file_window_ui.objectName():
            choose_file_window_ui.setObjectName(u"choose_file_window_ui")
        choose_file_window_ui.setWindowModality(Qt.WindowModality.ApplicationModal)
        choose_file_window_ui.resize(719, 577)
        icon = QIcon()
        icon.addFile(u":/favicon/icons/maze.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        choose_file_window_ui.setWindowIcon(icon)
        choose_file_window_ui.setStyleSheet(u"color: rgb(119, 186, 198);\n"
"background-color: #263238;")
        self.verticalLayout = QVBoxLayout(choose_file_window_ui)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.drop_and_drag_widget = QWidget(choose_file_window_ui)
        self.drop_and_drag_widget.setObjectName(u"drop_and_drag_widget")
        self.drop_and_drag_widget.setMinimumSize(QSize(0, 300))

        self.verticalLayout.addWidget(self.drop_and_drag_widget)

        self.label = QLabel(choose_file_window_ui)
        self.label.setObjectName(u"label")
        self.label.setEnabled(True)
        font = QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.next_button = QPushButton(choose_file_window_ui)
        self.next_button.setObjectName(u"next_button")
        self.next_button.setEnabled(False)
        self.next_button.setMinimumSize(QSize(0, 100))
        font1 = QFont()
        font1.setBold(True)
        font1.setItalic(False)
        self.next_button.setFont(font1)
        self.next_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.next_button.setStyleSheet(u"#next_button {\n"
"	background-color: #007d9c;\n"
"	color: #005568;\n"
"	font-size: 32px;\n"
"}\n"
"\n"
"#next_button:hover {\n"
"	background-color: #00a3c8;\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u":/windows_icons/icons/next.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.next_button.setIcon(icon1)
        self.next_button.setIconSize(QSize(28, 28))

        self.verticalLayout.addWidget(self.next_button)


        self.retranslateUi(choose_file_window_ui)

        QMetaObject.connectSlotsByName(choose_file_window_ui)
    # setupUi

    def retranslateUi(self, choose_file_window_ui):
        choose_file_window_ui.setWindowTitle("")
        self.label.setText(QCoreApplication.translate("choose_file_window_ui", u"Please choose a file and click \"Next\" button", None))
        self.next_button.setText(QCoreApplication.translate("choose_file_window_ui", u"Next", None))
    # retranslateUi

