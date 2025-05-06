import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
application = Flask(__name__)

# Set the secret key used by Flask sessions
csrf = CSRFProtect(application)


# sqllite database path folder
os.makedirs('../instance/', exist_ok=True)
# Load configuration from config.py in the same folder
application.config.from_pyfile('config.py')

# Initialize the database with the Flask application
db.init_app(application) 

import app.models

migrate = Migrate(application, db)

import app.routes              
from app.auth_routes import auth_bp
from app.upload_routes import upload_bp    
from app.share import share_bp
from app.api_routes import api_bp
                             

# Register route blueprints 
application.register_blueprint(auth_bp)
application.register_blueprint(upload_bp)
application.register_blueprint(share_bp)
application.register_blueprint(api_bp)


