import os
import csv
import logging

from dotenv import load_dotenv
import psycopg2


log_format = "%(asctime)s - %(levelname)s %(message)s"
logging.basicConfig(level=logging.DEBUG, format=log_format)
logging.disable(logging.INFO)

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


# Needed -- armory_item, armory_weapon, charactercreator_character
# charactercreator_character_inventory, charactercreator_cleric
# charactercreator_fighter, charactercreator_mage, charactercreator_thief
# charactercreator_necromancer

# TODO: function executes query and writes csv row values into table
def write_to_table(query, table_name, engine):
    """Executes query and writes csv row values into new table"""
    engine.execute(query)
    csvPath = os.path.join(os.path.dirname(__file__),
                           'rpg_csv', f"{table_name}.csv")
    with open(csvPath, 'r') as csv:
        try:
            engine.copy_from(csv, f"{table_name}", sep=',')
        except psycopg2.errors.UniqueViolation as unqErr:
            logging.error(
              f"Attempting to write duplicate keys for table {table_name}"
            )


connection = psycopg2.connect(dbname=DB_NAME,
                              user=DB_USER,
                              password=DB_PASSWORD,
                              host=DB_HOST,
                              port=DB_PORT)
cursor = connection.cursor()

qItem = """
CREATE TABLE IF NOT EXISTS armory_item (
    item_id SERIAL PRIMARY KEY,
    name varchar(40),
    value int,
    weight int
);
"""
write_to_table(qItem, 'armory_item', cursor)

qWeapon = """
CREATE TABLE IF NOT EXISTS armory_weapon (
    item_ptr_id SERIAL PRIMARY KEY,
    weight int
);
"""
write_to_table(qWeapon, 'armory_weapon', cursor)

qCcc = """
CREATE TABLE IF NOT EXISTS charactercreator_character (
    character_id SERIAL PRIMARY KEY,
    name varchar(40),
    level int,
    exp int,
    hp int,
    strength int,
    intelligence int,
    dexterity int,
    wisdom int
);
"""
write_to_table(qCcc, 'charactercreator_character', cursor)

qCci = """
CREATE TABLE IF NOT EXISTS charactercreator_character_inventory (
    id SERIAL PRIMARY KEY,
    character_id int REFERENCES charactercreator_character,
    item_id int REFERENCES armory_item
);
"""
write_to_table(qCci, 'charactercreator_character_inventory', cursor)

connection.commit()
