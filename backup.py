# Goal of this project is to back up a database to a text file and upload to a git repo

# This file is responsible for the complete backup process
import modules.schemas.postgres as pg
import modules.config as config
import os
import json

# iterate through the tables and make text file

#check db string

#Gives the location of the YAML Configuration File
location = os.environ.get("config", None)

def main():
    conf = config.importConfig(location)
    print(json.dumps(conf, indent=4))
    dbOBJ = pg.connectDB(conf["databases"]["postgres"]["uri"])
    dbTableList = pg.getTableList(dbOBJ)
    tables = pg.removeUnwantedTables(dbTableList, ["Unwanted"])
    for x in tables:
        print(pg.dumpTable(dbOBJ, x))

if __name__ == "__main__":
    main()