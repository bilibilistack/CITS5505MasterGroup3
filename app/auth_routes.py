from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models import User
from app.models import db
from app.forms import LoginForm, RegisterForm
from functools import wraps

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            session['username'] = user.username
            print(f"User {user.username} logged in!")
            return render_template('redirect.html', target_url=url_for('main.homechart'))
        else:
            form.password.errors.append('Invalid credentials!')
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.intro'))


# Force login for all routes below this decorator
def login_required(f):
    @wraps(f)  # Use wraps to preserve the original function's metadata
    def wrapper(*args, **kwargs):  # Accept any arguments passed to the wrapped function
        if 'user_id' not in session:  # Check if the user is logged in
            return redirect(url_for('auth.login'))  # Redirect to login if not authenticated
        return f(*args, **kwargs)  # Call the original function if authenticated
    return wrapper