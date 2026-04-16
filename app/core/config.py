from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "OunceAI"
    APP_VERSION: str = "2.0.0"
    
    # PostgreSQL (Supabase ou Local)
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    
    # MongoDB
    MONGO_URL: str
    MONGO_DB_NAME: str = "Oncinha"
    
    # APIs Externas
    GROQ_API_KEY: str
    GEMINI_KEY: str
    WEATHER_KEY: str
    
    # Configuração do arquivo .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

# Instância global para ser usada em todo o projeto
settings = Settings()