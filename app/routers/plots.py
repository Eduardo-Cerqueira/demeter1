from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
from typing import Optional

from demeter.app.persistence.plot_repository import (
    get_plots,
    get_plot_by_number,
    update_plot,
    partial_update_plot,
    delete_plot,
    create_plot,
)

router = APIRouter()


class Plot(BaseModel):
    """
    Plot class for route validation
    """

    number: int
    surface: int
    name: str
    location: str


class PlotPatch(BaseModel):
    """
    Plot class for partial plot update route validation
    """

    surface: Optional[int] = None
    name: Optional[str] = None
    location: Optional[str] = None


@router.get("/plots", status_code=status.HTTP_200_OK)
def read_plots():
    """
    Get all plot's resources.

    :return dict: A dict of for the query response.
    """
    resources = get_plots()
    return {"status": status.HTTP_200_OK, "data": resources, "message": "Plots found"}


@router.get("/plots/{number}")
def read_plot_by_id(number: int):
    """
    Get a plot resource by its number.

    :param number: The plot's number to read.
    :return dict: A dict of the query response.
    """
    resource = get_plot_by_number(number)
    if not resource:
        raise HTTPException(status_code=404, detail=f"Plot {number} not found")
    return {"status": status.HTTP_200_OK, "data": resource, "message": "Plot found"}


@router.post("/plots")
def create_new_plot(plot: Plot):
    """
    Create a new plot.

    :param plot_number: The plot number.
    :param plot_surface: The plot's surface.
    :param plot_name: The plot's name.
    :param plot_location: The plot's location.
    :return dict: A dict of the query response.
    """
    plot_in_db = get_plot_by_number(plot.number)
    if plot_in_db:
        raise HTTPException(
            status_code=409, detail=f"Plot {plot.number} already exists"
        )
    create_plot(
        number=plot.number, surface=plot.surface, name=plot.name, location=plot.location
    )
    return {"status": status.HTTP_201_CREATED, "message": "Plot successfully created"}


@router.put("/plots/{plot_id}")
def update_plot_by_id(plot_id: int, plot: Plot):
    """
    Update a plot by its number.

    :param plot: The new plot's data.
    :param plot_id: The number of the plot to update.
    :return dict: A dict of the query response.
    """
    plot_to_update = get_plot_by_number(plot_id)
    if not plot_to_update:
        raise HTTPException(status_code=404, detail=f"Plot {plot_id} not found")
    update_plot(
        number=plot_id,
        new_surface=plot.surface,
        new_name=plot.name,
        new_location=plot.location,
    )
    return {"message": f"Plot {plot_id} successfully updated "}


@router.patch("/plots/{plot_id}")
def partial_update_plot_by_id(plot_id: int, plot: PlotPatch):
    """
    Parial update a plot by its number.

    :param plot_id: The number of the plot to update.
    :param plot: The new plot's data.
    :return dict: A dict of the query response.
    """
    plot_to_update = get_plot_by_number(plot_id)
    if not plot_to_update:
        raise HTTPException(status_code=404, detail=f"Plot {plot_id} not found")
    partial_update_plot(
        number=plot_id,
        new_surface=plot.surface,
        new_name=plot.name,
        new_location=plot.location,
    )
    return {"message": f"Plot {plot_id} successfully updated "}


@router.delete("/plots/{plot_id}")
def delete_plot_by_id(plot_id: int):
    """
    Delete a plot by its number.

    :param plot_id: The number of the plot to delete.
    :return dict: A dict of the query response.
    """
    plot_to_delete = get_plot_by_number(plot_id)
    if not plot_to_delete:
        raise HTTPException(status_code=404, detail=f"Plot {plot_id} not found")
    delete_plot(plot_id)
    return {"message": f"Plot {plot_id} successfully deleted "}
