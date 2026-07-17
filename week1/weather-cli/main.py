import requests

weather_codes = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    61: "Rain",
    71: "Snow",
    95: "Thunderstorm"
}

city = input("Enter your city name: ")
try: 
    response = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1")
except requests.exceptions.ConnectionError:
    print("No Internet Connection")
    exit(0)

data = response.json()

if "results" not in data or not data["results"]:
    print("Inavlid City name or city not found")
    exit(0)

location = data["results"]

latitude = location[0]["latitude"]
longitude = location[0]["longitude"]

try:
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,weathercode,windspeed_10m")
except requests.exceptions.ConnectionError:
    print("No Internet Connection")
    exit(0)

current_weather = response.json()["current"]

print(f"City Name: {location[0]["name"]}\nTemperature: {current_weather["temperature_2m"]}°C\nWind Speed: {current_weather["windspeed_10m"]}km/h\nWeather Condition: {weather_codes.get(current_weather["weathercode"], "Unknown condition")}")
