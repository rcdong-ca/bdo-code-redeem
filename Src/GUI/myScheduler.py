from scheduler import Scheduler
from PyQt6.QtCore import QDateTime, QThreadPool

from .workers import Worker


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
        worker = Worker(callBack)
        self.threadPool.start(worker)

