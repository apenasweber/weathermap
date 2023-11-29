from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    JWT_ALGORITHM: str
    OPEN_WEATHER_API_KEY: str
    OPEN_WEATHER_MAPS_FORECAST_URL: str
    API_PORT: int
    MONGO_URL: str
    MONGO_DB_NAME: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
