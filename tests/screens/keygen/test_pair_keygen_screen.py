from screens.keygen.pair_keygen_screen import PairKeygenScreen
from backend.rsa_key_manager import RsaKeyManager
from unittest.mock import MagicMock, patch
from PySide6 import QtWidgets as qtw
from tools.toolkit import Tools as t
from backend import signal_manager
import pytest


class TestPairKeygenScreen:
    @pytest.fixture(scope="function", autouse=True)
    def autorun(self, qtbot: qtw.QGridLayout):
        """
        Fixture to set up and tear down the PairKeygenScreen test environment.

        This fixture is automatically used for each test function in the
        TestPairKeygenScreen class. It initializes the PairKeygenScreen,
        adds it to the qtbot for interaction, and mocks the main window required
        for the screen to function properly.

        After the test, it ensures the screen is properly closed and cleaned up.
        """

        signal_manager.saved_data["save_main_window"] = MagicMock(spec=qtw.QWidget)
        self.ts = PairKeygenScreen()
        qtbot.addWidget(self.ts)
        yield

    def test_update_ui(self):
        """
        Tests that the user interface of the PairKeygenScreen is updated correctly
        on initialization. This includes the window title, the text of the top
        label and location info button, and the placeholder text of the key
        path line edit.
        """

        assert (
            self.ts.windowTitle()
            == "Key Generation | Select location to generate your keys"
        )
        assert (
            self.ts.top_lb.text()
            == "Select location to generate your private and public keys:"
        )
        assert (
            self.ts.location_info_btn.text() == "  Select location to save your keys:"
        )
        assert (
            self.ts.key_path_le.placeholderText()
            == 'Click "Select" to choose location to save your keys'
        )

    def test_browse_file(self):
        """
        Tests the browse_file method to ensure it correctly sets the selected_file_path
        attribute and sets the text of the key_path_le to the selected file path after
        the user selects a file using the QFileDialog. The test also verifies that the
        generate button is initially disabled, and is enabled after a file is selected.
        """

        with patch(
            "PySide6.QtWidgets.QFileDialog.getSaveFileName", autospec=True
        ), patch("tools.toolkit.Tools.all.format_input_path", autospec=True):
            selected_file_path = "my_keys.zip"
            qtw.QFileDialog.getSaveFileName.return_value = (selected_file_path, "_")
            formatted_path = "my_k...zip"
            t.all.format_input_path.return_value = formatted_path
            self.ts.key_match_lb.setText("Some text's going here")

            assert not self.ts.generate_btn.isEnabled()

            self.ts.browse_file()
            qtw.QFileDialog.getSaveFileName.assert_called_once_with(
                self.ts,
                self.ts.tr("Save Your Keys"),
                self.ts.tr("my_keys.zip"),
                self.ts.tr("ZIP Files (*.zip);;All Files (*)"),
            )

            assert self.ts.key_path_le.text() == formatted_path
            assert signal_manager.saved_data["saved_file_path"] == selected_file_path
            assert self.ts.generate_btn.isEnabled()

    def test_password_cb_click_handler(self):
        """
        Tests the password_cb_click_handler method to ensure that the UI elements respond
        correctly to changes in the checkbox state. It verifies that when the checkbox is
        checked, the key match label text is set, and the generate button is disabled. When
        unchecked, it ensures the generate button remains disabled unless a file path is
        selected, in which case it becomes enabled.
        """

        self.ts.password_cb_click_handler(True)

        assert self.ts.key_match_lb.text() == self.ts.key_match_lb_text
        assert not self.ts.generate_btn.isEnabled()

        self.ts.password_cb_click_handler(False)
        assert not self.ts.generate_btn.isEnabled()

        self.ts.selected_file_path = "some file path"
        self.ts.password_cb_click_handler(False)
        assert self.ts.generate_btn.isEnabled()

    def test_set_password_fields(self):
        """
        Tests the set_password_fields method to ensure that it correctly sets
        the enabled status of the password and repeat password input fields
        based on the given state. When the state is True, it verifies that the
        fields are enabled and when the state is False, it verifies that the
        fields are disabled and cleared.
        """

        self.ts.set_password_fields(True)

        assert self.ts.password_le.isEnabled()
        assert self.ts.password_repeat_le.isEnabled()

        self.ts.password_le.setText("some password :P")
        self.ts.password_repeat_le.setText("some password :P")

        self.ts.set_password_fields(False)
        assert self.ts.password_le.text() == ""
        assert self.ts.password_repeat_le.text() == ""
        assert not self.ts.password_le.isEnabled()
        assert not self.ts.password_repeat_le.isEnabled()

    def test_text_changed_handler(self):
        """
        Tests the text_changed_handler method to ensure that it correctly updates
        the enabled status of the "Generate" button based on the password match
        and the selected file path. The test verifies that the button is enabled
        when the passwords match and a file path is selected, and disabled when
        the passwords do not match or a file path is not selected.
        """

        assert not self.ts.generate_btn.isEnabled()
        self.ts.selected_file_path = "file_path"
        self.ts.password_le.setText("password")
        self.ts.password_repeat_le.setText("password")
        self.ts.text_changed_handler()
        assert self.ts.generate_btn.isEnabled()

        self.ts.password_repeat_le.setText("not matching password")
        self.ts.text_changed_handler()
        assert self.ts.key_match_lb.text() == self.ts.key_match_lb_text
        assert not self.ts.generate_btn.isEnabled()

    def test_process_keygen(self):
        """
        Tests the process_keygen method to ensure that it correctly generates a pair of RSA keys,
        encrypts them using the provided password if the password protection checkbox is checked,
        and exports the keys as a ZIP file to the selected file path. A success message is displayed
        upon successful generation and export of the keys, and the current window is closed.
        """

        with patch(
            "screens.keygen.pair_keygen_screen.RsaKeyManager", autospec=True
        ) as MockRsaKeyManager, patch(
            "PySide6.QtWidgets.QMessageBox.information"
        ) as mock_q_message_info:
            self.ts.show()
            key_manager = MagicMock(spec=RsaKeyManager)
            MockRsaKeyManager.return_value = key_manager

            self.ts.selected_file_path = "my_keys.zip"
            self.ts.password_cb.setChecked(True)
            password = "my_password"
            self.ts.password_le.setText(password)

            private_key = "private_key"
            key_manager.generate_private_key.return_value = private_key
            public_key = "public_key"
            key_manager.generate_public_key.return_value = public_key
            private_key_pem = "private_key_pem"
            key_manager.encrypt_private_key.return_value = private_key_pem
            public_key_pem = "public_key_pem"
            key_manager.encrypt_public_key.return_value = public_key_pem

            self.ts.process_keygen()

            key_manager.generate_private_key.assert_called_once()
            key_manager.generate_public_key.assert_called_once_with(private_key)
            key_manager.encrypt_private_key.assert_called_once_with(
                private_key, password
            )
            key_manager.encrypt_public_key.assert_called_once_with(public_key)
            key_manager.export_keys_to_zip.assert_called_once_with(
                private_key_pem, public_key_pem, self.ts.selected_file_path
            )
            mock_q_message_info.assert_called_once_with(
                self.ts,
                self.ts.tr("Success"),
                self.ts.tr("Your keys were generated successfully."),
            )
            assert not self.ts.isVisible()

    def test_closeEvent(self):
        """
        Tests that the closeEvent method correctly handles the window close event by
        centering and showing the main window, and then verifying that the PairKeygenScreen
        is no longer visible.
        """

        with patch("tools.toolkit.Tools.qt.center_widget") as mock_center_widget:
            main_window = signal_manager.saved_data["save_main_window"]
            mock_center_widget.return_value = main_window

            self.ts.show()
            self.ts.close()

            mock_center_widget.assert_called_once_with(main_window)
            main_window.show.assert_called_once()
            assert not self.ts.isVisible()
