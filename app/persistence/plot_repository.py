import psycopg2
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


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


def get_plots():
    """
    Get all the plots in the database.

    :return: A list of all plots.
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM plot")
    plots = cur.fetchall()
    plots_dict = []
    for plot in plots:
        plots_dict.append(
            {
                "number": plot[0],
                "surface": plot[1],
                "name": plot[2],
                "location": plot[3],
            }
        )
    conn.close()
    return plots_dict


def get_plot_by_number(number):
    """
    Get a plot by its number.

    :param (int) number: The plot number.
    :return: A dict with the plot's data or None if not found.
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM plot WHERE number = %s", (number,))
    plot = cur.fetchone()
    conn.close()

    if plot is None:
        return None

    plot_dict = {
        "number": plot[0],
        "surface": plot[1],
        "name": plot[2],
        "location": plot[3],
    }
    return plot_dict


def create_plot(number, surface, name, location):
    """
    Create a new plot in the database.

    :param (int) number: The plot number.
    :param (int) surface: The plot's surface.
    :param (string) name: The plot's name.
    :param (string) location: The plot's location.
    """
    existing_plot = get_plot_by_number(number)
    if existing_plot is not None:
        raise Exception(f"Plot with number {number} already exists")

    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO plot (number, surface, name, location) VALUES (%s, %s, %s, %s)",
        (number, surface, name, location),
    )
    conn.commit()
    conn.close()


def update_plot(number, new_surface, new_name, new_location):
    """
    Update plot information by its number.

    :param (int) number: The plot number to update.
    :param (int) new_surface: The new surface of the plot.
    :param (string) new_name: The new name of the plot.
    :param (string) new_location: The new location of the plot.
    """
    existing_plot = get_plot_by_number(number)
    if existing_plot is None:
        raise Exception(f"Plot with number {number} not found")

    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE plot SET surface = %s, name = %s, location = %s WHERE number = %s",
        (new_surface, new_name, new_location, number),
    )
    conn.commit()
    conn.close()


def partial_update_plot(number, new_surface, new_name, new_location):
    """
    Partial update plot information by its number.

    :param (int) number: The plot number to update.
    :param (int) new_surface: The new surface of the plot.
    :param (string) new_name: The new name of the plot.
    :param (string) new_location: The new location of the plot.
    """
    existing_plot = get_plot_by_number(number)
    if existing_plot is None:
        raise Exception(f"Plot with number {number} not found")

    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE plot SET  surface = COALESCE(%s,surface), name = COALESCE(%s,name), location = COALESCE(%s,location) WHERE number = COALESCE(%s,number)",
        (new_surface, new_name, new_location, number),
    )
    conn.commit()
    conn.close()


def delete_plot(number):
    """
    Delete a plot by its number.

    :param (int) number: The plot number to delete.
    """
    existing_plot = get_plot_by_number(number)
    if existing_plot is None:
        raise Exception(f"Plot with number {number} not found")

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM plot WHERE number = %s", (number,))
    conn.commit()
    conn.close()
