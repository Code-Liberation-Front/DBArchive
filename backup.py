# Goal of this project is to back up a database to a text file and upload to a git repo

# This file is responsible for the complete backup process
import modules.schemas.postgres as pg
import modules.config as config
import modules.timer as timer
import modules.error as error
import modules.time_utils as time_utils
import modules.archive as archive
import os
import json
import shutil
import signal

# Gives the location of the YAML Configuration File
location = os.environ.get("config", "config.yaml")
# Set yaml config as conf
conf = config.import_configuration(location)
# Import Standalone Arguments
args = conf["args"]


def main():
    # import config, print config, connect to db, get the list of tables, remove unwanted, dump each table
    print(json.dumps(conf, indent=4))

    # Iterates through all the configs and dumps the SQL files
    for key in conf["databases"]:
        database = conf["databases"][key]
        temp_dir = os.path.join(str(os.getcwd()), "tmp")

        try:
            backup_dir = os.path.join(args["backup_location"], key)

            # If the driver is postgres, it connects and dumps the tables using psycopg
            if database["driver"].lower() == "mysql":
                dbOBJ = None
            else:
                dbOBJ = pg.PostgresDriver(database["uri"])

            # Tables unwanted in the backup are then removed
            dbOBJ.removeUnwantedTables(database["excluded_tables"])

            # If the path does not exist for the database, create
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)

            # It then ensures the temporary compression directory is made
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)

            # Database is Dumped to temporary folder
            files = dbOBJ.dumpDatabase(temp_dir)
            filename = f"{key}_{time_utils.getDateTimeFSAware()}"
            archive.backup(os.path.join(str(backup_dir), filename), temp_dir)

            # Temporary directory is then cleaned
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

            # If there is more than the backup count, then the oldest backups are removed
            while 0 < int(args["backup_count"]) < archive.backup_count(backup_dir):
                os.remove(archive.oldest_backup(backup_dir))

            # Prints the names of the files it just created
            print(files)

            # Deletes the database object
            del dbOBJ
        except error.SQLServerError as e:
            print(e)

def sig_handler(sig, obj):
    print(f"Signal {sig} received. Deleting Object {obj}")
    del obj
    exit(0)

if __name__ == "__main__":
    # Run the program once
    main()

    # Start the timer if an interval is given
    if args["backup_interval"] > 0:
        mainTimer = timer.Scheduler(main, args["backup_interval"])

        # Sets up signal handlers to stop timer object
        signal.signal(signal.SIGINT, lambda sig, frame: sig_handler(sig, mainTimer))
        signal.signal(signal.SIGTERM, lambda sig, frame: sig_handler(sig, mainTimer))
        mainTimer.start_timer()