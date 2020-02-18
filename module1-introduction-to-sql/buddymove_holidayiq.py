import os
import pandas as pd
import sqlite3

dirname = os.path.dirname(__file__)
filename = "buddymove_holidayiq.csv"
csv_path = os.path.join(dirname, filename)
db_path = os.path.join(dirname, "buddymove_holidayiq.sqlite3")

df = pd.read_csv(csv_path)

conn = sqlite3.connect(db_path)
c = conn.cursor()

df.to_sql('review', con=conn, if_exists='replace')

# Count all rows
q1 = """
SELECT COUNT(*)
FROM review;
"""
row_count = c.execute(q1).fetchall()

print("Total Rows:", row_count[0][0])

# How many users who reviewed at least 100 Nature in the
# category also reviewed at least 100 in the Shopping category?
q2 = """
SELECT COUNT(*)
FROM review
WHERE Nature >= 100 AND Shopping >= 100;
"""
user_review_count = c.execute(q2).fetchall()

print("Total Users w/100 Nature & Shopping Review:",
      user_review_count[0][0])

# What are the average number of reviews for each category?
categories = ['Nature', 'Sports',
              'Religious', 'Theatre',
              'Shopping', 'Picnic']

for category in categories:
    query = f"""
    SELECT round(avg(review.{category}), 2)
    FROM review;
    """
    result = c.execute(query).fetchall()
    print(f"{category} Review Average:", result[0][0])
