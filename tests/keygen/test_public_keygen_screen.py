from screens.keygen.public_keygen_screen import PublicKeygenScreen
from backend.rsa_key_manager import RsaKeyManager
from unittest.mock import MagicMock, patch
from PySide6 import QtWidgets as qtw
from backend import signal_manager
import pytest


class TestPublicKeygenScreen:
    @pytest.fixture(scope="function", autouse=True)
    def autorun(self, qtbot: qtw.QGridLayout):
        """
        Fixture to set up and tear down the PublicKeygenScreen test environment.

        This fixture is automatically used for each test function in the
        TestPublicKeygenScreen class. It initializes the PublicKeygenScreen,
        adds it to the qtbot for interaction, and mocks the main window and
        dialog required for the screen to function properly.

        After the test, it ensures the screen is properly closed and cleaned up.

        :param self: The test class instance.
        :param qtbot: Pytest-qt's qtbot fixture for interacting with Qt widgets.
        """

        with patch(
            "PySide6.QtWidgets.QFileDialog", autospec=True
        ) as self.MockedQFileDialog, patch(
            "tools.toolkit.Tools.all.format_input_path"
        ) as self.mock_format_input_path:
            self.main_window = MagicMock(spec=qtw.QWidget)
            signal_manager.saved_data["save_main_window"] = self.main_window
            self.ts = PublicKeygenScreen()
            qtbot.addWidget(self.ts)
            yield

    def test_private_key_sel_btn_handler(self):
        """
        Tests the private_key_sel_btn_handler method to ensure that it correctly
        sets the private_key_full_path attribute and the text of the
        private_key_path_le to the selected file path after the user selects a
        file using the QFileDialog.
        """

        private_key_full_path = "private_key_full_path"
        private_key_formatted_path = "private_key_..._path"

        self.MockedQFileDialog.getOpenFileName.return_value = (
            private_key_full_path,
            "_",
        )
        self.mock_format_input_path.return_value = private_key_formatted_path
        self.ts.private_key_sel_btn_handler()

        self.MockedQFileDialog.getOpenFileName.assert_called_once_with(
            self.ts,
            self.ts.tr("Select Private Key File"),
            "",
            self.ts.tr("PEM Files (*.pem);;All Files (*)"),
        )
        assert self.ts.private_key_full_path == private_key_full_path
        assert self.ts.private_key_path_le.text() == private_key_formatted_path

    def test_password_cb_handler(self):
        """
        Tests the password_cb_handler method to ensure that it correctly
        enables the password input line edit when the password checkbox is
        checked and disables it when the checkbox is unchecked. It also
        verifies that the password input line edit is cleared when the
        checkbox is unchecked.
        """

        self.ts.password_cb_handler(True)

        assert self.ts.password_le.isEnabled()

        self.ts.password_le.setText("some password")
        self.ts.password_cb_handler(False)

        assert self.ts.password_le.text() == ""

    def test_pub_key_select_btn_handler(self):
        """
        Tests the pub_key_select_btn_handler method to ensure that it correctly
        sets the public_key_save_path attribute and the text of the
        pub_key_path_le to the selected file path after the user selects a
        file using the QFileDialog.
        """

        public_key_save_path = "public_key_save_path"
        public_key_formatted_save_path = "public_key...path"
        self.MockedQFileDialog.getSaveFileName.return_value = (
            public_key_save_path,
            "_",
        )
        self.mock_format_input_path.return_value = public_key_formatted_save_path
        self.ts.pub_key_select_btn_handler()

        self.MockedQFileDialog.getSaveFileName.assert_called_once_with(
            self.ts,
            self.ts.tr("Save Your Public Key"),
            self.ts.tr("public_key.pem"),
            self.ts.tr("PEM Files (*.pem);;All Files (*)"),
        )

        assert self.ts.public_key_save_path == public_key_save_path
        assert self.ts.pub_key_path_le.text() == public_key_formatted_save_path

    def test_generate_button_status_checker(self):
        """
        Tests the generate_button_status_checker method to ensure that it correctly
        updates the enabled status of the "Generate" button based on the input fields'
        conditions. The test verifies that the button is enabled when both private
        and public key paths are provided, and disabled if the "Password protect
        the private key" checkbox is checked without entering a password.
        """

        self.ts.private_key_path_le.setText("private_key_path")
        self.ts.pub_key_path_le.setText("pub_key_path")

        self.ts.generate_button_status_checker()
        assert self.ts.generate_btn.isEnabled()

        self.ts.password_cb.setChecked(True)
        self.ts.generate_button_status_checker()
        assert not self.ts.generate_btn.isEnabled()

    def test_process_keygen(self):
        """
        Tests the process_keygen method to ensure that it correctly generates and saves a
        public key based on the provided private key, and displays a success message
        upon successful generation and saving of the public key. The test also verifies
        that the method correctly handles exceptions and displays an error message if
        the public key cannot be generated.
        """

        with patch(
            "screens.keygen.public_keygen_screen.RsaKeyManager"
        ) as MockedRsaKeyManager, patch(
            "PySide6.QtWidgets.QMessageBox", autospec=True
        ) as MockQMessageBox:
            self.ts.show()
            self.ts.private_key_full_path = "private_key_full_path"
            self.ts.public_key_save_path = "public_key_save_path"

            key_manager = MagicMock(RsaKeyManager)
            MockedRsaKeyManager.return_value = key_manager
            private_key = "private_key"
            key_manager.load_private_key_from_file.return_value = private_key
            public_key = "public_key"
            key_manager.generate_public_key.return_value = public_key

            self.ts.process_keygen()

            key_manager.load_private_key_from_file.assert_called_once_with(
                self.ts.private_key_full_path, self.ts.password
            )
            key_manager.generate_public_key.assert_called_once_with(private_key)
            key_manager.save_public_key_to_file.assert_called_once_with(
                public_key, self.ts.public_key_save_path
            )
            MockQMessageBox.information.assert_called_once_with(
                self.ts,
                self.ts.tr("Success"),
                self.ts.tr("Your public key was successfully generated and saved."),
            )
            assert not self.ts.isVisible()

            exception_message = "Error during generating public key"
            key_manager.generate_public_key.side_effect = Exception(exception_message)
            self.ts.process_keygen()
            MockQMessageBox.critical.assert_called_once_with(
                self.ts, self.ts.tr("Error"), self.ts.tr(f"{exception_message}")
            )

    def test_closeEvent(self):
        """
        Tests that the closeEvent method of the PublicKeygenScreen is correctly implemented
        to hide the screen and show the main window.

        This test verifies that when the PublicKeygenScreen is closed, the main window
        becomes visible, ensuring that the user can return to the main application window
        after closing the PublicKeygenScreen. It also checks that the center_widget method
        is called with the main window and that the event is accepted.
        """

        with patch("tools.toolkit.Tools.qt.center_widget") as mocked_center_widget:
            self.ts.show()
            mock_event = MagicMock()
            mocked_center_widget.return_value = self.main_window
            self.ts.closeEvent(mock_event)

            mocked_center_widget.assert_called_once_with(self.main_window)
            self.main_window.show.assert_called_once()
            mock_event.accept.assert_called_once()

            self.ts.close()
            assert not self.ts.isVisible()
