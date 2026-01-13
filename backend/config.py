from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: Optional[str] = None
    
    # Auth
    JWT_SECRET: str
    JWT_EXPIRES_IN: int = 3600
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    OAUTH_REDIRECT_URI: str
    
    # Frontend
    CORS_ORIGINS: str = "http://localhost:3000"
    
    # Observability
    SENTRY_DSN: Optional[str] = None
    PROMETHEUS_ENABLED: bool = True
    
    # Notifications (Twilio)
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_FROM: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
