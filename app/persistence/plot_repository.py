import psycopg2
import os
from uuid import uuid4
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def connect_db():
    """
    Connect to the database.

    :return: Connection to the  database.
    """
    database_name = os.getenv("DATABASE_NAME")
    database_host = os.getenv("DATABASE_HOST")
    database_port = os.getenv("POSTGRES_PORT")
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


def create_plot(number, surface, name, location):
    """
    Create a new plot in the database.

    :param (int) number: The plot number.
    :param (int) surface: The plot's surface.
    :param (string) name: The plot's name.
    :param (string) location: The plot's location.
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO plot (number, surface, name, location) "
                "VALUES (%s, %s, %s, %s)",
                (number, surface, name, location))
    conn.commit()
    conn.close()

def get_plots():
    """
    Get all the plots in the database.

    :return: A list of all plots.
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM plot")
    plots = cur.fetchall()
    conn.close()
    return plots

def get_plot_by_number(number):
    """
    Get a plot by its number.

    :param (int) number: The plot number.
    :return: A tuple with the plot's data.
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM plot WHERE number = %s", (number,))
    plot = cur.fetchone()
    conn.close()
    return plot

def update_plot(number, new_surface, new_name, new_location):
    """
    Update plot information by its number.

    :param (int) number: The plot number to update.
    :param (int) new_surface: The new surface of the plot.
    :param (string) new_name: The new name of the plot.
    :param (string) new_location: The new location of the plot.
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE plot "
                "SET surface = %s, name = %s, location = %s "
                "WHERE number = %s",
                (new_surface, new_name, new_location, number))
    conn.commit()
    conn.close()

def delete_plot(number):
    """
    Delete a plot by its number.

    :param (int) number: The plot number to delete.
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM plot WHERE number = %s", (number,))
    conn.commit()
    conn.close()

# Test CRUD
if __name__ == "__main__":
    create_plot(1, 100, 'Plot A', 'Location A')
    create_plot(2, 100, 'Plot B', 'Location B')
    create_plot(3, 100, 'Plot C', 'Location C')
    plots = get_plots()
    for plot in plots:
        print(plot)
    plot = get_plot_by_number(1)
    update_plot(1, 120, 'Plot D', 'Location D')
    delete_plot(2)

