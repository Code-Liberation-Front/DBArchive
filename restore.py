# This file is responsible for the complete restore process
import modules.schemas.postgres as pg
import modules.config as config
import modules.error as error
import modules.archive as archive
import os
import shutil
import json

from modules.archive import newest_backup, extract

# Gives the location of the YAML Configuration File
location = os.environ.get("config", "config.yaml")
# Set yaml config as conf
conf = config.import_configuration(location)
# Import Standalone Arguments
args = conf["args"]


def main():
    print(json.dumps(conf, indent=4))

    # Iterates through all the configs and restores the SQL files
    for key in conf["databases"]:
        database = conf["databases"][key]

        try:
            restore_dir = os.path.join(args["backup_location"], key)
            temp_dir = os.path.join(str(os.getcwd()), "tmp")

            if database["driver"].lower() == "mysql":
                dbOBJ = None
            else:
                dbOBJ = pg.PostgresDriver(database["uri"])

            # It then ensures the temporary restore directory is made
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)

            # Extracts the zip file to the temporary folder
            file = archive.newest_backup(restore_dir)
            print(f"Extracting Backup {os.path.basename(file)}")
            archive.extract(file, temp_dir)

            # Restores the database
            dbOBJ.restoreSchema(str(temp_dir))
            dbOBJ.unlockConstraints()
            dbOBJ.restoreDatabase(str(temp_dir))
            dbOBJ.lockConstraints()
            del dbOBJ

            # Temporary directory is then cleaned up
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

        except error.SQLServerError as e:
            print(e)
        except error.SchemaError as e:
            print(e)
        except error.ConstraintError as e:
            print(e)


if __name__ == "__main__":
    main()