from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)##   username as unique identifier
    email = db.Column(db.String(120), unique=True, nullable=False)  ##  email address
    password_hash = db.Column(db.String(128), nullable=False) ## Store salted password
    date_registered = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    # Set the password as a hashed value
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    # Verify the password against the stored hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class WeatherData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    temp_min = db.Column(db.Float, nullable=False)
    temp_max = db.Column(db.Float, nullable=False)
    weather = db.Column(db.Float, nullable=False)
    wind_direction = db.Column(db.Float, nullable=False)
    wind_speed = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    precip_mm = db.Column(db.Float, nullable=False)
