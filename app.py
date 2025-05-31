import os               #Loh part
import sqlite3
import secrets
import pytz
import time
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import timedelta, datetime
from sqlalchemy.sql import func
from pathlib import Path
from werkzeug.utils import secure_filename
from flask import Flask, session, render_template, request, redirect, url_for, flash
from jinja2 import FileSystemLoader
from sqlalchemy import Column, Integer, ForeignKey, MetaData, create_engine
from sqlalchemy.orm import relationship
from PIL import Image

           
import smtplib      #Yuzhe part  
import uuid
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, redirect, flash ,session
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from datetime import timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

from sqlalchemy import or_, and_, not_      #Ash part
from sqlalchemy.sql.expression import func

app = Flask(__name__, static_folder='frontend/static')  
project_root = os.path.abspath(os.path.dirname(__file__))
template_paths = [
    os.path.join(project_root, 'templates'),         
    os.path.join(project_root, 'frontend/templates'),    
    os.path.join(project_root, 'ash/templates'),    
    os.path.join(project_root, 'website 2/templates'),   
    os.path.join(project_root, 'website/templates')   

]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app.jinja_loader = FileSystemLoader(template_paths)
app.config['SECRET_KEY'] = 'ForMchat1234'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/user/Projects/ForMchat/instance/users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['STATIC_FOLDER'] = os.path.join(BASE_DIR, 'static')
app.config['DEFAULT_AVATAR_PATH'] = os.path.join(app.config['STATIC_FOLDER'], 'images/default_avatar.jpg')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'} 
app.config['UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'uploads/user_avatars')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


metadata = MetaData()
db = SQLAlchemy(app)
migrate =  Migrate(app, db)

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'connect_args': {
        'options': '-c timezone=UTC'
    }
}

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
    avatar = db.Column(db.String(200), default=app.config['DEFAULT_AVATAR_PATH'])
    likes_received = db.relationship("Like", foreign_keys="Like.target_user_id", backref="target_user")
    loves_received = db.relationship("Love", foreign_keys="Love.target_user_id", backref="target_user")
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender')
    received_messages = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver')
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    login_count = db.Column(db.Integer, default=0)

class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False  )
    target_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    session_id = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),server_default=func.now(),nullable=False)


class Love(db.Model):
    __tablename__ = 'loves'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column( db.Integer,  db.ForeignKey('user.id'),  nullable=False  )
    target_user_id = db.Column(db.Integer,  db.ForeignKey('user.id'), nullable=False)
    session_id = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

class Dislike(db.Model):
    __tablename__ = 'dislikes'
    id = db.Column(db.Integer, primary_key=True)
    disliker_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    disliked_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.now)

class Interested(db.Model):
    __tablename__ = 'interested'
    id = db.Column(db.Integer, primary_key=True)
    liker_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    liked_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.now)

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.now)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='notifications')   

local_user = {
    "id": 99,
    "name": "Yu Zhe",
    "age": 21,
    "gender": "Male",
    "faculty": "Computing",
    "race": "Chinese"
}

with app.app_context():
    db.create_all()

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

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
        from sqlalchemy import create_engine, inspect
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        
        inspector = inspect(engine)
        columns = inspector.get_columns('user')
        column_names = [col['name'] for col in columns]
        
        with engine.connect() as connection:
            if 'sex' not in column_names:
                connection.execute('ALTER TABLE user ADD COLUMN sex VARCHAR(50)')
            if 'race' not in column_names:
                connection.execute('ALTER TABLE user ADD COLUMN race VARCHAR(50)')
        
        print("Database schema updated successfully")

