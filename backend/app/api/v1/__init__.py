"""

 Copyright 2025 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from fastapi import APIRouter, Depends

from app.api.v1.sales import router as sales_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.catalog import router as catalog_router
from app.api.v1.prediction import router as prediction_router

from app.utils.auth.middlewares import check_api_key

api_router = APIRouter()

api_router.include_router(
    sales_router,
    prefix="/sales",
    tags=["Sales"],
    dependencies=[Depends(check_api_key)],
)

api_router.include_router(
    dashboard_router,
    prefix="/dashboard",
    tags=["Dashboard"],
    dependencies=[Depends(check_api_key)],
)

api_router.include_router(
    catalog_router,
    prefix="/catalog",
    tags=["Catalog"],
    dependencies=[Depends(check_api_key)],
)

api_router.include_router(
    prediction_router,
    prefix="/prediction",
    tags=["Prediction"],
    dependencies=[Depends(check_api_key)],
)
