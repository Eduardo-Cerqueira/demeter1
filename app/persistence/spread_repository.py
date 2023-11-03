import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def connect_db():
    """
    Connect to the database.

    :return: Connection to the  database.
    """
    database_name = os.getenv("DATABASE_NAME")
    database_host = os.getenv("DATABASE_HOST")
    database_port = os.getenv("DATABASE_PORT")
    database_user = os.getenv("DATABASE_USER")
    database_password = os.getenv("DATABASE_PASSWORD")

    conn = psycopg2.connect(
        database=database_name,
        host=database_host,
        user=database_user,
        password=database_password,
        port=database_port,
    )
    return conn


def get_spreads():
    """
    Get all the spread in the database.

    :return: A list of all spread or an Exception.
    """
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM spread")
        return cur.fetchall()
    except Exception:
        return None
    finally:
        conn.close()



def get_spread_by_fertilizer(fertilizer_id):
    """
    Get a spread by fertilizer_id.

    :param (str) fertilizer_id: The ID of the fertilizer.
    :return: A Tuple with the spread's data or None if not found.
    """
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT * FROM spread WHERE fertilizer_id = %s",
            (fertilizer_id,),
        )
        return cur.fetchone()
    except Exception:
        return None
    finally:
        conn.close()

def get_spreads_order_by_quantity(sort_type):
    """
    Get all the spread in the database.

    :return: A list of all spread or None if no data.
    """
    conn = connect_db()
    cur = conn.cursor()
    try:
        if sort_type.lower() == "asc":
            cur.execute("SELECT * FROM spread ORDER BY spread_quantity ASC")
        else:
            cur.execute("SELECT * FROM spread ORDER BY spread_quantity DESC")
        return cur.fetchall()
    except Exception:
        return None
    finally:
        conn.close()



def create_spread(fertilizer_id, plot_number, date, spread_quantity):
    """
    Create a new spread in the database.

    :param (str) fertilizer_id: The ID of the fertilizer.
    :param (int) plot_number: The plot number.
    :param (date) date: The date of the spread.
    :param (int) spread_quantity: The quantity of the spread.
    :return: Exception if already exist.
    """
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO spread (fertilizer_id, plot_number, date, spread_quantity) VALUES (%s, %s, %s, %s)",
            (fertilizer_id, plot_number, date, spread_quantity),
        )
    except Exception as error:
        return error
    finally:
        conn.commit()
        conn.close()


def update_spread(fertilizer_id, plot_number, new_date, new_spread_quantity):
    """
    Update the spread quantity for a spread.

    :param (str) fertilizer_id: The ID of the fertilizer.
    :param (int) plot_number: The plot number.
    :param (date) new_date: The new date of the spread.
    :param (int) new_spread_quantity: The new quantity of the spread.
    :return: Expection if not spread not exist.
    """
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE spread SET spread_quantity = %s, date = %s WHERE fertilizer_id = %s",
            (new_spread_quantity, new_date, fertilizer_id),
        )
    except Exception as error:
        return error
    finally:
        conn.commit()
        conn.close()


def partial_update_spread(fertilizer_id, plot_number, new_date, new_spread_quantity):
    """
    Partial update spread information by fertilizer_id and plot_id.

    :param (str) fertilizer_id: The UUID of the fertilizer.
    :param (int) plot_number: The UUID of the plot.
    :param (date) new_date: The new date of the spread.
    :param (int) new_spread_quantity: The new spread quantity.
    :return: Expection if not spread not exist.
    """
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE spread SET date = COALESCE(%s, date), spread_quantity = COALESCE(%s, spread_quantity) WHERE "
            "fertilizer_id = %s",
            (new_date, new_spread_quantity, fertilizer_id,),
        )
    except Exception as error:
        return error
    finally:
        conn.commit()
        conn.close()


def delete_spread(fertilizer_id):
    """
    Delete spread by fertilizer_id.

    :param (str) fertilizer_id: The UUID of the fertilizer.
    :return: Expection if not spread not exist.
    """
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM spread WHERE fertilizer_id = %s", (fertilizer_id,))
    except Exception as error:
        return error
    finally:
        conn.commit()
        conn.close()

