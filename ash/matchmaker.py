from flask import Flask, render_template
from itertools import combinations

app = Flask(__name__)

# Sample users
users = [
    {"name": "Alice", "interests": ["music", "reading", "hiking"]},
    {"name": "Bob", "interests": ["music", "movies", "sports"]},
    {"name": "Charlie", "interests": ["reading", "sports", "gaming"]},
    {"name": "Diana", "interests": ["music", "hiking", "gaming"]}
]

def find_matches(users):
    matches = []
    for user1, user2 in combinations(users, 2):
        shared = set(user1['interests']) & set(user2['interests'])
        score = len(shared)
        if score > 0:
            matches.append({
                "pair": f"{user1['name']} ❤️ {user2['name']}",
                "shared_interests": list(shared),
                "score": score
            })
    matches.sort(key=lambda x: x["score"], reverse=True)
    return matches

@app.route('/')
def show_matches():
    matches = find_matches(users)
    return render_template('matches.html', matches=matches)

if __name__ == '__main__':
    app.run(debug=True)
    