from PySide6 import QtWidgets as qtw
from tools.toolkit import Tools as t
from PySide6 import QtCore as qtc
from backend import signal_manager
import os

logging = t.all.logging_config_screen()
logging = logging.getLogger(__name__)


class DragDropWidget(qtw.QFrame):
    def __init__(self):
        """
        Initialize the DragDropWidget.

        This constructor sets up the drag-and-drop widget by applying styles, configuring layout,
        and preparing labels for file display. It also initializes the drag-and-drop signals for
        handling file interactions.

        Attributes
        ----------
        layout : QVBoxLayout
            The main layout containing the file icon and name labels.
        file_ico_label : QLabel
            Label for displaying the file icon.
        file_name_label : QLabel
            Label for displaying the file name.
        """

        super().__init__()
        self.setObjectName("dragAndDropWidget")
        self.setAcceptDrops(True)
        self._apply_stylesheet()

        # Set up the main layout
        self.layout = qtw.QVBoxLayout(self)
        self.layout.setAlignment(qtc.Qt.AlignCenter)

        # Create the icon label and name label
        self.file_ico_label, self.file_name_label = self._create_file_display_labels()

        # Add the labels to the layout
        self.layout.addWidget(self.file_ico_label)
        self.layout.addWidget(self.file_name_label)
        self.setLayout(self.layout)

    def mousePressEvent(self, event):
        """
        Open a file dialog for selecting a file when the left mouse button is clicked.

        This method is a slot for the mousePressEvent signal.

        Parameters
        ----------
        event : QMouseEvent
            The mouse press event.

        """
        if event.button() == qtc.Qt.LeftButton:
            file_path, _ = qtw.QFileDialog.getOpenFileName(
                self, self.tr("Select a File")
            )
            if file_path:
                self.dropped_files_handler([file_path])

    def dragEnterEvent(self, event):
        """
        Handle the drag enter event for the widget.

        This method is invoked when a drag action enters the widget's area. It checks
        whether the dragged data contains URLs and accepts the proposed action if it does.
        Otherwise, it ignores the event.

        Parameters
        ----------
        event : QDragEnterEvent
            The drag enter event containing the mime data.

        """

        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        """
        Handle the drop event for the widget.

        This method is invoked when a drag action is dropped onto the widget. It
        checks whether the dragged data contains URLs and processes the files if it
        does. Otherwise, it ignores the event.

        Parameters
        ----------
        event : QDropEvent
            The drop event containing the mime data.

        """

        if event.mimeData().hasUrls():
            files = [url.toLocalFile() for url in event.mimeData().urls()]
            self.dropped_files_handler(files)

    def dropped_files_handler(self, files):
        """
        Handle the files that have been dropped onto the widget.

        This method is invoked when files are dropped onto the widget. It checks
        whether the dropped data contains URLs and processes the files if it does.
        Otherwise, it ignores the event.

        Parameters
        ----------
        files : List[str]
            The list of files that were dropped.

        """

        self.dropped_file_path = None

        for file in files:
            if os.path.isdir(file):
                self.file_name_label.setText(self.tr("Only files are allowed!"))
                signal_manager.update_next_button_status.emit(False)
                self.file_ico_label.clear()
                return

        self.dropped_file_path = files[0]

        if not self.dropped_file_path:
            self.file_name_label.setText(self.tr("Dropped data isn't a file"))
            signal_manager.update_next_button_status.emit(False)
            self.file_ico_label.clear()
            return

        self._display_dropped_file()

        logging.info(f"Dropped File Path: {self.dropped_file_path}")
        signal_manager.update_next_button_status.emit(True)
        signal_manager.file_dropped.emit(self.dropped_file_path)

    def _shorten_file_name(self, file_name, max_length=20):
        """
        Shorten a file name to a maximum length of 20 characters, if needed.

        If the file name is longer than 20 characters, it is shortened to 17
        characters plus the file extension.

        Parameters
        ----------
        file_name : str
            The file name to shorten.
        max_length : int, optional
            The maximum length of the shortened file name. Defaults to 20.

        Returns
        -------
        str
            The shortened file name.
        """
        if len(file_name) > max_length:
            file_extension = os.path.splitext(file_name)[1]
            file_name = f"{file_name[:17]}...{file_extension}"
            return file_name

        return file_name

    def _display_dropped_file(self):
        """
        Display the dropped file by setting the file icon and name label.

        This method uses the QFileIconProvider to get the icon for the file
        and sets the file name label to the name of the dropped file. The
        label is also set to wrap its text to the next line if it exceeds the
        maximum width and is centered vertically.

        """

        file_name = os.path.basename(self.dropped_file_path)
        file_name = self._shorten_file_name(file_name)

        file_info = qtc.QFileInfo(self.dropped_file_path)
        icon_provider = qtw.QFileIconProvider()
        file_icon = icon_provider.icon(file_info)

        pixmap = file_icon.pixmap(64, 64)
        self.file_ico_label.setPixmap(pixmap)

        self.file_name_label.setText(file_name)
        self.file_name_label.setWordWrap(True)
        self.file_name_label.setAlignment(qtc.Qt.AlignVCenter)

    def _apply_stylesheet(self):
        """
        Apply the stylesheet to the widget.

        This method sets the cursor to a pointing hand cursor and applies a stylesheet
        to the widget and its child QLabel elements. The stylesheet includes styles for
        the widget's background, border, and hover state, as well as styles for the
        file name label.

        The widget's border is styled as a dashed line with a specified color and
        radius. The background color changes on hover, and the file name label's font
        size and color are set with a transparent background.
        """

        object_name = self.objectName()
        self.setCursor(qtc.Qt.PointingHandCursor)
        self.setStyleSheet(
            f"""
            QLabel {{
                background-color: transparent;
            }}
            #{object_name} {{
                border: 2px dashed #749bab;
                border-radius: 10px;
                background-color: #222d32;   
               
            }}
            #{object_name}:hover {{
                background-color: #435963;
            }}

            #fileNameLabel {{
                font-size: 16px;
                color: #5c7988;
                background-color: transparent;
            }}
            """
        )

    def _create_file_display_labels(self):
        """
        Create and return QLabel objects for displaying the file icon and name.

        This method creates two QLabel objects: one for displaying a file icon and
        another for displaying the file name or instruction text. Both labels are
        centered within the widget.

        Returns
        -------
        Tuple[QLabel, QLabel]
            A tuple containing the QLabel for the file icon and the QLabel for the
            file name.
        """

        file_ico_label = qtw.QLabel(self)
        file_ico_label.setObjectName("fileIcoLabel")
        file_ico_label.setAlignment(qtc.Qt.AlignCenter)

        file_name_label = qtw.QLabel(self.tr("Click Or Drag & Drop A File Here"), self)
        file_name_label.setObjectName("fileNameLabel")
        file_name_label.setAlignment(qtc.Qt.AlignCenter)

        return (file_ico_label, file_name_label)
