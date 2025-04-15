class User:
    def __init__(self, name, gender, looking_for, preferences):
        self.name = name
        self.gender = gender
        self.looking_for = looking_for
        self.preferences = set(preferences)

    def __repr__(self):
        return f"{self.name} ({self.gender})"


def calculate_match_score(user1, user2):
    if user1.looking_for != user2.gender or user2.looking_for != user1.gender:
        return 0

    shared_preferences = user1.preferences.intersection(user2.preferences)
    return len(shared_preferences)


def find_matches(users):
    matches = []

    for i in range(len(users)):
        for j in range(i + 1, len(users)):
            score = calculate_match_score(users[i], users[j])
            if score > 0:
                matches.append((users[i], users[j], score))

    matches.sort(key=lambda x: x[2], reverse=True)
    return matches


if __name__ == "__main__":
    users = [
        User("Alice", "Female", "Male", ["music", "sports", "travel"]),
        User("Bob", "Male", "Female", ["music", "movies", "travel"]),
        User("Charlie", "Male", "Female", ["sports", "tech", "travel"]),
        User("Diana", "Female", "Male", ["movies", "tech", "music"]),
    ]

    matches = find_matches(users)

    print("Top Matches:")
    for user1, user2, score in matches:
        print(f"{user1} ❤️ {user2} — Score: {score}")