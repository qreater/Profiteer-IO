"""

 Copyright 2025 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

import time
from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from logging import getLogger

from app.models.common import BaseResponse, Status

from app.utils.exceptions.errors import APIError, handle_exception
from app.utils.exceptions.logger import logger_utility

logger = getLogger("api-logger")


async def api_response_handler(request: Request, response: dict):
    """
    Custom response handler for JSONResponse

    -- Parameters
    request: Request
        The request object.

    response: dict
        The response dictionary.

    -- Returns
    JSONResponse
        The response for the JSONResponse object.
    """
    response = JSONResponse(
        status_code=status.HTTP_200_OK,
        content=response,
        headers={
            "X-Request-ID": request.state.request_id,
            "X-Correlation-ID": request.state.correlation_id,
        },
    )

    return response


async def api_error_handler(request: Request, exc: APIError):
    """
    Custom exception handler for APIError

    -- Parameters
    request: Request
        The request object.

    exc: APIError
        The APIError exception.

    -- Returns
    JSONResponse
        The response for the APIError exception.
    """
    request.state.traceback = exc.detail

    response = BaseResponse(
        status=Status.error,
        errors=exc.detail,
    ).model_dump(exclude_none=True)

    return JSONResponse(
        status_code=exc.status_code,
        content=response,
        headers={
            "X-Request-ID": request.state.request_id,
            "X-Correlation-ID": request.state.correlation_id,
        },
    )


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """
        Middleware to handle exceptions and return a JSON response with the error message.

        -- Parameters
        request: Request
            The request object.
        call_next: Callable
            The next function to call.
        """
        headers = request.headers
        request.state.request_id = headers.get("X-Request-ID", "N/A")
        request.state.correlation_id = headers.get("X-Correlation-ID", "N/A")

        try:
            start_time = time.perf_counter_ns()

            response = await call_next(request)

            response.headers["X-Request-ID"] = request.state.request_id
            response.headers["X-Correlation-ID"] = request.state.correlation_id

            return response

        except Exception as e:
            error = handle_exception(e)

            request.state.traceback = error.detail
            logger.exception(f"Unhandled Exception: {str(e)}", exc_info=True)

            return self.json_response(
                Status.error,
                error.status_code,
                error.detail,
                request.state.request_id,
                request.state.correlation_id,
            )
        finally:
            end_time = time.perf_counter_ns()
            status_code = (
                getattr(response, "status_code", 500) if "response" in locals() else 500
            )

            logger_utility.log(
                request_id=request.state.request_id,
                correlation_id=request.state.correlation_id,
                request={
                    "method": request.method,
                    "path": request.url.path,
                    "query": dict(request.query_params),
                },
                response={
                    "status": status_code,
                    "traceback": (
                        request.state.traceback
                        if hasattr(request.state, "traceback")
                        else None
                    ),
                },
                duration_ms=(end_time - start_time) / 1_000_000,
            )

    def json_response(
        self,
        status: str,
        status_code: int,
        detail: str,
        request_id: str,
        correlation_id: str,
    ):
        """
        Return a JSON response with the error message and set custom headers.

        -- Parameters
        status_code: int
            The status code for the error.
        detail: str
            The error message.
        request_id: str
            The request ID from the headers.
        correlation_id: str
            The correlation ID from the headers.
        """
        headers = {
            "X-Request-ID": request_id,
            "X-Correlation-ID": correlation_id,
        }

        response = BaseResponse(
            status=status,
            errors=detail,
        ).model_dump(exclude_none=True)

        return JSONResponse(
            status_code=status_code,
            content=response,
            headers=headers,
        )
