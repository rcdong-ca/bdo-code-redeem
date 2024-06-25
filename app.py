import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPalette, QColor, QAction, QIcon

import sys
import logger
import traceback
import Workers
import bdoMainWeb

from layout import *

class MainWindow(QMainWindow):

    logHandler: logger.logging.Handler = None

    def __init__(self):
        super(MainWindow, self).__init__()

        self.threadPool = QThreadPool()
        self.setWindowTitle("BDO code Redemption")

        layoutFirst = QHBoxLayout()
        lhLayout = QVBoxLayout()
        configLayout = ConfigLayout(self.__redeemCode)
        logLayout = LogLayOut()
        timerLayout = timerLayOut()

        lhLayout.addLayout(configLayout)
        lhLayout.addLayout(timerLayout)
        layoutFirst.addLayout(lhLayout)
        layoutFirst.addLayout(logLayout)


        widget = QWidget()
        widget.setLayout(layoutFirst)
        self.setCentralWidget(widget)

        self.logHandler = logger.QPlainTextEditLogHandler(logLayout.getPlainTextWgt())


    def show_state(self, s):
        print(s == Qt.CheckState.Checked.value)
        print(s)
    
    def __redeemCode(self):
        logger.logging.info("in __redeemCode")
        import bdoMainWeb
        worker = Workers.Worker(bdoMainWeb.runCodeRedeem) # Any other args, kwargs are passed to the run function
        self.threadPool.start(worker)
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = MainWindow()

    # adding item into tray
    tray =QSystemTrayIcon()
    icon = QIcon("icon.jpg")
    tray.setIcon(icon)
    tray.setVisible(True)

    # add menu
    menu = QMenu()
    quit = QAction("Quit") 
    quit.triggered.connect(app.quit) 
    menu.addAction(quit)

    openWindow = QAction("Open")
    openWindow.triggered.connect(window.show)
    menu.addAction(openWindow)
    tray.setContextMenu(menu)

    window.show()
    logger.logging.getLogger().addHandler(window.logHandler)
    try:
        app.exec()
    except Exception as E:
        errorTraceBack = traceback.format_exc()
        logger.logging.error(errorTraceBack)
        print(errorTraceBack)
        print("Please refer to to log file at for further details: ", Tools.LOGFILE_PATH)

# Your application won't reach here until you exit and the event
# loop has stopped.

