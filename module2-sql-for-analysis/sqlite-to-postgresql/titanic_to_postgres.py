import os
import csv
from dotenv import load_dotenv
import psycopg2

load_dotenv() 

TDB_NAME = os.getenv("TDB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

connection = psycopg2.connect(dbname=TDB_NAME, 
                              user=DB_USER, 
                              password=DB_PASSWORD, 
                              host=DB_HOST,
                              port=DB_PORT)
cursor = connection.cursor()
query = """
CREATE TABLE IF NOT EXISTS passengers (
    survived bool,
    pclass int,
    name varchar,
    sex varchar,
    age float8,
    sib_spouse_count int,
    parent_child_count int,
    fare float8
);
"""
cursor.execute(query)

titanicCsvPath = os.path.join(os.path.dirname(__file__), 
                           '..', 'titanic.csv')

with open(titanicCsvPath, 'r') as titanicCsv:
    next(titanicCsv)
    cursor.copy_from(titanicCsv, 'passengers', sep=',')

connection.commit()
cursor.close()
connection.close()
