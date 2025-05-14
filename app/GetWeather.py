import requests
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.upload_routes import insert_data_into_db
import csv
from app import create_app
from app.config import DevelopmentConfig

# Define cities around WA
city_coords = [
    {"city": "Perth", "lat": -31.9505, "lon": 115.8605},
    {"city": "Geraldton", "lat": -28.7682, "lon": 114.6144},
    {"city": "Carnarvon", "lat": -24.8802, "lon": 113.6576},
    {"city": "Margaret River", "lat": -33.9530, "lon": 115.0731},
    {"city": "Busselton", "lat": -33.6525, "lon": 115.3455},
    {"city": "Bunbury", "lat": -33.3271, "lon": 115.6414},
    {"city": "Albany", "lat": -35.0228, "lon": 117.8814},
    {"city": "Denmark", "lat": -34.9614, "lon": 117.3530},
    {"city": "Esperance", "lat": -33.8613, "lon": 121.8896},
    {"city": "Manjimup", "lat": -34.2414, "lon": 116.1462},
    {"city": "Collie", "lat": -33.3624, "lon": 116.1519},
    {"city": "Narrogin", "lat": -32.9335, "lon": 117.1786},
    {"city": "Katanning", "lat": -33.6918, "lon": 117.5528},
    {"city": "Kalgoorlie", "lat": -30.7489, "lon": 121.4650},
    {"city": "Augusta", "lat": -34.3115, "lon": 115.1595},
    {"city": "Lancelin", "lat": -31.0176, "lon": 115.3303},
    {"city": "Kellerberrin", "lat": -31.6333, "lon": 117.7167},
    {"city": "Hyden", "lat": -32.4417, "lon": 118.8586},
    {"city": "Northcliffe", "lat": -34.6380, "lon": 116.1255},
    {"city": "Hopetoun", "lat": -33.9500, "lon": 120.1269}
]


# Date range
today = date.today()
start_date = (today - relativedelta(months=2)).isoformat()
end_date = today.isoformat()

# Daily weather fields to fetch
params_common = {
    "daily": (
        "temperature_2m_min,temperature_2m_max,weathercode,"
        "winddirection_10m_dominant,windspeed_10m_max,"
        "precipitation_sum,relative_humidity_2m_mean"
    ),
    "timezone": "Australia/Perth"
}

all_data = []

for city in city_coords:
    print(f"Fetching data for {city['city']}...", flush=True)

    try:
        # --- Historical ---
        hist_url = "https://archive-api.open-meteo.com/v1/archive"
        hist_params = {
            "latitude": city["lat"],
            "longitude": city["lon"],
            "start_date": start_date,
            "end_date": end_date,
            **params_common
        }

        r_hist = requests.get(hist_url, params=hist_params)
        hist_json = r_hist.json()

        if "daily" not in hist_json or "time" not in hist_json["daily"]:
            print(f"Skipping {city['city']} - historical data incomplete", flush=True)
            continue

        df_hist = pd.DataFrame(hist_json['daily'])
        df_hist['city'] = city["city"]
        df_hist['type'] = "historical"

        # --- Forecast ---
        forecast_url = "https://api.open-meteo.com/v1/forecast"
        forecast_params = {
            "latitude": city["lat"],
            "longitude": city["lon"],
            **params_common
        }

        r_forecast = requests.get(forecast_url, params=forecast_params)
        forecast_json = r_forecast.json()

        if "daily" not in forecast_json or "time" not in forecast_json["daily"]:
            print(f"Skipping {city['city']} - forecast data incomplete", flush=True)
            continue

        df_forecast = pd.DataFrame(forecast_json['daily'])
        df_forecast['city'] = city["city"]
        df_forecast['type'] = "forecast"

        # Combine
        combined = pd.concat([df_hist, df_forecast], ignore_index=True)
        combined = combined.rename(columns={"time": "date"})  
        all_data.append(combined)

    except Exception as e:
        print(f"Error fetching {city['city']}: {e}, flush=True")

# Combine all cities
final_df = pd.concat(all_data, ignore_index=True)

# Rename and reorder columns
final_df = final_df.rename(columns={
    "temperature_2m_min": "temp_min",
    "temperature_2m_max": "temp_max",
    "weathercode": "weather",
    "winddirection_10m_dominant": "wind_direction",
    "windspeed_10m_max": "wind_speed",
    "precipitation_sum": "precip_mm",
    "relative_humidity_2m_mean": "humidity"
})
final_df = final_df[[
    "date", "city", "type",
    "temp_min", "temp_max", "weather",
    "wind_direction", "wind_speed", "humidity", "precip_mm"
]]

# Remove rows where all weather values are empty
weather_columns = ["temp_min", "temp_max", "weather", "wind_direction", 
                  "wind_speed", "humidity", "precip_mm"]
final_df = final_df.dropna(subset=weather_columns, how='all')

# Generate file names using current timestamp
timestamp = date.today().strftime("%Y%m%d")
csv_file_path = os.path.join("app", "static", "chart", "resources", "weathersync", f"wa_weather_data_{timestamp}.csv")
json_file_path = os.path.join("app", "static", "chart", "resources", "weathersync", f"wa_weather_data_{timestamp}.json")

# Save to CSV and JSON
os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
final_df.to_csv(csv_file_path, index=False)
final_df.to_json(json_file_path, orient="records", date_format="iso")

print(" Latest Weather Data csv and json from -60 Days to + 7 Days are saved to server for backup", flush=True)

# --- Execute upload logic ---
application = create_app(config=DevelopmentConfig)
with application.app_context():
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        insert_data_into_db(reader)
print(" Weather data uploaded to database.", flush=True)