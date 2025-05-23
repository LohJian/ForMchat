from flask import Flask, render_template, request, redirect, flash 
from flask_sqlalchemy import SQLAlchemy 
from werkzeug.security import generate_password_hash,check_password_hash
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_migrate import Migrate
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'ForMchat1234'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)
migrate =  Migrate(app, db)

class User(db.Model):
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
    avatar = db.Column(db.String(200), default='default.jpg')
    likes = db.Column(db.Integer, default=0)
    loves = db.Column(db.Integer, default=0)

with app.app_context():
    db.create_all()

def send_verification_email(to_email):
    sender_email = "yipyuzhe1402@gmail.com"
    sender_password ="hatk oppz rfcs bqvr" 

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
    except Exception as e:
        print("Email sending failed", e)

def send_reset_password_email(to_email):
    sender_email = "yipyuzhe1402@gmail.com"
    sender_password = "hatk oppz rfcs bqvr"

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
        new_user =User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        send_verification_email(email)
        flash('Registered successfully. Please check your MMU email to verify your account.')
        return redirect("/register")

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            if user.is_verified:
                flash('Login successful! Welcome back.')
                return redirect('/dashboard')
            else:
                 flash('Please verify your email before logging in.')
        else:
            flash('Invalid email or password')
            
    return render_template('login.html')    

@app.route('/verify')
def verify_email():
    email = request.args.get('email')
    user = User.query.filter_by(email=email).first()

    if user:
        if email.endswith('@student.mmu.edu.my'):
            user.is_verified = True
            user.verification_status = "Verified"
            db.session.commit()
            flash('Student verified successfully! You can now log in.')    
            return redirect(f'/complete_profile/sex?email={email}')
        else:
           flash('This email is not a valid school email address.')
    else:
        flash('Verification failed. Email not found.')
    
    return redirect('/register')    

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

@app.route('/complete_profile/sex', methods=['GET', 'POST'])
def complete_profile_sex():
    email = request.args.get('email')
    user = User.query.filter_by(email=email).first()

    if not user:
        flash('User not found.')
        return redirect('/login')
    
    if request.method == 'POST':
        sex = request.form['sex']
        user.sex = sex
        db.session.commit()
        return redirect(f'/complete_profile/race?email={email}')

    return render_template('complete_profile_sex.html', email=email)

@app.route('/complete_profile/race', methods=['GET', 'POST'])
def complete_profile_race():
    email = request.args.get('email')
    user = User.query.filter_by(email=email).first()

    if not user:
        flash('User not found.')
        return redirect('/login')

    if request.method == 'POST':
        race = request.form['race']
        user.race = race
        db.session.commit()
        return redirect(f'/complete_profile/faculty?email={email}')

    return render_template('complete_profile_race.html', email=email)

@app.route('/complete_profile/faculty', methods=['GET', 'POST'])
def complete_profile_faculty():
    email = request.args.get('email')
    user = User.query.filter_by(email=email).first()

    if not user:
        flash('User not found.')
        return redirect('/login')

    if request.method == 'POST':
        faculty = request.form['faculty']
        user.faculty = faculty
        db.session.commit()
        return redirect(f'/complete_profile/age?email={email}')

    return render_template('complete_profile_faculty.html', email=email)

@app.route('/complete_profile/age', methods=['GET', 'POST'])
def complete_profile_age():
    email = request.args.get('email')
    user = User.query.filter_by(email=email).first()

    if not user:
        flash('User not found.')
        return redirect('/login')

    if request.method == 'POST':
        age = request.form['age']
        user.age = age
        db.session.commit()
        return redirect(f'/complete_profile/location?email={email}')

    return render_template('complete_profile_age.html', email=email)

@app.route('/complete_profile/location', methods=['GET', 'POST'])
def complete_profile_location():
    email = request.args.get('email')
    user = User.query.filter_by(email=email).first()

    if not user:
        flash('User not found.')
        return redirect('/login')

    if request.method == 'POST':
        location = request.form.get('location')

        if not location:
            flash('Please enter your location.')
            return redirect(request.url)

        user.location = location
        db.session.commit()

        return redirect(f'/complete_profile/avatar?email={email}')

    return render_template('complete_profile_location.html', email=email)

@app.route('/complete_profile/avatar', methods=['GET', 'POST'])
def complete_profile_avatar():
    email = request.args.get('email')
    user = User.query.filter_by(email=email).first()

    if not user:
        flash('User not found')
        return redirect('/login')
    
    if request.method == 'POST':
        if request.form.get('skip') == 'true':
            flash('You can upload an avatar later in Edit Profile.')
            return redirect('/dashboard')

        if 'avatar' not in request.files:
            flash('No file uploaded.')
            return redirect(request.url)
        
        file = request.files['avatar']

        if file.filename == '':
            flash('No file selected.')
            return redirect(request.url)
        
        if file:
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            upload_folder = os.path.join('static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, unique_filename)
            file.save(file_path)

            user.avatar = unique_filename
            db.session.commit()

            return redirect(f'/dashboard')

    return render_template('complete_profile_avatar.html', email=email)
      
if __name__ == '__main__':
    app.run(debug=True)