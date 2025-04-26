from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models import User
from app.models import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/successlogin')
def home():
    if 'user_id' in session:
        return f"Hello, {session['username']}! <a href='/logout'>Logout</a>"
    return "<a href={{url_for('auth.login')}}>Login</a> or <a href={{url_for('auth.register')}}>Register</a>"

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['newUsername']
        password = request.form['newPassword']
        password2 = request.form['confirmPassword']
        if User.query.filter_by(username=username).first():
            return "User already exists!"
        if (password!=password2):
            return "Passwords do not match! Please try again."
        if len(password) < 6:
            return "Password must be at least 6 characters long!"
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        print(f"Username: {username}, Password: {password} Added to database")
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            print(f"User {username} logged in!")
            return redirect(url_for('auth.home'))
        else:
            return "Invalid credentials!"
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.home'))
