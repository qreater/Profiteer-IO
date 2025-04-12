"""

 Copyright 2025 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""
from fastapi import APIRouter, status

from app.utils.catalog.utils import get_product, get_products

from app.models.catalog import ProductResponse, ProductListResponse


router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=ProductListResponse,
    response_model_exclude_none=True,
)
def list_products():
    """
    Fetches the list of products.

    Returns:
        ProductListResponse: A response model containing the list of products.
    """
    products_data = get_products()
    return {"message": "Products fetched successfully.", "data": products_data}


@router.get(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductResponse,
    response_model_exclude_none=True,
)
def get_product_by_id(product_id: str):
    """
    Fetches the product details by product ID.

    Args:
        product_id (str): The ID of the product to fetch.

    Returns:
        ProductResponse: A response model containing the product details.
    """
    product_data = get_product(product_id)
    return {"message": "Product Data fetched successfully.", "data": product_data}
