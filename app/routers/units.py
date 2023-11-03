from typing import Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.persistence.unit_repository import (
    fetch_all_unit,
    fetch_unit_by_unit,
    insert_unit,
    update_unit,
    delete_unit,
    partial_update_unit,
)

router = APIRouter(
    prefix="/units",
    tags=["units"],
)


class Unit(BaseModel):
    """Basic Unit class for route validation"""

    unit: str


class UnitOptional(BaseModel):
    """Unit class for route validation when values can be optional"""

    unit: Optional[str] = None


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Fetch all units",
    responses={
        200: {
            "content": {"application/json": {"example": {"data": [["foo"], ["bar"]]}}},
        },
    },
)
def read_units():
    """
    Fetch all units with all the information:

    - **unit**: each unit have a designation
    """
    return {"data": fetch_all_unit()}


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create one unit",
    responses={
        201: {
            "description": "Created",
        },
        400: {
            "content": {"application/json": {"example": {"detail": "Unit is empty"}}},
        },
        409: {
            "content": {
                "application/json": {"example": {"detail": "Unit already exists"}}
            },
        },
    },
)
def create_unit(unit: Unit):
    """
    Create a unit with all the information:

    - **unit**: each unit must have a designation
    """
    if not unit.unit:
        raise HTTPException(
            status_code=400,
            detail="Unit is empty",
            headers={"X-Error": "Resource empty"},
        )
    db_unit = fetch_unit_by_unit(unit=unit.unit)
    if db_unit is not None:
        raise HTTPException(
            status_code=409,
            detail="Unit already exists",
            headers={"X-Error": "Resource already exists"},
        )
    return insert_unit(unit=unit.unit)


@router.get(
    "/{unit}",
    status_code=status.HTTP_200_OK,
    summary="Fetch one unit",
    responses={
        200: {
            "content": {"application/json": {"example": {"data": ["foo"]}}},
        },
        404: {
            "content": {"application/json": {"example": {"detail": "Unit not found"}}},
        },
    },
)
def read_unit(unit: str):
    """
    Fetch one unit with all the information:

    - **unit**: each unit have a designation
    """
    db_unit = fetch_unit_by_unit(unit=unit)
    if not db_unit:
        raise HTTPException(
            status_code=404,
            detail="Unit not found",
            headers={"X-Error": "Resource not found"},
        )
    return {"data": db_unit}


@router.put(
    "/{unit_name}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Update a unit",
    responses={
        204: {
            "description": "No Content",
        },
        404: {
            "content": {"application/json": {"example": {"detail": "Unit not found"}}},
        },
    },
)
def update_unit_by_unit(unit_name: str, unit: Unit):
    """
    Update one unit using his unit value

    :parameter unit_name:
    :parameter unit:
    """
    db_unit = fetch_unit_by_unit(unit=unit_name)
    if not db_unit:
        raise HTTPException(
            status_code=404,
            detail="Unit not found",
            headers={"X-Error": "Resource not found"},
        )
    return update_unit(unit_value=unit.unit, unit=unit_name)


@router.patch(
    "/{unit_name}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Update partially a unit",
    responses={
        204: {
            "description": "No Content",
        },
        404: {
            "content": {"application/json": {"example": {"detail": "Unit not found"}}},
        },
    },
)
def update_partial_unit_by_unit(unit_name: str, unit: UnitOptional):
    """
    Update one unit partially using his unit value

    :parameter unit_name:
    :parameter unit:
    """
    db_unit = fetch_unit_by_unit(unit=unit_name)
    stored_model = UnitOptional(**unit.model_dump())
    if not db_unit:
        raise HTTPException(
            status_code=404,
            detail="Unit not found",
            headers={"X-Error": "Resource not found"},
        )
    return partial_update_unit(unit_value=stored_model.unit, unit=unit_name)


@router.delete(
    "/{unit}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a unit",
    responses={
        404: {
            "content": {"application/json": {"example": {"detail": "Unit not found"}}},
        },
    },
)
def delete_unit_by_unit(unit: str):
    """
    Delete a unit using his unit value

    :parameter unit:
    """
    db_unit = fetch_unit_by_unit(unit=unit)
    if not db_unit:
        raise HTTPException(
            status_code=404,
            detail="Unit not found",
            headers={"X-Error": "Resource not found"},
        )
    return delete_unit(unit=unit)
