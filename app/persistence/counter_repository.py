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


def fetch_counter_by_tag_route(route: str, tag: str) -> tuple[Any, ...] | None | Exception:
    """Returns a list of string representing a counter filtered by the tag and route fields inside the table counter.
    If this nothing is found, it will return a single empty array.
    :return: A list of tuples containing counter
    :rtype: list[tuple[str]] | Exception
    """
    try:
        db.execute("SELECT * FROM counter WHERE route = %s AND tag = %s", [route, tag])
        return db.fetchone()
    except Exception as error:
        return error


def insert_counter(route: str, tag: str, count: int) -> None | Exception:
    """Insert count into table counter.
    :parameter route:
    :parameter tag:
    :parameter count:
    :return: Nothing or an error
    :rtype: None | Exception
    """
    try:
        db.execute("INSERT INTO counter(route, tag, count) VALUES(%s,%s,%s)", [route, tag, count])
    except Exception as error:
        return error
    finally:
        conn.commit()


def update_counter_count(route: str, tag: str, count: int) -> None | Exception:
    """
    Update count field using his route and tag fields to filter from table counter.
    :parameter route:
    :parameter tag:
    :parameter count:
    :return: Nothing or an error
    :rtype: None | Exception
    """
    try:
        db.execute("UPDATE counter SET count = %s WHERE route = %s AND tag = %s", [count, route, tag])
    except Exception as error:
        return error
    finally:
        conn.commit()
