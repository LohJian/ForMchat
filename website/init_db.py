import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    age INTEGER,
    faculty TEXT,
    race TEXT,
    bio TEXT,
    common_traits TEXT,
    avatar TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS likes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    liker_id INTEGER NOT NULL,
    liked_id INTEGER NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    text TEXT NOT NULL
)
""")

cursor.execute("INSERT INTO users (username, age, faculty, race, bio, common_traits, avatar) VALUES (?, ?, ?, ?, ?, ?, ?)",
               ("TestUser", 20, "Engineering", "Asian", "Hi! I'm a test user.", "Friendly, Kind", "default.jpg"))

conn.commit()
conn.close()

print("✅ Database initialized.")