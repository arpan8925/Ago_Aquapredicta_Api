## API Endpoints

### 1. Get Current Weather
- **Endpoint:** `/current-weather`
- **Method:** `GET`
- **Description:** Fetches the current weather, temperature, humidity, and city name based on the user's IP.
- **Response Example:**
    ```json
    {
      "city": "New York",
      "weather_description": "clear sky",
      "temperature": 25.5,
      "humidity": 60
    }
    ```

### 2. Get Weather Forecast & Crop Risk Analysis
- **Endpoint:** `/weather-forecast`
- **Method:** `GET`
- **Description:** Provides a 5-day weather forecast and highlights risky temperature conditions for crops.
- **Response Example:**
    ```json
    {
      "forecast_days_count": 5,
      "next_rainfall": "Next rainfall expected on: 2023-09-30 12:00:00",
      "risky_temperatures": [
        {
          "date": "2023-09-30 12:00:00",
          "temperature": 36.5
        },
        {
          "date": "2023-09-30 18:00:00",
          "temperature": 4.2
        }
      ]
    }
    ```
- **Fields:**
  - `forecast_days_count`: Number of days in the forecast data.
  - `next_rainfall`: Date and time of the next expected rainfall, or a message if no rain is expected.
  - `risky_temperatures`: List of dates and temperatures that are risky for crops, based on predefined thresholds.
