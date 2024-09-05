# Grab tables and put into list
# Compare against file of unwanted tables
# Remove unwanted table names from list
# Run through list and create dump of each table

import psycopg
import psycopg.rows

# Return DB Object
def connectDB(mySQLURL):
    return psycopg.connect(f"{mySQLURL}")

# Return a list of tables in the database
def getTableList(dbObject):
    # row_factory outputs data as a dictionary
    with dbObject.cursor(row_factory=psycopg.rows.dict_row) as cur:
        # Pull list of names of tables
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        tables = []
        for item in cur.fetchall():
            tables.append(item["table_name"])
        return tables

# Removes Unwanted Tables from the Table List
def removeUnwantedTables(tableList, unwantedList):
    for y in unwantedList:
        for x in tableList:
            if x == y:
                tableList.remove(y)
    return tableList

# Dumps a single Postgres table
def dumpTable(dbObject, tableName : str):
    with dbObject.cursor(row_factory=psycopg.rows.dict_row) as cur:
        cur.execute(f"Select * FROM \"{tableName}\"")
        return {tableName: cur.fetchall()}

