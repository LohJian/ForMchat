import os
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from pathlib import Path
from werkzeug.utils import secure_filename
from flask import Flask, session, render_template, request, redirect, url_for, flash

basedir = Path(__file__).parent
instance_path = basedir / "instance"
instance_path.mkdir(exist_ok=True)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{instance_path}/users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your-secret-key-123'  
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['UPLOAD_FOLDER'] = 'static/uploads'  
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    age = db.Column(db.Integer)
    faculty = db.Column(db.String(50))
    bio = db.Column(db.Text)
    location = db.Column(db.String(100))
    avatar = db.Column(db.String(200), default='default.jpg')
    likes = db.Column(db.Integer, default=0)
    loves = db.Column(db.Integer, default=0)

with app.app_context():
    db.create_all()

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

@app.route('/test-db')
def test_db():
    try:
        users = User.query.all()
        return f"Database connected! Found {len(users)} users."
    except Exception as e:
        return f"Database error: {str(e)}"

@app.route('/profile/<int:user_id>')
def profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('profile.html', user=user)

@app.route('/like/<int:user_id>', methods=['POST'])
def handle_like(user_id):
    user = User.query.get_or_404(user_id)
    if not session.get(f'liked_{user_id}'):
        user.likes += 1
        session[f'liked_{user_id}'] = True
        db.session.commit()  
    return render_template('like_button.html', user=user)

@app.route('/loves/<int:user_id>', methods=['POST'])
def handle_loves(user_id):
    user = User.query.get_or_404(user_id)
    if not session.get(f'loves_{user_id}'):
        user.loves += 1
        session[f'loves_{user_id}'] = True
        db.session.commit()  
    return render_template('loves_button.html', user=user)

@app.route('/edit-profile/<int:user_id>', methods=['GET', 'POST'])
def edit_profile(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        try:

            if 'avatar' in request.files:
                file = request.files['avatar']
                if file.filename != '' and allowed_file(file.filename):
                    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True) 
                    filename = secure_filename(f"user_{user_id}_{file.filename}")
                    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)   
                    file.save(save_path)
                    user.avatar = f"uploads/{filename}"
                    print(f"File saved to: {save_path}")                 

            user.username = request.form['username']
            user.age = int(request.form['age'])
            user.faculty = request.form.get('faculty', user.faculty)
            user.location = request.form['location']
            user.bio = request.form['bio']

            db.session.commit()
            flash('Profile updated sucessfully!', 'success')

        except Exception as e:
            db.session.rollback()
            flash(f'Error updating profile: {str(e)}', 'error')
            print(f"Error: {str(e)}")

        return redirect(url_for('profile', user_id=user_id))
    
    return render_template('edit_profile.html', user=user)

@app.route('/create-user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        try:
            new_user = User(
                username=request.form['username'],
                age=request.form['age'],
                faculty=request.form['faculty'],
                bio=request.form['bio'],
                location=request.form['location'],
                avatar='default.jpg',
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('profile', user_id=new_user.id))
        except Exception as e:
            db.session.rollback()
            return f"Error creating user: {str(e)}"
    
    return render_template('create_user.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # 使用默认端口5000