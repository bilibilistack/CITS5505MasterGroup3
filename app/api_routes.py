from flask import Blueprint, jsonify
from .models import WeatherData, City

api_bp = Blueprint('api', __name__)

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
