# Goal of this project is to back up a database to a text file and upload to a git repo

# This file is responsible for the complete backup process
import modules.schemas.postgres as pg
import modules.config as config
import modules.timer as timer
import os
import json

# Gives the location of the YAML Configuration File
location = os.environ.get("config", "config.yaml")
# Set yaml config as conf
conf = config.importConfig(location)


def main():
    # import config, print config, connect to db, get the list of tables, remove unwanted, dump each table
    print(json.dumps(conf, indent=4))

    for key in conf["databases"]:
        database = conf["databases"][key]
        # Set path for backup files to go to
        if not os.path.exists(database["backup_location"]):
            os.mkdir(database["backup_location"])
        if database["driver"].lower() == "postgres":
            dbOBJ = pg.PostgresDriver(database["uri"])
            dbOBJ.removeUnwantedTables(database["excluded_tables"])
            dbOBJ.dumpTables(f"{database["backup_location"]}")
            del dbOBJ


if __name__ == "__main__":
    main()
    # if post["backup_interval"] > 0:
    #     mainTimer = timer.initializeTimer()
    #     timer.addJob(mainTimer, main, post["backup_interval"])
    #     print("Adding main to timer")
    # #timer.startTimer(mainTimer)
