from typing import Any

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


def fetch_all_production() -> list[tuple[Any, ...]] | Exception:
    """Returns a list of string representing all productions inside the table production.
    If this nothing is found, it will return a single empty array.
    :return: A list of tuples containing multiples production objects
    :rtype: list[tuple[str]] | Exception
    """
    try:
        db.execute("SELECT * FROM production")
        return db.fetchall()
    except Exception as error:
        return error


def fetch_production_by_code(code: int) -> tuple[Any, ...] | None | Exception:
    """Returns a list of string representing a production filtered by the code field inside the table production.
    If this nothing is found, it will return a single empty array.
    :return: A list of tuples containing a production object
    :rtype: list[tuple[str]] | Exception
    """
    try:
        db.execute("SELECT * FROM production WHERE code = %s", [code])
        return db.fetchone()
    except Exception as error:
        return error


def insert_production(code: int, unit: str, name: str) -> None | Exception:
    """Insert production into table production.
    :parameter code:
    :parameter unit:
    :parameter name:
    :return: Nothing or an error
    :rtype: None | Exception
    """
    try:
        db.execute(
            "INSERT INTO production(code, unit, name) VALUES(%s,%s,%s)",
            [code, unit, name],
        )
    except Exception as error:
        return error
    finally:
        conn.commit()


def update_production(
    code: int, new_code: int, new_unit: str, new_name: str
) -> None | Exception:
    """
    Update production row using his code field to filter from table production.
    :parameter code:
    :parameter new_unit:
    :parameter new_name:
    :return: Nothing or an error
    :rtype: None | Exception
    """
    try:
        db.execute(
            "UPDATE production SET code = %s, unit = %s, name = %s WHERE code = %s",
            [new_code, new_unit, new_name, code],
        )
    except Exception as error:
        return error
    finally:
        conn.commit()


def partial_update_production(
    code: int, new_code: int, new_unit: str, new_name: str
) -> None | Exception:
    """Partially update production row using his code field to filter from table unit.
    :parameter code:
    :parameter new_code:
    :parameter new_unit:
    :parameter new_name:
    :return: Nothing or an error
    :rtype: None | Exception
    """
    try:
        db.execute(
            "UPDATE production SET code = COALESCE(%s, code), unit = COALESCE(%s, unit), "
            "name = COALESCE(%s, name) WHERE code = %s",
            [new_code, new_unit, new_name, code],
        )
    except Exception as error:
        return error
    finally:
        conn.commit()


def delete_production(code: int) -> None | Exception:
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
