import string
from uuid import UUID

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


def get_fertilizers():
    """
    Get all fertilizers in the database.

    :return: A list of all fertilizers.
    """
    db.execute("SELECT * FROM fertilizer")
    fertilizers = db.fetchall()
    new_fertilizers = []
    for f in fertilizers:
        new_fertilizers.append(
            {
                "id": f[0],
                "unit": f[1],
                "name": f[2],
            }
        )
    return new_fertilizers


def get_fertilizer_by_id(identifier: UUID):
    """
    Get a fertilizer by his identifier.

    :param (uuid) identifier: The fertilizer identifier.
    :return: A tuple with the fertilizer's data.
    """
    db.execute("SELECT * FROM fertilizer WHERE id = %s", (str(identifier),))
    fertilizer = db.fetchone()
    if fertilizer is None:
        return None
    new_fertilizer = {
        "id": fertilizer[0],
        "unit": fertilizer[1],
        "name": fertilizer[2],
    }
    return new_fertilizer


def get_fertilizer_by_name(name: str):
    """
    Get a fertilizer by his name.

    :param (string) name: The fertilizer name.
    :return: A tuple with the fertilizer's data.
    """
    db.execute("SELECT * FROM fertilizer WHERE name = %s", (name,))
    fertilizer = db.fetchone()
    if fertilizer is None:
        return None
    new_fertilizer = {
        "id": fertilizer[0],
        "unit": fertilizer[1],
        "name": fertilizer[2],
    }
    return new_fertilizer


def create_fertilizer(unit, name):
    """
    Create a new fertilizer in the database.

    :param (string) unit: The fertilizer unit.
    :param (string) name: The fertilizer's name.
    """
    existing_fertilizer = get_fertilizer_by_name(name)
    if existing_fertilizer is not None:
        raise Exception(f"Fertilizer with name {name} already exists")
    db.execute("INSERT INTO fertilizer(unit,name) VALUES(%s,%s)", (unit, name))
    conn.commit()


def update_fertilizer(identifier, unit, name):
    """
    Update fertilizer information by his identifier.

    :param (uuid) identifier: The fertilizer identifier to update.
    :param (string) unit: The new unit of the fertilizer.
    :param (string) name: The new name of the fertilizer.
    """
    db.execute(
        "UPDATE fertilizer SET unit = %s, name = %s WHERE id = %s",
        (unit, name, identifier),
    )
    conn.commit()


def partial_update_fertilizer(identifier, unit, name):
    """
    Partial update fertilizer information by his identifier.

    :param (uuid) identifier: The plot identifier to update.
    :param (string) unit: The new unit of the fertilizer.
    :param (string) name: The new name of the fertilizer.
    """
    existing_fertilizer = get_fertilizer_by_id(identifier)
    if existing_fertilizer is None:
        raise Exception(f"Plot with number {identifier} not found")
    db.execute(
        "UPDATE fertilizer SET  unit = COALESCE(%s,unit), name = COALESCE(%s,unit) WHERE id = COALESCE(%s,id)",
        (unit, name, identifier),
    )
    conn.commit()
    conn.close()


def delete_fertilizer(identifier: UUID):
    """
    Delete a fertilizer by its identifier.

    :param (uuid) identifier: The fertilizer identifier to delete.
    """
    existing_fertilizer = get_fertilizer_by_id(identifier)
    if existing_fertilizer is None:
        raise Exception(f"Plot with number {identifier} not found")
    db.execute("DELETE FROM fertilizer WHERE id = %s", (identifier,))
    conn.commit()
