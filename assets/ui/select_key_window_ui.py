# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'select_key_window.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QRadioButton, QSizePolicy, QTextEdit, QVBoxLayout,
    QWidget)
import icons_rc

class Ui_KeyInputForm(object):
    def setupUi(self, KeyInputForm):
        if not KeyInputForm.objectName():
            KeyInputForm.setObjectName(u"KeyInputForm")
        KeyInputForm.setEnabled(True)
        KeyInputForm.resize(719, 577)
        icon = QIcon()
        icon.addFile(u":/favicon/icons/maze.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        KeyInputForm.setWindowIcon(icon)
        KeyInputForm.setWindowOpacity(1.000000000000000)
        KeyInputForm.setStyleSheet(u"QWidget {\n"
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
"}\n"
"\n"
"QLabel, QGroupBox {\n"
"	font-size: 18px;\n"
"}")
        self.verticalLayout = QVBoxLayout(KeyInputForm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.password_group_layout = QGroupBox(KeyInputForm)
        self.password_group_layout.setObjectName(u"password_group_layout")
        self.verticalLayout_2 = QVBoxLayout(self.password_group_layout)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.is_password_protected_cb = QCheckBox(self.password_group_layout)
        self.is_password_protected_cb.setObjectName(u"is_password_protected_cb")

        self.verticalLayout_2.addWidget(self.is_password_protected_cb)

        self.password_form_layout = QFormLayout()
        self.password_form_layout.setObjectName(u"password_form_layout")
        self.password_lineEdit = QLineEdit(self.password_group_layout)
        self.password_lineEdit.setObjectName(u"password_lineEdit")
        self.password_lineEdit.setEnabled(False)
        self.password_lineEdit.setEchoMode(QLineEdit.EchoMode.Password)

        self.password_form_layout.setWidget(0, QFormLayout.FieldRole, self.password_lineEdit)

        self.label = QLabel(self.password_group_layout)
        self.label.setObjectName(u"label")
        self.label.setEnabled(True)

        self.password_form_layout.setWidget(0, QFormLayout.LabelRole, self.label)


        self.verticalLayout_2.addLayout(self.password_form_layout)


        self.verticalLayout.addWidget(self.password_group_layout)

        self.file_radio = QRadioButton(KeyInputForm)
        self.file_radio.setObjectName(u"file_radio")
        self.file_radio.setStyleSheet(u"color: rgb(172, 215, 245);")
        icon1 = QIcon()
        icon1.addFile(u":/windows_icons/icons/encrypt.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.file_radio.setIcon(icon1)
        self.file_radio.setIconSize(QSize(25, 25))
        self.file_radio.setChecked(True)

        self.verticalLayout.addWidget(self.file_radio)

        self.file_layout = QHBoxLayout()
        self.file_layout.setObjectName(u"file_layout")
        self.file_path_input = QLineEdit(KeyInputForm)
        self.file_path_input.setObjectName(u"file_path_input")
        self.file_path_input.setEnabled(False)
        self.file_path_input.setStyleSheet(u"border-radius: 3px;")

        self.file_layout.addWidget(self.file_path_input)

        self.browse_button = QPushButton(KeyInputForm)
        self.browse_button.setObjectName(u"browse_button")
        self.browse_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.browse_button.setStyleSheet(u"#browse_button {\n"
"	background-color: #007d9c;\n"
"	color: #005568;\n"
"	font-size: 18px\n"
"}\n"
"\n"
"#next_button:hover {\n"
"	background-color: #00a3c8;\n"
"}")
        icon2 = QIcon()
        icon2.addFile(u":/windows_icons/icons/search.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.browse_button.setIcon(icon2)

        self.file_layout.addWidget(self.browse_button)


        self.verticalLayout.addLayout(self.file_layout)

        self.text_radio = QRadioButton(KeyInputForm)
        self.text_radio.setObjectName(u"text_radio")
        self.text_radio.setIcon(icon1)
        self.text_radio.setIconSize(QSize(25, 25))

        self.verticalLayout.addWidget(self.text_radio)

        self.key_text_area = QTextEdit(KeyInputForm)
        self.key_text_area.setObjectName(u"key_text_area")
        self.key_text_area.setEnabled(True)
        self.key_text_area.viewport().setProperty(u"cursor", QCursor(Qt.CursorShape.ArrowCursor))
        self.key_text_area.setStyleSheet(u"border-radius: 10px;")

        self.verticalLayout.addWidget(self.key_text_area)

        self.next_button = QPushButton(KeyInputForm)
        self.next_button.setObjectName(u"next_button")
        self.next_button.setEnabled(False)
        self.next_button.setMinimumSize(QSize(0, 100))
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
        icon3 = QIcon()
        icon3.addFile(u":/windows_icons/icons/next.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.next_button.setIcon(icon3)
        self.next_button.setIconSize(QSize(35, 35))

        self.verticalLayout.addWidget(self.next_button)


        self.retranslateUi(KeyInputForm)

        QMetaObject.connectSlotsByName(KeyInputForm)
    # setupUi

    def retranslateUi(self, KeyInputForm):
        KeyInputForm.setWindowTitle(QCoreApplication.translate("KeyInputForm", u"[PLACEHOLDER] | Select Key", None))
        self.password_group_layout.setTitle(QCoreApplication.translate("KeyInputForm", u"Key Access Control", None))
        self.is_password_protected_cb.setText(QCoreApplication.translate("KeyInputForm", u"Private key is password protected", None))
        self.password_lineEdit.setPlaceholderText(QCoreApplication.translate("KeyInputForm", u"Enter key password here...", None))
        self.label.setText(QCoreApplication.translate("KeyInputForm", u"Enter your password:", None))
        self.file_radio.setText(QCoreApplication.translate("KeyInputForm", u"Load Your Key from File [PLACEHOLDER]", None))
        self.file_path_input.setPlaceholderText(QCoreApplication.translate("KeyInputForm", u"Path to your key file...[PLACEHOLDER]", None))
        self.browse_button.setText(QCoreApplication.translate("KeyInputForm", u"Browse...", None))
        self.text_radio.setText(QCoreApplication.translate("KeyInputForm", u"Enter Your Key Manually [PLACEHOLDER]", None))
        self.key_text_area.setPlaceholderText(QCoreApplication.translate("KeyInputForm", u"Enter your key here...[PLACEHOLDER]", None))
        self.next_button.setText(QCoreApplication.translate("KeyInputForm", u" Next", None))
    # retranslateUi

