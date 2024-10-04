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
def getTime():
    now = time.localtime()
    current_time = time.strftime("%H:%M:%S", now)
    currentDateTime = str(date.today()) + " " + str(current_time) # Todays Date
    return currentDateTime