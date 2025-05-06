from shared_models import db
from sqlite3 import connect

def migrate_data():
    # Create new shared database
    shared_conn = connect('instance/shared.db')
    db.create_all(bind_key=None)  # Create tables
    
    # Connect to old databases
    frontend_conn = connect('frontend/user.db')
    website_conn = connect('website/user.db')
    
    # Migrate users (example)
    frontend_users = frontend_conn.execute('SELECT * FROM user').fetchall()
    website_users = website_conn.execute('SELECT * FROM user').fetchall()
    
    # Insert into new shared DB
    with shared_conn:
        for user in frontend_users + website_users:
            shared_conn.execute(
                '''INSERT INTO users (id, username, email) 
                   VALUES (?, ?, ?)''',
                (user[0], user[1], user[2]))
    
    print("Data migration complete!")

if __name__ == '__main__':
    migrate_data()