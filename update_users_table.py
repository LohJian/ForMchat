import sqlite3

# Connect to your existing users database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Add the 'race' column if it doesn't exist
try:
    cursor.execute("ALTER TABLE users ADD COLUMN race TEXT")
    print("Added 'race' column.")
except sqlite3.OperationalError:
    print("'race' column already exists.")

# Add the 'faculty' column if it doesn't exist
try:
    cursor.execute("ALTER TABLE users ADD COLUMN faculty TEXT")
    print("Added 'faculty' column.")
except sqlite3.OperationalError:
    print("'faculty' column already exists.")

conn.commit()
conn.close()
