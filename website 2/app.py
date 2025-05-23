import os
import smtplib
import uuid
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from datetime import datetime
from datetime import timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from flask import Flask, render_template, request, redirect, flash ,session
from flask_sqlalchemy import SQLAlchemy 
from jinja2 import FileSystemLoader
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)
template_paths = [
    'frontend/templates',      
    'website 2/templates'      
]
app.secret_key = 'ForMchat1234'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
UPLOAD_FOLDER = os.path.join('static', 'upload')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.jinja_loader = FileSystemLoader(template_paths)

db = SQLAlchemy(app)
migrate =  Migrate(app, db)

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    verification_status = db.Column(db.String(100), default="Pending")
    is_admin = db.Column(db.Boolean, default=False)
    age = db.Column(db.Integer)
    race = db.Column(db.String(50))
    faculty = db.Column(db.String(50))
    sex = db.Column(db.String(10))
    bio = db.Column(db.Text)
    location = db.Column(db.String(100))
    avatar = db.Column(db.String(200), default='default.jpg')
    likes = db.Column(db.Integer, default=0)
    loves = db.Column(db.Integer, default=0)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    login_count = db.Column(db.Integer, default=0)

with app.app_context():
    db.create_all()

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

@app.route('/')
def home():
    return render_template('home.html')

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
                return redirect('/dashboard')
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

@app.route('/dashboard')
def dashboard():
    return "<h1>Welcome to your dashboard!</h1>"

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

    if user.verification_status != "Verified":
        flash('Your email must be verified to complete your profile.')
        return redirect('/register')

    if request.method == 'POST':
        sex = request.form.get('sex')
        race = request.form.get('race')
        faculty = request.form.get('faculty')
        age = request.form.get('age')
        location = request.form.get('location')

        user.sex = sex
        user.race = race
        user.faculty = faculty
        user.age = age
        user.location = location

        avatar_file = request.files.get('avatar')
        if avatar_file and avatar_file.filename != '':
            filename = secure_filename(avatar_file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            upload_folder = app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, unique_filename)
            print("saving avatar", file_path)
            avatar_file.save(file_path)
            user.avatar = unique_filename
        
        else:
            print("avatar upload failed")
    
        if user.is_verified and all([user.age, user.race, user.faculty, user.sex, user.avatar != 'default.jpg']):
            user.verification_status = "Pending Approval"

        db.session.commit()
        flash('Profile updated successfully. Awaiting admin approval.')
        return redirect('/login')

    return render_template('complete_profile.html', email=email)

@app.route('/registerhome')
def registerhome():
    return render_template('home.html')  

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')  

if __name__ == '__main__':
    app.run(debug=True)