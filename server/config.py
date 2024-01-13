from pydantic import BaseSettings


class Settings(BaseSettings):
    env: str = 'dev'
    debug: bool = True
    rapid_api_secret: str | None = None
