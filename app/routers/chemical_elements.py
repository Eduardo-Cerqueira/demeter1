from typing import Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.persistence.chemical_element import (
    get_chemical_elements,
    get_chemical_element_by_code,
    create_chemical_elements,
    update_chemical_elements,
    delete_chemical_elements,
)

router = APIRouter(
    prefix="/chemical-elements",
    tags=["chemical-elements"],
)


class ChemicalElements(BaseModel):
    """Basic Production class for route validation"""
    code: str
    unit: str
    element_label: str


class ProductionOptional(BaseModel):
    """Production class for route validation when values can be optional"""

    code: Optional[int] = None
    unit: Optional[str] = None
    name: Optional[str] = None


@router.get("/", status_code=status.HTTP_200_OK, summary="Fetch all chemical_elements")
def read_chemical_elements():
    """
    Get all chemical_element's resources.

    :return dict: A dict of for the query response.
    """
    return {"data": get_chemical_elements()}


@router.post("/", status_code=status.HTTP_201_CREATED, summary="Create one chemical_element")
def create_chemical_element(chemicalelement: ChemicalElements):
    """
    Create a new plot.

    :param chemicalelement_code: The chemical_element code.
    :param chemicalelement_unit The chemical_element's unit.
    :param chemicalelement_element_label: The chemical_element's element_label.
    :return dict: A dict of the query response.
    """
    if not chemicalelement.code:
        raise HTTPException(
            status_code=400,
            detail="Production is empty",
            headers={"X-Error": "Resource empty"},
        )
    db_chemical_element = get_chemical_element_by_code(chemicalelement.code)
    if db_chemical_element is not None:
        raise HTTPException(
            status_code=409,
            detail="Production already exists",
            headers={"X-Error": "Resource already exists"},
        )
    return create_chemical_elements(chemicalelement.code, chemicalelement.unit, chemicalelement.element_label)


@router.get("/{code}", status_code=status.HTTP_200_OK, summary="Fetch one chemical_element")
def read_chemical_element(code: str):
    """
    Get a chemical_element resource by his code.

    :param code: The chemical_element's code to read.
    :return dict: A dict of the query response.
    """
    db_code = get_chemical_element_by_code(code)
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
def update_chemical_element_by_code(code: str, chemicalelement: ChemicalElements):
    """
    Update one chemical_element using his code value

    :parameter code: Chemical_element's code
    :parameter chemicalelement: Chemical_element's data
    """
    db_chemical_element = get_chemical_element_by_code(code)
    if not db_chemical_element:
        raise HTTPException(
            status_code=404,
            detail="Production not found",
            headers={"X-Error": "Resource not found"},
        )
    return update_chemical_elements(code,chemicalelement.unit, chemicalelement.element_label)


@router.delete(
    "/{code}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a chemical_element"
)
def delete_chemical_element_by_code(code: str):
    """
    Delete a chemical_element using his code value

    :parameter code:
    """
    db_chemical_element = get_chemical_element_by_code(code)
    if not db_chemical_element:
        raise HTTPException(
            status_code=404,
            detail="Production not found",
            headers={"X-Error": "Resource not found"},
        )
    return delete_chemical_elements(code=code)
