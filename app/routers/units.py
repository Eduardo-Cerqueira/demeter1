from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.persistence.unit_repository import (
    fetch_all_unit,
    fetch_unit_by_unit,
    insert_unit,
    update_unit,
    delete_unit,
)

router = APIRouter(
    prefix="/units",
    tags=["units"],
)


class Unit(BaseModel):
    unit: str


@router.get("/", status_code=status.HTTP_200_OK)
def read_units():
    return {"data": fetch_all_unit()}


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_unit(unit: Unit):
    if not unit.unit:
        raise HTTPException(
            status_code=400,
            detail="Unit is empty",
            headers={"X-Error": "Resource empty"},
        )
    db_unit = insert_unit(unit=unit.unit)
    if db_unit is not None:
        raise HTTPException(
            status_code=409,
            detail="Unit already exists",
            headers={"X-Error": "Resource already exists"},
        )


@router.get("/{unit}", status_code=status.HTTP_200_OK)
def read_unit(unit: str):
    db_unit = fetch_unit_by_unit(unit=unit)
    if not db_unit:
        raise HTTPException(
            status_code=404,
            detail="Unit not found",
            headers={"X-Error": "Resource not found"},
        )
    return {"data": unit}


@router.put("/{unit_name}", status_code=status.HTTP_204_NO_CONTENT)
def update_unit_by_unit(unit_name: str, unit: Unit):
    db_unit = fetch_unit_by_unit(unit=unit_name)
    if not db_unit:
        raise HTTPException(
            status_code=404,
            detail="Unit not found",
            headers={"X-Error": "Resource not found"},
        )
    return update_unit(unit_value=unit.unit, unit=unit_name)


@router.delete("/{unit}", status_code=status.HTTP_204_NO_CONTENT)
def delete_unit_by_unit(unit: str):
    unit = fetch_unit_by_unit(unit=unit)
    if not unit:
        raise HTTPException(
            status_code=404,
            detail="Unit not found",
            headers={"X-Error": "Resource not found"},
        )
    return delete_unit(unit=unit)
