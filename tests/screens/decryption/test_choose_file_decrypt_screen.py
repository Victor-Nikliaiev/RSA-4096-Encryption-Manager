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
        test_window = ChooseFileDecryptScreen()
        qtbot.addWidget(test_window)
        test_window.show()

        signal_manager.update_next_button_status.emit(False)

        assert not test_window.next_button.isEnabled()

    @patch.dict(
        signal_manager.saved_data, {"save_main_window": MagicMock(spec=qtw.QWidget)}
    )
    def test_close_event(self, qtbot: qtw.QGridLayout):
        main_window_mock = signal_manager.saved_data["save_main_window"]
        test_screen = ChooseFileDecryptScreen()
        qtbot.addWidget(test_screen)
        test_screen.show()
        test_screen.close()

        assert not test_screen.isVisible()

        main_window_mock.show.assert_called_once()
