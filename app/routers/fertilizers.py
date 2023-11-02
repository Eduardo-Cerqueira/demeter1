from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.persistence.fertilizer_repository import (
    get_fertilizers,
    get_fertilizer_by_id,
    create_fertilizer,
    update_fertilizer,
    delete_fertilizer,
)


router = APIRouter(
    prefix="/fertilizers",
    tags=["fertilizers"],
)


class Fertilizer(BaseModel):
    """Basic Fertilizer class for route validation"""
    id: str
    unit: str
    name: str


@router.get("/", status_code=status.HTTP_200_OK)
def read_fertilizers():
    fertilizers = get_fertilizers()
    return {"status": status.HTTP_200_OK, "data": fertilizers}


@router.get("/{identifier}", status_code=status.HTTP_200_OK)
def read_fertilizer_by_id(identifier):
    fertilizer = get_fertilizer_by_id(identifier)
    if not fertilizer:
        raise HTTPException(
            status_code=404,
            detail="Fertilizer not found",
        )
    return {"status": status.HTTP_200_OK, "data": fertilizer}


@router.post("/fertilizers", status_code=status.HTTP_201_CREATED)
def create_unit(fertilizer: Fertilizer):
    fertilizer_db = get_fertilizer_by_id(fertilizer.id)
    if fertilizer_db is not None:
        raise HTTPException(
            status_code=409,
            detail="Fertilizer already exists",
            headers={"X-Error": "Resource already exists"},
        )
    create_fertilizer(fertilizer.unit, fertilizer.name)


"""@router.put("/{identifier}", status_code=status.HTTP_204_NO_CONTENT)
def update_fertilizer_by_id(identifier, fertilizerclass : Fertilizer):
    fertilizer = get_fertilizer_by_id(identifier)
    if not fertilizer:
        raise HTTPException(
            status_code=404,
            detail="Unit not found",
            headers={"X-Error": "Resource not found"},
        )
    update_fertilizer(identifier, fertilizerclass.unit, fertilizerclass.name)
    return {"message": "db updated"}"""
