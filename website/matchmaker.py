from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
LOCAL_USER_ID = 1

def get_db_connection():
    conn = sqlite3.connect("../users.db") 
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return redirect(url_for("show_match", index=0))

@app.route("/match/<int:index>", methods=["GET", "POST"])
def show_match(index):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id != ?", (LOCAL_USER_ID,))
    all_matches = cursor.fetchall()
    total = len(all_matches)

    if total == 0:
        conn.close()
        return "No matches available."

    match = all_matches[index % total]
    cursor.execute("SELECT * FROM likes WHERE liker_id = ? AND liked_id = ?", (LOCAL_USER_ID, match["id"]))
    already_liked = cursor.fetchone() is not None
    conn.close()

    return render_template("matches.html", match=match, already_liked=already_liked, index=index, total=total)

@app.route("/like/<int:liked_id>/<int:index>", methods=["POST"])
def like_user(liked_id, index):
    conn = get_db_connection()
    conn.execute("INSERT INTO likes (liker_id, liked_id) VALUES (?, ?)", (LOCAL_USER_ID, liked_id))
    conn.commit()
    conn.close()
    return redirect(url_for("show_match", index=index))

@app.route("/chat/<int:other_user_id>", methods=["GET", "POST"])
def start_chat(other_user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        text = request.form["text"]
        cursor.execute("INSERT INTO messages (sender_id, receiver_id, text) VALUES (?, ?, ?)",
                       (LOCAL_USER_ID, other_user_id, text))
        conn.commit()

    cursor.execute("SELECT * FROM users WHERE id = ?", (LOCAL_USER_ID,))
    local_user = cursor.fetchone()

    cursor.execute("SELECT * FROM users WHERE id = ?", (other_user_id,))
    target_user = cursor.fetchone()

    cursor.execute("""
        SELECT * FROM messages
        WHERE (sender_id = ? AND receiver_id = ?)
           OR (sender_id = ? AND receiver_id = ?)
        ORDER BY id ASC
    """, (LOCAL_USER_ID, other_user_id, other_user_id, LOCAL_USER_ID))
    messages = cursor.fetchall()

    conn.close()
    return render_template("chat.html", messages=messages, local_user=local_user, target_user=target_user)

@app.route("/profile/<int:user_id>")
def profile(user_id):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return render_template("profile.html", user=user)

if __name__ == "__main__":
    app.run(debug=True)