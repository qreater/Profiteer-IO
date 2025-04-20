"""

 Copyright 2025 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from app.utils.data.data_source import DataStore
from app.utils.exceptions.errors import not_found_error

from app.utils.catalog.queries import (
    GET_PRODUCTS_QUERY,
    GET_PRODUCT_BY_ID_QUERY,
)

data_store = DataStore()


def get_products() -> dict:
    """
    Fetches the products from the database.

    Returns:
        dict: A dictionary containing the products.
    """

    products = data_store.execute_query(GET_PRODUCTS_QUERY, mode="retrieve")[
        "response"
    ][0]["data"]

    return products


def get_product(product_id: str) -> dict:
    """
    Fetches the product data from the database.

    Returns:
        dict: A dictionary containing the product data.
    """

    product = data_store.execute_query(
        GET_PRODUCT_BY_ID_QUERY,
        params=(product_id, product_id, product_id),
        mode="retrieve",
    )["response"][0]

    if not product.get("details"):
        raise not_found_error("Product", product_id)

    return product
