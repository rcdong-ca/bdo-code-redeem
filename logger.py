import logging
from PyQt6.QtWidgets import QPlainTextEdit

# Logger for GUI
class QPlainTextEditLogHandler(logging.Handler):
    def __init__(self, textWgt: QPlainTextEdit) -> None:
        super().__init__()
        self.plainTextWgt = textWgt

    def emit(self, record):
        msg = self.format(record)
        self.plainTextWgt.appendPlainText(msg)
    
    def write(self, msg):
        print(msg)
