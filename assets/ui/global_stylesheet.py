global_stylesheet = """QMessageBox {
    background-color: #263238;
    border-radius: 8px;
    color: rgb(119, 186, 198);
}

QMessageBox QLabel {
    color: rgb(119, 186, 198);
    font-size: 14px;
}

QMessageBox QPushButton {
    background-color: rgb(119, 186, 198);
    color: #263238;
    border: 1px solid rgb(97, 153, 163); /* Slightly darker shade */
    padding: 6px 12px;
    border-radius: 4px;
}

QMessageBox QPushButton:hover {
    background-color: rgb(97, 153, 163);
}

QScrollBar:vertical {
    border: 1px solid rgb(119, 186, 198); /* Border color */
    background: #263238; /* Background of the scrollbar */
    width: 16px;
    margin: 16px 0 16px 0; /* Adjust as needed */
}

QScrollBar::handle:vertical {
    background: rgb(119, 186, 198); /* Handle color */
    border-radius: 8px;
    border: 1px solid rgb(97, 153, 163); /* Border around the handle */
    min-height: 20px;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    background: rgb(97, 153, 163); /* Arrow button background */
    border: none;
    height: 16px;
    subcontrol-origin: margin;
}

QScrollBar::add-line:vertical:hover,
QScrollBar::sub-line:vertical:hover {
    background: rgb(119, 186, 198); /* Hover color for buttons */
}

QScrollBar::add-page:vertical, 
QScrollBar::sub-page:vertical {
    background: none; /* Space above and below the handle */
}

 QMenuBar {
                background-color: #263238;
                color: rgb(119, 186, 198);
            }
            QMenuBar::item {
                background-color: #263238;
                color: rgb(119, 186, 198);
               
            }
            QMenuBar::item:selected { /* Hover effect */
                background-color: rgb(119, 186, 198);
                color: #263238;
            }
            QMenu {
                background-color: #263238;
                color: rgb(119, 186, 198);
            }
            QMenu::item {
                background-color: #263238;
                color: rgb(119, 186, 198);
            }
            QMenu::item:selected { /* Hover effect for menu items */
                background-color: rgb(119, 186, 198);
                color: #263238;
            }
"""
