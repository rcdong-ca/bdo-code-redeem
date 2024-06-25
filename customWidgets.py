
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QMouseEvent, QPalette, QColor, QCursor
from PyQt6.QtCore import *


class Color(QWidget):

    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)



class LabelTextBox(QWidget):
    
    def __init__(self, label: str) -> None:
        super().__init__()
        boxLayout = QHBoxLayout()
        boxLayout.setSpacing(0)
        # boxLayout.setContentsMargins(0,0,0,0)
        self.labelWgt = QLabel(label)
        self.lineWgt = QLineEdit()
        self.labelWgt.setFixedSize(125,25)
        self.lineWgt.setFixedSize(150,25)
        # position label and widget right next to each other
        # self.lineWgt.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.Minimum)
        # self.lineWgt.resize(self.lineWgt.sizeHint())

        boxLayout.addWidget(self.labelWgt) #,0, Qt.AlignmentFlag.AlignLeft)
        boxLayout.addWidget(self.lineWgt) #,0, Qt.AlignmentFlag.AlignLeft)
        self.setLayout(boxLayout)
    
    def getLabel(self):
        return self.labelWgt.text()

    def getText(self):
        return self.lineWgt.text()
    
    def setText(self, text: str):
        self.lineWgt.setText(text)

class LabelComboBox(QWidget):
    def __init__(self, label: str, options: list) -> None:
        super().__init__()
        boxLayout = QHBoxLayout()
        self.labelWgt = QLabel(label, self)
        self.labelWgt.setStyleSheet("background-color:rgb(255,255,150)")
        self.labelWgt.setFixedSize(125,25)
        self.comboWgt = QComboBox()
        self.comboWgt.setFixedSize(150,25)
        self.comboWgt.addItems(options)
        # self.comboWgt.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.Minimum)
        # position label and widget right next to each other
        boxLayout.addWidget(self.labelWgt)
        boxLayout.addWidget(self.comboWgt)
        boxLayout.setSpacing(0)
        boxLayout.setContentsMargins(0,0,0,0)
        self.setLayout(boxLayout)
    
    def getLabel(self):
        return self.labelWgt.text()

    def getText(self):
        print("combo: currentText ", self.comboWgt.currentText() )
        return self.comboWgt.currentText()
    
    def setText(self, text: str):
        try:
            self.comboWgt.setCurrentText(text)
        except Exception:
            print("Invalid Text: ", text)

        