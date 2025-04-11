"""

 Copyright 2025 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from psycopg import connect
from app.utils.settings.config import settings

import logging

logger = logging.getLogger("api-logger")


class DataStore:
    """
    DataStore class to manage the connection to the database and the internal table.
    """

    def __init__(self):
        self.connection = None
        self._create_connection()

    def __del__(self):
        self._close_connection()

    def _create_connection(self):
        """
        Create a connection to the database
        """
        logger.info("Attempting to connect to the database...")
        try:
            self.connection = connect(
                dbname=settings.DB_NAME,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                host=settings.DB_HOST,
                port=settings.DB_PORT,
            )
            self.connection.autocommit = True
            logger.info("DataStore Connection Established!")

        except Exception as e:
            logger.exception(f"DataStore set-up failed: {e}")
            raise e

    def _close_connection(self):
        """
        Close the connection to the database
        """
        if self.connection:
            self.connection.close()
            logger.info("DataStore Connection Closed!")

    def execute_query(self, query, params=(), mode="submit") -> dict:
        """
        Execute a SQL query using a cursor, with error handling and cleanup.
        """
        response = None
        if not self.connection:
            raise RuntimeError("No database connection defined!")
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            if mode == "retrieve":
                response = [
                    dict(zip([column[0] for column in cursor.description], row))
                    for row in cursor.fetchall()
                ]
            rows_affected = cursor.rowcount
            cursor.close()

        except Exception as e:
            logger.exception(f"Query execution failed: {e}")
            raise e

        return {
            "rows_affected": rows_affected,
            "response": response,
        }
