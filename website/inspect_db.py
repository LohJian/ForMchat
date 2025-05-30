import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    avatar TEXT,
    age INTEGER,
    faculty TEXT,
    race TEXT,
    bio TEXT,
    common_traits TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS likes (
    liker_id INTEGER,
    liked_id INTEGER,
    PRIMARY KEY (liker_id, liked_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER,
    receiver_id INTEGER,
    text TEXT
)
''')

conn.commit()
conn.close()

print("✅ Tables created successfully in database.db.")