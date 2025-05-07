from flask import Blueprint, jsonify, request
from .models import WeatherData, City

api_bp = Blueprint('api', __name__)

# API for weather data
@api_bp.route('/api/weather_data')
def get_weather_data():
    data = WeatherData.query.all()
    result = [
        {
            "id": w.id,
            "date": w.date.isoformat(),
            "city": w.city,
            "type": w.type,
            "temp_min": w.temp_min,
            "temp_max": w.temp_max,
            "weather": w.weather,
            "wind_direction": w.wind_direction,
            "wind_speed": w.wind_speed,
            "humidity": w.humidity,
            "precip_mm": w.precip_mm
        }
        for w in data
    ]
    return jsonify(result)

# API for city list and position data
@api_bp.route('/api/city_lat_lon')
def get_city_data():
    data = City.query.all()
    result = [
        {
            "city": c.city_name,
            "lat": c.lat,
            "lon": c.lon
        }
        for c in data
    ]
    return jsonify(result)

# API for city travel tips and main spots
@api_bp.route('/api/travel_tips')
def get_travel_tips():
    city_name = request.args.get('city_name')
    query = City.query
    if city_name:
        query = query.filter_by(city_name=city_name)
    data = query.all()
    result = [
        {
            "city": c.city_name,
            "main_spots": c.main_spots.split(', ') if c.main_spots else [],
            "tips": c.tips.split('; ') if c.tips else []
        }
        for c in data
    ]
    return jsonify(result)
