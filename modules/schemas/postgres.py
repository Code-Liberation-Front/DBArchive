#This file pulls the data from the database and puts it into an object

import psycopg
import os

port = os.environ.get('DBName')
port = os.environ.get('DBUser')
port = os.environ.get('DBHost')

with psycopg.connect("host={DBHost} dbname={DBName} user={DBUser}") as conn:

    with conn.cursor() as cur:

        with cur.copy("SELECT table_name FROM information_schema.tables WHERE table_schema='public'") as copy:
            for row in copy.rows():
                print(row)  # return unparsed data