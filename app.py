import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPalette, QColor

# Only needed for access to command line arguments
import sys
from logger import QPlainTextEditLogHandler

from layout import *


class MainWindow(QMainWindow):

    configLayout: QVBoxLayout = None
    logHandler: logging.Handler = None

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        layoutFirst = QHBoxLayout()
        configLayout = ConfigLayout()
        logLayout = LogLayOut()

        layoutFirst.addLayout(configLayout)
        layoutFirst.addLayout(logLayout)


        widget = QWidget()
        widget.setLayout(layoutFirst)
        self.setCentralWidget(widget)

        self.logHandler = QPlainTextEditLogHandler(logLayout.getPlainTextWgt())


    def show_state(self, s):
        print(s == Qt.CheckState.Checked.value)
        print(s)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    logging.getLogger().addHandler(window.logHandler)
    app.exec()

# Your application won't reach here until you exit and the event
# loop has stopped.

