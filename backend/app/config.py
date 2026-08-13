from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "OPDAI"
    environment: str = "development"
    secret_key: str = "change-this-secret-key"
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 60
    database_url: str = "sqlite:///./opdai.db"
    upload_dir: str = "./uploads"
    max_upload_mb: int = 10
    allowed_extensions: str = "pdf,png,jpg,jpeg"
    openai_api_key: str = ""
    openai_model: str = "gpt-5"
    cors_origins: str = "http://localhost:8501"
    doctor_email: str = "doctor@example.com"
    doctor_password: str = "ChangeMe123!"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def allowed_extension_set(self):
        return {x.strip().lower() for x in self.allowed_extensions.split(",") if x.strip()}

@lru_cache
def get_settings():
    return Settings()
