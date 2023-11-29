from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    SECRET_KEY: str
    JWT_ALGORITHM: str
    DATABASE_URL: str
    OPEN_WEATHER_API_KEY: str
    OPEN_WEATHER_MAPS_FORECAST_URL = str
    API_PORT: int

    class Config:
        env_file = ".env"


settings = Settings()
