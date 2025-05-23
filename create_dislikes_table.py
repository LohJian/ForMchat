import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS dislikes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        disliker_id INTEGER NOT NULL,
        disliked_id INTEGER NOT NULL,
        UNIQUE(disliker_id, disliked_id)
    )
''')

conn.commit()
conn.close()

print("Dislikes table created.")