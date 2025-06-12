from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from crud import create_tables, add_weather, add_sale
from fetch_weather import get_today_weather, validate_weather_data, generate_mock_sales
from airflow.sdk import Variable
import os

def run_etl():
    print("Running etl")
    create_tables()
    API_KEY = os.getenv("WEATHER_API_KEY")
    weather = get_today_weather(API_KEY)
    if not validate_weather_data(weather):
        print("Validation failed.")
        return
    sales = generate_mock_sales(weather['temp_c'], weather['precip_mm'])
    add_weather(**weather)
    add_sale(weather['date'], sales['store_id'], sales['umbrellas'], sales['cold_drinks'])

default_args = {
    'description': 'A DAG to extract the data about weather and sales',
    'start_date': datetime(2024, 1, 1),
    'catchup': False,
}

with DAG(
    dag_id='weather_sales_etl',
    schedule=timedelta(minutes = 30),
    default_args=default_args,
) as dag:
    extract_load = PythonOperator(
        task_id='run_weather_sales_etl',
        python_callable=run_etl,
    )
