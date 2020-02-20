import os
import urllib
import sqlite3
import pprint
import logging

import pymongo
from dotenv import load_dotenv

log_format = "%(asctime)s - %(levelname)s %(message)s"
logging.basicConfig(level=logging.DEBUG, format=log_format)
logging.disable(logging.CRITICAL)

load_dotenv()

escape = urllib.parse.quote_plus

MONGO_USER = os.getenv("MONGO_USER", default="OOPS")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", default="OOPS")
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER_NAME", default="OOPS")

# Mongo
connection_uri = f"mongodb+srv://{MONGO_USER}:{escape(MONGO_PASSWORD)}"\
                 f"@{MONGO_CLUSTER}.mongodb.net/test?retryWrites=true"\
                  "&w=majority"
client = pymongo.MongoClient(connection_uri)
mongoDB = client.rpg
logging.info("Connection @: " + connection_uri)

# SQLite
db_dirname = "module1-introduction-to-sql"
db_filename = 'rpg_db.sqlite3'
db_path = os.path.join(os.path.dirname(__file__),
                       "..", "..", db_dirname, db_filename)
logging.info(os.path.abspath(db_path))


sqlite_connection = sqlite3.connect(db_path)
cursor = sqlite_connection.cursor()


def table_to_list(table_name, engine):
    """
    Take sqlite table and return a mongoDB bulk insertable list

    table_name: name of table to acquire from sqlite db

    engine: cursor from sqlite3 connection
    """
    query = f"""
    SELECT * FROM {table_name}
    """
    result = engine.execute(query).fetchall()

    column_headers = list(map(lambda x: x[0], engine.description))

    insertable_list = []

    for tup in result:
        document = {}
        for i in range(len(tup)):
            document[column_headers[i]] = tup[i]
        insertable_list.append(document)

    return insertable_list


table_query = """
SELECT
    name
FROM
    sqlite_master
WHERE
    type ='table' AND
    name NOT LIKE 'sqlite_%';
"""
tables = cursor.execute(table_query).fetchall()
sqlite_tables = []

for name in tables:
    sqlite_tables.append(name[0])

if __name__ == "__main__":
    for table in sqlite_tables:
        if table_to_list(table, cursor) == []:
            logging.info(f"Empty list @ table {table}")
        else:
            logging.info(f"Inserting {table}...")
            collection = mongoDB[table]
            collection.insert_many(table_to_list(table, cursor))
    logging.info("Complete.")
