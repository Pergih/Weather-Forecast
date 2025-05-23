import requests
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import numpy as np
import random
from crud import *

load_dotenv(dotenv_path='secrets.env')

API_KEY = os.getenv("WEATHER_API_KEY")
LOCATION = "Lisbon"
# url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"

def get_today_weather():
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={LOCATION}"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200:
        current = data['current']

        weather_entry = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "location": LOCATION,
            "temp_c": current['temp_c'],
            "humidity": current['humidity'],
            "precip_mm": current['precip_mm'],
            "wind_kph": current['wind_kph'],
            "api_timestamp": current['last_updated']
        }
        return weather_entry
    else:
        print("Error on", response.status_code)

def generate_mock_sales(temp_c, precip_mm):
    umbrellas = random.randint(10, 30) if precip_mm > 1 else random.randint(0, 10)
    cold_drinks = random.randint(20, 50) if temp_c > 20 else random.randint(5, 15)

    return {
        "store_id": "StoreA",
        "umbrellas": umbrellas,
        "cold_drinks": cold_drinks
    }

def run_pipeline():
    create_tables()
    weather = get_today_weather()
    sales = generate_mock_sales(weather['temp_c'], weather['precip_mm'])

    # Insert data
    add_weather(**weather)
    add_sale(weather['date'], sales['store_id'], sales['umbrellas'], sales['cold_drinks'])

    print("✅ Pipeline run completed.")

    
if __name__ == "__main__":
    run_pipeline()
