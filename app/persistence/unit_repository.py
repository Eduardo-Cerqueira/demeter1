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


def fetch_all_unit() -> list[str] | Exception:
    """Returns a list of string representing all units inside the table unit.
    If this nothing is found, it will return a single empty array.
    :return: A list of string unit
    :rtype: list[str] | Exception
    """
    try:
        db.execute("SELECT * FROM unit")
        return db.fetchall()
    except Exception as error:
        return error


def fetch_unit_by_unit(unit: str) -> list[str] | Exception:
    """Returns a list of string representing a unit filtered by the unit field inside the table unit.
    If this nothing is found, it will return a single empty array.
    :return: A list of string unit
    :rtype: list[str] | Exception
    """
    try:
        db.execute("SELECT * FROM unit WHERE unit = %s", [unit])
        return db.fetchone()
    except Exception as error:
        return error


def insert_unit(unit: str) -> None | Exception:
    """Insert unit into table unit.
    :parameter unit:
    :return: Nothing or an error
    :rtype: None | Exception
    """
    try:
        db.execute("INSERT INTO unit(unit) VALUES(%s)", [unit])
        print(type(db.lastrowid))
    except Exception as error:
        return error
    finally:
        conn.commit()


def update_unit(unit_value: str, unit: str) -> None | Exception:
    """
    Update unit field using his unit field to filter from table unit.
    :parameter unit_value:
    :parameter unit:
    :return: Nothing or an error
    :rtype: None | Exception
    """
    try:
        db.execute("UPDATE unit SET unit = %s WHERE unit = %s", [unit_value, unit])
    except Exception as error:
        return error
    finally:
        conn.commit()


def delete_unit(unit: str) -> None | Exception:
    """
    Delete unit field using his unit field to filter from table unit.
    :parameter unit:
    :return: Nothing or an error
    :rtype: None | Exception
    """
    try:
        db.execute("DELETE FROM unit WHERE unit = %s", [unit])
    except Exception as error:
        return error
    finally:
        conn.commit()
