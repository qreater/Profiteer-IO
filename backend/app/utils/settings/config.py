"""

 Copyright 2025 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings class to store the configuration values

    -- Parameters
    API_KEY: str
        The API key to access the API.
    """

    API_KEY: str = "OPEN_SESAME"


settings = Settings()
