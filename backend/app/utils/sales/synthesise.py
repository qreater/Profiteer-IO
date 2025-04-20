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


def generate_timestamp(hour_offset: int) -> str:
    """
    Generate a timestamp in ISO format based on the current time and an hour offset.

    Args:
        hour_offset (int): The number of hours to offset from the current time.

    Returns:
        str: The ISO formatted timestamp.
    """
    base = datetime.now().replace(
        hour=0, minute=0, second=0, microsecond=0
    ) - timedelta(days=2)
    timestamp = base + timedelta(hours=hour_offset)
    return timestamp.isoformat()


def calculate_popularity_factor(category_popularity: float, rating: float) -> float:
    """
    Calculate the popularity factor based on category popularity, rating, and device popularity.

    Args:
        category_popularity (float): The popularity of the product category, ranging from 0 to 1.
        rating (float): The rating of the product, ranging from 2.0 to 5.0.

    Returns:
        float: The computed popularity factor.
    """
    device_popularity = random.uniform(0.95, 1.05) * category_popularity
    rating_factor = ((rating - 2) / 3) ** 0.9 * 1.8
    return category_popularity * rating_factor * device_popularity


def determine_price(product: Any) -> float:
    """
    Determine the price of a product based on its pricing strategy.

    Args:
        product (Any): The product object containing price strategy and pricing details.

    Returns:
        float: The determined price for the product.
    """
    if product.price_strategy == "aggressive":
        price = random.uniform(product.base_price * 0.85, product.base_price * 1.05)
        return round(max(product.min_price, min(product.max_price, price)), 2)
    elif product.price_strategy == "moderate":
        std_dev = product.base_price * 0.05
        price = random.gauss(product.base_price, std_dev)
        return round(max(product.min_price, min(product.max_price, price)), 2)
    else:
        price = random.uniform(product.base_price * 0.9, product.base_price * 1.1)
        return round(max(product.min_price, min(product.max_price, price)), 2)


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
        base_views_map[product.product_id] = random.randint(8_000, 12_000)
    return base_views_map


def get_time_of_day_bucket(hour: int) -> str:
    """
    Get the time of day bucket based on the hour.

    Args:
        hour (int): The hour of the day (0-23).

    Returns:
        str: The time of day bucket ("Overnight", "Morning", "Afternoon", "Evening").
    """

    if 22 <= hour or hour < 6:
        return "Overnight"
    elif 6 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 18:
        return "Afternoon"
    else:
        return "Evening"


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
    base_views = base_views_map.get(product_id, 10_000)

    time_of_day_bucket = get_time_of_day_bucket(hour)

    if time_of_day_bucket == "Overnight":
        time_factor = 0.5
    elif time_of_day_bucket == "Morning":
        time_factor = 0.8
    elif time_of_day_bucket == "Afternoon":
        time_factor = 1.5
    else:
        time_factor = 1.0

    adjusted_views = base_views * popularity_factor * time_factor

    return max(100, int(adjusted_views))


def calculate_cart_adds(views: int, rating: float) -> int:
    """
    Calculate the number of cart additions based on views and rating.

    Args:
        views (int): The number of views the product received.
        rating (float): The rating of the product.

    Returns:
        int: The estimated number of cart additions.
    """
    rating_factor = ((rating - 2) / 3) ** 0.9 * 1.8
    conversion_rate = random.uniform(0.045, 0.055) * rating_factor

    return max(1, int(views * conversion_rate))


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
    price_sensitivity = product.base_price * 0.1
    price_diff = (price - product.base_price) / price_sensitivity
    demand_factor = 1 / (1 + math.exp(2.0 * price_diff))
    conversion_rate = random.uniform(0.16, 0.19) * demand_factor
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
                        min(5.0, max(2.0, product.base_rating)), 1
                    )
                else:
                    _rating_memory[product.product_id] = round(
                        random.uniform(2.0, 5), 1
                    )

            if random.random() < 0.1:
                delta = random.uniform(-0.2, 0.2)
                new_rating = _rating_memory[product.product_id] + delta
                _rating_memory[product.product_id] = round(
                    min(5.0, max(2.0, new_rating)), 1
                )

            rating = _rating_memory[product.product_id]

            category_popularity = float(CategoryPopularity[product.category.name].value)
            popularity_factor = calculate_popularity_factor(category_popularity, rating)
            price = determine_price(product)
            views = calculate_views(
                product.product_id, base_views_map, popularity_factor, timestamp
            )
            cart_adds = calculate_cart_adds(views, rating)
            purchases = calculate_purchases(cart_adds, price, product)
            hour = datetime.fromisoformat(timestamp).hour
            time_of_day_bucket = get_time_of_day_bucket(hour)

            sales_data.append(
                {
                    "timestamp": timestamp,
                    "product_id": product.product_id,
                    "product_name": product.product_name,
                    "product_image": product.product_image,
                    "category": product.category,
                    "category_popularity": category_popularity,
                    "base_price": product.base_price,
                    "current_price": price,
                    "price_strategy": product.price_strategy,
                    "popularity_factor": round(popularity_factor, 2),
                    "time_of_day_bucket": time_of_day_bucket,
                    "views": views,
                    "cart_adds": cart_adds,
                    "purchases": purchases,
                    "rating": rating,
                }
            )

    return sales_data
