import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
)
from PySide6.QtWebEngineWidgets import QWebEngineView


class GlowingLogo(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create the web engine view to display HTML
        self.web_view = QWebEngineView()

        # Load the HTML content directly
        html_content = """
       <!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {
    background-color: #263238;
    font-family: cursive;
}

.glow {
    padding-top: 30px;
    font-size: 60px;
    color: #fff;
    text-align: center;
    animation: glow 1s ease-in-out infinite alternate;
    font-family: monospace;
    will-change: text-shadow;
}

@keyframes glow {
    from {
        text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #06dbe6, 0 0 40px #06dbe6;
    }

    to {
        text-shadow: 0 0 20px #fff, 0 0 30px #49ffff, 0 0 40px #49ffff;
    }
}
</style>
</head>
<body>

<h1 class="glow">RSA-4096🛡️</h1>

</body>
</html>

        """

        # Load the HTML into the web view
        self.web_view.setHtml(html_content)

        # Set up the layout and add the web view to the main window
        layout = QVBoxLayout()
        layout.addWidget(self.web_view)

        # Set up the QWidget container
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Set the window title
        self.setWindowTitle("HTML and CSS in PySide6")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Create layout
        layout = QVBoxLayout()

        # Create custom widget and QPushButton
        custom_widget = GlowingWidget()
        custom_widget.setFixedSize(517, 250)
        button = QPushButton("Click Me")

        # Add widgets to the layout
        layout.addWidget(custom_widget)
        layout.addWidget(button)

        # Set the layout for the main window
        self.setLayout(layout)
        self.setWindowTitle("Main Window with Custom Widget")


if __name__ == "__main__":
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec()
