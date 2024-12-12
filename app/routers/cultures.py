from datetime import date
from typing import Optional, Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Body
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


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Fetch all cultures",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            [
                                "70dab050-0266-4d47-93c9-2a6fed5e3588",
                                100,
                                300,
                                "2023-09-08",
                                "2023-12-10",
                                20,
                            ],
                            [
                                "e295798f-5e06-4473-a4fd-c70ae8c96ef8",
                                200,
                                150,
                                "2022-10-30",
                                "2024-01-04",
                                50,
                            ],
                        ]
                    }
                }
            }
        },
    },
)
def read_cultures():
    """
    Fetch all cultures with all the information:

    - **id**: unique identifier
    - **plot_number**: plot_number associated with the culture
    - **production_code**: production_code associated with the culture
    - **start_date**: each start_date have a date
    - **end_date**: each end_date have a date
    - **quantity**: each quantity have integer value
    """
    db_cultures = fetch_all_culture()
    if not db_cultures:
        raise HTTPException(
            status_code=404,
            detail="Cultures not found",
            headers={"X-Error": "Resource not found"},
        )
    formatted_cultures = []
    for culture in db_cultures:
        formatted_cultures.append(
            {
                "id": culture[0],
                "plot_number": culture[1],
                "production_code": culture[2],
                "start_date": culture[3],
                "end_date": culture[4],
                "quantity": culture[5],
            }
        )
    return {
        "status": status.HTTP_200_OK,
        "data": formatted_cultures,
        "message": "Cultures found",
    }


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create one culture",
    responses={
        201: {
            "description": "Created",
        },
        400: {
            "content": {
                "application/json": {"example": {"detail": "Culture is empty"}}
            },
        },
        409: {
            "content": {
                "application/json": {"example": {"detail": "Culture already exists"}}
            },
        },
    },
)
def create_culture(
    culture: Annotated[
        CreateUpdateCulture,
        Body(
            examples=[
                {
                    "plot_number": 50,
                    "production_code": 200,
                    "start_date": "2023-01-01",
                    "end_date": "2023-02-01",
                    "quantity": 100,
                }
            ],
        ),
    ],
):
    """
    Create a culture with all the information:

    - **plot_number**: plot_number associated with the culture
    - **production_code**: production_code associated with the culture
    - **start_date**: each start_date have a date
    - **end_date**: each end_date have a date
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


@router.get(
    "/{culture_id}",
    status_code=status.HTTP_200_OK,
    summary="Fetch one culture",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            "70dab050-0266-4d47-93c9-2a6fed5e3588",
                            100,
                            300,
                            "2023-09-08",
                            "2023-12-10",
                            20,
                        ]
                    }
                }
            }
        },
    },
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
    return {
        "status": status.HTTP_200_OK,
        "data": {
            "id": db_culture[0],
            "plot_number": db_culture[1],
            "production_code": db_culture[2],
            "start_date": db_culture[3],
            "end_date": db_culture[4],
            "quantity": db_culture[5],
        },
        "message": "Culture found",
    }


@router.put(
    "/{culture_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Update a culture",
    responses={
        204: {
            "description": "No Content",
        },
        404: {
            "content": {
                "application/json": {"example": {"detail": "Culture not found"}}
            },
        },
    },
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
    responses={
        204: {
            "description": "No Content",
        },
        404: {
            "content": {
                "application/json": {"example": {"detail": "Culture not found"}}
            },
        },
    },
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
    "/{culture_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a culture",
    responses={
        404: {
            "content": {
                "application/json": {"example": {"detail": "Culture not found"}}
            },
        },
    },
)
def delete_culture_by_id(culture_id: int):
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
