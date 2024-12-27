from unittest.mock import patch, MagicMock
from screens.about import AboutScreen
from backend import signal_manager
from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from main import MainWindow


class TestAboutScreen:
    def test_update_ui(self, qtbot: qtw.QGridLayout):
        """
        Tests that the AboutScreen widget is configured correctly upon initialization.
        Specifically, it asserts that the window is a frameless window and that the
        scrollArea is a QScrollArea object.
        """
        about_screen = AboutScreen()
        qtbot.addWidget(about_screen)
        about_screen.show()
        about_screen.windowFlags() == (qtc.Qt.FramelessWindowHint | qtc.Qt.Window)

        assert isinstance(about_screen.scrollArea, qtw.QScrollArea)

    @patch("PySide6.QtCore.QObject.installEventFilter")
    def test_install_event_listeners(
        self, mock_installEventFilter: MagicMock, qtbot: qtw.QGridLayout
    ):
        """
        Tests that the event listeners for the AboutScreen's widgets are installed
        correctly upon initialization.

        This test uses a mock object to verify that the installEventFilter method
        is called the correct number of times with the correct widget arguments.
        """
        signal_manager.save_main_window.emit(MainWindow())

        about_screen = AboutScreen()
        qtbot.addWidget(about_screen)
        about_screen.show()

        widget_list = [
            about_screen.app_name_lb,
            about_screen.label,
            about_screen.label_2,
            about_screen.label_3,
            about_screen.frame,
        ]

        assert mock_installEventFilter.call_count == len(widget_list)

    def test_mouse_press_event(self, qtbot: qtw.QGridLayout):
        """
        Tests that the AboutScreen widget is hidden when a mouse button is clicked.

        This test verifies that the AboutScreen's mousePressEvent method is correctly
        implemented to hide the widget when a mouse button is clicked.
        """
        about_screen = AboutScreen()
        qtbot.addWidget(about_screen)
        about_screen.show()
        about_screen.mousePressEvent(qtc.QEvent.MouseButtonPress)

        assert not about_screen.isVisible()

    @patch("tools.toolkit.Tools.qt.center_widget")
    @patch.dict(
        signal_manager.saved_data, {"save_main_window": MagicMock(spec=qtw.QWidget)}
    )
    def test_close_event(self, mock_center_widget: MagicMock, qtbot: qtw.QGridLayout):
        """
        Tests that the AboutScreen's closeEvent method is correctly implemented to
        show the main window after the AboutScreen is closed.

        This test verifies that the closeEvent method calls the center_widget method
        to center the main window and then shows the main window.
        """
        main_window_mock = MagicMock(spec=qtw.QWidget)
        mock_center_widget.return_value = main_window_mock
        about_screen = AboutScreen()
        qtbot.addWidget(about_screen)
        about_screen.show()
        about_screen.close()

        mock_center_widget.assert_called_with(
            signal_manager.saved_data["save_main_window"]
        )

        main_window_mock.show.assert_called_once()
