from unittest.mock import MagicMock, patch
from PySide6.QtTest import QSignalSpy
from PySide6 import QtWidgets as qtw
from backend import signal_manager


class Test_SignalManagerSlots:
    def test_save_main_window_handler(self):
        """
        Tests the _save_main_window_handler method to ensure it correctly
        saves the main window widget into the saved data.

        The test verifies that after calling _save_main_window_handler
        with a mock widget, the widget is stored in the saved_data
        dictionary under the "save_main_window" key.
        """

        mock_widget = MagicMock(qtw.QWidget)
        signal_manager._save_main_window_handler(mock_widget)

        assert signal_manager.saved_data["save_main_window"] == mock_widget

    def test_file_dropped_handler(self):
        """
        Tests the _file_dropped_handler method to ensure it correctly
        saves the dropped file path into the saved data.

        The test verifies that after calling _file_dropped_handler
        with a file path, the file path is stored in the saved_data
        dictionary under the "file_dropped" key.
        """

        file_path = "file.path"
        signal_manager._file_dropped_handler(file_path)
        assert signal_manager.saved_data["file_dropped"] == file_path

    def test__public_key_accepted_handler(self):
        """
        Tests the _public_key_accepted_handler method to ensure it correctly
        saves the accepted public RSA key into the saved data.

        The test verifies that after calling _public_key_accepted_handler
        with a public key, the key is stored in the saved_data dictionary
        under the "public_key_accepted" key.
        """

        public_key = "public_key"
        signal_manager._public_key_accepted_handler(public_key)
        assert signal_manager.saved_data["public_key_accepted"] == public_key

    def test__private_key_accepted_handler(self):
        """
        Tests the _private_key_accepted_handler method to ensure it correctly
        saves the accepted private RSA key into the saved data.

        The test verifies that after calling _private_key_accepted_handler
        with a private key, the key is stored in the saved_data dictionary
        under the "private_key_accepted" key.
        """

        private_key = "private_key"
        signal_manager._private_key_accepted_handler(private_key)
        assert signal_manager.saved_data["private_key_accepted"] == private_key

    def test__saved_file_path_handler(self):
        """
        Tests the _saved_file_path_handler method to ensure it correctly
        saves the specified file path into the saved data.

        The test verifies that after calling _saved_file_path_handler
        with a file path, the file path is stored in the saved_data
        dictionary under the "saved_file_path" key.
        """

        file_path = "file.path"
        signal_manager._saved_file_path_handler(file_path)
        assert signal_manager.saved_data["saved_file_path"] == file_path

    def test__update_processed_bytes_handler(self):
        """
        Tests the _update_processed_bytes_handler method to ensure it correctly
        increments the total number of processed bytes.

        The test verifies that after calling _update_processed_bytes_handler
        with a given number of bytes, the total processed bytes are updated
        correctly in the saved_data dictionary.
        """

        signal_manager._update_processed_bytes_handler(100)
        assert signal_manager.saved_data["update_processed_bytes"] == 100

        signal_manager._update_processed_bytes_handler(105)
        assert signal_manager.saved_data["update_processed_bytes"] == 205

        del signal_manager.saved_data["update_processed_bytes"]

    def test__current_window_handler(self):
        """
        Tests the _current_window_handler method to ensure it correctly
        saves the current window object into the saved data.

        The test verifies that after calling _current_window_handler
        with a mock window object, the object is stored in the saved_data
        dictionary under the "current_window" key.
        """

        current_window = MagicMock(qtw.QWidget)
        signal_manager._current_window_handler(current_window)
        assert signal_manager.saved_data["current_window"] == current_window

    def test___critical_error_handler(self):
        """
        Tests the _critical_error_handler method to ensure it displays a critical
        error message and closes the current window without a confirmation dialog.

        The test verifies that after calling _critical_error_handler with a file
        path and an error message, a critical error message box is displayed with
        the correct message, the current window's cleanup_thread method is called
        once, the exit_without_dialog attribute is set to True, and the window is
        closed.
        """

        current_window = MagicMock()
        signal_manager.saved_data["current_window"] = current_window

        with patch("PySide6.QtWidgets.QMessageBox.critical") as mock_critical:
            file_path = "file.path"
            error_message = "error_message"

            signal_manager.critical_error.emit(file_path, error_message)

            mock_critical.assert_called_with(
                None, "Error", f"Error processing file: {file_path}, {error_message}"
            )

            current_window.cleanup_thread.assert_called_once()
            assert current_window.exit_without_dialog is True
            current_window.close.assert_called_once()

    def test__selected_option_handler(self):
        """
        Tests the _selected_option_handler method to ensure it correctly
        saves the selected keygen option into the saved data.

        The test verifies that after calling _selected_option_handler
        with a given option, the option is stored in the saved_data
        dictionary under the "selected_option" key.
        """

        option = "private"
        signal_manager._selected_option_handler(option)
        assert signal_manager.saved_data["selected_option"] == option

    class Test_SignalManagerConnections:
        def test_file_dropped(self):
            """
            Tests that the file_dropped signal is connected to the correct slot
            and that the signal triggers the correct handler with the correct
            argument.

            :param self: The test case instance.
            """

            file_path = "file.path"
            assert self._check_connection_and_integrity(
                signal_manager.file_dropped, "file_dropped", file_path
            )

        def test_public_key_accepted(self):
            """
            Tests that the public_key_accepted signal is connected to the correct slot
            and that the signal triggers the correct handler with the correct
            argument.

            :param self: The test case instance.
            """

            public_key = "public_key"
            assert self._check_connection_and_integrity(
                signal_manager.public_key_accepted, "public_key_accepted", public_key
            )

        def test_private_key_accepted(self):
            """
            Tests that the private_key_accepted signal is connected to the correct slot
            and that the signal triggers the correct handler with the correct
            argument.

            :param self: The test case instance.
            """

            private_key = "private_key"
            assert self._check_connection_and_integrity(
                signal_manager.private_key_accepted, "private_key_accepted", private_key
            )

        def test_save_main_window(self):
            """
            Tests that the save_main_window signal is connected to the correct slot
            and that the signal triggers the correct handler with the correct
            argument.

            The test verifies that after calling save_main_window with a given main
            window, the main window is stored in the saved_data dictionary under the
            "save_main_window" key.
            """

            qtw.QApplication()
            main_window = qtw.QMainWindow()
            signal_manager.save_main_window.emit(main_window)
            assert signal_manager.saved_data["save_main_window"] is main_window

        def test_saved_file_path(self):
            """
            Tests that the saved_file_path signal is connected to the correct slot
            and that the signal triggers the correct handler with the correct
            argument.

            The test verifies that after calling saved_file_path with a given file
            path, the file path is stored in the saved_data dictionary under the
            "saved_file_path" key.
            """

            file_path = "file.path"
            assert self._check_connection_and_integrity(
                signal_manager.saved_file_path, "saved_file_path", file_path
            )

        def test_update_processed_bytes(self):
            """
            Tests that the update_processed_bytes signal is connected to the correct slot
            and that the signal triggers the correct handler with the correct
            argument.

            The test verifies that after emitting the update_processed_bytes signal with a
            given number of bytes, the handler updates the saved data correctly.
            """

            bytes_processed = 100
            assert self._check_connection_and_integrity(
                signal_manager.update_processed_bytes,
                "update_processed_bytes",
                bytes_processed,
            )

        def test_current_window(self):
            """
            Tests that the current_window signal is connected to the correct slot
            and that the signal triggers the correct handler with the correct
            argument.

            The test verifies that after calling current_window with a given window
            object, the object is stored in the saved_data dictionary under the
            "current_window" key.
            """

            current_window = qtw.QWidget()
            signal_manager.current_window.emit(current_window)
            assert signal_manager.saved_data["current_window"] is current_window

        def test_critical_error(self):
            """
            Tests the critical_error method to ensure it displays a critical
            error message, calls the cleanup_thread method on the current window,
            sets the exit_without_dialog attribute of the current window to True,
            and closes the window.

            The test verifies that after emitting the critical_error signal with a
            file path and an error message, the error message box is displayed with
            the correct message, the current window's cleanup_thread method is called
            once, the exit_without_dialog attribute is set to True, and the window is
            closed.
            """

            with patch("PySide6.QtWidgets.QMessageBox.critical") as mock_critical:
                file_path = "file.path"
                error_message = "error_message"
                mock_window = MagicMock()
                signal_manager.saved_data["current_window"] = mock_window
                signal_manager.critical_error.emit(file_path, error_message)

                mock_window.cleanup_thread.assert_called_once()
                assert mock_window.exit_without_dialog is True
                mock_window.close.assert_called_once()

        def test_selected_option(self):
            """
            Tests that the selected_option signal is connected to the correct slot
            and that the signal triggers the correct handler with the correct
            argument.

            The test verifies that after emitting the selected_option signal with a
            given option, the handler updates the saved data correctly.
            """

            option = "private"
            assert self._check_connection_and_integrity(
                signal_manager.selected_option, "selected_option", option
            )

        def _check_connection_and_integrity(self, signal, signal_name, option):
            """
            Checks if the given signal is connected to the appropriate slot and verifies
            that the emitted signal triggers the correct handler with the correct argument.

            This method uses QSignalSpy to capture the signal emission and checks that the
            emitted value matches the expected option. It also verifies that the saved data
            is updated correctly in the signal manager.

            :param signal: The signal to be emitted and checked.
            :param signal_name: The name of the signal, used as a key in the saved data.
            :param option: The expected value to be emitted by the signal and stored in the saved data.

            :return: True if the signal emission and saved data match the expected option, False otherwise.
            """

            spy = QSignalSpy(signal)
            signal.emit(option)

            return (
                spy.at(0)[0] == option
                and signal_manager.saved_data[signal_name] == option
            )
