import sqlite3
import random

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("DROP TABLE IF EXISTS likes")
cursor.execute("DROP TABLE IF EXISTS dislikes")
cursor.execute("DROP TABLE IF EXISTS messages")

cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        gender TEXT,
        race TEXT,
        faculty TEXT
    )
''')

cursor.execute('''
    CREATE TABLE likes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        liker_id INTEGER,
        liked_id INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE dislikes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        disliker_id INTEGER,
        disliked_id INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_id INTEGER,
        receiver_id INTEGER,
        message TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

names = [
    "Alice", "Bob", "Clara", "Dan", "Eva", "Frank", "Grace", "Hannah", "Ian", "Jasmine",
    "Kevin", "Lily", "Marcus", "Nina", "Oscar", "Paula", "Quinn", "Rachel", "Sam", "Tina",
    "Uma", "Victor", "Wendy", "Xander", "Yasmin", "Zane", "Brian", "Cathy", "Derek", "Elise",
    "Felix", "Georgia", "Harry", "Isabel", "Jack", "Kara", "Leo", "Maya", "Noah", "Olive",
    "Peter", "Queenie", "Ron", "Sophie", "Tom", "Ursula", "Vince", "Will", "Xia", "Zoe"
]
genders = ["Male", "Female"]
races = ["Chinese", "Malay", "Indian", "Others"]
faculties = ["Computing", "Engineering", "Science", "Arts", "Business", "Law"]

for i in range(50):
    name = names[i % len(names)]
    age = random.randint(18, 28)
    gender = random.choice(genders)
    race = random.choice(races)
    faculty = random.choice(faculties)

    cursor.execute('''
        INSERT INTO users (name, age, gender, race, faculty)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, age, gender, race, faculty))

conn.commit()
conn.close()

print("✅ 50 fake users inserted into users.db!")
