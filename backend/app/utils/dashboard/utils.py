"""

 Copyright 2025 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from app.utils.data.data_source import DataStore

from app.utils.dashboard.queries import (
    DASHBOARD_SUMMARY_QUERY,
    DASHBOARD_GRAPH_QUERY,
    DASHBOARD_CATEGORY_QUERY,
    DASHBOARD_HOT_PRODUCTS_QUERY,
)

data_store = DataStore()


def get_dashboard_data() -> dict:
    """
    Fetches the dashboard data from the database.

    Returns:
        dict: A dictionary containing the dashboard data.
    """

    summary_data = data_store.execute_query(DASHBOARD_SUMMARY_QUERY, mode="retrieve")[
        "response"
    ]
    graph_data = data_store.execute_query(DASHBOARD_GRAPH_QUERY, mode="retrieve")[
        "response"
    ]
    category_data = data_store.execute_query(DASHBOARD_CATEGORY_QUERY, mode="retrieve")[
        "response"
    ]
    hot_products_data = data_store.execute_query(
        DASHBOARD_HOT_PRODUCTS_QUERY, mode="retrieve"
    )["response"]

    return {
        "summary": summary_data,
        "graph": graph_data,
        "category": category_data,
        "hot_products": hot_products_data,
    }
