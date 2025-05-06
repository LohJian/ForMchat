import os
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import timedelta, datetime
from pathlib import Path
from werkzeug.utils import secure_filename
from flask import Flask, session, render_template, request, redirect, url_for, flash
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-very-secret-key-here'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['UPLOAD_FOLDER'] = os.path.join('images', 'uploads') 
app.config['DEFAULT_AVATAR'] = 'images/default_avatar.jpg'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/user/Projects/ForMchat/frontend/users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

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
    likes_received = relationship("Like", foreign_keys="Like.target_user_id", backref="liked_user")
    loves_received = relationship("Love", foreign_keys="Love.target_user_id", backref="loved_user")


class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    target_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    session_id = db.Column(db.String(50))


class Love(db.Model):
    __tablename__ = 'loves'
    id = db.Column(db.Integer, primary_key=True)
    target_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    session_id = db.Column(db.String(50))

@app.before_request
def before_request():
    if 'session_id' not in session:
        session['session_id'] = secrets.token_hex(16)

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
    user = User.query.get(1)
    return render_template('mainpage.html', user=user)

@app.route('/profile/<int:user_id>', endpoint='profile-page')
def profile(user_id):
    user = User.query.get_or_404(user_id)
    
    like_count = len(user.likes_received)
    love_count = len(user.loves_received)
    
    return render_template('profile.html',
                        user=user,
                        like_count=like_count,
                        love_count=love_count)

@app.route('/user/<int:user_id>', endpoint='userprofile-page')
def user_profile(user_id):
    """Show other users' profiles (with interaction)"""
    user = User.query.get_or_404(user_id)
    
    # Get counts
    like_count = Like.query.filter_by(target_user_id=user_id).count()
    love_count = Love.query.filter_by(target_user_id=user_id).count()
    
    # Check if current session has already liked/loved
    has_liked = Like.query.filter_by(
        target_user_id=user_id,
        session_id=session['session_id']
    ).first() is not None
    
    has_loved = Love.query.filter_by(
        target_user_id=user_id,
        session_id=session['session_id']
    ).first() is not None
    
    return render_template('userprofile.html',
                         user=user,
                         like_count=like_count,
                         love_count=love_count,
                         has_liked=has_liked,
                         has_loved=has_loved)

@app.route('/like/<int:user_id>', methods=['POST'])
def like(user_id):
    """Handle like action"""
    if not Like.query.filter_by(target_user_id=user_id, session_id=session['session_id']).first():
        new_like = Like(target_user_id=user_id, session_id=session['session_id'])
        db.session.add(new_like)
        db.session.commit()
    return redirect(url_for('userprofile-page', user_id=user_id))

@app.route('/love/<int:user_id>', methods=['POST'])
def love(user_id):
    """Handle love action"""
    if not Love.query.filter_by(target_user_id=user_id, session_id=session['session_id']).first():
        new_love = Love(target_user_id=user_id, session_id=session['session_id'])
        db.session.add(new_love)
        db.session.commit()
    return redirect(url_for('userprofile-page', user_id=user_id))


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

            db.session.commit()  
            flash('Profile updated!', 'success')
            return redirect(url_for('profile-page', user_id=user_id))
            
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