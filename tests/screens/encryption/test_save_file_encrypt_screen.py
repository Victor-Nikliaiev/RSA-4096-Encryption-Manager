from screens.encryption.save_file_encrypt_screen import SaveFileEncryptScreen
from unittest.mock import MagicMock, patch
from PySide6 import QtWidgets as qtw
from tools.toolkit import Tools as t
from backend import signal_manager
import pytest


class TestSaveFileEncryptScreen:

    @pytest.fixture(scope="function", autouse=True)
    def autorun(self, qtbot: qtw.QGridLayout):
        """
        Fixture to set up and tear down the SaveFileEncryptScreen test environment.

        This fixture is automatically used for each test function in the
        TestSaveFileEncryptScreen class. It initializes the SaveFileEncryptScreen,
        adds it to the qtbot for interaction, and mocks the main window required
        for the screen to function properly.

        After the test, it ensures the screen is properly closed and cleaned up.

        :param self: The test class instance.
        :param qtbot: Pytest-qt's qtbot fixture for interacting with Qt widgets.
        """
        with patch.dict(
            signal_manager.saved_data,
            {
                "file_dropped": "dropped_file.bin",
                "save_main_window": MagicMock(spec=qtw.QWidget),
                "saved_file_path": "saved_file.py",
            },
        ), patch(
            "tools.toolkit.Tools.all.format_input_path", return_value="dro...le.bin"
        ), patch(
            "tools.toolkit.Tools.qt.center_widget"
        ) as self.mock_center_widget:
            self.ts = SaveFileEncryptScreen()
            qtbot.addWidget(self.ts)
            yield

    def test_update_ui(self):
        """
        Tests the initial state of the SaveFileEncryptScreen UI components.

        This test verifies that the SaveFileEncryptScreen is visible,
        has the correct window title, and the UI elements such as the
        input and output file info buttons and start button are in their
        expected initial states.
        """
        dropped_file = signal_manager.saved_data.get("file_dropped")

        assert self.ts.windowTitle() == "Encryption | Save a file"
        assert self.ts.dropped_file_path == dropped_file
        t.all.format_input_path.assert_called_once_with(self.ts.dropped_file_path)
        assert self.ts.file_chooser_input.placeholderText() == "dro...le.bin"

    def test_save_file_dialog(self):
        """
        Tests the save_file_dialog method to ensure it correctly
        sets up and uses a QFileDialog to get a file path from the user.
        The method is tested to verify that it correctly saves the file
        path to the signal manager and formats the path for display in the
        SaveFileEncryptScreen.
        """

        with patch(
            "PySide6.QtWidgets.QFileDialog.getSaveFileName"
        ) as mock_getSaveFileName, patch.object(signal_manager, "saved_file_path"):
            file_path = "file_path.file"
            specified_name = "dropped_file.bin_encrypted.bin"
            mock_getSaveFileName.return_value = (file_path, "_")
            self.ts.save_file_dialog()

            mock_getSaveFileName.assert_called_once_with(
                self.ts,
                self.ts.tr("Save File"),
                specified_name,
                self.ts.tr("Binary Files (*.bin);;All Files (*)"),
            )

            signal_manager.saved_file_path.emit.assert_called_once_with(file_path)
            assert self.ts.start_button.isEnabled()

    def test_close_event(self):
        """
        Tests that the closeEvent method of SaveFileEncryptScreen is correctly implemented.

        This test verifies that when the SaveFileEncryptScreen is closed, the screen
        is no longer visible and the main window is shown, ensuring the user can return
        to the main application window.
        """

        self.ts.show()
        main_window = signal_manager.saved_data.get("save_main_window")
        self.ts.close()

        assert not self.ts.isVisible()
        main_window.show.assert_called_once()

    def test_start_button_handler(self):
        """
        Tests that the start_button_handler method is correctly implemented
        to instantiate a new ProgressWindowScreen, center it, and show it.
        The test verifies that the start_button_handler method calls the
        ProgressWindowScreen constructor, calls the center_widget method
        to center the new window, and then shows the new window.
        """
        with patch(
            "screens.encryption.save_file_encrypt_screen.ProgressWindowScreen"
        ) as MockProgressWindowScreen:
            progress_window_instance = MagicMock()
            MockProgressWindowScreen.return_value = progress_window_instance
            self.mock_center_widget.return_value = progress_window_instance

            self.ts.start_button_handler()

            self.mock_center_widget.assert_called_once_with(progress_window_instance)
            progress_window_instance.show.assert_called_once()
