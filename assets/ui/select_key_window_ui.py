# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'select_key_window.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
import assets.ui.icons_rc


class Ui_KeyInputForm(object):
    def setupUi(self, KeyInputForm):
        if not KeyInputForm.objectName():
            KeyInputForm.setObjectName("KeyInputForm")
        KeyInputForm.setEnabled(True)
        KeyInputForm.resize(719, 577)
        icon = QIcon()
        icon.addFile(
            ":/favicon/icons/maze.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        KeyInputForm.setWindowIcon(icon)
        KeyInputForm.setWindowOpacity(1.000000000000000)
        KeyInputForm.setStyleSheet(
            "QWidget {\n"
            "	background-color: #263238;\n"
            "	color: rgb(172, 215, 245);\n"
            "}\n"
            "\n"
            "QLineEdit, QTextEdit {\n"
            "	background-color: rgb(50, 66, 74);\n"
            "	font-size: 18px;\n"
            "}\n"
            "\n"
            "QAbstractButton {\n"
            "	font-size: 19px\n"
            "}"
        )
        self.verticalLayout = QVBoxLayout(KeyInputForm)
        self.verticalLayout.setObjectName("verticalLayout")
        self.file_radio = QRadioButton(KeyInputForm)
        self.file_radio.setObjectName("file_radio")
        self.file_radio.setStyleSheet("color: rgb(172, 215, 245);")
        icon1 = QIcon()
        icon1.addFile(
            ":/windows_icons/icons/encrypt.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.file_radio.setIcon(icon1)
        self.file_radio.setIconSize(QSize(25, 25))
        self.file_radio.setChecked(True)

        self.verticalLayout.addWidget(self.file_radio)

        self.file_layout = QHBoxLayout()
        self.file_layout.setObjectName("file_layout")
        self.file_path_input = QLineEdit(KeyInputForm)
        self.file_path_input.setObjectName("file_path_input")
        self.file_path_input.setEnabled(False)
        self.file_path_input.setStyleSheet("border-radius: 3px;")

        self.file_layout.addWidget(self.file_path_input)

        self.browse_button = QPushButton(KeyInputForm)
        self.browse_button.setObjectName("browse_button")
        self.browse_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.browse_button.setStyleSheet(
            "#browse_button {\n"
            "	background-color: #007d9c;\n"
            "	color: #005568;\n"
            "	font-size: 18px\n"
            "}\n"
            "\n"
            "#next_button:hover {\n"
            "	background-color: #00a3c8;\n"
            "}"
        )
        icon2 = QIcon()
        icon2.addFile(
            ":/windows_icons/icons/search.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.browse_button.setIcon(icon2)

        self.file_layout.addWidget(self.browse_button)

        self.verticalLayout.addLayout(self.file_layout)

        self.text_radio = QRadioButton(KeyInputForm)
        self.text_radio.setObjectName("text_radio")
        self.text_radio.setIcon(icon1)
        self.text_radio.setIconSize(QSize(25, 25))

        self.verticalLayout.addWidget(self.text_radio)

        self.key_text_area = QTextEdit(KeyInputForm)
        self.key_text_area.setObjectName("key_text_area")
        self.key_text_area.setEnabled(True)
        self.key_text_area.viewport().setProperty(
            "cursor", QCursor(Qt.CursorShape.ArrowCursor)
        )
        self.key_text_area.setStyleSheet("border-radius: 10px;")

        self.verticalLayout.addWidget(self.key_text_area)

        self.next_button = QPushButton(KeyInputForm)
        self.next_button.setObjectName("next_button")
        self.next_button.setEnabled(False)
        self.next_button.setMinimumSize(QSize(0, 100))
        self.next_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.next_button.setStyleSheet(
            "#next_button {\n"
            "	background-color: #007d9c;\n"
            "	color: #005568;\n"
            "	font-size: 32px;\n"
            "}\n"
            "\n"
            "#next_button:hover {\n"
            "	background-color: #00a3c8;\n"
            "}"
        )
        icon3 = QIcon()
        icon3.addFile(
            ":/windows_icons/icons/next.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.next_button.setIcon(icon3)
        self.next_button.setIconSize(QSize(30, 30))

        self.verticalLayout.addWidget(self.next_button)

        self.retranslateUi(KeyInputForm)

        QMetaObject.connectSlotsByName(KeyInputForm)

    # setupUi

    def retranslateUi(self, KeyInputForm):
        KeyInputForm.setWindowTitle(
            QCoreApplication.translate(
                "KeyInputForm", "[PLACEHOLDER] | Select Key", None
            )
        )
        self.file_radio.setText(
            QCoreApplication.translate(
                "KeyInputForm", "Load Your Key from File [PLACEHOLDER]", None
            )
        )
        self.file_path_input.setPlaceholderText(
            QCoreApplication.translate(
                "KeyInputForm", "Path to your key file...[PLACEHOLDER]", None
            )
        )
        self.browse_button.setText(
            QCoreApplication.translate("KeyInputForm", "Browse...", None)
        )
        self.text_radio.setText(
            QCoreApplication.translate(
                "KeyInputForm", "Enter Your Key Manually [PLACEHOLDER]", None
            )
        )
        self.key_text_area.setPlaceholderText(
            QCoreApplication.translate(
                "KeyInputForm", "Enter your key here...[PLACEHOLDER]", None
            )
        )
        self.next_button.setText(
            QCoreApplication.translate("KeyInputForm", "Next", None)
        )

    # retranslateUi
