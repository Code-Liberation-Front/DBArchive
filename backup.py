# Goal of this project is to back up a database to a text file and upload to a git repo

# This file is responsible for the complete backup process
import modules.schemas.postgres as pg
import modules.config as config
import modules.timer as timer
import modules.error as error
import os
import json

# Gives the location of the YAML Configuration File
location = os.environ.get("config", "config.yaml")
# Set yaml config as conf
conf = config.importConfig(location)
args = conf["args"]


def main():
    # import config, print config, connect to db, get the list of tables, remove unwanted, dump each table
    print(json.dumps(conf, indent=4))

    # Iterates through all the configs and dumps the SQL files
    for key in conf["databases"]:
        database = conf["databases"][key]
        files = []

        # Set path for backup files to go to
        if not os.path.exists(args["backup_location"]):
            os.mkdir(args["backup_location"])

        # If the driver is postgres, it connects and dumps the tables using psycopg
        if database["driver"].lower() == "postgres":
            try:
                dbOBJ = pg.PostgresDriver(database["uri"])
                dbOBJ.removeUnwantedTables(database["excluded_tables"])
                files = dbOBJ.dumpTables(f"{args["backup_location"]}")
                print(files)
                del dbOBJ
            except error.SQLServerError as e:
                print(e)


if __name__ == "__main__":
    main()
    # if post["backup_interval"] > 0:
    #     mainTimer = timer.initializeTimer()
    #     timer.addJob(mainTimer, main, post["backup_interval"])
    #     print("Adding main to timer")
    # #timer.startTimer(mainTimer)
