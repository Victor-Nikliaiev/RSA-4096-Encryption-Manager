# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QVBoxLayout,
    QWidget)
import icons_rc

class Ui_main_window(object):
    def setupUi(self, main_window):
        if not main_window.objectName():
            main_window.setObjectName(u"main_window")
        main_window.resize(719, 577)
        icon = QIcon()
        icon.addFile(u":/favicon/icons/maze.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        main_window.setWindowIcon(icon)
        main_window.setAutoFillBackground(False)
        main_window.setStyleSheet(u"QMainWindow {\n"
"    background-color: #263238;\n"
"}\n"
"\n"
"QPushButton {\n"
"	background-color: #35a3a7;\n"
"	color: #024e55;\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"")
        self.actionEncrypt = QAction(main_window)
        self.actionEncrypt.setObjectName(u"actionEncrypt")
        icon1 = QIcon()
        icon1.addFile(u":/menu_icons/icons/encryption.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionEncrypt.setIcon(icon1)
        self.actionDecrypt = QAction(main_window)
        self.actionDecrypt.setObjectName(u"actionDecrypt")
        icon2 = QIcon()
        icon2.addFile(u":/menu_icons/icons/decryption.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionDecrypt.setIcon(icon2)
        self.actionExit = QAction(main_window)
        self.actionExit.setObjectName(u"actionExit")
        icon3 = QIcon()
        icon3.addFile(u":/menu_icons/icons/switch.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionExit.setIcon(icon3)
        self.actionGenerateKeys = QAction(main_window)
        self.actionGenerateKeys.setObjectName(u"actionGenerateKeys")
        icon4 = QIcon()
        icon4.addFile(u":/windows_icons/icons/encrypt.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionGenerateKeys.setIcon(icon4)
        self.actionAbout = QAction(main_window)
        self.actionAbout.setObjectName(u"actionAbout")
        icon5 = QIcon()
        icon5.addFile(u":/menu_icons/icons/question.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionAbout.setIcon(icon5)
        self.actionEnglish = QAction(main_window)
        self.actionEnglish.setObjectName(u"actionEnglish")
        self.action = QAction(main_window)
        self.action.setObjectName(u"action")
        self.actionEspa_ol = QAction(main_window)
        self.actionEspa_ol.setObjectName(u"actionEspa_ol")
        self.centralwidget = QWidget(main_window)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.q_logo = QWidget(self.centralwidget)
        self.q_logo.setObjectName(u"q_logo")
        self.q_logo.setMaximumSize(QSize(16777215, 500))

        self.verticalLayout.addWidget(self.q_logo)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 100))
        font = QFont()
        font.setPointSize(31)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(7)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_2 = QSpacerItem(200, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.encrypt_button = QPushButton(self.centralwidget)
        self.encrypt_button.setObjectName(u"encrypt_button")
        self.encrypt_button.setMinimumSize(QSize(0, 50))
        self.encrypt_button.setBaseSize(QSize(0, 0))
        font1 = QFont()
        font1.setPointSize(14)
        self.encrypt_button.setFont(font1)
        self.encrypt_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.encrypt_button.setIcon(icon1)
        self.encrypt_button.setIconSize(QSize(30, 30))

        self.verticalLayout_2.addWidget(self.encrypt_button)

        self.decrypt_button = QPushButton(self.centralwidget)
        self.decrypt_button.setObjectName(u"decrypt_button")
        self.decrypt_button.setMinimumSize(QSize(0, 50))
        self.decrypt_button.setFont(font1)
        self.decrypt_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.decrypt_button.setIcon(icon2)
        self.decrypt_button.setIconSize(QSize(30, 30))

        self.verticalLayout_2.addWidget(self.decrypt_button)

        self.generate_keys_button = QPushButton(self.centralwidget)
        self.generate_keys_button.setObjectName(u"generate_keys_button")
        self.generate_keys_button.setMinimumSize(QSize(0, 50))
        self.generate_keys_button.setFont(font1)
        self.generate_keys_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.generate_keys_button.setStyleSheet(u"")
        self.generate_keys_button.setIcon(icon4)
        self.generate_keys_button.setIconSize(QSize(30, 30))

        self.verticalLayout_2.addWidget(self.generate_keys_button)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.horizontal_Spacer = QSpacerItem(200, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontal_Spacer)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        main_window.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(main_window)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 719, 25))
        self.menubar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.menubar.setStyleSheet(u"background-color: #212d31;\n"
"color: rgb(119, 186, 198)")
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuFile.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.menuFile.setStyleSheet(u"background-color: #212d31;\n"
"color: rgb(119, 186, 198)")
        self.menuKeys = QMenu(self.menubar)
        self.menuKeys.setObjectName(u"menuKeys")
        self.menuKeys.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuHelp.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.menuHelp.setStyleSheet(u"background-color: #212d31;\n"
"color: rgb(119, 186, 198)")
        self.menuLanguage = QMenu(self.menubar)
        self.menuLanguage.setObjectName(u"menuLanguage")
        self.menuLanguage.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        main_window.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(main_window)
        self.statusbar.setObjectName(u"statusbar")
        main_window.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuKeys.menuAction())
        self.menubar.addAction(self.menuLanguage.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionEncrypt)
        self.menuFile.addAction(self.actionDecrypt)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuKeys.addAction(self.actionGenerateKeys)
        self.menuHelp.addAction(self.actionAbout)
        self.menuLanguage.addAction(self.actionEnglish)
        self.menuLanguage.addAction(self.action)
        self.menuLanguage.addAction(self.actionEspa_ol)

        self.retranslateUi(main_window)

        QMetaObject.connectSlotsByName(main_window)
    # setupUi

    def retranslateUi(self, main_window):
        main_window.setWindowTitle(QCoreApplication.translate("main_window", u"RSA-4096 Encryption Manager  v1.0", None))
        self.actionEncrypt.setText(QCoreApplication.translate("main_window", u"Encrypt", None))
        self.actionDecrypt.setText(QCoreApplication.translate("main_window", u"Decrypt", None))
        self.actionExit.setText(QCoreApplication.translate("main_window", u"Exit", None))
        self.actionGenerateKeys.setText(QCoreApplication.translate("main_window", u"Generate", None))
        self.actionAbout.setText(QCoreApplication.translate("main_window", u"About", None))
        self.actionEnglish.setText(QCoreApplication.translate("main_window", u"English", None))
        self.action.setText(QCoreApplication.translate("main_window", u"\u0420\u0443\u0441\u0441\u043a\u0438\u0439", None))
        self.actionEspa_ol.setText(QCoreApplication.translate("main_window", u"Espa\u00f1ol", None))
        self.label.setText(QCoreApplication.translate("main_window", u"<html><head/><body><p><span style=\" font-size:26pt; color:#b6f1b7;\">Choose process:</span></p></body></html>", None))
        self.encrypt_button.setText(QCoreApplication.translate("main_window", u"Encrypt File", None))
        self.decrypt_button.setText(QCoreApplication.translate("main_window", u"Decrypt File", None))
        self.generate_keys_button.setText(QCoreApplication.translate("main_window", u"Generate Keys", None))
        self.menuFile.setTitle(QCoreApplication.translate("main_window", u"File", None))
        self.menuKeys.setTitle(QCoreApplication.translate("main_window", u"RSA Keys", None))
        self.menuHelp.setTitle(QCoreApplication.translate("main_window", u"Help", None))
        self.menuLanguage.setTitle(QCoreApplication.translate("main_window", u"Language", None))
    # retranslateUi

