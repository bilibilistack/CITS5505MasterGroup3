from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models import User
from app.models import db
from app.forms import LoginForm, RegisterForm
from functools import wraps
from app.controllers import register_user, authenticate_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user, error = register_user(form.username.data, form.email.data, form.password.data)
        if error:
            flash(error, 'danger')
            return render_template('register.html', form=form)
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user, error = authenticate_user(form.username.data, form.password.data)
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            print(f"User {user.username} logged in!")
            return render_template('redirect.html', target_url=url_for('main.homechart'))
        else:
            form.password.errors.append(error)
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.intro'))


# Force login for all routes
def login_required(f):
    @wraps(f)  # Use wraps to preserve the original function's metadata
    def wrapper(*args, **kwargs):  # Accept any arguments passed to the wrapped function
        if 'user_id' not in session:  # Check if the user is logged in
            return redirect(url_for('auth.login'))  # Redirect to login if not authenticated
        return f(*args, **kwargs)  # Call the original function if authenticated
    return wrapper