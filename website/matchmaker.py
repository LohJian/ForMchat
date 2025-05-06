from flask import Flask, request, jsonify, render_template_string, url_for
import sqlite3
import os

app = Flask(__name__, static_folder='static')

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Find Your Match</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #ffe6f0;
            text-align: center;
            padding: 30px;
        }
        .card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            width: 350px;
            margin: auto;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        .avatars {
            display: flex;
            justify-content: space-around;
            align-items: center;
        }
        .avatar-box {
            text-align: center;
        }
        .avatar {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            object-fit: cover;
            border: 2px solid #000;
            background: #ccc;
        }
        .arrow {
            font-size: 30px;
            margin: 20px;
            cursor: pointer;
        }
        .btn {
            background: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 10px;
            text-decoration: none;
            display: inline-block;
        }
    </style>
</head>
<body>

    <h1>Here's your best match! 💖</h1>

    <div class="card" id="matchCard">
        <div class="avatars">
            <div class="avatar-box">
                <img src="{{ url_for('static', filename='default.jpg') }}" class="avatar" id="localAvatar">
                <p id="localUsername">Local User</p>
            </div>
            <div style="font-size: 24px;">❤️</div>
            <div class="avatar-box">
                <img src="{{ url_for('static', filename='default.jpg') }}" class="avatar" id="matchAvatar">
                <p id="matchUsername">Match User</p>
            </div>
        </div>
        <p id="bio">Bio goes here</p>
        <p id="commonTraits">Common traits: 0</p>
        <a id="profileLink" href="#" class="btn" target="_blank">Click to view profile</a>
    </div>

    <div>
        <span class="arrow" onclick="prevMatch()">⬅️</span>
        <span class="arrow" onclick="nextMatch()">➡️</span>
        <p>More matches here</p>
    </div>

    <script>
        const matches = [];
        let currentIndex = 0;
        let localName = "";

        function displayMatch(index) {
            const match = matches[index];
            document.getElementById('matchUsername').textContent = match.username;
            document.getElementById('bio').textContent = match.bio;
            document.getElementById('commonTraits').textContent = "Common traits: " + match.common_traits;
            document.getElementById('matchAvatar').src = "/static/" + match.avatar;
            document.getElementById('localAvatar').src = "/static/default.jpg"; // Assuming local user is Yu Zhe
            document.getElementById('localUsername').textContent = localName;
            document.getElementById('profileLink').href = "/profile/" + match.username;
        }

        function nextMatch() {
            if (matches.length === 0) return;
            currentIndex = (currentIndex + 1) % matches.length;
            displayMatch(currentIndex);
        }

        function prevMatch() {
            if (matches.length === 0) return;
            currentIndex = (currentIndex - 1 + matches.length) % matches.length;
            displayMatch(currentIndex);
        }

        fetch('/api/matches')
            .then(res => res.json())
            .then(data => {
                localName = data.username;
                matches.push(...data.matches);
                if (matches.length > 0) {
                    displayMatch(0);
                } else {
                    document.getElementById("matchCard").innerHTML = "<h2>No matches found</h2>";
                }
            });
    </script>

</body>
</html>
"""

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
    cursor.execute('SELECT * FROM user WHERE id != ?', (current_user['id'],))
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
def home():
    return render_template_string(HTML_PAGE)

@app.route('/api/matches')
def get_matches():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username = ?", ("Yu Zhe",))
    user = cursor.fetchone()
    if not user:
        return jsonify({'error': 'Local user not found'}), 404
    current_user = dict(user)
    matches = find_compatible_users(current_user)
    return jsonify({'username': current_user['username'], 'matches': matches})

@app.route('/profile/<username>')
def profile(username):
    return f"<h1>Profile page for {username}</h1>"

def setup_database():
    if os.path.exists('user.db'):
        os.remove('user.db')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            age INTEGER,
            sex TEXT,
            faculty TEXT,
            race TEXT,
            bio TEXT,
            avatar TEXT
        )
    ''')
    sample_users = [
        ("Yu Zhe", 19, "male", "FCI", "chinese", "Hi, I'm Yu Zhe!", "default.jpg"),
        ("Jasmine", 19, "female", "FCI", "chinese", "Hi there, I'm Jasmine!", "default.jpg"),
        ("Siti", 19, "female", "FCI", "malay", "Nice to meet you! I'm Siti.", "default.jpg"),
        ("Fatimah", 18, "female", "FOE", "malay", "Hey! I'm Fatimah!", "default.jpg"),
        ("Issha", 18, "female", "FOM", "indian", "Issha here!", "default.jpg")
    ]
    cursor.executemany('INSERT INTO user (username, age, sex, faculty, race, bio, avatar) VALUES (?, ?, ?, ?, ?, ?, ?)', sample_users)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    setup_database()
    app.run(debug=True)