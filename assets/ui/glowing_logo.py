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
          body  {
              background-color: #263238;
              font-family: cursive;
          }

          p {
              text-align: center;
              color: #fff;
              font-family: monospace;}

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
          <body style="margin: 0; background: #263238; overflow: hidden;">
          <h1 class="glow">RSA-4096🛡️</h1>
          <canvas style="opacity: 0.7"> </canvas>
          </body>

          <script>
          const C = document.querySelector("canvas"),
            $ = C.getContext("2d"),
            W = (C.width = window.innerWidth),
            H = (C.height = window.innerHeight);

          const str = "01 001 110 01001 1 0 0 10  010 01 010 01 01 010 101 0 000 10 10 100 01",
            matrix = str.split("");

          let font = 15,
            col = W / font,
            arr = [];

          for (let i = 0; i < col; i++) arr[i] = 1;

          function draw() {
            $.fillStyle = "rgba(38,50,56)";
            $.fillRect(0, 0, W, H);
            $.fillStyle = "#609b9e";
            $.font = font + "px system-ui";
            for (let i = 0; i < arr.length; i++) {
              let txt = matrix[Math.floor(Math.random() * matrix.length)];
              $.fillText(txt, i * font, arr[i] * font);
              if (arr[i] * font > H && Math.random() > 0.01) arr[i] = 0;
              arr[i]++;
            }
          }

          setInterval(draw, 121);

          </script>
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
