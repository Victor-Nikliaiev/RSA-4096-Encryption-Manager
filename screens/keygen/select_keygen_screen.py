from screens.keygen.private_keygen_screen import PrivateKeygenScreen
from screens.keygen.public_keygen_screen import PublicKeygenScreen
from screens.keygen.pair_keygen_screen import PairKeygenScreen
from assets.ui.keygen import Ui_SelectKeygen
from PySide6 import QtWidgets as qtw
from tools.toolkit import Tools as t
from backend import signal_manager
from PySide6 import QtCore as qtc


class SelectKeygenScreen(qtw.QWidget, Ui_SelectKeygen):

    def __init__(self):
        """
        Initializes the SelectKeygenScreen widget.

        This constructor sets up the user interface, updates the UI based on the
        settings, and connects various UI elements to their respective event
        handlers, including buttons and radio buttons. It also initializes the
        state of the 'show_next_screen' flag to False.

        :return: None
        """
        super().__init__()
        self.setupUi(self)
        self.show_next_screen = False

        self.next_button.clicked.connect(self.click_next_handler)
        self.gen_priv_key_rb.clicked.connect(
            lambda: signal_manager.selected_option.emit("private")
        )
        self.gen_pub_key_rb.clicked.connect(
            lambda: signal_manager.selected_option.emit("public")
        )
        self.gen_key_pair_rb.clicked.connect(
            lambda: signal_manager.selected_option.emit("key_pair")
        )
        signal_manager.selected_option.connect(self.selected_option_handler)

    @qtc.Slot()
    def click_next_handler(self):
        """
        Slot connected to the clicked signal of the "Next" button.

        This slot retrieves the selected keygen option from the signal manager,
        looks up the corresponding screen class from a dictionary, and shows the
        selected screen. If an invalid option is selected, the slot does nothing.

        :return: None
        """
        screenOptions = {
            "private": PrivateKeygenScreen,
            "public": PublicKeygenScreen,
            "key_pair": PairKeygenScreen,
        }

        selectedOption = signal_manager.saved_data.get("selected_option")
        SelectedScreen = screenOptions.get(selectedOption)

        if not SelectedScreen:
            return

        self.next_screen = SelectedScreen()
        t.qt.center_widget(self.next_screen).show()
        self.show_next_screen = True
        self.close()

    @qtc.Slot()
    def selected_option_handler(self):
        """
        Slot connected to the selected_option signal.
        This slot enables the "Next" button when it receives a signal, indicating
        that a keygen option has been selected.
        """
        self.next_button.setEnabled(True)

    def closeEvent(self, event):
        """
        Reimplements the closeEvent method to show the main window when
        this window is closed, if the 'show_next_screen' flag is False.
        Otherwise, the close event is accepted and the window is closed.
        """
        if self.show_next_screen:
            event.accept()
            return

        signal_manager.saved_data.get("save_main_window").show()
        event.accept()
