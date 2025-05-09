from flask import Blueprint, jsonify, request, session, abort
from .models import WeatherData, City, Share
from app import db

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

# API to update is_read, is_deleted, is_favorite for a Share
@api_bp.route('/api/share/<int:share_id>/update_flags', methods=['POST'])
def update_share_flags(share_id):
    share = Share.query.get_or_404(share_id)
    # Get current user ID from session to avoid unauthorized modification
    user_id = session.get('user_id')
    if user_id is None or share.shared_to != user_id:
        abort(403, description="You are not authorized to update this share message.")
    data = request.get_json()
    if 'is_read' in data:
        share.is_read = bool(data['is_read'])
    if 'is_deleted' in data:
        share.is_deleted = bool(data['is_deleted'])
    if 'is_favorite' in data:
        share.is_favorite = bool(data['is_favorite'])
    db.session.commit()
    return jsonify({
        "success": True,
        "share_id": share.id,
        "is_read": share.is_read,
        "is_deleted": share.is_deleted,
        "is_favorite": share.is_favorite
    })

@api_bp.route('/unread', methods=['GET'])
def unread():
    """
    Get count of unread
    """
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"success": False, "message": "User not logged in."}), 401

    unread_count = db.session.query(Share).filter(
        Share.shared_to == user_id,
        ((Share.is_read == 0)),
        (Share.is_deleted == 0)  
    ).count()

    return jsonify({
        "unread_count": unread_count
    })