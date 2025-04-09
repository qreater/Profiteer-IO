"""

 Copyright 2025 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from pydantic import BaseModel, Field, ConfigDict
from enum import Enum

from app.models.common import ListResponse


class ProductCategory(str, Enum):
    """
    Enum for product categories.
    """

    LAPTOPS = "Laptops"
    PC = "Pre-Built PC"
    CONSOLES = "Consoles"


class CategoryPopularity(str, Enum):
    """
    Enum for category popularity.
    """

    LAPTOPS = 1.1
    PC = 1.0
    CONSOLES = 0.9
    DEFAULT = 1.0


class ProductPriceStrategy(str, Enum):
    """
    Enum for product price strategies.
    """

    AGGRESSIVE = "aggressive"
    MODERATE = "moderate"
    RANDOM = "random"


class ProductBase(BaseModel):
    """
    Base model for product data.
    """

    product_id: str
    product_name: str
    product_image: str
    category: ProductCategory

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "product_id": "P001",
                "product_name": "SafariBook Lite",
                "product_image": "./images/laptop.png",
                "category": "Laptops",
            }
        }
    )


class ProductMeta(ProductBase):
    """
    Model for product metadata.
    """

    base_price: float
    base_rating: float = Field(4.2, ge=2.0, le=5.0)
    price_strategy: ProductPriceStrategy = ProductPriceStrategy.RANDOM
    min_price: float
    max_price: float

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                **ProductBase.model_config["json_schema_extra"]["example"],
                "base_price": 999.99,
                "base_rating": 4.2,
                "price_strategy": "random",
                "min_price": 899.99,
                "max_price": 1099.99,
            }
        }
    )


class ProductSales(ProductBase):
    """
    Model for product sales data.
    """

    category_popularity: float
    rating: float
    base_price: float
    current_price: float
    price_strategy: ProductPriceStrategy
    popularity_factor: float
    time_of_day_bucket: str
    timestamp: str
    views: int
    cart_adds: int
    purchases: int


class SalesRequest(BaseModel):
    """
    Model for sales request data.
    """

    hours: int = 24
    products: list[ProductMeta] = Field(default_factory=list)


class SalesResponse(ListResponse[ProductSales]):
    """
    Model for sales response data.
    """

    pass
