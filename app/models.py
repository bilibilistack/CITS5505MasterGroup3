from flask_login import UserMixin
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):  # Add UserMixin here
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)##   username as unique identifier
    email = db.Column(db.String(120), unique=True, nullable=False)  ##  email address
    password_hash = db.Column(db.String(128), nullable=False) ## Store salted password
    date_registered = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    # Set the password as a hashed value
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Verify the password against the stored hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    



class WeatherData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    city = db.Column(db.String(100),db.ForeignKey('city.city_name', name='fk_weatherdata_city_cityname'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    temp_min = db.Column(db.Float, nullable=False)
    temp_max = db.Column(db.Float, nullable=False)
    weather = db.Column(db.Float, nullable=False)
    wind_direction = db.Column(db.Float, nullable=False)
    wind_speed = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    precip_mm = db.Column(db.Float, nullable=False)
    city_rel = db.relationship('City', backref='weather_data', foreign_keys=[city])

class Share(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    weatherdata = db.Column(db.String(500), nullable=False)  
    shared_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    shared_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    share_time = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    is_read = db.Column(db.Boolean, default=False)  # Flag to indicate if the share has been read
    is_deleted = db.Column(db.Boolean, default=False)  # Flag to indicate if the share has been deleted
    is_favorite = db.Column(db.Boolean, default=False)  # Flag to indicate if the share is marked as favorite
    shared_by_user = db.relationship('User', foreign_keys=[shared_by])
    shared_to_user = db.relationship('User', foreign_keys=[shared_to])

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(100), unique=True, nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    main_spots = db.Column(db.String(500), nullable=True)  # List of main spots in the city
    tips = db.Column(db.String(1000), nullable=True)  # Tips for the city

    def __repr__(self):
        return f'<City {self.city_name}>'

