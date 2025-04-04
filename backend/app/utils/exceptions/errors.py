"""

 Copyright 2025 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from fastapi import HTTPException, status


class APIError(HTTPException):
    """
    APIError class for handling exceptions.

    -- Parameters
    status_code: int
        The status code for the error.
    error_type: str
        The type of error.
    detail: str
        The detail for the error.
    """

    def __init__(self, status_code: int, error_type: str, detail: str):
        error_detail = {"type": error_type, "msg": detail}
        super().__init__(status_code=status_code, detail=[error_detail])


def handle_exception(
    e: Exception,
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    error_type: str = "server_error",
):
    """
    Handle exceptions and return an APIError object.

    -- Parameters
    e: Exception
        The exception to handle.
    status_code: int
        The status code for the error.
    error_type: str
        The type of error.
    """

    error_detail = f"Internal Server Error: {str(e)}"
    return APIError(status_code=status_code, error_type=error_type, detail=error_detail)


def conflict_error(entity: str, key: str):
    """
    Return a conflict error.

    -- Parameters
    entity: str
        The entity causing the conflict.
    key: str
        The key causing the conflict.
    """

    return APIError(
        status_code=status.HTTP_409_CONFLICT,
        error_type="conflict_error",
        detail=f"{entity.capitalize()} already exists with '{key}'!",
    )


def not_found_error(entity: str, key: str):
    """
    Return a not found error.

    -- Parameters
    field: str
        The field that was not found.
    """
    return APIError(
        status_code=status.HTTP_404_NOT_FOUND,
        error_type="not_found_error",
        detail=f"{entity.capitalize()} not found with '{key}'!",
    )


def validation_error(field: str, extra_info: str = ""):
    """
    Return a validation error.

    -- Parameters
    field: str
        The field that was not valid.
    """

    return APIError(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error_type="validation_error",
        detail=f"Invalid {field.capitalize()}! {extra_info}",
    )


def unauthorized_error():
    """
    Return an unauthorized error.
    """

    return APIError(
        status_code=status.HTTP_401_UNAUTHORIZED,
        error_type="unauthorized_error",
        detail="Please provide a valid API key.",
    )