def get_avatar_url(self):
    if self.avatar:
        return url_for('static', filename=f'uploads/user_avatars/{self.avatar}')
    return url_for('static', filename='images/default_avatar.jpg')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

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
        try:
            avatar_folder = app.config['UPLOAD_FOLDER']
            avatar_path = os.path.join(avatar_folder, filename)


            timestamp = int(time.time())
            filename = secure_filename(f"{user.id}_{timestamp}.jpg")
            upload_path = os.path.join(avatar_folder, filename)

            img = Image.open(file.stream)
            img = img.convert('RGB')
            img.thumbnail((500, 500))
            img.save(upload_path, 'JPEG', quality=85)

            if user.avatar and 'default' not in user.avatar:
                old_path = os.path.join(avatar_folder, user.avatar)
                if os.path.exists(old_path):
                    os.remove(old_path)

            user.avatar = filename
            db.session.commit()

            flash('Avatar updated successfully!', 'success')

        except Exception as e:
            app.logger.error(f"Error processing avatar: {str(e)}")
            flash('Error processing image', 'error')
    else:
        flash('Invalid file type', 'error')

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
#我改了这里的东西你看下
@app.route('/')
def home():
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))
    return render_template('mainpage.html')
#这个是新加的for那个notification你看下
@app.context_processor
def inject_user_and_notifications():
    user = None
    unread_count = 0
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        unread_count = Notification.query.filter_by(user_id=user_id, is_read=False).count()
    return dict(user=user, unread_count=unread_count)

@app.route('/profile/<int:user_id>', endpoint='profile-page')
def profile(user_id):
    try:
        user = User.query.get_or_404(user_id)
        like_count = Like.query.filter_by(target_user_id=user_id).count()
        love_count = Love.query.filter_by(target_user_id=user_id).count()
        
        return render_template(
            'profile.html',
            user=user,
            like_count=like_count,
            love_count=love_count
        )
    except Exception as e:
        app.logger.error(f"Profile Error: {str(e)}")
        flash("Error loading profile", "error")
        return redirect(url_for('mainpage'))

@app.route('/user/<int:user_id>', endpoint='userprofile-page')
def user_profile(user_id):
    """Show other users' profiles (with interaction)"""
    user = User.query.get_or_404(user_id)
    
    like_count = Like.query.filter_by(target_user_id=user_id).count()
    love_count = Love.query.filter_by(target_user_id=user_id).count()
    
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
    if 'session_id' not in session:
        session['session_id'] = secrets.token_hex(16)

    existing_like = Like.query.filter_by(
        user_id=user_id,
        session_id=session['session_id']
    ).first()

    if existing_like:
        flash("You've already liked this profile!", 'info')
        return redirect(url_for('userprofile-page', user_id=user_id))

    new_like = Like(
        user_id=user_id,
        target_user_id=request.form['receiver_id'],
        session_id=session['session_id'],
        created_at=datetime.now(pytz.timezone('Asia/Kuala_Lumpur'))
    )
    db.session.add(new_like)
    db.session.commit()
    return redirect(url_for('userprofile-page', user_id=user_id))

@app.route('/love/<int:user_id>', methods=['POST'])
def love(user_id):
    if 'session_id' not in session:
        session['session_id'] = secrets.token_hex(16)

    existing_love = Love.query.filter_by(
        user_id=user_id,
        session_id=session['session_id']
    ).first()

    if existing_love:
        flash("You've already loved this profile!", 'info')
        return redirect(url_for('userprofile-page', user_id=user_id))

    new_love = Love(
        user_id=user_id,
        target_user_id=request.form['receiver_id'],
        session_id=session['session_id'],
        created_at=datetime.now(pytz.timezone('Asia/Kuala_Lumpur'))
    )
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
            user.username = request.form.get('username', user.username)
            user.age = int(request.form.get('age', user.age))
            user.sex = request.form.get('sex', user.sex)
            user.race = request.form.get('race', user.race)
            user.faculty = request.form.get('faculty', user.faculty)
            user.location = request.form.get('location', user.location)
            user.bio = request.form.get('bio', user.bio)

            if 'avatar' in request.files:
                avatar_file = request.files['avatar']
                if avatar_file and allowed_file(avatar_file.filename):
                    try:
                        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                        
                        ext = avatar_file.filename.rsplit('.', 1)[1].lower()
                        filename = f"user_{user_id}_{int(time.time())}.{ext}"
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        
                        img = Image.open(avatar_file)
                        img = img.convert('RGB')
                        img.thumbnail((500, 500))
                        img.save(filepath, 'JPEG', quality=85)
                        
                        if user.avatar and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], user.avatar)):
                            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], user.avatar))
                        
                        user.avatar = filename
                    except Exception as img_error:
                        app.logger.error(f"Image processing error: {str(img_error)}")
                        flash('Error processing image', 'error')

            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile-page', user_id=user.id))

        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error updating profile: {str(e)}")
            flash("An error occurred while updating the profile.", "error")

    return render_template("edit_profile.html", user=user)

