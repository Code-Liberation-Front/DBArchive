# Grab tables and put into list
# Compare against file of unwanted tables
# Remove unwanted table names from list
# Run through list and create dump of each table

import psycopg
import psycopg.rows
from psycopg import Error
import modules.error as error
from subprocess import PIPE, Popen
import shlex


class PostgresDriver:

    # Constructor sets up key items for backing up database
    def __init__(self, postgresuri):
        self.uri = postgresuri
        self.connection = self.connectDB(postgresuri)
        self.tables = self.getTableList()
        print(f"Initializing Postgres connection to {self.uri}")

    # Destructor cleans up any items left after working with a database
    def __del__(self):
        self.connection.close()
        print(f"Postgres connection to {self.uri} has been closed")

    # Return DB Object
    def connectDB(self, uri):
        try:
            connection = psycopg.connect(f"{uri}")
        except Error:
            print("Cannot connect to DB, either unreachable or uri is incorrect")
            error.exit_program()
        return connection

    # Return a list of tables in the database
    def getTableList(self):
        # row_factory outputs data as a dictionary
        with self.connection.cursor(row_factory=psycopg.rows.dict_row) as cur:
            # Pull list of names of tables
            cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
            tables = []
            for item in cur.fetchall():
                tables.append(item["table_name"])
            if not tables:
                print("List of tables is empty")
                error.exit_program()
            else:
                return tables

    # Removes Unwanted Tables from the Table List
    def removeUnwantedTables(self, unwantedList):
        if not unwantedList:
            print("No tables to remove from list, skipping remove")
            return self.tables
        else:
            for y in unwantedList:
                for x in self.tables:
                    if x == y:
                        self.tables.remove(y)

    # Dumps a single Postgres table
    def dumpTables(self, fileLocation: str):
        processes = []
        for name in self.tables:
            command = f"pg_dump {self.uri} -c -f {fileLocation}/{name}.sql -t \\\"{name}\\\""
            command = shlex.split(command)
            print(command)
            processes.append(Popen(command, shell=False))
        while processes:
            for index, process in enumerate(processes):
                process.poll()
                if process.returncode is not None:
                    processes.pop(index)
                    break
