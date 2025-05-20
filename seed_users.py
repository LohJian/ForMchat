import sqlite3

conn = sqlite3.connect('users.db')
users = [
    (1, "Alice Johnson", 25, "Female", "Science"),
    (2, "Bob Smith", 28, "Male", "Engineering"),
    (3, "Cathy Lee", 22, "Female", "Arts"),
    (4, "David Kim", 30, "Male", "Business"),
    (5, "Emma Davis", 27, "Female", "Law"),
    (6, "Frank Miller", 24, "Male", "Medicine")
]

conn.executemany("INSERT INTO users (id, name, age, gender, faculty) VALUES (?, ?, ?, ?, ?)", users)
conn.commit()
conn.close()
