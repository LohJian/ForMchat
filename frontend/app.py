import os
from datetime import timedelta
from werkzeug.utils import secure_filename
from flask import Flask, session, render_template, request, redirect, url_for, flash


app = Flask(__name__)
app.secret_key = 'your-secret-key-123'  # Must be set for sessions to work
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # 上传文件保存路径
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  # 文件类型
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 最大文件2mb

def create_mock_user():
    return{
        "id": 1,
        "likes":0,
        "loves":0,
        "username": "JIANLOH",
        "instagram" : "jianloh_123",
        "age": 19,
        "faculty": "FCI",
        "bio": "like girl",
        "location": "From Seremban",
        "interests": ["Valorant", "Basketball"],
        "avatar" : 'images/default_avatar.jpg'
    }

with app.app_context():
    mock_user = create_mock_user()

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

@app.route('/profile/<int:user_id>')
def profile(user_id):
    return render_template('profile.html', user=mock_user)

@app.route('/like/<int:user_id>', methods=['POST'])
def handle_like(user_id):
    if not session.get('liked'):
        mock_user['likes'] += 1
        session['liked'] = True  
    return render_template('like_button.html', user=mock_user)

@app.route('/love/<int:user_id>', methods=['POST'])
def handle_love(user_id):
    if not session.get('loved'):
        mock_user['loves'] += 1
        session['loved'] = True
    return render_template('love_button.html', user=mock_user)

@app.route('/edit-profile/<int:user_id>', methods=['GET', 'POST'])
def edit_profile(user_id):
    if request.method == 'POST':
        print("Form submitted!")  
        print("Form data:", request.form)
        print("Files:", request.files)

        if 'avatar' in request.files:
            file = request.files['avatar']

            if file.filename != '' :
                if allowed_file(file.filename):
                    try:
                        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                        
                        filename = secure_filename(f"user_{user_id}_{file.filename}")
                        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        
                        file.save(save_path)
                        print(f"File saved to: {save_path}")
                        
                        mock_user['avatar'] = f"uploads/{filename}"
                        flash('Avatar updated successfully!', 'success')
                    except Exception as e:
                        print(f"Error saving file: {str(e)}")
                        flash('Error saving avatar file', 'error')
                else:
                    flash('Invalid file type (allowed: PNG, JPG, JPEG, GIF)', 'error')

        mock_user.update({
            'username': request.form['username'],
            'age': int(request.form['age']),
            'faculty': request.form.get('faculty', mock_user['faculty']),
            'location': request.form['location'],
            'bio': request.form['bio'],
            'interests': [i.strip() for i in request.form['interests'].split(',')]
        })
        
        return redirect(url_for('profile', user_id=user_id))
    
    return render_template('edit_profile.html', user=mock_user)


if __name__ == '__main__':
    app.run(debug=True, port=5000)  # 使用默认端口5000