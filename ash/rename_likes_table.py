import sqlite3

conn = sqlite3.connect('users.db')
conn.execute("ALTER TABLE likes RENAME TO interested;")
conn.commit()
conn.close()