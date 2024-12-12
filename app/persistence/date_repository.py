import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

database_host = os.getenv("DATABASE_HOST")
database_port = os.getenv("DATABASE_PORT")
database_name = os.getenv("DATABASE_NAME")
database_user = os.getenv("DATABASE_USER")
database_password = os.getenv("DATABASE_PASSWORD")

conn = psycopg2.connect(
    database=database_name,
    host=database_host,
    user=database_user,
    password=database_password,
    port=database_port,
)

db = conn.cursor()


def get_date():
    """
    Get all dates in the database.

    :return: A list of all dates.
    """
    db.execute("SELECT * FROM date")
    return db.fetchall()


def get_date_by_id(date):
    """
    Get a date by his date.

    :param (date) date: The date identifier.
    :return: A tuple with the date's data.
    """
    db.execute("SELECT * FROM date WHERE date = %s", (date,))
    return db.fetchone()


def date(date):
    """
    Create a new date in the database.

    :param (date) date: the date

    """
    db.execute("INSERT INTO date(date) VALUES(%s)", (date,))
    conn.commit()


def update_date(date):
    """
    Update date information

    :param (date) date: The date to update.
    """
    db.execute("UPDATE date SET date = %s, date = %s WHERE date = %s", (date,))
    conn.commit()


def delete_date(date):
    """
    Delete a date

    :param (date) date: The date to delete.
    """
    db.execute("DELETE FROM date WHERE date = %s", (date,))
    conn.commit()


db.close()
conn.close()
