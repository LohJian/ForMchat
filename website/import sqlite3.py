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
    PRIMARY KEY (liker_id, liked_id),
    FOREIGN KEY (liker_id) REFERENCES users(id),
    FOREIGN KEY (liked_id) REFERENCES users(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER,
    receiver_id INTEGER,
    text TEXT,
    FOREIGN KEY (sender_id) REFERENCES users(id),
    FOREIGN KEY (receiver_id) REFERENCES users(id)
)
''')

conn.commit()
conn.close()

print("Database initialized.")