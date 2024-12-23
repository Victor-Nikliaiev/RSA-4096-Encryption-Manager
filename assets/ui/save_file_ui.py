# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'save_file.ui'
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
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)
import assets.ui.icons_rc


class Ui_SaveFileForm(object):
    def setupUi(self, SaveFileForm):
        if not SaveFileForm.objectName():
            SaveFileForm.setObjectName("SaveFileForm")
        SaveFileForm.setEnabled(True)
        SaveFileForm.resize(719, 577)
        icon = QIcon()
        icon.addFile(
            ":/favicon/icons/maze.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        SaveFileForm.setWindowIcon(icon)
        SaveFileForm.setWindowOpacity(1.000000000000000)
        SaveFileForm.setStyleSheet(
            "QWidget {\n"
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
            "}"
        )
        self.verticalLayout = QVBoxLayout(SaveFileForm)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalSpacer_3 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.groupBox = QGroupBox(SaveFileForm)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalSpacer_4 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.verticalLayout_2.addItem(self.verticalSpacer_4)

        self.input_file_info_btn = QPushButton(self.groupBox)
        self.input_file_info_btn.setObjectName("input_file_info_btn")
        self.input_file_info_btn.setEnabled(False)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.input_file_info_btn.sizePolicy().hasHeightForWidth()
        )
        self.input_file_info_btn.setSizePolicy(sizePolicy)
        self.input_file_info_btn.setMinimumSize(QSize(0, 60))
        self.input_file_info_btn.setStyleSheet(
            "background-color: rgb(38, 50, 56);\n"
            "color: rgb(83, 106, 117);\n"
            "font-size: 25px;"
        )
        icon1 = QIcon()
        icon1.addFile(
            ":/windows_icons/icons/encrypt_file.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.input_file_info_btn.setIcon(icon1)
        self.input_file_info_btn.setIconSize(QSize(40, 40))
        self.input_file_info_btn.setFlat(True)

        self.verticalLayout_2.addWidget(self.input_file_info_btn)

        self.file_chooser_input = QLineEdit(self.groupBox)
        self.file_chooser_input.setObjectName("file_chooser_input")
        self.file_chooser_input.setEnabled(False)
        self.file_chooser_input.setMinimumSize(QSize(0, 50))
        self.file_chooser_input.setStyleSheet("border-radius: 3px;")

        self.verticalLayout_2.addWidget(self.file_chooser_input)

        self.verticalSpacer_2 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.output_file_info_btn = QPushButton(self.groupBox)
        self.output_file_info_btn.setObjectName("output_file_info_btn")
        self.output_file_info_btn.setEnabled(False)
        sizePolicy.setHeightForWidth(
            self.output_file_info_btn.sizePolicy().hasHeightForWidth()
        )
        self.output_file_info_btn.setSizePolicy(sizePolicy)
        self.output_file_info_btn.setMinimumSize(QSize(0, 60))
        self.output_file_info_btn.setStyleSheet(
            "background-color: rgb(38, 50, 56);\n"
            "color: rgb(83, 106, 117);\n"
            "font-size: 25px;"
        )
        icon2 = QIcon()
        icon2.addFile(
            ":/windows_icons/icons/file.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.output_file_info_btn.setIcon(icon2)
        self.output_file_info_btn.setIconSize(QSize(40, 40))
        self.output_file_info_btn.setFlat(True)

        self.verticalLayout_2.addWidget(self.output_file_info_btn)

        self.file_layout = QHBoxLayout()
        self.file_layout.setObjectName("file_layout")
        self.saved_name_input = QLineEdit(self.groupBox)
        self.saved_name_input.setObjectName("saved_name_input")
        self.saved_name_input.setEnabled(False)
        self.saved_name_input.setMinimumSize(QSize(0, 50))
        self.saved_name_input.setStyleSheet("border-radius: 3px;")

        self.file_layout.addWidget(self.saved_name_input)

        self.save_file_button = QPushButton(self.groupBox)
        self.save_file_button.setObjectName("save_file_button")
        self.save_file_button.setMinimumSize(QSize(120, 50))
        self.save_file_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.save_file_button.setStyleSheet(
            "#save_file_button {\n"
            "	background-color: #007d9c;\n"
            "	color: #005568;\n"
            "}\n"
            "\n"
            "#save_file_button:hover {\n"
            "	background-color: #00a3c8;\n"
            "}"
        )
        icon3 = QIcon()
        icon3.addFile(
            ":/windows_icons/icons/ssd-card.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.save_file_button.setIcon(icon3)
        self.save_file_button.setIconSize(QSize(30, 30))

        self.file_layout.addWidget(self.save_file_button)

        self.verticalLayout_2.addLayout(self.file_layout)

        self.verticalLayout.addWidget(self.groupBox)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.verticalLayout.addItem(self.verticalSpacer)

        self.start_button = QPushButton(SaveFileForm)
        self.start_button.setObjectName("start_button")
        self.start_button.setEnabled(False)
        self.start_button.setMinimumSize(QSize(0, 100))
        self.start_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.start_button.setStyleSheet(
            "#start_button {\n"
            "	background-color: #007d9c;\n"
            "	color: #005568;\n"
            "	font-size: 32px;\n"
            "}\n"
            "\n"
            "#start_button:hover {\n"
            "	background-color: #00a3c8;\n"
            "}"
        )
        icon4 = QIcon()
        icon4.addFile(
            ":/windows_icons/icons/next.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.start_button.setIcon(icon4)
        self.start_button.setIconSize(QSize(30, 30))

        self.verticalLayout.addWidget(self.start_button)

        self.retranslateUi(SaveFileForm)

        QMetaObject.connectSlotsByName(SaveFileForm)

    # setupUi

    def retranslateUi(self, SaveFileForm):
        SaveFileForm.setWindowTitle(
            QCoreApplication.translate(
                "SaveFileForm", "[PLACEHOLDER] |  Choose file name", None
            )
        )
        self.groupBox.setTitle("")
        self.input_file_info_btn.setText(
            QCoreApplication.translate("SaveFileForm", "File to be encrypted:", None)
        )
        self.file_chooser_input.setPlaceholderText(
            QCoreApplication.translate(
                "SaveFileForm", "Path to selected file...[PLACEHOLDER]", None
            )
        )
        self.output_file_info_btn.setText(
            QCoreApplication.translate(
                "SaveFileForm", "Choose file name for encrypted file:", None
            )
        )
        self.saved_name_input.setPlaceholderText(
            QCoreApplication.translate(
                "SaveFileForm", 'Click "Save" button to choose file name...', None
            )
        )
        self.save_file_button.setText(
            QCoreApplication.translate("SaveFileForm", "Save", None)
        )
        self.start_button.setText(
            QCoreApplication.translate("SaveFileForm", "Start Encryption", None)
        )

    # retranslateUi
