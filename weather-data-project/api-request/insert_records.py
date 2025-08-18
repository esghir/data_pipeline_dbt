import psycopg2
from api_request import mock_fetch_data,fetch_data

def connect_to_db():
    print("connecting to the postgreSQL database...")
    try:
        conn = psycopg2.connect(
            host="db",
            port="5432",
            dbname="db",
            user="db_user",
            password="db_password",
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        raise

def create_table(conn):
    print("Creating table if not exists...")
    try:
        cursor = conn.cursor()
        cursor.execute("""
                        create schema if not exists dev;
                        create table if not exists dev.raw_weather_data (
                            id serial primary key,
                            city TEXT,
                            temperature FLOAT,
                            weather_description text,
                            wind_spead float,
                            time timestamp,
                            inserted_at TIMESTAMP DEFAULT NOW(),
                            utc_offset text
                       );

                       """)
        conn.commit()
        print("table was created .")

    except psycopg2.Error as e:
        print(f"Error creating table: {e}")
        raise


def insert_records(conn,data):
    print("Inserting weather data Into the database...")
    try:
        weather = data['current']
        location = data['location']
        cursor = conn.cursor()
        cursor.execute("""
                        INSERT INTO dev.raw_weather_data (city, temperature, weather_description, wind_spead, time,inserted_at, utc_offset)
                        VALUES (%s, %s, %s, %s,%s, NOW(), %s);
                        """,
                       (data['location']['name'],
                        weather['temperature'],
                        weather['weather_descriptions'][0],
                        weather['wind_speed'],
                        location['localtime'],
                        location['utc_offset']))
        conn.commit()
        print("Data inserted successfully.")
    except psycopg2.Error as e:
        print(f"Error inserting data: {e}")
        raise

def main():
    try:
        # data = mock_fetch_data()
        data = fetch_data()
        conn = connect_to_db()
        create_table(conn)
        insert_records(conn, data)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

main()