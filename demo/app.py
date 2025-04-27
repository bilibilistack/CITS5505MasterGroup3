from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import *                       
from models import db                      
from backend.auth_routes import auth_bp    
import os                                  

os.makedirs('data', exist_ok=True)

# Create Flask application instance
app = Flask(__name__)

# Load configuration from config.py
app.config.from_object('config')

# Set the secret key used by Flask sessions
app.secret_key = SECRET_KEY

# Bind SQLAlchemy instance to the Flask app
db.init_app(app)

# Register route blueprints 
app.register_blueprint(auth_bp)

# Create tables in the database (only if they don't already exist)
with app.app_context():
    db.create_all()

# Main entry point of the application
if __name__ == '__main__':
    app.run(debug=True)