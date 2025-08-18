import requests
api_key = "a6a068011f76cee8498934e92f557538"
api_url = f"http://api.weatherstack.com/current?access_key={api_key}&query=New York"

def fetch_data():
    print
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        print("Data fetched successfully.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        raise

# fetch_data()

def mock_fetch_data():
   return {'request': {'type': 'City', 'query': 'New York, United States of America', 'language': 'en', 'unit': 'm'}, 'location': {'name': 'New York', 'country': 'United States of America', 'region': 'New York', 'lat': '40.714', 'lon': '-74.006', 'timezone_id': 'America/New_York', 'localtime': '2025-08-14 10:11', 'localtime_epoch': 1755166260, 'utc_offset': '-4.0'}, 'current': {'observation_time': '02:11 PM', 'temperature': 24, 'weather_code': 116, 'weather_icons': ['https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0002_sunny_intervals.png'], 'weather_descriptions': ['Partly Cloudy '], 'astro': {'sunrise': '06:06 AM', 'sunset': '07:55 PM', 'moonrise': '10:34 PM', 'moonset': '12:10 PM', 'moon_phase': 'Waning Gibbous', 'moon_illumination': 75}, 'air_quality': {'co': '425.5', 'no2': '20.905', 'o3': '175', 'so2': '12.025', 'pm2_5': '38.85', 'pm10': '39.035', 'us-epa-index': '2', 'gb-defra-index': '2'}, 'wind_speed': 10, 'wind_degree': 359, 'wind_dir': 'N', 'pressure': 1014, 'precip': 0, 'humidity': 85, 'cloudcover': 0, 'feelslike': 26, 'uv_index': 4, 'visibility': 16, 'is_day': 'yes'}}