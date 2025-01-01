from screens.encryption.encryption_progress_window_screen import ProgressWindowScreen
from unittest.mock import MagicMock, patch
from PySide6 import QtWidgets as qtw
from backend import signal_manager
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg
from functools import partial
import pytest


class TestEncryptionProgressWindowScreen:

    @pytest.fixture(scope="function", autouse=True)
    def autorun(self, qtbot: qtw.QGridLayout):
        """
        Fixture to set up and tear down the ProgressWindowScreen test environment.

        This fixture is automatically used for each test function in the
        TestEncryptionProgressWindowScreen class. It patches various components
        necessary for testing the ProgressWindowScreen, including methods and
        attributes to mock, and sets up a test instance of the screen.

        The fixture provides a mocked environment for the encryption process,
        simulating file paths, public keys, and signal manager data. It also
        configures the UI elements for testing without displaying actual dialogs.

        :param self: The test class instance.
        :param qtbot: Pytest-qt's qtbot fixture for interacting with Qt widgets.
        """
        self.original__handle_encryption = ProgressWindowScreen._handle_encryption

        with patch(
            "PySide6.QtWidgets.QMessageBox.question",
            return_value=qtw.QMessageBox.Yes,
        ) as self.mock_question, patch.dict(
            signal_manager.saved_data,
            {
                "save_main_window": MagicMock(qtw.QWidget),
                "file_dropped": "test_file.txt",
                "saved_file_path": "output_file.txt",
                "public_key_accepted": "test_public_key",
                "update_processed_bytes": 500,
            },
        ), patch.object(
            qtw.QWidget, "thread"
        ) as self.mock_thread, patch(
            "tools.toolkit.Tools.qt.center_widget"
        ) as self.mock_center_widget, patch.object(
            target=ProgressWindowScreen,
            attribute="_handle_encryption",
            return_value=None,
        ) as self.mock_handle_encryption:
            with patch("os.path.getsize", return_value=1000):
                self.ts = ProgressWindowScreen()
                qtbot.addWidget(self.ts)
                yield

    def test_update_ui(self):
        """
        Tests the initial state of the ProgressWindowScreen UI components for encryption.

        This test verifies that the ProgressWindowScreen is visible,
        has the correct window title for an encryption process, and the UI
        elements such as the window flags and centering are in their expected states.
        It asserts the window title is "Encryption...", checks that the window flags
        are set correctly, and ensures the widget is centered on the screen.
        """

        assert self.ts.windowTitle() == "Encryption..."
        assert self.ts.windowFlags() == (
            qtc.Qt.Window | qtc.Qt.WindowTitleHint | qtc.Qt.WindowSystemMenuHint
        )
        self.mock_center_widget.assert_called_once_with(self.ts)

    def test_update_processed_bytes_handler(self):
        """
        Tests the update_processed_bytes_handler method to ensure that it correctly
        updates the progress bar value based on the bytes processed.

        This test verifies that when the method is called with a given
        number of bytes, the operation_progress bar is updated with the
        corresponding percentage value.
        """

        self.ts.update_processed_bytes_handler(500)
        assert self.ts.operation_progress.value() == 50

    def test_operation_completed_handler(self):
        """
        Tests the operation_completed_handler method to ensure that it correctly
        handles the encryption operation completion.

        This test verifies that the operation_completed_handler method displays
        a success message box, calls the cleanup_thread method to clean up the
        encryption thread, and saves the main window for later use. It also checks
        that the method saves the main window to the signal manager, and that the
        main window show method is called once.
        """
        with patch(
            "PySide6.QtWidgets.QMessageBox.information"
        ) as mock_q_message_information, patch.object(
            target=ProgressWindowScreen, attribute="cleanup_thread", return_value=None
        ) as mock_cleanup_thread:
            self.ts.show()
            message_title = self.ts.tr("Success")
            message_text = self.ts.tr("Operation has been completed successfully")

            self.ts.operation_completed_handler()
            signal_manager.saved_data["save_main_window"] = MagicMock(qtw.QWidget)
            mock_q_message_information.assert_called_once_with(
                self.ts, message_title, message_text
            )
            mock_cleanup_thread.assert_called_once()
            assert not self.ts.isVisible()

    def test_closeEvent(self):
        """
        Tests that the closeEvent method of ProgressWindowScreen is correctly
        implemented to handle the window close event.

        This test verifies that when the window is closed, the main window is
        shown, and the event is accepted. It also checks that when the
        exit_without_dialog flag is False, a confirmation dialog is shown to
        confirm the user's intention to exit. If the user confirms, the thread
        is stopped, the main window is shown, and the event is accepted. If the
        user cancels, the event is ignored and the window is not closed.
        """

        with patch.object(
            target=ProgressWindowScreen, attribute="cleanup_thread", return_value=None
        ) as mock_cleanup_thread:
            self.ts.exit_without_dialog = True
            mock_event = MagicMock(spec=qtg.QCloseEvent)

            main_window: MagicMock = signal_manager.saved_data["save_main_window"]
            self.ts.closeEvent(mock_event)
            signal_manager.saved_data["save_main_window"] = main_window
            mock_event.accept.assert_called_once()
            main_window.show.assert_called_once()
            mock_event.accept.assert_called_once()

            self.ts.exit_without_dialog = False
            self.ts.closeEvent(mock_event)
            signal_manager.saved_data["save_main_window"] = main_window

            self.mock_question.assert_called_once_with(
                self.ts,
                self.ts.tr("Exit"),
                self.ts.tr(
                    "Are you sure you want to exit, it will interrupt current encryption?"
                ),
                qtw.QMessageBox.Yes | qtw.QMessageBox.No,
            )

            mock_cleanup_thread.assert_called_once()
            assert main_window.show.call_count == 2
            assert mock_event.accept.call_count == 2

    def test_cleanup_thread(self):
        """
        Tests the cleanup_thread method of ProgressWindowScreen to ensure that it
        correctly cleans up the resources associated with the encryption thread.

        This test verifies that when the method is called, the thread is stopped,
        waited for, and then deleted. This ensures that all resources associated
        with the thread are properly released.
        """

        with patch("backend.signal_manager.signal_manager.stop_process"), patch.object(
            self.ts, "deleteLater"
        ):
            self.ts.show()
            self.ts.thread.quit = MagicMock()
            self.ts.thread.wait = MagicMock()
            self.ts.thread.deleteLater = MagicMock()
            signal_manager.stop_process.emit = MagicMock()

            self.ts.cleanup_thread()

            signal_manager.stop_process.emit.assert_called_once()
            self.ts.thread.quit.assert_called_once()
            self.ts.thread.wait.assert_called_once()
            self.ts.thread.deleteLater.assert_called_once()
            self.ts.deleteLater.assert_called_once()

    def test__handle_encryption(self):
        """
        Tests the _handle_encryption method to ensure that it correctly sets up the FileManager
        instance, moves it to a new thread, and starts the thread. It also verifies that the
        start_encryption signal is connected to the FileManager's encrypt_file method.

        The test verifies that the FileManager's moveToThread method is called with the correct
        arguments and that the start_encryption signal is connected to the encrypt_file method.
        It also checks that the thread is started.

        :return: None
        """
        with patch(
            "screens.encryption.encryption_progress_window_screen.FileManager",
            autospec=True,
        ), patch("PySide6.QtCore.QThread", autospec=True) as MockQThread, patch.object(
            self.ts, "start_encryption", autospec=True
        ):

            thread = MagicMock()
            MockQThread.return_value = thread

            original__handle_encryption = partial(
                self.original__handle_encryption, self.ts
            )

            original__handle_encryption(
                "dropped_file_path", "saved_file_path", "public_key"
            )

            self.ts.file_manager.moveToThread.assert_called_once_with(thread)
            self.ts.start_encryption.connect.assert_called_once()
            self.ts.thread.started.connect.assert_called_once()
