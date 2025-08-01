import psycopg2
from psycopg2 import Error
import uuid
from datetime import datetime, date

db_config = {
    'host': 'localhost',
    'database': 'school_management',  # <-- Updated database name
    'user': 'postgres',
    'password': '12345',
    'port': 5432
}


def get_db_connection():
    conn = None
    try:
        conn = psycopg2.connect(**db_config)
        return conn
    except Error as e:
        print(f"Error connecting to PostgreSQL database: {e}")
        return None


# insert_new_tenant(
#     tenant_name="Python Test School",
#     address="123 Script Lane",
#     city="Pokhara",
#     country="Nepal",
#     email="pythonschool@test.com",
#     established_date=date(2024, 3, 15)
# )
