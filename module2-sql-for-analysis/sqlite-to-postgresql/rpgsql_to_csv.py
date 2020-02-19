import os
import sqlite3
import csv
import logging

log_format = "%(asctime)s - %(levelname)s %(message)s"
logging.basicConfig(level=logging.DEBUG, format=log_format)
logging.disable(logging.CRITICAL)

db_dirname = "module1-introduction-to-sql"
db_filename = 'rpg_db.sqlite3'
db_path = os.path.join(os.path.dirname(__file__),
                       "..", "..", db_dirname, db_filename)


conn = sqlite3.connect(db_path)
c = conn.cursor()


def table_to_csv(table_name):
    query = f"""
    SELECT * FROM {table_name}
    """
    result = c.execute(query).fetchall()

    csv_dir_path = os.path.join(os.path.dirname(__file__), "rpg_csv")

    with open(os.path.join(csv_dir_path,
              f"{table_name}.csv"), 'w') as file:
        writer = csv.writer(file)

        for tup in result:

            # check for tuple items with commas
            check_tup = [(type(item) == str) and
                         (',' in item) for item in tup]

            # if tuple item has comma, remove it and create new tuple
            if any(check_tup):
                logging.info('FTWC')
                corrected = []
                for item in tup:
                    if type(item) == str and ',' in item:
                        s = item.replace(',', '')
                        corrected.append(s)
                    else:
                        corrected.append(item)
                new_row = tuple(corrected)
                logging.info(f"Corrected: {new_row}")
                writer.writerow(new_row)
            else:
                logging.info(f"Writing, unprocessed: {tup}")
                writer.writerow(tup)


table_query = """
SELECT
    name
FROM
    sqlite_master
WHERE
    type ='table' AND
    name NOT LIKE 'sqlite_%';
"""
tables = c.execute(table_query).fetchall()
table_names = []

for name in tables:
    table_names.append(name[0])

if __name__ == "__main__":
    for table in table_names:
        table_to_csv(table)
