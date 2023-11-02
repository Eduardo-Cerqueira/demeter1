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


def fetch_all_production() -> list[str] | Exception:
    """Returns a list of string representing all productions inside the table production.
    If this nothing is found, it will return a single empty array.
    :return: A list of string unit
    :rtype: list[str] | Exception
    """
    try:
        db.execute("SELECT * FROM production")
        return db.fetchall()
    except Exception as error:
        return error


def fetch_production_by_code(code: str) -> list[str] | Exception:
    """Returns a list of string representing a production filtered by the code field inside the table production.
    If this nothing is found, it will return a single empty array.
    :return: A list of string unit
    :rtype: list[str] | Exception
    """
    try:
        db.execute("SELECT * FROM production WHERE code = %s", [code])
        return db.fetchone()
    except Exception as error:
        return error


def insert_production(unit: str, name: str) -> None | Exception:
    """Insert production row into table production.
    :parameter unit:
    :parameter name:
    :return: Nothing or an error
    :rtype: None | Exception
    """
    try:
        db.execute("INSERT INTO production(unit, name) VALUES(%s,%s)", [unit, name])
        print(type(db.lastrowid))
    except Exception as error:
        return error
    finally:
        conn.commit()


def update_production(unit: str, name: str) -> None | Exception:
    """
    Update production row using his code field to filter from table production.
    :parameter unit:
    :parameter name:
    :return: Nothing or an error
    :rtype: None | Exception
    """
    try:
        db.execute(
            "UPDATE production SET unit = %s, name = %s WHERE code = %s", [unit, name]
        )
    except Exception as error:
        return error
    finally:
        conn.commit()


def delete_production(code: str) -> None | Exception:
    """
    Delete production row using his code field to filter from table production.
    :parameter code:
    :return: Nothing or an error
    :rtype: None | Exception
    """
    try:
        db.execute("DELETE FROM production WHERE code = %s", [code])
    except Exception as error:
        return error
    finally:
        conn.commit()
