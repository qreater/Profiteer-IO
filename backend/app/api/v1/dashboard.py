"""

 Copyright 2025 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""
from fastapi import APIRouter, status

from app.utils.dashboard.utils import get_dashboard_data
from app.models.dashboard import DashboardResponse


router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=DashboardResponse,
    response_model_by_alias=False,
    response_model_exclude_none=True,
)
def get_dashboard():
    """
    Fetches the dashboard data.

    Returns:
        DashboardResponse: A response model containing the dashboard data.
    """
    dashboard_data = get_dashboard_data()
    return {"message": "Dashboard Data fetched successfully.", "data": dashboard_data}
