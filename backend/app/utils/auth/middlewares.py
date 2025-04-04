"""

 Copyright 2025 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

import secrets

from fastapi import Security

from app.utils.settings.config import settings
from app.utils.exceptions.errors import unauthorized_error

from fastapi.security import APIKeyHeader

request_api_key = APIKeyHeader(name="Authorization", scheme_name="Bearer")


def check_api_key(api_key=Security(request_api_key)):
    """
    Check if the API key is valid

    -- Parameters
    api_key: str
        The API key to validate

    -- Raises
    HTTPException: 401
        If the API key is incorrect
    """

    correct_api_key = secrets.compare_digest(api_key, settings.API_KEY)
    if not correct_api_key:
        raise unauthorized_error()
