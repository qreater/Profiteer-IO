"""

 Copyright 2025 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""
from fastapi import APIRouter, status

from app.utils.prediction.utils import predict_product_purchases
from app.models.prediction import PredictionRequest, PredictionResponse


router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=PredictionResponse,
    response_model_exclude_none=True,
)
def predict_purchases(prediction_parameters: PredictionRequest):
    """
    Predicts the purchases with given data.

    Args:
        prediction_parameters (PredictionRequest): The request data containing the parameters for prediction.

    Returns:
        PredictionResponse: A response model containing the prediction data.
    """
    purchases = predict_product_purchases(
        product_id=prediction_parameters.product_id,
        time_of_day_bucket=prediction_parameters.time_of_day_bucket,
        price=prediction_parameters.price,
    )
    return {"message": "Predicted Product Purchases Successfuly.", "data": purchases}
