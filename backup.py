# Goal of this project is to back up a database to a text file and upload to a git repo

# This file is responsible for the complete backup process
import modules.schemas.postgres as pg
import modules.config as config
import modules.timer as timer
import os
import json

# iterate through the tables and make text file

#check db string

# Gives the location of the YAML Configuration File
location = os.environ.get("config", "config.yaml")
# Set yaml config as conf
conf = config.importConfig(location)
post = conf["databases"]["postgres"]
# Set path for backup files to go to
savepath = post["backup_location"]
if not os.path.exists(savepath):
    os.mkdir(savepath)
os.chdir(savepath)

def main():
    # import config, print config, connect to db, get the list of tables, remove unwanted, dump each table
    print(json.dumps(conf, indent=4))
    dbOBJ = pg.connectDB(conf["databases"]["postgres"]["uri"])
    dbTableList = pg.getTableList(dbOBJ)
    tables = pg.removeUnwantedTables(dbTableList, post["excluded_tables"])
    # Loop throught tables and take snapshot
    for name in tables:
        f = open(str(name+".json"), "w")
        tableContents = json.dumps(pg.dumpTable(dbOBJ, name), indent=2)
        print("Contents to be written to file" + str(tableContents))
        f.write(tableContents)
        f.close()
    dbOBJ.close()

if __name__ == "__main__":
    main()
    print(os.getcwd())
    if post["backup_interval"] > 0:
        mainTimer = timer.initializeTimer()
        timer.addJob(mainTimer, main, post["backup_interval"])
        print("Adding main to timer")
    #timer.startTimer(mainTimer)
    
        