import requests
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv(dotenv_path='secrets.env')

API_KEY = os.getenv("WEATHER_API_KEY")
LOCATION = "Lisbon"
# url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"

def fetch_past_weather(days=7):
    base_url = "http://api.weatherapi.com/v1/history.json"
    today = datetime.today()
    weather_rows = []

    for i in range(1):
        date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        response = requests.get(base_url, params={
            "key": API_KEY,
            "q": LOCATION,
            "dt": date
        })

        if response.status_code == 200:
            data = response.json()
            print(data)
            day_data = data["forecast"]["forecastday"][0]["day"]
            weather_rows.append({
                "date": date,
                "avg_temp_c": day_data["avgtemp_c"],
                "precip_mm": day_data["totalprecip_mm"],
                "condition": day_data["condition"]["text"]
            })
        else:
            print("Error on", date, response.status_code)

    # df = pd.DataFrame(weather_rows)
    # df.to_csv("data/weather_data.csv", index=False)
    print("Saved weather data.")
    
if __name__ == "__main__":
    fetch_past_weather()
