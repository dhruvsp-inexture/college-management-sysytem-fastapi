from typing import List

from dotenv import load_dotenv, find_dotenv
from pydantic import BaseSettings

load_dotenv(find_dotenv())


class JWTConfig(BaseSettings):

    # JWT Token configuration
    ACCESS_TOKEN_EXPIRE_TIME_MINUTES: int
    REFRESH_TOKEN_EXPIRE_TIME_HOURS: int

    JWT_ALGORITHM: str
    AUTHJWT_HEADER_TYPE: str
    authjwt_secret_key: str
    # Configure algorithms which is permitted
    AUTHJWT_DECODE_ALGORITHMS: List

    class Config:
        env_file = '.env'  # set the env file path.
        env_file_encoding = 'utf-8'
