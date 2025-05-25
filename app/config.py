from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # Ton token API Nuclia (défini en variable d’environnement NUCLIA_API_TOKEN)
    nuclia_api_token: str = Field(..., env="NUCLIA_API_TOKEN")
    # Zone ou dataset Nuclia si nécessaire
    nuclia_zone_id: str = Field(..., env="NUCLIA_ZONE_ID")
    # URL de base de l’API Nuclia
    nuclia_base_url: str = Field(..., env="NUCLIA_BASE_URL")
    # URL Nuclia Complet
    nuclia_url: str = Field(..., env="NUCLIA_URL")
    # KB ID
    nuclia_base_url_general: str = Field(..., env="NUCLIA_BASE_URL_GENERAL")
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
