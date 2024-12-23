# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'progress_window.ui'
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
from PySide6.QtWidgets import (QApplication, QProgressBar, QSizePolicy, QVBoxLayout,
    QWidget)
import icons_rc

class Ui_operation_progress_window(object):
    def setupUi(self, operation_progress_window):
        if not operation_progress_window.objectName():
            operation_progress_window.setObjectName(u"operation_progress_window")
        operation_progress_window.resize(510, 209)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(operation_progress_window.sizePolicy().hasHeightForWidth())
        operation_progress_window.setSizePolicy(sizePolicy)
        operation_progress_window.setMinimumSize(QSize(510, 209))
        operation_progress_window.setMaximumSize(QSize(510, 209))
        operation_progress_window.setCursor(QCursor(Qt.CursorShape.BusyCursor))
        icon = QIcon()
        icon.addFile(u":/favicon/icons/maze.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        operation_progress_window.setWindowIcon(icon)
        operation_progress_window.setStyleSheet(u"background-color: rgb(38, 50, 56)")
        self.verticalLayout = QVBoxLayout(operation_progress_window)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.operation_progress = QProgressBar(operation_progress_window)
        self.operation_progress.setObjectName(u"operation_progress")
        self.operation_progress.setValue(0)

        self.verticalLayout.addWidget(self.operation_progress)


        self.retranslateUi(operation_progress_window)

        QMetaObject.connectSlotsByName(operation_progress_window)
    # setupUi

    def retranslateUi(self, operation_progress_window):
        operation_progress_window.setWindowTitle(QCoreApplication.translate("operation_progress_window", u"Process  status...[PLACEHOLDER]", None))
    # retranslateUi

