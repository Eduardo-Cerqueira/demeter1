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


def count_logs() -> tuple[int, ...] | Exception:
    """Returns number representing the number of all logs inside the table log.
    :return: A number containing the number of logs
    :rtype: tuple[int, ...] | Exception
    """
    try:
        db.execute("Count(*) FROM log")
        return db.fetchone()
    except Exception as error:
        return error


def insert_log(log: str) -> None | Exception:
    """Insert log into table log.
    :parameter log:
    :return: Nothing or an error
    :rtype: None | Exception
    """
    try:
        db.execute("INSERT INTO log(log) VALUES(%s)", [log])
    except Exception as error:
        return error
    finally:
        conn.commit()