@app.route('/registerhome')
def registerhome():
    return render_template('home.html')  

@app.route('/matching')
def matching():
    return render_template('matches.html')  


# Yuzhe part
def send_verification_email(to_email):
    sender_email = "yipyuzhe1402@gmail.com"
    sender_password ="ickx ujbm ggmu iggr" 

    subject = "Verify your email - ForMchat"
    verification_link = f"http://localhost:5000/verify?email={to_email}"
    body = f"""
    <html>
      <body>
        <p>Hello,</p>
        <p>Thanks for registering with ForMchat!</p>
        <p>
          <a href="{verification_link}" style="padding: 10px 20px; background-color: #ff99ac; color: white; text-decoration: none; border-radius: 5px;">
            Click here to verify your email
          </a>
        </p>
        <p>Regards,<br>ForMchat Team</p>
      </body>
    </html>
    """
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))


    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print(f"Verification email sent to {to_email}")
            return True
    except Exception as e:
        print("Email sending failed", e)
        return False

def send_reset_password_email(to_email):
    sender_email = "yipyuzhe1402@gmail.com"
    sender_password = "ickx ujbm ggmu iggr"

    subject = "Reset your password - ForMchat"
    reset_link = f"http://localhost:5000/reset_password?email={to_email}"
    body = f"""
     <html><body>
        <p>Hello,</p>
        <p>We received a request to reset your password.</p>
        <p><a href="{reset_link}" style="padding:10px 20px; background-color:#66b3ff; color:white; text-decoration:none; border-radius:5px;">Click here to reset your password</a></p>
        <p>If you did not request this, you can ignore this email.</p>
        <p>Regards,<br>ForMchat Team</p>
    </body></html>
    """
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print(f"Reset password email sent to {to_email}")
    except Exception as e:
        print("Email sending failed", e)

def send_approval_email(to_email):
    sender_email = "yipyuzhe1402@gmail.com"
    sender_password = "ickx ujbm ggmu iggr"

    subject = "Your ForMchat Profile Has Been Approved"
    login_link = "http://localhost:5000/login"
    body = f"""
    <html>
      <body>
        <p>Hi there,</p>
        <p>Congratulations! Your ForMchat profile has been <strong>approved</strong> by the admin.</p>
        <p>
          <a href="{login_link}" style="padding:10px 20px; background-color:#28a745; color:white; text-decoration:none; border-radius:5px;">
            Click here to login
          </a>
        </p>
        <p>Enjoy connecting with others!</p>
        <p>Regards,<br>ForMchat Team</p>
      </body>
    </html>
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print(f"Approval email sent to {to_email}")
            return True
    except Exception as e:
        print("Approval email failed:", e)
        return False
    
def send_rejection_email(to_email):
    sender_email = "yipyuzhe1402@gmail.com"
    sender_password = "ickx ujbm ggmu iggr"

    subject = "Your ForMchat Profile Was Rejected"
    update_link = "http://localhost:5000/complete_profile?email=" + to_email
    body = f"""
    <html>
      <body>
        <p>Hi there,</p>
        <p>We're sorry to inform you that your ForMchat profile was <strong>rejected</strong>.</p>
        <p>You can update your profile and try again:</p>
        <p>
          <a href="{update_link}" style="padding:10px 20px; background-color:#dc3545; color:white; text-decoration:none; border-radius:5px;">
            Update Your Profile
          </a>
        </p>
        <p>Regards,<br>ForMchat Team</p>
      </body>
    </html>
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print(f"Rejection email sent to {to_email}")
            return True
    except Exception as e:
        print("Rejection email failed:", e)
        return False

