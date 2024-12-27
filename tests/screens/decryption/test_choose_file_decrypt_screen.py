from screens.decryption import ChooseFileDecryptScreen
from unittest.mock import MagicMock, patch
from PySide6 import QtWidgets as qtw
from backend import signal_manager


class TestChooseFileDecryptScreen:
    @patch("tools.toolkit.Tools.qt.center_widget")
    @patch("screens.decryption.choose_file_decrypt_screen.ChoosePrivateKeyScreen")
    def test_handle_click_next(
        self, mock_choose_private_key_screen, mock_center_widget, qtbot
    ):
        """
        Tests that the handle_click_next method is correctly implemented
        to hide the ChooseFileDecryptScreen, create a new ChoosePrivateKeyScreen
        instance, center it, and show it.

        The test verifies that the handle_click_next method calls the
        ChoosePrivateKeyScreen constructor, calls the center_widget method
        to center the new window, and then shows the new window.
        """
        mock_new_screen = MagicMock(spec=qtw.QWidget)
        mock_choose_private_key_screen.return_value = mock_new_screen
        mock_center_widget.return_value = mock_new_screen

        test_window = ChooseFileDecryptScreen()
        qtbot.addWidget(test_window)
        test_window.show()

        test_window.handle_click_next()

        assert not test_window.isVisible()

        mock_choose_private_key_screen.assert_called_once_with()
        mock_center_widget.assert_called_once_with(mock_new_screen)

        mock_new_screen.show.assert_called_once()

    def test_update_next_button_status(self, qtbot):
        """
        Tests that the update_next_button_status method is correctly implemented
        to update the enabled status of the "Next" button based on the given
        status that comes from the DragDropWidget.
        """

        test_window = ChooseFileDecryptScreen()
        qtbot.addWidget(test_window)
        test_window.show()

        signal_manager.update_next_button_status.emit(False)
        assert not test_window.next_button.isEnabled()

        signal_manager.update_next_button_status.emit(True)
        assert test_window.next_button.isEnabled()

    @patch.dict(
        signal_manager.saved_data, {"save_main_window": MagicMock(spec=qtw.QWidget)}
    )
    def test_close_event(self, qtbot: qtw.QGridLayout):
        """
        Tests that the closeEvent method is correctly implemented to hide
        the ChooseFileDecryptScreen and show the main window.

        This test verifies that when the ChooseFileDecryptScreen is closed,
        the main window is made visible again, ensuring the user can return
        to the main application window.
        """

        main_window_mock = signal_manager.saved_data["save_main_window"]
        test_screen = ChooseFileDecryptScreen()
        qtbot.addWidget(test_screen)
        test_screen.show()
        test_screen.close()

        assert not test_screen.isVisible()

        main_window_mock.show.assert_called_once()
