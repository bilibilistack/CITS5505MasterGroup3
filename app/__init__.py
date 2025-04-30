from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

application = Flask(__name__)

# Set the secret key used by Flask sessions
application.config['SECRET_KEY'] = 'GROUP3_BEST_TEAM'  # Replace with a secure key
csrf = CSRFProtect(application)

import app.routes              
from app.models import db
from app.auth_routes import auth_bp
from app.upload_routes import upload_bp    
from app.share import share_bp
import os                                  

# sqllite database path folder
os.makedirs('../instance/', exist_ok=True)

# Load configuration from config.py in the same folder
application.config.from_pyfile('config.py')

db.init_app(application)  # Initialize db
migrate = Migrate(application, db)

# Register route blueprints 
application.register_blueprint(auth_bp)
application.register_blueprint(upload_bp)
application.register_blueprint(share_bp)

# Create tables in the database (only if they don't already exist)
with application.app_context():
    db.create_all()

