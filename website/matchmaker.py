from flask import Flask, render_template, redirect, url_for, request
import sqlite3
import os

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('user.db')
    conn.row_factory = sqlite3.Row
    return conn

def count_common_traits(user1, user2):
    common = 0
    if user1['race'] == user2['race']:
        common += 1
    if user1['faculty'] == user2['faculty']:
        common += 1
    if abs(user1['age'] - user2['age']) <= 5:
        common += 1
    return common

def find_compatible_users(current_user):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE id != ?", (current_user['id'],))
    users = cursor.fetchall()
    matches = []
    for user in users:
        if user['sex'] != current_user['sex']:
            common = count_common_traits(current_user, user)
            user_dict = dict(user)
            user_dict['common_traits'] = common
            matches.append(user_dict)
    matches.sort(key=lambda u: u['common_traits'], reverse=True)
    conn.close()
    return matches

@app.route('/')
@app.route('/match/<int:index>')
def show_match(index=0):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username = ?", ("Yu Zhe",))
    local_user = cursor.fetchone()
    if not local_user:
        return "Local user not found", 404

    matches = find_compatible_users(local_user)
    if not matches:
        return "No matches found"

    match = matches[index % len(matches)]

    cursor.execute('SELECT 1 FROM likes WHERE liker_id = ? AND liked_id = ?', (local_user['id'], match['id']))
    already_liked = cursor.fetchone() is not None

    conn.close()
    return render_template('matches.html',
                           match=match,
                           local_user=local_user,
                           index=index,
                           total=len(matches),
                           already_liked=already_liked)

@app.route('/like/<int:liked_id>/<int:index>', methods=['POST'])
def like_user(liked_id, index):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username = ?", ("Yu Zhe",))
    local_user = cursor.fetchone()
    if not local_user:
        return "Local user not found", 404

    try:
        cursor.execute('INSERT INTO likes (liker_id, liked_id) VALUES (?, ?)', (local_user['id'], liked_id))
        conn.commit()
    except sqlite3.IntegrityError:
        pass

    conn.close()
    return redirect(url_for('show_match', index=index))

@app.route('/chat/<int:user_id>', methods=["GET", "POST"])
def chat(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username = ?", ("Yu Zhe",))
    local_user = cursor.fetchone()

    cursor.execute("SELECT * FROM user WHERE id = ?", (user_id,))
    target_user = cursor.fetchone()

    if request.method == "POST":
        sender = request.form["sender"]
        text = request.form["text"]
        cursor.execute('INSERT INTO messages (sender_id, receiver_id, text) VALUES (?, ?, ?)', (local_user['id'], target_user['id'], text))
        conn.commit()

    cursor.execute("SELECT * FROM messages WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?)", 
                   (local_user['id'], target_user['id'], target_user['id'], local_user['id']))
    messages = cursor.fetchall()

    conn.close()
    return render_template('chat.html', local_user=local_user, target_user=target_user, messages=messages)

def setup_database():
    if os.path.exists('user.db'):
        os.remove('user.db')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE user (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT,
                        age INTEGER,
                        sex TEXT,
                        faculty TEXT,
                        race TEXT,
                        bio TEXT,
                        avatar TEXT)''')
    cursor.execute('''CREATE TABLE likes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        liker_id INTEGER,
                        liked_id INTEGER,
                        UNIQUE(liker_id, liked_id))''')
    cursor.execute('''CREATE TABLE messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        sender_id INTEGER,
                        receiver_id INTEGER,
                        text TEXT)''')
    users = [
        ("Yu Zhe", 19, "male", "FCI", "chinese", "Hi, I'm Yu Zhe!", "default.jpg"),
        ("Jasmine", 19, "female", "FCI", "chinese", "Hi there, I'm Jasmine!", "default.jpg"),
        ("Siti", 19, "female", "FCI", "malay", "Nice to meet you! I'm Siti.", "default.jpg"),
        ("Fatimah", 18, "female", "FOE", "malay", "Hey! I'm Fatimah!", "default.jpg"),
        ("Issha", 18, "female", "FOM", "indian", "Issha here!", "default.jpg")
    ]
    cursor.executemany('INSERT INTO user (username, age, sex, faculty, race, bio, avatar) VALUES (?, ?, ?, ?, ?, ?, ?)', users)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    setup_database()
    app.run(debug=True)