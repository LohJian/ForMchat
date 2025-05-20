from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

local_user = {"id": 99, "name": "Yu Zhe", "age": 21, "gender": "Male", "faculty": "Computing"}

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return redirect(url_for('show_match', index=0))

@app.route('/matches/<int:index>')
def show_match(index):
    conn = get_db_connection()
    users = conn.execute("SELECT * FROM users WHERE gender = 'Female'").fetchall()
    total = len(users)
    if index >= total:
        return redirect(url_for('show_match', index=0))
    match = users[index]
    likes = conn.execute("SELECT liked_id FROM likes WHERE liker_id = ?", (local_user['id'],)).fetchall()
    liked_user_ids = {like['liked_id'] for like in likes}
    already_liked = match['id'] in liked_user_ids
    liked_users = conn.execute("SELECT * FROM users WHERE id IN ({seq})".format(
        seq=','.join(['?']*len(liked_user_ids)) if liked_user_ids else '0'), tuple(liked_user_ids)).fetchall() if liked_user_ids else []
    conn.close()
    return render_template('matches.html', match=match, index=index, total=total, already_liked=already_liked, liked_users=liked_users)

@app.route('/like/<int:liked_id>/<int:index>', methods=['POST'])
def like_user(liked_id, index):
    conn = get_db_connection()
    conn.execute("INSERT OR IGNORE INTO likes (liker_id, liked_id) VALUES (?, ?)", (local_user['id'], liked_id))
    conn.commit()
    conn.close()
    return redirect(url_for('show_match', index=index + 1))

@app.route('/chat/<int:other_user_id>', methods=['GET', 'POST'])
def chat(other_user_id):
    conn = get_db_connection()
    user = local_user
    other_user = conn.execute("SELECT * FROM users WHERE id = ?", (other_user_id,)).fetchone()
    if not other_user:
        conn.close()
        return "User not found", 404
    if request.method == 'POST':
        msg = request.form['message']
        if msg.strip():
            conn.execute(
                "INSERT INTO messages (sender_id, receiver_id, message) VALUES (?, ?, ?)",
                (user['id'], other_user_id, msg)
            )
            conn.commit()
    chat_history = conn.execute(
        "SELECT sender_id, receiver_id, message, timestamp FROM messages WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?) ORDER BY timestamp",
        (user['id'], other_user_id, other_user_id, user['id'])
    ).fetchall()
    conn.close()
    return render_template('chat.html', user=user, other_user=other_user, chat_history=chat_history)

@app.route('/profile/<int:user_id>')
def view_profile(user_id):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    if not user:
        return "Profile not found", 404
    return render_template('profile.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
