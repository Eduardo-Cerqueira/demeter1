from typing import Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.persistence.counter_repository import fetch_counter_by_tag_route, insert_counter, update_counter_count
from app.persistence.log_repository import insert_log

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


class ProductionOptional(BaseModel):
    """Production class for route validation when values can be optional"""

    code: Optional[int] = None
    unit: Optional[str] = None
    name: Optional[str] = None


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Fetch all productions",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "data": [[100, "foo", "FooBar"], [200, "bar", "BarFoo"]]
                    }
                }
            }
        },
    },
)
def read_productions():
    """
    Fetch all productions with all the information:

    - **code**: each code have a designation
    - **unit**: each unit have a designation
    - **name**: each name have a designation
    """
    counter = fetch_counter_by_tag_route(route="productions", tag="fetch_productions")
    if not counter:
        insert_counter(route="productions", tag="fetch_productions", count=1)
    else:
        update_counter_count(route="productions", tag="fetch_productions")

    insert_log(f"Fetch cultures: {fetch_all_production()} at route fetch_productions on cultures")
    return {"data": fetch_all_production()}


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create one production",
    responses={
        201: {
            "description": "Created",
        },
        400: {
            "content": {
                "application/json": {"example": {"detail": "Production is empty"}}
            },
        },
        409: {
            "content": {
                "application/json": {"example": {"detail": "Production already exists"}}
            },
        },
    },
)
def create_production(production: Production):
    """
    Create a production with all the information:

    - **code**: each code have a designation
    - **unit**: each unit have a designation
    - **name**: each name have a designation
    """
    counter = fetch_counter_by_tag_route(route="productions", tag="create_production")
    if not counter:
        insert_counter(route="productions", tag="create_production", count=1)
    else:
        update_counter_count(route="productions", tag="create_production")

    if not production.code:
        insert_log("HTTPException 400 Production is empty at route create_production on productions")
        raise HTTPException(
            status_code=400,
            detail="Production is empty",
            headers={"X-Error": "Resource empty"},
        )
    db_production = fetch_production_by_code(code=production.code)
    if db_production is not None:
        insert_log("HTTPException 409 Production already exists at route create_production on productions")
        raise HTTPException(
            status_code=409,
            detail="Production already exists",
            headers={"X-Error": "Resource already exists"},
        )
    insert_log(f"Insert productions: {fetch_all_production()} at route create_production on productions")
    return insert_production(
        code=production.code, unit=production.unit, name=production.name
    )


@router.get(
    "/{code}",
    status_code=status.HTTP_200_OK,
    summary="Fetch one production",
    responses={
        200: {
            "content": {"application/json": {"example": {"data": [100, "foo", "Bar"]}}},
        },
        404: {
            "content": {
                "application/json": {"example": {"detail": "Production not found"}}
            },
        },
    },
)
def read_production(code: int):
    """
    Fetch one production with all the information:

    - **code**: each code have a designation
    - **unit**: each unit have a designation
    - **name**: each name have a designation

    :parameter code:
    """
    counter = fetch_counter_by_tag_route(route="productions", tag="fetch_one")
    if not counter:
        insert_counter(route="productions", tag="fetch_one", count=1)
    else:
        update_counter_count(route="productions", tag="fetch_one")

    db_code = fetch_production_by_code(code=code)
    if not db_code:
        insert_log("HTTPException 404 Production not found at route fetch_one on productions")
        raise HTTPException(
            status_code=404,
            detail="Production not found",
            headers={"X-Error": "Resource not found"},
        )
    insert_log(f"Fetch {db_code} at route fetch_one on productions")
    return {"data": db_code}


@router.put(
    "/{code_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Update a production",
    responses={
        204: {
            "description": "No Content",
        },
        404: {
            "content": {
                "application/json": {"example": {"detail": "Production not found"}}
            },
        },
    },
)
def update_production_by_code(code_id: int, production: Production):
    """
    Update one production using his code value

    :parameter code_id:
    :parameter production:
    """
    counter = fetch_counter_by_tag_route(route="productions", tag="update_by_id")
    if not counter:
        insert_counter(route="productions", tag="update_by_id", count=1)
    else:
        update_counter_count(route="productions", tag="update_by_id")

    db_production = fetch_production_by_code(code=code_id)
    if not db_production:
        insert_log("HTTPException 404 Production not found at route update_by_id on productions")
        raise HTTPException(
            status_code=404,
            detail="Production not found",
            headers={"X-Error": "Resource not found"},
        )
    insert_log(f"Updated {db_production} to {production} at route update_by_id on productions")
    return update_production(
        code=code_id,
        new_code=production.code,
        new_unit=production.unit,
        new_name=production.name,
    )


@router.patch(
    "/{code_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Update partially a production",
    responses={
        204: {
            "description": "No Content",
        },
        404: {
            "content": {
                "application/json": {"example": {"detail": "Production not found"}}
            },
        },
    },
)
def update_partial_production_by_code(code_id: int, production: ProductionOptional):
    """
    Update one production partially using his code value

    :parameter code_id:
    :parameter production:
    """
    counter = fetch_counter_by_tag_route(route="productions", tag="partial_update_by_id")
    if not counter:
        insert_counter(route="productions", tag="partial_update_by_id", count=1)
    else:
        update_counter_count(route="productions", tag="partial_update_by_id")

    db_production = fetch_production_by_code(code=code_id)
    stored_model = ProductionOptional(**production.model_dump())
    if not db_production:
        insert_log("HTTPException 404 Culture not found at route partial_update_by_id on productions")
        raise HTTPException(
            status_code=404,
            detail="Production not found",
            headers={"X-Error": "Resource not found"},
        )
    insert_log(f"Updated {db_production} to {stored_model} at route partial_update_by_id on productions")
    return partial_update_production(
        code=code_id,
        new_code=stored_model.code,
        new_unit=stored_model.unit,
        new_name=stored_model.name,
    )


@router.delete(
    "/{code}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a production",
    responses={
        404: {
            "content": {
                "application/json": {"example": {"detail": "Production not found"}}
            },
        },
    },
)
def delete_production_by_code(code: int):
    """
    Delete a production using his code value

    :parameter code:
    """
    db_production = fetch_production_by_code(code=code)
    if not db_production:
        insert_log("HTTPException 404 Production not found at route delete_production on productions")
        raise HTTPException(
            status_code=404,
            detail="Production not found",
            headers={"X-Error": "Resource not found"},
        )
    insert_log(f"Deleted {db_production} at route delete_production on productions")
    return delete_production(code=code)
