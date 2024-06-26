from PyQt6.QtCore import Qt, QThreadPool
from PyQt6.QtWidgets import *

from .workers import Worker
from ..Tools.logger import logging, QPlainTextEditLogHandler
from .layout import ConfigLayout, LogLayOut, TimerLayOut

class MainWindow(QMainWindow):

    logHandler: logging.Handler = None
    fn = None
    def __init__(self, callBack):
        super(MainWindow, self).__init__()
        self.fn = callBack
        self.threadPool = QThreadPool()
        self.setWindowTitle("BDO code Redemption")

        layoutFirst = QHBoxLayout()
        lhLayout = QVBoxLayout()
        configLayout = ConfigLayout(self.__runJob)
        logLayout = LogLayOut()
        timerLayout = TimerLayOut()

        lhLayout.addLayout(configLayout)
        lhLayout.addLayout(timerLayout)
        layoutFirst.addLayout(lhLayout)
        layoutFirst.addLayout(logLayout)


        widget = QWidget()
        widget.setLayout(layoutFirst)
        self.setCentralWidget(widget)

        self.logHandler = QPlainTextEditLogHandler(logLayout.getPlainTextWgt())


    def show_state(self, s):
        print(s == Qt.CheckState.Checked.value)
        print(s)
    
    def __runJob(self):
        logging.info("Running job...")
        worker = Worker(self.fn) # Any other args, kwargs are passed to the run function
        self.threadPool.start(worker)
        pass