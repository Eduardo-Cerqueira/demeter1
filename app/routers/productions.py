from typing import Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.persistence.production_repository import (
    fetch_all_production,
    fetch_production_by_code,
    insert_production,
    update_production,
    delete_production,
    partial_update_production,
)

router = APIRouter(
    prefix="/productions",
    tags=["productions"],
)


class Production(BaseModel):
    """Basic Production class for route validation"""

    code: int
    unit: str
    name: str


class UpdateProduction(BaseModel):
    """Production class for update route"""

    unit: str
    name: str


class ProductionOptional(BaseModel):
    """Production class for route validation when values can be optional"""

    unit: Optional[str] = None
    name: Optional[str] = None


@router.get("/", status_code=status.HTTP_200_OK, summary="Fetch all productions")
def read_productions():
    """
    Fetch all productions with all the information:

    - **code**: each code have a designation
    - **unit**: each unit have a designation
    - **name**: each name have a designation
    """
    return {"data": fetch_all_production()}

