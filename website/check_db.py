import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables found:", cursor.fetchall())

cursor.execute("PRAGMA table_info(users);")
print("Users table structure:", cursor.fetchall())

conn.close()