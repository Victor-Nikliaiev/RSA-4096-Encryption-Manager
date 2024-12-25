import sys
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from assets.ui import Ui_main_window, global_stylesheet
from assets.ui import GlowingLogo
from screens.about import AboutScreen
from screens.encryption import ChooseFileEncryptScreen
from screens.decryption import ChooseFileDecryptScreen
from screens.keygen.select_keygen_screen import SelectKeygenScreen
from tools.toolkit import Tools as t
from backend import signal_manager


class MainWindow(qtw.QMainWindow, Ui_main_window):
    def __init__(self):
        """
        Initializes the main window of the application.

        This constructor sets up the user interface, sets up the language
        translation system, and connects various UI elements to their
        respective event handlers.

        :return: None
        """
        super().__init__()
        self.translator = qtc.QTranslator()
        self.current_language = "en"

        self.setupUi(self)
        self.setupWebLogoAnimation()

        self.actionEnglish.triggered.connect(lambda: self.change_language("en"))
        self.actionEnglish.triggered.emit()

        self.action.triggered.connect(lambda: self.change_language("ru"))
        self.actionEspa_ol.triggered.connect(lambda: self.change_language("es"))

        self.actionExit.triggered.connect(qtw.QApplication.quit)
        self.encrypt_button.clicked.connect(self.handle_encrypt)
        self.actionEncrypt.triggered.connect(self.handle_encrypt)
        self.decrypt_button.clicked.connect(self.handle_decrypt)
        self.actionDecrypt.triggered.connect(self.handle_decrypt)
        self.generate_keys_button.clicked.connect(self.handle_generate_keys)
        self.actionGenerateKeys.triggered.connect(self.handle_generate_keys)
        self.actionAbout.triggered.connect(self.handle_about)

    def setupWebLogoAnimation(self):
        """
        Setup the logo animation.

        This method creates an instance of GlowingLogo() and
        adds it to the layout of the q_logo widget.
        """

        glowing_log = GlowingLogo()

        layout = qtw.QVBoxLayout(self.q_logo)
        layout.addWidget(glowing_log)
        self.q_logo.setLayout(layout)

    @qtc.Slot()
    def handle_encrypt(self):
        """
        Slot connected to the encrypt button's clicked signal and
        the "Encrypt" menu item's triggered signal.

        This slot creates a ChooseFileEncryptScreen instance,
        saves the current main window, closes the current window,
        and shows the new window.

        :return: None
        """
        self.encrypt_window = t.qt.center_widget(ChooseFileEncryptScreen())
        signal_manager.save_main_window.emit(self)
        self.close()
        self.encrypt_window.show()

    @qtc.Slot()
    def handle_decrypt(self):
        """
        Slot connected to the decrypt button's clicked signal and
        the "Decrypt" menu item's triggered signal.

        This slot creates a ChooseFileDecryptScreen instance,
        saves the current main window, closes the current window,
        and shows the new window.

        :return: None
        """
        self.decrypt_window = t.qt.center_widget(ChooseFileDecryptScreen())
        signal_manager.save_main_window.emit(self)
        self.close()
        self.decrypt_window.show()

    @qtc.Slot()
    def handle_generate_keys(self):
        """
        Slot connected to the "Generate Keys" button's clicked signal and
        the "Generate Keys" menu item's triggered signal.

        This slot creates a SelectKeygenScreen instance, saves the current
        main window, closes the current window, and shows the new window.

        :return: None
        """
        self.gen_keys_window = t.qt.center_widget(SelectKeygenScreen())
        signal_manager.save_main_window.emit(self)
        self.close()
        self.gen_keys_window.show()

    @qtc.Slot()
    def handle_about(self):
        """
        Slot connected to the "About" menu item's triggered signal.

        This slot creates an AboutScreen instance, saves the current main window,
        closes the current window, and shows the new window.

        :return: None
        """

        signal_manager.save_main_window.emit(self)
        self.window = t.qt.center_widget(AboutScreen())
        self.window.show()
        self.close()

    @qtc.Slot()
    def change_language(self, language_code):
        """
        Slot connected to the language change menu items' triggered signal.

        Loads the translation file for the given language code and updates the
        UI text with the new translation.

        :param language_code: A string representing the language code (e.g., "en", "ru", etc.)
        :return: None
        """

        translation_file = f"translations/encryption_{language_code}.qm"
        if self.translator.load(translation_file):
            qtw.QApplication.instance().installTranslator(self.translator)
            self.retranslateUi(self)  # Update UI text with new translation
            self.current_language = language_code
        else:
            print(f"Failed to load translation: {translation_file}")


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    app.setStyleSheet(global_stylesheet)

    window = t.qt.center_widget(MainWindow())
    window.show()
    sys.exit(app.exec())
