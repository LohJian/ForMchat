class User:
    def __init__(self, user_data):
        self.name = user_data["name"]             
        self.gender = user_data["gender"]          
        self.looking_for = user_data["looking_for"]  
        self.preferences = set(user_data["preferences"])  

    def __repr__(self):
        return self.name  



def calculate_match_score(user1, user2):
    
    if user1.looking_for != user2.gender or user2.looking_for != user1.gender:
        return 0

    shared = user1.preferences.intersection(user2.preferences)
    return len(shared)



def find_matches(users):
    matches = []

   
    for i in range(len(users)):
        for j in range(i + 1, len(users)):
            score = calculate_match_score(users[i], users[j])
            if score > 0:
                matches.append((users[i], users[j], score))

   
    matches.sort(key=lambda match: match[2], reverse=True)
    return matches



user_data_list = [
    {"name": "Alice", "gender": "Female", "looking_for": "Male", "preferences": ["music", "travel", "sports"]},
    {"name": "Bob", "gender": "Male", "looking_for": "Female", "preferences": ["music", "travel", "movies"]},
    {"name": "Charlie", "gender": "Male", "looking_for": "Female", "preferences": ["sports", "tech", "gaming"]},
    {"name": "Diana", "gender": "Female", "looking_for": "Male", "preferences": ["music", "tech", "movies"]}
]


users = [User(data) for data in user_data_list]


matches = find_matches(users)

print("Top Matches:")
for user1, user2, score in matches:
    print(f"{user1} ❤️ {user2} — Shared interests: {score}")