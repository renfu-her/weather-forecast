import os
import time
from datetime import datetime
from flask import Flask, render_template, request, flash
import requests
from dotenv import load_dotenv
import urllib3

# Disable SSL warnings for CWA API
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')
application = app

# CWA API configuration
CWA_API_URL = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"
CWA_API_KEY = os.environ.get('CWA_API_KEY')

# Simple in-memory cache with TTL
cache = {}
CACHE_TTL = 300  # 5 minutes

# Taiwan counties/cities list (as used by CWA API)
COUNTIES = [
    "臺北市", "新北市", "桃園市", "臺中市", "臺南市", "高雄市",
    "基隆市", "新竹市", "嘉義市", "新竹縣", "苗栗縣", "彰化縣",
    "南投縣", "雲林縣", "嘉義縣", "屏東縣", "宜蘭縣", "花蓮縣",
    "臺東縣", "澎湖縣", "金門縣", "連江縣"
]

def get_cached_forecast(location):
    """Get forecast from cache if valid, otherwise return None"""
    if location in cache:
        data, timestamp = cache[location]
        if time.time() - timestamp < CACHE_TTL:
            return data
        else:
            del cache[location]
    return None

def cache_forecast(location, data):
    """Cache forecast data with current timestamp"""
    cache[location] = (data, time.time())

def fetch_forecast(location_name):
    """Fetch weather forecast from CWA API"""
    if not CWA_API_KEY:
        return None, "API key not configured"
    
    # Check cache first
    cached_data = get_cached_forecast(location_name)
    if cached_data:
        return cached_data, None
    
    try:
        response = requests.get(
            CWA_API_URL,
            params={
                'Authorization': CWA_API_KEY,
                'locationName': location_name
            },
            timeout=10,
            verify=False  # Bypass SSL verification for CWA API
        )
        
        if response.status_code != 200:
            return None, f"API request failed with status {response.status_code}"
        
        data = response.json()
        
        if not data.get('success'):
            return None, "API returned error"
        
        records = data.get('records', {}).get('location', [])
        if not records:
            return None, "No data found for this location"
        
        # Process and normalize data
        forecast_data = process_forecast_data(records[0])
        cache_forecast(location_name, forecast_data)
        
        return forecast_data, None
        
    except requests.exceptions.RequestException as e:
        return None, f"Network error: {str(e)}"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"

def process_forecast_data(location_data):
    """Process CWA API data into 3 time slots"""
    elements = location_data.get('weatherElement', [])
    
    # Extract data by element type
    data_by_element = {}
    for element in elements:
        element_name = element.get('elementName')
        time_data = element.get('time', [])
        
        if element_name in ['Wx', 'PoP', 'MinT', 'MaxT', 'CI']:
            data_by_element[element_name] = time_data
    
    # Group by time periods (next 3 periods)
    time_slots = []
    for i in range(min(3, len(data_by_element.get('Wx', [])))):
        wx_data = data_by_element.get('Wx', [])[i]
        pop_data = data_by_element.get('PoP', [])[i]
        min_t_data = data_by_element.get('MinT', [])[i]
        max_t_data = data_by_element.get('MaxT', [])[i]
        ci_data = data_by_element.get('CI', [])[i]
        
        time_slot = {
            'start_time': wx_data.get('startTime', ''),
            'end_time': wx_data.get('endTime', ''),
            'weather': wx_data.get('parameter', {}).get('parameterName', ''),
            'weather_code': wx_data.get('parameter', {}).get('parameterValue', ''),
            'pop': pop_data.get('parameter', {}).get('parameterName', '0'),
            'min_temp': min_t_data.get('parameter', {}).get('parameterName', '0'),
            'max_temp': max_t_data.get('parameter', {}).get('parameterName', '0'),
            'comfort': ci_data.get('parameter', {}).get('parameterName', '')
        }
        time_slots.append(time_slot)
    
    return {
        'location': location_data.get('locationName', ''),
        'time_slots': time_slots
    }

@app.route('/')
def index():
    location = request.args.get('location', '')
    forecast_data = None
    error_message = None
    
    if location:
        if location not in COUNTIES:
            error_message = "請選擇有效的縣市"
        else:
            forecast_data, error_message = fetch_forecast(location)
    
    return render_template('index.html', 
                         counties=COUNTIES, 
                         selected_location=location,
                         forecast_data=forecast_data,
                         error_message=error_message,
                         api_key_configured=bool(CWA_API_KEY))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
