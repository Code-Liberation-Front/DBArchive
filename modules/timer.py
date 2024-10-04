from apscheduler.schedulers.blocking import BlockingScheduler

# Used to inialize the python timer
def initializeTimer():
    scheduler = BlockingScheduler()
    return scheduler

# Add a program to the timer
def addJob(timer, program, time):
    timer.add_job(program,'interval', hours=int(time))

# Start the timer
def startTimer(scheduler):
    scheduler.start()