DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    race TEXT,
    faculty TEXT
);

DROP TABLE IF EXISTS likes;
CREATE TABLE likes (
    liker_id INTEGER,
    liked_id INTEGER,
    PRIMARY KEY (liker_id, liked_id)
);

DROP TABLE IF EXISTS dislikes;
CREATE TABLE dislikes (
    disliker_id INTEGER,
    disliked_id INTEGER,
    PRIMARY KEY (disliker_id, disliked_id)
);

DROP TABLE IF EXISTS messages;
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER,
    receiver_id INTEGER,
    message TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Add some sample users
INSERT INTO users (name, age, gender, race, faculty) VALUES
('Zachary Wong', 23, 'Male', 'Chinese', 'Computing'),
('Sophia Tan', 22, 'Female', 'Chinese', 'Arts'),
('Amir Khan', 24, 'Male', 'Malay', 'Engineering'),
('Emily Lee', 21, 'Female', 'Chinese', 'Science'),
('Nina Patel', 20, 'Female', 'Indian', 'Computing');