from unittest.mock import MagicMock, patch
from backend import signal_manager
from screens.decryption.decryption_progress_window_screen import ProgressWindowScreen
from screens.decryption.save_file_decrypt_screen import SaveFileDecryptScreen
import pytest
import sys
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg
from PySide6 import QtUiTools as qtu
from tools.toolkit import Tools as t


from PySide6 import QtWidgets as qtw


class TestSaveFileDecryptScreen:
    @pytest.fixture(scope="function", autouse=True)
    def startup_fixture(self, qtbot: qtw.QGridLayout):
        """
        Fixture to set up and tear down the SaveFileDecryptScreen test environment.

        This fixture is automatically used for each test function in the
        TestSaveFileDecryptScreen class. It initializes the SaveFileDecryptScreen,
        adds it to the qtbot for interaction, and mocks the main window required
        for the screen to function properly.

        After the test, it ensures the screen is properly closed and cleaned up.

        :param self: The test class instance.
        :param qtbot: Pytest-qt's qtbot fixture for interacting with Qt widgets.
        """

        self.ts = SaveFileDecryptScreen()
        qtbot.addWidget(self.ts)
        signal_manager.saved_data["save_main_window"] = MagicMock(spec=qtw.QWidget)
        self.ts.show()
        yield
        self.ts.deleteLater()

    def test_update_ui(self):
        """
        Tests the initial state of the SaveFileDecryptScreen UI components.

        This test verifies that the SaveFileDecryptScreen is visible,
        has the correct window title, and the UI elements such as the
        input and output file info buttons and start button are in their
        expected initial states.
        """
        assert self.ts.isVisible()
        assert self.ts.windowTitle() == "Decryption | Save a file"
        assert self.ts.input_file_info_btn.text() == "File to be decrypted:"
        assert (
            self.ts.output_file_info_btn.text()
            == "Choose file name for decrypted file:"
        )

        assert self.ts.start_button.text() == "Start Decryption"

    def test_save_file_dialog(self):
        """
        Tests the save_file_dialog method to ensure it correctly
        sets up and uses a QFileDialog to get a file path from the user.
        The method is tested to verify that it correctly saves the file
        path to the signal manager and formats the path for display in the
        SaveFileDecryptScreen.
        """

        with patch(
            "PySide6.QtWidgets.QFileDialog.getSaveFileName"
        ) as mock_get_save_file, patch(
            "tools.toolkit.Tools.all.format_input_path",
        ) as mock_format_input_path:
            saved_file = "saved_file.txt"
            formatted_saved_file_path = "sav...file.txt"
            mock_get_save_file.return_value = (saved_file, "")
            mock_format_input_path.return_value = formatted_saved_file_path
            self.ts.dropped_file_path = "dropped_file.txt"
            self.ts.save_file_dialog()

            assert signal_manager.saved_data["saved_file_path"] == saved_file
            mock_format_input_path.assert_called_once_with(saved_file)
            assert (
                self.ts.saved_name_input.placeholderText() == formatted_saved_file_path
            )

    def test_close_event(self):
        """
        Tests the closeEvent method to ensure that the SaveFileDecryptScreen
        is hidden and the main window is shown when the close event is triggered.

        This test verifies that the main window's show method is called once,
        the close event is accepted, and the SaveFileDecryptScreen is no longer visible.
        """

        mock_event = MagicMock()
        mock_event.accept = MagicMock()

        main_window = signal_manager.saved_data.get("save_main_window")
        main_window.show = MagicMock()

        self.ts.closeEvent(mock_event)

        main_window.show.assert_called_once()
        mock_event.accept.assert_called_once()

        self.ts.close()

        assert self.ts.isVisible() is False

    def test_start_button_handler(self):
        """
        Tests that the start button handler correctly sets up a new
        ProgressWindowScreen, shows it, and hides the SaveFileDecryptScreen.

        The test verifies that when the start button is clicked, the
        ProgressWindowScreen is instantiated, shown, and the SaveFileDecryptScreen
        is hidden.
        """
        self.ts.start_button_handler()

        assert self.ts.progress_window.isVisible()
        assert isinstance(self.ts.progress_window, ProgressWindowScreen)
        assert self.ts.isVisible() is False
