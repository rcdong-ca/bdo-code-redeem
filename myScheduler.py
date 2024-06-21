import datetime as dt
from scheduler import Scheduler
from PyQt6.QtCore import QDateTime, QThreadPool
import Workers
import logger


class MyScheduler(Scheduler):
    def __init__(self):
        super().__init__()
        self.threadPool = QThreadPool()
    
    # this will be the one we want to run if run callback periodically
    def cyclicJob(self, callBack, day:int, hour:int):
        # schedule the next job
        
        nextDate = QDateTime.currentDateTime()
        nextDate = nextDate.addDays(day)
        nextDate = nextDate.addSecs(60 * 60 * hour)
        self.once(nextDate.toPyDateTime(), self.cyclicJob, args=(callBack, day, hour))
        # run current job
        worker = Workers.Worker(callBack)
        print("THIS SHOULD BE SEPERATE THREAD...")
        self.threadPool.start(worker)

