from screens.keygen.private_keygen_screen import PrivateKeygenScreen
from backend.rsa_key_manager import RsaKeyManager
from unittest.mock import MagicMock, patch
from PySide6 import QtWidgets as qtw
from backend import signal_manager
import pytest


class TestPrivateKeygenScreen:
    @pytest.fixture(scope="function", autouse=True)
    def autorun(self, qtbot: qtw.QGridLayout):
        """
        Fixture to set up and tear down the PrivateKeygenScreen test environment.

        This fixture is automatically used for each test function in the
        TestPrivateKeygenScreen class. It initializes the PrivateKeygenScreen,
        adds it to the qtbot for interaction, and mocks the main window required
        for the screen to function properly.

        After the test, it ensures the screen is properly closed and cleaned up.

        :param self: The test class instance.
        :param qtbot: Pytest-qt's qtbot fixture for interacting with Qt widgets.
        """

        signal_manager.saved_data["save_main_window"] = MagicMock(spec=qtw.QWidget)
        self.ts = PrivateKeygenScreen()
        qtbot.addWidget(self.ts)
        yield

    def test_browse_file(self):
        """
        Tests the browse_file method to ensure it correctly sets the selected_file_path
        attribute and sets the text of the key_path_le to the selected file path after
        the user selects a file using the QFileDialog. The test also verifies that the
        generate button is initially disabled, and is enabled after a file is selected.
        """

        with patch(
            "PySide6.QtWidgets.QFileDialog.getSaveFileName"
        ) as mocked_getSaveFileName, patch(
            "tools.toolkit.Tools.all.format_input_path"
        ) as mocked_format_input_path:

            saved_file_path = "save_file_path"
            formatted_saved_file_path = "sav...file_path"
            mocked_getSaveFileName.return_value = (saved_file_path, "_")

            mocked_format_input_path.return_value = formatted_saved_file_path

            self.ts.browse_file()

            mocked_getSaveFileName.assert_called_once_with(
                self.ts,
                self.ts.tr("Save Private File"),
                self.ts.tr("private_key.pem"),
                self.ts.tr("PEM Files (*.pem);;All Files (*)"),
            )

            assert self.ts.selected_file_path == saved_file_path
            assert self.ts.key_path_le.text() == formatted_saved_file_path
            assert (
                signal_manager.saved_data.get("saved_file_path")
                == self.ts.selected_file_path
            )
            assert self.ts.generate_btn.isEnabled()

    def test_password_cb_click_handler(self):
        """
        Tests the password_cb_click_handler method to ensure it correctly sets the
        enabled status of the password and password repeat input fields based on
        the checkbox state. If the checkbox is checked, it sets the text of the key
        match label to the key match label text and sets the enabled status of the
        "Generate" button to False. If the checkbox is unchecked and a file path
        has been selected, it sets the enabled status of the "Generate" button to
        True.
        """

        with patch.object(self.ts, "set_password_fields"):
            self.ts.selected_file_path = "selected_file_path"
            self.ts.password_cb_click_handler(False)
            assert self.ts.generate_btn.isEnabled()
            self.ts.set_password_fields.assert_called_once_with(False)

            self.ts.password_cb_click_handler(True)
            assert self.ts.key_match_lb.text() == self.ts.key_match_lb_text
            assert not self.ts.generate_btn.isEnabled()

    def test_set_password_fields(self):
        """
        Tests the set_password_fields method to ensure that it correctly adjusts
        the enabled status of the password and repeat password input fields.

        Initially verifies that the fields are disabled. When the state is set
        to True, it checks that the fields are enabled. It also ensures that when
        the state is set to False, the fields are disabled and cleared of any text.
        """

        assert not self.ts.password_le.isEnabled()
        assert not self.ts.password_repeat_le.isEnabled()

        self.ts.set_password_fields(True)
        assert self.ts.password_le.isEnabled()
        assert self.ts.password_repeat_le.isEnabled()

        self.ts.password_le.setText("password")
        self.ts.password_repeat_le.setText("password")
        self.ts.set_password_fields(False)
        assert self.ts.password_le.text() == ""
        assert self.ts.password_repeat_le.text() == ""

    def test_text_changed_handler(self):
        """
        Tests the text_changed_handler method to ensure that it correctly updates
        the enabled status of the "Generate" button based on the password match
        and the selected file path. The test verifies that the button is enabled
        when the passwords match and a file path is selected, and disabled when
        the passwords do not match or a file path is not selected.
        """

        password = "pass_word"
        self.ts.selected_file_path = "file_path"
        self.ts.password_le.setText(password)
        self.ts.password_repeat_le.setText(password)

        self.ts.text_changed_handler()
        assert self.ts.generate_btn.isEnabled()

        self.ts.password_le.setText(password)
        self.ts.password_repeat_le.setText("not matching one")
        self.ts.text_changed_handler()
        assert self.ts.key_match_lb.text()
        assert not self.ts.generate_btn.isEnabled()

    def test_process_keygen(self):
        """
        Tests the process_keygen method to ensure that it correctly generates a
        private key, saves it to the selected file path, and displays a success
        message upon successful generation and export of the key. The test also
        verifies that the method correctly handles exceptions and displays an
        error message if the private key cannot be saved to the selected file
        path.

        :return: None
        """

        with patch(
            "screens.keygen.private_keygen_screen.RsaKeyManager", autospec=True
        ) as MockRsaKeyManager, patch(
            "PySide6.QtWidgets.QMessageBox", autospec=True
        ) as MockQMessageBox:
            self.ts.show()
            self.ts.selected_file_path = "selected_file_path"
            key_manager = MagicMock(spec=RsaKeyManager)
            MockRsaKeyManager.return_value = key_manager
            private_key = "private_key"
            key_manager.generate_private_key.return_value = private_key

            self.ts.process_keygen()

            key_manager.generate_private_key.assert_called_once()
            key_manager.save_private_key_to_file.assert_called_once_with(
                self.ts.selected_file_path, None, private_key
            )
            MockQMessageBox.information.assert_called_once_with(
                self.ts,
                self.ts.tr("Success"),
                self.ts.tr("Private key generated successfully."),
            )
            assert not self.ts.isVisible()

            except_message = "Error saving private key to file"
            key_manager.save_private_key_to_file.side_effect = Exception(except_message)
            self.ts.process_keygen()
            MockQMessageBox.critical.assert_called_once_with(
                self.ts, self.ts.tr("Error"), self.ts.tr(f"{except_message}")
            )

    def test_close_event(self):
        """
        Tests that the closeEvent method of PrivateKeygenScreen is implemented
        correctly to show the main window when the PrivateKeygenScreen is closed.

        This test verifies that when the PrivateKeygenScreen is closed, the main
        window becomes visible, ensuring that the user can return to the main
        application window after closing the PrivateKeygenScreen.
        """

        with patch("tools.toolkit.Tools.qt.center_widget") as mock_center_widget:

            main_window = signal_manager.saved_data.get("save_main_window")
            mock_center_widget.return_value = main_window
            self.ts.close()

            mock_center_widget.assert_called_once_with(main_window)
            main_window.show.assert_called_once()
