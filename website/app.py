from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import  generate_passeord_hash
import os

app = Flask(_name_)
app.secret_key = 'ForMchat1234'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.string(80))
    email = db.Column(db.string(120))
    password = db.Column(db.string(200))

with app.app_context():
    cd.create_all()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered.')
            return redirect('/regiter')

        new_user =User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registered successfully.')
        return redirect('/register')

    return render_template('/regiter.html')

if _name_ == '_main_':
    app.run(debug=True)