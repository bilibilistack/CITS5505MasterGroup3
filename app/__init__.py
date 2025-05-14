import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from .config import Config, DevelopmentConfig

# Initialize extensions (without app)
db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO()
csrf = CSRFProtect()

# Create the Flask application factory
def create_app(config=Config):
    """Create and configure the Flask application."""
    application = Flask(__name__)
    # Ensure instance folder exists
    os.makedirs('../instance/', exist_ok=True)
    # Load configuration
    application.config.from_object(config)

    # Initialize extensions with app
    db.init_app(application)
    migrate.init_app(application, db)
    socketio.init_app(application)
    csrf.init_app(application)

    # Register blueprints
    from app.auth_routes import auth_bp
    from app.upload_routes import upload_bp
    from app.share_routes import share_bp
    from app.api_routes import api_bp
    from app.routes import main_bp
    application.register_blueprint(auth_bp)
    application.register_blueprint(upload_bp)
    application.register_blueprint(share_bp)
    application.register_blueprint(api_bp)
    application.register_blueprint(main_bp)

    # Initialize login manager
    login = LoginManager(application)
    login.login_view = 'auth.login'

    # Import models and routes
    from app import models, routes
    from app.models import User

    # User loader for Flask-Login
    @login.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return application

# For legacy support, create an app instance if running directly
application = create_app(config=DevelopmentConfig)