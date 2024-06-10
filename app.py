import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPalette, QColor

# Only needed for access to command line arguments
import sys
from logger import QPlainTextEditLogHandler

from layout import *


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        self.fn(*self.args, **self.kwargs)



class MainWindow(QMainWindow):

    configLayout: QVBoxLayout = None
    logHandler: logging.Handler = None

    def __init__(self):
        super(MainWindow, self).__init__()

        self.threadPool = QThreadPool()
        self.setWindowTitle("My App")

        layoutFirst = QHBoxLayout()
        configLayout = ConfigLayout(self.__redeemCode)
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
    
    def __redeemCode(self):
        logging.info("in __redeemCode")
        import bdoMainWeb
        worker = Worker(bdoMainWeb.runCodeRedeem) # Any other args, kwargs are passed to the run function
        self.threadPool.start(worker)
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    logging.getLogger().addHandler(window.logHandler)
    app.exec()

# Your application won't reach here until you exit and the event
# loop has stopped.

