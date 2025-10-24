from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    FLASK_ENV: str = "DEVELOPMENT"
    LOG_LEVEL: str = "DEBUG"
    DATABASE_URL: str = "sqlite:///./test.db"
    SCHEDULER_ENABLED: bool = False

    class Config:
        env_file = ".env" # Load environment variables from a .env file

settings = Settings()