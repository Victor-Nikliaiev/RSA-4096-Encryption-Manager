from screens.encryption.choose_public_key_screen import ChoosePublicKeyScreen
from unittest.mock import MagicMock, patch
from PySide6 import QtWidgets as qtw
from backend import signal_manager
from functools import partial
import pytest


class TestChoosePublicKeyScreen:
    @pytest.fixture(scope="function", autouse=True)
    def autorun(self, qtbot: qtw.QGridLayout):
        signal_manager.saved_data["save_main_window"] = MagicMock(spec=qtw.QWidget)
        with patch(
            "screens.encryption.choose_public_key_screen.ChoosePublicKeyScreen.disable_password_protection"
        ) as self.mock_disable_password_protection:
            self.ts = ChoosePublicKeyScreen()
        qtbot.addWidget(self.ts)
        yield

    def test_update_ui(self):
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
        original_disable_password_protection = partial(
            ChoosePublicKeyScreen.disable_password_protection, self.ts
        )

        original_disable_password_protection()
        assert self.ts.password_group_layout is None

    def test_toggle_input_mode(self):
        self.ts.toggle_input_mode(True)

        assert self.ts.browse_button.isEnabled()
        assert not self.ts.key_text_area.isEnabled()

        self.ts.toggle_input_mode(False)

        assert not self.ts.browse_button.isEnabled()
        assert self.ts.key_text_area.isEnabled()

    def test_browse_file(self):
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
        self.ts.file_path_input.setText("Some text")
        assert self.ts.next_button.isEnabled()
        self.ts.file_path_input.clear()
        assert self.ts.next_button.isEnabled() is False

        self.ts.key_text_area.setText("Some key area text")
        assert self.ts.next_button.isEnabled()
        self.ts.key_text_area.clear()
        assert self.ts.next_button.isEnabled() is False

    def test_handle_click_next(self):
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
            exception_message = f"Serialization failed, oops :P"
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
            mock_destroy.assert_called_once()
            original_destroy()
            assert not self.ts.isVisible()

    def test_closeEvent(self):
        main_window = signal_manager.saved_data.get("save_main_window")
        self.ts.close()

        main_window.show.assert_called_once()
