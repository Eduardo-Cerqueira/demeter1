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
        spreads_data = cur.fetchall()
        spreads_list = []
        for spread in spreads_data:
            spread_dict = {
                "fertilizer_id": spread[0],
                "plot_number": spread[1],
                "date": spread[2],
                "spread_quantity": float(spread[3]),
            }
            spreads_list.append(spread_dict)
            return spreads_list
    except Exception as error:
        return error
    finally:
        conn.close()



def get_spread_by_fertilizer(fertilizer_id):
    """
    Get a spread by fertilizer_id.

    :param (str) fertilizer_id: The ID of the fertilizer.
    :return: A list of dict with the spread's data, None or Error if not found.
    """
    conn = connect_db()
    cur = conn.cursor()
    try:

        cur.execute(
            "SELECT * FROM spread WHERE fertilizer_id = %s",
            (fertilizer_id,),
        )
        spread_dict = {
            "fertilizer_id": spread[0],
            "plot_number": spread[1],
            "date": spread[2],
            "spread_quantity": float(spread[3]),
        }
        return spread_dict
    except Exception as error:
        return error
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
            "UPDATE spread SET spread_quantity = %s WHERE fertilizer_id = %s AND plot_number = %s AND date = %s",
            (new_spread_quantity, fertilizer_id, plot_number, new_date),
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
            "UPDATE public.spread SET date = COALESCE(%s, date), spread_quantity = COALESCE(%s, spread_quantity) WHERE "
            "fertilizer_id = %s AND plot_number = %s",
            (new_date, new_spread_quantity, fertilizer_id, plot_number),
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
        cur.execute("DELETE FROM public.spread WHERE fertilizer_id = %s", (fertilizer_id,))
    except Exception as error:
        return error
    finally:
        conn.commit()
        conn.close()

