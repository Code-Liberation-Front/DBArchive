# Goal of this project is to back up a database to a text file and upload to a git repo

# This file is responsible for the complete backup process
import modules.schemas.postgres as pg
import modules.config as config
import modules.timer as timer
import modules.error as error
import modules.time as time
import modules.archive as archive
import os
import json
import shutil

# Gives the location of the YAML Configuration File
location = os.environ.get("config", "config.yaml")
# Set yaml config as conf
conf = config.importConfig(location)
# Import Standalone Arguments
args = conf["args"]


def main():
    # import config, print config, connect to db, get the list of tables, remove unwanted, dump each table
    print(json.dumps(conf, indent=4))

    # Iterates through all the configs and dumps the SQL files
    for key in conf["databases"]:
        database = conf["databases"][key]
        temp_dir = os.path.join(str(os.getcwd()), "tmp")
        files = []

        try:
            backup_dir = os.path.join(args["backup_location"], key)

            # If the driver is postgres, it connects and dumps the tables using psycopg
            if database["driver"].lower() == "mysql":
                dbOBJ = None
            else:
                dbOBJ = pg.PostgresDriver(database["uri"])

            dbOBJ.removeUnwantedTables(database["excluded_tables"])

            # If the path does not exist for the database, create
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)

            # It then ensures the temporary compression directory is made
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)

            # Database is Dumped to temporary folder
            files = dbOBJ.dumpDatabase(temp_dir)
            filename = f"{key}_{time.getDateTimeFSAware()}"
            archive.backup(os.path.join(str(backup_dir), filename), temp_dir)

            # Temporary directory is then cleaned
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

            # If there is more than the backup count, then the oldest backups are removed
            while 0 < int(args["backup_count"]) < archive.backup_count(backup_dir):
                os.remove(archive.oldest_backup(backup_dir))

            print(files)
            del dbOBJ
        except error.SQLServerError as e:
            print(e)


if __name__ == "__main__":
    # Run the program once
    main()
    # Start the timer if an interval is given
    if args["backup_interval"] > 0:
        mainTimer = timer.initializeTimer()
        timer.addJob(mainTimer, main, args["backup_interval"])
        print("Adding program to timer")
        timer.startTimer(mainTimer)
