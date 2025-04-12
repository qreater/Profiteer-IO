"""

 Copyright 2025 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

import mindsdb_sdk
import json

from app.utils.settings.config import settings
from app.utils.data.data_source import DataStore

from app.utils.exceptions.errors import not_found_error

from app.utils.prediction.queries import (
    PRODUCT_SCENARIO_METRICS_QUERY,
)

data_store = DataStore()

mdb = mindsdb_sdk.connect(settings.MINDSDB_URL)


def predict_product_purchases(
    product_id: str, time_of_day_bucket: str, price: float
) -> dict:
    """
    Predicts product purchases based on the given parameters using MindsDB.

    Args:
        product_id (str): The ID of the product.
        time_of_day_bucket (str): The time of day bucket.
        price (float): The current price of the product.

    Returns:
        dict: A dictionary containing the predicted purchases and other details.
    """

    product_metrics = data_store.execute_query(
        PRODUCT_SCENARIO_METRICS_QUERY,
        params=(price, product_id, time_of_day_bucket),
        mode="retrieve",
    )["response"][0]

    if product_metrics.get("views") is None or product_metrics.get("cart_adds") is None:
        raise not_found_error("Product", product_id)

    prediction_params = {
        "input_views": float(product_metrics["views"]),
        "cart_adds": float(product_metrics["cart_adds"]),
        "price_ratio": float(product_metrics["price_ratio"]),
        "popularity_factor": float(product_metrics["popularity_factor"]),
    }

    prediction_result = mdb.models.sales_forecast.predict(prediction_params)
    flat_result = prediction_result.to_dict(orient="records")[0]

    purchases = flat_result["purchases"]
    purchases_explain = flat_result["purchases_explain"]

    return {
        "purchases": purchases,
        "purchases_explain": json.loads(purchases_explain),
    }
