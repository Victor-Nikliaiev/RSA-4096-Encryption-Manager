# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'about.ui'
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
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)
import assets.ui.icons_rc


class Ui_About(object):
    def setupUi(self, About):
        if not About.objectName():
            About.setObjectName("About")
        About.resize(657, 448)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(About.sizePolicy().hasHeightForWidth())
        About.setSizePolicy(sizePolicy)
        About.setMinimumSize(QSize(657, 448))
        About.setMaximumSize(QSize(657, 448))
        icon = QIcon()
        icon.addFile(
            ":/favicon/icons/maze.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        About.setWindowIcon(icon)
        self.verticalLayout_2 = QVBoxLayout(About)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QLabel(About)
        self.label.setObjectName("label")
        self.label.setMaximumSize(QSize(100, 100))
        self.label.setPixmap(QPixmap(":/favicon/icons/maze.png"))
        self.label.setScaledContents(True)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.label)

        self.app_name_lb = QLabel(About)
        self.app_name_lb.setObjectName("app_name_lb")
        self.app_name_lb.setStyleSheet(
            "color: rgb(195, 221, 247);\n" "font-size: 32px;"
        )

        self.horizontalLayout.addWidget(self.app_name_lb)

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(
            20, 7, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum
        )

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.frame = QFrame(About)
        self.frame.setObjectName("frame")
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.label_2.setMinimumSize(QSize(0, 40))
        self.label_2.setStyleSheet("background-color: rgb(8, 115, 129);")
        self.label_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.label_2.setFrameShadow(QFrame.Shadow.Sunken)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_2)

        self.verticalSpacer_2 = QSpacerItem(
            20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum
        )

        self.verticalLayout_3.addItem(self.verticalSpacer_2)

        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        sizePolicy1 = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)
        self.label_3.setStyleSheet("padding: 10px;")
        self.label_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.label_3.setTextFormat(Qt.TextFormat.RichText)
        self.label_3.setScaledContents(False)
        self.label_3.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.label_3)

        self.verticalLayout_2.addWidget(self.frame)

        self.retranslateUi(About)

        QMetaObject.connectSlotsByName(About)

    # setupUi

    def retranslateUi(self, About):
        About.setWindowTitle(QCoreApplication.translate("About", "About", None))
        self.label.setText("")
        self.app_name_lb.setText(
            QCoreApplication.translate("About", "   RSA-4096 Encryption Manager", None)
        )
        self.label_2.setText(QCoreApplication.translate("About", "Version 1.0", None))
        self.label_3.setText(
            QCoreApplication.translate(
                "About",
                '<html><head/><body><p><span style=" font-size:11pt; font-weight:700; text-decoration: underline;">Welcome to RSA-4096 Encryption Manager!</span></p><p align="justify"><span style=" font-size:11pt;">Your privacy and security matter. This application is designed to help you encrypt and decrypt sensitive data with ease and confidence.</span></p><p align="justify"><span style=" font-size:11pt;">In addition, you can generate highly secure RSA-4096 public and private keys, including encrypted private keys, ensuring robust protection for your information in future use. </span></p><p align="justify"><span style=" font-size:11pt;">This is a non-commercial project, and  I am proud to offer it completely free of charge.</span></p><p align="justify"><span style=" font-size:11pt;">Thank you for trusting with your security needs.</span></p><p align="justify"><span style=" font-size:11pt; font-style:italic;">December 22, 2024</span><span style=" font-size:11pt;"><br/></span><span style=" font-size:11'
                'pt; font-weight:700;">Arhis Alight</span></p></body></html>',
                None,
            )
        )

    # retranslateUi
