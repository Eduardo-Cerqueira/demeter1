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


def get_chemical_elements():
    """
        Get all chemical_elements in the database.

        :return: A list of all chemical_elements.
    """
    db.execute("SELECT * FROM chemical_element")
    return db.fetchall()


def get_chemical_element_by_code(code: str):
    """
        Get a chemical_element by his code.

        :param (string) code: The chemical_element code.
        :return: A tuple with the chemical_element's data.
    """
    db.execute("SELECT * FROM chemical_element WHERE code = %s", (code,))
    return db.fetchone()


def create_chemical_elements(code: str, unit: str, element_label: str):
    """
        Create a new chemical_element in the database.

        :param (string) code: The chemical_element code.
        :param (string) unit: The chemical_element unit.
        :param (string) element_label: The chemical_element's element_label.
    """
    db.execute("INSERT INTO chemical_element(code, unit, element_label) VALUES(%s,%s,%s)", (code, unit, element_label))
    conn.commit()


def update_chemical_elements(code: str, unit: str, element_label: str):
    """
        Update fertilizer information by his code.

        :param (string) code: The chemical_element code to update.
        :param (string) unit: The new unit of the chemical_element.
        :param (string) element_label: The new element_label of the chemical_element.
    """
    db.execute("UPDATE chemical_element SET code = %s, unit = %s, element_label = %s WHERE code = %s", (code, unit, element_label))
    conn.commit()


def delete_chemical_elements(code: str):
    """
        Delete a chemical_element by his code.

        :param (string) code: The chemical_element code to delete.
    """
    db.execute("DELETE FROM chemical_element WHERE code = %s", (code,))
    conn.commit()
