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
