import os
import json
import datetime
from app import application, db
from app.models import City, WeatherData, User

def safe_float(value):
    # Note: !!!All invalid values will be converted to 0.0!!!
    """Convert value to float, return 0.0 if empty or invalid."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

def load_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def load_cities(city_json_path):
    cities = load_json(city_json_path)
    for c in cities:
        city = City(
            city_name=c['city'],
            lat=safe_float(c['lat']),
            lon=safe_float(c['lon'])
        )
        db.session.merge(city)  # merge to avoid duplicates
    db.session.commit()
    print(f"loaded {len(cities)} cities.")

def load_city_tips(city_tips_json_path):
    city_tips = load_json(city_tips_json_path)
    for ct in city_tips:
        city = City.query.filter_by(city_name=ct['city']).first()
        if city:
            # Join main_spots and tips as strings for db column constraint
            city.main_spots = ', '.join(ct.get('main_spots', []))
            city.tips = '; '.join(ct.get('tips', []))
            db.session.add(city)
    db.session.commit()
    print(f"Updated {len(city_tips)} cities with main_spots and tips.")

def load_weather(weather_json_path):
    weather_data = load_json(weather_json_path)
    for w in weather_data:
        date_obj = datetime.datetime.strptime(w['date'], "%Y-%m-%d").date()
        # Check if a record with the same date and city already exists
        existing_record = WeatherData.query.filter_by(date=date_obj, city=w['city']).first()
        if existing_record:
            existing_record.type = w['type']
            existing_record.temp_min = safe_float(w['temp_min'])
            existing_record.temp_max = safe_float(w['temp_max'])
            existing_record.weather = safe_float(w['weather'])
            existing_record.wind_direction = safe_float(w['wind_direction'])
            existing_record.wind_speed = safe_float(w['wind_speed'])
            existing_record.humidity = safe_float(w['humidity'])
            existing_record.precip_mm = safe_float(w['precip_mm'])
        else:
            wd = WeatherData(
                date=date_obj,
                city=w['city'],
                type=w['type'],
                temp_min=safe_float(w['temp_min']),
                temp_max=safe_float(w['temp_max']),
                weather=safe_float(w['weather']),
                wind_direction=safe_float(w['wind_direction']),
                wind_speed=safe_float(w['wind_speed']),
                humidity=safe_float(w['humidity']),
                precip_mm=safe_float(w['precip_mm'])
            )
            db.session.add(wd)
    db.session.commit()
    print(f"loaded {len(weather_data)} weather records.")

# Load demo users, remove in production
def load_users():
    users = [
        {'username': 'canaan_demo', 'email': 'canaan@example.com', 'password': 'canaandemo'},
        {'username': 'jack_demo', 'email': 'cj@example.com', 'password': 'jackdemo'},
        {'username': 'marcus_demo', 'email': 'marcus@example.com', 'password': 'marcusdemo'}
    ]
    for u in users:
        user = User(username=u['username'], email=u['email'])
        user.set_password(u['password'])
        db.session.merge(user)
    db.session.commit()
    print(f"loaded {len(users)} users.")

if __name__ == "__main__":
    # WARNING: This will delete ALL data in User, City, and WeatherData tables!
    print("WARNING: This db operation will DELETE ALL data in User, City, and WeatherData tables and cannot be undone.")
    confirm = input("Type 'y' to continue: ")
    if confirm.lower() != 'y':
        print("Aborted.")
        exit(0)

    # Location of city and weather feeds JSON files
    city_json = os.path.join('app', 'static', 'chart', 'resources', 'city_lat_lon.json')
    city_tips_json = os.path.join('app', 'static', 'chart', 'resources', 'city_tips.json')
    weather_json = os.path.join('app', 'static', 'chart', 'resources', 'wa_weather_data.json')
    with application.app_context():
    # Clear tables before loading new data
    # Use db.inspect(db.engine).has_table to avoid deprecation warning and ensure compatibility
        inspector = db.inspect(db.engine)
        if inspector.has_table('weather_data'):
            db.session.execute(WeatherData.__table__.delete())
        if inspector.has_table('city'):
            db.session.execute(City.__table__.delete())
        if inspector.has_table('user'):
            db.session.execute(User.__table__.delete())
        db.session.commit()
        # Load data
        load_cities(city_json)
        load_city_tips(city_tips_json)
        load_weather(weather_json)
        load_users()