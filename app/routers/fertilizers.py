from typing import Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.persistence.fertilizer_repository import (
    get_fertilizers,
    get_fertilizer_by_id,
    create_fertilizer,
    update_fertilizer,
    partial_update_fertilizer,
    delete_fertilizer,
)

# Add prefix "fertilizers" to not re-use "fertilizers" in each routes
router = APIRouter(
    prefix="/fertilizers",
    tags=["fertilizers"],
)


class Fertilizer(BaseModel):
    """Basic Fertilizer class for route validation"""
    unit: str
    name: str


class FertilizerPatch(BaseModel):
    """Fertilizer class for partial fertilizer update route validation"""
    unit: Optional[str] = None
    name: Optional[str] = None


@router.get("/", status_code=status.HTTP_200_OK)
def read_fertilizers():
    """
    Get all fertilizer's resources.

    :return dict: A dict of for the query response.
    """
    fertilizers = get_fertilizers()
    return {"status": status.HTTP_200_OK, "data": fertilizers}


@router.get("/{identifier}", status_code=status.HTTP_200_OK)
def read_fertilizer_by_id(identifier):
    """
    Get a fertilizer resource by its identifier.

    :param identifier: The fertilizer's identifier to read.
    :return dict: A dict of the query response.
    """
    fertilizer = get_fertilizer_by_id(identifier)
    if not fertilizer:
        raise HTTPException(
            status_code=404,
            detail="Fertilizer not found",
        )
    return {"status": status.HTTP_200_OK, "data": fertilizer}


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_fertilizers(fertilizer: Fertilizer):
    """
    Create a new fertilizer.

    :param fertilizer: The new fertilizer's data.
    :param fertilizer.unit: The fertilizer unit.
    :param fertilizer.name: The fertilizer's name.
    :return dict: A dict of the query response.
    """
    create_fertilizer(fertilizer.unit, fertilizer.name)
    return {"status": status.HTTP_201_CREATED, "message": "Fertilizer created"}


@router.put("/{identifier}", status_code=status.HTTP_204_NO_CONTENT)
def update_fertilizer_by_id(identifier, fertilizer: Fertilizer):
    """
    Update a fertilizer by his identifier.

    :param fertilizer: The new fertilizer's data.
    :param identifier: The identifier of the fertilizer to update.
    :return dict: A dict of the query response.
    """
    fertilizer_db = get_fertilizer_by_id(identifier)
    if not fertilizer_db:
        raise HTTPException(
            status_code=404,
            detail="Unit not found",
            headers={"X-Error": "Resource not found"},
        )
    update_fertilizer(identifier, fertilizer.unit, fertilizer.name)
    return {"message": "Fertilizer updated"}


@router.delete("/{identifier}")
def delete_fertilizer_by_id(identifier):
    """
    Delete a fertilizer by his identifier.

    :param identifier: The identifier of the fertilizer to delete.
    :return dict: A dict of the query response.
    """
    fertilizer_to_delete = get_fertilizer_by_id(identifier)
    if not fertilizer_to_delete:
        raise HTTPException(status_code=404, detail=f"Fertilizer {identifier} not found")
    delete_fertilizer(identifier)
    return {"message": f"Fertilizer {identifier} successfully deleted"}


@router.patch("/{identifier}")
def partial_update_fertilizer_by_id(identifier, fertilizer: FertilizerPatch):
    """
    Partial update a fertilizer by its identifier.

    :param identifier: The identifier of the fertilizer to update.
    :param fertilizer: The new fertilizer's data.
    :return dict: A dict of the query response.
    """
    fertilizer_to_update = get_fertilizer_by_id(identifier)
    if not fertilizer_to_update:
        raise HTTPException(status_code=404, detail=f"Fertilizer {identifier} not found")
    partial_update_fertilizer(identifier, fertilizer.unit, fertilizer.name)
    return {"message": f"Fertilizer {identifier} successfully updated"}