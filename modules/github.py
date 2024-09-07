import os
from git import Repo
import modules.config as config
import modules.time as t

def gitCommit(location, token):
    repo = Repo(location)
    os.chdir(location)
    backups = os.listdir(location)
    commit_message = "Backup on "+str(t.getTime())
    repo.index.add(backups)
    repo.index.commit(commit_message)
    origin = repo.remote('origin')
    origin.push()

