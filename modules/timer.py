from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.base import SchedulerNotRunningError

# Used to initialize the python timer
def initialize_timer():
    scheduler = BlockingScheduler()
    return scheduler

# Runs the job at the specified interval
class Scheduler:
    def __init__(self, function, interval):
        self.scheduler = initialize_timer()
        self.function = function
        self.interval = interval
        print("Adding program to timer")
        self.add_job()

    def __del__(self):
        try:
            self.scheduler.shutdown()
        except SchedulerNotRunningError:
            pass

    # Add a program to the timer
    def add_job(self):
        self.scheduler.add_job(self.function,'interval', hours=int(self.interval))

    # Start the timer
    def start_timer(self):
        self.scheduler.start()