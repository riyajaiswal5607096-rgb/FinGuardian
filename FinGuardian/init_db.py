import sqlite3

conn=sqlite3.connect("expenses.db")
cur=conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS expenses(id INTEGER PRIMARY KEY AUTOINCREMENT,amount REAL,category TEXT)""")
conn.commit()
conn.close()

print("Database created Succesfully!")