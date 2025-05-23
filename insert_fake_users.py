import sqlite3

users = [
    ("Alice Tan", 22, "Female", "Chinese", "Computing"),
    ("Bob Lee", 24, "Male", "Chinese", "Engineering"),
    ("Cindy Wong", 21, "Female", "Malay", "Business"),
    ("David Kumar", 23, "Male", "Indian", "Science"),
    ("Emma Lim", 25, "Female", "Chinese", "Arts"),
    ("Frank Ong", 20, "Male", "Malay", "Computing"),
    ("Grace Chua", 22, "Female", "Indian", "Engineering"),
    ("Henry Goh", 24, "Male", "Chinese", "Business"),
    ("Ivy Tan", 23, "Female", "Malay", "Science"),
    ("Jack Sim", 21, "Male", "Indian", "Arts"),
    ("Karen Lee", 22, "Female", "Chinese", "Computing"),
    ("Leo Wong", 24, "Male", "Malay", "Engineering"),
    ("Maya Singh", 23, "Female", "Indian", "Business"),
    ("Nathan Lim", 21, "Male", "Chinese", "Science"),
    ("Olivia Tan", 25, "Female", "Malay", "Arts"),
    ("Peter Ng", 20, "Male", "Indian", "Computing"),
    ("Queenie Chua", 22, "Female", "Chinese", "Engineering"),
    ("Ryan Lee", 24, "Male", "Malay", "Business"),
    ("Sophie Tan", 23, "Female", "Indian", "Science"),
    ("Tommy Ong", 21, "Male", "Chinese", "Arts"),
    ("Ursula Goh", 22, "Female", "Malay", "Computing"),
    ("Victor Lim", 24, "Male", "Indian", "Engineering"),
    ("Wendy Tan", 23, "Female", "Chinese", "Business"),
    ("Xavier Sim", 21, "Male", "Malay", "Science"),
    ("Yvonne Lee", 25, "Female", "Indian", "Arts"),
    ("Zachary Wong", 20, "Male", "Chinese", "Computing"),
    ("Amy Tan", 22, "Female", "Malay", "Engineering"),
    ("Brian Lee", 24, "Male", "Indian", "Business"),
    ("Claire Ong", 23, "Female", "Chinese", "Science"),
    ("Derek Lim", 21, "Male", "Malay", "Arts"),
    ("Eva Goh", 25, "Female", "Indian", "Computing"),
    ("Felix Tan", 20, "Male", "Chinese", "Engineering"),
    ("Gloria Sim", 22, "Female", "Malay", "Business"),
    ("Harold Lee", 24, "Male", "Indian", "Science"),
    ("Isabel Wong", 23, "Female", "Chinese", "Arts"),
    ("Jason Ng", 21, "Male", "Malay", "Computing"),
    ("Kelly Tan", 25, "Female", "Indian", "Engineering"),
    ("Louis Lim", 20, "Male", "Chinese", "Business"),
    ("Monica Goh", 22, "Female", "Malay", "Science"),
    ("Nick Lee", 24, "Male", "Indian", "Arts"),
    ("Ophelia Wong", 23, "Female", "Chinese", "Computing"),
    ("Paul Tan", 21, "Male", "Malay", "Engineering"),
    ("Rachel Sim", 25, "Female", "Indian", "Business"),
    ("Steven Ong", 20, "Male", "Chinese", "Science"),
    ("Tina Lee", 22, "Female", "Malay", "Arts"),
    ("Victor Tan", 24, "Male", "Indian", "Computing"),
    ("Willa Goh", 23, "Female", "Chinese", "Engineering"),
    ("Xander Lim", 21, "Male", "Malay", "Business"),
    ("Yasmin Wong", 25, "Female", "Indian", "Science"),
    ("Zane Lee", 20, "Male", "Chinese", "Arts")
]

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

for user in users:
    cursor.execute(
        "INSERT INTO users (name, age, gender, race, faculty) VALUES (?, ?, ?, ?, ?)", user
    )

conn.commit()
conn.close()

print("50 fake users inserted successfully.")