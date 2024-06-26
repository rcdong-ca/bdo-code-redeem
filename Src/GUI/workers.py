from PyQt6.QtCore import QRunnable, pyqtSlot, QThreadPool
from PyQt6.QtWidgets import *


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

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


# def workerStartJob(callBack):
#         threadPool = QThreadPool()
#         worker = Worker(callBack) # Any other args, kwargs are passed to the run function
#         threadPool.start(worker)