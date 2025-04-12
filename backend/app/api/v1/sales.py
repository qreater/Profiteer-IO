"""

 Copyright 2025 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""
from fastapi import APIRouter, status

from app.models.sales import SalesRequest, SalesResponse
from app.utils.sales.synthesise import generate_sales_data

router = APIRouter()


@router.post(
    "/",
    response_model=SalesResponse,
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
def generate_sales(data: SalesRequest):
    """
    Generates sales data for the given products over the specified number of hours.

    Args:
        data (SalesRequest): The request data containing the number of hours and product details.

    Returns:
        SalesResponse: A response model containing the generated sales data.
    """
    sales_data = generate_sales_data(data)
    return {
        "message": "Sales Data listed successfully.",
        "data": {
            "results": sales_data,
            "meta": {"page": 1, "limit": len(sales_data), "total": len(sales_data)},
        },
    }
