
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def fetch_weather_data(city):
    api_key = "f7dafa0d5a6f4fa287d21542250510"
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        return {
            "city": data['location']['name'],
            "region": data['location']['region'],
            "country": data['location']['country'],
            "time_zone": data['location']['tz_id'],
            "local_time": data['location']['localtime'],
            "temp_in_c": data['current']['temp_c'],
            "condition": data['current']['condition']['text'],
            "wind_speed": data['current']['wind_kph'],
            "humidity": data['current']['humidity'],
            "feel_temp": data['current']['feelslike_c']
        }
    else:
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None
    if request.method == "POST":
        city_name = request.form["city"]
        weather = fetch_weather_data(city_name)
        if not weather:
            error = "Failed to fetch weather data. Please check the city name or try again later."
    return render_template("index.html", weather=weather, error=error)

if __name__ == "__main__":
    app.run(debug=True)