from screens.encryption.choose_file_encrypt_screen import ChooseFileEncryptScreen
from unittest.mock import MagicMock, patch
from PySide6 import QtWidgets as qtw
from backend import signal_manager
import pytest


class TestChooseFileEncryptScreen:

    @pytest.fixture(scope="function", autouse=True)
    def autorun(self, qtbot: qtw.QGridLayout):
        """
        Fixture to set up and tear down the ChooseFileEncryptScreen test environment.

        This fixture is automatically used for each test function in the
        TestChooseFileEncryptScreen class. It initializes the ChooseFileEncryptScreen,
        adds it to the qtbot for interaction, and mocks the main window required
        for the screen to function properly.

        After the test, it ensures the screen is properly closed and cleaned up.

        :param self: The test class instance.
        :param qtbot: Pytest-qt's qtbot fixture for interacting with Qt widgets.
        """
        signal_manager.saved_data["save_main_window"] = MagicMock(spec=qtw.QWidget)
        self.ts = ChooseFileEncryptScreen()
        qtbot.addWidget(self.ts)
        yield

    def test_handle_click_next(self, qtbot: qtw.QGridLayout):
        """
        Tests that the handle_click_next method is correctly implemented
        to hide the ChooseFileEncryptScreen, create a new ChoosePublicKeyScreen
        instance, center it, and show it.

        The test verifies that the handle_click_next method calls the
        ChoosePublicKeyScreen constructor, calls the center_widget method
        to center the new window, and then shows the new window.
        """
        with patch("tools.toolkit.Tools.qt.center_widget") as mock_center_widget, patch(
            "screens.encryption.choose_file_encrypt_screen.ChoosePublicKeyScreen"
        ) as MockChoosePublicKeyScreen:

            mock_new_screen = MagicMock(spec=qtw.QWidget)
            mock_center_widget.return_value = mock_new_screen
            MockChoosePublicKeyScreen.return_value = mock_new_screen
            self.ts.handle_click_next()

            mock_center_widget.assert_called_once_with(mock_new_screen)
            mock_new_screen.show.assert_called_once()
            assert self.ts.isVisible() is False

    def test_update_next_button_status(self):
        """
        Tests that the update_next_button_status method is correctly implemented
        to update the enabled status of the "Next" button based on the given
        status that comes from the DragDropWidget.
        """
        self.ts.update_next_button_status(True)
        assert self.ts.next_button.isEnabled()

        self.ts.update_next_button_status(False)
        assert not self.ts.next_button.isEnabled()

    def test_closeEvent(self):
        """
        Tests that the closeEvent method is correctly implemented to hide
        the ChooseFileEncryptScreen and show the main window.

        This test verifies that when the ChooseFileEncryptScreen is closed,
        the main window is made visible again, ensuring the user can return
        to the main application window.
        """

        main_window = signal_manager.saved_data.get("save_main_window")
        self.ts.show()
        self.ts.close()

        assert not self.ts.isVisible()
        main_window.show.assert_called_once()
