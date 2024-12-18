from PySide6 import QtCore as qtc
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey


class Signal(qtc.QObject):
    file_dropped = qtc.Signal(str)
    update_next_button_status = qtc.Signal(bool)
    public_key_accepted = qtc.Signal(RSAPublicKey)


signal = Signal()
