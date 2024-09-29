from flask import Flask, jsonify
from weather_api import get_location, fetch_current_weather, fetch_weather_forecast

app = Flask(__name__)

# Endpoint to get current weather
@app.route('/current-weather', methods=['GET'])
def current_weather():
    lat, lon = get_location()
    if not lat or not lon:
        return jsonify({"error": "Unable to fetch location."}), 400
    
    weather_data = fetch_current_weather(lat, lon)
    if "error" in weather_data:
        return jsonify({"error": weather_data["error"]}), 500
    return jsonify(weather_data)

# Endpoint to get weather forecast and crop risk analysis
@app.route('/weather-forecast', methods=['GET'])
def weather_forecast():
    lat, lon = get_location()
    if not lat or not lon:
        return jsonify({"error": "Unable to fetch location."}), 400
    
    forecast_data = fetch_weather_forecast(lat, lon)
    if "error" in forecast_data:
        return jsonify({"error": forecast_data["error"]}), 500
    return jsonify(forecast_data)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
