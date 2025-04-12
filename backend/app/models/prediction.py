"""

 Copyright 2025 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from pydantic import BaseModel, Field
from enum import Enum

from app.models.common import ReadResponse


class PredictionTimeOfDay(str, Enum):
    """
    Enum for time of day buckets.
    """

    overnight = "Overnight"
    morning = "Morning"
    afternoon = "Afternoon"
    evening = "Evening"


class PredictionData(BaseModel):
    """
    Model for the prediction data.
    """

    purchases: int
    purchases_explain: dict


class PredictionRequest(BaseModel):
    """
    Model for the prediction request data.
    """

    product_id: str
    time_of_day_bucket: PredictionTimeOfDay
    price: float = Field(..., gt=0, description="Price of the product")


class PredictionResponse(ReadResponse[PredictionData]):
    """
    Model for the prediction response data.
    """

    pass
