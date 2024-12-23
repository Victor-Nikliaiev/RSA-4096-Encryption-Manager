# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'select_keygen.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGroupBox, QHBoxLayout,
    QLabel, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)
import icons_rc

class Ui_SelectKeygen(object):
    def setupUi(self, SelectKeygen):
        if not SelectKeygen.objectName():
            SelectKeygen.setObjectName(u"SelectKeygen")
        SelectKeygen.resize(719, 577)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SelectKeygen.sizePolicy().hasHeightForWidth())
        SelectKeygen.setSizePolicy(sizePolicy)
        SelectKeygen.setMinimumSize(QSize(719, 577))
        SelectKeygen.setMaximumSize(QSize(719, 577))
        icon = QIcon()
        icon.addFile(u":/favicon/icons/maze.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        SelectKeygen.setWindowIcon(icon)
        SelectKeygen.setStyleSheet(u"QWidget {\n"
"	\n"
"	background-color: rgb(38, 50, 56);\n"
"}\n"
"\n"
"QRadioButton {\n"
"	color:  rgb(198, 235, 243);\n"
"	font-size: 22px;\n"
"} ")
        self.verticalLayout = QVBoxLayout(SelectKeygen)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame = QFrame(SelectKeygen)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.frame.setLineWidth(1)
        self.verticalLayout_4 = QVBoxLayout(self.frame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        self.label.setStyleSheet(u"color: rgb(153, 193, 241);\n"
"font-size: 30px;\n"
"text-align: center;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_4.addWidget(self.label)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.groupBox = QGroupBox(self.frame)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setStyleSheet(u"background-color: #415661;")
        self.groupBox.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.gen_priv_key_rb = QRadioButton(self.groupBox)
        self.gen_priv_key_rb.setObjectName(u"gen_priv_key_rb")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.gen_priv_key_rb.sizePolicy().hasHeightForWidth())
        self.gen_priv_key_rb.setSizePolicy(sizePolicy2)

        self.verticalLayout_3.addWidget(self.gen_priv_key_rb)

        self.gen_pub_key_rb = QRadioButton(self.groupBox)
        self.gen_pub_key_rb.setObjectName(u"gen_pub_key_rb")
        sizePolicy2.setHeightForWidth(self.gen_pub_key_rb.sizePolicy().hasHeightForWidth())
        self.gen_pub_key_rb.setSizePolicy(sizePolicy2)

        self.verticalLayout_3.addWidget(self.gen_pub_key_rb)

        self.gen_key_pair_rb = QRadioButton(self.groupBox)
        self.gen_key_pair_rb.setObjectName(u"gen_key_pair_rb")
        sizePolicy2.setHeightForWidth(self.gen_key_pair_rb.sizePolicy().hasHeightForWidth())
        self.gen_key_pair_rb.setSizePolicy(sizePolicy2)

        self.verticalLayout_3.addWidget(self.gen_key_pair_rb)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.next_button = QPushButton(self.groupBox)
        self.next_button.setObjectName(u"next_button")
        self.next_button.setEnabled(False)
        self.next_button.setMinimumSize(QSize(0, 0))
        self.next_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.next_button.setStyleSheet(u"QPushButton {\n"
"	color: #024e55;\n"
"	background-color:  #35a3a7;\n"
"	font-size: 28px;\n"
"	border-radius: 5px;\n"
"}\n"
"QPushButton::hover {\n"
"	background-color: #49e1e6;\n"
"}")

        self.verticalLayout_3.addWidget(self.next_button)


        self.horizontalLayout.addWidget(self.groupBox)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_4.addItem(self.verticalSpacer_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy3)
        self.label_2.setMaximumSize(QSize(200, 200))
        self.label_2.setAutoFillBackground(False)
        self.label_2.setPixmap(QPixmap(u":/misc/icons/cyber_key.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.verticalSpacer_4 = QSpacerItem(20, 60, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_4)


        self.verticalLayout.addWidget(self.frame)


        self.retranslateUi(SelectKeygen)

        QMetaObject.connectSlotsByName(SelectKeygen)
    # setupUi

    def retranslateUi(self, SelectKeygen):
        SelectKeygen.setWindowTitle(QCoreApplication.translate("SelectKeygen", u"Select Keygen Option", None))
        self.label.setText(QCoreApplication.translate("SelectKeygen", u"Select an option:", None))
        self.groupBox.setTitle("")
        self.gen_priv_key_rb.setText(QCoreApplication.translate("SelectKeygen", u"Generate private key", None))
        self.gen_pub_key_rb.setText(QCoreApplication.translate("SelectKeygen", u"Generate public key", None))
        self.gen_key_pair_rb.setText(QCoreApplication.translate("SelectKeygen", u"Generate public and private key", None))
        self.next_button.setText(QCoreApplication.translate("SelectKeygen", u"Next", None))
        self.label_2.setText("")
    # retranslateUi

