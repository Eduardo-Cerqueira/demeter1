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


@router.post("/", status_code=status.HTTP_201_CREATED, summary="Create one production")
def create_production(production: Production):
    """
    Create a production with all the information:

    - **code**: each code have a designation
    - **unit**: each unit have a designation
    - **name**: each name have a designation
    """
    if not production.code:
        raise HTTPException(
            status_code=400,
            detail="Production is empty",
            headers={"X-Error": "Resource empty"},
        )
    db_production = fetch_production_by_code(code=production.code)
    if db_production is not None:
        raise HTTPException(
            status_code=409,
            detail="Production already exists",
            headers={"X-Error": "Resource already exists"},
        )
    return insert_production(
        code=production.code, unit=production.unit, name=production.name
    )


@router.get("/{code}", status_code=status.HTTP_200_OK, summary="Fetch one production")
def read_production(code: int):
    """
    Fetch one production with all the information:

    - **code**: each code have a designation
    - **unit**: each unit have a designation
    - **name**: each name have a designation

    :parameter code:
    """
    db_code = fetch_production_by_code(code=code)
    if not db_code:
        raise HTTPException(
            status_code=404,
            detail="Production not found",
            headers={"X-Error": "Resource not found"},
        )
    return {"data": db_code}


@router.put(
    "/{code}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Update a production",
)
def update_production_by_code(code: int, production: UpdateProduction):
    """
    Update one production using his code value

    :parameter code:
    :parameter production:
    """
    db_production = fetch_production_by_code(code=code)
    if not db_production:
        raise HTTPException(
            status_code=404,
            detail="Production not found",
            headers={"X-Error": "Resource not found"},
        )
    return update_production(
        code=code,
        new_unit=production.unit,
        new_name=production.name,
    )


@router.patch(
    "/{code}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Update partially a production",
)
def update_partial_production_by_code(code: int, production: ProductionOptional):
    """
    Update one production partially using his code value

    :parameter code:
    :parameter production:
    """
    db_production = fetch_production_by_code(code=code)
    stored_model = ProductionOptional(**production.model_dump())
    if not db_production:
        raise HTTPException(
            status_code=404,
            detail="Production not found",
            headers={"X-Error": "Resource not found"},
        )
    return partial_update_production(
        code=code,
        new_unit=stored_model.unit,
        new_name=stored_model.name,
    )
