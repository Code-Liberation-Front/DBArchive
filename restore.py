# This file is responsible for the complete backup process
import modules.schemas.postgres as pg
import modules.config as config
import modules.error as error
import os
import json

# Gives the location of the YAML Configuration File
location = os.environ.get("config", "config.yaml")
# Set yaml config as conf
conf = config.importConfig(location)
# Import Standalone Arguments
args = conf["args"]


def main():
    print(json.dumps(conf, indent=4))

    # Iterates through all the configs and restores the SQL files
    for key in conf["databases"]:
        database = conf["databases"][key]

        # If the driver is postgres, it connects and restores the tables
        if database["driver"].lower() == "postgres":
            try:
                dbOBJ = pg.PostgresDriver(database["uri"])
                dbOBJ.restoreTables(f"{args["backup_location"]}/{key}")
                del dbOBJ
            except error.SQLServerError as e:
                print(e)


if __name__ == "__main__":
    main()