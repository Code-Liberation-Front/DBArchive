# Goal of this project is to back up a database to a text file and upload to a git repo

# This file is responsible for the complete backup process
import modules.schemas.postgres as pg
import os

# iterate through the tables and make text file

#check db string

dbstring = os.environ.get('DBString')

def main():
    dbOBJ = pg.connectDB(dbstring)
    dbTableList = pg.getTableList(dbOBJ)
    for x in dbTableList:
        print(x)
