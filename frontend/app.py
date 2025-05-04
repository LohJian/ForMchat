import os
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import timedelta
from pathlib import Path
from werkzeug.utils import secure_filename
from flask import Flask, session, render_template, request, redirect, url_for, flash
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
import secrets

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or 'dev-key-123' 
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['UPLOAD_FOLDER'] = os.path.join('images', 'uploads') 
app.config['DEFAULT_AVATAR'] = 'images/default_avatar.jpg'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/user/Projects/ForMchat/frontend/user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    verification_status = db.Column(db.String(100), default="Pending")
    age = db.Column(db.Integer)
    race = db.Column(db.String(50))
    faculty = db.Column(db.String(50))
    sex = db.Column(db.String(10))
    bio = db.Column(db.Text)
    location = db.Column(db.String(100))
    avatar = db.Column(db.String(100), default=app.config['DEFAULT_AVATAR'])
    liked_users = relationship("Like", foreign_keys="Like.user_id", backref="liker")
    loved_users = relationship("Love", foreign_keys="Love.user_id", backref="lover")
    likes_received = relationship("Like", foreign_keys="Like.target_user_id", backref="liked_user")
    loves_received = relationship("Love", foreign_keys="Love.target_user_id", backref="loved_user")


class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  
    target_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Love(db.Model):
    __tablename__ = 'loves'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    target_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

def generate_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)
    return session['csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token

@app.route('/test-db')
def test_db():
    first_user = User.query.first()
    return f"First user: {first_user.username if first_user else 'No users found'}"

def migrate_database():
    with app.app_context():
        # Create a database engine directly
        from sqlalchemy import create_engine, inspect
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        
        # Check if columns exist
        inspector = inspect(engine)
        columns = inspector.get_columns('user')
        column_names = [col['name'] for col in columns]
        
        # Add missing columns
        with engine.connect() as connection:
            if 'sex' not in column_names:
                connection.execute('ALTER TABLE user ADD COLUMN sex VARCHAR(50)')
            if 'race' not in column_names:
                connection.execute('ALTER TABLE user ADD COLUMN race VARCHAR(50)')
        
        print("Database schema updated successfully")

@app.route('/upload_avatar/<int:user_id>', methods=['POST'])
def upload_avatar(user_id):
    user = User.query.get_or_404(user_id)
    if 'avatar' not in request.files:
        flash('No file selected', 'error')
        return redirect(request.url)
        
    file = request.files['avatar']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(request.url)
        
    if file and allowed_file(file.filename):
        filename = secure_filename(f"{user.id}_{file.filename}")
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        os.makedirs(os.path.dirname(upload_path), exist_ok=True)
        file.save(upload_path)
        
        user.avatar = os.path.join('uploads', filename)
        db.session.commit()
        flash('Avatar updated successfully!', 'success')
        
    return redirect(url_for('profile', user_id=user.id))
        
def check_interaction(action):
    session.permanent = True
    if not session.get(f'has_{action}'):
        session[f'has_{action}'] = True
        return True
    return False

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def home():
    return "Welcome! <a href='/profile/1'>View Profile</a>"

@app.route('/profile/<int:user_id>', endpoint='profile-page')
def profile(user_id):
    user = User.query.get_or_404(user_id)
    print(f"User avatar path: {user.avatar}")  
    print(f"Static folder: {app.static_folder}")
    likes = Like.query.filter_by(target_user_id=user.id).count()
    loves = Love.query.filter_by(target_user_id=user.id).count()
    return render_template('my_profile.html',
                         user=user,
                         likes=likes,
                         loves=loves)

@app.route('/user/<int:user_id>', endpoint='userprofile-page')
def view_profile(user_id):
    user = User.query.get_or_404(user_id)
    print(f"User avatar path: {user.avatar}")  
    print(f"Static folder: {app.static_folder}")
    current_user_id = 1  
    has_liked = Like.query.filter_by(user_id=current_user_id, target_user_id=user.id).first()
    has_loved = Love.query.filter_by(user_id=current_user_id, target_user_id=user.id).first()
    return render_template('view_profile.html',
                         user=user,
                         has_liked=has_liked,
                         has_loved=has_loved)

@app.route('/like/<int:sender_id>/<int:receiver_id>', methods=['POST'])
def handle_like(sender_id, receiver_id):
    if not Like.query.filter_by(user_id=sender_id, target_user_id=receiver_id).first():
        new_like = Like(user_id=sender_id, target_user_id=receiver_id)
        db.session.add(new_like)
        db.session.commit()
    return render_template('like_button.htmx', 
                         user_id=sender_id,
                         target_user_id=receiver_id)

@app.route('/love/<int:sender_id>/<int:receiver_id>', methods=['POST'])
def handle_love(sender_id, receiver_id):
    if not Love.query.filter_by(user_id=sender_id, target_user_id=receiver_id).first():
        new_love = Love(user_id=sender_id, target_user_id=receiver_id)
        db.session.add(new_love)
        db.session.commit()
    return render_template('love_button.htmx',
                         user_id=sender_id,
                         target_user_id=receiver_id)

@app.route('/test-save')
def test_save():
    user = User.query.get(1)
    user.bio = "Test " + datetime.now().strftime("%H:%M:%S")
    db.session.commit()
    return "Saved current time to bio"

@app.route('/edit-profile/<int:user_id>', methods=['GET', 'POST'])
def edit_profile(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        try:
            if 'avatar' in request.files:
                file = request.files['avatar']
                if file.filename != '' and allowed_file(file.filename):
                    filename = secure_filename(f"user_{user_id}_{file.filename}")
                    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    os.makedirs(os.path.dirname('forntend/images/default-avatar.jpg'), exist_ok=True)
                    file.save('static/uploads')
                    user.avatar = f"uploads/{filename}"                

            user.username = request.form['username']
            user.age = int(request.form['age'])
            user.sex = request.form['sex']
            user.race = request.form['race']
            user.faculty = request.form.get('faculty', user.faculty)
            user.location = request.form['location']
            user.bio = request.form['bio']

            db.session.commit()  # Critical!
            flash('Profile updated!', 'success')
            return redirect(url_for('profile', user_id=user_id))
            
        except ValueError as e:
            db.session.rollback()
            flash(f'Invalid data: {str(e)}', 'error')
        except Exception as e:
            db.session.rollback() 
            flash(f'Error updating profile: {str(e)}', 'error')
            app.logger.error(f"Error in edit_profile: {e}")
    
    return render_template('edit_profile.html', user=user)

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # 使用默认端口5000