from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QVBoxLayout,
    QFrame,
    QFileIconProvider,
    QFileDialog,
)
from PySide6.QtCore import Qt, QFileInfo, Signal

import sys
import os
from backend import signal_manager


class DragDropWidget(QFrame):

    def __init__(self):
        super().__init__()
        self.setObjectName("dragDropWidget")
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(
            """
            #dragDropWidget {
                border: 2px dashed #749bab;
                border-radius: 10px;
                background-color: #222d32;   
               
            }
            #dragDropWidget:hover {
                background-color: #435963;
            }

            #fileNameLabel {
                font-size: 16px;
                color: #5c7988;
            }

            """
        )

        # Set up the main layout
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)  # Center the layout inside the widget

        self.setAcceptDrops(True)

        # Create the icon label and name label
        self.file_ico_label = QLabel(self)
        self.file_ico_label.setObjectName("fileIcoLabel")
        self.file_ico_label.setAlignment(Qt.AlignCenter)

        self.file_name_label = QLabel("Click Or Drag & Drop A File Here", self)
        self.file_name_label.setObjectName("fileNameLabel")
        self.file_name_label.setAlignment(Qt.AlignCenter)

        # Add the labels to the layout
        self.layout.addWidget(self.file_ico_label)
        self.layout.addWidget(self.file_name_label)

        # Set up drag-and-drop signals
        self.dragEnterEvent = self.dragEnterEvent
        self.dropEvent = self.dropEvent
        self.setLayout(self.layout)

        self.file_path = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            file_path, _ = QFileDialog.getOpenFileName(self, "Select a File")
            if file_path:
                self.handleFiles([file_path])

    def dragEnterEvent(self, event):
        """Handle the drag enter event."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        """Handle the drop event."""
        if event.mimeData().hasUrls():
            files = [url.toLocalFile() for url in event.mimeData().urls()]
            self.handleFiles(files)

    def handleFiles(self, files):
        """Process the dropped files."""
        self.file_path = None

        for file in files:
            if os.path.isdir(file):
                self.file_name_label.setText(f"Only files are allowed!")
                signal_manager.update_next_button_status.emit(False)
                self.file_ico_label.clear()
                return
        self.file_path = files[0]
        if not self.file_path:
            self.file_name_label.setText("Dropped data isn't a file")
            signal_manager.update_next_button_status.emit(False)
            self.file_ico_label.clear()
            return
        file_name = os.path.basename(self.file_path)
        if len(file_name) > 20:
            file_extension = os.path.splitext(file_name)[1]
            file_name = file_name[:17] + "..." + file_extension

        file_info = QFileInfo(self.file_path)

        icon_provider = QFileIconProvider()
        file_icon = icon_provider.icon(file_info)

        pixmap = file_icon.pixmap(64, 64)
        self.file_ico_label.setPixmap(pixmap)

        self.file_name_label.setText(file_name)
        self.file_name_label.setWordWrap(True)
        self.file_name_label.setAlignment(Qt.AlignVCenter)

        if self.file_path:
            signal_manager.update_next_button_status.emit(True)
            signal_manager.file_dropped.emit(self.file_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DragDropWidget()
    window.show()
    sys.exit(app.exec())