def send_match_email(to_email, match_name):
    sender_email = "yipyuzhe1402@gmail.com"
    sender_password = "ickx ujbm ggmu iggr"

    subject = "You Have a New Match on ForMchat!"
    login_link = "http://localhost:5000/login"
    body = f"""
    <html>
      <body>
        <p>Hi there,</p>
        <p>🎉 You have a new match with <strong>{match_name}</strong>!</p>
        <p>
          <a href="{login_link}" style="padding:10px 20px; background-color:#ff69b4; color:white; text-decoration:none; border-radius:5px;">
            Login to check it out!
          </a>
        </p>
        <p>Good luck!</p>
        <p>Regards,<br>ForMchat Team</p>
      </body>
    </html>
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print(f"Match email sent to {to_email}")
    except Exception as e:
        print("Match email failed:", e)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect('/admin_dashboard')
        else:
            return 'Invalid admin credentials'
    return render_template('admin_login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect('/admin_login')

    pending_approval_users = User.query.filter(
        User.verification_status == "Pending Approval",
        User.faculty.isnot(None),
        User.age.isnot(None),
        User.sex.isnot(None),
        User.avatar != 'default.jpg'
    ).all()

    verified_users = User.query.filter(User.verification_status == "Approved").all()
    rejected_users = User.query.filter(User.verification_status == "Rejected").all()

    return render_template('admin_dashboard.html', pending_users=pending_approval_users, verified_users=verified_users, rejected_users=rejected_users)

@app.route('/approve/<int:user_id>', methods=['POST'])
def approve_user(user_id):
    if not session.get('admin_logged_in'):
        return redirect('/admin_login')

    user = User.query.get(user_id)
    if user and user.verification_status == "Pending Approval":
        user.verification_status = "Approved"
        db.session.commit()

        if send_approval_email(user.email):
            flash(f'User approved and login email sent to {user.email}')
        else:
            flash('User approved but failed to send login email.')
    return redirect('/admin_dashboard')

@app.route('/reject/<int:user_id>', methods=['POST'])
def reject_user(user_id):
    if not session.get('admin_logged_in'):
        return redirect('/admin_login')

    user = User.query.get(user_id)
    if user and user.verification_status == "Pending Approval":
        user.verification_status = "Rejected"
        db.session.commit()

        if send_rejection_email(user.email):
            flash(f'User rejected and email sent to {user.email}')
        else:
            flash('User rejected but failed to send rejection email.')

    return redirect('/admin_dashboard')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()

        if user:
            send_reset_password_email(user.email)
            flash('Password reset link sent to your email.')
        else:
            flash('Email not found.')

        return redirect('/forgot-password')

    return render_template('forgot_password.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not email.endswith('@student.mmu.edu.my'):
            flash('Please use your school email to register.')
            return redirect('/register')
        
        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect('/register')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered.')
            return redirect('/register')

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        if send_verification_email(email):
            flash('Registration successful. Please verify your email to complete your profile.')
        else:
            flash('There was an issue sending the verification email. Please try again.')
        
        return redirect('/register')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            if user.verification_status == "Approved":
                session['user_id'] = user.id
                user.last_login = datetime.utcnow()
                user.login_count += 1
                db.session.commit()
                flash('Login successful!')
                return redirect('/mainpage')
            elif user.verification_status == "Rejected":
                flash('Your profile was rejected. Please update your profile.')
                return redirect(f'/complete_profile?email={email}')
            elif user.verification_status == "Pending Approval":
                flash('Your profile is still waiting for admin approval.')
                return redirect('/login')
            else:
                flash('Please complete your profile verification.')
                return redirect('/login')
        else:
            flash('Invalid email or password')
            return redirect('/login')
        
        
    return render_template('login.html')

@app.route('/top-active')
def top_active_users():
    one_week_ago = datetime.utcnow() - timedelta(days=7)
    
    top_users = User.query.filter(User.last_login >= one_week_ago)\
                          .order_by(User.login_count.desc())\
                          .limit(5).all()
    
    return render_template('top_active.html', users=top_users)

def reset_weekly_logins():
    with app.app_context():
        User.query.update({User.login_count: 0})
        db.session.commit()
        print("Weekly Leaderboard reset.")
    
scheduler = BackgroundScheduler()
scheduler.add_job(reset_weekly_logins, trigger='cron', day_of_week='mon', hour=0, minute=0)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

@app.route('/verify')
def verify_email():
    email = request.args.get('email')
    user = User.query.filter_by(email=email).first()

    if not email.endswith('@student.mmu.edu.my'):
        flash('This email is not a valid school email address.')
        return redirect('/register')
    
    if user:
        user.is_verified = True
        if user.faculty and user.age and user.sex and user.avatar != 'default.jpg':
            user.verification_status = "Pending Approval"
        else:
            user.verification_status = "Verified"

        db.session.commit()
        flash('Email verified! Please complete your profile.')
    return redirect(f'/complete_profile?email={email}')

@app.route('/mainpage')
def mainpage():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if not user:
        flash('User not found')
        return redirect(url_for('login'))
#zj你看下这里是不是多写了我上面有top active了
    one_week_ago = datetime.utcnow() - timedelta(days=7)
    top_users = User.query.filter(User.last_login >= one_week_ago)\
                          .order_by(User.login_count.desc())\
                          .limit(5).all()

    return render_template('mainpage.html', user=user, users=top_users)

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    email = request.args.get('email')
    user = User.query.filter_by(email=email).first()

    if not user:
        flash('Invalid reset link.')
        return redirect('/login')

    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            flash('Passwords do not match.')
            return redirect(request.url)

        user.password = generate_password_hash(new_password)
        db.session.commit()
        flash('Password reset successfully. You can now log in.')
        return redirect('/login')
    
    return render_template('reset_password.html', email=email)

@app.route('/complete_profile', methods=['GET', 'POST'])
def complete_profile():
    email = request.args.get('email')
    user = User.query.filter_by(email=email).first()

    if not user:
        flash('User not found.')
        return redirect('/login')

    if request.method == 'POST':
        try:
            if 'avatar' in request.files:
                file = request.files['avatar']
                if file.filename != '' and allowed_file(file.filename):
                    filename = secure_filename(f"{user.id}_{int(time.time())}.jpg")
                    upload_path = os.path.join(app.config['AVATAR_UPLOAD_FOLDER'], filename)
                    
                    img = Image.open(file.stream)
                    img = img.convert('RGB')
                    img.thumbnail((500, 500))
                    img.save(upload_path, 'JPEG', quality=85)
                    
                    user.avatar = f"uploads/user_avatars/{filename}"

            user.sex = request.form.get('sex')
            user.race = request.form.get('race')
            user.faculty = request.form.get('faculty')
            user.age = request.form.get('age')
            user.location = request.form.get('location')

            if all([user.age, user.race, user.faculty, user.sex, user.avatar]):
                user.verification_status = "Pending Approval"

            db.session.commit()
            flash('Profile updated successfully. Awaiting admin approval.')
            return render_template('complete_profile.html', email=email)

        except Exception as e:
            db.session.rollback()
            flash(f'Error updating profile: {str(e)}', 'error')
            app.logger.error(f"Error in complete_profile: {e}")

    return render_template('complete_profile.html', email=email)

@app.route('/notifications')
def notifications():
    if 'user_id' not in session:
        flash("Please login first.")
        return redirect('/login')

    user_id = session['user_id']
    notes = Notification.query.filter_by(user_id=user_id).order_by(Notification.timestamp.desc()).all()

    for note in notes:
        if not note.is_read:
            note.is_read = True
    db.session.commit()

    return render_template('notifications.html', notifications=notes)

def view_notifications():
    if 'user_id' not in session:
        flash("Please login first.")
        return redirect('/login')

    user_id = session['user_id']
    notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.timestamp.desc()).all()
    return render_template('notifications.html', notifications=notifications)

# Ashton part
@app.route('/show')
def show():
    return redirect(url_for('show_match'))

@app.route('/matches')
def show_matches():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    current_user = User.query.get(session['user_id'])
    
    reacted_ids = db.session.query(
        or_(
            Interested.liked_id,
            Dislike.disliked_id
        )
    ).filter(
        or_(
            Interested.liker_id == current_user.id,
            Dislike.disliker_id == current_user.id
        )
    ).distinct().all()
    
    reacted_ids = [id[0] for id in reacted_ids] if reacted_ids else []

    match = User.query.filter(
        User.id != current_user.id,
        ~User.id.in_(reacted_ids),
        func.abs(User.age - current_user.age) <= 5
    ).order_by(func.random()).first()

    interested_users = User.query.join(
        Interested, 
        User.id == Interested.liked_id
    ).filter(
        Interested.liker_id == current_user.id
    ).all()

    return render_template(
        'matches.html',
        match=match,
        interested_users=interested_users,
        user=current_user,
        current_user=current_user
    )

@app.route('/interested/<int:liked_id>', methods=['POST'])
def mark_interested(liked_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    new_interest = Interested(
        liker_id=session['user_id'],
        liked_id=liked_id
    )
    db.session.add(new_interest)
    db.session.commit()
    
    mutual_match = Interested.query.filter_by(
        liker_id=liked_id,
        liked_id=session['user_id']
    ).first()
   
    if mutual_match:
        user1 = User.query.get(session['user_id'])
        user2 = User.query.get(liked_id)

        # 通知两人
        notif1 = Notification(user_id=session['user_id'], content=f"You matched with {user2.username}!")
        notif2 = Notification(user_id=liked_id, content=f"You matched with {user1.username}!")
        db.session.add_all([notif1, notif2])
        db.session.commit()

        # 发 email（假设你写的是 send_match_email(email, match_name)）
        try:
            send_match_email(user1.email, user2.username)
            send_match_email(user2.email, user1.username)
        except Exception as e:
            print(f"Email error: {e}")

    return redirect(url_for('show_matches'))

@app.route('/dislike/<int:disliked_id>', methods=['POST'])
def dislike_user(disliked_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    new_dislike = Dislike(
        disliker_id=session['user_id'],
        disliked_id=disliked_id
    )
    db.session.add(new_dislike)
    db.session.commit()
    
    return redirect(url_for('show_matches'))


@app.route('/chat/<int:other_user_id>', methods=['GET', 'POST'])
def chat(other_user_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    current_user = User.query.get_or_404(session['user_id'])
    other_user = User.query.get_or_404(other_user_id)

    if request.method == 'POST':
        message_content = request.form['message'].strip()
        if message_content:
            new_message = Message(
                sender_id=current_user.id,
                receiver_id=other_user.id,
                message=message_content
            )
            db.session.add(new_message)
            db.session.commit()

    chat_history = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == other_user.id)) |
        ((Message.sender_id == other_user.id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.timestamp.asc()).all()

    return render_template(
        'chat.html',
        user=current_user,
        other_user=other_user,
        chat_history=chat_history
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000) 