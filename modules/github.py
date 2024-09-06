import os
from git import Repo
import modules.config as config

# Gives the location of the YAML Configuration File
location = os.environ.get("config", "config.yaml")
# Set yaml config as conf
conf = config.importConfig(location)

def setDir(location):
    repo = Repo(location)