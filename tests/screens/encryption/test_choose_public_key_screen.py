from screens.encryption.choose_public_key_screen import ChoosePublicKeyScreen
from unittest.mock import MagicMock, patch
from PySide6 import QtWidgets as qtw
from backend import signal_manager
from functools import partial
import pytest


class TestChoosePublicKeyScreen:
    @pytest.fixture(scope="function", autouse=True)
    def autorun(self, qtbot: qtw.QGridLayout):
        """
        Fixture to set up and tear down the ChoosePublicKeyScreen test environment.

        This fixture is automatically used for each test function in the
        TestChoosePublicKeyScreen class. It initializes the ChoosePublicKeyScreen,
        adds it to the qtbot for interaction, and mocks the main window required
        for the screen to function properly.

        After the test, it ensures the screen is properly closed and cleaned up.

        :param self: The test class instance.
        :param qtbot: Pytest-qt's qtbot fixture for interacting with Qt widgets.
        """
        signal_manager.saved_data["save_main_window"] = MagicMock(spec=qtw.QWidget)
        with patch(
            "screens.encryption.choose_public_key_screen.ChoosePublicKeyScreen.disable_password_protection"
        ) as self.mock_disable_password_protection:
            self.ts = ChoosePublicKeyScreen()
        qtbot.addWidget(self.ts)
        yield

    def test_update_ui(self):
        """
        Tests the initial state of the ChoosePublicKeyScreen UI components.

        This test verifies that the ChoosePublicKeyScreen is visible,
        has the correct window title, and the UI elements such as the
        browse button and radio buttons are in their expected enabled or
        disabled states. Additionally, it checks that the text and
        placeholder text of key input fields are set correctly. Finally,
        it verifies that the password protection is disabled by default.
        """
        self.ts.show()
        assert self.ts.windowTitle() == "Encryption | Choose a public key"
        assert self.ts.browse_button.isEnabled()
        assert not self.ts.key_text_area.isEnabled()
        assert self.ts.file_radio.text() == "Load public key from file"
        assert self.ts.text_radio.text() == "Enter public key manually"
        assert (
            self.ts.file_path_input.placeholderText()
            == "Browse for a public key file (the path will be generated automatically)..."
        )
        assert (
            self.ts.key_text_area.placeholderText() == "Enter your public key here..."
        )

        self.mock_disable_password_protection.assert_called_once()

    def test_disable_password_protection(self):
        """
        Tests that the disable_password_protection method correctly disables
        the password protection UI elements by removing the password group
        layout from the ChoosePublicKeyScreen instance.

        The test verifies that the method deletes all children widgets of the
        password group layout and then deletes the layout itself, as password
        protection is not applicable for public keys.

        :return: None
        """
        original_disable_password_protection = partial(
            ChoosePublicKeyScreen.disable_password_protection, self.ts
        )

        original_disable_password_protection()
        assert self.ts.password_group_layout is None

    def test_toggle_input_mode(self):
        """
        Tests that the toggle_input_mode method correctly enables/disables the browse button and
        the public key text area based on the status of the radio button. If the radio button is
        toggled on (i.e., the user wants to load the public key from a file), the public key text
        area is cleared, and if the radio button is toggled off (i.e., the user wants to enter the
        public key manually), the file path input is cleared.
        """

        self.ts.toggle_input_mode(True)

        assert self.ts.browse_button.isEnabled()
        assert not self.ts.key_text_area.isEnabled()

        self.ts.toggle_input_mode(False)

        assert not self.ts.browse_button.isEnabled()
        assert self.ts.key_text_area.isEnabled()

    def test_browse_file(self):
        """
        Tests the browse_file method to ensure it correctly sets the selected_file_path
        attribute of the ChoosePublicKeyScreen instance and sets the text of the file_path_input
        to the selected file path after the user selects a file using the QFileDialog.
        """

        with patch.object(
            qtw.QFileDialog, "getOpenFileName"
        ) as mock_getOpenFileName, patch(
            "tools.toolkit.Tools.all.format_input_path"
        ) as mock_format_input_path:
            selected_public_key = "selected_public_key.pem"
            formatted_path = "select...key.pem"
            mock_getOpenFileName.return_value = (selected_public_key, "_")
            mock_format_input_path.return_value = formatted_path
            self.ts.browse_file()

            assert self.ts.selected_file_path == selected_public_key
            mock_format_input_path.assert_called_once_with(selected_public_key)
            assert self.ts.file_path_input.text() == formatted_path

    def test_update_next_button_status(self):
        """
        Tests the update_next_button_status method to ensure that it correctly
        updates the enabled status of the "Next" button based on the text
        contents of the file path input and the key text area. If either of
        these fields contains some text, the "Next" button should be enabled,
        and if either of them are empty, the "Next" button should be disabled.
        """
        self.ts.file_path_input.setText("Some text")
        assert self.ts.next_button.isEnabled()
        self.ts.file_path_input.clear()
        assert self.ts.next_button.isEnabled() is False

        self.ts.key_text_area.setText("Some key area text")
        assert self.ts.next_button.isEnabled()
        self.ts.key_text_area.clear()
        assert self.ts.next_button.isEnabled() is False

    def test_handle_click_next(self):
        """
        Tests that the handle_click_next method is correctly implemented
        to handle the selected input mode (file or text area) and calls the
        appropriate method to validate the input. If the input is valid, it
        calls process_public_key to proceed with the encryption process.
        """
        self.ts.show()
        with patch(
            "screens.encryption.choose_public_key_screen.ChoosePublicKeyScreen._handle_file_input"
        ) as mock__handle_file_input, patch(
            "screens.encryption.choose_public_key_screen.ChoosePublicKeyScreen._handle_text_input"
        ) as mock__handle_text_input, patch(
            "screens.encryption.choose_public_key_screen.ChoosePublicKeyScreen.process_public_key"
        ) as mock_process_public_key:

            mock__handle_file_input.return_value = True
            mock__handle_text_input.return_value = True

            self.ts.file_radio.setCheckable(True)
            self.ts.handle_click_next()
            mock__handle_file_input.assert_called_once()
            mock_process_public_key.assert_called_once()

            self.ts.file_radio.setCheckable(False)
            self.ts.handle_click_next()
            mock__handle_text_input.assert_called_once()
            assert mock_process_public_key.call_count == 2

    def test__handle_file_input(self):
        """
        Tests the _handle_file_input method to ensure it correctly loads a public key
        from a file and handles exceptions appropriately.

        The test checks that:
        1. When a valid file path is provided, load_public_key_from_file is called with the correct argument,
        and the public_key attribute is set to the returned key.
        2. The method returns True when the public key is successfully loaded.
        3. If an exception occurs during key loading, a critical error message is displayed,
        and the method returns False.

        :return: None
        """

        self.ts.selected_file_path = "/valid/path/to/key.pem"
        public_key = "public_key.pem"
        with patch.object(
            self.ts.key_manager, "load_public_key_from_file"
        ) as mock_load_public_key_from_file, patch(
            "PySide6.QtWidgets.QMessageBox.critical"
        ) as mock_q_message_box:
            mock_load_public_key_from_file.return_value = public_key

            return_value = self.ts._handle_file_input()
            mock_load_public_key_from_file.assert_called_once_with(
                self.ts.selected_file_path
            )
            assert self.ts.public_key == public_key
            assert return_value is True

            error_message = "Something wrong with key :P"
            mock_load_public_key_from_file.side_effect = Exception(error_message)
            return_value = self.ts._handle_file_input()

            mock_q_message_box.assert_called_once_with(
                self.ts,
                self.ts.tr("Unsupported File Detected"),
                self.ts.tr(error_message),
            )
            assert return_value is False

    def test__handle_text_input(self):
        """
        Tests the _handle_text_input method to ensure it correctly handles public key input in the text area.
        The test verifies that the method:
        1. Calls the serialize_public_key method with the input public key and sets the public_key attribute
        to the returned key.
        2. Calls the validate_public_key method with the input public key and returns True if the key is valid.
        3. Displays a critical error message if the serialization fails.
        4. Displays a warning message if the public key is invalid.

        :return: None
        """
        with patch.object(
            self.ts.key_manager, "serialize_public_key"
        ) as mock_serialize_public_key, patch.object(
            self.ts, "validate_public_key"
        ) as mock_validate_public_key, patch(
            "PySide6.QtWidgets.QMessageBox.critical"
        ) as mock_q_message_critical, patch(
            "PySide6.QtWidgets.QMessageBox.warning"
        ) as mock_q_message_warning:
            input_public_key = "input_public_key.pem"
            ser_public_key = "ser_public_key.pem"
            self.ts.key_text_area.setText(input_public_key)
            mock_validate_public_key.return_value = True
            mock_serialize_public_key.return_value = ser_public_key

            result_value = self.ts._handle_text_input()
            mock_serialize_public_key.assert_called_once_with(input_public_key)
            mock_validate_public_key.assert_called_once_with(input_public_key)
            assert self.ts.public_key == ser_public_key
            assert result_value is True

            exception_title = "Key Format Error"
            exception_message = "Serialization failed, oops :P"
            mock_serialize_public_key.side_effect = Exception(exception_message)
            result_value = self.ts._handle_text_input()
            assert mock_validate_public_key.call_count == 2
            mock_q_message_critical.assert_called_once_with(
                self.ts, self.ts.tr(exception_title), self.ts.tr(exception_message)
            )
            assert result_value is False

            exception_message = "Please enter a valid public key to proceed"
            mock_validate_public_key.return_value = False
            result_value = self.ts._handle_text_input()
            assert mock_validate_public_key.call_count == 3
            mock_q_message_warning.assert_called_once_with(
                self.ts, self.ts.tr(exception_title), self.ts.tr(exception_message)
            )
            assert result_value is False

    def test_validate_public_key(self):
        """
        Tests the validate_public_key method to ensure that it correctly identifies
        valid and invalid public keys.

        The test verifies that the method correctly identifies valid public keys
        with "BEGIN PUBLIC KEY" and "END PUBLIC KEY" tags, and invalid public keys
        that do not contain the required tags.

        :return: None
        """
        public_key = "BEGIN PUBLIC KEY some key END PUBLIC KEY"
        result_value = self.ts.validate_public_key(public_key)
        assert result_value is True

        public_key = "BEGIN PUBLIC KEY some key WRONG END"
        result_value = self.ts.validate_public_key(public_key)
        assert result_value is False

        public_key = "WRONG START some key END PUBLIC KEY"
        result_value = self.ts.validate_public_key(public_key)
        assert result_value is False

    def test_process_public_key(self):
        """
        Tests the process_public_key method to ensure that it emits the public key
        acceptance signal, transitions to the SaveFileEncryptScreen, and properly
        destroys the current widget.

        The test verifies that:
        - The center_widget method is called with a SaveFileEncryptScreen instance.
        - The new screen is displayed by checking the show method is called.
        - The destroy method is called on the current widget.
        - The current widget is no longer visible after transitioning.
        """
        self.ts.public_key = "public_key"

        with patch("tools.toolkit.Tools.qt.center_widget") as mock_center_widget, patch(
            "screens.encryption.choose_public_key_screen.SaveFileEncryptScreen",
            autospec=True,
        ) as MockSaveFileEncryptScreen, patch.object(
            self.ts, "destroy"
        ) as mock_destroy:
            original_destroy = partial(ChoosePublicKeyScreen.destroy, self.ts)
            self.ts.show()
            save_file_encrypt_instance = MagicMock()
            MockSaveFileEncryptScreen.return_value = save_file_encrypt_instance
            mock_center_widget.return_value = save_file_encrypt_instance
            self.ts.process_public_key()

            mock_center_widget.assert_called_once_with(save_file_encrypt_instance)
            assert self.ts.save_file_encrypt_screen is save_file_encrypt_instance
            save_file_encrypt_instance.show.assert_called_once()
            mock_destroy.assert_called_once()
            original_destroy()
            assert not self.ts.isVisible()

    def test_closeEvent(self):
        """
        Tests the closeEvent method is correctly implemented to hide
        the ChoosePublicKeyScreen and show the main window.

        This test verifies that when the ChoosePublicKeyScreen is closed,
        the main window is made visible again, ensuring the user can return
        to the main application window.
        """

        main_window = signal_manager.saved_data.get("save_main_window")
        self.ts.close()

        assert not self.ts.isVisible()

        main_window.show.assert_called_once()
