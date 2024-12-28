from screens.decryption.choose_private_key_screen import ChoosePrivateKeyScreen
from screens.decryption.save_file_decrypt_screen import SaveFileDecryptScreen
from unittest.mock import MagicMock, patch
from PySide6 import QtWidgets as qtw
from tools.toolkit import Tools as t
from backend import signal_manager
import pytest


class TestChoosePrivateKeyScreen:
    @pytest.fixture(scope="function", autouse=True)
    def auto_fixture(self, qtbot: qtw.QGridLayout):
        # ts = tested_screen

        """
        Auto fixture to initialize and cleanup ChoosePrivateKeyScreen.

        This fixture is necessary because Pytest's qtbot fixture doesn't work
        well with our screen class. The screen needs to be initialized and
        shown before the test starts, and then cleaned up after the test
        finishes. This fixture takes care of that.

        The screen is initialized and shown. The qtbot is passed to the
        fixture, and the tested screen is stored in self.ts.

        The fixture also sets up a mock of the main window, which is
        necessary for the screen to work properly.

        After the test is finished, the fixture will clean up the tested
        screen by calling deleteLater() on it.
        """
        self.ts = ChoosePrivateKeyScreen()
        qtbot.addWidget(self.ts)
        signal_manager.saved_data["save_main_window"] = MagicMock(spec=qtw.QWidget)
        self.ts.show()
        self.ts.show()

        yield
        self.ts.deleteLater()

    def test_update_ui(self):
        """
        Tests the initial state of the ChoosePrivateKeyScreen UI components.

        This test verifies that the ChoosePrivateKeyScreen is visible,
        has the correct window title, and the UI elements such as the
        browse button and radio buttons are in their expected enabled or
        disabled states. Additionally, it checks that the text and
        placeholder text of key input fields are set correctly.
        """

        assert self.ts.isVisible()
        assert self.ts.windowTitle() == "Decryption | Choose a private key"
        assert self.ts.browse_button.isEnabled()
        assert not self.ts.key_text_area.isEnabled()
        assert self.ts.file_radio.text() == "Load private key from file"
        assert self.ts.text_radio.text() == "Enter private key manually"
        assert (
            self.ts.file_path_input.placeholderText()
            == "Browse for a private key file (the path will be generated automatically)..."
        )
        assert (
            self.ts.key_text_area.placeholderText() == "Enter your private key here..."
        )

    def test_toggle_input_mode(self):
        """
        Tests that the toggle_input_mode method correctly enables/disables the browse button and
        the private key text area based on the status of the radio button. If the radio button is
        toggled on (i.e., the user wants to load the private key from a file), the private key text
        area is cleared, and if the radio button is toggled off (i.e., the user wants to enter the
        private key manually), the file path input is cleared.
        """

        self.ts.file_radio.toggled.emit(True)

        assert self.ts.browse_button.isEnabled()
        assert not self.ts.key_text_area.isEnabled()

        self.ts.file_radio.toggled.emit(False)

        assert not self.ts.browse_button.isEnabled()
        assert self.ts.key_text_area.isEnabled()

    def test_browse_file(self):
        """
        Tests that the browse_file method correctly sets the selected_file_path
        attribute and sets the text of the file_path_input to the selected file
        path. The test uses a mock of QFileDialog.getOpenFileName to simulate
        the user selecting a file.
        """
        mock_file_path = "home/username/path/to/private_key.pem"
        with patch(
            "PySide6.QtWidgets.QFileDialog.getOpenFileName",
            return_value=(mock_file_path, ""),
        ):

            self.ts.browse_file()
            assert self.ts.selected_file_path == mock_file_path
            assert self.ts.file_path_input.text() == t.all.format_input_path(
                mock_file_path
            )

    def test_update_next_button_status(self):
        """
        Tests that the update_next_button_status method correctly updates the
        enabled status of the "Next" button based on the following conditions:
        1.  The user has entered a file path in the file path input or has entered a
            private key in the key text area.
        2.  If the user has checked the "Password protect the private key" checkbox,
            the user must have entered a password in the password line edit.
        """
        self.ts.file_path_input.setText("/home/username/path/to/private_key.pem")
        assert self.ts.next_button.isEnabled()

        self.ts.is_password_protected_cb.setChecked(True)
        assert not self.ts.next_button.isEnabled()

        self.ts.password_lineEdit.setText("password")
        assert self.ts.next_button.isEnabled()

        self.ts.is_password_protected_cb.setChecked(False)
        assert self.ts.next_button.isEnabled()

    def test_handle_click_next(self):
        """
        Tests that the handle_click_next method correctly calls the appropriate
        private method and calls process_private_key if the input is valid.
        """
        self.ts._handle_file_input = MagicMock(return_value=True)
        self.ts._handle_text_input = MagicMock(return_value=True)
        self.ts.process_private_key = MagicMock()

        self.ts.file_radio.setChecked(True)
        self.ts.is_password_protected_cb.setChecked(True)
        password = "my_password"
        self.ts.password_lineEdit.setText(password)

        self.ts.handle_click_next()
        self.ts._handle_file_input.assert_called_once_with(password)
        self.ts.process_private_key.assert_called_once()

        self.ts.file_radio.setChecked(False)
        self.ts.text_radio.setChecked(True)
        self.ts.is_password_protected_cb.setChecked(False)

        self.ts.handle_click_next()

        self.ts._handle_text_input.assert_called_once_with(None)
        self.ts.process_private_key.assert_called_with()

        assert self.ts.process_private_key.call_count == 2

        self.ts.file_radio.setChecked(True)
        self.ts.text_radio.setChecked(False)
        self.ts._handle_file_input.return_value = False

        self.ts.handle_click_next()
        assert self.ts.process_private_key.call_count == 2

    def test__handle_file_input(self):
        """
        Tests the _handle_file_input method to ensure that it correctly handles loading a
        private key from a file and sets the private_key attribute of the ChoosePrivateKeyScreen
        instance. The test also verifies that the method correctly handles exceptions and
        displays an error message if the private key cannot be loaded.

        The test first sets the selected_file_path attribute of the ChoosePrivateKeyScreen
        instance to a valid path and calls the _handle_file_input method with a password.
        It then verifies that the key_manager's load_private_key_from_file method is called
        with the correct arguments and that the private_key attribute of the
        ChoosePrivateKeyScreen instance is set to the mock private key.

        The test then sets the side effect of the key_manager's load_private_key_from_file
        method to raise an exception and verifies that the method correctly handles the
        exception and displays an error message.

        :return: None
        """

        self.ts.selected_file_path = "/valid/path/to/key.pem"
        password = "my_pass"
        mock_private_key = MagicMock()
        self.ts.key_manager = MagicMock()
        self.ts.key_manager.load_private_key_from_file.return_value = mock_private_key

        result = self.ts._handle_file_input(password)

        self.ts.key_manager.load_private_key_from_file.assert_called_once_with(
            self.ts.selected_file_path, password
        )

        assert self.ts.private_key == mock_private_key
        assert result is True

        except_message = "Error loading key"
        self.ts.key_manager.load_private_key_from_file.side_effect = Exception(
            except_message
        )

        with patch("PySide6.QtWidgets.QMessageBox.critical") as mock_critical:
            result = self.ts._handle_file_input(password=password)

            mock_critical.assert_called_once_with(
                self.ts,
                self.ts.tr("Unsupported File Detected"),
                self.ts.tr(except_message),
            )

            assert result is False

    def test__handle_text_input(self):
        """
        Tests the _handle_text_input method to ensure it processes and validates
        the entered private key correctly.

        This test verifies that when a valid private key is entered, the method
        serializes it and sets the private_key attribute. It also checks that
        if serialization fails, a critical error message is displayed and the
        private_key attribute is not set. Additionally, it tests that if the
        private key validation fails, a warning message is shown.

        Scenarios tested:
        1. A valid private key is correctly serialized and stored.
        2. A serialization exception is handled by displaying a critical error message.
        3. An invalid private key prompts a warning message.

        :return: None
        """

        mock_private_key = MagicMock()
        password = "my_pass"

        self.ts.validate_private_key = MagicMock(return_value=True)
        self.ts.key_manager = MagicMock()
        self.ts.key_manager.serialize_private_key.return_value = mock_private_key

        result = self.ts._handle_text_input(password)

        assert not self.ts.private_key is None
        assert result is True
        assert self.ts.private_key == mock_private_key

        self.ts.private_key = None
        error_message = "Error serializing key"
        self.ts.key_manager.serialize_private_key.side_effect = Exception(error_message)

        with patch("PySide6.QtWidgets.QMessageBox.critical") as mock_critical:

            result = self.ts._handle_text_input(password=password)

            mock_critical.assert_called_once_with(
                self.ts,
                self.ts.tr("Key Format Error"),
                self.ts.tr(error_message),
            )
            assert result is False
            assert self.ts.private_key is None

        self.ts.validate_private_key = MagicMock(return_value=False)
        with patch("PySide6.QtWidgets.QMessageBox.warning") as mock_warning:

            result = self.ts._handle_text_input(password=password)

            mock_warning.assert_called_once_with(
                self.ts,
                self.ts.tr("Private Key Format Error"),
                self.ts.tr("Please enter a valid private key to proceed"),
            )
            assert result is False
            assert self.ts.private_key is None

    def test_validate_private_key(self):
        """
        Tests the validate_private_key method to ensure that it correctly identifies
        valid and invalid private keys.

        The test verifies that the method correctly identifies valid private keys
        with "BEGIN PRIVATE KEY" and "END PRIVATE KEY" tags, and encrypted private
        keys with "BEGIN ENCRYPTED PRIVATE KEY" and "END ENCRYPTED PRIVATE KEY" tags.
        The test also verifies that the method correctly identifies invalid private
        keys that do not contain the required tags.

        :return: None
        """

        private_key = "BEGIN PRIVATE KEY\nEND PRIVATE KEY"
        protected_key = "BEGIN ENCRYPTED PRIVATE KEY\nEND ENCRYPTED PRIVATE KEY"
        wrong_key = "wrong_key"

        assert self.ts.validate_private_key(private_key)
        assert self.ts.validate_private_key(protected_key)
        assert not self.ts.validate_private_key(wrong_key)

        assert not self.ts.validate_private_key("BEGIN PRIVATE KEY")
        assert not self.ts.validate_private_key("END PRIVATE KEY")
        assert not self.ts.validate_private_key("BEGIN ENCRYPTED PRIVATE KEY")
        assert not self.ts.validate_private_key("END ENCRYPTED PRIVATE KEY")

    def test_process_private_key(self):
        """
        Tests the process_private_key method to ensure that it emits the private key
        acceptance signal, transitions to the SaveFileDecryptScreen, and properly
        destroys the current widget.

        The test verifies that:
        - The center_widget method is called with a SaveFileDecryptScreen instance.
        - The new screen is displayed by checking the show method is called.
        - The private_key_accepted signal contains the expected private key.
        - The current widget is destroyed after transitioning.
        """

        self.ts.private_key = MagicMock()

        with patch("tools.toolkit.Tools.qt.center_widget") as mock_center_widget, patch(
            "PySide6.QtWidgets.QWidget.destroy"
        ) as mock_destroy:

            mock_window = MagicMock()
            mock_window.show = MagicMock()
            mock_center_widget.return_value = mock_window

            self.ts.process_private_key()

            called_with = mock_center_widget.call_args[0][0]
            assert isinstance(called_with, SaveFileDecryptScreen)

            mock_window.show.assert_called_once()
            assert (
                signal_manager.saved_data["private_key_accepted"] == self.ts.private_key
            )

            mock_destroy.assert_called_once()

    def test_handle_password_input_accessability(self):
        """
        Tests the handle_password_input_accessability method to ensure that it correctly
        updates the enabled status of the password input field based on the given state.

        The test verifies that the method sets the enabled status of the password input
        field to True when the state is True, and sets it to False when the state is False.

        :return: None
        """

        self.ts.handle_password_input_accessability(True)

        assert self.ts.password_lineEdit.isEnabled()

        self.ts.handle_password_input_accessability(False)

        assert not self.ts.password_lineEdit.isEnabled()

    def test_close_event(self):
        """
        Tests that the closeEvent method of ChoosePrivateKeyScreen is implemented
        correctly to hide the screen and show the main window.

        This test verifies that when the ChoosePrivateKeyScreen is closed, the main
        window becomes visible, ensuring that the user can return to the main
        application window after closing the ChoosePrivateKeyScreen.
        """

        main_window = signal_manager.saved_data["save_main_window"]
        main_window.show = MagicMock()

        self.ts.close()

        main_window.show.assert_called_once()

        assert not self.ts.isVisible()
