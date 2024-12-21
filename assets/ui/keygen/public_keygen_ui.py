# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'public_keygen.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)
import icons_rc

class Ui_PublicKeygen(object):
    def setupUi(self, PublicKeygen):
        if not PublicKeygen.objectName():
            PublicKeygen.setObjectName(u"PublicKeygen")
        PublicKeygen.setEnabled(True)
        PublicKeygen.resize(719, 577)
        icon = QIcon()
        icon.addFile(u":/favicon/icons/maze.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        PublicKeygen.setWindowIcon(icon)
        PublicKeygen.setWindowOpacity(1.000000000000000)
        PublicKeygen.setStyleSheet(u"QWidget {\n"
"	background-color: #263238;\n"
"	color: rgb(172, 215, 245);\n"
"}\n"
"\n"
"QLineEdit {\n"
"	background-color: rgb(50, 66, 74);\n"
"	font-size: 18px;\n"
"	padding: 10px;\n"
"}\n"
"\n"
"QAbstractButton {\n"
"	font-size: 19px\n"
"}")
        self.verticalLayout_4 = QVBoxLayout(PublicKeygen)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_3)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(PublicKeygen)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"background-color: rgb(38, 50, 56);\n"
"color: rgb(49, 169, 196);\n"
"font-size: 25px;\n"
"font-weight: bold;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.groupBox = QGroupBox(PublicKeygen)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.file_layout = QHBoxLayout()
        self.file_layout.setObjectName(u"file_layout")
        self.private_key_path_le = QLineEdit(self.groupBox)
        self.private_key_path_le.setObjectName(u"private_key_path_le")
        self.private_key_path_le.setEnabled(False)
        self.private_key_path_le.setMinimumSize(QSize(0, 50))
        self.private_key_path_le.setStyleSheet(u"border-radius: 3px;")

        self.file_layout.addWidget(self.private_key_path_le)

        self.private_key_sel_btn = QPushButton(self.groupBox)
        self.private_key_sel_btn.setObjectName(u"private_key_sel_btn")
        self.private_key_sel_btn.setMinimumSize(QSize(120, 50))
        self.private_key_sel_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.private_key_sel_btn.setStyleSheet(u"QPushButton {background-color: #007d9c;\n"
"color: #005568;\n"
" }\n"
"\n"
"QPushButton:hover {\n"
"	background-color: #00a3c8;\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u":/windows_icons/icons/next.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.private_key_sel_btn.setIcon(icon1)
        self.private_key_sel_btn.setIconSize(QSize(30, 30))

        self.file_layout.addWidget(self.private_key_sel_btn)


        self.verticalLayout_2.addLayout(self.file_layout)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_4)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.password_cb = QCheckBox(self.groupBox)
        self.password_cb.setObjectName(u"password_cb")

        self.horizontalLayout_4.addWidget(self.password_cb)

        self.password_le = QLineEdit(self.groupBox)
        self.password_le.setObjectName(u"password_le")
        self.password_le.setEnabled(False)
        self.password_le.setMinimumSize(QSize(0, 50))
        self.password_le.setStyleSheet(u"border-radius: 3px;")
        self.password_le.setEchoMode(QLineEdit.EchoMode.Password)

        self.horizontalLayout_4.addWidget(self.password_le)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)


        self.verticalLayout_4.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(PublicKeygen)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_5)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton_2 = QPushButton(self.groupBox_2)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setEnabled(False)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setMinimumSize(QSize(0, 60))
        self.pushButton_2.setStyleSheet(u"background-color: rgb(38, 50, 56);\n"
"color: rgb(83, 106, 117);\n"
"font-size: 25px;")
        icon2 = QIcon()
        icon2.addFile(u":/windows_icons/icons/encrypt.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_2.setIcon(icon2)
        self.pushButton_2.setIconSize(QSize(40, 40))
        self.pushButton_2.setFlat(True)

        self.horizontalLayout_2.addWidget(self.pushButton_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_6)

        self.file_layout_2 = QHBoxLayout()
        self.file_layout_2.setObjectName(u"file_layout_2")
        self.pub_key_path_le = QLineEdit(self.groupBox_2)
        self.pub_key_path_le.setObjectName(u"pub_key_path_le")
        self.pub_key_path_le.setEnabled(False)
        self.pub_key_path_le.setMinimumSize(QSize(0, 50))
        self.pub_key_path_le.setStyleSheet(u"border-radius: 3px;")

        self.file_layout_2.addWidget(self.pub_key_path_le)

        self.pub_key_select_btn = QPushButton(self.groupBox_2)
        self.pub_key_select_btn.setObjectName(u"pub_key_select_btn")
        self.pub_key_select_btn.setMinimumSize(QSize(120, 50))
        self.pub_key_select_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pub_key_select_btn.setStyleSheet(u"QPushButton {\n"
"	background-color: #007d9c;\n"
"	color: #005568;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	background-color: #00a3c8;\n"
"}")
        icon3 = QIcon()
        icon3.addFile(u":/windows_icons/icons/ssd-card.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pub_key_select_btn.setIcon(icon3)
        self.pub_key_select_btn.setIconSize(QSize(30, 30))

        self.file_layout_2.addWidget(self.pub_key_select_btn)


        self.verticalLayout_3.addLayout(self.file_layout_2)


        self.verticalLayout_4.addWidget(self.groupBox_2)

        self.generate_btn = QPushButton(PublicKeygen)
        self.generate_btn.setObjectName(u"generate_btn")
        self.generate_btn.setEnabled(False)
        self.generate_btn.setMinimumSize(QSize(0, 100))
        self.generate_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.generate_btn.setStyleSheet(u"QPushButton {\n"
"	background-color: #007d9c;\n"
"	color: #005568;\n"
"	font-size: 32px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	background-color: #00a3c8;\n"
"}")
        icon4 = QIcon()
        icon4.addFile(u":/windows_icons/icons/magic-wand.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.generate_btn.setIcon(icon4)
        self.generate_btn.setIconSize(QSize(35, 35))

        self.verticalLayout_4.addWidget(self.generate_btn)


        self.retranslateUi(PublicKeygen)

        QMetaObject.connectSlotsByName(PublicKeygen)
    # setupUi

    def retranslateUi(self, PublicKeygen):
        PublicKeygen.setWindowTitle(QCoreApplication.translate("PublicKeygen", u"Key Manager | Select location to generate your public key", None))
        self.label.setText(QCoreApplication.translate("PublicKeygen", u"Select your private key to generate the public key:", None))
        self.groupBox.setTitle("")
        self.private_key_path_le.setPlaceholderText(QCoreApplication.translate("PublicKeygen", u"Click \"Select Private Key\"", None))
        self.private_key_sel_btn.setText(QCoreApplication.translate("PublicKeygen", u"  Select Private Key", None))
        self.password_cb.setText(QCoreApplication.translate("PublicKeygen", u"Password-encrypted?", None))
        self.password_le.setPlaceholderText(QCoreApplication.translate("PublicKeygen", u"\u2190 Checkbox and enter your password for private key here...", None))
        self.groupBox_2.setTitle("")
        self.pushButton_2.setText(QCoreApplication.translate("PublicKeygen", u"  Select location to save your public key:", None))
        self.pub_key_path_le.setPlaceholderText(QCoreApplication.translate("PublicKeygen", u"Click \"Select\" to choose location to save your public key", None))
        self.pub_key_select_btn.setText(QCoreApplication.translate("PublicKeygen", u" Select", None))
        self.generate_btn.setText(QCoreApplication.translate("PublicKeygen", u"Generate", None))
    # retranslateUi

