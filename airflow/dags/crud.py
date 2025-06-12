import psycopg2

def get_connection():
    return psycopg2.connect(
        host="postgres",       # or "postgres" if using Docker and Airflow
        database="weather_db",
        user="weather_user",
        password="weather_pass",
        port=5432
    )


def create_tables():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather_data (
                id SERIAL PRIMARY KEY,
                date DATE NOT NULL,
                location TEXT,
                temp_c REAL,
                humidity REAL,
                precip_mm REAL,
                wind_kph REAL,
                api_timestamp TIMESTAMP NOT NULL
            );
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales_data (
                id SERIAL PRIMARY KEY,
                date DATE NOT NULL,
                store_id TEXT,
                umbrellas INTEGER,
                cold_drinks INTEGER
            );
        ''')

# --- WEATHER_DATA ---
# --- WEATHER_DATA ---
def add_weather(date, location, temp_c, humidity, precip_mm, wind_kph, api_timestamp):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO weather_data (date, location, temp_c, humidity, precip_mm, wind_kph, api_timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (date, location, temp_c, humidity, precip_mm, wind_kph, api_timestamp))
        conn.commit()

def read_weather():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM weather_data")
        return cursor.fetchall()

def update_weather(id, temp_c=None, humidity=None):
    with get_connection() as conn:
        cursor = conn.cursor()
        if temp_c is not None:
            cursor.execute("UPDATE weather_data SET temp_c = %s WHERE id = %s", (temp_c, id))
        if humidity is not None:
            cursor.execute("UPDATE weather_data SET humidity = %s WHERE id = %s", (humidity, id))
        conn.commit()

def delete_weather(id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM weather_data WHERE id = %s", (id,))
        conn.commit()

# --- SALES_DATA ---
def add_sale(date, store_id, umbrellas, cold_drinks):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO sales_data (date, store_id, umbrellas, cold_drinks)
            VALUES (%s, %s, %s, %s)
        """, (date, store_id, umbrellas, cold_drinks))
        conn.commit()

def read_sales():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sales_data")
        return cursor.fetchall()

def update_sale(id, umbrellas=None, cold_drinks=None):
    with get_connection() as conn:
        cursor = conn.cursor()
        if umbrellas is not None:
            cursor.execute("UPDATE sales_data SET umbrellas = %s WHERE id = %s", (umbrellas, id))
        if cold_drinks is not None:
            cursor.execute("UPDATE sales_data SET cold_drinks = %s WHERE id = %s", (cold_drinks, id))
        conn.commit()

def delete_sale(id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sales_data WHERE id = %s", (id,))
        conn.commit()