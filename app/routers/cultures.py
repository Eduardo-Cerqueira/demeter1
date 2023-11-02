from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.persistence.culture_repository import (
    fetch_all_culture,
    fetch_culture_by_id,
    insert_culture,
    update_culture,
    delete_culture,
    partial_update_culture,
)

router = APIRouter(
    prefix="/cultures",
    tags=["cultures"],
)


class Culture(BaseModel):
    """Basic Culture class for route validation"""

    id: UUID
    plot_number: int
    production_code: int
    start_date: datetime
    end_date: datetime
    quantity: int


class CreateUpdateCulture(BaseModel):
    """Culture class for update route"""

    plot_number: int
    production_code: int
    start_date: datetime
    end_date: datetime
    quantity: int


class CultureOptional(BaseModel):
    """Culture class for route validation when values can be optional"""

    plot_number: Optional[int] = None
    production_code: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    quantity: Optional[int] = None


@router.get("/", status_code=status.HTTP_200_OK, summary="Fetch all cultures")
def read_cultures():
    """
    Fetch all cultures with all the information:

    - **id**: unique identifier
    - **plot_number**: plot_number associated with the culture
    - **production_code**: production_code associated with the culture
    - **start_date**: each start_date have a datetime
    - **end_date**: each end_date have a datetime
    - **quantity**: each quantity have integer value
    """
    return {"data": fetch_all_culture()}


@router.post("/", status_code=status.HTTP_201_CREATED, summary="Create one culture")
def create_culture(culture: Culture):
    """
    Create a culture with all the information:

    - **plot_number**: plot_number associated with the culture
    - **production_code**: production_code associated with the culture
    - **start_date**: each start_date have a datetime
    - **end_date**: each end_date have a datetime
    - **quantity**: each quantity have integer value
    """
    if not culture.id:
        raise HTTPException(
            status_code=400,
            detail="Culture is empty",
            headers={"X-Error": "Resource empty"},
        )
    db_culture = fetch_culture_by_id(culture_id=culture.id)
    if db_culture is not None:
        raise HTTPException(
            status_code=409,
            detail="Culture already exists",
            headers={"X-Error": "Resource already exists"},
        )
    return insert_culture(
        plot_number=culture.plot_number,
        production_code=culture.production_code,
        start_date=culture.start_date,
        end_date=culture.end_date,
        quantity=culture.quantity,
    )
