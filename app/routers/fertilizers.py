from typing import Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.persistence.fertilizer_repository import (
    get_fertilizers,
    get_fertilizer_by_id,
    get_fertilizer_by_name,
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


@router.get("/", status_code=status.HTTP_200_OK, summary="Get all fertilizers")
def read_fertilizers(skip: int = 0, limit: int = 10):
    """
    Get all fertilizer's resources.

    :return dict: A dict of for the query response.
    """
    fertilizers = get_fertilizers()[skip : skip + limit]
    return {"status": status.HTTP_200_OK, "data": fertilizers}


@router.get("/{identifier}", status_code=status.HTTP_200_OK, summary="Get fertilizer by his id")
def read_fertilizer_by_id(identifier: UUID):
    """
    Get a fertilizer resource by its identifier.

    :param identifier: The fertilizer's identifier to read.
    :return dict: A dict of the query response.
    """
    fertilizer = get_fertilizer_by_id(identifier)
    if not fertilizer:
        raise HTTPException(status_code=404, detail=f"Fertilizer {identifier} not found")
    return {"status": status.HTTP_200_OK, "data": fertilizer}


@router.post("/", status_code=status.HTTP_201_CREATED, summary="Create one fertilizer")
def create_fertilizers(fertilizer: Fertilizer):
    """
    Create a new fertilizer.

    :param fertilizer: The new fertilizer's data.
    :return dict: A dict of the query response.
    """
    existing_fertilizer = get_fertilizer_by_name(fertilizer.name)
    if existing_fertilizer is not None:
        raise HTTPException(
            status_code=409, detail=f"Fertilizer {fertilizer.name} already exists"
        )
    create_fertilizer(fertilizer.unit, fertilizer.name)
    return {"status": status.HTTP_201_CREATED, "message": "Fertilizer created"}


@router.put("/{identifier}", status_code=status.HTTP_204_NO_CONTENT, summary="Update a fertilizer by his id")
def update_fertilizer_by_id(identifier: UUID, fertilizer: Fertilizer):
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
            detail="Fertilizer not found",
            headers={"X-Error": "Resource not found"},
        )
    update_fertilizer(str(identifier), fertilizer.unit, fertilizer.name)
    return {"message": "Fertilizer updated"}


@router.delete("/{identifier}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a fertilizer by his id")
def delete_fertilizer_by_id(identifier: UUID):
    """
    Delete a fertilizer by his identifier.

    :param identifier: The identifier of the fertilizer to delete.
    :return dict: A dict of the query response.
    """
    fertilizer_to_delete = get_fertilizer_by_id(identifier)
    if fertilizer_to_delete is None:
        raise HTTPException(status_code=404, detail=f"Fertilizer {identifier} not found")
    delete_fertilizer(str(identifier))
    return {"message": f"Fertilizer {identifier} successfully deleted"}


@router.patch("/{identifier}", status_code=status.HTTP_204_NO_CONTENT, summary="Update partially a fertilizer")
def partial_update_fertilizer_by_id(identifier: UUID, fertilizer: FertilizerPatch):
    """
    Partial update a fertilizer by its identifier.

    :param identifier: The identifier of the fertilizer to update.
    :param fertilizer: The new fertilizer's data.
    :return dict: A dict of the query response.
    """
    fertilizer_to_update = get_fertilizer_by_id(identifier)
    if not fertilizer_to_update:
        raise HTTPException(status_code=404, detail=f"Fertilizer {identifier} not found")
    partial_update_fertilizer(str(identifier), fertilizer.unit, fertilizer.name)
    return {"message": f"Fertilizer {identifier} successfully updated"}
