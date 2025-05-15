from app.models import User, db
from werkzeug.security import check_password_hash

def register_user(username, email, password):
    """Create and save a new user. Returns (user, error_message)."""
    if User.query.filter_by(username=username).first():
        return None, 'Username already exists.'
    if User.query.filter_by(email=email).first():
        return None, 'Email already registered.'
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return new_user, None

def authenticate_user(username, password):
    """Authenticate user. Returns (user, error_message)."""
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user, None
    return None, 'Invalid credentials!'
