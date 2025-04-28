import time
from datetime import date
import os
import modules.config as config

# Gives the location of the YAML Configuration File
location = os.environ.get("config", "config.yaml")
# Set yaml config as conf
conf = config.importConfig(location)
# Set the tz from the config
os.environ['TZ'] = conf["args"]["tz"]

# Get the current time are return a string with date and time
def getDateTime():
    now = time.localtime()
    currentTime = time.strftime("%H:%M:%S", now)
    currentDateTime = str(date.today()) + "_" + str(currentTime) # Todays Date
    return currentDateTime

def getDateTimeFSAware():
    now = time.localtime()
    currentTime = time.strftime("%H%M%S", now)
    currentDateTime = str(date.today()) + "_" + str(currentTime)
    return currentDateTime

# Get the current time
def getTime():
    now = time.localtime()
    currentTime = time.strftime("%H:%M:%S", now)
    return str(currentTime)

# Get the current Date
def getDate():
    currentDate = str(date.today()) # Todays Date
    return currentDate

# Get the current Year
def getYear():
    year = str(date.today().year) # Todays Date
    return year