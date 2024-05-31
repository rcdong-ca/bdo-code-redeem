import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
    QHBoxLayout
)
from PyQt6.QtGui import QPalette, QColor

# Only needed for access to command line arguments
import sys
import customWidgets as CW
from layout import *



class MainWindow(QMainWindow):

    configLayout: QVBoxLayout = None
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        layoutFirst = QHBoxLayout()
        configLayout = ConfigLayout()

        layoutFirst.addLayout(configLayout)
        layoutFirst.addWidget(CW.Color("Red"))

        widget = QWidget()
        widget.setLayout(layoutFirst)
        self.setCentralWidget(widget)

        print(configLayout.getData())


    def show_state(self, s):
        print(s == Qt.CheckState.Checked.value)
        print(s)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

# Your application won't reach here until you exit and the event
# loop has stopped.

