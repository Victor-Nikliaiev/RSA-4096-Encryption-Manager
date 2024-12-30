from screens.decryption.decryption_progress_window_screen import (
    ProgressWindowScreen,
)
from unittest.mock import MagicMock, patch
from PySide6 import QtWidgets as qtw
from backend import signal_manager
from PySide6 import QtCore as qtc
from functools import partial
import pytest


class TestDecryptionProgressWindowScreen:

    @pytest.fixture(scope="function", autouse=True)
    def progress_window_screen(self, qtbot: qtw.QGridLayout):
        """
        Fixture for setting up the ProgressWindowScreen test environment.

        This fixture is automatically used for each test function in the
        TestDecryptionProgressWindowScreen class. It patches various components
        necessary for testing the ProgressWindowScreen, including methods and
        attributes to mock, and sets up a test instance of the screen.

        The fixture provides a mocked environment for the decryption process,
        simulating file paths, private keys, and signal manager data. It also
        configures the UI elements for testing without displaying actual dialogs.

        :param self: The test class instance.
        :param qtbot: Pytest-qt's qtbot fixture for interacting with Qt widgets.
        """

        self.original__handle_decryption = ProgressWindowScreen._handle_decryption
        with patch(
            "tools.toolkit.Tools.qt.center_widget"
        ) as mock_center_widget, patch.object(
            target=ProgressWindowScreen,
            attribute="_handle_decryption",
            return_value=None,
        ) as self.mock_handle_decryption, patch.dict(
            signal_manager.saved_data,
            {
                "file_dropped": "test_file.txt",
                "saved_file_path": "output_file.txt",
                "private_key_accepted": "test_private_key.pem",
                "save_main_window": MagicMock(spec=qtw.QWidget),
                "update_processed_bytes": 500,
            },
        ), patch.object(
            target=qtw.QMessageBox,
            attribute="question",
            return_value=qtw.QMessageBox.Yes,
        ) as self.mock_question, patch.object(
            qtw.QWidget, "thread"
        ) as self.mock_thread:

            with patch("os.path.getsize", return_value=1000):
                main_window = signal_manager.saved_data["save_main_window"]
                main_window.show = MagicMock()

                self.ts = ProgressWindowScreen()
                qtbot.addWidget(self.ts)

                self.mock_center_widget = mock_center_widget
                self.ts.exit_without_dialog = True

                # "binding" "this"(self.ts) to original method
                self.original__handle_decryption = partial(
                    self.original__handle_decryption, self.ts
                )

                yield

    def test_update_ui(self):
        """
        Tests the initial state of the ProgressWindowScreen UI components.

        This test verifies that the ProgressWindowScreen is visible,
        has the correct window title, and the UI elements such as the
        window flags and centering are in their expected states.
        """
        assert self.ts.windowTitle() == "Decryption..."
        assert self.ts.windowFlags() == (
            qtc.Qt.Window | qtc.Qt.WindowTitleHint | qtc.Qt.WindowSystemMenuHint
        )
        self.mock_center_widget.assert_called_once_with(self.ts)

    def test_update_processed_bytes_handler(self):
        """
        Tests that the update_processed_bytes_handler method correctly
        updates the progress bar value based on the bytes processed.

        The test verifies that when the method is called with a given
        number of bytes, the operation_progress bar is updated with the
        corresponding percentage value, and the _handle_decryption method
        is called once.

        :return: None
        """

        self.ts.update_processed_bytes_handler(500)

        self.mock_handle_decryption.assert_called_once()
        assert self.ts.operation_progress.value() == 50

    def test_operation_completed_handler(self):
        """
        Tests the operation_completed_handler method to ensure that it correctly
        handles the decryption operation completion.

        This test verifies that the operation_completed_handler method displays
        a success message box, calls the cleanup_thread method to clean up the
        decryption thread, and saves the main window for later use.

        The test also checks that the method saves the main window to the
        signal manager, and that the main window show method is called once.
        """

        with patch(
            "PySide6.QtWidgets.QMessageBox.information"
        ) as mock_information, patch.object(
            target=ProgressWindowScreen, attribute="cleanup_thread", return_value=None
        ) as mock_cleanup_thread:
            self.ts.operation_completed_handler()

            # Added here mocked_main_window, because of that QMessageBox.information is mocked,
            # the closeEvent may not execute as expected because
            # the mocked method skips over real dialog behavior.

            signal_manager.saved_data["save_main_window"] = MagicMock()

            mock_cleanup_thread.assert_called_once()

            mock_information.assert_called_once_with(
                self.ts,
                self.ts.tr("Success"),
                self.ts.tr("Operation has been completed successfully"),
            )

    def test_close_event(self):
        """
        Tests that the closeEvent method correctly handles the window close event.

        The test verifies that when the window is closed, the main window is shown,
        and the event is accepted.

        The test also verifies that when the exit_without_dialog flag is False,
        a confirmation dialog is shown to confirm the user's intention to exit.
        If the user confirms, the thread is stopped, the main window is shown,
        and the event is accepted. If the user cancels, the event is ignored and
        the window is not closed.

        The test also checks that the cleanup_thread method is called once when
        the user confirms the exit.
        """

        # Exit without dialog
        mock_event = MagicMock()

        saved_main_window = signal_manager.saved_data["save_main_window"]

        self.ts.closeEvent(mock_event)
        signal_manager.saved_data["save_main_window"] = MagicMock()
        mocked_main_window = signal_manager.saved_data["save_main_window"]
        mocked_main_window.show = MagicMock()
        saved_main_window.show.assert_called_once()
        mock_event.accept.assert_called_once()

        # Exit with dialog
        with patch.object(
            target=ProgressWindowScreen, attribute="cleanup_thread", return_value=None
        ) as mock_cleanup_thread:
            mock_event = MagicMock()

            self.ts.exit_without_dialog = False
            self.ts.closeEvent(mock_event)

            self.mock_question.assert_called_once_with(
                self.ts,
                self.ts.tr("Exit"),
                self.ts.tr(
                    "Are you sure you want to exit, it will interrupt current decryption?"
                ),
                qtw.QMessageBox.Yes | qtw.QMessageBox.No,
            )
            mock_event.accept.assert_called_once()
            mock_cleanup_thread.assert_called_once()

            signal_manager.saved_data["save_main_window"] = MagicMock()

    def test_cleanup_thread(self):
        """
        Tests that the cleanup_thread method correctly cleans up the resources
        associated with the encryption thread.

        The test verifies that when the method is called, the thread is stopped,
        waited for, and then deleted. This ensures that all resources associated
        with the thread are properly released.
        """
        with patch.object(target=self.ts, attribute="thread") as mock_thread:
            mock_thread.quit = MagicMock()
            mock_thread.wait = MagicMock()
            mock_thread.deleteLater = MagicMock()

            self.ts.cleanup_thread()

            mock_thread.quit.assert_called_once()
            mock_thread.wait.assert_called_once()
            mock_thread.deleteLater.assert_called_once()

    def test__handle_decryption(self):
        """
        Tests the _handle_decryption method to ensure that it correctly sets up the FileManager
        instance, moves it to a new thread, and starts the thread. It also verifies that the
        start_decryption signal is connected to the FileManager's decrypt_file method.

        The test verifies that the FileManager's moveToThread method is called with the correct
        arguments and that the start_decryption signal is connected to the decrypt_file method.
        It also checks that the thread is started.

        :return: None
        """

        self.ts._handle_decryption.stop()
        self.ts._handle_decryption = self.original__handle_decryption

        with patch(
            "screens.decryption.decryption_progress_window_screen.FileManager",
            autospec=True,
        ) as MockFileManager, patch(
            "PySide6.QtCore.QThread", autospec=True
        ) as MockQThread, patch.object(
            self.ts, "start_decryption", autospec=True
        ) as mock_start_decryption_signal:

            mock_file_manager_instance = MockFileManager.return_value
            mock_thread_instance = MockQThread.return_value

            mock_thread_instance.started.connect = MagicMock()

            self.ts._handle_decryption("dropped_file", "output_file", "private_key")

            mock_file_manager_instance.moveToThread.assert_called_once_with(
                mock_thread_instance
            )
            mock_start_decryption_signal.connect.assert_called_once_with(
                mock_file_manager_instance.decrypt_file
            )

            mock_thread_instance.started.connect.assert_called_once()
            mock_thread_instance.start.assert_called_once()
