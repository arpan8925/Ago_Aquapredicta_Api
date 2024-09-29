import requests

# Your OpenWeatherMap API Key
API_KEY = "9e3022f865218f4d3f8780a1db8832b0"

# Define temperature thresholds for crops (these are just examples, adjust as needed)
RISKY_HIGH_TEMP = 35  # Degrees Celsius (high-risk temperature for low-temp crops)
RISKY_LOW_TEMP = 5    # Degrees Celsius (low-risk temperature for low-temp crops)

# Helper function to get location
def get_location():
    try:
        response = requests.get("https://ipinfo.io/")
        data = response.json()
        location = data['loc'].split(',')
        lat, lon = location[0], location[1]
        return lat, lon
    except Exception as e:
        print("Error getting location:", e)
        return None, None

# Function to get current weather data
def fetch_current_weather(lat, lon):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
        response = requests.get(url)
        data = response.json()
        if data['cod'] == 200:
            weather_data = {
                "city": data['name'],
                "weather_description": data['weather'][0]['description'],
                "temperature": data['main']['temp'],
                "humidity": data['main']['humidity']
            }
            return weather_data
        else:
            return {"error": "Unable to fetch weather data."}
    except Exception as e:
        return {"error": str(e)}

# Function to get weather forecast and crop risk analysis
def fetch_weather_forecast(lat, lon):
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

                # Check for rain in forecast
                if 'rain' in forecast and rain_forecast is None:
                    rain_forecast = dt_txt

                # Check for risky temperatures for crops
                if temp >= RISKY_HIGH_TEMP or temp <= RISKY_LOW_TEMP:
                    risky_temperature_dates.append({"date": dt_txt, "temperature": temp})

            days_count = len(forecasted_days)

            response_data = {
                "forecast_days_count": days_count,
                "next_rainfall": rain_forecast if rain_forecast else f"No rainfall expected in the next {days_count} days.",
                "risky_temperatures": risky_temperature_dates if risky_temperature_dates else f"No risky temperatures for crops expected in the next {days_count} days."
            }

            return response_data
        else:
            return {"error": "Unable to fetch forecast data."}
    except Exception as e:
        return {"error": str(e)}
