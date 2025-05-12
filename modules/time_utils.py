import time
from datetime import date
import os
import modules.config as config

# Gives the location of the YAML Configuration File
location = os.environ.get("config", "config.yaml")
# Set yaml config as conf
conf = config.import_configuration(location)
# Set the tz from the config
os.environ['TZ'] = conf["args"]["tz"]

# Get the current time are return a string with date and time
def getDateTime():
    now = time.localtime()
    current_time = time.strftime("%H:%M:%S", now)
    current_datetime = str(date.today()) + "_" + str(current_time) # Todays Date
    return current_datetime

def getDateTimeFSAware():
    now = time.localtime()
    current_time = time.strftime("%H%M%S", now)
    current_datetime = str(date.today()) + "_" + str(current_time)
    return current_datetime

# Get the current time
def getTime():
    now = time.localtime()
    current_time = time.strftime("%H:%M:%S", now)
    return str(current_time)

# Get the current Date
def getDate():
    current_date = str(date.today()) # Todays Date
    return current_date

# Get the current Year
def getYear():
    year = str(date.today().year) # Todays Date
    return year