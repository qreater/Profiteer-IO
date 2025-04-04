"""

 Copyright 2025 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

import random
import math
from datetime import datetime, timedelta
from typing import List, Dict, Any

from app.models.sales import CategoryPopularity, SalesRequest, ProductMeta

import random
import math
from datetime import datetime, timedelta
from typing import Any, Dict, List


def generate_timestamp(hours_ago: int) -> str:
    """
    Generate an ISO formatted timestamp for a given number of hours ago.

    Args:
        hours_ago (int): The number of hours ago for which to generate the timestamp.

    Returns:
        str: The ISO formatted timestamp.
    """
    now = datetime.utcnow()
    return (now - timedelta(hours=hours_ago)).isoformat()


def calculate_popularity_factor(category_popularity: float, rating: float) -> float:
    """
    Calculate the popularity factor based on category popularity, rating, and a random device popularity multiplier.

    Args:
        category_popularity (float): The popularity of the product category, ranging from 0 to 1.
        rating (float): The rating of the product, ranging from 3.0 to 5.0.

    Returns:
        float: The computed popularity factor.
    """
    device_popularity = random.uniform(0.9, 1.1)  # reduced range for stability
    return category_popularity * (rating / 5) * device_popularity


def determine_price(product: Any) -> float:
    """
    Determine the price of a product based on its pricing strategy.

    Args:
        product (Any): The product object containing price strategy and pricing details.

    Returns:
        float: The determined price for the product.
    """
    if product.price_strategy == "aggressive":
        return round(random.uniform(product.min_price, product.max_price), 2)
    elif product.price_strategy == "moderate":
        price = round(
            random.gauss(
                product.base_price, (product.max_price - product.min_price) / 6
            ),
            2,
        )
        return max(product.min_price, min(price, product.max_price))
    else:
        return round(random.uniform(product.min_price, product.max_price), 2)


def assign_initial_base_views(products: List[ProductMeta]) -> Dict[str, int]:
    """
    Assigns an initial base view count to each product.

    Args:
        products (List[Any]): The list of products.

    Returns:
        Dict[str, int]: A dictionary mapping product_id to its initial base views.
    """
    base_views_map = {}
    for product in products:
        base_views_map[product.product_id] = random.randint(20_000, 50_000)
    return base_views_map


def calculate_views(
    product_id: str,
    base_views_map: Dict[str, int],
    popularity_factor: float,
    timestamp: str,
) -> int:
    """
    Calculate the number of views for a product based on its initial base, popularity, and time of day.

    Args:
        product_id (str): The ID of the product.
        base_views_map (Dict[str, int]): The stored base views for each product.
        popularity_factor (float): The computed popularity factor.
        timestamp (str): The ISO timestamp.

    Returns:
        int: The estimated number of views.
    """
    hour = datetime.fromisoformat(timestamp).hour
    base_views = base_views_map.get(product_id, 30_000)

    if 0 <= hour < 6:
        time_factor = 0.3
    elif 6 <= hour < 10:
        time_factor = 0.7
    elif 10 <= hour < 18:
        time_factor = 1.2
    else:
        time_factor = 0.7

    adjusted_views = base_views * popularity_factor * time_factor

    return max(5_000, int(adjusted_views))


def calculate_cart_adds(views: int, rating: float) -> int:
    """
    Calculate the number of times a product is added to the cart based on views and rating.

    Args:
        views (int): The number of views the product received.
        rating (float): The rating of the product.

    Returns:
        int: The estimated number of cart additions.
    """
    return max(1, int(views * random.uniform(0.02, 0.08) * (rating / 5)))


def calculate_purchases(cart_adds: int, price: float, product: ProductMeta) -> int:
    """
    Calculate the number of purchases based on cart additions, price sensitivity, and demand factor.

    Args:
        cart_adds (int): The number of times the product was added to the cart.
        price (float): The current price of the product.
        product (Any): The product object containing price sensitivity details.

    Returns:
        int: The estimated number of purchases.
    """
    price_sensitivity = max(1e-6, (product.max_price - product.min_price) / 3)
    price_diff = (price - product.base_price) / price_sensitivity
    demand_factor = 1 / (1 + math.exp(3.0 * price_diff))
    conversion_rate = random.uniform(0.05, 0.25) * demand_factor
    return max(1, int(cart_adds * conversion_rate))


_rating_memory: Dict[str, float] = {}


def generate_sales_data(data: SalesRequest) -> List[Dict[str, Any]]:
    """
    Generate sales data for a given dataset containing multiple products.

    Args:
        data (SalesRequest): The request data containing the number of hours and product details.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing sales data for each product.
    """
    sales_data = []
    base_views_map = assign_initial_base_views(data.products)

    for index in range(data.hours):
        timestamp = generate_timestamp(index)

        for product in data.products:
            if product.product_id not in _rating_memory:
                if hasattr(product, "base_rating") and product.base_rating:
                    _rating_memory[product.product_id] = round(
                        min(5.0, max(3.0, product.base_rating)), 1
                    )
                else:
                    _rating_memory[product.product_id] = round(
                        random.uniform(3.5, 4.5), 1
                    )

            if random.random() < 0.1:
                delta = random.uniform(-0.1, 0.1)
                new_rating = _rating_memory[product.product_id] + delta
                _rating_memory[product.product_id] = round(
                    min(5.0, max(3.0, new_rating)), 1
                )

            rating = _rating_memory[product.product_id]

            category_popularity = (
                float(CategoryPopularity[product.category.name].value) / 5
            )
            popularity_factor = calculate_popularity_factor(category_popularity, rating)
            price = determine_price(product)
            views = calculate_views(
                product.product_id, base_views_map, popularity_factor, timestamp
            )
            cart_adds = calculate_cart_adds(views, rating)
            purchases = calculate_purchases(cart_adds, price, product)

            sales_data.append(
                {
                    "timestamp": timestamp,
                    "product_id": product.product_id,
                    "product_name": product.product_name,
                    "product_image": product.product_image,
                    "category": product.category,
                    "current_price": price,
                    "views": views,
                    "cart_adds": cart_adds,
                    "purchases": purchases,
                    "rating": rating,
                }
            )

    return sales_data
