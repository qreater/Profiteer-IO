"""

 Copyright 2025 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

import logging
import logging.config

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.utils.exceptions.errors import APIError
from app.utils.exceptions.logger import get_log_config
from app.utils.exceptions.handler import ErrorHandlingMiddleware, api_error_handler

from app.api.v1 import api_router as api_router_v1

app = FastAPI(
    title="Profiteer API",
    description="Profiteer API for managing AI Sales Predictions",
    version="1.0.0",
)

logging.config.dictConfig(get_log_config())

app.mount("/cdn-assets/", StaticFiles(directory="app/static/"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(APIError, api_error_handler)
app.add_middleware(ErrorHandlingMiddleware)
app.include_router(api_router_v1, prefix="/api/v1")


@app.get("/")
@app.get("/health")
@app.get("/readiness-probe")
def health_check():
    """
    Health check, Welcomes a user to the API
    """
    return {"message": "Welcome to Profiteer.IO API"}
