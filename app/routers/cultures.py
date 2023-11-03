from datetime import date
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
    start_date: date
    end_date: date
    quantity: int


class CreateUpdateCulture(BaseModel):
    """Culture class for update route"""

    plot_number: int
    production_code: int
    start_date: date
    end_date: date
    quantity: int


class CultureOptional(BaseModel):
    """Culture class for route validation when values can be optional"""

    plot_number: Optional[int] = None
    production_code: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    quantity: Optional[int] = None


@router.get("/", status_code=status.HTTP_200_OK, summary="Fetch all cultures")
def read_cultures(page: int = 0, limit: int = 10):
    """
    Fetch all cultures with all the information:

    - **id**: unique identifier
    - **plot_number**: plot_number associated with the culture
    - **production_code**: production_code associated with the culture
    - **start_date**: each start_date have a date
    - **end_date**: each end_date have a date
    - **quantity**: each quantity have integer value
    """
    return {"data": fetch_all_culture()[page : page + limit]}


@router.post("/", status_code=status.HTTP_201_CREATED, summary="Create one culture")
def create_culture(culture: CreateUpdateCulture):
    """
    Create a culture with all the information:

    - **plot_number**: plot_number associated with the culture
    - **production_code**: production_code associated with the culture
    - **start_date**: each start_date have a date
    - **end_date**: each end_date have a date
    - **quantity**: each quantity have integer value
    """
    return insert_culture(
        plot_number=culture.plot_number,
        production_code=culture.production_code,
        start_date=culture.start_date,
        end_date=culture.end_date,
        quantity=culture.quantity,
    )


@router.get(
    "/{culture_id}", status_code=status.HTTP_200_OK, summary="Fetch one culture"
)
def read_culture(culture_id: UUID):
    """
    Fetch one culture with all the information:

    - **id**: unique identifier
    - **plot_number**: plot_number associated with the culture
    - **production_code**: production_code associated with the culture
    - **start_date**: each start_date have a date
    - **end_date**: each end_date have a date
    - **quantity**: each quantity have integer value

    :parameter culture_id:
    """
    db_culture = fetch_culture_by_id(culture_id=culture_id)
    if not db_culture:
        raise HTTPException(
            status_code=404,
            detail="Culture not found",
            headers={"X-Error": "Resource not found"},
        )
    return {"data": db_culture}


@router.put(
    "/{culture_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Update a culture",
)
def update_culture_by_id(culture_id: UUID, culture: CreateUpdateCulture):
    """
    Update one culture using his id value

    :parameter culture_id:
    :parameter culture:
    """
    db_culture = fetch_culture_by_id(culture_id=culture_id)
    if not db_culture:
        raise HTTPException(
            status_code=404,
            detail="Culture not found",
            headers={"X-Error": "Resource not found"},
        )
    update_culture(
        culture_id=culture_id,
        plot_number=culture.plot_number,
        production_code=culture.production_code,
        start_date=culture.start_date,
        end_date=culture.end_date,
        quantity=culture.quantity,
    )
    return {"message": "success"}


@router.patch(
    "/{culture_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Update partially a culture",
)
def update_partial_culture_by_id(culture_id: UUID, culture: CultureOptional):
    """
    Update one culture partially using his id value

    :parameter culture_id:
    :parameter culture:
    """
    db_culture = fetch_culture_by_id(culture_id=culture_id)
    stored_model = CultureOptional(**culture.model_dump())
    if not db_culture:
        raise HTTPException(
            status_code=404,
            detail="Culture not found",
            headers={"X-Error": "Resource not found"},
        )
    partial_update_culture(
        culture_id=culture_id,
        plot_number=stored_model.plot_number,
        production_code=stored_model.production_code,
        start_date=stored_model.start_date,
        end_date=stored_model.end_date,
        quantity=stored_model.quantity,
    )
    return {"message": "success"}


@router.delete(
    "/{culture_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a culture"
)
def delete_culture_by_id(culture_id: UUID):
    """
    Delete a culture using his id value

    :parameter culture_id:
    """
    db_culture = fetch_culture_by_id(culture_id=culture_id)
    if not db_culture:
        raise HTTPException(
            status_code=404,
            detail="Culture not found",
            headers={"X-Error": "Resource not found"},
        )
    delete_culture(culture_id=culture_id)
    return {"message": "success"}
