import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

if tables:
    print("Tables in the database:", tables)
else:
    print("No tables found in the database.")

conn.close()