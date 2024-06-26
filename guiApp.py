from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QAction, QIcon

import sys
import logging
import traceback

from Src.GUI.gui import MainWindow
from Src.Tools.tools import LOGFILE_PATH, IMAGEDIR_PATH
from Src.Page.bdoMainWeb import runCodeRedeem


if __name__ == "__main__":

    # general logger
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename=LOGFILE_PATH, encoding='utf-8', level=logging.INFO, filemode='w')

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = MainWindow(runCodeRedeem)

    # adding item into tray
    tray =QSystemTrayIcon()
    icon = QIcon(IMAGEDIR_PATH + "/icon.jpg")
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
    logging.getLogger().addHandler(window.logHandler)
    try:
        app.exec()
    except Exception as E:
        errorTraceBack = traceback.format_exc()
        logging.error(errorTraceBack)
        print(errorTraceBack)
        print("Please refer to to log file at for further details: ", LOGFILE_PATH)

# Your application won't reach here until you exit and the event
# loop has stopped.

