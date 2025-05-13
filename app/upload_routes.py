import csv
import datetime
import subprocess
import sys
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from app.models import db, WeatherData  # Assuming WeatherData is the model for storing weather data
from flask_socketio import emit
from app import socketio

# Define a blueprint for upload-related routes
upload_bp = Blueprint('upload', __name__)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/upload_csv', methods=['POST'])
def upload_file():
    """Handle the upload of a CSV file."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        try:
            # Read and verify the CSV data
            csv_data = file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(csv_data)
            print(f"CSV Headers: {reader.fieldnames}")
            if not verify_csv_format(reader):
                return jsonify({'error': 'Invalid CSV format'}), 400

            # Insert data into the database
            insert_data_into_db(reader)
            return jsonify({'message': f'File {filename} uploaded and processed successfully'}), 200
        except Exception as e:
            return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Invalid file type. Only CSV files are allowed'}), 400


@socketio.on('run_getweather')
def handle_run_getweather():
    process = subprocess.Popen(
        [sys.executable, '-u', 'app/GetWeather.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        universal_newlines=True
    )
    for line in iter(process.stdout.readline, ''):
        emit('getweather_output', {'data': line.rstrip()})
    process.stdout.close()
    process.wait()
    emit('getweather_output', {'data': '[GetWeather.py finished]'})

def verify_csv_format(reader):
    """Verify the format of the CSV file."""
    required_columns = {
        'date', 'city', 'type', 'temp_min', 'temp_max', 
        'weather', 'wind_direction', 'wind_speed', 
        'humidity', 'precip_mm'
    }
    if not set(reader.fieldnames).issuperset(required_columns):
        return False
    return True

def safe_float(value):
    # Note： !!!All invalid values will be converted to 0.0!!!
    """Convert value to float, return 0.0 if empty or invalid."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

def insert_data_into_db(reader):
    """Insert the CSV data into the database, overriding existing records for the same date and city."""
    for row in reader:
        # Convert date string to a Python date object
        date_obj = datetime.datetime.strptime(row['date'], "%Y-%m-%d").date()
        # Check if a record with the same date and city already exists
        existing_record = WeatherData.query.filter_by(date=date_obj, city=row['city']).first()
        if existing_record:
            # Update the existing record
            existing_record.type = row['type']
            existing_record.temp_min = safe_float(row['temp_min'])
            existing_record.temp_max = safe_float(row['temp_max'])
            existing_record.weather = safe_float(row['weather'])
            existing_record.wind_direction = safe_float(row['wind_direction'])
            existing_record.wind_speed = safe_float(row['wind_speed'])
            existing_record.humidity = safe_float(row['humidity'])
            existing_record.precip_mm = safe_float(row['precip_mm'])
        else:
            # Create a new WeatherData object for the row
            weather_data = WeatherData(
                date=date_obj,
                city=row['city'],
                type=row['type'],
                temp_min=safe_float(row['temp_min']),
                temp_max=safe_float(row['temp_max']),
                weather=safe_float(row['weather']),
                wind_direction=safe_float(row['wind_direction']),
                wind_speed=safe_float(row['wind_speed']),
                humidity=safe_float(row['humidity']),
                precip_mm=safe_float(row['precip_mm'])
            )
            db.session.add(weather_data)
    db.session.commit()