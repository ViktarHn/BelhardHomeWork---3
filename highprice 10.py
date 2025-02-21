import sqlite3
import pandas as pd

conn = sqlite3.connect('wines.db')
query = """
    SELECT title, winery, country, price 
    FROM wines 
    WHERE price IS NOT NULL 
    ORDER BY price DESC 
    LIMIT 10
"""

df = pd.read_sql(query, conn)
print(df)
conn.close()