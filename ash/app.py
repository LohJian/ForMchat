from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

local_user = {
    "id": 99,
    "name": "Yu Zhe",
    "age": 21,
    "gender": "Male",
    "faculty": "Computing",
    "race": "Chinese"
}

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return redirect(url_for('show_match'))

@app.route('/matches')
def show_match():
    conn = get_db_connection()

    reacted_users = conn.execute(
        "SELECT liked_id FROM interested WHERE liker_id = ? UNION SELECT disliked_id FROM dislikes WHERE disliker_id = ?",
        (local_user['id'], local_user['id'])
    ).fetchall()
    reacted_ids = [row[0] for row in reacted_users]

    if reacted_ids:
        reacted_filter = "AND id NOT IN ({})".format(','.join(['?'] * len(reacted_ids)))
    else:
        reacted_filter = ""

    query = f"""
        SELECT * FROM users
        WHERE id != ?
        {reacted_filter}
        AND ABS(age - ?) <= 5
        LIMIT 1
    """

    params = [local_user['id']] + reacted_ids + [local_user['age']] if reacted_ids else [local_user['id'], local_user['age']]
    match = conn.execute(query, params).fetchone()

    liked_users = conn.execute(
        "SELECT * FROM users WHERE id IN (SELECT liked_id FROM interested WHERE liker_id = ?)",
        (local_user['id'],)
    ).fetchall()
    conn.close()
    return render_template('matches.html', match=match, liked_users=liked_users)

@app.route('/like/<int:liked_id>', methods=['POST'])
def like_user(liked_id):
    conn = get_db_connection()
    conn.execute("INSERT OR IGNORE INTO interested (liker_id, liked_id) VALUES (?, ?)", (local_user['id'], liked_id))
    conn.commit()
    conn.close()
    return redirect(url_for('show_match'))

@app.route('/dislike/<int:disliked_id>', methods=['POST'])
def dislike_user(disliked_id):
    conn = get_db_connection()
    conn.execute("INSERT OR IGNORE INTO dislikes (disliker_id, disliked_id) VALUES (?, ?)", (local_user['id'], disliked_id))
    conn.commit()
    conn.close()
    return redirect(url_for('show_match'))

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
