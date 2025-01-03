from screens.keygen.select_keygen_screen import SelectKeygenScreen
from unittest.mock import MagicMock, patch
from PySide6 import QtWidgets as qtw
from backend import signal_manager
import pytest


class TestSelectKeygenScreen:
    @pytest.fixture(scope="function", autouse=True)
    def autorun(self, qtbot: qtw.QGridLayout):
        """
        Fixture to set up and tear down the SelectKeygenScreen test environment.

        This fixture is automatically used for each test function in the
        TestSelectKeygenScreen class. It initializes the SelectKeygenScreen,
        adds it to the qtbot for interaction, and mocks the main window required
        for the screen to function properly.

        After the test, it ensures the screen is properly closed and cleaned up.
        """

        self.ts = SelectKeygenScreen()
        signal_manager.saved_data["save_main_window"] = MagicMock(spec=qtw.QWidget)
        self.main_window = signal_manager.saved_data["save_main_window"]
        qtbot.addWidget(self.ts)
        yield

    def test_click_next_handler(self):
        """
        Tests that the click_next_handler method correctly handles the selected
        keygen option and shows the appropriate screen.

        The test verifies that the click_next_handler method calls the
        appropriate screen class constructor, calls the center_widget method
        to center the new window, and then shows the new window.

        The test also verifies that the SelectKeygenScreen instance is no longer
        visible after the click_next_handler method is called.
        """

        with patch(
            "screens.keygen.select_keygen_screen.PrivateKeygenScreen"
        ) as MockPrivateKeygenScreen, patch(
            "screens.keygen.select_keygen_screen.PublicKeygenScreen"
        ) as MockPublicKeygenScreen, patch(
            "screens.keygen.select_keygen_screen.PairKeygenScreen"
        ) as MockPairKeygenScreen, patch(
            "tools.toolkit.Tools.qt.center_widget"
        ) as self.mock_center_widget:
            private_keygen_instance = MagicMock(qtw.QWidget)
            public_keygen_instance = MagicMock(qtw.QWidget)
            pair_keygen_instance = MagicMock(qtw.QWidget)

            MockPrivateKeygenScreen.return_value = private_keygen_instance
            MockPublicKeygenScreen.return_value = public_keygen_instance
            MockPairKeygenScreen.return_value = pair_keygen_instance

            self.ts.show()
            self.__test_next_handler_with_option("private", private_keygen_instance)
            self.mock_center_widget.assert_called_once_with(private_keygen_instance)
            assert not self.ts.isVisible()

            self.__test_next_handler_with_option("public", public_keygen_instance)
            self.__test_next_handler_with_option("key_pair", pair_keygen_instance)

    def test_selected_option_handler(self):
        """
        Tests the selected_option_handler method to ensure that it correctly
        enables the "Next" button when a keygen option is selected.
        """

        assert not self.ts.next_button.isEnabled()
        self.ts.selected_option_handler()
        assert self.ts.next_button.isEnabled()

    def test_close_event(self):
        """
        Tests the closeEvent method to ensure that it correctly handles the window
        close event and shows the main window if the show_next_screen flag is set
        to False.

        The test verifies that the closeEvent method calls the accept method of the
        event and shows the main window if the show_next_screen flag is set to
        False. It also verifies that the SelectKeygenScreen instance is no longer
        visible after the closeEvent method is called.
        """

        self.ts.show()
        mock_event = MagicMock()
        self.ts.show_next_screen = True

        self.ts.closeEvent(mock_event)
        mock_event.accept.assert_called_once()

        self.ts.show_next_screen = False
        self.ts.close()
        self.main_window.show.assert_called_once()
        assert not self.ts.isVisible()

    def __test_next_handler_with_option(self, option, instance):
        """
        Helper method to test the next handler with the given option.

        This method tests the click_next_handler method to ensure that it correctly
        instantiates the corresponding screen class from a dictionary, centers it,
        and shows it after the user selects a keygen option.

        :param option: The selected keygen option
        :param instance: The instance of the screen class to be tested
        """
        signal_manager.saved_data["selected_option"] = option
        self.mock_center_widget.return_value = instance
        self.ts.click_next_handler()
        instance.show.assert_called_once()
