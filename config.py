import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

OMDB_API_KEY = os.getenv("OMDB_API_KEY")

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Hemasri@1234"
DB_NAME = "MovieTicketBookingDB"


def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )