import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from .config import Config

db = SQLAlchemy()
application = Flask(__name__)

# Set the secret key used by Flask sessions
csrf = CSRFProtect(application)

socketio = SocketIO(application)  

# sqllite database path folder
os.makedirs('../instance/', exist_ok=True)
# Load configuration from config.py in the same folder
application.config.from_object(Config)

# Initialize the database with the Flask application
db.init_app(application) 



migrate = Migrate(application, db)


import app.routes              
from app.auth_routes import auth_bp
from app.upload_routes import upload_bp    
from app.share_routes import share_bp
from app.api_routes import api_bp
                             
# Initialize the login manager
login = LoginManager(application)
login.login_view = 'auth.login'  # Redirect to the login page if not logged in


# Register route blueprints 
application.register_blueprint(auth_bp)
application.register_blueprint(upload_bp)
application.register_blueprint(share_bp)
application.register_blueprint(api_bp)


# # User loader for Flask-Login
# import app.models
# from app.models import User  # Make sure User is imported
from app import routes, models

# Move the user loader function to here to avoid circular imports
@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))