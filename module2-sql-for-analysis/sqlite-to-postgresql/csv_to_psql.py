import os
import csv
from dotenv import load_dotenv
import psycopg2

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
cursor.execute(qItem)

itemCsvPath = os.path.join(os.path.dirname(__file__), 
                           'rpg_csv', 'armory_item.csv')

with open(itemCsvPath, 'r') as itemCsv:
    cursor.copy_from(itemCsv, 'armory_item', sep=',')

qWeapon = """
CREATE TABLE IF NOT EXISTS armory_weapon (
    item_ptr_id SERIAL PRIMARY KEY,
    weight int
);
"""

weaponCsvPath = os.path.join(os.path.dirname(__file__), 
                           'rpg_csv', 'armory_weapon.csv')

with open(weaponCsvPath, 'r') as weaponCsv:
    cursor.copy_from(weaponCsv, 'armory_weapon', sep=',')

connection.commit()

# TODO: read CSV contents and insert rows into a new table

# ~ query = """
# ~ CREATE TABLE IF NOT EXISTS passengers (
    # ~ id SERIAL PRIMARY KEY,
    # ~ survived bool,
    # ~ pclass int,
    # ~ name varchar,
    # ~ sex varchar,
    # ~ age int,
    # ~ sib_spouse_count int,
    # ~ parent_child_count int,
    # ~ fare float8
# ~ );
# ~ """
