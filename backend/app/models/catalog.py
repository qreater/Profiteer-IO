"""

 Copyright 2025 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from pydantic import BaseModel, Field, HttpUrl

from typing import List, Dict

from app.models.common import ReadResponse
from app.models.sales import ProductCategory


class ProductData(BaseModel):
    """
    Product data model.
    """

    product_id: str
    product_name: str
    product_image: HttpUrl
    average_rating: float
    revenue: float


class ProductExtension(ProductData):
    """
    Product extension model.
    """

    category: ProductCategory
    base_price: float
    total_purchases: int
    total_views: int
    total_cart_adds: int


class ProductGraphItem(BaseModel):
    """
    Product graph item model.
    """

    timestamp: str
    views: int
    cart_adds: int
    purchases: int


class ProductSpecifics(BaseModel):
    """
    Product specifics model.
    """

    details: ProductExtension
    graph: List[ProductGraphItem]


class ProductResponse(ReadResponse[ProductSpecifics]):
    """
    Product response model.
    """

    pass


class ProductListResponse(ReadResponse[Dict[ProductCategory, List[ProductData]]]):
    """
    Product list response model.
    """

    pass
