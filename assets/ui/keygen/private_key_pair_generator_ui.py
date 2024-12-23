# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'private_key_pair_generator.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)
import icons_rc

class Ui_PrivateKeyPairGenerator(object):
    def setupUi(self, PrivateKeyPairGenerator):
        if not PrivateKeyPairGenerator.objectName():
            PrivateKeyPairGenerator.setObjectName(u"PrivateKeyPairGenerator")
        PrivateKeyPairGenerator.setEnabled(True)
        PrivateKeyPairGenerator.resize(719, 577)
        icon = QIcon()
        icon.addFile(u":/favicon/icons/maze.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        PrivateKeyPairGenerator.setWindowIcon(icon)
        PrivateKeyPairGenerator.setWindowOpacity(1.000000000000000)
        PrivateKeyPairGenerator.setStyleSheet(u"QWidget {\n"
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
        self.verticalLayout_4 = QVBoxLayout(PrivateKeyPairGenerator)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_3)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.top_lb = QLabel(PrivateKeyPairGenerator)
        self.top_lb.setObjectName(u"top_lb")
        self.top_lb.setStyleSheet(u"background-color: rgb(38, 50, 56);\n"
"color: rgb(49, 169, 196);\n"
"font-size: 25px;\n"
"font-weight: bold;")
        self.top_lb.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.top_lb)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.groupBox_2 = QGroupBox(PrivateKeyPairGenerator)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_5)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.location_info_btn = QPushButton(self.groupBox_2)
        self.location_info_btn.setObjectName(u"location_info_btn")
        self.location_info_btn.setEnabled(False)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.location_info_btn.sizePolicy().hasHeightForWidth())
        self.location_info_btn.setSizePolicy(sizePolicy)
        self.location_info_btn.setMinimumSize(QSize(0, 60))
        self.location_info_btn.setStyleSheet(u"background-color: rgb(38, 50, 56);\n"
"color: rgb(83, 106, 117);\n"
"font-size: 25px;")
        icon1 = QIcon()
        icon1.addFile(u":/windows_icons/icons/encrypt.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.location_info_btn.setIcon(icon1)
        self.location_info_btn.setIconSize(QSize(40, 40))
        self.location_info_btn.setFlat(True)

        self.horizontalLayout_2.addWidget(self.location_info_btn)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_6)

        self.file_layout_2 = QHBoxLayout()
        self.file_layout_2.setObjectName(u"file_layout_2")
        self.key_path_le = QLineEdit(self.groupBox_2)
        self.key_path_le.setObjectName(u"key_path_le")
        self.key_path_le.setEnabled(False)
        self.key_path_le.setMinimumSize(QSize(0, 50))
        self.key_path_le.setStyleSheet(u"border-radius: 3px;")

        self.file_layout_2.addWidget(self.key_path_le)

        self.key_browse_btn = QPushButton(self.groupBox_2)
        self.key_browse_btn.setObjectName(u"key_browse_btn")
        self.key_browse_btn.setMinimumSize(QSize(120, 50))
        self.key_browse_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.key_browse_btn.setStyleSheet(u"QPushButton {\n"
"	background-color: #007d9c;\n"
"	color: #005568;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	background-color: #00a3c8;\n"
"}")
        icon2 = QIcon()
        icon2.addFile(u":/windows_icons/icons/next.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.key_browse_btn.setIcon(icon2)
        self.key_browse_btn.setIconSize(QSize(30, 30))

        self.file_layout_2.addWidget(self.key_browse_btn)


        self.verticalLayout.addLayout(self.file_layout_2)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_4)

        self.line = QFrame(self.groupBox_2)
        self.line.setObjectName(u"line")
        self.line.setEnabled(False)
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.password_cb = QCheckBox(self.groupBox_2)
        self.password_cb.setObjectName(u"password_cb")

        self.verticalLayout.addWidget(self.password_cb)

        self.password_le = QLineEdit(self.groupBox_2)
        self.password_le.setObjectName(u"password_le")
        self.password_le.setEnabled(False)
        self.password_le.setMinimumSize(QSize(0, 50))
        self.password_le.setStyleSheet(u"border-radius: 3px;")
        self.password_le.setEchoMode(QLineEdit.EchoMode.Password)

        self.verticalLayout.addWidget(self.password_le)

        self.key_match_lb = QLabel(self.groupBox_2)
        self.key_match_lb.setObjectName(u"key_match_lb")
        self.key_match_lb.setStyleSheet(u"color: rgb(182, 186, 233)")

        self.verticalLayout.addWidget(self.key_match_lb)

        self.password_repeat_le = QLineEdit(self.groupBox_2)
        self.password_repeat_le.setObjectName(u"password_repeat_le")
        self.password_repeat_le.setEnabled(False)
        self.password_repeat_le.setMinimumSize(QSize(0, 50))
        self.password_repeat_le.setStyleSheet(u"border-radius: 3px;")
        self.password_repeat_le.setEchoMode(QLineEdit.EchoMode.Password)

        self.verticalLayout.addWidget(self.password_repeat_le)


        self.verticalLayout_4.addWidget(self.groupBox_2)

        self.verticalSpacer_2 = QSpacerItem(20, 60, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)

        self.generate_btn = QPushButton(PrivateKeyPairGenerator)
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
        icon3 = QIcon()
        icon3.addFile(u":/windows_icons/icons/magic-wand.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.generate_btn.setIcon(icon3)
        self.generate_btn.setIconSize(QSize(35, 35))

        self.verticalLayout_4.addWidget(self.generate_btn)

        QWidget.setTabOrder(self.key_path_le, self.key_browse_btn)
        QWidget.setTabOrder(self.key_browse_btn, self.password_cb)
        QWidget.setTabOrder(self.password_cb, self.password_le)
        QWidget.setTabOrder(self.password_le, self.password_repeat_le)
        QWidget.setTabOrder(self.password_repeat_le, self.generate_btn)
        QWidget.setTabOrder(self.generate_btn, self.location_info_btn)

        self.retranslateUi(PrivateKeyPairGenerator)

        QMetaObject.connectSlotsByName(PrivateKeyPairGenerator)
    # setupUi

    def retranslateUi(self, PrivateKeyPairGenerator):
        PrivateKeyPairGenerator.setWindowTitle(QCoreApplication.translate("PrivateKeyPairGenerator", u"Key Generation | Select location to generate your private key", None))
        self.top_lb.setText(QCoreApplication.translate("PrivateKeyPairGenerator", u"Select location to generate your private key:", None))
        self.groupBox_2.setTitle("")
        self.location_info_btn.setText(QCoreApplication.translate("PrivateKeyPairGenerator", u"  Select location to save your private key:", None))
        self.key_path_le.setPlaceholderText(QCoreApplication.translate("PrivateKeyPairGenerator", u"Click \"Select\" to choose location to save your private key", None))
        self.key_browse_btn.setText(QCoreApplication.translate("PrivateKeyPairGenerator", u" Select", None))
        self.password_cb.setText(QCoreApplication.translate("PrivateKeyPairGenerator", u"Encrypt by password?", None))
        self.password_le.setPlaceholderText(QCoreApplication.translate("PrivateKeyPairGenerator", u"\u2191 Checkbox and enter your password for private key here...", None))
        self.key_match_lb.setText("")
        self.password_repeat_le.setPlaceholderText(QCoreApplication.translate("PrivateKeyPairGenerator", u"Repeat your password here...", None))
        self.generate_btn.setText(QCoreApplication.translate("PrivateKeyPairGenerator", u"Generate", None))
    # retranslateUi

