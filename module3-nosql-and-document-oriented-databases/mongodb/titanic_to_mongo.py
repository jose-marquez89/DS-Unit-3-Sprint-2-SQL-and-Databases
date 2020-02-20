import os
import urllib
import pprint
import logging
import csv

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
mongoDB = client.titanic
logging.info("Connection @: " + connection_uri)


def csv_to_list(path):
    """Read csv and return a mongoDB bulk insertable list"""
    with open(path, 'r') as c:
        reader = csv.reader(c)

        reader_rows = [row for row in reader]
        column_names = reader_rows[0]
        logging.info(pprint.pprint(column_names))

        insertable_list = []

        for x in range(len(reader_rows)):
            if x == 0:
                continue
            document = {}
            for y in range(len(reader_rows[x])):
                document[column_names[y]] = reader_rows[x][y]
            insertable_list.append(document)

    return insertable_list


if __name__ == "__main__":
    titanicCsvPath = os.path.join(os.path.dirname(__file__),
                                  "..", "..",
                                  "module2-sql-for-analysis",
                                  "titanic.csv")
    collection = mongoDB.passengers
    collection.insert_many(csv_to_list(titanicCsvPath))
