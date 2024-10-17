# Grab tables and put into list
# Compare against file of unwanted tables
# Remove unwanted table names from list
# Run through list and create dump of each table

import psycopg
import psycopg.rows
from psycopg import Error
import modules.error as error
from subprocess import Popen
import shlex
import os


class PostgresDriver:

    # Constructor sets up key items for backing up database
    def __init__(self, postgresuri):
        self.uri = postgresuri
        try:
            self.connection = self.connectDB(postgresuri)
            self.tables = self.getTableList()
            print(f"Initializing Postgres connection to {self.uri}")
        except Error:
            raise error.SQLServerError("Could not connect to DB, either unreachable or uri is incorrect")

    # Destructor cleans up any items left after working with a database
    def __del__(self):
        try:
            self.connection.close()
            print(f"Postgres connection to {self.uri} has been closed")
        except AttributeError:
            pass

    # Return DB Object
    def connectDB(self, uri):
        connection = psycopg.connect(f"{uri}")
        return connection

    def processWait(self, processes):
        # Ensures all the processes are done before finishing
        while processes:
            for index, process in enumerate(processes):
                process.poll()
                if process.returncode is not None:
                    processes.pop(index)
                    break

    # Return a list of tables in the database
    def getTableList(self):
        # row_factory outputs data as a dictionary
        with self.connection.cursor(row_factory=psycopg.rows.dict_row) as cur:

            # Pull list of names of tables and places
            cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
            tables = []

            # Appends tables to object list
            for item in cur.fetchall():
                tables.append(item["table_name"])
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
    def dumpDatabase(self, fileLocation: str):
        processes = []
        locations = []

        # First it dumps the database schema to ensure relationships are properly applied
        command = f"pg_dump {self.uri} -s -c -f {fileLocation}/schema.sql"
        command = shlex.split(command)
        print(command)
        processes.append(Popen(command, shell=False))

        # Runs the commands to dump all the tables
        for name in self.tables:
            command = f"pg_dump {self.uri} -a -f {fileLocation}/{name}.sql -t \\\"{name}\\\""
            command = shlex.split(command)
            print(command)
            processes.append(Popen(command, shell=False))
            # Dumps the locations of files for later use
            locations.append(f"{fileLocation}/{name}.sql")

        # Ensures all the dumping processes are done before finishing
        self.processWait(processes)

        # Returns list of file locations
        return locations

    def restoreSchema(self, fileLocation: str):
        if os.path.exists(f"{fileLocation}/schema.sql"):
            command = f"psql {self.uri} -f {fileLocation}/schema.sql"
            command = shlex.split(command)
            print(command)
            processes = [Popen(command, shell=False)]
            self.processWait(processes)
        else:
            pass


    def restoreDatabase(self, fileLocation: str):
        processes = []

        for file in os.listdir(fileLocation):
            if os.path.isfile(f"{fileLocation}/{file}") and file.endswith(".sql") and file != "schema.sql":
                command = f"psql {self.uri} -f {fileLocation}/{file}"
                command = shlex.split(command)
                print(command)
                processes.append(Popen(command, shell=False))

        # Ensures all the restoring processes are done before finishing
        self.processWait(processes)

    def unlockConstraints(self):
        self.tables = self.getTableList()
        print("Unlocking Database Constraints")
        command = f"psql {self.uri} -c \""
        for table in self.tables:
            command = command + f"ALTER TABLE {table} DISABLE TRIGGER ALL; "
        command = command + "\""
        command = shlex.split(command)
        process = [Popen(command, shell=False)]
        self.processWait(process)
        print("Ensuring Triggers are disabled")
        for table in self.tables:
            with self.connection.cursor(row_factory=psycopg.rows.dict_row) as cur:

                # Pulls list of triggers for a particular table
                cur.execute(f"SELECT oid, tgenabled FROM pg_trigger WHERE tgrelid = '{table}' :: regclass")

                # Ensures triggers are disabled
                for item in cur.fetchall():
                    if item["tgenabled"] != "D":
                        print(f"Constraint {item["oid"]} in table \'{table}\' did not disable properly")

    def lockConstraints(self):
        self.tables = self.getTableList()
        print("Locking Database Constraints")
        command = f"psql {self.uri} -c \""
        for table in self.tables:
            command = command + f"ALTER TABLE {table} ENABLE TRIGGER ALL; "
        command = command + "\""
        command = shlex.split(command)
        process = [Popen(command, shell=False)]
        self.processWait(process)

        print("Ensuring Triggers are reenabled")
        for table in self.tables:
            with self.connection.cursor(row_factory=psycopg.rows.dict_row) as cur:

                # Pulls list of triggers for a particular table
                cur.execute(f"SELECT oid, tgenabled FROM pg_trigger WHERE tgrelid = '{table}' :: regclass")

                # Ensures triggers are enabled
                for item in cur.fetchall():
                    if item["tgenabled"] == "D":
                        print(f"Constraint {item["oid"]} in table \'{table}\' did not reenable")
