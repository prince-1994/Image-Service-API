from pydantic import BaseSettings


class Settings(BaseSettings):
    env: str
    debug: bool
    rapid_api_secret: str
