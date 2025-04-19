from flask import Flask, render_template, request, redirect, flash 
from flask_sqlalchemy import SQLAlchemy 
from werkzeug.security import generate_password_hash,check_password_hash
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = 'ForMchat1234'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)

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
          <a href="{verification_link}" style="padding: 10px 20px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px;">
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
    
@app.route('/')
def home():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
    
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
        return redirect('/register')

    return render_template('register.html')

@app.route('/verify')
def verify_email():
    email = request.args.get('email')
    user = User.query.filter_by(email=email).first()

    if user:
        user.is_verified = True
        db.session.commit()
        flash('Email verified successfully! You can now log in. ')
    else:
        flash('Verification failed. Email not found.')

    return redirect('/register')    
 
if __name__ == '__main__':
    app.run(debug=True)