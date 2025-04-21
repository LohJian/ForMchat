class User:
    def __init__(self, user_data):
        self.name = user_data["name"]              # Name from registration
        self.gender = user_data["gender"]          # User's gender
        self.looking_for = user_data["looking_for"]  # What gender they're looking for
        self.preferences = set(user_data["preferences"])  # Their interests (converted to a set)

    def __repr__(self):
        return self.name  # Makes printing look nice


# Step 2: Function to calculate match score between two users
def calculate_match_score(user1, user2):
    # Check if both users are looking for each other's gender
    if user1.looking_for != user2.gender or user2.looking_for != user1.gender:
        return 0

    # Count how many interests they have in common
    shared = user1.preferences.intersection(user2.preferences)
    return len(shared)


# Step 3: Function to find matches
def find_matches(users):
    matches = []

    # Compare every pair of users
    for i in range(len(users)):
        for j in range(i + 1, len(users)):
            score = calculate_match_score(users[i], users[j])
            if score > 0:
                matches.append((users[i], users[j], score))

    # Sort best matches first
    matches.sort(key=lambda match: match[2], reverse=True)
    return matches


# Step 4: Simulate registered users (you'll get this from a database in a real app)
user_data_list = [
    {"name": "Alice", "gender": "Female", "looking_for": "Male", "preferences": ["music", "travel", "sports"]},
    {"name": "Bob", "gender": "Male", "looking_for": "Female", "preferences": ["music", "travel", "movies"]},
    {"name": "Charlie", "gender": "Male", "looking_for": "Female", "preferences": ["sports", "tech", "gaming"]},
    {"name": "Diana", "gender": "Female", "looking_for": "Male", "preferences": ["music", "tech", "movies"]}
]

# Step 5: Convert user data into User objects
users = [User(data) for data in user_data_list]

# Step 6: Get and print matches
matches = find_matches(users)

print("Top Matches:")
for user1, user2, score in matches:
    print(f"{user1} ❤️ {user2} — Shared interests: {score}")