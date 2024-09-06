import time
from datetime import date
import os
import modules.config as config

# Gives the location of the YAML Configuration File
location = os.environ.get("config", "config.yaml")
# Set yaml config as conf
conf = config.importConfig(location)

os.environ['TZ'] = conf["databases"]["postgres"]["tz"]

def getTime():
    now = time.localtime()
    current_time = time.strftime("%H:%M:%S", now)
    currentDateTime = str(date.today()) + " " + str(current_time) # Todays Date
    return currentDateTime