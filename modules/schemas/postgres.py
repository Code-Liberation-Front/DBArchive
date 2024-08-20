# Grab tables and put into list
# Compare against file of unwanted tables
# Remove unwanted table names from list
# Run through list and create dump of each table

import psycopg
import subprocess

# Return DB Object
def connectDB(mySQLURL):
    return psycopg.connect(f"{mySQLURL}")

def getTableList(dbObject):
    with dbObject.cursor() as cur:
        # Pull list of names of tables
        return cur.copy("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    
def removeUnwantedTables(tableList, unwantedList):
    for x in tableList:
        for y in unwantedList:
            if x == y:
                tableList.remove(y)
    return tableList

def dumpTable(dburl,tableName):
    try:
        process = subprocess.Popen(
            ['pg_dump',
             '--dbname=postgresql://{}'.format(dburl),
             '-Fc',
             '-f', f"data/backup/{tableName}.sql",
             '-v'],
            stdout=subprocess.PIPE
        )
        output = process.communicate()[0]
        if int(process.returncode) != 0:
            print('Command failed. Return code : {}'.format(process.returncode))
            exit(1)
        return output
    except Exception as e:
        print(e)
        exit(1)