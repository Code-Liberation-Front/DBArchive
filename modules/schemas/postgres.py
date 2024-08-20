#This file pulls the data from the database and puts it into an object

import psycopg
import os

dbstring = os.environ.get('DBString')

with psycopg.connect(f"{dbstring}") as conn:

    with conn.cursor() as cur:

        # Pull list of names of tables
        with cur.copy("SELECT table_name FROM information_schema.tables WHERE table_schema='public'") as tableNames:
            for tableNames in tableNames.rows():
                print(tableNames)  # return unparsed tables