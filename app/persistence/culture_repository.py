from uuid import UUID
from datetime import date
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


def fetch_all_culture() -> list[tuple[Any, ...]] | Exception:
    """Returns a list of string representing all cultures inside the table culture.
    If this nothing is found, it will return a single empty array.
    :return: A list of tuples containing multiples culture objects
    :rtype: list[tuple[str]] | Exception
    """
    try:
        db.execute("SELECT * FROM culture")
        return db.fetchall()
    except Exception as error:
        return error


def fetch_culture_by_id(culture_id: UUID) -> tuple[Any, ...] | None | Exception:
    """Returns a list of string representing a culture filtered by the id field inside the table culture.
    If this nothing is found, it will return a single empty array.
    :parameter culture_id:
    :return: A list of tuples containing a culture object
    :rtype: list[tuple[str]] | Exception
    """
    try:
        db.execute("SELECT * FROM culture WHERE id = %s", [culture_id])
        return db.fetchone()
    except Exception as error:
        return error


def insert_culture(
    plot_number: int,
    production_code: int,
    start_date: date,
    end_date: date,
    quantity: int,
) -> None | Exception:
    """Insert culture into table culture.
    :parameter plot_number:
    :parameter production_code:
    :parameter start_date:
    :parameter end_date:
    :parameter quantity:
    :return: Nothing or an error
    :rtype: None | Exception
    """
    try:
        db.execute(
            "INSERT INTO culture(plot_number, production_code, start_date, end_date, quantity) VALUES(%s,%s,%s,%s,%s)",
            [plot_number, production_code, start_date, end_date, quantity],
        )
    except Exception as error:
        return error
    finally:
        conn.commit()


def update_culture(
    culture_id: UUID,
    plot_number: int,
    production_code: int,
    start_date: date,
    end_date: date,
    quantity: int,
) -> None | Exception:
    """
    Update culture row using his id field to filter from table culture.
    :parameter culture_id:
    :parameter plot_number:
    :parameter production_code:
    :parameter start_date:
    :parameter end_date:
    :parameter quantity:
    :return: Nothing or an error
    :rtype: None | Exception
    """
    try:
        db.execute(
            "UPDATE culture SET plot_number = %s, production_code = %s, start_date = %s, end_date = %s, "
            "quantity = %s WHERE id = %s",
            [plot_number, production_code, start_date, end_date, quantity, culture_id],
        )
    except Exception as error:
        return error
    finally:
        conn.commit()


def partial_update_culture(
    culture_id: UUID,
    plot_number: int,
    production_code: int,
    start_date: date,
    end_date: date,
    quantity: int,
) -> None | Exception:
    """Partially update culture row using his id field to filter from table culture.
    :parameter culture_id:
    :parameter plot_number:
    :parameter production_code:
    :parameter start_date:
    :parameter end_date:
    :parameter quantity:
    :return: Nothing or an error
    :rtype: None | Exception
    """
    try:
        db.execute(
            "UPDATE culture SET plot_number = COALESCE(%s, plot_number), "
            "production_code = COALESCE(%s, production_code), start_date = COALESCE(%s, start_date), "
            "end_date = COALESCE(%s, end_date), quantity = COALESCE(%s, quantity) WHERE id = %s",
            [plot_number, production_code, start_date, end_date, quantity, culture_id],
        )
    except Exception as error:
        return error
    finally:
        conn.commit()


def delete_culture(culture_id: UUID) -> None | Exception:
    """
    Delete culture row using his id field to filter from table culture.
    :parameter culture_id:
    :return: Nothing or an error
    :rtype: None | Exception
    """
    try:
        db.execute("DELETE FROM culture WHERE id = %s", [culture_id])
    except Exception as error:
        return error
    finally:
        conn.commit()
