from PySide6 import QtCore as qtc


class Signal(qtc.QObject):
    file_dropped = qtc.Signal(str)
    update_next_button_status = qtc.Signal(bool)


signal = Signal()
