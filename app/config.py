"""Configuration centralisée de l'application, chargée depuis les variables d'environnement."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./coaching.db"
    secret_key: str = "change-me-to-a-long-random-string"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    food_recognition_api_key: str = ""
    food_recognition_provider: str = "mock"
    allowed_origins: str = "http://localhost:5173"
    @property
    def allowed_origins_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]


    class Config:
        env_file = ".env"


settings = Settings()
