from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from crud import create_tables, add_weather, add_sale
from fetch_weather import get_today_weather, validate_weather_data, generate_mock_sales

def run_etl():
    create_tables()
    weather = get_today_weather()
    if not validate_weather_data(weather):
        print("Validation failed.")
        return
    sales = generate_mock_sales(weather['temp_c'], weather['precip_mm'])
    add_weather(**weather)
    add_sale(weather['date'], sales['store_id'], sales['umbrellas'], sales['cold_drinks'])

default_args = {
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

with DAG(
    dag_id='weather_sales_etl',
    schedule='@daily',
    default_args=default_args,
    catchup=False
) as dag:
    extract_load = PythonOperator(
        task_id='run_weather_sales_etl',
        python_callable=run_etl,
    )
