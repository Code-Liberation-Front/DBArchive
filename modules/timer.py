from apscheduler.schedulers.blocking import BlockingScheduler

def initializeTimer():
    scheduler = BlockingScheduler()
    return scheduler

def addJob(timer, program, time):
    timer.add_job(program,'interval', hours=int(time))

def startTimer(scheduler):
    scheduler.start()