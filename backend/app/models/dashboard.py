"""

 Copyright 2025 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from typing import List

from app.models.common import ReadResponse


class SummaryItem(BaseModel):
    """
    Summary item model for the dashboard.
    """

    date: datetime = Field(..., alias="day_2_date")
    revenue: float = Field(..., alias="revenue_day_2")
    revenue_change_pct: float = Field(..., alias="revenue_percent_change")
    items: int = Field(..., alias="items_day_2")
    items_change_pct: float = Field(..., alias="items_percent_change")
    conversion_rate: float = Field(..., alias="conversion_rate_day_2")
    conversion_rate_change_pct: float = Field(
        ..., alias="conversion_rate_percent_change"
    )
    top_category: str = Field(..., alias="top_category_day_2")


class GraphItem(BaseModel):
    """
    Graph item model for the dashboard.
    """

    timestamp: datetime
    total_views: int
    total_cart_adds: int
    total_purchases: int


class CategoryItem(BaseModel):
    """
    Category item model for the dashboard.
    """

    name: str = Field(..., alias="category")
    revenue: float = Field(..., alias="revenue_day_2")
    has_increased: bool


class HotProductItem(BaseModel):
    """
    Hot product item model for the dashboard.
    """

    id: str = Field(..., alias="product_id")
    name: str = Field(..., alias="product_name")
    image: HttpUrl = Field(..., alias="product_image")
    revenue: float = Field(..., alias="total_revenue")
    category: str = Field(...)


class DashboardData(BaseModel):
    """
    Dashboard data model for the API.
    """

    summary: List[SummaryItem]
    graph: List[GraphItem]
    category: List[CategoryItem]
    hot_products: List[HotProductItem]


class DashboardResponse(ReadResponse[DashboardData]):
    """
    Dashboard response model for the API.
    """

    pass
