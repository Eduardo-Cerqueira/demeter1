from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.persistence.spread_repository import (
    get_spreads,
    get_spread_by_fertilizer,
    update_spread,
    partial_update_spread,
    delete_spread,
    create_spread,
    get_spreads_order_by_quantity
)

router = APIRouter(tags=["spread"])


class Spread(BaseModel):
    """
    Spread class for route validation.
    """
    fertilizer_id: str
    plot_number: int
    date: str
    spread_quantity: int


class SpreadOptional(BaseModel):
    """
    Spread class for partial spread update route validation.
    """
    date: Optional[str] = None
    spread_quantity: Optional[int] = None


@router.get("/spreads", status_code=status.HTTP_200_OK)
def read_spreads(skip: int = 0, limit: int = 10, sort_quantity = "ASC"):
    """
    Get all spread resources.

    :return dict: A dict of the query response.
    """
    if sort_quantity:
        resources = get_spreads_order_by_quantity(sort_quantity)[skip : skip + limit]
    else:
        resources = get_spreads()[skip : skip + limit]

    if not resources:
        raise HTTPException(status_code=404, detail="Spreads not found")
    resources_list = []
    for spread in resources:
        spread_dict = {
            "fertilizer_id": spread[0],
            "plot_number": spread[1],
            "date": spread[2],
            "spread_quantity": spread[3],
        }
        resources_list.append(spread_dict)
    return {"status": status.HTTP_200_OK, "data": resources_list, "message": "Spreads found"}


@router.get("/spreads/{fertilizer_id}")
def read_spread_by_fertilizer(fertilizer_id: str):
    """
    Get a spread resource by fertilizer.

    :param fertilizer_id: The fertilizer's UUID.
    :return dict: A dict of the query response.
    """
    resource = get_spread_by_fertilizer(fertilizer_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Spread not found")
    resource_dict = {
        "fertilizer_id": resource[0],
        "plot_number": resource[1],
        "date": resource[2],
        "spread_quantity": resource[3],
    }

    return {"status": status.HTTP_200_OK, "data": resource_dict, "message": "Spread found"}


@router.post("/spreads")
def create_new_spread(spread: Spread):
    """
    Create a new spread.

    :param spread: The spread data.
    :return dict: A dict of the query response.
    """
    resource = get_spread_by_fertilizer(spread.fertilizer_id)

    if resource:
        raise HTTPException(status_code=409,detail="Spread already exists")

    create_spread(
        fertilizer_id=spread.fertilizer_id,
        plot_number=spread.plot_number,
        date=spread.date,
        spread_quantity=spread.spread_quantity,
    )
    return {"status": status.HTTP_201_CREATED, "message": "Spread successfully created"}


@router.put("/spreads/{fertilizer_id}")
def update_spread_by_fertilizer(fertilizer_id: str, spread: Spread):
    """
    Update a spread by fertilizer.

    :param fertilizer_id: The fertilizer's UUID.
    :param spread: The new spread data.
    :return dict: A dict of the query response.
    """
    spread_to_update = get_spread_by_fertilizer(fertilizer_id)
    if not spread_to_update:
        raise HTTPException(status_code=404, detail="Spread not found")
    update_spread(
        fertilizer_id=fertilizer_id,
        plot_number=spred.plot_number,
        new_date=spread.date,
        new_spread_quantity=spread.spread_quantity,
    )
    return {"message": "Spread successfully updated"}


@router.patch("/spreads/{fertilizer_id}")
def partial_update_spread_by_fertilizer(
    fertilizer_id: str, spread: SpreadOptional
):
    """
    Partial update a spread by fertilizer.

    :param fertilizer_id: The fertilizer's UUID.
    :param spread: The new spread data.
    :return dict: A dict of the query response.
    """
    spread_to_update = get_spread_by_fertilizer(fertilizer_id)
    if not spread_to_update:
        raise HTTPException(status_code=404, detail="Spread not found")
    partial_update_spread(
        fertilizer_id=fertilizer_id,
        plot_number=spred.plot_number,
        new_date=spread.date,
        new_spread_quantity=spread.spread_quantity,
    )
    return {"message": "Spread successfully updated"}


@router.delete("/spreads/{fertilizer_id}")
def delete_spread_by_fertilizer(fertilizer_id: str):
    """
    Delete a spread by fertilizer.

    :param fertilizer_id: The fertilizer's UUID.
    :return dict: A dict of the query response.
    """
    spread_to_delete = get_spread_by_fertilizer(fertilizer_id)
    if not spread_to_delete:
        raise HTTPException(status_code=404, detail="Spread not found")
    delete_spread(fertilizer_id)

    return {"message": "Spread successfully deleted"}
