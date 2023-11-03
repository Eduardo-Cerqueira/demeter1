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
    Get all the owns in the database.

    :return: A list of all owns.
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM own")
    owns = cur.fetchall()
    owns_dict = []
    for own in owns:
        owns_dict.append(
            {
                "fertilizer_id": own[0],
                "element_code": own[1],
                "value": own[2],
            }
        )
    conn.close()
    return owns_dict


def get_own_by_fertilizer_id(fertilizer_id):
    """
    Get a plot by its fertilizer id.

    :param (uuid) fertilizer_id: The own fertilizer_id.
    :return: A dict with the owns data or None if not found.
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM own WHERE fertilizer_id = %s", (fertilizer_id,))
    own = cur.fetchone()
    conn.close()

    if own is None:
        return None

    own_dict = {
        "fertilizer_id": own[0],
        "element_code": own[1],
        "value": own[2],
    }
    return own_dict


def create_own(fertilizer_id, element_code, value):
    """
    Create a new own in the database.

    :param (uuid) fertilizer_id: The own fertilizer_id.
    :param (string) element_code: The own element_code.
    :param (string) value: The own value.
    """
    existing_own = get_own_by_fertilizer_id(fertilizer_id)
    if existing_own is not None:
        raise Exception(f"own with {fertilizer_id} already exists")

    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO own (fertilizer_id, element_code, value) VALUES (%s, %s, %s)",
        (fertilizer_id, element_code, value,),
    )
    conn.commit()
    conn.close()


def update_own(fertilizer_id, element_code, value):
    """
    Update own information by its number.

    :param (uuid) fertilizer_id: The new own fertilizer_id.
    :param (string) element_code: The new own element_code.
    :param (string) value: The own new value.
    """
    existing_own = get_own_by_fertilizer_id(fertilizer_id)
    if existing_own is None:
        raise Exception(f"Plot with number {fertilizer_id} not found")

    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE own SET element_code = %s, value = %s WHERE  fertilizer_id = %s",
        (fertilizer_id, element_code, value),
    )
    conn.commit()
    conn.close()


def partial_update_own(fertilizer_id, element_code, value):
    """
    Partial update plot information by its number.

    :param (uuid) fertilizer_id: The new own fertilizer_id.
    :param (string) element_code: The new own element_code.
    :param (string) value: The own new value.
    """
    existing_own = get_own_by_fertilizer_id(fertilizer_id)
    if existing_own is not None:
        raise Exception(f"own with {fertilizer_id} already exists")

    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE own SET  element_code = COALESCE(%s,element_code), value = COALESCE(%s,value)  WHERE fertilizer_id = COALESCE(%s,fertilizer_id)",
        (fertilizer_id, element_code, value),
    )
    conn.commit()
    conn.close()


def delete_own(fertilizer_id):
    """
    Delete own by its fertilizer_id.

    :param (uuid) fertilizer_id: The own fertilizer_id to delete.
    """
    existing_own = get_own_by_fertilizer_id(fertilizer_id)
    if existing_own is not None:
        raise Exception(f"own with {fertilizer_id} already exists")

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM own WHERE fertilizer_id = %s", (fertilizer_id,))
    conn.commit()
    conn.close()
