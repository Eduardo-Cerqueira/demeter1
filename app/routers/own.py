from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
from typing import Optional

from demeter.app.persistence.own_repository import (
    get_owns,
    get_own_by_fertilizer_id,
    update_own,
    partial_update_own,
    delete_own,
    create_own,
)

router = APIRouter()


class Own(BaseModel):
    """
    Own class for route validation
    """

    fertilizer_id: str
    element_code: str
    value: int



class OwnPatch(BaseModel):
    """
    Own class for partial own update route validation
    """

    element_code: Optional[str] = None
    value: Optional[int] = None


@router.get("/owns", status_code=status.HTTP_200_OK)
def read_owns():
    """
    Get all owns resources.

    :return dict: A dict of for the query response.
    """
    resources = get_owns()
    return {"status": status.HTTP_200_OK, "data": resources, "message": "Owns found"}


@router.get("/owns/{fertilizer_id}")
def read_own_by_fertilizer_id(fertilizer_id: str):
    """
    Get own resource by its fertilizer_id.

    :param fertilizer_id: The own fertilizer_id to read.
    :return dict: A dict of the query response.
    """
    resource = get_own_by_fertilizer_id(fertilizer_id)
    if not resource:
        raise HTTPException(status_code=404, detail=f"Own {fertilizer_id} not found")
    return {"status": status.HTTP_200_OK, "data": resource, "message": "Plot found"}


@router.post("/owns")
def create_new_own(own: Own):
    """
    Create a new own.

    :param own.fertilizer_id: The own fertilizer_id.
    :param own.element_code: The own element_code.
    :param own.value: The own value.
    :return dict: A dict of the query response.
    """
    own_in_db = get_own_by_fertilizer_id(own.fertilizer_id)
    if own_in_db:
        raise HTTPException(
            status_code=409, detail=f"Own {own.fertilizer_id} already exists"
        )
    create_own(
        fertilizer_id=own.fertilizer_id, element_code=own.element_code, value=own.value,
    )
    return {"status": status.HTTP_201_CREATED, "message": "Own successfully created"}


@router.put("/owns/{fertilizer_id}")
def update_own_by_fertilizer_id(fertilizer_id: str, own: Own):
    """
    Update own by its fertilizer_id.

    :param own: The new own data.
    :param fertilizer_id: The fertilizer_id of the own to update.
    :return dict: A dict of the query response.
    """
    own_to_update = get_own_by_fertilizer_id(fertilizer_id)
    if not own_to_update:
        raise HTTPException(status_code=404, detail=f"Own {fertilizer_id} not found")
    update_own(
        fertilizer_id=own.fertilizer_id,
        element_code=own.element_code,
        value=own.value,

    )
    return {"message": f"Own {fertilizer_id} successfully updated "}


@router.patch("/owns/{fertilizer_id}")
def partial_update_own(fertilizer_id: str, own: OwnPatch):
    """
    Partial update own by its number.

    :param fertilizer_id: The fertilizer_id of the own to update.
    :param own: The new own data.
    :return dict: A dict of the query response.
    """
    own_to_update = get_own_by_fertilizer_id(fertilizer_id)
    if not own_to_update:
        raise HTTPException(status_code=404, detail=f"Own {fertilizer_id} not found")
    partial_update_own(

        new_fertilizer_id=own.fertilizer_id,
        new_element_code=own.element_code,
        new_value=own.value,
    )
    return {"message": f"Own {fertilizer_id} successfully updated "}


@router.delete("/owns/{fertilizer_id}")
def delete_own(fertilizer_id: str):
    """
    Delete own by its fertilizer_id.

    :param fertilizer_id: The fertilizer_id of the own to delete.
    :return dict: A dict of the query response.
    """
    own_to_delete = get_own_by_fertilizer_id(fertilizer_id)
    if not own_to_delete:
        raise HTTPException(status_code=404, detail=f"Own {fertilizer_id} not found")
    delete_own(fertilizer_id)
    return {"message": f"Own {fertilizer_id} successfully deleted "}
