from datetime import date
from typing import Optional, Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Body
from pydantic import BaseModel

from app.persistence.counter_repository import fetch_counter_by_tag_route, insert_counter, update_counter_count
from app.persistence.culture_repository import (
    fetch_all_culture,
    fetch_culture_by_id,
    insert_culture,
    update_culture,
    delete_culture,
    partial_update_culture,
)
from app.persistence.log_repository import insert_log

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
    counter = fetch_counter_by_tag_route(route="cultures", tag="fetch_cultures")
    if not counter:
        insert_counter(route="cultures", tag="fetch_cultures", count=1)
    else:
        update_counter_count(route="cultures", tag="fetch_cultures")

    insert_log(f"Fetch cultures: {fetch_all_culture} at route fetch_cultures on cultures")
    return {"data": fetch_all_culture()}


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
    counter = fetch_counter_by_tag_route(route="cultures", tag="create_culture")
    if not counter:
        insert_counter(route="cultures", tag="create_culture", count=1)
    else:
        update_counter_count(route="cultures", tag="create_culture")

    if not culture.id:
        raise HTTPException(
            status_code=400,
            detail="Culture is empty",
            headers={"X-Error": "Resource empty"},
        )
    db_culture = fetch_culture_by_id(culture_id=culture.id)
    if db_culture is not None:
        insert_log("HTTPException 409 Culture not found at route fetch_one on cultures")
        raise HTTPException(
            status_code=409,
            detail="Culture already exists",
            headers={"X-Error": "Resource already exists"},
        )
    insert_log(f"Insert cultures: {fetch_all_culture} at route create_culture on cultures")
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
    counter = fetch_counter_by_tag_route(route="cultures", tag="fetch_one")
    if not counter:
        insert_counter(route="cultures", tag="fetch_one", count=1)
    else:
        update_counter_count(route="cultures", tag="fetch_one")

    db_culture = fetch_culture_by_id(culture_id=culture_id)
    if not db_culture:
        insert_log("HTTPException 404 Culture not found at route fetch_one on cultures")
        raise HTTPException(
            status_code=404,
            detail="Culture not found",
            headers={"X-Error": "Resource not found"},
        )
    insert_log(f"Fetch {db_culture} at route fetch_one on cultures")
    return {"data": db_culture}


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
    counter = fetch_counter_by_tag_route(route="cultures", tag="update_by_id")
    if not counter:
        insert_counter(route="cultures", tag="update_by_id", count=1)
    else:
        update_counter_count(route="cultures", tag="update_by_id")

    db_culture = fetch_culture_by_id(culture_id=culture_id)
    if not db_culture:
        insert_log("HTTPException 404 Culture not found at route update_by_id on cultures")
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
    insert_log(f"Updated {db_culture} to {culture} at route update_by_id on cultures")
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
    counter = fetch_counter_by_tag_route(route="cultures", tag="partial_update_by_id")
    if not counter:
        insert_counter(route="cultures", tag="partial_update_by_id", count=1)
    else:
        update_counter_count(route="cultures", tag="partial_update_by_id")

    db_culture = fetch_culture_by_id(culture_id=culture_id)
    stored_model = CultureOptional(**culture.model_dump())
    if not db_culture:
        insert_log("HTTPException 404 Culture not found at route partial_update_by_id on cultures")
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
    insert_log(f"Updated {db_culture} to {stored_model} at route partial_update_by_id on cultures")
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
def delete_culture_by_id(culture_id: UUID):
    """
    Delete a culture using his id value

    :parameter culture_id:
    """
    counter = fetch_counter_by_tag_route(route="cultures", tag="delete_culture")
    if not counter:
        insert_counter(route="cultures", tag="delete_culture", count=1)
    else:
        update_counter_count(route="cultures", tag="delete_culture")

    db_culture = fetch_culture_by_id(culture_id=culture_id)
    if not db_culture:
        insert_log("HTTPException 404 Culture not found at route delete_culture on cultures")
        raise HTTPException(
            status_code=404,
            detail="Culture not found",
            headers={"X-Error": "Resource not found"},
        )
    insert_log(f"Deleted {db_culture} at route delete_culture on cultures")
    delete_culture(culture_id=culture_id)
    return {"message": "success"}
