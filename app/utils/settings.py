from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///weather.db"
    ALEMBIC_DATABASE_URL: str = "sqlite:///weather.db"

    SECRET_KEY: str = "dc5c4065eaf6b91d19f29709932e896e89f8d4762630e8f2b2e95fdf2d890d3c"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
