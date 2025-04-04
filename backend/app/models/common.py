"""

 Copyright 2025 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from typing import Optional, Any, TypeVar, Generic
from pydantic import BaseModel, Field
from enum import Enum

T = TypeVar("T", bound=BaseModel)


class Status(str, Enum):
    """
    Enum class for status
    """

    success = "SUCCESS"
    error = "FAILURE"


class MetaData(BaseModel):
    """
    Metadata class
    """

    page: int = Field(..., description="The current page number.")
    limit: int = Field(..., description="The limit for the number of items to return.")
    total: int = Field(..., description="The total number of items.")


class ListData(BaseModel, Generic[T]):
    """
    List data class
    """

    results: list[T] = Field(..., description="The list of items.")
    meta: MetaData = Field(..., description="The metadata for the list.")


class BaseResponse(BaseModel, Generic[T]):
    """
    Generic response class
    """

    status: Status = Field(Status.success, description="The status of the response.")
    message: Optional[str] = Field(None, description="The message for the response.")
    data: Optional[T] = Field(None, description="The data for the response.")
    errors: Optional[Any] = Field(None, description="The errors for the response.")


class CreateResponse(BaseResponse[T]):
    """
    Create response class
    """

    data: T


class ReadResponse(BaseResponse[T]):
    """
    Read response class
    """

    data: T


class ListResponse(BaseResponse[ListData[T]]):
    """
    List response class
    """

    data: ListData[T]


class UpdateResponse(BaseResponse[T]):
    """
    Update response class
    """

    data: T


class DeleteResponse(BaseResponse[T]):
    """
    Delete response class
    """

    data: T
