"""

 Copyright 2025 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

import json
import logging

logger = logging.getLogger("api-logger")


class LoggerUtility:
    """
    Logger Utility to standardize log format and include additional information.
    """

    def log(
        self,
        request_id,
        correlation_id,
        request,
        response,
        duration_ms,
        extras=None,
    ):
        log_data = {
            "request_id": request_id,
            "correlation_id": correlation_id,
            "request": request,
            "response": response,
            "duration_ms": f"{duration_ms}ms",
            "extras": extras,
        }

        logger.info("API Log: %s", json.dumps(log_data))


def get_log_config():
    """
    Return a logging configuration for the application.
    """
    return {
        "version": 1,
        "formatters": {
            "detailed": {
                "format": "%(asctime)s | %(levelname)s | %(name)s | "
                "[%(filename)s:%(lineno)d] | %(message)s",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "detailed",
                "stream": "ext://sys.stdout",
            }
        },
        "loggers": {
            "api-logger": {
                "level": "INFO",
                "handlers": ["console"],
                "propagate": False,
            }
        },
        "root": {
            "level": "INFO",
            "handlers": ["console"],
        },
        "disable_existing_loggers": False,
    }


logging.config.dictConfig(get_log_config())
logger_utility = LoggerUtility()
