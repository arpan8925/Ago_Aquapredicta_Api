from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

API_KEY = "9e3022f865218f4d3f8780a1db8832b0"  

# Ekta Risky Temp Declare kore disi Age theke
RISKY_HIGH_TEMP = 35  
RISKY_LOW_TEMP = 5  

def get_location():
    try:
        response = requests.get("https://ipinfo.io/")
        if response.status_code != 200:
            return None, None, f"Error fetching location: {response.status_code}"
        data = response.json()
        location = data.get('loc', None)
        if location:
            lat, lon = location.split(',')
            return lat, lon, None
        else:
            return None, None, "Error: No 'loc' field in response from IP geolocation."
    except Exception as e:
        return None, None, f"Error getting location: {str(e)}"


@app.route('/current-weather', methods=['GET'])
def current_weather():
    lat, lon, error = get_location()
    if error or not lat or not lon:
        return jsonify({"error": error or "Unable to fetch location."}), 400
    
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
        response = requests.get(url)
        data = response.json()
        if data['cod'] == 200:
            weather_desc = data['weather'][0]['description']
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            city = data['name']
            return jsonify({
                "city": city,
                "weather_description": weather_desc,
                "temperature": temperature,
                "humidity": humidity
            })
        else:
            return jsonify({"error": "Unable to fetch weather data."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/weather-forecast', methods=['GET'])
def weather_forecast():
    lat, lon, error = get_location()
    if error or not lat or not lon:
        return jsonify({"error": error or "Unable to fetch location."}), 400

    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
        response = requests.get(url)
        data = response.json()
        if data['cod'] == "200":
            forecast_list = data['list']
            rain_forecast = None
            risky_temperature_dates = []
            forecasted_days = set()

            for forecast in forecast_list:
                temp = forecast['main']['temp']
                dt_txt = forecast['dt_txt']
                forecast_date = dt_txt.split(" ")[0]
                forecasted_days.add(forecast_date)
                

                if 'rain' in forecast and rain_forecast is None:
                    rain_forecast = dt_txt


                if temp >= RISKY_HIGH_TEMP or temp <= RISKY_LOW_TEMP:
                    risky_temperature_dates.append({"date": dt_txt, "temperature": temp})

            days_count = len(forecasted_days)
            
            response_data = {
                "forecast_days_count": days_count,
                "next_rainfall": rain_forecast if rain_forecast else f"No rainfall expected in the next {days_count} days.",
                "risky_temperatures": risky_temperature_dates if risky_temperature_dates else f"No risky temperatures for crops expected in the next {days_count} days."
            }

            return jsonify(response_data)
        else:
            return jsonify({"error": "Unable to fetch forecast data."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
